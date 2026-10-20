from __future__ import annotations

import json
from pathlib import Path

from knowledge_review_agent.concept_store import save_concept_metadata
from knowledge_review_agent.graph_bundle import GraphPresentationPaths, build_graph_bundle, write_graph_bundle
from urllib.parse import parse_qs, urlsplit, unquote
from knowledge_review_agent.models import ConceptMetadata, GraphEdge, GraphNode


def test_graph_bundle_enriches_nodes_and_writes_graph_json(tmp_path: Path) -> None:
    graphs_root = tmp_path / "knowledge_base" / "graphs"
    concepts_root = tmp_path / "knowledge_base" / "refined"
    site = tmp_path / "website"
    site.mkdir()
    (site / "concept.html").write_text("viewer")
    paths = GraphPresentationPaths(tmp_path, tmp_path / "knowledge_base" / "concepts", concepts_root, site)
    concept_dir = concepts_root / "Gradient Descent"
    concept_dir.mkdir(parents=True)

    save_concept_metadata(
        concept_dir / "metadata.json",
        ConceptMetadata(
            last_updated_timestamp="2026-07-10T00:00:00+00:00",
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

    (concept_dir / "concept.md").write_text("# Gradient Descent\n")

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
        study_priority=5,
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

    calculus_dir = concepts_root / "Calculus"
    calculus_dir.mkdir()
    save_concept_metadata(calculus_dir / "metadata.json", ConceptMetadata(concept_name="Calculus", canonical_key="calculus", last_updated_timestamp="2026-07-10T00:00:00+00:00"))
    (calculus_dir / "concept.md").write_text("# Calculus\n")
    calculus = GraphNode("calculus", "calculus", "Calculus", str(calculus_dir / "metadata.json"), 1, "2026-07-10T00:00:00+00:00")
    bundle = build_graph_bundle([node, calculus], [edge], graphs_root=graphs_root, generated_at="2026-07-10T00:00:00+00:00", paths=paths)
    gradient = next(n for n in bundle.nodes if n.node_id == "gradient-descent")
    assert bundle.stats["total_concepts"] == 2
    assert bundle.stats["total_edges"] == 1
    assert bundle.stats["multi_course_concepts"] == 1
    assert gradient.concept_name == "Gradient Descent"
    assert gradient.concept_url.endswith("concept.md")
    assert "../knowledge_base/refined/Gradient Descent/concept.md" in unquote(parse_qs(urlsplit(gradient.concept_url).query)["path"][0])
    assert "Calculus" in gradient.search_terms
    assert gradient.connected_edge_count == 1

    graph_json = write_graph_bundle(graphs_root, [node, calculus], [edge], generated_at="2026-07-10T00:00:00+00:00", paths=paths)
    payload = json.loads(graph_json.read_text(encoding="utf-8"))
    assert payload["stats"]["total_concepts"] == 2
    assert next(n for n in payload["nodes"] if n["node_id"] == "gradient-descent")["definition"] == "Gradient Descent iteratively minimizes a loss function."
    assert next(n for n in payload["nodes"] if n["node_id"] == "gradient-descent")["interview_notes"] == ""
    assert payload["edges"][0]["relation_type"] == "prerequisite"
