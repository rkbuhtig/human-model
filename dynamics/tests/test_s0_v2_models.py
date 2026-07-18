from __future__ import annotations

from copy import deepcopy
import unittest

from dynamics.s0.v2_core import (
    HStateEnvelope, ObservablePrefixV2, PredictionKey, PublicContext, PublicDeltaV2,
    SCHEMA_VERSION, S0V2Error, TypedReceipt,
)
from dynamics.s0.v2_models import (
    apply_receipt, b2_features, empty_parameters, h_full_state, initialize_h,
    predict_full, predict_h_state_only, state_delta, step_h,
)
from dynamics.s0.v2_runner import run_full, run_h_state_only


def receipt(ordinal: int, event: str, *, scope="REGISTERED_REPORT", actor="counterpart", target="focal"):
    return TypedReceipt(f"r{ordinal}", ordinal, scope, event, actor, target)


def make_prefix(events, *, trajectory="t1", instance="TEST-INSTANCE-0000", history="H-STABLE", continuation="F-DEFLECT"):
    receipts = []
    for index, event in enumerate(events, 1):
        if event.startswith("SELF_"):
            receipts.append(receipt(index, event, scope="INTERNAL_OCCURRENCE_REPORT", actor="focal", target="focal"))
        elif event in ("AUDIENCE_CONSTRAINT_PRESENT", "ROLE_CONSTRAINT_PRESENT", "NO_NEW_INFORMATION"):
            receipts.append(receipt(index, event, actor="environment", target="interaction"))
        else:
            receipts.append(receipt(index, event))
    return ObservablePrefixV2(
        SCHEMA_VERSION,
        PredictionKey(instance, trajectory, len(receipts), "p0"),
        PublicContext(history, continuation, "PRIVATE_RELATION", "NO_AUDIENCE"),
        tuple(receipts), (), (),
    )


