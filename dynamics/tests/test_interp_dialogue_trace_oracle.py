from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
import unittest

from dynamics.labs.interp_dialogue_scenario_contract import (
    ScenarioContractError,
    loads_exact,
)
from dynamics.labs.interp_dialogue_trace_oracle_contract import (
    TraceOracleContractError,
    load_and_validate_trace_oracle,
    load_oracle,
    validate_trace_oracle,
)


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_ROOT = ROOT / "research" / "scenarios" / "interp-dialogue-001"
ORACLE_PATH = SCENARIO_ROOT / "trace-oracle-v1.json"
SCHEMA_PATH = SCENARIO_ROOT / "trace-oracle.schema.json"
VALIDATOR_PATH = ROOT / "dynamics" / "labs" / (
    "interp_dialogue_trace_oracle_contract.py"
)


def _by_id(records: list[dict], key: str, value: str) -> dict:
    return next(record for record in records if record[key] == value)


class InterpDialogueTraceOracleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.oracle = load_oracle(ORACLE_PATH)

    def assert_invalid(self, oracle: dict) -> None:
        with self.assertRaises(TraceOracleContractError):
            validate_trace_oracle(oracle, oracle_path=ORACLE_PATH)

    def test_canonical_unexecuted_oracle_validates_with_exact_coverage(self) -> None:
        oracle = load_and_validate_trace_oracle(ORACLE_PATH)
        self.assertEqual(len(oracle["observation_points"]), 11)
        self.assertEqual(len(oracle["horizons"]), 3)
        self.assertEqual(len(oracle["trace_fields"]), 23)
        self.assertEqual(len(oracle["guard_policy_catalog"]), 4)
        self.assertEqual(len(oracle["factor_oracles"]), 9)
        self.assertEqual(
            sum(len(item["hypotheses"]) for item in oracle["factor_oracles"]),
            38,
        )
        self.assertEqual(len(oracle["matched_future_oracles"]), 3)
        self.assertEqual(
            oracle["authority"]["empirical_status"],
            "NO_HUMAN_LLM_OR_D2A_TRACE_DATA",
        )

    def test_explicit_schema_and_duplicate_key_loader_are_enforced(self) -> None:
        validate_trace_oracle(
            self.oracle, oracle_path=ORACLE_PATH, schema_path=SCHEMA_PATH
        )
        loads_exact(SCHEMA_PATH.read_bytes())
        with self.assertRaises(ScenarioContractError):
            loads_exact(b'{"oracle_id":"a","oracle_id":"b"}')

    def test_result_vocabularies_are_exact_and_pairwise_disjoint(self) -> None:
        missing = deepcopy(self.oracle)
        missing["adjudication_vocabulary"].remove("SIGNATURE_CONFORMS")
        self.assert_invalid(missing)

        collision = deepcopy(self.oracle)
        collision["adjudication_vocabulary"].append("MUST_REMAIN_EQUAL")
        self.assert_invalid(collision)

        relation_meaning = deepcopy(self.oracle)
        relation_meaning["relation_vocabulary"][0]["meaning"] = (
            "This is a correct human ground-truth mechanism."
        )
        self.assert_invalid(relation_meaning)

        observation_meaning = deepcopy(self.oracle)
        observation_meaning["observation_vocabulary"][0]["meaning"] = (
            "Equality certifies direct causal residence."
        )
        self.assert_invalid(observation_meaning)

        self.assertTrue(
            set(item["relation"] for item in self.oracle["relation_vocabulary"])
            .isdisjoint(
                item["observation"]
                for item in self.oracle["observation_vocabulary"]
            )
        )

    def test_observation_points_and_horizon_boundaries_are_exact(self) -> None:
        swapped_ordinals = deepcopy(self.oracle)
        points = {
            item["observation_point_id"]: item
            for item in swapped_ordinals["observation_points"]
        }
        points["O1_INITIAL_ACCESS_WINDOW_CLOSED"]["ordinal"], points[
            "O2_INITIAL_ENCOUNTER_WINDOW_CLOSED"
        ]["ordinal"] = (
            points["O2_INITIAL_ENCOUNTER_WINDOW_CLOSED"]["ordinal"],
            points["O1_INITIAL_ACCESS_WINDOW_CLOSED"]["ordinal"],
        )
        self.assert_invalid(swapped_ordinals)

        stage_drift = deepcopy(self.oracle)
        _by_id(
            stage_drift["observation_points"],
            "observation_point_id",
            "O7_LATER_ACCESS_WINDOW_CLOSED",
        )["stage"] = "CANDIDATE"
        self.assert_invalid(stage_drift)

        horizon_drift = deepcopy(self.oracle)
        _by_id(
            horizon_drift["observation_points"],
            "observation_point_id",
            "O1_INITIAL_ACCESS_WINDOW_CLOSED",
        )["horizon_id"] = "H_PREFIX_BEFORE_K"
        self.assert_invalid(horizon_drift)

        early_end = deepcopy(self.oracle)
        _by_id(
            early_end["horizons"], "horizon_id", "H_INITIAL_ACCESS_K"
        )["end_observation_point_id"] = "O4_INITIAL_ADJUDICATION_WINDOW_CLOSED"
        self.assert_invalid(early_end)

    def test_bound_family_digest_and_snapshot_cannot_drift(self) -> None:
        digest_drift = deepcopy(self.oracle)
        digest_drift["bound_family_files"][0]["content_sha256"] = "0" * 64
        self.assert_invalid(digest_drift)

        snapshot_drift = deepcopy(self.oracle)
        snapshot_drift["factor_oracles"][0]["source_contract_snapshot"][
            "status"
        ] = "OPEN_CHANGED"
        self.assert_invalid(snapshot_drift)

    def test_every_hypothesis_is_a_total_closed_projection_vector(self) -> None:
        missing = deepcopy(self.oracle)
        missing["factor_oracles"][0]["hypotheses"][0]["relations"].pop()
        self.assert_invalid(missing)

        duplicated = deepcopy(self.oracle)
        relations = duplicated["factor_oracles"][0]["hypotheses"][0][
            "relations"
        ]
        relations[-1] = deepcopy(relations[0])
        self.assert_invalid(duplicated)

        omitted_placement = deepcopy(self.oracle)
        omitted_placement["factor_oracles"][0]["hypotheses"].pop()
        self.assert_invalid(omitted_placement)

        duplicate_placement = deepcopy(self.oracle)
        hypotheses = duplicate_placement["factor_oracles"][0]["hypotheses"]
        hypotheses[-1]["placement_id"] = hypotheses[0]["placement_id"]
        self.assert_invalid(duplicate_placement)

    def test_placement_ids_are_bound_to_exact_relation_signatures(self) -> None:
        swaps = (
            (
                "oracle.rel.reported_current_mood",
                "CA_ACCESS_FIRST_ASSOCIATION",
                "CE_ENCOUNTER_FIRST_ASSOCIATION",
            ),
            (
                "oracle.rel.externally_cued_prior_material",
                "QA_ADMISSION_OR_ACCESS_ASSOCIATION",
                "QE_ENCOUNTER_ASSOCIATION",
            ),
            (
                "oracle.work.public_feedback_addendum",
                "WU_INFORMATION_UPTAKE_ASSOCIATION",
                "WC_CANDIDATE_OR_REVISION_AFFORDANCE_ASSOCIATION",
            ),
            (
                "oracle.risk.route_match_observation",
                "RRE_ENCOUNTER_ASSOCIATION",
                "RRA_ACTION_AFFORDANCE_ASSOCIATION",
            ),
        )
        for oracle_id, left_id, right_id in swaps:
            with self.subTest(oracle_id=oracle_id):
                swapped = deepcopy(self.oracle)
                factor_oracle = _by_id(
                    swapped["factor_oracles"], "oracle_id", oracle_id
                )
                left = _by_id(
                    factor_oracle["hypotheses"], "placement_id", left_id
                )
                right = _by_id(
                    factor_oracle["hypotheses"], "placement_id", right_id
                )
                left["relations"], right["relations"] = (
                    right["relations"], left["relations"]
                )
                self.assert_invalid(swapped)

    def test_factor_projections_cannot_move_into_evidence_or_writer_guards(
        self,
    ) -> None:
        for forbidden_field in (
            "evidence_assessment_by_claim_scope",
            "durable_targetform_write",
        ):
            with self.subTest(forbidden_field=forbidden_field):
                moved = deepcopy(self.oracle)
                factor_oracle = moved["factor_oracles"][0]
                old = factor_oracle["projection_set"][0]
                old_coordinate = (
                    old["observation_point_id"], old["trace_field_id"]
                )
                old["observation_point_id"] = (
                    "O4_INITIAL_ADJUDICATION_WINDOW_CLOSED"
                )
                old["trace_field_id"] = forbidden_field
                for hypothesis in factor_oracle["hypotheses"]:
                    relation = next(
                        item
                        for item in hypothesis["relations"]
                        if (
                            item["observation_point_id"], item["trace_field_id"]
                        ) == old_coordinate
                    )
                    relation["observation_point_id"] = (
                        "O4_INITIAL_ADJUDICATION_WINDOW_CLOSED"
                    )
                    relation["trace_field_id"] = forbidden_field
                self.assert_invalid(moved)

    def test_factor_placement_family_and_join_identities_are_exact(self) -> None:
        wrong_family = deepcopy(self.oracle)
        mood = _by_id(
            wrong_family["factor_oracles"],
            "oracle_id",
            "oracle.rel.reported_current_mood",
        )
        cue = _by_id(
            wrong_family["factor_oracles"],
            "oracle_id",
            "oracle.rel.externally_cued_prior_material",
        )
        mood["placement_family_id"] = cue["placement_family_id"]
        mood_coordinates = [
            (item["observation_point_id"], item["trace_field_id"])
            for item in mood["projection_set"]
        ]
        cue_coordinates = [
            (item["observation_point_id"], item["trace_field_id"])
            for item in cue["projection_set"]
        ]
        mood["hypotheses"] = deepcopy(cue["hypotheses"])
        coordinate_map = dict(zip(cue_coordinates, mood_coordinates))
        for hypothesis in mood["hypotheses"]:
            for relation in hypothesis["relations"]:
                coordinate = (
                    relation["observation_point_id"], relation["trace_field_id"]
                )
                relation["observation_point_id"], relation["trace_field_id"] = (
                    coordinate_map[coordinate]
                )
        self.assert_invalid(wrong_family)

        renamed_oracle = deepcopy(self.oracle)
        renamed_oracle["factor_oracles"][0]["oracle_id"] = "oracle.rel.renamed"
        self.assert_invalid(renamed_oracle)

        renamed_hypothesis = deepcopy(self.oracle)
        renamed_hypothesis["factor_oracles"][0]["hypotheses"][0][
            "hypothesis_id"
        ] = "rel.mood.renamed"
        self.assert_invalid(renamed_hypothesis)

        collided_hypothesis = deepcopy(self.oracle)
        collided_hypothesis["factor_oracles"][1]["hypotheses"][0][
            "hypothesis_id"
        ] = collided_hypothesis["factor_oracles"][0]["hypotheses"][0][
            "hypothesis_id"
        ]
        self.assert_invalid(collided_hypothesis)

    def test_trace_and_placement_catalogs_reject_unused_expansion(self) -> None:
        extra_field = deepcopy(self.oracle)
        extra_field["trace_fields"].append(
            {
                "trace_field_id": "unused_latent_score",
                "field_role": "FUNCTIONAL_TRACE",
                "authority": "UNUSED",
            }
        )
        self.assert_invalid(extra_field)

        extra_family = deepcopy(self.oracle)
        extra_family["placement_catalog"].append(
            {
                "placement_family_id": "UNUSED_FAMILY",
                "placements": [
                    {
                        "placement_id": "UNUSED_PLACEMENT",
                        "label": "unused",
                        "authority": "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT",
                    }
                ],
            }
        )
        self.assert_invalid(extra_family)

        label_drift = deepcopy(self.oracle)
        label_drift["placement_catalog"][0]["placements"][0]["label"] = (
            "human ground-truth condition mechanism"
        )
        self.assert_invalid(label_drift)

        collapsed_authority = deepcopy(self.oracle)
        fields = {
            item["trace_field_id"]: item
            for item in collapsed_authority["trace_fields"]
        }
        link = fields["external_target_evidence_link_set"]
        assessment = fields["evidence_assessment_by_claim_scope"]
        link["authority"], assessment["authority"] = (
            assessment["authority"], link["authority"]
        )
        self.assert_invalid(collapsed_authority)

    def test_source_sensitive_guard_vectors_are_total_and_not_interchangeable(
        self,
    ) -> None:
        missing = deepcopy(self.oracle)
        missing["guard_policy_catalog"][0][
            "unconditional_guard_relations"
        ].pop()
        self.assert_invalid(missing)

        wrong_policy = deepcopy(self.oracle)
        risk = _by_id(
            wrong_policy["factor_oracles"],
            "oracle_id",
            "oracle.risk.recent_threat_history",
        )
        risk["guard_policy_id"] = "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS"
        self.assert_invalid(wrong_policy)

        arbitrary_rule = deepcopy(self.oracle)
        route = _by_id(
            arbitrary_rule["factor_oracles"],
            "oracle_id",
            "oracle.risk.route_match_observation",
        )
        route["adjacent_evidence_lane_rule"] = "ROUTE_CERTIFIES_HOSTILE_INTENT"
        self.assert_invalid(arbitrary_rule)

        leaked_rule = deepcopy(self.oracle)
        leaked_rule["factor_oracles"][0]["adjacent_evidence_lane_rule"] = (
            route["adjacent_evidence_lane_rule"]
        )
        self.assert_invalid(leaked_rule)

    def test_evidence_link_set_and_claim_scoped_assessment_remain_separate(
        self,
    ) -> None:
        policies = {
            item["guard_policy_id"]: item
            for item in self.oracle["guard_policy_catalog"]
        }

        def relation(policy_id: str, field_id: str) -> str:
            return next(
                item["relation"]
                for item in policies[policy_id]["unconditional_guard_relations"]
                if item["trace_field_id"] == field_id
            )

        self.assertEqual(
            relation(
                "GUARD_EXPERIMENTER_CUE", "external_target_evidence_link_set"
            ),
            "MUST_REMAIN_EQUAL",
        )
        self.assertEqual(
            relation(
                "GUARD_EXPERIMENTER_CUE",
                "evidence_assessment_by_claim_scope",
            ),
            "NOT_EVALUABLE_WITHOUT_FROZEN_REASSESSMENT_POLICY",
        )
        self.assertEqual(
            relation(
                "GUARD_DECLARED_PUBLIC_HISTORY_OR_STIMULUS",
                "evidence_assessment_by_claim_scope",
            ),
            "MAY_DIFFER_WITH_DECLARED_PUBLIC_INPUT",
        )
        self.assertEqual(
            relation(
                "GUARD_RISK_SEPARATE_HISTORY",
                "evidence_assessment_by_claim_scope",
            ),
            "MUST_REMAIN_EQUAL",
        )

    def test_world_unknowns_and_cue_membership_authorities_are_closed(self) -> None:
        world_drift = deepcopy(self.oracle)
        _by_id(world_drift["trace_fields"], "trace_field_id", "world_unknowns")[
            "authority"
        ] = "UNKNOWN_NOT_NEGATIVE_EVIDENCE"
        self.assert_invalid(world_drift)

        cue_drift = deepcopy(self.oracle)
        cue = _by_id(
            cue_drift["guard_policy_catalog"],
            "guard_policy_id",
            "GUARD_EXPERIMENTER_CUE",
        )
        cue["link_equality_authority"] = "EQUALITY_ASSERTS_MEMBERSHIP"
        self.assert_invalid(cue_drift)

    def test_prefix_nonretroactivity_is_within_arm_not_cross_arm(self) -> None:
        guard = self.oracle["prefix_extension_guard"]
        self.assertFalse(guard["cross_factor_arm_equality_required"])
        self.assertIn("SAME_ARM", guard["comparison_unit"])
        self.assertIn("NOT_COMPARED", guard["forbidden_comparison"])
        for policy in self.oracle["guard_policy_catalog"]:
            self.assertNotIn(
                "prior_occurrence_prefix",
                {item["trace_field_id"] for item in policy["guard_projection_set"]},
            )

        cross_arm = deepcopy(self.oracle)
        cross_arm["prefix_extension_guard"][
            "cross_factor_arm_equality_required"
        ] = True
        self.assert_invalid(cross_arm)

        incomplete_prefix = deepcopy(self.oracle)
        incomplete_prefix["prefix_extension_guard"][
            "protected_initial_trace_observation_point_ids"
        ].pop()
        self.assert_invalid(incomplete_prefix)

    def test_durable_state_and_slow_cache_are_horizon_limited_candidates(self) -> None:
        candidate_drift = deepcopy(self.oracle)
        target_family = _by_id(
            candidate_drift["placement_catalog"],
            "placement_family_id",
            "TARGET_HISTORY_RESIDENCE",
        )
        durable = _by_id(
            target_family["placements"],
            "placement_id",
            "TS_TARGET_SCOPED_READOUT",
        )
        durable["authority"] = "COMPETING_FUNCTIONAL_PLACEMENT_NOT_RESULT"
        self.assert_invalid(candidate_drift)

        alias_drift = deepcopy(self.oracle)
        target_family = _by_id(
            alias_drift["placement_catalog"],
            "placement_family_id",
            "TARGET_HISTORY_RESIDENCE",
        )
        target_family["horizon_limitation"]["forbidden_conclusions"].remove(
            "OPERATIONALLY_ALIASED"
        )
        self.assert_invalid(alias_drift)

    def test_same_surface_eligibility_excludes_the_design_anchor(self) -> None:
        future = self.oracle["matched_future_oracles"][0]
        eligibility = future["same_surface_eligibility"]
        self.assertNotIn("DESIGN_ANCHOR_ONLY", eligibility["allowed_bases"])
        self.assertEqual(eligibility["failure_status"], "NOT_EVALUABLE")

        anchor_cast = deepcopy(self.oracle)
        anchor_cast["matched_future_oracles"][0]["same_surface_eligibility"][
            "allowed_bases"
        ][0] = "DESIGN_ANCHOR_ONLY"
        self.assert_invalid(anchor_cast)

        mapping_scope = deepcopy(self.oracle)
        mapping_scope["matched_future_oracles"][0]["same_surface_eligibility"][
            "required_scope_keys"
        ].remove("measurement_mapping_version")
        self.assert_invalid(mapping_scope)

        point_cast = deepcopy(self.oracle)
        _by_id(
            point_cast["observation_points"],
            "observation_point_id",
            "O5_IMMEDIATE_SURFACE_RECORDED",
        )["authority"] = "OBSERVATION_SLOT_NOT_RESULT"
        self.assert_invalid(point_cast)

    def test_every_future_option_uses_an_exact_same_option_arm(self) -> None:
        for future in self.oracle["matched_future_oracles"]:
            with self.subTest(family=future["family_id"]):
                self.assertEqual(
                    {item["option_index"] for item in future["matched_option_arms"]},
                    set(range(future["source_option_count"])),
                )
                for arm in future["matched_option_arms"]:
                    self.assertEqual(arm["left_option_index"], arm["option_index"])
                    self.assertEqual(arm["right_option_index"], arm["option_index"])

        mismatched = deepcopy(self.oracle)
        mismatched["matched_future_oracles"][0]["matched_option_arms"][0][
            "right_option_index"
        ] = 1
        self.assert_invalid(mismatched)

        missing = deepcopy(self.oracle)
        missing["matched_future_oracles"][0]["matched_option_arms"].pop()
        self.assert_invalid(missing)

    def test_future_guards_preserve_input_and_forbid_writer_casts(self) -> None:
        drift = deepcopy(self.oracle)
        future_record = next(
            item
            for item in drift["matched_future_oracles"][0][
                "future_guard_relations"
            ]
            if item["trace_field_id"] == "future_option_public_record"
        )
        future_record["relation"] = "MAY_DIFFER_DOWNSTREAM"
        self.assert_invalid(drift)

        evidence_drift = deepcopy(self.oracle)
        evidence_assessment = next(
            item
            for item in evidence_drift["matched_future_oracles"][0][
                "future_guard_relations"
            ]
            if item["trace_field_id"] == "evidence_assessment_by_claim_scope"
        )
        evidence_assessment["relation"] = "MAY_DIFFER_DOWNSTREAM"
        self.assert_invalid(evidence_drift)

    def test_future_oracle_ids_and_functional_projections_are_exact(self) -> None:
        renamed = deepcopy(self.oracle)
        renamed["matched_future_oracles"][0]["oracle_id"] = "future.rel.renamed"
        self.assert_invalid(renamed)

        for forbidden_field in (
            "evidence_assessment_by_claim_scope",
            "durable_targetform_write",
            "future_option_public_record",
        ):
            with self.subTest(forbidden_field=forbidden_field):
                moved = deepcopy(self.oracle)
                projection = moved["matched_future_oracles"][0][
                    "later_projection_refs"
                ][0]
                projection["observation_point_id"] = (
                    "O9_LATER_CANDIDATE_ADJUDICATION_REORGANIZATION_CLOSED"
                )
                projection["trace_field_id"] = forbidden_field
                self.assert_invalid(moved)

    def test_rel_factorial_is_independent_of_same_surface_eligibility(self) -> None:
        cells = self.oracle["rel_delayed_reorganization_factorial"]["cells"]
        self.assertEqual(len(cells), 4)
        duplicate = deepcopy(self.oracle)
        duplicate["rel_delayed_reorganization_factorial"]["cells"][-1][
            "initial_reported_mood"
        ] = duplicate["rel_delayed_reorganization_factorial"]["cells"][0][
            "initial_reported_mood"
        ]
        self.assert_invalid(duplicate)

        swapped_mapping = deepcopy(self.oracle)
        swapped_mapping["rel_delayed_reorganization_factorial"][
            "later_option_mapping"
        ][0]["source_option_index"] = 1
        self.assert_invalid(swapped_mapping)

        pattern_drift = deepcopy(self.oracle)
        pattern_drift["rel_delayed_reorganization_factorial"][
            "candidate_patterns"
        ][0]["later_edge_relation"] = "MUST_DIFFER_IF_PLACEMENT"
        self.assert_invalid(pattern_drift)

        unbound_paths = deepcopy(self.oracle)
        factorial = unbound_paths["rel_delayed_reorganization_factorial"]
        factorial["fixed_initial_factor_levels"][
            "externally_cued_prior_material"
        ] = "cue_prior_unexplained_distance"
        for cell in factorial["cells"]:
            cell["initial_cell_id"] = {
                "rel-000": "rel-001",
                "rel-100": "rel-101",
            }[cell["initial_cell_id"]]
        self.assert_invalid(unbound_paths)

    def test_natural_oracles_cannot_claim_direct_residence(self) -> None:
        direct = deepcopy(self.oracle)
        hypothesis = direct["factor_oracles"][0]["hypotheses"][0]
        hypothesis["direct_edge_claim"] = "D2A_NODE_CLAMP_REQUIRED"
        self.assert_invalid(direct)

    def test_ghost_adjudicator_and_action_gate_remain_d2a_only(self) -> None:
        clamped_target = deepcopy(self.oracle)
        challenge = clamped_target["d2a_only_challenges"][0]
        challenge["clamped_fields"].append(challenge["observed_field"])
        self.assert_invalid(clamped_target)

        wrong_status = deepcopy(self.oracle)
        wrong_status["d2a_only_challenges"][0]["status"] = "001A_INTERVENTION"
        self.assert_invalid(wrong_status)

        wrong_matrix = deepcopy(self.oracle)
        wrong_matrix["d2a_only_challenges"][1]["varied_input"] = (
            "ghost_exploration_program"
        )
        self.assert_invalid(wrong_matrix)

    def test_alias_and_out_of_model_lanes_cannot_silently_collapse(self) -> None:
        alias = deepcopy(self.oracle)
        alias["operational_alias_rule"]["durable_cache_rule"] = (
            "TS_TARGET_SCOPED_READOUT and TC_SLOW_CACHE_READOUT are equal."
        )
        self.assert_invalid(alias)

        coercion = deepcopy(self.oracle)
        coercion["out_of_model_policy"][
            "forced_cast_to_registered_trace_field"
        ] = "ALLOWED"
        self.assert_invalid(coercion)

        provenance = deepcopy(self.oracle)
        provenance["out_of_model_policy"]["record_fields"].remove(
            "source_provenance"
        )
        self.assert_invalid(provenance)

        scope_drift = deepcopy(self.oracle)
        scope_drift["out_of_model_policy"]["scope_failure_requirements"].pop()
        self.assert_invalid(scope_drift)

        alias_definition = deepcopy(self.oracle)
        alias_definition["operational_alias_rule"]["definition"] = (
            "Observed equality is enough to establish an alias."
        )
        self.assert_invalid(alias_definition)

    def test_authority_prohibitions_are_an_exact_closed_set(self) -> None:
        for prohibition in (
            "NO_CORRECT_OUTPUT_OR_PLACEMENT_WINNER_IS_RECORDED",
            "NO_PRESENTED_CUE_IS_CAST_AS_ACCESS_USE_INTEGRATION_EPISODE_OR_NARRATIVE",
            (
                "NO_PROVISIONAL_TARGET_REPRESENTATION_IS_CAST_AS_A_RESOLVED_"
                "ENTITY_IDENTITY_OR_INTENTION"
            ),
            "NO_DURABLE_TARGETFORM_EPISODE_OR_NARRATIVE_WRITER_IS_CREATED",
        ):
            with self.subTest(prohibition=prohibition):
                missing = deepcopy(self.oracle)
                missing["prohibitions"].remove(prohibition)
                self.assert_invalid(missing)

    def test_contract_module_imports_no_runtime_or_routing_modules(self) -> None:
        tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"))
        dynamics_from_imports = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("dynamics")
        }
        dynamics_direct_imports = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
            if alias.name.startswith("dynamics")
        }
        self.assertEqual(
            dynamics_from_imports,
            {
                "dynamics.labs.interp_dialogue_scenario_contract",
                "dynamics.labs.interp_m1_common",
            },
        )
        self.assertEqual(dynamics_direct_imports, set())


if __name__ == "__main__":
    unittest.main()
