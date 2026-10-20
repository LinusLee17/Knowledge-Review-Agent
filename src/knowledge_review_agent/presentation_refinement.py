"""Presentation preparation guarded by exact, source-bound evaluation evidence."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from .concept_document import (
    CANONICAL_SECTION_ORDER, SECTION_ALIASES, format_concept_document,
    assert_presentation_preserved, map_document_links,
)
from .concept_store import concept_history_root
from .quality_gate import (
    GateError, GateSnapshot, require_eligible_report, load_evaluation_report,
    assert_gate_snapshot_current,
)


@dataclass(frozen=True)
class RefinementResult:
    concept_name: str
    source_dir: Path
    refined_dir: Path
    created: bool
    updated: bool


@dataclass
class RefinementReport:
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    concepts_processed: int = 0


def _validate_destination(snapshot: GateSnapshot, refined_root: Path, report_path: Path) -> None:
    source = snapshot.paths.concepts_root.resolve()
    output = refined_root.resolve()
    if refined_root.is_symlink() or output.is_relative_to(source) or source.is_relative_to(output):
        raise GateError("Draft and refined roots must be separate, non-overlapping directories")
    if report_path.resolve().is_relative_to(source) or report_path.resolve().is_relative_to(output):
        raise GateError("Evaluation report must be outside draft and refined roots")
    # Output cannot overwrite any other evaluated source/review/evidence root.
    for root in (snapshot.paths.processed_root, snapshot.paths.reviews_root,
                 concept_history_root(snapshot.paths.concepts_root), *snapshot.paths.asset_roots):
        if output.is_relative_to(root.resolve()) or root.resolve().is_relative_to(output):
            raise GateError("Refined output overlaps evaluated evidence/review inputs")
    for concept in snapshot.concepts:
        for suffix in ("concept.md", "metadata.json"):
            path = refined_root / concept.relative_dir / suffix
            cursor = refined_root
            for part in path.relative_to(refined_root).parts:
                cursor /= part
                if cursor.is_symlink():
                    raise GateError(f"Symlink refined output path: {cursor}")
                if cursor.exists() and cursor != path and not cursor.is_dir():
                    raise GateError(f"Invalid refined output directory: {cursor}")
            if path.exists() and not path.is_file():
                raise GateError(f"Invalid refined output file: {path}")


def _relocate_links(markdown: str, source: Path, output: Path) -> str:
    def rebase(destination):
        url = urlsplit(destination)
        if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
            return destination
        original = (source / unquote(url.path)).resolve()
        relative = os.path.relpath(original, output.resolve()).replace(os.sep, "/")
        return urlunsplit(("", "", quote(relative, safe="/~"), url.query, url.fragment))
    return map_document_links(markdown, rebase)


def _atomic_output(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".refinement-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _prepare_and_publish(snapshot: GateSnapshot, refined_root: Path, report_path: Path, selected=None) -> list[RefinementResult]:
    _validate_destination(snapshot, refined_root, report_path)
    results = []
    prepared = []
    with tempfile.TemporaryDirectory(prefix="knowledge-refinement-") as staging:
        stage = Path(staging)
        for index, concept in enumerate(snapshot.concepts):
            if selected is not None and concept.relative_dir != selected:
                continue
            source = snapshot.paths.concepts_root / concept.relative_dir
            output = refined_root / concept.relative_dir
            original = concept.markdown.decode("utf-8")
            formatted = format_concept_document(original)
            assert_presentation_preserved(original, formatted)
            formatted = _relocate_links(formatted, source, output)
            payloads = {"concept.md": formatted.encode("utf-8"), "metadata.json": concept.metadata}
            created = any(not (output / name).exists() for name in payloads)
            updated = False
            for name, content in payloads.items():
                destination = output / name
                if not destination.exists() or destination.read_bytes() != content:
                    staged = stage / str(index) / name
                    staged.parent.mkdir(parents=True, exist_ok=True)
                    staged.write_bytes(content)
                    prepared.append((destination, staged))
                    updated = True
            results.append(RefinementResult(json.loads(concept.metadata)["concept_name"], source, output, created, updated))
        if not results:
            raise GateError("Requested concept is not in evaluated corpus")
        assert_gate_snapshot_current(snapshot)
        # Revalidate destination topology after staging; no partial output on validation failure.
        _validate_destination(snapshot, refined_root, report_path)
        for destination, staged in prepared:
            _atomic_output(destination, staged.read_bytes())
    return results


def refine_concept_page(concept_dir: Path, refined_root: Path, *, evaluation_report: Path | None = None) -> RefinementResult:
    if evaluation_report is None:
        raise GateError("Evaluation report required before refinement")
    report = load_evaluation_report(evaluation_report)
    root = Path(report["roots"]["concepts"])
    snapshot = require_eligible_report(evaluation_report, root)
    if concept_dir.is_symlink():
        raise GateError("Symlink concept directory")
    try:
        selected = concept_dir.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise GateError("Requested concept outside evaluated corpus") from exc
    return _prepare_and_publish(snapshot, refined_root, evaluation_report, selected)[0]


def refine_concepts(concepts_root: Path, refined_root: Path, *, evaluation_report: Path | None = None) -> RefinementReport:
    snapshot = require_eligible_report(evaluation_report, concepts_root)
    results = _prepare_and_publish(snapshot, refined_root, evaluation_report)
    report = RefinementReport(concepts_processed=len(results))
    for result in results:
        if result.created:
            report.created.append(result.concept_name)
        if result.updated:
            report.updated.append(result.concept_name)
        else:
            report.unchanged.append(result.concept_name)
    return report


def refinement_report_to_json(report: RefinementReport) -> str:
    return json.dumps(asdict(report), indent=2, ensure_ascii=True)
