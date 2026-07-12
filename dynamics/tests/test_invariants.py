from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from dynamics.engine import DynamicsEngine, EngineConfig
from dynamics.invariants import validate_action_chain, validate_epistemics
from dynamics.scenario import load_scenario
from dynamics.types import (
    BodyState,
    Candidate,
    ClaimState,
    ClaimSignal,
    EpistemicState,
    EvidenceLink,
    EvidenceRelation,
    HumanState,
    JudgmentStance,
    IntentDecision,
    ObservationArtifact,
    ProvenanceKind,
    RoutedCandidate,
    ScenarioEvent,
    SourceContribution,
)


SCENARIO = Path(__file__).parents[1] / "scenarios" / "delayed_reply.json"


class HardInvariantTests(unittest.TestCase):
    def test_wait_candidate_maps_only_to_hold_intent(self) -> None:
        wait = RoutedCandidate(Candidate("candidate:wait", "wait"), 1.0, 1.0, ())
        valid = IntentDecision("intent:hold", "hold", "candidate:wait", 0.0)
        forged = IntentDecision("intent:wait", "wait", "candidate:wait", 0.0)
        ask = RoutedCandidate(Candidate("candidate:ask", "ask"), 1.0, 1.0, ())
        forged_hold = IntentDecision("intent:forged-hold", "hold", "candidate:ask", 0.0)
        nonfinite = IntentDecision("intent:nan", "hold", "candidate:wait", float("nan"))

        self.assertEqual(validate_action_chain(valid, None, None, None, (wait,)), [])
        self.assertIn(
            "ACTION_KIND_MISMATCH_CANDIDATE_INTENT",
            validate_action_chain(forged, None, None, None, (wait,)),
        )
        self.assertIn(
            "ACTION_KIND_MISMATCH_CANDIDATE_INTENT",
            validate_action_chain(forged_hold, None, None, None, (ask,)),
        )
        self.assertIn(
            "INTENT_COERCION_BOUND",
            validate_action_chain(nonfinite, None, None, None, (wait,)),
        )

    def test_internal_simulation_never_becomes_evidence(self) -> None:
        events = tuple(
            ScenarioEvent(
                event_id=f"internal-{tick}",
                tick=tick,
                kind="internal_rehearsal",
                external=False,
                source_id="internal_simulation",
                provenance_kind=ProvenanceKind.IMAGINATION,
                independence_key="same-internal-loop",
                ambiguity=1.0,
                salience=1.0,
                supports=(ClaimSignal("C4_counterpart_rejects_relationship", 1.0, "internal-only"),),
            )
            for tick in range(40)
        )
        result = DynamicsEngine().run(HumanState(), events)
        self.assertEqual(result.ledger.evidence_links, [])
        self.assertEqual(result.final_state.epistemic.claims, ())
        self.assertEqual(result.authority_leak_count, 0)

    def test_same_source_repetition_is_not_independent_evidence(self) -> None:
        events = tuple(
            ScenarioEvent(
                event_id=f"rumor-{tick}",
                tick=tick,
                kind="repeated_adversarial_rumor",
                external=True,
                source_id="friend_a",
                provenance_kind=ProvenanceKind.TESTIMONY,
                independence_key="friend-a-single-rumor",
                supports=(ClaimSignal("C3_counterpart_intentionally_avoids", 0.30, "testimony-avoidance"),),
            )
            for tick in range(30)
        )
        result = DynamicsEngine().run(HumanState(), events)
        claim = result.final_state.epistemic.get("C3_counterpart_intentionally_avoids")
        self.assertAlmostEqual(claim.support_mass, 0.30)
        self.assertEqual(len(claim.supports), 1)
        self.assertEqual(claim.stance, JudgmentStance.HELD)

    def test_duplicate_event_id_is_idempotent(self) -> None:
        event = ScenarioEvent(
            event_id="same-event",
            tick=0,
            kind="platform_online_indicator",
            external=True,
            source_id="sensor",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            independence_key="sensor-reading",
            supports=(ClaimSignal("C1_platform_displayed_online", 0.90, "observe-platform-online"),),
        )
        engine = DynamicsEngine()
        once = engine.run(HumanState(), (event,))
        twice = engine.run(HumanState(), (event, event))
        self.assertEqual(once.final_state, twice.final_state)
        self.assertEqual(twice.ledger.processed, 1)
        self.assertEqual(twice.ledger.duplicate_event_ids, ["same-event"])
        self.assertTrue(twice.input_accounting_ok)

    def test_blocked_attempt_does_not_create_performance_or_action_occurrence(self) -> None:
        scenario = load_scenario(SCENARIO)
        events = tuple(event for event in scenario.events if event.tick <= 5)
        energetic_body = BodyState(energy=0.35, arousal=0.58, action_capacity=0.99)
        blocked_body = BodyState(energy=0.35, arousal=0.58, action_capacity=0.01)
        energetic = DynamicsEngine().run(replace(scenario.initial_state, body=energetic_body), events)
        blocked = DynamicsEngine().run(replace(scenario.initial_state, body=blocked_body), events)

        energetic_tick = energetic.ledger.tick_traces[-1]
        blocked_tick = blocked.ledger.tick_traces[-1]
        self.assertEqual(energetic_tick.routed, blocked_tick.routed)
        self.assertIsNotNone(energetic_tick.attempt)
        self.assertIsNotNone(blocked_tick.attempt)
        self.assertIsNotNone(energetic_tick.performance)
        self.assertIsNone(blocked_tick.performance)
        self.assertIsNone(blocked_tick.action_occurrence)
        self.assertEqual(blocked.phantom_action_count, 0)

    def test_all_persistent_values_remain_bounded(self) -> None:
        scenario = load_scenario(SCENARIO)
        result = scenario.run()
        self.assertFalse(any("NUMERIC_BOUND" in error for error in result.ledger.invariant_errors))
        self.assertEqual(result.ledger.invariant_errors, [])

    def test_grounding_rule_rejects_arbitrary_observation_to_claim_cast(self) -> None:
        forged = ScenarioEvent(
            event_id="forged-grounding",
            tick=0,
            kind="pixel_was_blue",
            external=True,
            source_id="camera",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            independence_key="camera-pixel",
            supports=(
                ClaimSignal(
                    "C3_counterpart_intentionally_avoids",
                    1.0,
                    "observe-platform-online",
                ),
            ),
        )
        result = DynamicsEngine().run(HumanState(), (forged,))
        self.assertEqual(result.ledger.evidence_links, [])
        self.assertGreater(result.authority_leak_count, 0)
        self.assertEqual(
            result.final_state.epistemic.get("C3_counterpart_intentionally_avoids").support_mass,
            0.0,
        )

    def test_claim_scope_prevents_cross_subject_evidence_aggregation(self) -> None:
        events = tuple(
            ScenarioEvent(
                event_id=f"scope-{scope}",
                tick=index,
                kind="ambiguous_no_reply_cue",
                external=True,
                source_id="inbox",
                provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
                independence_key=f"inbox:{scope}",
                supports=(
                    ClaimSignal(
                        "C0_no_reply_observed",
                        0.50,
                        "observe-no-reply",
                        scope=scope,
                    ),
                ),
            )
            for index, scope in enumerate(("person:a", "person:b"))
        )
        result = DynamicsEngine().run(HumanState(), events)
        for scope in ("person:a", "person:b"):
            claim = result.final_state.epistemic.get("C0_no_reply_observed", scope)
            self.assertAlmostEqual(claim.support_mass, 0.50)
            self.assertEqual(claim.stance, JudgmentStance.HELD)

    def test_support_and_contradiction_in_one_event_are_adjudicated_atomically(self) -> None:
        event = ScenarioEvent(
            event_id="atomic-bundle",
            tick=0,
            kind="counterpart_explanation_message",
            external=True,
            source_id="counterpart",
            provenance_kind=ProvenanceKind.TESTIMONY,
            independence_key="counterpart:atomic",
            supports=(
                ClaimSignal(
                    "C3_counterpart_intentionally_avoids",
                    0.80,
                    "testimony-avoidance",
                ),
            ),
            contradicts=(
                ClaimSignal(
                    "C3_counterpart_intentionally_avoids",
                    0.30,
                    "testimony-denies-avoidance",
                ),
            ),
        )
        result = DynamicsEngine().run(HumanState(), (event,))
        claim = result.final_state.epistemic.get("C3_counterpart_intentionally_avoids")
        self.assertAlmostEqual(claim.confidence, 0.80 / 1.30)
        self.assertEqual(claim.stance, JudgmentStance.HELD)
        self.assertEqual(result.authority_leak_count, 0)

    def test_event_id_payload_collision_is_hard_error_not_duplicate(self) -> None:
        first = ScenarioEvent(
            event_id="collision",
            tick=0,
            kind="platform_online_indicator",
            external=True,
            source_id="platform",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            independence_key="platform:online",
            supports=(
                ClaimSignal(
                    "C1_platform_displayed_online",
                    0.90,
                    "observe-platform-online",
                ),
            ),
        )
        conflicting = replace(
            first,
            supports=(
                ClaimSignal(
                    "C1_platform_displayed_online",
                    0.80,
                    "observe-platform-online",
                ),
            ),
        )
        result = DynamicsEngine().run(HumanState(), (first, conflicting))
        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(result.ledger.duplicate_event_ids, [])
        self.assertEqual(result.ledger.collision_event_ids, ["collision"])
        self.assertIn("collision:EVENT_ID_PAYLOAD_COLLISION", result.ledger.invariant_errors)
        self.assertTrue(result.input_accounting_ok)

    def test_imagination_cannot_smuggle_an_action_window(self) -> None:
        event = ScenarioEvent(
            event_id="imagined-action-window",
            tick=0,
            kind="internal_rejection_simulation",
            external=False,
            source_id="internal_simulation",
            provenance_kind=ProvenanceKind.IMAGINATION,
            independence_key="internal",
            ambiguity=1.0,
            time_pressure=1.0,
            action_window=True,
        )
        result = DynamicsEngine().run(HumanState(), (event,))
        self.assertEqual(result.ledger.attempts, [])
        self.assertEqual(result.ledger.performance_receipts, [])
        self.assertEqual(result.ledger.action_occurrences, [])
        self.assertIn(
            "imagined-action-window:INVALID_ACTION_WINDOW_EVENT",
            result.ledger.invariant_errors,
        )

    def test_json_loader_rejects_string_booleans(self) -> None:
        payload = {
            "schema_version": "human-model-scenario/0.1",
            "scenario_id": "bad-bool",
            "initial_state": {},
            "events": [
                {
                    "event_id": "bad",
                    "tick": 0,
                    "kind": "quiet",
                    "external": "false",
                    "source_id": "test",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(TypeError):
                load_scenario(path)

    def test_validator_independently_rejects_forged_grounding_link(self) -> None:
        artifact = ObservationArtifact(
            artifact_id="artifact:forged",
            event_id="forged",
            source_tick=0,
            observed_tick=0,
            kind="platform_online_indicator",
            source_id="platform",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            external=True,
        )
        link = EvidenceLink(
            link_id="link:forged",
            artifact_id=artifact.artifact_id,
            claim_id="C3_counterpart_intentionally_avoids",
            relation=EvidenceRelation.SUPPORTS,
            strength=0.90,
            scope="scenario",
            independence_key="forged",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            grounding_rule_id="observe-platform-online",
        )
        claim = ClaimState(
            claim_id=link.claim_id,
            supports=(SourceContribution("forged", link.link_id, 0.90),),
            stance=JudgmentStance.ADOPTED,
            grounds=(link.link_id,),
        )
        errors = validate_epistemics(
            EpistemicState((claim,)),
            {link.link_id: link},
            {artifact.artifact_id: artifact},
            (link,),
            adoption_threshold=0.75,
            release_threshold=0.55,
            minimum_ground_mass=0.50,
        )
        self.assertIn("AUTHORITY_LINK_RULE_MISMATCH:link:forged", errors)

    def test_validator_rejects_forged_assessment_multiplicity_and_nonfinite_mass(self) -> None:
        artifact = ObservationArtifact(
            artifact_id="artifact:mass-forgery",
            event_id="mass-forgery",
            source_tick=0,
            observed_tick=0,
            kind="platform_online_indicator",
            source_id="platform",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            external=True,
        )
        link = EvidenceLink(
            link_id="link:mass-forgery:C1_platform_displayed_online:scenario:supports",
            artifact_id=artifact.artifact_id,
            claim_id="C1_platform_displayed_online",
            relation=EvidenceRelation.SUPPORTS,
            strength=0.5,
            scope="scenario",
            independence_key="same-source",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            grounding_rule_id="observe-platform-online",
        )
        duplicate_contribution = SourceContribution(
            "same-source",
            link.link_id,
            0.5,
        )
        duplicated = ClaimState(
            claim_id=link.claim_id,
            supports=(duplicate_contribution, duplicate_contribution),
            grounds=(link.link_id, link.link_id),
        )
        duplicate_errors = validate_epistemics(
            EpistemicState((duplicated, duplicated)),
            {link.link_id: link},
            {artifact.artifact_id: artifact},
            adoption_threshold=0.75,
            release_threshold=0.55,
            minimum_ground_mass=0.50,
        )
        self.assertTrue(
            any("AUTHORITY_DUPLICATE_INDEPENDENCE_KEY" in error for error in duplicate_errors)
        )
        self.assertIn(
            "AUTHORITY_DUPLICATE_CLAIM_KEY:C1_platform_displayed_online:scenario",
            duplicate_errors,
        )

        nonfinite_link = replace(link, strength=float("nan"))
        nonfinite = ClaimState(
            claim_id=link.claim_id,
            supports=(
                SourceContribution(
                    "same-source",
                    link.link_id,
                    float("nan"),
                ),
            ),
            grounds=(link.link_id,),
        )
        nonfinite_errors = validate_epistemics(
            EpistemicState((nonfinite,)),
            {link.link_id: nonfinite_link},
            {artifact.artifact_id: artifact},
            adoption_threshold=0.75,
            release_threshold=0.55,
            minimum_ground_mass=0.50,
        )
        self.assertTrue(
            any("NONFINITE" in error or "INVALID_LINK_STRENGTH" in error for error in nonfinite_errors)
        )

    def test_empty_run_still_validates_initial_state(self) -> None:
        invalid = HumanState(body=BodyState(energy=1.5, arousal=0.2, action_capacity=0.5))
        result = DynamicsEngine().run(invalid, ())
        self.assertTrue(any("NUMERIC_BOUND:body.energy" in error for error in result.ledger.invariant_errors))


if __name__ == "__main__":
    unittest.main()
