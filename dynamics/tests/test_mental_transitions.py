from __future__ import annotations

from dataclasses import fields, replace
import unittest

from dynamics.contract import ProvenanceKind
from dynamics.engine import DynamicsEngine, EngineConfig
from dynamics.mental_transitions import (
    CanonicalWindowDuration,
    MentalStateDelta,
    MentalTransition,
    MentalTransitionLedger,
    MentalTransitionQualificationPolicy,
    MentalTransitionWindowReport,
    PERSISTENT_DESCRIPTIVE_FIELDS,
    QualifiedTransitionCount,
    QualifiedTransitionDensity,
    TransitionQualificationReceipt,
    build_mental_transition_ledger,
)
from dynamics.models import HumanState
from dynamics.protocol import ScenarioEvent
from dynamics.temporal import EventTemporalEnvelope, SimTime


HABIT_FIELD = "habit.impulsivity"
UNCHANGED_HABIT_FIELD = "habit.withdrawal_bias"


def _policy(
    *,
    minimum_absolute_delta: float = 0.0001,
    state_fields: tuple[str, ...] = (HABIT_FIELD,),
) -> MentalTransitionQualificationPolicy:
    return MentalTransitionQualificationPolicy(
        minimum_absolute_delta=minimum_absolute_delta,
        state_fields=state_fields,
    )


def _event(
    delivery_id: str,
    *,
    occurrence_id: str | None = None,
    occurred_at: int = 0,
    available_at: int = 0,
    delivery_sequence: int | None = None,
    reexposure_of_occurrence_id: str | None = None,
    soothing: float = 0.0,
) -> ScenarioEvent:
    occurrence = occurrence_id or f"occurrence:{delivery_id}"
    return ScenarioEvent(
        event_id=delivery_id,
        tick=available_at,
        kind="internal_rehearsal",
        external=False,
        source_id="internal",
        provenance_kind=ProvenanceKind.IMAGINATION,
        independence_key="internal",
        soothing=soothing,
        temporal=EventTemporalEnvelope(
            occurrence_id=occurrence,
            delivery_id=delivery_id,
            occurred_at=SimTime(occurred_at),
            available_at=SimTime(available_at),
            delivery_sequence=delivery_sequence,
            reexposure_of_occurrence_id=reexposure_of_occurrence_id,
        ),
    )


def _run(
    events: tuple[ScenarioEvent, ...],
    policy: MentalTransitionQualificationPolicy,
    *,
    capacity: int = 6,
    drain_ticks: int = 2,
):
    return DynamicsEngine(
        EngineConfig(
            base_capacity_per_tick=capacity,
            drain_ticks=drain_ticks,
            mental_transition_policy=policy,
        )
    ).run(HumanState(), events)


def _non_mental_projection(result) -> tuple[object, ...]:
    """Everything the read-only Q projection must not feed back into."""

    return (
        result.final_state,
        tuple(result.ledger.observations),
        tuple(result.ledger.evidence_links),
        tuple(result.ledger.episode_traces),
        tuple(result.ledger.tick_traces),
        tuple(result.ledger.action_opportunities),
        tuple(result.ledger.attempts),
        tuple(result.ledger.performance_receipts),
        tuple(result.ledger.action_occurrences),
        tuple(result.ledger.invariant_errors),
    )


