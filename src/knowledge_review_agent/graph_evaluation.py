from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .graph_store import load_graph_edges, load_graph_nodes


@dataclass(frozen=True)
class GraphEvaluation:
    node_count: int
    edge_count: int
    unresolved_edge_targets: int
    self_loops: int
    isolated_nodes: int
    relation_counts: dict[str, int]
    integrity_score: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def evaluate_graph(graphs_root: Path) -> GraphEvaluation:
    nodes_path = graphs_root / "nodes.json"
    edges_path = graphs_root / "edges.json"

    nodes = load_graph_nodes(nodes_path) if nodes_path.exists() else []
    edges = load_graph_edges(edges_path) if edges_path.exists() else []

    node_ids = {node.node_id for node in nodes}
    relation_counts: dict[str, int] = {}
    unresolved_edge_targets = 0
    self_loops = 0
    incident_nodes: set[str] = set()

    for edge in edges:
        relation_counts[edge.relation_type] = relation_counts.get(edge.relation_type, 0) + 1
        if not edge.target_resolved or edge.target_node_id not in node_ids:
            unresolved_edge_targets += 1
        if edge.source_node_id == edge.target_node_id:
            self_loops += 1
        incident_nodes.add(edge.source_node_id)
        incident_nodes.add(edge.target_node_id)

    isolated_nodes = sum(1 for node in nodes if node.node_id not in incident_nodes)
    denominator = max(len(nodes), 1)
    coverage = 1.0 - (isolated_nodes / denominator)
    resolution = 1.0 - (unresolved_edge_targets / max(len(edges), 1))
    loop_penalty = 1.0 - (self_loops / max(len(edges), 1))
    integrity_score = round(max(0.0, min(100.0, 100.0 * (0.45 * coverage + 0.45 * resolution + 0.10 * loop_penalty))), 2)

    return GraphEvaluation(
        node_count=len(nodes),
        edge_count=len(edges),
        unresolved_edge_targets=unresolved_edge_targets,
        self_loops=self_loops,
        isolated_nodes=isolated_nodes,
        relation_counts=relation_counts,
        integrity_score=integrity_score,
    )
