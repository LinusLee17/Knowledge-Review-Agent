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

from knowledge_review_agent.slide_extractor import run_slide_extractor  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract lecture PDFs into Markdown and JSON notes.")
    parser.add_argument("--raw", default=str(ROOT / "data" / "raw"), help="Raw PDF root")
    parser.add_argument("--processed", default=str(ROOT / "data" / "processed"), help="Processed output root")
    parser.add_argument(
        "--metadata",
        default=str(ROOT / "data" / "metadata.csv"),
        help="Course metadata CSV",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = run_slide_extractor(
        raw_root=Path(args.raw),
        processed_root=Path(args.processed),
        metadata_csv=Path(args.metadata),
    )
    print(json.dumps({"processed": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
