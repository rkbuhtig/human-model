"""CLI for the INTERP-DIALOGUE-001P1-v0 scripted development pilot.

Usage:
    python -m dynamics.labs.interp_dialogue_p1_run_cli --write
    python -m dynamics.labs.interp_dialogue_p1_run_cli --verify

`--write` materializes every generated P1 artifact from the frozen P0-v0
instrument, the P1 coverage manifest and the scripted response corpus.
`--verify` rebuilds the same artifacts deterministically and fails if any
checked-in byte differs. Neither mode mutates a frozen P0 artifact, creates
an actual acquisition occurrence, or emits a defect receipt.
"""

from __future__ import annotations

import argparse
import sys

from dynamics.labs.interp_dialogue_p1_runner import (
    P1PilotContractError,
    verify_all,
    write_all,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--write",
        action="store_true",
        help="materialize and write every generated P1 artifact",
    )
    mode.add_argument(
        "--verify",
        action="store_true",
        help="rebuild deterministically and compare against checked-in bytes",
    )
    args = parser.parse_args(argv)
    try:
        if args.write:
            for relpath in write_all():
                print(f"wrote {relpath}")
        else:
            verify_all()
            print("all generated P1 artifacts are byte-identical to rebuild")
    except P1PilotContractError as exc:
        print(f"P1 contract failure: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())