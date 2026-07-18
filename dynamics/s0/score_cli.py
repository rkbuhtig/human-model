from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import canonical_bytes
from .scoring import score_prediction_documents


def _load_list(path: str) -> list[dict[str, object]]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"expected JSON array of objects: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Score detached S0 predictions.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--targets", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = score_prediction_documents(_load_list(args.predictions), _load_list(args.targets))
    Path(args.output).write_bytes(canonical_bytes(report) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
