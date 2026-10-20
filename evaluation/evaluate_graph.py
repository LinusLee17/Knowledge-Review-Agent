#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from knowledge_review_agent.graph_bundle import GraphPresentationPaths, GraphContractError, GraphContractIssue, load_graph_bundle
from knowledge_review_agent.graph_evaluation import evaluate_graph  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate graph integrity metrics.")
    parser.add_argument("--graphs", help="Graph output root relative to repo")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--refined", help="Refined concept root relative to repo")
    parser.add_argument("--site", help="Website root relative to repo")
    parser.add_argument("--concepts", help="Canonical root (not required for presentation check)")
    parser.add_argument("--presentation", action="store_true", help="Validate published graph contract and files")
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
    if args.presentation:
        payload = load_graph_bundle(graphs_root / "graph.json", paths=paths, check_files=True)
        print(json.dumps({"valid": True, "schema_version": payload["schema_version"],
                          "node_count": len(payload["nodes"]), "edge_count": len(payload["edges"])}))
        return 0
    result = evaluate_graph(graphs_root)
    print(json.dumps(result.to_dict(), indent=2))
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
