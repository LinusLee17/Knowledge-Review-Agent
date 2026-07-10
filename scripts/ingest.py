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

from knowledge_review_agent.ingestion import run_incremental_ingestion  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Incrementally ingest lecture PDFs.")
    parser.add_argument("--raw", default=str(ROOT / "data" / "raw"), help="Raw PDF root")
    parser.add_argument("--processed", default=str(ROOT / "data" / "processed"), help="Processed output root")
    parser.add_argument("--index", default=str(ROOT / "data" / "index.json"), help="Repository index JSON")
    parser.add_argument("--metadata", default=str(ROOT / "data" / "metadata.csv"), help="Course metadata CSV")
    parser.add_argument("--rebuild-all", action="store_true", help="Reprocess every PDF explicitly")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_incremental_ingestion(
        raw_root=Path(args.raw),
        processed_root=Path(args.processed),
        index_path=Path(args.index),
        metadata_csv=Path(args.metadata),
        rebuild_all=args.rebuild_all,
    )
    payload = {
        "processed": [entry.relative_file_path for entry in report.processed],
        "skipped": [entry.relative_file_path for entry in report.skipped],
        "errors": [entry.relative_file_path for entry in report.errors],
    }
    print(json.dumps(payload, indent=2))
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