class MentalTransitionLedgerTests(unittest.TestCase):
    def test_one_receipt_per_processed_occurrence_and_qualified_subset(self) -> None:
        unchanged = _event(
            "delivery:unchanged",
            occurrence_id="occurrence:unchanged",
            delivery_sequence=1,
        )
        changed = _event(
            "delivery:changed",
            occurrence_id="occurrence:changed",
            delivery_sequence=2,
            soothing=1.0,
        )
        result = _run((unchanged, changed), _policy())
        ledger = result.ledger.mental_transitions

        self.assertEqual(len(ledger.receipts), result.ledger.processed)
        self.assertEqual(len(ledger.receipts), 2)
        self.assertEqual([receipt.qualified for receipt in ledger.receipts], [False, True])
        self.assertEqual(len(ledger.transitions), 1)
        self.assertEqual(
            {transition.qualification_receipt_id for transition in ledger.transitions},
            {receipt.receipt_id for receipt in ledger.receipts if receipt.qualified},
        )
        self.assertEqual(
            [receipt.cause_occurrence_id for receipt in ledger.receipts],
            ["occurrence:unchanged", "occurrence:changed"],
        )
        self.assertEqual(
            ledger,
            build_mental_transition_ledger(
                result.ledger.tick_traces,
                result.ledger.mental_transitions.policy,
            ),
        )
        forged_duplicate = replace(
            ledger.transitions[0],
            transition_id=ledger.transitions[0].transition_id + ":forged",
        )
        with self.assertRaisesRegex(ValueError, "only one transition"):
            MentalTransitionLedger(
                policy=ledger.policy,
                receipts=ledger.receipts,
                transitions=(ledger.transitions[0], forged_duplicate),
            )
        qualified_index = next(
            index for index, receipt in enumerate(ledger.receipts) if receipt.qualified
        )
        with self.assertRaisesRegex(ValueError, "checkpoint processed_at"):
            replace(
                ledger.receipts[qualified_index],
                qualified_at=SimTime(99),
            )
        unqualified_receipt = next(
            receipt for receipt in ledger.receipts if not receipt.qualified
        )
        with self.assertRaisesRegex(ValueError, "checkpoint processed_at"):
            replace(unqualified_receipt, qualified_at=SimTime(99))
        duplicate_occurrence_receipt = replace(
            ledger.receipts[0],
            receipt_id=ledger.receipts[0].receipt_id + ":forged",
            cause_delivery_id="delivery:forged-duplicate-occurrence",
            processing_sequence=3,
        )
        with self.assertRaisesRegex(ValueError, "only one receipt"):
            MentalTransitionLedger(
                policy=ledger.policy,
                receipts=(*ledger.receipts, duplicate_occurrence_receipt),
                transitions=ledger.transitions,
            )
        qualified_receipt = ledger.receipts[qualified_index]
        with self.assertRaisesRegex(ValueError, "complete processing order"):
            MentalTransitionLedger(
                policy=ledger.policy,
                receipts=(qualified_receipt,),
                transitions=ledger.transitions,
            )

    def test_transport_redelivery_does_not_create_mental_transition(self) -> None:
        first = _event(
            "delivery:first",
            occurrence_id="occurrence:soothing",
            soothing=1.0,
        )
        redelivery = _event(
            "delivery:redelivery",
            occurrence_id="occurrence:soothing",
            available_at=1,
            soothing=1.0,
        )
        result = _run((first, first, redelivery), _policy())
        ledger = result.ledger.mental_transitions

        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(
            [decision.disposition for decision in result.ledger.ingress_decisions],
            ["accepted", "duplicate", "redundant_delivery"],
        )
        self.assertEqual(len(ledger.receipts), 1)
        self.assertEqual(len(ledger.transitions), 1)
        self.assertEqual(ledger.transitions[0].cause_occurrence_id, "occurrence:soothing")

    def test_explicit_current_reexposure_can_independently_qualify(self) -> None:
        source = _event(
            "delivery:source",
            occurrence_id="occurrence:source",
            occurred_at=4,
            available_at=4,
        )
        reexposure = _event(
            "delivery:reexposure",
            occurrence_id="occurrence:reexposure",
            occurred_at=5,
            available_at=5,
            reexposure_of_occurrence_id="occurrence:source",
            soothing=1.0,
        )
        result = _run((source, reexposure), _policy())
        ledger = result.ledger.mental_transitions

        self.assertEqual(len(ledger.receipts), 2)
        self.assertEqual([receipt.qualified for receipt in ledger.receipts], [False, True])
        self.assertEqual(len(ledger.transitions), 1)
        transition = ledger.transitions[0]
        self.assertEqual(transition.cause_occurrence_id, "occurrence:reexposure")
        self.assertEqual(
            transition.reexposure_of_occurrence_id,
            "occurrence:source",
        )
        receipt = next(
            item
            for item in ledger.receipts
            if item.cause_occurrence_id == "occurrence:reexposure"
        )
        self.assertEqual(receipt.reexposure_of_occurrence_id, "occurrence:source")
        self.assertEqual(receipt.cause_occurred_at, SimTime(5))
        self.assertEqual(receipt.became_available_at, SimTime(5))
        with self.assertRaisesRegex(ValueError, "earlier processed occurrence"):
            MentalTransitionLedger(
                policy=ledger.policy,
                receipts=tuple(
                    replace(
                        item,
                        reexposure_of_occurrence_id="occurrence:missing",
                    )
                    if item is receipt
                    else item
                    for item in ledger.receipts
                ),
                transitions=ledger.transitions,
            )
        with self.assertRaisesRegex(ValueError, "predate source processing"):
            MentalTransitionLedger(
                policy=ledger.policy,
                receipts=tuple(
                    replace(item, cause_occurred_at=SimTime(3))
                    if item is receipt
                    else item
                    for item in ledger.receipts
                ),
                transitions=ledger.transitions,
            )
        with self.assertRaisesRegex(ValueError, "own occurrence"):
            replace(
                receipt,
                reexposure_of_occurrence_id=receipt.cause_occurrence_id,
            )

    def test_policy_ablation_changes_only_read_only_ledger(self) -> None:
        event = _event(
            "delivery:soothing",
            occurrence_id="occurrence:soothing",
            soothing=1.0,
        )
        low_threshold = _run((event,), _policy(minimum_absolute_delta=0.0001))
        high_threshold = _run((event,), _policy(minimum_absolute_delta=0.001))
        other_scope = _run(
            (event,),
            _policy(state_fields=(UNCHANGED_HABIT_FIELD,)),
        )

        self.assertEqual(len(low_threshold.ledger.mental_transitions.transitions), 1)
        self.assertEqual(len(high_threshold.ledger.mental_transitions.transitions), 0)
        self.assertEqual(len(other_scope.ledger.mental_transitions.transitions), 0)
        self.assertEqual(
            _non_mental_projection(low_threshold),
            _non_mental_projection(high_threshold),
        )
        self.assertEqual(
            _non_mental_projection(low_threshold),
            _non_mental_projection(other_scope),
        )

    def test_backlog_times_are_preserved_and_effective_at_is_processed_at(self) -> None:
        blocker = _event(
            "delivery:blocker",
            occurrence_id="occurrence:blocker",
            occurred_at=4,
            available_at=4,
            delivery_sequence=1,
        )
        target = _event(
            "delivery:target",
            occurrence_id="occurrence:past",
            occurred_at=1,
            available_at=4,
            delivery_sequence=2,
            soothing=1.0,
        )
        result = _run(
            (blocker, target),
            _policy(),
            capacity=1,
            drain_ticks=1,
        )
        transition = next(
            item
            for item in result.ledger.mental_transitions.transitions
            if item.cause_occurrence_id == "occurrence:past"
        )

        self.assertEqual(transition.cause_occurred_at, SimTime(1))
        self.assertEqual(transition.became_available_at, SimTime(4))
        self.assertEqual(transition.processed_at, SimTime(5))
        self.assertEqual(transition.transition_effective_at, transition.processed_at)
        self.assertEqual(transition.qualified_at, transition.processed_at)
        receipt = next(
            item
            for item in result.ledger.mental_transitions.receipts
            if item.cause_occurrence_id == "occurrence:past"
        )
        self.assertEqual(receipt.cause_occurred_at, SimTime(1))
        self.assertEqual(receipt.became_available_at, SimTime(4))
        self.assertEqual(receipt.processed_at, SimTime(5))

    def test_future_events_cannot_requalify_prefix(self) -> None:
        prefix_events = (
            _event(
                "delivery:prefix-1",
                occurrence_id="occurrence:prefix-1",
                available_at=0,
            ),
            _event(
                "delivery:prefix-2",
                occurrence_id="occurrence:prefix-2",
                available_at=1,
                soothing=1.0,
            ),
        )
        future = _event(
            "delivery:future",
            occurrence_id="occurrence:future",
            available_at=10,
            soothing=1.0,
        )
        prefix = _run(prefix_events, _policy(), drain_ticks=0)
        extended = _run((*prefix_events, future), _policy(), drain_ticks=0)
        prefix_ledger = prefix.ledger.mental_transitions
        extended_ledger = extended.ledger.mental_transitions

        self.assertEqual(
            extended_ledger.receipts[: len(prefix_ledger.receipts)],
            prefix_ledger.receipts,
        )
        self.assertEqual(
            extended_ledger.transitions[: len(prefix_ledger.transitions)],
            prefix_ledger.transitions,
        )
        self.assertGreaterEqual(len(extended_ledger.transitions), 2)
        with self.assertRaisesRegex(ValueError, "processing order"):
            MentalTransitionLedger(
                policy=extended_ledger.policy,
                receipts=extended_ledger.receipts,
                transitions=tuple(reversed(extended_ledger.transitions)),
            )

    def test_transition_window_keeps_count_and_density_distinct(self) -> None:
        first = _event(
            "delivery:first",
            occurrence_id="occurrence:first",
            available_at=0,
            soothing=1.0,
        )
        endpoint = _event(
            "delivery:endpoint",
            occurrence_id="occurrence:endpoint",
            available_at=2,
            soothing=1.0,
        )
        ledger = _run((first, endpoint), _policy(), drain_ticks=0).ledger.mental_transitions

        report = ledger.window_report(SimTime(0), SimTime(2))
        self.assertIs(type(report.canonical_duration), CanonicalWindowDuration)
        self.assertIs(type(report.qualified_count), QualifiedTransitionCount)
        self.assertIs(type(report.density_per_sim_time), QualifiedTransitionDensity)
        self.assertEqual(report.canonical_duration, 2)
        self.assertEqual(report.qualified_count, 1)
        self.assertAlmostEqual(report.density_per_sim_time, 0.5)

        endpoint_report = ledger.window_report(SimTime(2), SimTime(3))
        self.assertEqual(endpoint_report.qualified_count, 1)
        self.assertAlmostEqual(endpoint_report.density_per_sim_time, 1.0)
        with self.assertRaises(ValueError):
            ledger.window_report(SimTime(1), SimTime(1))
        with self.assertRaises(ValueError):
            ledger.window_report(SimTime(2), SimTime(1))
        with self.assertRaisesRegex(TypeError, "plain float"):
            QualifiedTransitionDensity(QualifiedTransitionCount(2))
        with self.assertRaisesRegex(TypeError, "plain float"):
            QualifiedTransitionDensity(CanonicalWindowDuration(2))

        empty = _run((), _policy(), drain_ticks=0).ledger.mental_transitions
        empty_report = empty.window_report(SimTime(0), SimTime(1))
        self.assertEqual(empty.receipts, ())
        self.assertEqual(empty.transitions, ())
        self.assertEqual(empty_report.qualified_count, 0)
        self.assertEqual(empty_report.density_per_sim_time, 0.0)


