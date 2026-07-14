from __future__ import annotations

import argparse

from dynamics.labs.interp_d2a0_contract import verify_frozen_contract


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the frozen, unexecuted INTERP-001D2a0 contract"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify schemas, semantic boundaries and frozen digests",
    )
    args = parser.parse_args()
    if not args.verify:
        parser.error("--verify is required; D2a0 has no runner or writer")
    summary = verify_frozen_contract()
    print(
        "INTERP-001D2a0 FROZEN / UNEXECUTED: "
        + ", ".join(f"{key}={value}" for key, value in sorted(summary.items()))
    )


if __name__ == "__main__":
    main()
