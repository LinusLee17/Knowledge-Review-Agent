from __future__ import annotations

import csv
from pathlib import Path

from .models import CourseMetadata
from .utils import normalize_spaces, slugify


def load_metadata(csv_path: Path) -> list[CourseMetadata]:
    if not csv_path.exists():
        return []

    rows: list[CourseMetadata] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            rows.append(
                CourseMetadata(
                    course_id=normalize_spaces(raw.get("course_id", "")),
                    course_name=normalize_spaces(raw.get("course_name", "")),
                    category=normalize_spaces(raw.get("category", "")),
                    semester=normalize_spaces(raw.get("semester", "")),
                    folder=normalize_spaces(raw.get("folder", "")),
                    notes=normalize_spaces(raw.get("notes", "")),
                )
            )
    return rows


def resolve_course(pdf_path: Path, raw_root: Path, metadata_rows: list[CourseMetadata]) -> CourseMetadata:
    try:
        relative = pdf_path.relative_to(raw_root)
    except ValueError:
        relative = pdf_path.name  # type: ignore[assignment]

    relative_str = relative.as_posix() if isinstance(relative, Path) else str(relative)
    folder_parts = relative_str.split("/")

    matches: list[tuple[int, CourseMetadata]] = []
    for row in metadata_rows:
        for candidate in (row.folder, row.course_id):
            if not candidate:
                continue
            folder = candidate.strip("/")
            if relative_str == folder or relative_str.startswith(folder + "/"):
                matches.append((len(folder.split("/")), row))
                continue
            if folder in folder_parts:
                matches.append((len(folder.split("/")), row))

    if matches:
        matches.sort(key=lambda item: item[0], reverse=True)
        return matches[0][1]

    if len(metadata_rows) == 1:
        return metadata_rows[0]

    blank_folder_rows = [row for row in metadata_rows if not row.folder]
    if len(blank_folder_rows) == 1:
        return blank_folder_rows[0]

    if folder_parts and not folder_parts[0].lower().endswith(".pdf"):
        inferred = folder_parts[0]
        return CourseMetadata(course_id=inferred, course_name="", category="", semester="", folder=inferred, notes="inferred from data/raw folder")

    stem = slugify(pdf_path.stem)
    return CourseMetadata(course_id="", course_name="", category="", semester="", folder="", notes=stem)
