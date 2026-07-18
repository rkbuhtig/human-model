from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from dynamics.s0.core import (
    IMMEDIATE_ACTIONS,
    LONG_HORIZON_REGIONS,
    PROBABILITY_SCALE,
    SCHEMA_VERSION,
    ObservableEpisodePrefix,
    S0ValidationError,
    TrainingExample,
    canonical_bytes,
)
from dynamics.s0.models import (
    b0_features,
    b1_features,
    b2_features,
    fit_parameters,
    h_features,
    h_state,
    update_h_state,
)
from dynamics.s0.runner import run_model


def receipt(ordinal: int, event: str, *, scope: str = "REGISTERED_REPORT") -> dict[str, object]:
    return {
        "receipt_id": f"r:{ordinal}:{event}",
        "ordinal": ordinal,
        "scope": scope,
        "event_kind": event,
        "actor": "counterpart",
        "target": "focal",
        "public_value": event,
    }


def prefix(
    events: list[str],
    *,
    history: str = "H-STABLE",
    continuation: str = "F-DEFLECT",
) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "trajectory_id": "toy:1",
        "history_condition": history,
        "continuation_condition": continuation,
        "receipts": [receipt(index + 1, event) for index, event in enumerate(events)],
        "public_actions": [],
        "counterpart_feedback": [],
        "role_context": "PRIVATE_RELATION",
        "audience_context": "NO_AUDIENCE",
        "step_ordinal": len(events),
    }


ROOT = Path(__file__).resolve().parents[2]
MODEL_CARDS_PATH = ROOT / "research" / "benchmarks" / "models" / "s0" / "model-cards.json"
PARAMETERS_PATH = ROOT / "research" / "benchmarks" / "models" / "s0" / "initial-parameters.json"


