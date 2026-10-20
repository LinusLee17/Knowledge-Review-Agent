#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from knowledge_review_agent.quality_gate import (  # noqa: E402
    GatePaths, GateError, evaluate_for_refinement, write_evaluation_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate concept consolidation quality.")
    parser.add_argument("--concepts", default=str(ROOT / "knowledge_base" / "concepts"), help="Canonical concept root")
    parser.add_argument("--processed", default=str(ROOT / "data" / "processed"))
    parser.add_argument("--reviews", default=str(ROOT / "evaluation" / "reviews"))
    parser.add_argument("--asset-root", action="append", default=[])
    parser.add_argument("--reports", default=str(ROOT / "evaluation" / "runs" / "gates"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        paths = GatePaths(Path(args.concepts), Path(args.processed), Path(args.reviews), tuple(map(Path, args.asset_root)))
        result = evaluate_for_refinement(paths)
        report = write_evaluation_report(result, Path(args.reports))
        print(json.dumps({"report": str(report), "eligibility": result["eligibility"],
                          "findings": result["findings"], "diagnostics": result["diagnostics"]}, indent=2))
        return 0 if result["eligibility"] == "pass" else 1
    except (GateError, OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc), "eligibility": "blocked"}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
