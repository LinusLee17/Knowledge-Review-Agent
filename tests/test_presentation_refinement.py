from __future__ import annotations

import json
from pathlib import Path

from knowledge_review_agent.concept_store import save_concept_metadata
from knowledge_review_agent.models import ConceptMetadata
from knowledge_review_agent.presentation_refinement import refine_concepts


def test_presentation_refinement_reorders_sections_without_changing_content(tmp_path: Path) -> None:
    concepts_root = tmp_path / "knowledge_base" / "concepts"
    refined_root = tmp_path / "knowledge_base" / "refined"
    concept_dir = concepts_root / "Gradient Descent"
    concept_dir.mkdir(parents=True)

    concept_md = concept_dir / "concept.md"
    concept_md.write_text(
        """---
concept_name: "Gradient Descent"
---

# Gradient Descent

## Provenance
- BT4240 Week 4

## Definition
Gradient Descent is an iterative optimization method.

## Why it Matters
It trains many machine learning models.

## Classification
- domain: Machine Learning
- topic: Optimization

## Slide-derived Evidence
- slide 4
""",
        encoding="utf-8",
    )
    save_concept_metadata(
        concept_dir / "metadata.json",
        ConceptMetadata(
            concept_name="Gradient Descent",
            canonical_key="gradient descent",
            domain="Machine Learning",
            topic="Optimization",
            contributing_courses=["BT4240"],
            contributing_lecture_files=["BT4240/L4-Optimization/lecture.json"],
            source_lecture_hashes={"BT4240/L4-Optimization/lecture.json": "abc"},
        ),
    )

    report = refine_concepts(concepts_root=concepts_root, refined_root=refined_root)

    refined_md = refined_root / "Gradient Descent" / "concept.md"
    refined_meta = refined_root / "Gradient Descent" / "metadata.json"

    assert report.concepts_processed == 1
    assert report.created == ["Gradient Descent"]
    assert refined_md.exists()
    assert refined_meta.exists()

    refined_text = refined_md.read_text(encoding="utf-8")
    classification_pos = refined_text.index("## Classification")
    definition_pos = refined_text.index("## Definition")
    why_pos = refined_text.index("## Why it Matters")
    evidence_pos = refined_text.index("## Slide-derived Evidence")
    provenance_pos = refined_text.index("## Provenance")

    assert classification_pos < definition_pos < why_pos < evidence_pos < provenance_pos
    assert "Gradient Descent is an iterative optimization method." in refined_text
    assert "BT4240 Week 4" in refined_text

    metadata = json.loads(refined_meta.read_text(encoding="utf-8"))
    assert metadata["concept_name"] == "Gradient Descent"
    assert metadata["domain"] == "Machine Learning"
