from __future__ import annotations

from pathlib import Path
import unittest

from dynamics.labs.interp_d2a0_exec0_contract import (
    D2A0_DIR,
    EXEC0_DIR,
    PREDECESSOR_MANIFEST_SHA256,
    D2A0Exec0ContractError,
    load_contract_bundle,
    mutated_bundle,
    validate_contract_bundle,
    verify_frozen_contract,
)
from dynamics.labs.interp_d1_common import file_sha256


def _row(rows: list[dict], key: str, value: str) -> dict:
    return next(row for row in rows if row[key] == value)


class InterpD2A0Exec0ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = load_contract_bundle()

    def test_frozen_exec0_contract_verifies_without_execution(self) -> None:
        self.assertEqual(
            verify_frozen_contract(),
            {
                "operator_count": 8,
                "golden_vector_count": 20,
                "extension_fixture_count": 3,
                "execution_unit_count": 46,
                "assertion_count": 20,
                "frozen_artifact_count": 10,
            },
        )

    def test_predecessor_frozen_manifest_is_byte_identical(self) -> None:
        self.assertEqual(
            file_sha256(D2A0_DIR / "frozen-artifact-manifest-v0.json"),
            PREDECESSOR_MANIFEST_SHA256,
        )

    def test_exec0_contains_no_runner_evaluator_or_result(self) -> None:
        labs = Path(__file__).resolve().parents[1] / "labs"
        for name in (
            "interp_d2a1_runner.py",
            "interp_d2a1_evaluator.py",
            "interp_d2a1_run_cli.py",
            "interp_d2a1_evaluate_cli.py",
        ):
            self.assertFalse((labs / name).exists(), name)
        for name in ("run-v1.json", "evaluation-receipt-v1.json", "result-v1.json"):
            self.assertFalse((EXEC0_DIR / name).exists(), name)

    def test_all_documents_bind_one_predecessor(self) -> None:
        for kind in (
            "operator_catalog", "operator_golden_vectors", "fixture_extension",
            "execution_unit_manifest", "lifecycle_processor", "evaluator_policy",
            "evaluation_manifest", "frozen_artifact_manifest",
        ):
            self.assertEqual(
                self.bundle[kind]["predecessor_manifest_sha256"],
                PREDECESSOR_MANIFEST_SHA256,
            )

    def test_temporal_operator_cannot_read_role(self) -> None:
        bundle = mutated_bundle()
        operator = _row(
            bundle["operator_catalog"]["payload"]["operators"],
            "operator_id",
            "D2A-T2-ACCUMULATE",
        )
        operator["forbidden_reads"].remove("role")
        with self.assertRaisesRegex(D2A0Exec0ContractError, "may read role"):
            validate_contract_bundle(bundle)

    def test_projection_operator_cannot_write_revision(self) -> None:
        bundle = mutated_bundle()
        operator = _row(
            bundle["operator_catalog"]["payload"]["operators"],
            "operator_id",
            "D2A-P1-ROLE",
        )
        operator["forbidden_writes"].remove("revision_decision")
        with self.assertRaisesRegex(D2A0Exec0ContractError, "revision authority"):
            validate_contract_bundle(bundle)

    def test_operator_randomness_is_rejected(self) -> None:
        bundle = mutated_bundle()
        bundle["operator_catalog"]["payload"]["randomness_policy"] = "SEEDED"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "randomness"):
            validate_contract_bundle(bundle)

    def test_every_operator_has_contract_test_only_golden_vector(self) -> None:
        vectors = self.bundle["operator_golden_vectors"]["payload"]["vectors"]
        operators = self.bundle["operator_catalog"]["payload"]["operators"]
        self.assertEqual(
            {row["operator_id"] for row in vectors},
            {row["operator_id"] for row in operators},
        )
        self.assertEqual(
            self.bundle["operator_golden_vectors"]["payload"]["visibility"],
            "CONTRACT_TEST_ONLY_NOT_RUNNER_INPUT",
        )

    def test_t1_mask_golden_semantics_are_closed(self) -> None:
        bundle = mutated_bundle()
        vector = _row(
            bundle["operator_golden_vectors"]["payload"]["vectors"],
            "vector_id",
            "GV-T1-MASK",
        )
        vector["expected"]["adjudicated_path"] = "PATH-ADVERSE"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "T1 masked"):
            validate_contract_bundle(bundle)

    def test_fixture_extension_cannot_contain_expected_relation(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_extension"]["payload"]["fixtures"][0][
            "expected_relation"
        ] = "NOT_EQUAL"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "leaks"):
            validate_contract_bundle(bundle)

    def test_execution_units_are_explicit_and_ordered(self) -> None:
        units = self.bundle["execution_unit_manifest"]["payload"]["execution_units"]
        self.assertEqual(
            [row["execution_unit_id"] for row in units],
            [f"U{index:03d}" for index in range(1, 47)],
        )
        self.assertEqual(
            [row["trace_id"] for row in units],
            [f"TRACE-U{index:03d}" for index in range(1, 47)],
        )

    def test_execution_unit_unknown_arm_is_rejected(self) -> None:
        bundle = mutated_bundle()
        bundle["execution_unit_manifest"]["payload"]["execution_units"][0][
            "arm_id"
        ] = "UNKNOWN"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "unknown fixture arm"):
            validate_contract_bundle(bundle)

    def test_h0_execution_unit_cannot_use_heterogeneous_profile(self) -> None:
        bundle = mutated_bundle()
        bundle["execution_unit_manifest"]["payload"]["execution_units"][0][
            "profile_id"
        ] = "HET-B"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "invalid cell/profile"):
            validate_contract_bundle(bundle)

    def test_runner_visibility_excludes_golden_and_evaluator_inputs(self) -> None:
        bundle = mutated_bundle()
        bundle["execution_unit_manifest"]["payload"]["runner_visible_inputs"].append(
            "operator_golden_vectors"
        )
        with self.assertRaisesRegex(D2A0Exec0ContractError, "visibility lanes overlap"):
            validate_contract_bundle(bundle)

    def test_lifecycle_dependency_order_begins_with_adjudication(self) -> None:
        bundle = mutated_bundle()
        order = bundle["lifecycle_processor"]["payload"]["dependency_order"]
        order[0], order[1] = order[1], order[0]
        with self.assertRaisesRegex(D2A0Exec0ContractError, "dependency order"):
            validate_contract_bundle(bundle)

    def test_lifecycle_receipts_have_separate_processor_steps(self) -> None:
        steps = self.bundle["lifecycle_processor"]["payload"]["steps"]
        self.assertEqual(
            [row["step_id"] for row in steps],
            [
                "READ_ELIGIBLE_REVISION",
                "APPLY_REVISION_FOR_ACCESS",
                "OBSERVE_RETENTION",
            ],
        )

    def test_typed_rejection_continues_unit_run_only(self) -> None:
        semantics = self.bundle["lifecycle_processor"]["payload"][
            "terminal_semantics"
        ]
        self.assertEqual(
            semantics["typed_policy_rejection"],
            "TERMINATE_UNIT_AND_CONTINUE_RUN",
        )
        self.assertEqual(
            semantics["malformed_contract_or_digest"], "ABORT_WHOLE_RUN"
        )

    def test_completed_and_rejected_trace_are_disjoint(self) -> None:
        trace = self.bundle["trace_schema"]
        completed = trace["$defs"]["completedTrace"]
        rejected = trace["$defs"]["rejectedTrace"]
        self.assertNotIn("rejection_receipt", completed["properties"])
        self.assertIn("rejection_receipt", rejected["required"])

    def test_rejection_schema_matches_lifecycle_vocabulary(self) -> None:
        bundle = mutated_bundle()
        codes = bundle["trace_schema"]["$defs"]["rejectionReceipt"]["properties"][
            "rejection_code"
        ]["enum"]
        codes.pop()
        with self.assertRaisesRegex(D2A0Exec0ContractError, "rejection codes"):
            validate_contract_bundle(bundle)

    def test_assertion_status_is_not_interpretation_code(self) -> None:
        policy = self.bundle["evaluator_policy"]["payload"]
        self.assertFalse(
            set(policy["assertion_evaluation_statuses"])
            & set(policy["interpretation_codes"])
        )

    def test_selector_unknown_execution_unit_is_rejected(self) -> None:
        bundle = mutated_bundle()
        assertion = bundle["evaluation_manifest"]["payload"]["assertions"][0]
        assertion["operands"][0]["execution_unit_id"] = "U999"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "unknown execution unit"):
            validate_contract_bundle(bundle)

    def test_selector_cannot_cross_fixture(self) -> None:
        bundle = mutated_bundle()
        assertion = bundle["evaluation_manifest"]["payload"]["assertions"][0]
        assertion["operands"][0]["execution_unit_id"] = "U007"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "crosses"):
            validate_contract_bundle(bundle)

    def test_selector_cardinality_is_exactly_one(self) -> None:
        bundle = mutated_bundle()
        assertion = bundle["evaluation_manifest"]["payload"]["assertions"][0]
        assertion["operands"][0]["cardinality"] = "FIRST"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "EXACTLY_ONE"):
            validate_contract_bundle(bundle)

    def test_selector_pointer_must_exist_in_record_payload_contract(self) -> None:
        bundle = mutated_bundle()
        assertion = bundle["evaluation_manifest"]["payload"]["assertions"][0]
        assertion["operands"][0]["json_pointer"] = "/payload/hidden_answer"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "outside record payload"):
            validate_contract_bundle(bundle)

    def test_predicate_arity_is_closed(self) -> None:
        bundle = mutated_bundle()
        assertion = bundle["evaluation_manifest"]["payload"]["assertions"][0]
        assertion["operands"].pop()
        with self.assertRaisesRegex(D2A0Exec0ContractError, "arity"):
            validate_contract_bundle(bundle)

    def test_predicate_relation_is_closed(self) -> None:
        bundle = mutated_bundle()
        assertion = bundle["evaluation_manifest"]["payload"]["assertions"][0]
        assertion["expected_relation"] = "GREATER_THAN"
        with self.assertRaisesRegex(D2A0Exec0ContractError, "relation mismatch"):
            validate_contract_bundle(bundle)

    def test_all_nine_fixtures_have_typed_assertions(self) -> None:
        fixture_ids = {
            row["fixture_id"]
            for row in self.bundle["evaluation_manifest"]["payload"]["assertions"]
        }
        self.assertEqual(len(fixture_ids), 9)
        self.assertTrue(
            {
                "FX-TRANSIENT-GATE",
                "FX-BOUNDED-ACCUMULATION",
                "FX-DECLARED-PROFILE-DISSOCIATION",
            }
            <= fixture_ids
        )

    def test_mutation_helper_is_deep_copy(self) -> None:
        bundle = mutated_bundle()
        bundle["operator_catalog"]["status"] = "CHANGED"
        self.assertEqual(self.bundle["operator_catalog"]["status"], "FROZEN_UNEXECUTED")


if __name__ == "__main__":
    unittest.main()
