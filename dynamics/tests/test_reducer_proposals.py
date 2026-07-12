from __future__ import annotations

from dataclasses import fields, replace
import unittest

from dynamics.adapters import legacy_v01_access_pressure_bridge
from dynamics.contract import PerformanceReceipt, ProvenanceKind
from dynamics.engine import DynamicsEngine, EngineConfig
from dynamics.interfaces import ModelInput
from dynamics.mental_transitions import MentalTransitionQualificationPolicy
from dynamics.models import (
    BodyState,
    HabitPolicy,
    HumanState,
    PhenomenalActivation,
    ReducerDriverChannel,
    ReducerDriverContribution,
    ReducerFieldProposal,
    apply_fast_update,
    apply_fast_update_traced,
    apply_slow_update,
    apply_slow_update_traced,
    phenomenal_activation,
)
from dynamics.protocol import ScenarioEvent, encode_model_input
from dynamics.reducer_proposals import (
    REDUCER_PROPOSAL_MODEL_ID,
    ReducerProposalLedger,
    ReducerProposalReceipt,
    _receipt_id,
    build_reducer_proposal_ledger,
)
from dynamics.scenario import load_scenario
from dynamics.temporal import EventTemporalEnvelope, SimTime


def _event(
    delivery_id: str,
    *,
    occurrence_id: str | None = None,
    occurred_at: int = 0,
    available_at: int = 0,
    delivery_sequence: int | None = None,
    reexposure_of_occurrence_id: str | None = None,
    energy_delta: float = 0.0,
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
        energy_delta=energy_delta,
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
    *,
    initial_state: HumanState | None = None,
    mental_policy: MentalTransitionQualificationPolicy | None = None,
):
    config = EngineConfig(
        drain_ticks=0,
        mental_transition_policy=(
            mental_policy or MentalTransitionQualificationPolicy()
        ),
    )
    return DynamicsEngine(config).run(initial_state or HumanState(), events)


def _proposal(receipt: ReducerProposalReceipt, operator_id: str) -> ReducerFieldProposal:
    return next(
        proposal
        for proposal in receipt.proposals
        if proposal.operator_id == operator_id
    )


