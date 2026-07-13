from __future__ import annotations

from pathlib import Path
import subprocess
import sys


RUN_PATH = "research/benchmarks/interp-001-m1-v1-run.json"
REPORT_PATH = "research/benchmarks/interp-001-m1-v1-conformance.json"


def generate_artifacts(repository_root: str | Path) -> tuple[Path, Path]:
    root = Path(repository_root)
    benchmark = root / "research" / "benchmarks"
    run_path = root / RUN_PATH
    report_path = root / REPORT_PATH
    subprocess.run(
        [
            sys.executable,
            "-m",
            "dynamics.labs.interp_m1_run_cli",
            "--execution",
            str(benchmark / "interp-001-m1-v1-execution.json"),
            "--output",
            str(run_path),
        ],
        cwd=root,
        check=True,
    )
    # Evaluation bytes are not loaded or passed to the runner.  The evaluator
    # process starts only after the runner exits with a complete serialized run.
    subprocess.run(
        [
            sys.executable,
            "-m",
            "dynamics.labs.interp_m1_evaluate_cli",
            "--execution",
            str(benchmark / "interp-001-m1-v1-execution.json"),
            "--evaluation",
            str(benchmark / "interp-001-m1-v1-evaluation.json"),
            "--cell-schema",
            str(benchmark / "interp-001-m1-v1-result.schema.json"),
            "--run-schema",
            str(benchmark / "interp-001b-m1-run.schema.json"),
            "--run",
            str(run_path),
            "--policy",
            str(benchmark / "interp-001b-m1-evaluator-policy-v1.json"),
            "--report-schema",
            str(benchmark / "interp-001b-m1-conformance-report.schema.json"),
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
