from __future__ import annotations

import argparse

from dynamics.labs.interp_d2a0_mat0_contract import verify_frozen_contract


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify frozen INTERP-001D2a0-MAT0 without executing it."
    )
    parser.add_argument("--verify", action="store_true", help="verify frozen MAT0")
    arguments = parser.parse_args()
    if not arguments.verify:
        parser.error("--verify is required; MAT0 has no runner or writer")
    summary = verify_frozen_contract()
    counts = ", ".join(f"{key}={value}" for key, value in sorted(summary.items()))
    print(f"INTERP-001D2a0-MAT0 FROZEN / UNEXECUTED: {counts}")


if __name__ == "__main__":
    main()