class ReducerProposalLedgerTests(unittest.TestCase):
    def test_one_reducer_proposal_receipt_per_processed_occurrence(self) -> None:
        events = (
            _event(
                "delivery:first",
                occurrence_id="occurrence:first",
                delivery_sequence=1,
            ),
            _event(
                "delivery:second",
                occurrence_id="occurrence:second",
                delivery_sequence=2,
                soothing=1.0,
            ),
        )
        result = _run(events)
        ledger = result.ledger.reducer_proposals

        self.assertEqual(len(ledger.receipts), result.ledger.processed)
        self.assertEqual(
            [receipt.processing_sequence for receipt in ledger.receipts],
            [1, 2],
        )
        self.assertEqual(
            [receipt.cause_occurrence_id for receipt in ledger.receipts],
            ["occurrence:first", "occurrence:second"],
        )
        self.assertEqual(
            ledger,
            build_reducer_proposal_ledger(result.ledger.tick_traces),
        )
        summary = result.summary()
        self.assertEqual(summary["reducer_proposal_receipts"], 2)
        self.assertEqual(
            summary["reducer_proposal_measurement_model"],
            f"{REDUCER_PROPOSAL_MODEL_ID}@1.0.0",
        )

    def test_pre_constraint_reducer_proposal_is_distinct_from_committed_delta(self) -> None:
        initial = HumanState(body=BodyState(energy=0.99))
        result = _run(
            (_event("delivery:saturated", energy_delta=0.25),),
            initial_state=initial,
        )
        receipt = result.ledger.reducer_proposals.receipts[0]
        energy = _proposal(receipt, "fast.body.energy")

        self.assertAlmostEqual(energy.requested_delta, 0.25)
        self.assertAlmostEqual(energy.requested_after_unbounded, 1.24)
        self.assertAlmostEqual(energy.committed_delta, 0.01)
        self.assertEqual(energy.committed_after, 1.0)

        sequential = apply_slow_update_traced(
            HumanState(habit=HabitPolicy(impulsivity=1.0)),
            ModelInput(
                event_id="mixed-write",
                kind="internal_rehearsal",
                source_is_external=False,
                soothing=1.0,
            ),
            PhenomenalActivation(distress=0.0, urgency=0.0, ambiguity=0.0),
            PerformanceReceipt(
                receipt_id="performance:mixed",
                attempt_id="attempt:mixed",
                action_kind="accuse",
                agency=1.0,
                tick=0,
            ),
        )
        habit_writes = [
            proposal
            for proposal in sequential.proposals
            if proposal.field == "habit.impulsivity"
        ]
        self.assertEqual(len(habit_writes), 2)
        self.assertEqual(habit_writes[0].requested_after_unbounded, 1.001)
        self.assertEqual(habit_writes[0].committed_after, 1.0)
        self.assertEqual(habit_writes[1].basis_before, 1.0)
        self.assertAlmostEqual(habit_writes[1].committed_after, 0.9995)

    def test_saturated_reducer_proposal_can_exist_without_mental_transition(self) -> None:
        policy = MentalTransitionQualificationPolicy(
            state_fields=("body.energy",),
            minimum_absolute_delta=0.0001,
        )
        result = _run(
            (_event("delivery:fully-saturated", energy_delta=0.25),),
            initial_state=HumanState(body=BodyState(energy=1.0)),
            mental_policy=policy,
        )
        proposal_receipt = result.ledger.reducer_proposals.receipts[0]
        energy = _proposal(proposal_receipt, "fast.body.energy")

        self.assertAlmostEqual(energy.requested_delta, 0.25)
        self.assertEqual(energy.committed_delta, 0.0)
        self.assertFalse(result.ledger.mental_transitions.receipts[0].qualified)
        self.assertEqual(result.ledger.mental_transitions.transitions, ())

    def test_transport_redelivery_does_not_create_reducer_proposal_receipt(self) -> None:
        first = _event(
            "delivery:first",
            occurrence_id="occurrence:source",
            energy_delta=0.25,
        )
        redelivery = _event(
            "delivery:redelivery",
            occurrence_id="occurrence:source",
            available_at=1,
            energy_delta=0.25,
        )
        result = _run((first, first, redelivery))

        self.assertEqual(
            [decision.disposition for decision in result.ledger.ingress_decisions],
            ["accepted", "duplicate", "redundant_delivery"],
        )
        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(len(result.ledger.reducer_proposals.receipts), 1)

    def test_current_reexposure_creates_new_reducer_proposal_with_source_provenance(self) -> None:
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
            energy_delta=-0.10,
        )
        result = _run((source, reexposure))
        ledger = result.ledger.reducer_proposals

        self.assertEqual(len(ledger.receipts), 2)
        receipt = ledger.receipts[1]
        self.assertEqual(receipt.cause_occurrence_id, "occurrence:reexposure")
        self.assertEqual(
            receipt.reexposure_of_occurrence_id,
            "occurrence:source",
        )
        self.assertEqual(receipt.cause_occurred_at, SimTime(5))
        self.assertAlmostEqual(
            _proposal(receipt, "fast.body.energy").requested_delta,
            -0.10,
        )

    def test_future_events_cannot_rewrite_reducer_proposal_prefix(self) -> None:
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
                energy_delta=-0.10,
            ),
        )
        future = _event(
            "delivery:future",
            occurrence_id="occurrence:future",
            occurred_at=10,
            available_at=10,
            energy_delta=0.25,
        )
        prefix = _run(prefix_events).ledger.reducer_proposals
        extended = _run((*prefix_events, future)).ledger.reducer_proposals

        self.assertEqual(extended.receipts[: len(prefix.receipts)], prefix.receipts)
        self.assertEqual(len(extended.receipts), len(prefix.receipts) + 1)

    def test_reducer_proposal_instrumentation_preserves_committed_runtime_semantics(self) -> None:
        event = _event("delivery:no-feedback", energy_delta=0.25, soothing=1.0)
        model_input = encode_model_input(event)
        initial = HumanState(body=BodyState(energy=0.99))
        access_pressure = legacy_v01_access_pressure_bridge(0.25)

        fast_state = apply_fast_update(
            initial,
            model_input,
            processed_tick=0,
            access_pressure=access_pressure,
        )
        fast_traced = apply_fast_update_traced(
            initial,
            model_input,
            processed_tick=0,
            access_pressure=access_pressure,
        )
        self.assertEqual(fast_traced.state_after, fast_state)
        phenomenal = phenomenal_activation(fast_state, model_input)
        self.assertEqual(
            apply_slow_update(fast_state, model_input, phenomenal, None),
            apply_slow_update_traced(
                fast_state,
                model_input,
                phenomenal,
                None,
            ).state_after,
        )

        result = _run((event,), initial_state=initial)
        projection_before = (
            result.final_state,
            tuple(result.ledger.evidence_links),
            tuple(result.ledger.action_occurrences),
            tuple(result.ledger.tick_traces),
        )
        rebuilt = build_reducer_proposal_ledger(result.ledger.tick_traces)
        projection_after = (
            result.final_state,
            tuple(result.ledger.evidence_links),
            tuple(result.ledger.action_occurrences),
            tuple(result.ledger.tick_traces),
        )
        self.assertEqual(rebuilt, result.ledger.reducer_proposals)
        self.assertEqual(projection_after, projection_before)
        self.assertNotIn("reducer_proposals", {item.name for item in fields(HumanState)})

    def test_reducer_proposal_records_require_immutable_typed_components(self) -> None:
        receipt = _run(
            (_event("delivery:immutable", energy_delta=0.25),)
        ).ledger.reducer_proposals.receipts[0]
        proposal = _proposal(receipt, "fast.body.energy")

        with self.assertRaisesRegex(TypeError, "immutable tuple"):
            replace(proposal, drivers=list(proposal.drivers))  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "clamped requested target"):
            replace(proposal, committed_after=0.5)
        with self.assertRaisesRegex(ValueError, "sum to requested_delta"):
            replace(
                proposal,
                drivers=(
                    ReducerDriverContribution(
                        channel=ReducerDriverChannel.ENCODED_INPUT,
                        label="forged",
                        contribution=0.0,
                    ),
                ),
            )
        forged_operator = replace(proposal, operator_id="forged.operator")
        with self.assertRaisesRegex(ValueError, "mandatory reducer proposal schema"):
            replace(
                receipt,
                proposals=(forged_operator, *receipt.proposals[1:]),
            )
        forged_driver = replace(
            proposal,
            drivers=(
                ReducerDriverContribution(
                    channel=ReducerDriverChannel.ACTION_CONSEQUENCE,
                    label="forged.action",
                    contribution=proposal.requested_delta,
                ),
            ),
        )
        with self.assertRaisesRegex(ValueError, "driver is not allowed"):
            replace(
                receipt,
                proposals=(forged_driver, *receipt.proposals[1:]),
            )
        first, second, *remaining = receipt.proposals
        reordered = (
            replace(second, write_sequence=1),
            replace(first, write_sequence=2),
            *remaining,
        )
        with self.assertRaisesRegex(ValueError, "mandatory reducer proposal schema"):
            replace(receipt, proposals=reordered)
        saturated = _run(
            (_event("delivery:mandatory-saturation", energy_delta=0.25),),
            initial_state=HumanState(body=BodyState(energy=1.0)),
        ).ledger.reducer_proposals.receipts[0]
        without_saturated_write = tuple(
            replace(item, write_sequence=index)
            for index, item in enumerate(saturated.proposals[1:], start=1)
        )
        with self.assertRaisesRegex(ValueError, "mandatory reducer proposal schema"):
            replace(saturated, proposals=without_saturated_write)
        with self.assertRaisesRegex(TypeError, "immutable tuple"):
            replace(receipt, proposals=list(receipt.proposals))  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "proposal_digest"):
            replace(receipt, proposal_digest="0" * 64)
        with self.assertRaisesRegex(ValueError, "state_before_digest"):
            replace(receipt, state_before_digest="0" * 64)
        with self.assertRaisesRegex(ValueError, "fixed ordered scope"):
            replace(
                receipt,
                state_before_projection=receipt.state_before_projection[:-1],
                state_after_projection=receipt.state_after_projection[:-1],
            )
        last_energy = next(
            item
            for item in reversed(receipt.proposals)
            if item.field == "body.energy"
        )
        phantom_action_write = ReducerFieldProposal(
            write_sequence=len(receipt.proposals) + 1,
            stage_id="slow-descriptive-update@0.1.0",
            operator_id="slow.action.body.energy",
            field="body.energy",
            basis_before=last_energy.committed_after,
            requested_after_unbounded=last_energy.committed_after,
            committed_after=last_energy.committed_after,
            unit="normalized_simulation_unit",
            constraint_id="clamp01",
            drivers=(),
        )
        with self.assertRaisesRegex(ValueError, "do not match trace context"):
            replace(
                receipt,
                proposals=(*receipt.proposals, phantom_action_write),
            )

        scenario = load_scenario("dynamics/scenarios/delayed_reply.json")
        action_receipt = next(
            item
            for item in scenario.run(DynamicsEngine()).ledger.reducer_proposals.receipts
            if item.context.performance_action_kind == "ask"
        )
        action_proposal = _proposal(action_receipt, "slow.action.body.energy")
        relabeled_driver = replace(
            action_proposal.drivers[0],
            label="performance.withdraw.energy_cost",
        )
        relabeled_proposal = replace(
            action_proposal,
            drivers=(relabeled_driver,),
        )
        with self.assertRaisesRegex(ValueError, "drivers do not match trace context"):
            replace(
                action_receipt,
                proposals=tuple(
                    relabeled_proposal if item is action_proposal else item
                    for item in action_receipt.proposals
                ),
            )
        with self.assertRaisesRegex(ValueError, "context_digest"):
            replace(action_receipt, context_digest="0" * 64)
        with self.assertRaisesRegex(TypeError, "immutable tuple"):
            ReducerProposalLedger(
                policy=_run(()).ledger.reducer_proposals.policy,
                receipts=[receipt],  # type: ignore[arg-type]
            )

    def test_reducer_proposal_ledger_rejects_inconsistent_lineage_and_content_identity(self) -> None:
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
        )
        ledger = _run((source, reexposure)).ledger.reducer_proposals
        source_receipt, reexposure_receipt = ledger.receipts

        with self.assertRaisesRegex(ValueError, "canonical proposal identity"):
            replace(
                reexposure_receipt,
                reexposure_of_occurrence_id="occurrence:missing",
            )
        with self.assertRaisesRegex(ValueError, "canonical proposal identity"):
            replace(reexposure_receipt, cause_occurred_at=SimTime(3))
        with self.assertRaisesRegex(ValueError, "canonical proposal identity"):
            replace(source_receipt, cause_delivery_id="delivery:forged")

        other_receipt = _run(
            (
                _event(
                    "delivery:other-state",
                    occurrence_id="occurrence:other-state",
                    occurred_at=5,
                    available_at=5,
                ),
            ),
            initial_state=HumanState(body=BodyState(energy=0.2)),
        ).ledger.reducer_proposals.receipts[0]
        chained_id = _receipt_id(
            other_receipt.measurement_model_id,
            other_receipt.measurement_model_version,
            other_receipt.policy_digest,
            2,
            other_receipt.cause_occurrence_id,
            other_receipt.cause_delivery_id,
            other_receipt.reexposure_of_occurrence_id,
            other_receipt.cause_occurred_at,
            other_receipt.became_available_at,
            other_receipt.processed_at,
            other_receipt.context_digest,
            other_receipt.proposal_digest,
            other_receipt.state_before_digest,
            other_receipt.state_after_digest,
        )
        discontinuous = replace(
            other_receipt,
            receipt_id=chained_id,
            processing_sequence=2,
        )
        with self.assertRaisesRegex(ValueError, "state chain is discontinuous"):
            ReducerProposalLedger(
                policy=ledger.policy,
                receipts=(source_receipt, discontinuous),
            )
        with self.assertRaisesRegex(ValueError, "complete processing order"):
            ReducerProposalLedger(
                policy=ledger.policy,
                receipts=(reexposure_receipt,),
            )

    def test_reducer_proposal_capture_preserves_invalid_initial_audit_path(self) -> None:
        invalid = HumanState(
            body=BodyState(energy=1.2, arousal=0.2, action_capacity=0.5)
        )
        result = _run((_event("delivery:invalid-initial"),), initial_state=invalid)

        self.assertEqual(result.final_state.body.energy, 1.0)
        self.assertIn(
            "initial:NUMERIC_BOUND:body.energy:1.2",
            result.ledger.invariant_errors,
        )
        self.assertEqual(len(result.ledger.reducer_proposals.receipts), 1)
        energy = _proposal(
            result.ledger.reducer_proposals.receipts[0],
            "fast.body.energy",
        )
        self.assertEqual(energy.basis_before, 1.2)
        self.assertEqual(energy.committed_after, 1.0)


if __name__ == "__main__":
    unittest.main()
