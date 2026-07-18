from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
import unittest

from dynamics.s0 import source_diagnostics_v2
from dynamics.s0.source_diagnostics_v2 import dobrushin_coefficient, process_adequacy_report
from dynamics.s0.source_family_v2 import generate_instance

ROOT = Path(__file__).resolve().parents[2]
HYPERPRIOR = json.loads(
    (ROOT / "research/benchmarks/sources/sim-rel-boundary-family-002-hyperprior.json").read_text()
)


class SourceDiagnosticsV2Tests(unittest.TestCase):
    def test_process_diagnostic_is_model_independent(self) -> None:
        source = inspect.getsource(source_diagnostics_v2)
        for forbidden in ("v2_models", "v3_models", "runner", "scoring", "B2_MINUS_H"):
            self.assertNotIn(forbidden, source)

    def test_generated_instance_passes_registered_memory_and_mixing_bounds(self) -> None:
        seed = hashlib.sha256(b"diagnostic-source").hexdigest()
        instance = generate_instance(HYPERPRIOR, family_seed_hex=seed, instance_index=0)
        report = process_adequacy_report(instance, HYPERPRIOR["process_adequacy"])
        self.assertEqual(report["failures"], [])
        self.assertGreater(report["metrics"]["p2_immediate_predictive_memory_gain_nats"], 0.0)
        self.assertGreater(report["metrics"]["p3_terminal_predictive_memory_gain_nats"], 0.0)

    def test_dobrushin_definition_is_exact_row_tv_maximum(self) -> None:
        scale = 1_000_000
        matrix = [
            [scale, 0],
            [0, scale],
        ]
        self.assertEqual(dobrushin_coefficient(matrix), 1.0)

    def test_calibration_report_contains_no_source_parameters(self) -> None:
        report = json.loads(
            (ROOT / "research/benchmarks/sources/sim-rel-boundary-family-002-calibration-report.json").read_text()
        )
        self.assertFalse(report["source_parameters_retained"])
        self.assertFalse(report["future_beacon_seed_used"])
        self.assertFalse(report["model_outputs_or_scores_read"])


if __name__ == "__main__":
    unittest.main()