class V2ModelTests(unittest.TestCase):
    def setUp(self):
        self.parameters = empty_parameters()

    def test_b2_preserves_count_and_exact_order(self):
        left = make_prefix(["CURRENT_COMMITMENT_MISSED", "COUNTERPART_ACKNOWLEDGES_IMPACT", "CURRENT_COMMITMENT_MISSED", "COUNTERPART_ACKNOWLEDGES_IMPACT"])
        right = make_prefix(["CURRENT_COMMITMENT_MISSED", "COUNTERPART_ACKNOWLEDGES_IMPACT", "COUNTERPART_ACKNOWLEDGES_IMPACT", "CURRENT_COMMITMENT_MISSED"])
        repeated = make_prefix(["CURRENT_COMMITMENT_MISSED", "CURRENT_COMMITMENT_MISSED", "COUNTERPART_ACKNOWLEDGES_IMPACT"])
        short = make_prefix(["CURRENT_COMMITMENT_MISSED", "COUNTERPART_ACKNOWLEDGES_IMPACT"])
        self.assertNotEqual(b2_features(left), b2_features(right))
        self.assertEqual(b2_features(repeated)["event=CURRENT_COMMITMENT_MISSED"], 2)
        self.assertNotEqual(b2_features(repeated), b2_features(short))
        self.assertIn("trigram=CURRENT_COMMITMENT_MISSED>CURRENT_COMMITMENT_MISSED>COUNTERPART_ACKNOWLEDGES_IMPACT", b2_features(repeated))

    def test_receipt_compatibility_rejects_wrong_actor(self):
        with self.assertRaises(S0V2Error):
            receipt(1, "SELF_RESPONSIBILITY_ACCEPTED", actor="counterpart", target="focal")
        with self.assertRaises(S0V2Error):
            receipt(1, "AUDIENCE_CONSTRAINT_PRESENT", actor="counterpart", target="focal")

    def test_report_and_certified_occurrence_have_different_weight(self):
        context = PublicContext("H-STABLE", "F-DEFLECT", "PRIVATE_RELATION", "NO_AUDIENCE")
        base = initialize_h(context, "TEST-INSTANCE-0000", "t1").predictive_state
        report = apply_receipt(base, receipt(1, "CURRENT_COMMITMENT_MISSED"))
        certified = apply_receipt(base, receipt(1, "CURRENT_COMMITMENT_MISSED", scope="CERTIFIED_WORLD_OCCURRENCE"))
        self.assertNotEqual(report.unresolved_breach, certified.unresolved_breach)

    def test_action_authorship_dimensions_do_not_collapse(self):
        prefix = make_prefix(["SELF_ACTION_CAUSALLY_ATTRIBUTED"])
        state = h_full_state(prefix).predictive_state
        self.assertGreater(state.causal_attribution, 0)
        self.assertEqual(state.endorsement, 0)
        self.assertEqual(state.responsibility_acceptance, 0)

    def test_full_and_incremental_state_match(self):
        prefix = make_prefix(["CURRENT_COMMITMENT_MISSED", "COUNTERPART_ACKNOWLEDGES_IMPACT", "COUNTERPART_OFFERS_COSTLY_REPAIR"], continuation="F-REPAIR")
        full = h_full_state(prefix)
        state = initialize_h(prefix.context, prefix.key.source_instance_id, prefix.key.trajectory_id)
        for item in prefix.receipts:
            key = PredictionKey(prefix.key.source_instance_id, prefix.key.trajectory_id, item.ordinal, f"state:{item.ordinal}")
            state = step_h(state, PublicDeltaV2(SCHEMA_VERSION, key, prefix.context, item))
        self.assertEqual(full.to_dict(), state.to_dict())
        full_pred = predict_full("H", prefix, self.parameters)
        state_pred = predict_h_state_only(state, prefix.context, self.parameters)
        self.assertEqual(full_pred, state_pred)

    def test_state_only_runner_forbids_history_by_type_and_reports_no_reread(self):
        prefix = make_prefix(["CURRENT_COMMITMENT_MISSED"])
        initial = initialize_h(prefix.context, prefix.key.source_instance_id, prefix.key.trajectory_id)
        delta = PublicDeltaV2(SCHEMA_VERSION, prefix.key, prefix.context, prefix.receipts[0])
        result = run_h_state_only(initial.to_dict(), delta, self.parameters)
        self.assertFalse(result["runtime_receipt"]["raw_history_read"])
        self.assertEqual(result["runtime_receipt"]["serialized_input_bytes"], 0)
        with self.assertRaises((AttributeError, TypeError, S0V2Error)):
            run_h_state_only(prefix.to_dict(), delta, self.parameters)

    def test_incremental_state_rejects_duplicate_reverse_cross_trajectory_and_tamper(self):
        prefix = make_prefix(["CURRENT_COMMITMENT_MISSED"])
        initial = initialize_h(prefix.context, "TEST-INSTANCE-0000", "t1")
        delta = PublicDeltaV2(SCHEMA_VERSION, PredictionKey("TEST-INSTANCE-0000", "t1", 1, "p1"), prefix.context, prefix.receipts[0])
        state = step_h(initial, delta)
        with self.assertRaises(S0V2Error):
            step_h(state, delta)
        wrong = PublicDeltaV2(SCHEMA_VERSION, PredictionKey("TEST-INSTANCE-0000", "other", 2, "p2"), prefix.context, receipt(2, "NO_NEW_INFORMATION", actor="environment", target="interaction"))
        with self.assertRaises(S0V2Error):
            step_h(state, wrong)
        document = state.to_dict(); document["predictive_state"]["threat"] += 1
        with self.assertRaises(S0V2Error):
            HStateEnvelope.from_dict(document)

    def test_multi_clock_fast_decay_and_slow_consolidation(self):
        context = PublicContext("H-STABLE", "F-REPAIR", "PRIVATE_RELATION", "NO_AUDIENCE")
        state = initialize_h(context, "TEST-INSTANCE-0000", "t1")
        breach = receipt(1, "CURRENT_COMMITMENT_MISSED")
        after_breach = step_h(state, PublicDeltaV2(SCHEMA_VERSION, PredictionKey("TEST-INSTANCE-0000", "t1", 1, "p1"), context, breach))
        idle = receipt(2, "NO_NEW_INFORMATION", actor="environment", target="interaction")
        after_idle = step_h(after_breach, PublicDeltaV2(SCHEMA_VERSION, PredictionKey("TEST-INSTANCE-0000", "t1", 2, "p2"), context, idle))
        self.assertLess(after_idle.predictive_state.threat, after_breach.predictive_state.threat)
        self.assertEqual(after_idle.predictive_state.trust_expectation, after_breach.predictive_state.trust_expectation)
        repair = receipt(3, "COUNTERPART_OFFERS_COSTLY_REPAIR")
        after_repair = step_h(after_idle, PublicDeltaV2(SCHEMA_VERSION, PredictionKey("TEST-INSTANCE-0000", "t1", 3, "p3"), context, repair))
        self.assertGreaterEqual(after_repair.predictive_state.trust_expectation, after_idle.predictive_state.trust_expectation)

    def test_directional_readout_is_actual_delta(self):
        prefix = make_prefix(["CURRENT_COMMITMENT_MISSED"])
        initial = initialize_h(prefix.context, "TEST-INSTANCE-0000", "t1")
        current = step_h(initial, PublicDeltaV2(SCHEMA_VERSION, prefix.key, prefix.context, prefix.receipts[0]))
        directions = state_delta(initial, current)
        self.assertEqual(directions["threat"], "increase")
        self.assertEqual(directions["approach"], "decrease")

    def test_incremental_state_rejects_cross_source_instance(self):
        prefix = make_prefix(["CURRENT_COMMITMENT_MISSED"])
        initial = initialize_h(prefix.context, "TEST-INSTANCE-0000", "t1")
        wrong_key = PredictionKey("TEST-INSTANCE-0001", "t1", 1, "p1")
        with self.assertRaises(S0V2Error):
            step_h(initial, PublicDeltaV2(SCHEMA_VERSION, wrong_key, prefix.context, prefix.receipts[0]))

    def test_b1_is_order_invariant(self):
        from dynamics.s0.v2_models import b1_accumulators
        left = make_prefix(["COUNTERPART_OFFERS_COSTLY_REPAIR", "SIMILAR_VIOLATION_REPEATED"])
        right = make_prefix(["SIMILAR_VIOLATION_REPEATED", "COUNTERPART_OFFERS_COSTLY_REPAIR"])
        self.assertEqual(b1_accumulators(left), b1_accumulators(right))

    def test_full_prediction_has_no_directional_common_output(self):
        result = run_full("B2", make_prefix(["CURRENT_COMMITMENT_MISSED"]).to_dict(), self.parameters)
        self.assertNotIn("directional_readout", result)


