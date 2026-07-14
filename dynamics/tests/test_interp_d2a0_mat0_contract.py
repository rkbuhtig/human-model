from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from dynamics.labs.interp_d1_common import file_sha256
from dynamics.labs.interp_d2a0_mat0_contract import (
    D2A0Mat0ContractError,
    EXEC0_MANIFEST_SHA256,
    MAT0_MANIFEST_SHA256,
    PREDECESSOR_MANIFEST_SHA256,
    load_contract_bundle,
    mutated_bundle,
    validate_contract_bundle,
    verify_frozen_contract,
)


ROOT = Path(__file__).resolve().parents[2]
D2A0 = ROOT / "research/scenarios/interp-dialogue-001/d2a0"
MAT0 = D2A0 / "mat0"


class InterpD2A0Mat0ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = load_contract_bundle()

    def assert_rejected(self, bundle: dict[str, object]) -> None:
        with self.assertRaises(D2A0Mat0ContractError):
            validate_contract_bundle(bundle)

    def test_frozen_mat0_contract_verifies_without_execution(self) -> None:
        self.assertEqual(
            verify_frozen_contract(),
            {
                "composed_runner_input_count": 16,
                "fixture_program_count": 9,
                "cell_program_count": 10,
                "record_type_count": 11,
                "lifecycle_program_count": 7,
                "rejection_rule_count": 8,
                "golden_trace_count": 3,
                "frozen_artifact_count": 12,
            },
        )

    def test_predecessor_and_exec0_manifests_are_byte_identical(self) -> None:
        self.assertEqual(
            file_sha256(D2A0 / "frozen-artifact-manifest-v0.json"),
            PREDECESSOR_MANIFEST_SHA256,
        )
        self.assertEqual(
            file_sha256(D2A0 / "exec0/frozen-artifact-manifest-v0.json"),
            EXEC0_MANIFEST_SHA256,
        )
        self.assertEqual(
            file_sha256(MAT0 / "frozen-artifact-manifest-v0.json"),
            MAT0_MANIFEST_SHA256,
        )

    def test_mat0_contains_no_runner_evaluator_or_result(self) -> None:
        names = {path.name for path in MAT0.iterdir()}
        self.assertNotIn("run-v1.json", names)
        self.assertNotIn("evaluation-v1.json", names)
        self.assertFalse((ROOT / "dynamics/labs/interp_d2a1_runner.py").exists())
        self.assertFalse((ROOT / "dynamics/labs/interp_d2a1_evaluator.py").exists())

    def test_every_mat0_document_binds_both_frozen_predecessors(self) -> None:
        for kind, document in self.bundle.items():
            if kind in {"contract_schema", "evaluation_schema", "publication_schema", "exec0_bundle"}:
                continue
            self.assertEqual(document["predecessor_manifest_sha256"], PREDECESSOR_MANIFEST_SHA256)
            self.assertEqual(document["exec0_manifest_sha256"], EXEC0_MANIFEST_SHA256)

    def test_strategy_catalog_is_explicit_runner_input(self) -> None:
        bundle = mutated_bundle()
        rows = bundle["composed_runner_input"]["payload"]["predecessor_runner_visible_documents"]
        rows[:] = [row for row in rows if row["document_kind"] != "strategy_catalog"]
        self.assert_rejected(bundle)

    def test_mat0_manifest_is_the_runner_bootstrap_authority(self) -> None:
        bootstrap = self.bundle["composed_runner_input"]["payload"]["mat0_bootstrap"]
        self.assertEqual(bootstrap["path"], "frozen-artifact-manifest-v0.json")
        bundle = mutated_bundle()
        bundle["composed_runner_input"]["payload"]["mat0_bootstrap"]["path"] = "discover.json"
        self.assert_rejected(bundle)

    def test_runtime_spine_binding_cannot_change(self) -> None:
        bundle = mutated_bundle()
        bundle["composed_runner_input"]["payload"]["predecessor_runner_visible_documents"][0]["sha256"] = "0" * 64
        self.assert_rejected(bundle)

    def test_predecessor_supplied_path_has_two_target_fields(self) -> None:
        bundle = mutated_bundle()
        adapter = bundle["fixture_normalization"]["payload"]["field_adapters"][0]
        adapter["targets"] = ["supplied_path"]
        self.assert_rejected(bundle)

    def test_predecessor_path_vocabulary_must_be_closed(self) -> None:
        bundle = mutated_bundle()
        del bundle["fixture_normalization"]["payload"]["path_value_adapter"]["PATH-SHARED"]
        self.assert_rejected(bundle)

    def test_opaque_subjective_paths_do_not_gain_rank_difference(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_normalization"]["payload"]["path_value_adapter"]["PATH-B"] = "PATH-ADVERSE"
        self.assert_rejected(bundle)

    def test_raw_subjective_identity_must_be_preserved(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_normalization"]["payload"]["source_identity_rule"] = "discard raw token"
        self.assert_rejected(bundle)

    def test_fixture_merge_precedence_is_frozen(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_normalization"]["payload"]["merge_precedence"].reverse()
        self.assert_rejected(bundle)

    def test_equal_surface_intervention_is_explicit(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_normalization"]["payload"]["fixture_programs"][0]["access_rules"][0]["surface_override"] = "NONE"
        self.assert_rejected(bundle)

    def test_all_nine_fixture_programs_are_exact(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_normalization"]["payload"]["fixture_programs"].pop()
        self.assert_rejected(bundle)

    def test_fixture_program_cannot_materialize_undeclared_access(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_normalization"]["payload"]["fixture_programs"][0]["access_rules"][1]["access_ordinal"] = 99
        self.assert_rejected(bundle)

    def test_cell_program_inventory_is_exact_not_parsed(self) -> None:
        bundle = mutated_bundle()
        bundle["operator_program"]["payload"]["cell_programs"].pop()
        self.assert_rejected(bundle)

    def test_cell_operator_binding_cannot_change(self) -> None:
        bundle = mutated_bundle()
        bundle["operator_program"]["payload"]["cell_programs"][0]["temporal_operator"] = "D2A-T3-REVISE"
        self.assert_rejected(bundle)

    def test_cell_id_parsing_is_forbidden(self) -> None:
        bundle = mutated_bundle()
        bundle["operator_program"]["payload"]["forbidden_shortcuts"].remove("PARSE_CELL_ID")
        self.assert_rejected(bundle)

    def test_absent_revision_has_exact_sentinel(self) -> None:
        bundle = mutated_bundle()
        bundle["operator_program"]["payload"]["intermediate_construction"]["revision_path_absence_sentinel"] = "NONE"
        self.assert_rejected(bundle)

    def test_prior_revision_application_precedes_interpretation(self) -> None:
        stages = self.bundle["operator_program"]["payload"]["per_access_stage_order"]
        self.assertLess(
            stages.index("APPLY_MATCHING_PRIOR_REVISION_FOR_ACCESS_IF_SCHEDULED"),
            stages.index("FORM_RECEPTION_CANDIDATE"),
        )

    def test_candidate_set_binds_same_access_application(self) -> None:
        rows = self.bundle["record_materialization"]["payload"]["stage_ranks"]
        candidate = next(row for row in rows if row["type_id"] == "InterpretationCandidateSet")
        self.assertIn("AccessLocalApplicationReceipt when emitted", candidate["source_types"])

    def test_record_stage_ranks_are_exact(self) -> None:
        bundle = mutated_bundle()
        bundle["record_materialization"]["payload"]["stage_ranks"][0]["rank"] = 2
        self.assert_rejected(bundle)

    def test_record_payload_contract_cannot_widen(self) -> None:
        bundle = mutated_bundle()
        bundle["record_materialization"]["payload"]["payload_contract"]["ReceptionCandidate"].append("expected_relation")
        self.assert_rejected(bundle)

    def test_record_source_must_precede_writer(self) -> None:
        bundle = mutated_bundle()
        bundle["record_materialization"]["payload"]["stage_ranks"][1]["source_types"] = ["RetentionObservationReceipt"]
        self.assert_rejected(bundle)

    def test_record_source_order_rule_is_frozen(self) -> None:
        bundle = mutated_bundle()
        bundle["record_materialization"]["payload"]["source_record_id_rule"] = "sort source IDs"
        self.assert_rejected(bundle)

    def test_lifecycle_program_inventory_is_exact(self) -> None:
        bundle = mutated_bundle()
        bundle["lifecycle_emission"]["payload"]["programs"].pop()
        self.assert_rejected(bundle)

    def test_future_revision_is_conditionally_applied_at_next_access(self) -> None:
        bundle = mutated_bundle()
        program = bundle["lifecycle_emission"]["payload"]["programs"][1]
        program["read"][0]["condition"] = "ALWAYS"
        self.assert_rejected(bundle)

    def test_eligible_not_read_emits_no_read_receipt(self) -> None:
        bundle = mutated_bundle()
        program = bundle["lifecycle_emission"]["payload"]["programs"][3]
        program["read"] = [{"access_ordinal": 2, "read_status": "READ"}]
        self.assert_rejected(bundle)

    def test_revision_read_selection_is_exact_and_fail_closed(self) -> None:
        bundle = mutated_bundle()
        bundle["lifecycle_emission"]["payload"]["revision_read_selection_rule"] = "take first match"
        self.assert_rejected(bundle)

    def test_applied_not_retained_has_negative_observation(self) -> None:
        bundle = mutated_bundle()
        bundle["lifecycle_emission"]["payload"]["programs"][5]["observe"][0]["observation_status"] = "OBSERVED_RETAINED"
        self.assert_rejected(bundle)

    def test_rejection_precedence_is_exact(self) -> None:
        bundle = mutated_bundle()
        bundle["rejection_materialization"]["payload"]["rows"].reverse()
        self.assert_rejected(bundle)

    def test_rejection_vocabulary_matches_exec0(self) -> None:
        bundle = mutated_bundle()
        bundle["rejection_materialization"]["payload"]["rows"][0]["rejection_code"] = "FREE_FORM"
        self.assert_rejected(bundle)

    def test_same_access_rejection_stage_is_exact(self) -> None:
        bundle = mutated_bundle()
        bundle["rejection_materialization"]["payload"]["rows"][3]["rejected_stage"] = "ADJUDICATE_SCOPED_CANDIDATES"
        self.assert_rejected(bundle)

    def test_rejection_offending_input_refs_are_not_free_form(self) -> None:
        bundle = mutated_bundle()
        bundle["rejection_materialization"]["payload"]["rows"][1]["offending_input_refs"] = ["something went wrong"]
        self.assert_rejected(bundle)

    def test_digest_target_inventory_is_exact(self) -> None:
        bundle = mutated_bundle()
        bundle["digest_contract"]["payload"]["digest_rules"].pop()
        self.assert_rejected(bundle)

    def test_persisted_artifacts_require_one_lf(self) -> None:
        bundle = mutated_bundle()
        bundle["digest_contract"]["payload"]["serialization_rule"] = "platform newline"
        self.assert_rejected(bundle)

    def test_evaluation_schema_has_four_status_mapping_rules(self) -> None:
        bundle = mutated_bundle()
        bundle["evaluation_schema"]["$defs"]["assertionResult"]["allOf"].pop()
        self.assert_rejected(bundle)

    def test_evaluation_resolved_operand_is_auditable(self) -> None:
        bundle = mutated_bundle()
        bundle["evaluation_schema"]["$defs"]["recordResolvedOperand"]["required"].remove("record_id")
        self.assert_rejected(bundle)

    def test_trace_operand_omits_record_only_fields(self) -> None:
        trace_operand = self.bundle["evaluation_schema"]["$defs"]["traceResolvedOperand"]
        self.assertNotIn("record_id", trace_operand["properties"])
        self.assertNotIn("access_ordinal", trace_operand["properties"])

    def test_run_status_precedence_includes_not_applicable(self) -> None:
        rules = self.bundle["evaluation_schema"]["x-semantic-rules"]
        self.assertEqual(
            rules[-3:],
            [
                "one or more VIOLATED results yields DOES_NOT_CONFORM",
                "otherwise one or more NOT_EVALUABLE results yields PARTIALLY_EVALUABLE",
                "otherwise SATISFIED and NOT_APPLICABLE results yield CONFORMS_WITHIN_REGISTERED_SCOPE",
            ],
        )

    def test_evaluation_artifact_must_bind_mat0(self) -> None:
        bundle = mutated_bundle()
        bundle["evaluation_schema"]["required"].remove("mat0_manifest_sha256")
        self.assert_rejected(bundle)

    def test_publication_carrier_binds_run_evaluation_and_sources(self) -> None:
        bundle = mutated_bundle()
        bundle["publication_schema"]["required"].remove("mat0_manifest_sha256")
        self.assert_rejected(bundle)

    def test_publication_forbids_timestamp_identity(self) -> None:
        bundle = mutated_bundle()
        bundle["source_bundle_contract"]["payload"]["publication_carrier"]["timestamp_policy"] = "OPTIONAL"
        self.assert_rejected(bundle)

    def test_future_source_bundle_paths_are_exact(self) -> None:
        bundle = mutated_bundle()
        bundle["source_bundle_contract"]["payload"]["bundles"][0]["paths"].pop()
        self.assert_rejected(bundle)

    def test_source_bundle_requires_transitive_repo_local_closure(self) -> None:
        bundle = mutated_bundle()
        bundle["source_bundle_contract"]["payload"]["repo_local_import_policy"] = "DIRECT_IMPORTS_ONLY"
        self.assert_rejected(bundle)

    def test_runner_evaluator_cross_imports_remain_forbidden(self) -> None:
        bundle = mutated_bundle()
        bundle["source_bundle_contract"]["payload"]["cross_role_import_policy"].pop()
        self.assert_rejected(bundle)

    def test_three_golden_traces_are_exact_canonical_bytes(self) -> None:
        cases = self.bundle["materialization_golden_traces"]["payload"]["cases"]
        self.assertEqual(
            {case["case_kind"] for case in cases},
            {"COMPLETED_SINGLE_ACCESS", "TYPED_REJECTED_TRACE", "COMPLETED_MULTI_ACCESS"},
        )
        validate_contract_bundle(self.bundle)

    def test_golden_payload_mutation_is_rejected(self) -> None:
        bundle = mutated_bundle()
        trace = bundle["materialization_golden_traces"]["payload"]["cases"][0]["expected_trace"]
        trace["records"][0]["payload"]["runtime_id"] = "RUNTIME-MUTATED"
        self.assert_rejected(bundle)

    def test_golden_input_mutation_is_rejected_by_semantic_derivation(self) -> None:
        bundle = mutated_bundle()
        case = bundle["materialization_golden_traces"]["payload"]["cases"][0]
        case["normalized_unit_input"]["access_plan"][0]["supplied_path"] = "PATH-BENIGN"
        self.assert_rejected(bundle)

    def test_multi_access_golden_applies_revision_before_t3(self) -> None:
        case = next(
            row for row in self.bundle["materialization_golden_traces"]["payload"]["cases"]
            if row["case_id"] == "GOLDEN-MULTI-ACCESS-LIFECYCLE"
        )
        access_two = [
            row for row in case["expected_trace"]["records"]
            if row["access_ordinal"] == 2
        ]
        types = [row["type_id"] for row in access_two]
        self.assertLess(types.index("AccessLocalApplicationReceipt"), types.index("ScopedAdjudicationReceipt"))
        candidates = next(row for row in access_two if row["type_id"] == "InterpretationCandidateSet")
        adjudication = next(row for row in access_two if row["type_id"] == "ScopedAdjudicationReceipt")
        self.assertEqual(candidates["payload"]["candidate_paths"], ["PATH-BENIGN", "PATH-ADVERSE"])
        self.assertEqual(adjudication["payload"]["adjudicated_path"], "PATH-ADVERSE")

    def test_golden_forward_source_reference_is_rejected(self) -> None:
        bundle = mutated_bundle()
        trace = bundle["materialization_golden_traces"]["payload"]["cases"][0]["expected_trace"]
        trace["records"][0]["source_record_ids"] = [trace["records"][1]["record_id"]]
        self.assert_rejected(bundle)

    def test_golden_traces_cannot_become_runner_visible(self) -> None:
        bundle = mutated_bundle()
        bundle["materialization_golden_traces"]["payload"]["lane"] = "RUNNER_VISIBLE"
        self.assert_rejected(bundle)

    def test_selector_access_must_exist_in_fixture_lineage(self) -> None:
        bundle = mutated_bundle()
        assertion = bundle["exec0_bundle"]["evaluation_manifest"]["payload"]["assertions"][0]
        assertion["operands"][0]["access_ordinal"] = 99
        self.assert_rejected(bundle)

    def test_frozen_artifact_lane_mutation_is_rejected(self) -> None:
        bundle = mutated_bundle()
        bundle["frozen_artifact_manifest"]["payload"]["artifacts"][-1]["visibility_lane"] = "RUNNER_VISIBLE"
        with self.assertRaises(D2A0Mat0ContractError):
            validate_contract_bundle(bundle, verify_files=True)

    def test_mutation_helper_is_deep_copy(self) -> None:
        bundle = mutated_bundle()
        bundle["fixture_normalization"]["payload"]["path_value_adapter"]["PATH-A"] = "MUTATED"
        fresh = load_contract_bundle()
        self.assertEqual(
            fresh["fixture_normalization"]["payload"]["path_value_adapter"]["PATH-A"],
            "PATH-AMBIGUOUS",
        )

    def test_loaded_bundle_is_stable_under_deepcopy(self) -> None:
        self.assertEqual(self.bundle, deepcopy(self.bundle))


if __name__ == "__main__":
    unittest.main()
