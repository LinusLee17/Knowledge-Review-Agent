from __future__ import annotations

import json
from pathlib import Path

from knowledge_review_agent.concept_store import load_concept_metadata, save_concept_metadata
from knowledge_review_agent.consolidation import consolidate_concepts, discover_concept_records
from knowledge_review_agent.evaluation import evaluate_consolidation
from knowledge_review_agent.models import ConceptMetadata


def _write_lecture_json(
    path: Path,
    *,
    course_id: str,
    course_name: str,
    pdf: str,
    pages: list[dict],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "pdf": pdf,
        "course": {
            "course_id": course_id,
            "course_name": course_name,
            "category": "",
            "semester": "",
            "folder": "",
            "notes": "",
        },
        "title": path.parent.name,
        "page_count": len(pages),
        "parser_version": "anthropic-pdf-skill-bridge/1",
        "warnings": [],
        "pages": pages,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def _write_concept_fixture(
    concepts_root: Path,
    *,
    directory_name: str,
    concept_name: str,
    canonical_key: str,
    courses: list[str],
    lectures: list[str],
    hashes: dict[str, str],
    timestamp: str,
    version: int,
) -> Path:
    directory = concepts_root / directory_name
    directory.mkdir(parents=True, exist_ok=True)
    metadata = ConceptMetadata(
        concept_name=concept_name,
        canonical_key=canonical_key,
        contributing_courses=courses,
        contributing_lecture_files=lectures,
        source_lecture_hashes=hashes,
        last_updated_timestamp=timestamp,
        version_number=version,
        graph_node_id=canonical_key.replace(" ", "-"),
    )
    (directory / "concept.md").write_text(f"# {concept_name}\n", encoding="utf-8")
    save_concept_metadata(directory / "metadata.json", metadata)
    return directory


def test_consolidate_concepts_merges_duplicates_and_keeps_provenance(tmp_path: Path) -> None:
    processed_root = tmp_path / "data" / "processed"
    concepts_root = tmp_path / "knowledge_base" / "concepts"
    processed_root.mkdir(parents=True)
    concepts_root.mkdir(parents=True)

    _write_concept_fixture(
        concepts_root,
        directory_name="Decision Tree",
        concept_name="Decision Tree",
        canonical_key="decision tree",
        courses=["CS099"],
        lectures=["old/decision_tree/lecture.json"],
        hashes={"old/decision_tree/lecture.json": "oldhash-a"},
        timestamp="2025-01-01T00:00:00+00:00",
        version=1,
    )
    _write_concept_fixture(
        concepts_root,
        directory_name="Decision Trees",
        concept_name="Decision Trees",
        canonical_key="decision tree",
        courses=["STAT200"],
        lectures=["stats/trees/lecture.json"],
        hashes={"stats/trees/lecture.json": "oldhash-b"},
        timestamp="2025-01-02T00:00:00+00:00",
        version=1,
    )

    _write_lecture_json(
        processed_root / "cs101" / "week1" / "lecture.json",
        course_id="CS101",
        course_name="Intro ML",
        pdf="cs101/week1/lecture1.pdf",
        pages=[
            {
                "page_number": 1,
                "heading": "Decision Trees",
                "extracted_text": "Decision Trees split data.\nLinear Regression fits a line.",
                "tables": [],
                "image_count": 0,
                "concept_candidates": ["Decision Trees", "Linear Regression"],
            }
        ],
    )
    _write_lecture_json(
        processed_root / "stats201" / "week2" / "lecture.json",
        course_id="STAT201",
        course_name="Statistics II",
        pdf="stats201/week2/lecture2.pdf",
        pages=[
            {
                "page_number": 1,
                "heading": "Decision Tree",
                "extracted_text": "Decision Tree nodes split on feature thresholds.",
                "tables": [],
                "image_count": 0,
                "concept_candidates": ["Decision Tree"],
            },
            {
                "page_number": 2,
                "heading": "Linear Regression",
                "extracted_text": "Linear Regression minimizes squared error.",
                "tables": [],
                "image_count": 0,
                "concept_candidates": ["Linear Regression"],
            },
        ],
    )

    report = consolidate_concepts(processed_root=processed_root, concepts_root=concepts_root)
    assert "linear regression" in report.created
    assert "decision tree" in report.updated
    assert report.duplicate_dirs

    records = discover_concept_records(concepts_root)
    grouped: dict[str, list] = {}
    for record in records:
        grouped.setdefault(record.key, []).append(record)

    assert set(grouped) == {"decision tree", "linear regression"}
    assert len(grouped["decision tree"]) == 1

    decision_tree = grouped["decision tree"][0].metadata
    assert set(decision_tree.contributing_courses) == {"CS099", "STAT200", "CS101", "STAT201"}
    assert "cs101/week1/lecture.json" in decision_tree.contributing_lecture_files
    assert "stats201/week2/lecture.json" in decision_tree.contributing_lecture_files

    decision_tree_md = grouped["decision tree"][0].directory / "concept.md"
    markdown = decision_tree_md.read_text(encoding="utf-8")
    assert "Decision Trees" in markdown
    assert "cs101/week1/lecture1.pdf" in markdown
    assert "stats201/week2/lecture2.pdf" in markdown
    assert "old/decision_tree/lecture.json" in markdown

    linear_regression_md = grouped["linear regression"][0].directory / "concept.md"
    linear_markdown = linear_regression_md.read_text(encoding="utf-8")
    assert linear_markdown.index("## Definition") < linear_markdown.index("## Why it Matters")
    assert linear_markdown.index("## Why it Matters") < linear_markdown.index("## Core Intuition")
    assert linear_markdown.index("## Core Intuition") < linear_markdown.index("## How it Works")
    assert "## Mathematical Foundation" in linear_markdown
    assert "## Key Components" in linear_markdown
    assert "## Common Mistakes" in linear_markdown
    assert "## Common Variants" in linear_markdown
    assert "## Connections" in linear_markdown
    assert linear_markdown.rfind("## Slide-derived Evidence") > linear_markdown.rfind("## Further Reading")
    assert linear_markdown.rfind("## Provenance") > linear_markdown.rfind("## Slide-derived Evidence")
    assert linear_markdown.rfind("## Extraction Metadata") > linear_markdown.rfind("## Provenance")

    evaluation = evaluate_consolidation(concepts_root)
    assert evaluation.duplicate_key_groups == 0
    assert evaluation.concepts_with_multi_course_provenance >= 1
    assert evaluation.heuristic_merge_score > 0