class V2FairnessTests(unittest.TestCase):
    def test_shared_learner_has_no_model_specific_base_logits(self):
        from pathlib import Path
        source = (Path(__file__).resolve().parents[1] / "s0" / "v2_models.py").read_text(encoding="utf-8")
        self.assertNotIn("_base_logits", source)
        self.assertNotIn("if model_id == \"B1\"", source)
        self.assertIn("COUNTED_MULTINOMIAL_NAIVE_BAYES_NO_MODEL_SPECIFIC_BASE_LOGITS", source)

    def test_authority_probe_fields_are_not_predictive_state(self):
        from dynamics.s0.v2_core import AuthorityProbeState, PredictiveHState
        self.assertTrue(set(AuthorityProbeState.__dataclass_fields__).isdisjoint(PredictiveHState.__dataclass_fields__))

    def test_hidden_source_fields_rejected(self):
        prefix = make_prefix(["CURRENT_COMMITMENT_MISSED"]).to_dict()
        prefix["source_seed"] = "forbidden"
        with self.assertRaises(S0V2Error):
            ObservablePrefixV2.from_dict(prefix)

    def test_counted_learner_reads_multiplicity(self):
        from dynamics.s0.v2_models import fit_parameters
        repeated = make_prefix(["CURRENT_COMMITMENT_MISSED", "CURRENT_COMMITMENT_MISSED"])
        single = make_prefix(["CURRENT_COMMITMENT_MISSED"])
        parameters = empty_parameters()
        fitted = fit_parameters("B2", [(repeated, "ASSERT_BOUNDARY", "CONFLICT_LOOP")], parameters)
        repeated_prediction = predict_full("B2", repeated, fitted)["immediate_action"]
        single_prediction = predict_full("B2", single, fitted)["immediate_action"]
        self.assertNotEqual(repeated_prediction, single_prediction)


if __name__ == "__main__":
    unittest.main()
