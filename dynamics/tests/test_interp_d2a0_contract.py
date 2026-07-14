from __future__ import annotations

import unittest

from dynamics.labs.interp_d2a0_contract import (
    D2A0ContractError,
    ROOT,
    load_contract_bundle,
    mutated_bundle,
    validate_contract_bundle,
    validate_trace_document,
    verify_frozen_contract,
)


DIGEST = "0" * 64


def _catalog_row(rows: list[dict], key: str, value: str) -> dict:
    return next(row for row in rows if row[key] == value)


def _base_record(**overrides: object) -> dict:
    record = {
        "record_id": "REC-1",
        "type_id": "RevisionCandidateOccurrence",
        "runtime_id": "RUNTIME-E",
        "target_scope_id": "TARGET-E",
        "interpretation_scope_id": "INTERP-E",
        "access_id": "ACCESS-K",
        "access_ordinal": 1,
        "writer_stage": "DECIDE_REVISION_ELIGIBILITY",
        "source_record_ids": [],
        "payload_digest": DIGEST,
        "external_evidence_link_set_digest": DIGEST,
        "evidence_assessment_digest": DIGEST,
        "subjective_path_digest": DIGEST,
        "source_access_ordinal": 1,
        "effective_from_ordinal": 2,
    }
    record.update(overrides)
    return record


def _read_record(**overrides: object) -> dict:
    record = {
        "record_id": "REC-2",
        "type_id": "RevisionReadReceipt",
        "runtime_id": "RUNTIME-E",
        "target_scope_id": "TARGET-E",
        "interpretation_scope_id": "INTERP-E",
        "access_id": "ACCESS-J",
        "access_ordinal": 2,
        "writer_stage": "MATERIALIZE_DECLARED_VIEW",
        "source_record_ids": ["REC-1"],
        "payload_digest": DIGEST,
        "external_evidence_link_set_digest": DIGEST,
        "evidence_assessment_digest": DIGEST,
        "subjective_path_digest": DIGEST,
        "revision_record_id": "REC-1",
        "source_access_ordinal": 1,
        "effective_from_ordinal": 2,
        "read_status": "READ",
    }
    record.update(overrides)
    return record


def _trace(records: list[dict]) -> dict:
    return {
        "trace_id": "TRACE-1",
        "contract_id": "INTERP-001D2A0-V0",
        "execution_manifest_sha256": DIGEST,
        "cell_id": "T3-P0-H0",
        "fixture_id": "FX-REVISION-LIFECYCLE-SEPARATION",
        "arm_id": "READ-NOT-APPLIED",
        "status": "COMPLETED",
        "records": records,
    }


