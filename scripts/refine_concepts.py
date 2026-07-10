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

from knowledge_review_agent.presentation_refinement import refine_concepts  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refine canonical concept pages into presentation-ready output.")
    parser.add_argument("--concepts", default=str(ROOT / "knowledge_base" / "concepts"), help="Canonical concept root")
    parser.add_argument("--refined", default=str(ROOT / "knowledge_base" / "refined"), help="Refined concept root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = refine_concepts(
        concepts_root=Path(args.concepts),
        refined_root=Path(args.refined),
    )
    print(
        json.dumps(
            {
                "concepts_processed": report.concepts_processed,
                "created": report.created,
                "updated": report.updated,
                "unchanged": report.unchanged,
                "skipped": report.skipped,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
