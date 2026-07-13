from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path
import unittest

from dynamics.labs.interp_dialogue_scenario_contract import (
    ScenarioContractError,
    derive_hamming_one_contrasts,
    load_and_validate_family,
    load_family,
    loads_exact,
    validate_family,
)


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_ROOT = ROOT / "research" / "scenarios" / "interp-dialogue-001"
FAMILY_ROOT = SCENARIO_ROOT / "families"
SCHEMA_PATH = SCENARIO_ROOT / "scenario.schema.json"
FAMILY_PATHS = {
    "REL": FAMILY_ROOT / "rel-boundary.json",
    "WORK": FAMILY_ROOT / "work-feedback.json",
    "RISK": FAMILY_ROOT / "risk-footsteps.json",
}

EXPECTED_FACTOR_IDS = {
    "REL": {
        "reported_current_mood",
        "target_history",
        "externally_cued_prior_material",
    },
    "WORK": {
        "reported_evaluation_threat",
        "evaluator_criterion_history",
        "public_feedback_addendum",
    },
    "RISK": {
        "reported_pre_event_arousal",
        "recent_threat_history",
        "route_match_observation",
    },
}

EXPECTED_FACTOR_DECLARATIONS = {
    "REL": {
        "reported_current_mood": (
            "vignette_reported_current_mood",
            "FIRST_PERSON_CONDITION_REPORT",
        ),
        "target_history": (
            "vignette_relational_history",
            "VIGNETTE_HISTORY_RECORD",
        ),
        "externally_cued_prior_material": (
            "vignette_externally_cued_material",
            "EXPERIMENTER_CUE",
        ),
    },
    "WORK": {
        "reported_evaluation_threat": (
            "vignette_reported_evaluation_threat",
            "FIRST_PERSON_CONDITION_REPORT",
        ),
        "evaluator_criterion_history": (
            "vignette_evaluator_criterion_history",
            "VIGNETTE_HISTORY_RECORD",
        ),
        "public_feedback_addendum": (
            "vignette_feedback_addendum",
            "PUBLIC_STIMULUS_VARIANT",
        ),
    },
    "RISK": {
        "reported_pre_event_arousal": (
            "vignette_reported_pre_event_arousal",
            "FIRST_PERSON_CONDITION_REPORT",
        ),
        "recent_threat_history": (
            "vignette_recent_threat_history",
            "VIGNETTE_HISTORY_RECORD",
        ),
        "route_match_observation": (
            "vignette_route_match_observation",
            "PUBLIC_STIMULUS_VARIANT",
        ),
    },
}

EXPECTED_FAMILY_IDS = {
    "REL": "REL-BOUNDARY-001",
    "WORK": "WORK-FEEDBACK-001",
    "RISK": "RISK-FOOTSTEPS-001",
}

EXPECTED_CHANGED_FACTOR_IDS = {
    "REL": "reported_current_mood",
    "WORK": "reported_evaluation_threat",
    "RISK": "reported_pre_event_arousal",
}


class InterpDialogueScenarioContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.families = {
            domain: load_family(path) for domain, path in FAMILY_PATHS.items()
        }

    def test_exact_three_family_set_validates_without_execution(self) -> None:
        self.assertEqual(
            {path.name for path in FAMILY_ROOT.glob("*.json")},
            {path.name for path in FAMILY_PATHS.values()},
        )
        for domain, path in FAMILY_PATHS.items():
            with self.subTest(domain=domain):
                family = load_and_validate_family(path)
                self.assertEqual(family["domain"], domain)
                self.assertEqual(
                    family["status"],
                    "INTERNAL_PREREGISTRATION_UNEXECUTED_NO_HUMAN_DATA",
                )

    def test_validator_accepts_an_explicit_schema_path(self) -> None:
        validate_family(self.families["REL"], schema_path=SCHEMA_PATH)

    def test_each_family_has_twelve_factor_label_hamming_one_contrasts(self) -> None:
        for domain, family in self.families.items():
            with self.subTest(domain=domain):
                pairs = validate_family(family)
                self.assertEqual(len(family["factors"]), 3)
                self.assertEqual(len(family["cells"]), 8)
                self.assertEqual(len(pairs), 12)
                changed_counts = {
                    factor["factor_id"]: 0 for factor in family["factors"]
                }
                for _, _, changed_factor in pairs:
                    changed_counts[changed_factor] += 1
                self.assertEqual(set(changed_counts.values()), {4})
                self.assertEqual(pairs, derive_hamming_one_contrasts(family))

    def test_family_factor_axes_are_declared_and_domain_specific(self) -> None:
        self.assertEqual(
            {family["family_id"] for family in self.families.values()},
            set(EXPECTED_FAMILY_IDS.values()),
        )
        for domain, family in self.families.items():
            with self.subTest(domain=domain):
                self.assertEqual(family["family_id"], EXPECTED_FAMILY_IDS[domain])
                self.assertEqual(
                    {factor["factor_id"] for factor in family["factors"]},
                    EXPECTED_FACTOR_IDS[domain],
                )
                declarations = {}
                for factor in family["factors"]:
                    lanes = {level["source_lane"] for level in factor["levels"]}
                    self.assertEqual(len(lanes), 1)
                    declarations[factor["factor_id"]] = (
                        factor["operational_source_kind"],
                        next(iter(lanes)),
                    )
                self.assertEqual(declarations, EXPECTED_FACTOR_DECLARATIONS[domain])

    def test_factor_contrast_contracts_cover_each_factor_without_trace_answers(self) -> None:
        for domain, family in self.families.items():
            with self.subTest(domain=domain):
                contracts = family["factor_contrast_contracts"]
                self.assertEqual(
                    {contract["factor_id"] for contract in contracts},
                    EXPECTED_FACTOR_IDS[domain],
                )
                source_lanes = {
                    factor["factor_id"]: {
                        level["source_lane"] for level in factor["levels"]
                    }
                    for factor in family["factors"]
                }
                for contract in contracts:
                    factor_id = contract["factor_id"]
                    self.assertEqual(source_lanes[factor_id], {contract["source_lane"]})
                    self.assertEqual(
                        set(contract["held_constant_factor_ids"]),
                        EXPECTED_FACTOR_IDS[domain] - {factor_id},
                    )
                    self.assertEqual(contract["status"], "OPEN_NO_EXPECTED_TRACE")
                    self.assertTrue(contract["registered_candidate_probe_domains"])
                    self.assertNotIn("expected_trace", contract)

    def test_resolved_and_unresolved_target_scope_contracts_are_distinct(self) -> None:
        for domain in ("REL", "WORK"):
            scope = self.families[domain]["target_scope"]
            self.assertEqual(scope["resolution"], "resolved")
            self.assertEqual(
                scope["stable_entity_target_form_applicability"],
                "OPEN_DISCRIMINATOR",
            )
            self.assertEqual(
                scope["provisional_target_representation_status"], "OUT_OF_SCOPE"
            )

    def test_author_origin_material_is_not_a_public_record_or_evidence_lane(self) -> None:
        for domain, family in self.families.items():
            with self.subTest(domain=domain):
                author_entries = family["shared_contract"]["author_origin_possibilities"]
                public_record = {
                    record["statement"] for record in family["stimulus"]["public_record"]
                }
                public_record.update(
                    record["statement"]
                    for factor in family["factors"]
                    for level in factor["levels"]
                    for record in level["level_specific_public_record"]
                )
                self.assertFalse(
                    {entry["statement"] for entry in author_entries} & public_record
                )
                self.assertTrue(
                    all("AUTHOR" in entry["authority"] for entry in author_entries)
                )
                self.assertNotIn("evidence", family["shared_contract"])

    def test_open_discriminators_and_same_projection_claims_remain_unresolved(self) -> None:
        for domain, family in self.families.items():
            with self.subTest(domain=domain):
                for discriminator in family["shared_contract"]["open_discriminators"]:
                    self.assertIn("OPEN", discriminator["status"])
                    self.assertNotIn("RESOLVED", discriminator["status"])
                    self.assertEqual(
                        set(discriminator), {"id", "question", "status"}
                    )
                claim = family["same_immediate_projection_claim"]
                self.assertEqual(claim["status"], "OPEN")
                self.assertEqual(
                    claim["changed_factor_id"], EXPECTED_CHANGED_FACTOR_IDS[domain]
                )
                self.assertTrue(claim["future_probe"]["no_expected_result"])
                self.assertGreaterEqual(
                    len(claim["future_probe"]["probe_options"]), 2
                )

    def test_cells_have_no_mechanism_or_output_answer_fields(self) -> None:
        for domain, family in self.families.items():
            with self.subTest(domain=domain):
                for cell in family["cells"]:
                    self.assertEqual(set(cell), {"cell_id", "factor_levels"})

    def test_risk_family_keeps_unknown_target_outside_stable_entity_target_form_scope(
        self,
    ) -> None:
        risk = self.families["RISK"]
        self.assertEqual(risk["target_scope"]["resolution"], "unresolved")
        self.assertEqual(
            risk["target_scope"]["stable_entity_target_form_applicability"],
            "NOT_APPLICABLE",
        )
        self.assertEqual(
            risk["target_scope"]["provisional_target_representation_status"],
            "OPEN_DISCRIMINATOR",
        )
        validate_family(risk)

    def test_missing_or_duplicate_cube_cell_is_rejected(self) -> None:
        missing = deepcopy(self.families["REL"])
        missing["cells"].pop()
        with self.assertRaisesRegex(ScenarioContractError, "schema minItems mismatch"):
            validate_family(missing)

        duplicate = deepcopy(self.families["REL"])
        duplicate["cells"][-1]["factor_levels"] = deepcopy(
            duplicate["cells"][0]["factor_levels"]
        )
        with self.assertRaisesRegex(ScenarioContractError, "duplicate cube assignment"):
            validate_family(duplicate)

    def test_unknown_level_and_answer_injection_are_rejected(self) -> None:
        unknown_level = deepcopy(self.families["WORK"])
        factor_id = unknown_level["factors"][0]["factor_id"]
        unknown_level["cells"][0]["factor_levels"][factor_id] = "not-a-level"
        with self.assertRaisesRegex(ScenarioContractError, "unknown factor level"):
            validate_family(unknown_level)

        mechanism_answer = deepcopy(self.families["WORK"])
        mechanism_answer["cells"][0]["correct_mechanism"] = "reception_changes_access"
        with self.assertRaisesRegex(ScenarioContractError, "forbidden post-001A field"):
            validate_family(mechanism_answer)

        output_answer = deepcopy(self.families["WORK"])
        output_answer["cells"][0]["correct_output"] = "wait"
        with self.assertRaisesRegex(ScenarioContractError, "forbidden post-001A field"):
            validate_family(output_answer)

    def test_open_discriminator_cannot_acquire_an_answer_or_resolution(self) -> None:
        answered = deepcopy(self.families["REL"])
        answered["shared_contract"]["open_discriminators"][0]["answer"] = "formation"
        with self.assertRaisesRegex(ScenarioContractError, "schema additional property"):
            validate_family(answered)

        resolved = deepcopy(self.families["REL"])
        resolved["shared_contract"]["open_discriminators"][0]["status"] = "RESOLVED"
        with self.assertRaisesRegex(ScenarioContractError, "schema const mismatch"):
            validate_family(resolved)

    def test_same_projection_claim_requires_a_future_probe_without_expected_result(self) -> None:
        missing_probe = deepcopy(self.families["REL"])
        del missing_probe["same_immediate_projection_claim"]["future_probe"]
        with self.assertRaisesRegex(ScenarioContractError, "schema required property"):
            validate_family(missing_probe)

        expected_result = deepcopy(self.families["REL"])
        expected_result["same_immediate_projection_claim"]["future_probe"][
            "no_expected_result"
        ] = False
        with self.assertRaisesRegex(ScenarioContractError, "schema const mismatch"):
            validate_family(expected_result)

        non_minimal = deepcopy(self.families["REL"])
        cells = non_minimal["cells"]
        first = cells[0]
        first_assignment = first["factor_levels"]
        distant = next(
            cell
            for cell in cells
            if sum(
                first_assignment[factor_id] != cell["factor_levels"][factor_id]
                for factor_id in first_assignment
            )
            >= 2
        )
        non_minimal["same_immediate_projection_claim"]["compared_cell_ids"] = [
            first["cell_id"],
            distant["cell_id"],
        ]
        with self.assertRaisesRegex(
            ScenarioContractError, "factor-label Hamming-one contrast"
        ):
            validate_family(non_minimal)

    def test_author_lane_cannot_be_cast_as_evidence(self) -> None:
        cast = deepcopy(self.families["RISK"])
        cast["shared_contract"]["author_origin_possibilities"][0][
            "authority"
        ] = "EVIDENCE"
        with self.assertRaisesRegex(ScenarioContractError, "schema enum mismatch"):
            validate_family(cast)

    def test_author_lane_cannot_be_copied_into_level_specific_public_record(self) -> None:
        cast = deepcopy(self.families["REL"])
        author_statement = cast["shared_contract"]["author_origin_possibilities"][0][
            "statement"
        ]
        cast["factors"][0]["levels"][0]["level_specific_public_record"][0][
            "statement"
        ] = author_statement
        with self.assertRaisesRegex(
            ScenarioContractError, "cannot be copied into the public record"
        ):
            validate_family(cast)

    def test_invalid_token_projection_kind_and_family_id_collision_are_rejected(
        self,
    ) -> None:
        bad_token = deepcopy(self.families["REL"])
        bad_token["family_id"] = "invalid family id"
        with self.assertRaisesRegex(ScenarioContractError, "schema pattern mismatch"):
            validate_family(bad_token)

        bad_kind = deepcopy(self.families["REL"])
        bad_kind["same_immediate_projection_claim"]["candidate_projection"][
            "kind"
        ] = "latent_report"
        with self.assertRaisesRegex(ScenarioContractError, "schema enum mismatch"):
            validate_family(bad_kind)

        id_collision = deepcopy(self.families["REL"])
        id_collision["same_immediate_projection_claim"]["claim_id"] = id_collision[
            "shared_contract"
        ]["open_discriminators"][0]["id"]
        with self.assertRaisesRegex(ScenarioContractError, "IDs collide"):
            validate_family(id_collision)

    def test_same_projection_declared_changed_factor_must_match_pair(self) -> None:
        wrong_axis = deepcopy(self.families["WORK"])
        claim = wrong_axis["same_immediate_projection_claim"]
        claim["changed_factor_id"] = next(
            factor_id
            for factor_id in EXPECTED_FACTOR_IDS["WORK"]
            if factor_id != claim["changed_factor_id"]
        )
        with self.assertRaisesRegex(ScenarioContractError, "does not match its pair"):
            validate_family(wrong_axis)

    def test_factor_contrast_contract_must_match_factor_and_other_axes(self) -> None:
        wrong_held_constant = deepcopy(self.families["RISK"])
        contract = wrong_held_constant["factor_contrast_contracts"][0]
        other = next(
            factor_id
            for factor_id in EXPECTED_FACTOR_IDS["RISK"]
            if factor_id != contract["factor_id"]
        )
        contract["held_constant_factor_ids"] = [contract["factor_id"], other]
        with self.assertRaisesRegex(ScenarioContractError, "exactly the other two"):
            validate_family(wrong_held_constant)

        wrong_lane = deepcopy(self.families["RISK"])
        contract = wrong_lane["factor_contrast_contracts"][0]
        contract["source_lane"] = "EXPERIMENTER_CUE"
        with self.assertRaisesRegex(ScenarioContractError, "does not match"):
            validate_family(wrong_lane)

    def test_unresolved_risk_target_cannot_acquire_stable_entity_target_form(
        self,
    ) -> None:
        cast = deepcopy(self.families["RISK"])
        cast["target_scope"][
            "stable_entity_target_form_applicability"
        ] = "OPEN_DISCRIMINATOR"
        with self.assertRaisesRegex(
            ScenarioContractError, "stable_entity_target_form_applicability"
        ):
            validate_family(cast)

    def test_factor_operational_source_kind_and_lane_are_domain_bound(self) -> None:
        all_declarations = [
            declaration
            for domain_declarations in EXPECTED_FACTOR_DECLARATIONS.values()
            for declaration in domain_declarations.values()
        ]
        all_lanes = {lane for _, lane in all_declarations}
        all_kinds = {kind for kind, _ in all_declarations}
        for domain, expected in EXPECTED_FACTOR_DECLARATIONS.items():
            for factor_id, (expected_kind, expected_lane) in expected.items():
                with self.subTest(domain=domain, factor_id=factor_id, field="kind"):
                    mutated = deepcopy(self.families[domain])
                    factor = next(
                        item
                        for item in mutated["factors"]
                        if item["factor_id"] == factor_id
                    )
                    factor["operational_source_kind"] = next(
                        kind for kind in sorted(all_kinds) if kind != expected_kind
                    )
                    with self.assertRaisesRegex(
                        ScenarioContractError, "operational_source_kind changed"
                    ):
                        validate_family(mutated)

                with self.subTest(domain=domain, factor_id=factor_id, field="lane"):
                    mutated = deepcopy(self.families[domain])
                    factor = next(
                        item
                        for item in mutated["factors"]
                        if item["factor_id"] == factor_id
                    )
                    wrong_lane = next(
                        lane for lane in sorted(all_lanes) if lane != expected_lane
                    )
                    for level in factor["levels"]:
                        level["source_lane"] = wrong_lane
                    with self.assertRaisesRegex(
                        ScenarioContractError, "source lane changed"
                    ):
                        validate_family(mutated)

    def test_level_specific_public_record_effect_requires_both_levels(self) -> None:
        mutated = deepcopy(self.families["REL"])
        mutated["factors"][0]["levels"][0]["level_specific_public_record"] = []
        with self.assertRaisesRegex(
            ScenarioContractError, "requires a public record for both factor levels"
        ):
            validate_family(mutated)

    def test_registered_candidate_probe_domains_are_nonexhaustive(self) -> None:
        mutated = deepcopy(self.families["WORK"])
        mutated["factor_contrast_contracts"][0][
            "registered_candidate_probe_domains"
        ].append("future_unlisted_candidate_domain")
        validate_family(mutated)

    def test_declaration_identity_is_family_scoped(self) -> None:
        mutated = deepcopy(self.families["RISK"])
        mutated["stimulus"]["public_record"][0]["id"] = self.families["REL"][
            "stimulus"
        ]["public_record"][0]["id"]
        validate_family(mutated)

    def test_runtime_human_llm_and_writer_fields_are_rejected(self) -> None:
        for forbidden_field in (
            "runtime_state",
            "human_response",
            "llm_activation",
            "narrative_writer",
            "expected_trace",
        ):
            with self.subTest(forbidden_field=forbidden_field):
                mutated = deepcopy(self.families["REL"])
                mutated["shared_contract"][forbidden_field] = {}
                with self.assertRaisesRegex(
                    ScenarioContractError, "forbidden post-001A field"
                ):
                    validate_family(mutated)

    def test_exact_json_loader_rejects_duplicate_keys(self) -> None:
        source = json.dumps(self.families["REL"])
        duplicate = source[:-1] + ',"study_id":"INTERP-DIALOGUE-001A"}'
        with self.assertRaisesRegex(ScenarioContractError, "duplicate JSON key"):
            loads_exact(duplicate)

    def test_scenario_contract_module_has_no_runtime_package_imports(self) -> None:
        module_path = ROOT / "dynamics" / "labs" / "interp_dialogue_scenario_contract.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
        dynamics_imports = {
            module
            for module in imported_modules
            if module == "dynamics" or module.startswith("dynamics.")
        }
        self.assertEqual(
            dynamics_imports,
            {"dynamics.labs.interp_m1_common"},
        )


if __name__ == "__main__":
    unittest.main()
