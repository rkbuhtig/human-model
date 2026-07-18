from __future__ import annotations

import argparse
from pathlib import Path

from .runner import encode_prediction, load_json_object, run_model


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one frozen S0 candidate model.")
    parser.add_argument("--model", required=True, choices=("B0", "B1", "B2", "H"))
    parser.add_argument("--input", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--model-cards", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--include-h-diagnostics", action="store_true")
    args = parser.parse_args()
    document = run_model(
        args.model,
        load_json_object(args.input),
        load_json_object(args.parameters),
        load_json_object(args.model_cards),
        seed=args.seed,
        include_h_diagnostics=args.include_h_diagnostics,
    )
    Path(args.output).write_bytes(encode_prediction(document))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
