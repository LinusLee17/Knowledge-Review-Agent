from __future__ import annotations

import json
from pathlib import Path

from knowledge_review_agent.concept_store import save_concept_metadata
from knowledge_review_agent.graph_bundle import build_graph_bundle, write_graph_bundle
from knowledge_review_agent.models import ConceptMetadata, GraphEdge, GraphNode


def test_graph_bundle_enriches_nodes_and_writes_graph_json(tmp_path: Path) -> None:
    graphs_root = tmp_path / "knowledge_base" / "graphs"
    concepts_root = tmp_path / "knowledge_base" / "concepts"
    concept_dir = concepts_root / "Gradient Descent"
    concept_dir.mkdir(parents=True)

    save_concept_metadata(
        concept_dir / "metadata.json",
        ConceptMetadata(
            concept_name="Gradient Descent",
            canonical_key="gradient descent",
            domain="Machine Learning",
            topic="Optimization",
            importance_score=5,
            definition="Gradient Descent iteratively minimizes a loss function.",
            intuition="Move downhill in parameter space.",
            applications=["Neural Networks"],
            aliases=["GD"],
            contributing_courses=["BT4240", "CS3244"],
            contributing_lecture_files=["BT4240/L4/lecture.json"],
            prerequisites=["Calculus"],
            related_concepts=["Learning Rate"],
            broader_topics=["Optimization"],
        ),
    )

    node = GraphNode(
        node_id="gradient-descent",
        concept_key="gradient descent",
        concept_name="Gradient Descent",
        metadata_path=(concept_dir / "metadata.json").as_posix(),
        version_number=1,
        last_updated_timestamp="2026-07-10T00:00:00+00:00",
        domain="Machine Learning",
        topic="Optimization",
        importance_score=5,
        contributing_courses=["BT4240", "CS3244"],
        contributing_lecture_files=["BT4240/L4/lecture.json"],
        graph_node_id="gradient-descent",
    )
    edge = GraphEdge(
        edge_id="prerequisite::calculus::gradient-descent",
        source_node_id="calculus",
        source_concept_key="calculus",
        target_node_id="gradient-descent",
        target_concept_key="gradient descent",
        relation_type="prerequisite",
        target_resolved=True,
        source_concept_name="Calculus",
        target_concept_name="Gradient Descent",
        source_metadata_path="/tmp/calculus/metadata.json",
        source_version_number=1,
        supporting_concept_keys=["gradient descent"],
        supporting_metadata_paths=[(concept_dir / "metadata.json").as_posix()],
        supporting_courses=["BT4240"],
        supporting_lecture_files=["BT4240/L4/lecture.json"],
        supporting_lecture_hashes={"BT4240/L4/lecture.json": "abc"},
        last_updated_timestamp="2026-07-10T00:00:00+00:00",
    )

    bundle = build_graph_bundle([node], [edge], graphs_root=graphs_root, generated_at="2026-07-10T00:00:00+00:00")
    assert bundle.stats["total_concepts"] == 1
    assert bundle.stats["total_edges"] == 1
    assert bundle.stats["multi_course_concepts"] == 1
    assert bundle.nodes[0].concept_name == "Gradient Descent"
    assert bundle.nodes[0].concept_url.endswith("concept.md")
    assert "../knowledge_base/refined/Gradient Descent/concept.md" in bundle.nodes[0].concept_url
    assert "Calculus" in bundle.nodes[0].search_terms
    assert bundle.nodes[0].connected_edge_count == 1

    graph_json = write_graph_bundle(graphs_root, [node], [edge], generated_at="2026-07-10T00:00:00+00:00")
    payload = json.loads(graph_json.read_text(encoding="utf-8"))
    assert payload["stats"]["total_concepts"] == 1
    assert payload["nodes"][0]["definition"] == "Gradient Descent iteratively minimizes a loss function."
    assert payload["nodes"][0]["interview_notes"] == ""
    assert payload["edges"][0]["relation_type"] == "prerequisite"
