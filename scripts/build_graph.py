#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from knowledge_review_agent.graph_builder import build_knowledge_graph  # noqa: E402
from knowledge_review_agent.graph_bundle import GraphPresentationPaths, GraphContractError, GraphContractIssue, validate_graph_paths, write_graph_bundle  # noqa: E402
from knowledge_review_agent.graph_store import load_graph_edges, load_graph_nodes  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build incremental graph data from canonical concepts.")
    parser.add_argument("--concepts", help="Canonical concept root relative to repo")
    parser.add_argument("--graphs", help="Graph output root relative to repo")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--refined", help="Refined concept root relative to repo")
    parser.add_argument("--site", help="Website root relative to repo")
    return parser.parse_args()


def _run() -> int:
    args = parse_args()
    repo = Path(args.repo_root).absolute()
    def configured(value, default):
        path = Path(value or default)
        return path if path.is_absolute() else repo/path
    paths = GraphPresentationPaths(repo, configured(args.concepts, "knowledge_base/concepts"),
        configured(args.refined, "knowledge_base/refined"), configured(args.site, "website"))
    graphs_root = configured(args.graphs, "knowledge_base/graphs")
    validate_graph_paths(paths, graphs_root=graphs_root)
    concepts_root = paths.concepts_root
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
        paths=paths,
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


def main() -> int:
    try:
        return _run()
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        issues = exc.issues if isinstance(exc, GraphContractError) else (GraphContractIssue("io_error", "graph", str(exc)),)
        print(json.dumps({"error": str(exc), "issues": [asdict(i) for i in issues]}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
