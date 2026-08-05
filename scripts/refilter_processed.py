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

from knowledge_review_agent.concept_filter import refilter_processed_lectures  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Re-filter stored lecture JSON without parsing PDFs.")
    parser.add_argument("--processed", default=str(ROOT / "data" / "processed"), help="Processed lecture root")
    parser.add_argument("--course", action="append", default=[], help="Course ID; repeat for multiple courses")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = refilter_processed_lectures(Path(args.processed), set(args.course))
    print(json.dumps({
        "lectures": len(results),
        "candidate_concepts": sum(int(item["candidate_concepts"]) for item in results),
        "concepts_accepted": sum(int(item["concepts_accepted"]) for item in results),
        "concepts_rejected": sum(int(item["concepts_rejected"]) for item in results),
        "results": results,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
