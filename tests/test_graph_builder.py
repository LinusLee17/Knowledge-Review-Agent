from __future__ import annotations

from pathlib import Path

from knowledge_review_agent.concept_store import save_concept_metadata
from knowledge_review_agent.graph_builder import build_knowledge_graph
from knowledge_review_agent.graph_evaluation import evaluate_graph
from knowledge_review_agent.graph_store import load_graph_edges, load_graph_nodes
from knowledge_review_agent.models import ConceptMetadata


def _write_concept_fixture(
    concepts_root: Path,
    *,
    directory_name: str,
    concept_name: str,
    canonical_key: str,
    courses: list[str],
    lectures: list[str],
    hashes: dict[str, str],
    prerequisites: list[str] | None = None,
    related: list[str] | None = None,
    used_in: list[str] | None = None,
    timestamp: str = "2025-01-01T00:00:00+00:00",
    version: int = 1,
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
        prerequisites=prerequisites or [],
        related_concepts=related or [],
        used_in=used_in or [],
        graph_node_id=canonical_key.replace(" ", "-"),
    )
    (directory / "concept.md").write_text(f"# {concept_name}\n", encoding="utf-8")
    save_concept_metadata(directory / "metadata.json", metadata)
    return directory


def test_build_knowledge_graph_resolves_aliases_and_skips_unknown_targets(tmp_path: Path) -> None:
    concepts_root = tmp_path / "knowledge_base" / "concepts"
    graphs_root = tmp_path / "knowledge_base" / "graphs"
    concepts_root.mkdir(parents=True)

    _write_concept_fixture(
        concepts_root,
        directory_name="Probability",
        concept_name="Probability",
        canonical_key="probability",
        courses=["STAT101"],
        lectures=["stat101/week1/lecture.json"],
        hashes={"stat101/week1/lecture.json": "hash-prob"},
    )
    _write_concept_fixture(
        concepts_root,
        directory_name="Decision Trees",
        concept_name="Decision Trees",
        canonical_key="decision tree",
        courses=["STAT201", "CS201"],
        lectures=["stat201/week2/lecture.json", "cs201/week3/lecture.json"],
        hashes={
            "stat201/week2/lecture.json": "hash-tree",
            "cs201/week3/lecture.json": "hash-tree-2",
        },
        prerequisites=["Probability"],
        related=["Random Forest"],
        used_in=["Classification"],
        version=1,
    )
    _write_concept_fixture(
        concepts_root,
        directory_name="Random Forest",
        concept_name="Random Forest",
        canonical_key="random forest",
        courses=["CS202"],
        lectures=["cs202/week4/lecture.json"],
        hashes={"cs202/week4/lecture.json": "hash-rf"},
        related=["Decision Trees"],
    )

    first = build_knowledge_graph(concepts_root=concepts_root, graphs_root=graphs_root)
    assert first.nodes_created == ["decision-tree", "probability", "random-forest"]
    assert first.edges_created == ["prerequisite::decision tree::probability", "related::decision tree::random forest"]
    assert first.unresolved_edge_targets == 0

    nodes = load_graph_nodes(graphs_root / "nodes.json")
    edges = load_graph_edges(graphs_root / "edges.json")
    assert len(nodes) == 3
    assert len(edges) == 2
    assert evaluate_graph(graphs_root).node_count == 3
    assert evaluate_graph(graphs_root).unresolved_edge_targets == 0

    second = build_knowledge_graph(concepts_root=concepts_root, graphs_root=graphs_root)
    assert second.nodes_unchanged == ["decision-tree", "probability", "random-forest"]
    assert second.edges_unchanged == ["prerequisite::decision tree::probability", "related::decision tree::random forest"]
    assert second.nodes_created == []
    assert second.edges_created == []

    _write_concept_fixture(
        concepts_root,
        directory_name="Classification",
        concept_name="Classification",
        canonical_key="classification",
        courses=["CS202"],
        lectures=["cs202/week5/lecture.json"],
        hashes={"cs202/week5/lecture.json": "hash-cls"},
        timestamp="2025-01-03T00:00:00+00:00",
    )

    third = build_knowledge_graph(concepts_root=concepts_root, graphs_root=graphs_root)
    assert "classification" in third.nodes_created
    assert "used_in::decision tree::classification" in third.edges_created
    assert third.unresolved_edge_targets == 0

    updated_edges = load_graph_edges(graphs_root / "edges.json")
    used_in = [edge for edge in updated_edges if edge.edge_id == "used_in::decision tree::classification"][0]
    assert used_in.target_resolved is True

    eval_result = evaluate_graph(graphs_root)
    assert eval_result.node_count == 4
    assert eval_result.unresolved_edge_targets == 0
