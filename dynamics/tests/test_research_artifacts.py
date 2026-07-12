from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]

CLAIM_ID = re.compile(r"^HM-(TYPE|INV|DYN|MEAS|META)-[0-9]{3}$")
DEFECT_ID = re.compile(r"^HM-DEFECT-[A-Z0-9-]+$")
HEX_40 = re.compile(r"^[0-9a-f]{40}$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
LINE_RANGE = re.compile(r"^[0-9]+(?:-[0-9]+)?$")

CLAIM_KINDS = {
    "TYPE",
    "INVARIANT",
    "DYNAMICAL_HYPOTHESIS",
    "MEASUREMENT_MODEL",
    "METAPHOR",
}
ADOPTION_STATUSES = {"DRAFT", "PROPOSED", "ADOPTED", "REVISED", "REJECTED", "HOLD"}
IMPLEMENTATION_STATUSES = {
    "NOT_APPLICABLE",
    "UNIMPLEMENTED",
    "PARTIAL",
    "IMPLEMENTED",
}
CLAIM_REQUIRED = {
    "id",
    "kind",
    "adoption_status",
    "implementation_status",
    "statement",
    "scope",
    "exclusions",
    "depends_on",
    "support",
    "failure_condition",
}
CLAIM_OPTIONAL = {"notes"}
DEFECT_CLASSES = {
    "ILLEGAL_CAST",
    "UNAUTHORIZED_WRITE",
    "PROVENANCE_LOSS",
    "SCOPE_COLLAPSE",
    "TEMPORAL_ALIASING",
    "IDENTITY_COLLISION",
    "ORACLE_LEAKAGE",
}


def _assert_string_list(test: unittest.TestCase, values: object, *, nonempty: bool = False) -> None:
    test.assertIsInstance(values, list)
    if nonempty:
        test.assertTrue(values)
    test.assertEqual(len(values), len(set(values)))
    test.assertTrue(all(isinstance(value, str) and value for value in values))


class ResearchArtifactTests(unittest.TestCase):
    def test_claim_registry_has_typed_failure_conditions(self) -> None:
        registry = json.loads((ROOT / "research/claims/registry.json").read_text())
        self.assertEqual(set(registry), {"schema_version", "claims"})
        self.assertEqual(registry["schema_version"], "1.0.0")
        expected_failure = {
            "TYPE": "INVALID_CONSTRUCTION",
            "INVARIANT": "COUNTEREXAMPLE_TRACE",
            "DYNAMICAL_HYPOTHESIS": "DISCRIMINATING_OBSERVATION",
            "MEASUREMENT_MODEL": "CALIBRATION_OR_IDENTIFIABILITY_FAILURE",
            "METAPHOR": "MISUSE_AS_EVIDENCE",
        }
        ids: set[str] = set()
        for claim in registry["claims"]:
            self.assertEqual(set(claim) - CLAIM_OPTIONAL, CLAIM_REQUIRED)
            self.assertFalse(set(claim) - CLAIM_REQUIRED - CLAIM_OPTIONAL)
            self.assertRegex(claim["id"], CLAIM_ID)
            self.assertNotIn(claim["id"], ids)
            ids.add(claim["id"])
            self.assertIn(claim["kind"], CLAIM_KINDS)
            self.assertIn(claim["adoption_status"], ADOPTION_STATUSES)
            self.assertIn(claim["implementation_status"], IMPLEMENTATION_STATUSES)
            _assert_string_list(self, claim["scope"], nonempty=True)
            _assert_string_list(self, claim["exclusions"])
            _assert_string_list(self, claim["depends_on"])
            self.assertEqual(
                claim["failure_condition"]["type"],
                expected_failure[claim["kind"]],
            )
            self.assertEqual(
                set(claim["failure_condition"]), {"type", "description"}
            )
            self.assertTrue(claim["failure_condition"]["description"])
            self.assertEqual(
                set(claim["support"]),
                {"historical_cases", "structural_tests", "empirical_datasets"},
            )
            for values in claim["support"].values():
                _assert_string_list(self, values)

    def test_defect_case_separates_record_from_retrospective_reading(self) -> None:
        path = ROOT / "research/defects/cases/event-count-slow-update-v01.json"
        case = json.loads(path.read_text())
        self.assertEqual(
            set(case),
            {
                "schema_version",
                "id",
                "source",
                "artifact_status",
                "branch_status",
                "contemporaneous_record",
                "retrospective_interpretation",
                "principle_value",
            },
        )
        self.assertEqual(case["schema_version"], "1.0.0")
        self.assertRegex(case["id"], DEFECT_ID)
        self.assertEqual(case["artifact_status"], "OBSERVED_FAILURE")
        self.assertIn(
            case["artifact_status"],
            {"OBSERVED_FAILURE", "LATENT_DESIGN_RISK", "AUTHOR_CLAIM"},
        )
        self.assertIn(
            case["branch_status"],
            {"ADOPTED", "SIDE_BRANCH", "LATER_NOT_SELECTED", "UNKNOWN"},
        )
        self.assertIn("contemporaneous_record", case)
        self.assertIn("retrospective_interpretation", case)
        self.assertRegex(case["source"]["baseline_commit"], HEX_40)
        for artifact in case["source"]["artifacts"]:
            self.assertEqual(set(artifact), {"path", "sha256", "line_ranges"})
            self.assertRegex(artifact["sha256"], HEX_64)
            source = ROOT / artifact["path"]
            self.assertTrue(source.is_file(), artifact["path"])
            self.assertEqual(
                hashlib.sha256(source.read_bytes()).hexdigest(), artifact["sha256"]
            )
            line_count = len(source.read_text().splitlines())
            for line_range in artifact["line_ranges"]:
                self.assertRegex(line_range, LINE_RANGE)
                bounds = [int(value) for value in line_range.split("-")]
                self.assertGreaterEqual(bounds[0], 1)
                self.assertLessEqual(bounds[-1], line_count)
                self.assertEqual(bounds, sorted(bounds))

        self.assertEqual(
            set(case["contemporaneous_record"]),
            {
                "observed_behavior",
                "contemporaneous_diagnosis",
                "historical_repair",
                "observed_side_effect",
            },
        )
        retrospective = case["retrospective_interpretation"]
        self.assertEqual(
            set(retrospective),
            {
                "defect_classes",
                "candidate_principles",
                "competing_repairs",
                "legal_control_cases",
                "minimal_counterexample",
                "current_regression_tests",
                "empirical_status",
            },
        )
        self.assertTrue(set(retrospective["defect_classes"]) <= DEFECT_CLASSES)
        self.assertTrue(retrospective["candidate_principles"])
        for candidate in retrospective["candidate_principles"]:
            self.assertEqual(
                set(candidate),
                {
                    "principle_id",
                    "statement",
                    "predicted_repairs",
                    "prohibited_legal_behavior",
                    "failure_condition",
                },
            )
            self.assertTrue(candidate["principle_id"])
            self.assertTrue(candidate["statement"])
            _assert_string_list(self, candidate["predicted_repairs"])
            _assert_string_list(self, candidate["prohibited_legal_behavior"])
            self.assertTrue(candidate["failure_condition"])
        self.assertTrue(retrospective["competing_repairs"])
        self.assertTrue(retrospective["legal_control_cases"])
        _assert_string_list(self, retrospective["competing_repairs"], nonempty=True)
        _assert_string_list(self, retrospective["legal_control_cases"], nonempty=True)
        _assert_string_list(self, retrospective["current_regression_tests"])
        self.assertEqual(retrospective["empirical_status"], "NOT_TESTED_ON_HUMANS")
        self.assertIn(
            retrospective["empirical_status"],
            {
                "NOT_TESTED_ON_HUMANS",
                "PILOT_ONLY",
                "EMPIRICALLY_CONTESTED",
                "EMPIRICALLY_SUPPORTED",
            },
        )

        principle_value = case["principle_value"]
        self.assertEqual(
            set(principle_value),
            {
                "independent_defects_addressed",
                "discriminating_predictions",
                "blocked_legal_controls",
                "added_degrees_of_freedom",
            },
        )
        for values in principle_value.values():
            _assert_string_list(self, values)

    def test_research_json_files_are_valid_json(self) -> None:
        for path in sorted((ROOT / "research").rglob("*.json")):
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text())


if __name__ == "__main__":
    unittest.main()
