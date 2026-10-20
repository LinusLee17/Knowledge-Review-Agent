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

from dataclasses import asdict
from knowledge_review_agent.source_occurrences import SourceValidationError
from knowledge_review_agent.consolidation import consolidate_concepts  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Consolidate lecture notes into canonical concept files.")
    parser.add_argument("--processed", default=str(ROOT / "data" / "processed"), help="Processed lecture root")
    parser.add_argument("--concepts", default=str(ROOT / "knowledge_base" / "concepts"), help="Canonical concept root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = consolidate_concepts(
        processed_root=Path(args.processed),
        concepts_root=Path(args.concepts),
    )
    print(
        json.dumps(
            {
                "created": report.created,
                "updated": report.updated,
                "unchanged": report.unchanged,
                "duplicate_dirs": report.duplicate_dirs,
                "total_mentions": report.total_mentions,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SourceValidationError as exc:
        print(json.dumps({"error": str(exc), "issues": [asdict(i) for i in exc.issues]}), file=sys.stderr)
        raise SystemExit(1)
