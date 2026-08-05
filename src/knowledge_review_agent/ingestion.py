from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .index_store import index_entries_by_hash, index_entries_by_path, load_index, save_index, sha256_file
from .metadata import load_metadata, resolve_course
from .models import CourseMetadata, IngestionResult, RepositoryIndexEntry
from .pdf_skill_adapter import ExternalPdfSkillBridge, PdfSkillBridge, PARSER_VERSION
from .concept_filter import discover_pdfs, run_concept_filter


def relative_pdf_path(pdf_path: Path, raw_root: Path) -> str:
    try:
        return pdf_path.relative_to(raw_root).as_posix()
    except ValueError:
        return pdf_path.name


def build_index_entry(
    pdf_path: Path,
    raw_root: Path,
    course: CourseMetadata,
    sha256: str,
    outputs: dict[str, str],
    status: str,
    page_count: int,
) -> RepositoryIndexEntry:
    now = datetime.now(timezone.utc).isoformat()
    relative_path = relative_pdf_path(pdf_path, raw_root)
    lecture_name = pdf_path.stem
    output_location = outputs.get("lecture_dir", "")

    return RepositoryIndexEntry(
        filename=pdf_path.name,
        relative_file_path=relative_path,
        sha256=sha256,
        processing_status=status,
        processing_timestamp=now,
        source_course=course.course_id or course.course_name,
        source_lecture=lecture_name,
        output_location=output_location,
        parser_version=PARSER_VERSION,
        outputs=outputs,
        previous_relative_paths=[],
        last_seen_timestamp=now,
        page_count=page_count,
    )


def run_incremental_ingestion(
    raw_root: Path,
    processed_root: Path,
    index_path: Path,
    metadata_csv: Path,
    skill_bridge: PdfSkillBridge | None = None,
    rebuild_all: bool = False,
    force_course_ids: set[str] | None = None,
) -> IngestionResult:
    metadata_rows = load_metadata(metadata_csv)
    index = load_index(index_path)
    by_path = index_entries_by_path(index)
    by_hash = index_entries_by_hash(index)
    seen_hashes = set(by_hash.keys())
    bridge = skill_bridge or ExternalPdfSkillBridge()
    forced_courses = {str(course_id).strip() for course_id in (force_course_ids or set()) if str(course_id).strip()}

    all_pdfs = discover_pdfs(raw_root)
    changed_pdfs: list[Path] = []
    skipped_entries: list[RepositoryIndexEntry] = []
    processed_now: list[RepositoryIndexEntry] = []

    for pdf_path in all_pdfs:
        rel_path = relative_pdf_path(pdf_path, raw_root)
        current_hash = sha256_file(pdf_path)
        course = resolve_course(pdf_path, raw_root, metadata_rows)
        if course.course_id in forced_courses:
            seen_hashes.add(current_hash)
            changed_pdfs.append(pdf_path)
            continue
        existing_by_path = by_path.get(rel_path)
        existing_by_hash = by_hash.get(current_hash)

        if rebuild_all:
            seen_hashes.add(current_hash)
            changed_pdfs.append(pdf_path)
            continue

        if existing_by_path and existing_by_path.sha256 == current_hash:
            existing_by_path.last_seen_timestamp = datetime.now(timezone.utc).isoformat()
            skipped_entries.append(existing_by_path)
            seen_hashes.add(current_hash)
            continue

        if existing_by_hash and existing_by_hash.relative_file_path != rel_path:
            if rel_path not in existing_by_hash.previous_relative_paths:
                existing_by_hash.previous_relative_paths.append(existing_by_hash.relative_file_path)
            existing_by_hash.relative_file_path = rel_path
            existing_by_hash.filename = pdf_path.name
            existing_by_hash.last_seen_timestamp = datetime.now(timezone.utc).isoformat()
            skipped_entries.append(existing_by_hash)
            seen_hashes.add(current_hash)
            continue

        if current_hash in seen_hashes:
            if existing_by_hash:
                existing_by_hash.last_seen_timestamp = datetime.now(timezone.utc).isoformat()
                skipped_entries.append(existing_by_hash)
            continue

        seen_hashes.add(current_hash)
        changed_pdfs.append(pdf_path)

    if changed_pdfs:
        extractions = run_concept_filter(
            raw_root=raw_root,
            processed_root=processed_root,
            metadata_csv=metadata_csv,
            skill_bridge=bridge,
            pdf_paths=changed_pdfs,
        )
        for result in extractions:
            pdf_path = Path(result["pdf"])
            if not pdf_path.is_absolute():
                # Extractor may return either raw-root-relative paths or paths
                # already rooted at the caller's working directory.
                if not pdf_path.exists():
                    pdf_path = raw_root / pdf_path
            rel_path = relative_pdf_path(pdf_path, raw_root)
            current_hash = sha256_file(pdf_path)
            course = resolve_course(pdf_path, raw_root, metadata_rows)
            entry = build_index_entry(
                pdf_path=pdf_path,
                raw_root=raw_root,
                course=course,
                sha256=current_hash,
                outputs={
                    "lecture_dir": result["lecture_dir"],
                    "lecture_md": result["lecture_md"],
                    "lecture_json": result["lecture_json"],
                },
                status="processed",
                page_count=int(result.get("pages", 0) or 0),
            )
            index.entries = [
                existing
                for existing in index.entries
                if existing.relative_file_path != rel_path and existing.sha256 != current_hash
            ]
            index.entries.append(entry)
            processed_now.append(entry)

    save_index(index, index_path)
    return IngestionResult(
        processed=processed_now,
        skipped=skipped_entries,
        errors=[entry for entry in index.entries if entry.processing_status == "error"],
    )
