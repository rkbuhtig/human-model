"""Write or verify the INTERP-DIALOGUE-001P0-v1 frozen artifact set."""

from __future__ import annotations

import argparse
import sys

from dynamics.labs.interp_dialogue_p0_v1_builder import (
    P0V1ContractError,
    verify_all,
    write_all,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.write:
            for relpath in write_all():
                print(f"wrote {relpath}")
        else:
            verify_all()
            print("all P0-v1 artifacts are byte-identical to rebuild")
    except P0V1ContractError as exc:
        print(f"P0-v1 contract failure: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
