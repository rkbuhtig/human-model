from __future__ import annotations

import argparse
from pathlib import Path

from dynamics.labs.interp_d1_runner import encode_run, run_d1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute the frozen INTERP-001D1 detached matrix"
    )
    parser.add_argument("--execution", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    arguments.output.write_bytes(
        encode_run(run_d1(arguments.execution.read_bytes()))
    )


if __name__ == "__main__":
    main()
