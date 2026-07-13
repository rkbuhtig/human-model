from __future__ import annotations

import argparse
from pathlib import Path

from dynamics.labs.interp_m1_evaluator import encode_report, evaluate_m1


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a completed INTERP M1 run")
    parser.add_argument("--execution", required=True, type=Path)
    parser.add_argument("--evaluation", required=True, type=Path)
    parser.add_argument("--cell-schema", required=True, type=Path)
    parser.add_argument("--run-schema", required=True, type=Path)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--report-schema", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    report = evaluate_m1(
        arguments.execution.read_bytes(),
        arguments.evaluation.read_bytes(),
        arguments.cell_schema.read_bytes(),
        arguments.run_schema.read_bytes(),
        arguments.run.read_bytes(),
        arguments.policy.read_bytes(),
        arguments.report_schema.read_bytes(),
    )
    arguments.output.write_bytes(encode_report(report))


if __name__ == "__main__":
    main()