class MentalTransitionPolicyTests(unittest.TestCase):
    def test_policy_digest_changes_with_threshold_or_scope(self) -> None:
        base = _policy(minimum_absolute_delta=0.0001)
        same = _policy(minimum_absolute_delta=0.0001)
        threshold_changed = _policy(minimum_absolute_delta=0.001)
        scope_changed = _policy(state_fields=(UNCHANGED_HABIT_FIELD,))

        self.assertEqual(base.policy_digest, same.policy_digest)
        self.assertNotEqual(base.policy_digest, threshold_changed.policy_digest)
        self.assertNotEqual(base.policy_digest, scope_changed.policy_digest)

        event = _event(
            "delivery:policy-identity",
            occurrence_id="occurrence:policy-identity",
            soothing=1.0,
        )
        base_receipt = _run((event,), base).ledger.mental_transitions.receipts[0]
        changed_receipt = _run(
            (event,), threshold_changed
        ).ledger.mental_transitions.receipts[0]
        self.assertNotEqual(base_receipt.receipt_id, changed_receipt.receipt_id)

    def test_policy_rejects_unknown_or_duplicate_state_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown"):
            _policy(state_fields=("unknown.field",))
        with self.assertRaisesRegex(ValueError, "unique"):
            _policy(state_fields=(HABIT_FIELD, HABIT_FIELD))
        with self.assertRaisesRegex(ValueError, "current-trace"):
            MentalTransitionQualificationPolicy(
                state_fields=(HABIT_FIELD,),
                available_information=("future_outcome",),
            )
        with self.assertRaisesRegex(ValueError, "identity and version are fixed"):
            MentalTransitionQualificationPolicy(
                qualifier_id="morphic-load",
                qualifier_version="999.0.0",
                state_fields=(HABIT_FIELD,),
            )
        with self.assertRaisesRegex(ValueError, "must be finite"):
            MentalStateDelta(
                field=HABIT_FIELD,
                before=float("nan"),
                after=0.5,
                delta=0.0,
                unit="normalized_simulation_unit",
            )
        self.assertIn(HABIT_FIELD, PERSISTENT_DESCRIPTIVE_FIELDS)

    def test_tuple_typed_artifacts_reject_mutable_lists(self) -> None:
        mutable_scope = [HABIT_FIELD]
        with self.assertRaisesRegex(TypeError, "immutable tuple"):
            MentalTransitionQualificationPolicy(state_fields=mutable_scope)  # type: ignore[arg-type]

        event = _event(
            "delivery:immutable",
            occurrence_id="occurrence:immutable",
            soothing=1.0,
        )
        ledger = _run((event,), _policy()).ledger.mental_transitions
        with self.assertRaisesRegex(TypeError, "immutable tuple"):
            MentalTransitionLedger(
                policy=ledger.policy,
                receipts=list(ledger.receipts),  # type: ignore[arg-type]
                transitions=ledger.transitions,
            )
        with self.assertRaisesRegex(TypeError, "immutable tuple"):
            replace(
                ledger.receipts[0],
                typed_deltas=list(ledger.receipts[0].typed_deltas),  # type: ignore[arg-type]
            )

    def test_schema_has_no_morphic_or_qualia_fields_and_no_state_feedback(self) -> None:
        schema_types = (
            MentalTransitionQualificationPolicy,
            MentalStateDelta,
            TransitionQualificationReceipt,
            MentalTransition,
            MentalTransitionWindowReport,
            MentalTransitionLedger,
        )
        field_names = {
            item.name.lower()
            for schema_type in schema_types
            for item in fields(schema_type)
        }
        for forbidden in (
            "morphic",
            "qualia",
            "phenomenal",
            "deformation",
            "strain",
        ):
            self.assertFalse(
                any(forbidden in name for name in field_names),
                (forbidden, sorted(field_names)),
            )

        event = _event(
            "delivery:projection-only",
            occurrence_id="occurrence:projection-only",
            soothing=1.0,
        )
        low = _run((event,), _policy(minimum_absolute_delta=0.0001))
        high = _run((event,), _policy(minimum_absolute_delta=0.001))
        self.assertEqual(_non_mental_projection(low), _non_mental_projection(high))


if __name__ == "__main__":
    unittest.main()
