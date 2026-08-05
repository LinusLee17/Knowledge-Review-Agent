from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from pathlib import Path

from .concept_store import load_concept_metadata, save_concept_metadata
from .utils import normalize_spaces


CANONICAL_SECTION_ORDER = [
    "Classification",
    "Contributing Courses",
    "Definition",
    "Why it Matters",
    "Core Intuition",
    "How it Works",
    "Mathematical Foundation",
    "Key Components",
    "Advantages",
    "Limitations",
    "Common Mistakes",
    "Common Variants",
    "Real-world Applications",
    "Interview Questions",
    "Related Concepts",
    "Connections",
    "Prerequisites",
    "Further Reading",
    "Slide-derived Evidence",
    "Provenance",
    "Extraction Metadata",
]

SECTION_ALIASES = {
    "real-world applications": "Real-world Applications",
    "real world applications": "Real-world Applications",
    "applications": "Real-world Applications",
    "assumptions": "Assumptions",
}


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


def discover_concept_directories(concepts_root: Path) -> list[Path]:
    if not concepts_root.exists():
        return []
    return sorted(path for path in concepts_root.iterdir() if path.is_dir())


def _canonical_section_name(raw_name: str) -> str:
    cleaned = normalize_spaces(raw_name).strip()
    key = cleaned.lower()
    if key in SECTION_ALIASES:
        return SECTION_ALIASES[key]
    for section in CANONICAL_SECTION_ORDER:
        if section.lower() == key:
            return section
    return cleaned


def _parse_sections(markdown: str) -> tuple[list[str], str, dict[str, list[str]], list[str]]:
    prefix_lines: list[str] = []
    title = ""
    sections: dict[str, list[str]] = {}
    ordered_sections: list[str] = []
    current = "__preamble__"
    sections[current] = []
    seen_title = False

    for line in markdown.splitlines():
        if line.startswith("# ") and not seen_title:
            title = line[2:].strip()
            seen_title = True
            continue
        match = re.match(r"^##\s+(.*)$", line)
        if match:
            current = _canonical_section_name(match.group(1))
            if current not in sections:
                sections[current] = []
                ordered_sections.append(current)
            continue
        if not seen_title and current == "__preamble__":
            prefix_lines.append(line)
            continue
        sections.setdefault(current, []).append(line)

    return prefix_lines, title, sections, ordered_sections


def _render_sections(
    prefix_lines: list[str],
    title: str,
    sections: dict[str, list[str]],
    ordered_sections: list[str],
) -> str:
    lines: list[str] = []
    if prefix_lines:
        lines.extend(prefix_lines)
        if lines[-1] != "":
            lines.append("")
    if title:
        lines.append(f"# {title}")
    else:
        lines.append("# Concept")

    if sections.get("__preamble__"):
        preamble = "\n".join(sections["__preamble__"]).strip()
        if preamble:
            lines.extend(["", preamble])

    seen: set[str] = set()
    ordered = [section for section in CANONICAL_SECTION_ORDER if section in sections]
    extras = [section for section in ordered_sections if section not in CANONICAL_SECTION_ORDER]
    tail = [section for section in extras if section not in ordered]

    for section in [*ordered, *tail]:
        if section == "__preamble__" or section in seen:
            continue
        seen.add(section)
        content = sections.get(section, [])
        cleaned_content = "\n".join(content).rstrip()
        if cleaned_content:
            lines.extend(["", f"## {section}", cleaned_content])
        else:
            lines.extend(["", f"## {section}"])

    return "\n".join(lines).rstrip() + "\n"


def refine_concept_page(concept_dir: Path, refined_root: Path) -> RefinementResult:
    concept_md = concept_dir / "concept.md"
    metadata_path = concept_dir / "metadata.json"
    if not concept_md.exists() or not metadata_path.exists():
        return RefinementResult(
            concept_name=concept_dir.name,
            source_dir=concept_dir,
            refined_dir=refined_root / concept_dir.name,
            created=False,
            updated=False,
        )

    metadata = load_concept_metadata(metadata_path)
    if not metadata:
        return RefinementResult(
            concept_name=concept_dir.name,
            source_dir=concept_dir,
            refined_dir=refined_root / concept_dir.name,
            created=False,
            updated=False,
        )

    prefix_lines, title, sections, ordered_sections = _parse_sections(concept_md.read_text(encoding="utf-8"))
    refined_dir = refined_root / concept_dir.name
    refined_md = refined_dir / "concept.md"
    refined_metadata = refined_dir / "metadata.json"
    created = not refined_md.exists() or not refined_metadata.exists()
    refined_dir.mkdir(parents=True, exist_ok=True)

    new_markdown = _render_sections(prefix_lines, title or metadata.concept_name or concept_dir.name, sections, ordered_sections)
    existing_markdown = refined_md.read_text(encoding="utf-8") if refined_md.exists() else None
    existing_metadata = load_concept_metadata(refined_metadata)

    updated = existing_markdown != new_markdown or existing_metadata != metadata
    if updated:
        refined_md.write_text(new_markdown, encoding="utf-8")
        save_concept_metadata(refined_metadata, metadata)

    return RefinementResult(
        concept_name=metadata.concept_name or concept_dir.name,
        source_dir=concept_dir,
        refined_dir=refined_dir,
        created=created,
        updated=updated,
    )


def refine_concepts(concepts_root: Path, refined_root: Path) -> RefinementReport:
    report = RefinementReport()
    for concept_dir in discover_concept_directories(concepts_root):
        result = refine_concept_page(concept_dir, refined_root)
        report.concepts_processed += 1
        if not result.refined_dir.exists():
            report.skipped.append(result.concept_name)
            continue
        if result.created:
            report.created.append(result.concept_name)
        if result.updated:
            report.updated.append(result.concept_name)
        else:
            report.unchanged.append(result.concept_name)
    return report


def refinement_report_to_json(report: RefinementReport) -> str:
    return json.dumps(
        {
            "concepts_processed": report.concepts_processed,
            "created": report.created,
            "updated": report.updated,
            "unchanged": report.unchanged,
            "skipped": report.skipped,
        },
        indent=2,
        ensure_ascii=True,
    )