class InterpD2A0ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = load_contract_bundle()

    def test_frozen_contract_verifies_without_execution(self) -> None:
        self.assertEqual(
            verify_frozen_contract(),
            {
                "type_count": 13,
                "stage_count": 7,
                "cell_count": 10,
                "fixture_count": 6,
                "assertion_count": 12,
                "frozen_artifact_count": 8,
            },
        )

    def test_slice_has_no_runner_evaluator_or_result(self) -> None:
        labs = ROOT / "dynamics" / "labs"
        self.assertFalse((labs / "interp_d2a0_runner.py").exists())
        self.assertFalse((labs / "interp_d2a0_evaluator.py").exists())
        d2a0 = ROOT / "research" / "scenarios" / "interp-dialogue-001" / "d2a0"
        self.assertFalse((d2a0 / "run-v0.json").exists())
        self.assertFalse((d2a0 / "result-v0.json").exists())
        self.assertFalse((d2a0 / "evaluation-receipt-v0.json").exists())

    def test_declared_runtime_view_rejects_new_field(self) -> None:
        bundle = mutated_bundle()
        bundle["runtime_spine"]["runtime_view"]["allowed_fields"].append(
            "undeclared_human_state"
        )
        with self.assertRaisesRegex(D2A0ContractError, "runtime view"):
            validate_contract_bundle(bundle)

    def test_stage_may_only_write_detached_trace(self) -> None:
        bundle = mutated_bundle()
        bundle["runtime_spine"]["stages"][0]["may_write"].append("HumanState")
        with self.assertRaisesRegex(D2A0ContractError, "may write"):
            validate_contract_bundle(bundle)

    def test_t0_cannot_be_given_future_revision_authority(self) -> None:
        bundle = mutated_bundle()
        strategy = _catalog_row(
            bundle["strategy_catalog"]["temporal_strategies"],
            "strategy_id",
            "D2A-T0",
        )
        strategy["revision_decisions"].append("ELIGIBLE_FROM_FUTURE_ACCESS")
        with self.assertRaisesRegex(D2A0ContractError, "may not emit"):
            validate_contract_bundle(bundle)

    def test_projection_axis_cannot_gain_revision_authority(self) -> None:
        bundle = mutated_bundle()
        bundle["strategy_catalog"]["projection_strategies"][0][
            "revision_decisions"
        ] = ["NOT_EMITTED"]
        with self.assertRaisesRegex(D2A0ContractError, "non-temporal"):
            validate_contract_bundle(bundle)

    def test_cell_identity_encodes_independent_axes(self) -> None:
        bundle = mutated_bundle()
        bundle["strategy_catalog"]["registered_cells"][0]["cell_id"] = "S0"
        with self.assertRaisesRegex(D2A0ContractError, "does not encode"):
            validate_contract_bundle(bundle)

    def test_random_seed_contract_is_rejected(self) -> None:
        bundle = mutated_bundle()
        bundle["strategy_catalog"]["seed"] = 7
        with self.assertRaises(D2A0ContractError):
            validate_contract_bundle(bundle)

    def test_role_fixture_requires_no_feedback_clamps(self) -> None:
        bundle = mutated_bundle()
        fixture = _catalog_row(
            bundle["fixture_catalog"]["fixtures"],
            "fixture_id",
            "FX-ROLE-PROJECTION-ONLY",
        )
        clamp = _catalog_row(fixture["clamped_fields"], "field", "world_outcome")
        clamp["value"] = "AVAILABLE"
        with self.assertRaisesRegex(D2A0ContractError, "role fixture"):
            validate_contract_bundle(bundle)

    def test_evidence_fixture_requires_exact_authority_clamps(self) -> None:
        bundle = mutated_bundle()
        fixture = _catalog_row(
            bundle["fixture_catalog"]["fixtures"],
            "fixture_id",
            "FX-EVIDENCE-SUBJECTIVE-PATH",
        )
        clamp = _catalog_row(
            fixture["clamped_fields"], "field", "evidence_writer_authority"
        )
        clamp["value"] = "WRITE_ALLOWED"
        with self.assertRaisesRegex(D2A0ContractError, "evidence fixture"):
            validate_contract_bundle(bundle)

    def test_fixture_catalog_rejects_expected_signature_leakage(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_catalog"]["fixtures"][0]["expected_signature"] = "EQUAL"
        with self.assertRaises(D2A0ContractError):
            validate_contract_bundle(bundle)

    def test_execution_manifest_cannot_receive_evaluation_manifest(self) -> None:
        bundle = mutated_bundle()
        bundle["execution_manifest"]["runner_isolation"][
            "permitted_input_kinds"
        ].append("evaluation_manifest")
        with self.assertRaisesRegex(D2A0ContractError, "may not receive"):
            validate_contract_bundle(bundle)

    def test_execution_manifest_rejects_evaluator_only_field(self) -> None:
        bundle = mutated_bundle()
        bundle["execution_manifest"]["expected_signature"] = "NOT_EQUAL"
        with self.assertRaises(D2A0ContractError):
            validate_contract_bundle(bundle)

    def test_evaluation_covers_every_registered_fixture(self) -> None:
        bundle = mutated_bundle()
        bundle["evaluation_manifest"]["assertions"] = [
            row
            for row in bundle["evaluation_manifest"]["assertions"]
            if row["fixture_id"] != "FX-NON-FALSIFIABLE-ESCAPE"
        ]
        with self.assertRaisesRegex(D2A0ContractError, "cover every fixture"):
            validate_contract_bundle(bundle)

    def test_retirement_vocabulary_cannot_claim_global_stage_removal(self) -> None:
        bundle = mutated_bundle()
        bundle["policy"]["retirement_vocabulary"][0] = "STAGE_UNNECESSARY"
        with self.assertRaisesRegex(D2A0ContractError, "retirement vocabulary"):
            validate_contract_bundle(bundle)

    def test_same_access_fixture_is_frozen_as_adversarial_input(self) -> None:
        bundle = mutated_bundle()
        fixture = _catalog_row(
            bundle["fixture_catalog"]["fixtures"],
            "fixture_id",
            "FX-SAME-ACCESS-REJECTION",
        )
        fixture["arms"][0]["assignments"][0]["value"] = 2
        with self.assertRaisesRegex(D2A0ContractError, "same-k"):
            validate_contract_bundle(bundle)

    def test_future_access_revision_read_is_trace_valid(self) -> None:
        validate_trace_document(
            _trace([_base_record(), _read_record()]),
            self.bundle,
        )

    def test_same_access_revision_read_is_hard_rejected(self) -> None:
        read = _read_record(access_id="ACCESS-K", access_ordinal=1)
        with self.assertRaisesRegex(D2A0ContractError, "same-access"):
            validate_trace_document(_trace([_base_record(), read]), self.bundle)

    def test_revision_read_cannot_cross_runtime_or_scope(self) -> None:
        for field, value in (
            ("runtime_id", "RUNTIME-X"),
            ("target_scope_id", "TARGET-X"),
            ("interpretation_scope_id", "INTERP-X"),
        ):
            with self.subTest(field=field):
                read = _read_record(**{field: value})
                with self.assertRaisesRegex(D2A0ContractError, field):
                    validate_trace_document(
                        _trace([_base_record(), read]), self.bundle
                    )

    def test_trace_cannot_forward_reference_source_record(self) -> None:
        trace = _trace([_read_record(), _base_record()])
        with self.assertRaisesRegex(D2A0ContractError, "forward-referenced"):
            validate_trace_document(trace, self.bundle)

    def test_mutation_helper_returns_deep_copy(self) -> None:
        bundle = mutated_bundle()
        bundle["runtime_spine"]["status"] = "CHANGED"
        self.assertEqual(self.bundle["runtime_spine"]["status"], "FROZEN_UNEXECUTED")


if __name__ == "__main__":
    unittest.main()