class S0ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model_cards = json.loads(MODEL_CARDS_PATH.read_text(encoding="utf-8"))
        cls.initial_parameters = json.loads(PARAMETERS_PATH.read_text(encoding="utf-8"))

    def setUp(self) -> None:
        self.parameters = deepcopy(self.initial_parameters)

    def test_all_models_emit_complete_normalized_distributions(self) -> None:
        document = prefix(["CURRENT_COMMITMENT_MISSED"])
        for model_id in ("B0", "B1", "B2", "H"):
            with self.subTest(model_id=model_id):
                result = run_model(model_id, document, self.parameters, self.model_cards, seed=11)
                self.assertEqual(set(result["immediate_action_distribution"]), set(IMMEDIATE_ACTIONS))
                self.assertEqual(set(result["long_horizon_region_distribution"]), set(LONG_HORIZON_REGIONS))
                self.assertEqual(sum(result["immediate_action_distribution"].values()), PROBABILITY_SCALE)
                self.assertEqual(sum(result["long_horizon_region_distribution"].values()), PROBABILITY_SCALE)
                self.assertFalse(result["runtime_receipt"]["target_visible"])
                self.assertFalse(result["runtime_receipt"]["reference_state_visible"])

    def test_b0_is_history_invariant_under_identical_current_surface(self) -> None:
        stable = prefix(["CURRENT_COMMITMENT_MISSED"], history="H-STABLE")
        breach = prefix(["CURRENT_COMMITMENT_MISSED"], history="H-BREACH")
        self.assertEqual(
            run_model("B0", stable, self.parameters, self.model_cards)["immediate_action_distribution"],
            run_model("B0", breach, self.parameters, self.model_cards)["immediate_action_distribution"],
        )

    def test_b1_ignores_event_order_when_accumulators_match(self) -> None:
        left = ObservableEpisodePrefix.from_dict(prefix([
            "COUNTERPART_ACKNOWLEDGES_IMPACT",
            "COUNTERPART_MINIMIZES_IMPACT",
            "NO_NEW_INFORMATION",
        ]))
        right = ObservableEpisodePrefix.from_dict(prefix([
            "COUNTERPART_MINIMIZES_IMPACT",
            "COUNTERPART_ACKNOWLEDGES_IMPACT",
            "NO_NEW_INFORMATION",
        ]))
        self.assertEqual(b1_features(left), b1_features(right))
        self.assertNotEqual(b2_features(left), b2_features(right))

    def test_feature_residences_are_distinct(self) -> None:
        parsed = ObservableEpisodePrefix.from_dict(prefix([
            "CURRENT_COMMITMENT_MISSED",
            "COUNTERPART_ACCEPTS_RESPONSIBILITY",
            "COUNTERPART_OFFERS_COSTLY_REPAIR",
        ], continuation="F-REPAIR"))
        self.assertNotEqual(b0_features(parsed), b1_features(parsed))
        self.assertNotEqual(b1_features(parsed), b2_features(parsed))
        self.assertNotEqual(b2_features(parsed), h_features(parsed))

    def test_authorship_dimensions_do_not_auto_collapse(self) -> None:
        parsed = ObservableEpisodePrefix.from_dict(prefix([]))
        state = h_state(parsed)
        caused = update_h_state(state, "SELF_ACTION_CAUSALLY_ATTRIBUTED")
        self.assertGreater(caused.causal_attribution, state.causal_attribution)
        self.assertEqual(caused.control_attribution, state.control_attribution)
        accepted = update_h_state(state, "SELF_RESPONSIBILITY_ACCEPTED")
        self.assertGreater(accepted.responsibility_acceptance, state.responsibility_acceptance)
        self.assertEqual(accepted.endorsement, state.endorsement)
        endorsed = update_h_state(state, "SELF_ENDORSEMENT_EXPRESSED")
        self.assertGreater(endorsed.endorsement, state.endorsement)
        self.assertEqual(endorsed.responsibility_acceptance, state.responsibility_acceptance)

    def test_receipt_scope_is_preserved_without_world_truth_promotion(self) -> None:
        document = prefix(["CURRENT_COMMITMENT_MISSED"])
        document["receipts"][0]["scope"] = "INTERNAL_OCCURRENCE_REPORT"
        parsed = ObservableEpisodePrefix.from_dict(document)
        self.assertEqual(parsed.receipts[0].scope, "INTERNAL_OCCURRENCE_REPORT")
        self.assertNotEqual(parsed.receipts[0].scope, "CERTIFIED_WORLD_OCCURRENCE")

    def test_hidden_and_reference_state_fields_are_rejected(self) -> None:
        for key in ("latent_state", "target_probabilities", "reference_state"):
            document = prefix(["CURRENT_COMMITMENT_MISSED"])
            document[key] = "forbidden"
            with self.subTest(key=key), self.assertRaises(S0ValidationError):
                run_model("H", document, self.parameters, self.model_cards)

    def test_b2_and_h_receive_identical_prefix_digest_and_visible_fields(self) -> None:
        document = prefix(["CURRENT_COMMITMENT_MISSED", "COUNTERPART_MINIMIZES_IMPACT"])
        b2 = run_model("B2", document, self.parameters, self.model_cards)
        h = run_model("H", document, self.parameters, self.model_cards)
        self.assertEqual(b2["runtime_receipt"]["prefix_sha256"], h["runtime_receipt"]["prefix_sha256"])
        self.assertEqual(b2["runtime_receipt"]["visible_field_names"], h["runtime_receipt"]["visible_field_names"])

    def test_h_diagnostics_are_explicitly_non_leaderboard_and_h_only(self) -> None:
        document = prefix(["CURRENT_COMMITMENT_MISSED"])
        h = run_model("H", document, self.parameters, self.model_cards, include_h_diagnostics=True)
        self.assertEqual(h["diagnostic_authority"], "H_ONLY_NOT_LEADERBOARD_EVIDENCE")
        with self.assertRaises(S0ValidationError):
            run_model("B2", document, self.parameters, self.model_cards, include_h_diagnostics=True)

    def test_free_text_and_unregistered_feedback_cannot_smuggle_targets(self) -> None:
        document = prefix(["CURRENT_COMMITMENT_MISSED"])
        document["receipts"][0]["public_value"] = "q3:RELATION_EXIT"
        with self.assertRaises(S0ValidationError):
            ObservableEpisodePrefix.from_dict(document)
        document = prefix(["CURRENT_COMMITMENT_MISSED"])
        document["counterpart_feedback"] = ["target=RELATION_EXIT"]
        with self.assertRaises(S0ValidationError):
            ObservableEpisodePrefix.from_dict(document)

    def test_runner_module_has_no_scoring_import(self) -> None:
        import ast
        path = Path(__file__).resolve().parents[1] / "s0" / "runner.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                imports.append((node.module or ""))
            elif isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
        self.assertFalse(any("scoring" in name for name in imports))

    def test_training_is_deterministic_and_changes_only_selected_model(self) -> None:
        parsed = ObservableEpisodePrefix.from_dict(prefix(["CURRENT_COMMITMENT_MISSED"]))
        examples = [TrainingExample(parsed, "ASSERT_BOUNDARY", "CONFLICT_LOOP")]
        fitted_a = fit_parameters("B2", examples, self.parameters)
        fitted_b = fit_parameters("B2", examples, self.parameters)
        self.assertEqual(canonical_bytes(fitted_a), canonical_bytes(fitted_b))
        self.assertEqual(fitted_a["models"]["B0"], self.parameters["models"]["B0"])
        self.assertEqual(fitted_a["models"]["H"], self.parameters["models"]["H"])
        self.assertEqual(fitted_a["models"]["B2"]["channels"]["immediate_action"]["example_count"], 1)

    def test_same_input_model_version_and_seed_is_byte_reproducible(self) -> None:
        document = prefix(["CURRENT_COMMITMENT_MISSED", "COUNTERPART_SHIFTS_RESPONSIBILITY"])
        first = run_model("H", document, self.parameters, self.model_cards, seed=20260718)
        second = run_model("H", deepcopy(document), deepcopy(self.parameters), deepcopy(self.model_cards), seed=20260718)
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))


if __name__ == "__main__":
    unittest.main()
