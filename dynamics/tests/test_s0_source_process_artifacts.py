from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "research/benchmarks/sources"


class SourceProcessArtifactTests(unittest.TestCase):
    def test_all_source_process_json_artifacts_parse(self) -> None:
        names = (
            "sim-rel-boundary-family-002-public.json",
            "sim-rel-boundary-family-002-hyperprior.json",
            "sim-rel-boundary-family-002-runtime.json",
            "s0-public-event-v3.json",
            "sim-rel-boundary-family-002-process-adequacy.json",
            "sim-rel-boundary-family-002-calibration-report.json",
            "s0-source-process-activation-gate.json",
            "s0-structural-predicates-v3.json",
        )
        for name in names:
            with self.subTest(name=name):
                json.loads((SOURCE_DIR / name).read_text()) if name.startswith("sim-") or name.startswith("s0-public") or name.startswith("s0-source") else json.loads((ROOT / "research/benchmarks" / name).read_text())

    def test_beacon_and_materialization_remain_absent(self) -> None:
        gate = json.loads((SOURCE_DIR / "s0-source-process-activation-gate.json").read_text())
        self.assertFalse(gate["beacon"]["authorized"])
        self.assertIsNone(gate["beacon"]["family_seed"])
        self.assertTrue(all(value == 0 for value in gate["materialization"].values()))
        self.assertFalse(gate["model_compatibility"]["present"])

    def test_claim_authority_is_co_designed_process_conditional(self) -> None:
        public = json.loads((SOURCE_DIR / "sim-rel-boundary-family-002-public.json").read_text())
        self.assertEqual(
            public["claim_authority"],
            "NON_HUMAN_CO_DESIGNED_PROCESS_CONDITIONAL_ADEQUACY_ONLY",
        )


if __name__ == "__main__":
    unittest.main()
