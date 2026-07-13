from __future__ import annotations

from pathlib import Path
import subprocess
import sys


RUN_PATH = "research/benchmarks/interp-001d1-v1-run.json"
REPORT_PATH = "research/benchmarks/interp-001d1-v1-conformance.json"


def generate_artifacts(repository_root: str | Path) -> tuple[Path, Path]:
    """Run the D1 producer to completion before starting its evaluator."""
    root = Path(repository_root)
    benchmark = root / "research" / "benchmarks"
    run_path = root / RUN_PATH
    report_path = root / REPORT_PATH

    subprocess.run(
        [
            sys.executable,
            "-m",
            "dynamics.labs.interp_d1_run_cli",
            "--execution",
            str(benchmark / "interp-001d1-v1-execution.json"),
            "--output",
            str(run_path),
        ],
        cwd=root,
        check=True,
    )

    # The evaluator bytes are not loaded until the runner has exited and the
    # complete serialized run exists.  The orchestrator imports neither role.
    subprocess.run(
        [
            sys.executable,
            "-m",
            "dynamics.labs.interp_d1_evaluate_cli",
            "--execution",
            str(benchmark / "interp-001d1-v1-execution.json"),
            "--evaluation",
            str(benchmark / "interp-001d1-v1-evaluation.json"),
            "--cell-schema",
            str(benchmark / "interp-001d1-v1-result.schema.json"),
            "--run-schema",
            str(benchmark / "interp-001d1-v1-run.schema.json"),
            "--run",
            str(run_path),
            "--policy",
            str(benchmark / "interp-001d1-v1-evaluator-policy.json"),
            "--report-schema",
            str(benchmark / "interp-001d1-v1-conformance-report.schema.json"),
            "--output",
            str(report_path),
        ],
        cwd=root,
        check=True,
    )
    return run_path, report_path


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    run_path, report_path = generate_artifacts(root)
    print(run_path.relative_to(root))
    print(report_path.relative_to(root))


if __name__ == "__main__":
    main()
