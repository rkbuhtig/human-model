from __future__ import annotations

import argparse

from dynamics.labs.interp_d2a0_exec0_contract import verify_frozen_contract


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the frozen, unexecuted INTERP-001D2a0-EXEC0 closure"
    )
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if not args.verify:
        parser.error("--verify is required; EXEC0 has no runner, evaluator or writer")
    summary = verify_frozen_contract()
    print(
        "INTERP-001D2a0-EXEC0 FROZEN / UNEXECUTED: "
        + ", ".join(f"{key}={value}" for key, value in sorted(summary.items()))
    )


if __name__ == "__main__":
    main()
