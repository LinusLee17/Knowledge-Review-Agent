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

from knowledge_review_agent.evaluation import evaluate_consolidation  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate concept consolidation quality.")
    parser.add_argument("--concepts", default=str(ROOT / "knowledge_base" / "concepts"), help="Canonical concept root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = evaluate_consolidation(Path(args.concepts))
    print(json.dumps(result.to_dict(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
