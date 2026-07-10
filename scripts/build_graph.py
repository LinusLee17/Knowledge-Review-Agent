#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from knowledge_review_agent.graph_builder import build_knowledge_graph  # noqa: E402
from knowledge_review_agent.graph_bundle import write_graph_bundle  # noqa: E402
from knowledge_review_agent.graph_store import load_graph_edges, load_graph_nodes  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build incremental graph data from canonical concepts.")
    parser.add_argument("--concepts", default=str(ROOT / "knowledge_base" / "concepts"), help="Canonical concept root")
    parser.add_argument("--graphs", default=str(ROOT / "knowledge_base" / "graphs"), help="Graph output root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    graphs_root = Path(args.graphs)
    concepts_root = Path(args.concepts)
    if not any(concepts_root.rglob("metadata.json")):
        print(
            json.dumps(
                {
                    "error": "no concept metadata found",
                    "concepts_root": concepts_root.as_posix(),
                    "graphs_root": graphs_root.as_posix(),
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1
    report = build_knowledge_graph(
        concepts_root=concepts_root,
        graphs_root=graphs_root,
    )
    nodes = load_graph_nodes(graphs_root / "nodes.json")
    edges = load_graph_edges(graphs_root / "edges.json")
    graph_json = write_graph_bundle(
        graphs_root=graphs_root,
        nodes=nodes,
        edges=edges,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
    print(
        json.dumps(
            {
                "concepts_processed": report.concepts_processed,
                "nodes_created": report.nodes_created,
                "nodes_updated": report.nodes_updated,
                "nodes_unchanged": report.nodes_unchanged,
                "nodes_deleted": report.nodes_deleted,
                "edges_created": report.edges_created,
                "edges_updated": report.edges_updated,
                "edges_unchanged": report.edges_unchanged,
                "edges_deleted": report.edges_deleted,
                "unresolved_edge_targets": report.unresolved_edge_targets,
                "graph_json": graph_json.as_posix(),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
