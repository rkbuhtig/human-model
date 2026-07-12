from __future__ import annotations

import ast
from dataclasses import fields
from pathlib import Path
import unittest

from dynamics.contract import (
    ActionOpportunity,
    ActionAttempt,
    EvidenceAssessmentState,
    EvidenceRelation,
    GroundingSignal,
    IntentDecision,
    MotorFeasibility,
    ObservationArtifact,
    links_from_submission,
    validate_action_opportunity,
)
from dynamics.interfaces import ModelInput
from dynamics.models import HumanState, run_action_pipeline
from dynamics.protocol import (
    ClaimSignal,
    ScenarioEvent,
    action_opportunity_from_event,
    encode_grounding_submission,
    encode_model_input,
)
from dynamics.types import BodyAuthorization as FacadeBodyAuthorization
from dynamics.types import EpistemicState as FacadeEpistemicState
from dynamics.types import ProvenanceKind


PACKAGE = Path(__file__).parents[1]


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            base = prefix + (node.module or "")
            result.add(base)
            for alias in node.names:
                separator = "." if node.module else ""
                result.add(base + separator + alias.name)
    return result


class PackageBoundaryTests(unittest.TestCase):
    def test_contract_does_not_import_model_protocol_or_facade(self) -> None:
        forbidden = (
            "..models",
            "..protocol",
            "..types",
            "..mental_transitions",
            "..reducer_proposals",
            "dynamics.models",
            "dynamics.protocol",
            "dynamics.mental_transitions",
            "dynamics.reducer_proposals",
        )
        for path in (PACKAGE / "contract").rglob("*.py"):
            imports = _imports(path)
            self.assertFalse(
                any(name.startswith(forbidden) for name in imports),
                f"{path.name}: {sorted(imports)}",
            )

    def test_models_do_not_import_protocol_or_facade(self) -> None:
        forbidden = (
            "..protocol",
            "..types",
            "..mental_transitions",
            "..reducer_proposals",
            "dynamics.protocol",
            "dynamics.types",
            "dynamics.mental_transitions",
            "dynamics.reducer_proposals",
        )
        for path in (PACKAGE / "models").rglob("*.py"):
            imports = _imports(path)
            self.assertFalse(
                any(name.startswith(forbidden) for name in imports),
                f"{path.name}: {sorted(imports)}",
            )

    def test_protocol_does_not_import_human_state_or_facade(self) -> None:
        forbidden = (
            "..models",
            "..types",
            "..mental_transitions",
            "..reducer_proposals",
            "dynamics.models",
            "dynamics.types",
            "dynamics.mental_transitions",
            "dynamics.reducer_proposals",
        )
        for path in (PACKAGE / "protocol").rglob("*.py"):
            imports = _imports(path)
            self.assertFalse(
                any(name.startswith(forbidden) for name in imports),
                f"{path.name}: {sorted(imports)}",
            )

    def test_engine_uses_canonical_packages_not_legacy_facades(self) -> None:
        imports = _imports(PACKAGE / "engine.py")
        self.assertNotIn(".types", imports)
        self.assertNotIn(".epistemics", imports)
        self.assertNotIn(".routing", imports)
        self.assertNotIn(".invariants", imports)

    def test_legacy_names_are_exact_import_aliases(self) -> None:
        self.assertIs(FacadeEpistemicState, EvidenceAssessmentState)
        self.assertIs(FacadeBodyAuthorization, MotorFeasibility)
        import dynamics.contract as contract

        self.assertFalse(hasattr(contract, "EpistemicState"))
        self.assertFalse(hasattr(contract, "BodyAuthorization"))

    def test_canonical_state_and_motor_names_are_stored(self) -> None:
        self.assertIn("evidence_assessment", {item.name for item in fields(HumanState)})
        self.assertNotIn("epistemic", {item.name for item in fields(HumanState)})
        state = HumanState()
        self.assertIs(state.epistemic, state.evidence_assessment)

        feasibility = MotorFeasibility("mf:1", True, 0.8, 0.4)
        attempt = ActionAttempt("a:1", "i:1", "ask", feasibility, 0)
        self.assertIs(attempt.authorization, attempt.motor_feasibility)
        self.assertEqual(feasibility.authorization_id, feasibility.feasibility_id)
        self.assertEqual(feasibility.allowed, feasibility.feasible)

        legacy_assessment = EvidenceAssessmentState()
        legacy_state = HumanState(epistemic=legacy_assessment)
        legacy_feasibility = FacadeBodyAuthorization(
            authorization_id="legacy:1",
            allowed=True,
            available_capacity=0.8,
            required_capacity=0.4,
        )
        legacy_attempt = ActionAttempt(
            attempt_id="legacy-attempt:1",
            intent_id="legacy-intent:1",
            action_kind="ask",
            authorization=legacy_feasibility,
            tick=0,
        )
        self.assertIs(legacy_state.evidence_assessment, legacy_assessment)
        self.assertIs(legacy_attempt.motor_feasibility, legacy_feasibility)

    def test_model_projection_excludes_grounding_and_evidence_fields(self) -> None:
        event = ScenarioEvent(
            event_id="projection",
            tick=0,
            kind="friend_interpretation",
            external=True,
            source_id="friend",
            provenance_kind=ProvenanceKind.TESTIMONY,
            independence_key="friend:one",
            supports=(
                ClaimSignal(
                    "C5_friend_said_avoidance",
                    0.5,
                    "observe-friend-speech",
                ),
            ),
        )
        model_input = encode_model_input(event)
        self.assertIsInstance(model_input, ModelInput)
        model_fields = {item.name for item in fields(ModelInput)}
        self.assertTrue(
            {
                "supports",
                "contradicts",
                "provenance_kind",
                "independence_key",
                "action_window",
            }.isdisjoint(
                model_fields
            )
        )
        submission = encode_grounding_submission(event)
        self.assertEqual(len(submission.signals), 1)
        self.assertFalse(hasattr(submission, "ambiguity"))

    def test_invalid_raw_action_window_is_not_encoded_as_model_authority(self) -> None:
        event = ScenarioEvent(
            event_id="imagined-window",
            tick=0,
            kind="internal_rehearsal",
            external=False,
            source_id="simulation",
            provenance_kind=ProvenanceKind.IMAGINATION,
            independence_key="internal",
            action_window=True,
        )
        model_input = encode_model_input(event)
        opportunity, error = action_opportunity_from_event(event)
        self.assertFalse(hasattr(model_input, "action_window"))
        self.assertIsNone(opportunity)
        self.assertEqual(error, "INVALID_ACTION_WINDOW_EVENT")
        self.assertEqual(
            run_action_pipeline(HumanState(), model_input, ()),
            (None, None, None, None),
        )

    def test_grounding_submission_must_match_its_observation_artifact(self) -> None:
        event = ScenarioEvent(
            event_id="submission-event",
            tick=0,
            kind="platform_online_indicator",
            external=True,
            source_id="platform",
            provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
            independence_key="platform:one",
            supports=(
                ClaimSignal(
                    "C1_platform_displayed_online",
                    0.8,
                    "observe-platform-online",
                ),
            ),
        )
        artifact = ObservationArtifact(
            artifact_id="artifact:other-event",
            event_id="other-event",
            source_tick=0,
            observed_tick=0,
            kind=event.kind,
            source_id=event.source_id,
            provenance_kind=event.provenance_kind,
            external=True,
        )
        links, errors = links_from_submission(
            encode_grounding_submission(event),
            artifact,
        )
        self.assertEqual(links, ())
        self.assertEqual(
            errors,
            ("PROVENANCE_SUBMISSION_ARTIFACT_MISMATCH:event_id",),
        )

    def test_contract_grounding_signal_rejects_invalid_strength_and_scope(self) -> None:
        for strength in (float("nan"), -0.1, 1.1):
            with self.subTest(strength=strength), self.assertRaises(ValueError):
                GroundingSignal(
                    claim_id="C1_platform_displayed_online",
                    strength=strength,
                    rule_id="observe-platform-online",
                    relation=EvidenceRelation.SUPPORTS,
                )
        with self.assertRaises(ValueError):
            GroundingSignal(
                claim_id="C1_platform_displayed_online",
                strength=0.8,
                rule_id="observe-platform-online",
                relation=EvidenceRelation.SUPPORTS,
                scope="",
            )

    def test_action_opportunity_is_auditable_before_intent(self) -> None:
        intent = IntentDecision("intent:e", "hold", "candidate:e", 0.0)
        self.assertEqual(
            validate_action_opportunity(None, intent, event_id="e"),
            ["PHANTOM_INTENT_WITHOUT_ACTION_OPPORTUNITY"],
        )
        forged = ActionOpportunity("forged", "e", "internal-decision-window-v01")
        self.assertEqual(
            validate_action_opportunity(forged, intent, event_id="e"),
            [
                "ACTION_OPPORTUNITY_IDENTITY_MISMATCH",
                "INTENT_ACTION_OPPORTUNITY_MISMATCH",
            ],
        )


if __name__ == "__main__":
    unittest.main()
