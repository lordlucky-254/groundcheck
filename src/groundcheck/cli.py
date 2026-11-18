"""Command-line interface for GroundCheck."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .core import check_answer


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag answer claims with little lexical overlap with retrieved context."
    )
    parser.add_argument("input", type=Path, help="JSON file with answer and contexts fields")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.2,
        help="minimum Jaccard overlap to mark a claim supported (default: 0.2)",
    )
    args = parser.parse_args()

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("input JSON must be an object")
        report = check_answer(
            payload["answer"], payload["contexts"], threshold=args.threshold
        )
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"groundcheck: {error}", file=sys.stderr)
        return 2

    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
