from __future__ import annotations

from dataclasses import fields, replace
import math
import unittest

from dynamics.contract import ProvenanceKind
from dynamics.engine import DynamicsEngine, EngineConfig
from dynamics.mental_transitions import MentalTransitionQualificationPolicy
from dynamics.models import (
    AffectivePrior,
    AssociativeState,
    BodyState,
    HabitPolicy,
    HumanState,
    RelationalProfile,
)
from dynamics.protocol import ScenarioEvent
from dynamics.reducer_envelope_comparisons import (
    REDUCER_ENVELOPE_COMPARISON_MODEL_ID,
    ReducerProposalEnvelopeBand,
    ReducerProposalEnvelopeLedger,
    ReducerProposalEnvelopePolicy,
    _comparison_digest,
    _receipt_id,
    build_reducer_proposal_envelope_ledger,
    validate_reducer_proposal_envelope_ledger,
)
from dynamics.temporal import EventTemporalEnvelope, SimTime


def _event(
    delivery_id: str,
    *,
    occurrence_id: str | None = None,
    occurred_at: int = 0,
    available_at: int = 0,
    reexposure_of_occurrence_id: str | None = None,
    energy_delta: float = 0.0,
    soothing: float = 0.0,
) -> ScenarioEvent:
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
            occurrence_id=occurrence_id or f"occurrence:{delivery_id}",
            delivery_id=delivery_id,
            occurred_at=SimTime(occurred_at),
            available_at=SimTime(available_at),
            reexposure_of_occurrence_id=reexposure_of_occurrence_id,
        ),
    )


def _policy_with_band(
    field: str,
    lower: float,
    upper: float,
    *,
    policy_id: str,
) -> ReducerProposalEnvelopePolicy:
    base = ReducerProposalEnvelopePolicy()
    bands = tuple(
        replace(band, lower_delta=lower, upper_delta=upper)
        if band.field == field
        else band
        for band in base.field_bands
    )
    return replace(base, policy_id=policy_id, field_bands=bands)


def _run(
    events: tuple[ScenarioEvent, ...],
    *,
    initial_state: HumanState | None = None,
    envelope_policy: ReducerProposalEnvelopePolicy | None = None,
    mental_policy: MentalTransitionQualificationPolicy | None = None,
):
    return DynamicsEngine(
        EngineConfig(
            drain_ticks=0,
            mental_transition_policy=(
                mental_policy or MentalTransitionQualificationPolicy()
            ),
            reducer_proposal_envelope_policy=envelope_policy,
        )
    ).run(initial_state or HumanState(), events)


def _energy_component(result):
    ledger = result.ledger.reducer_proposal_envelopes
    assert ledger is not None
    return next(
        item
        for item in ledger.receipts[0].comparisons
        if item.source_operator_id == "fast.body.energy"
    )


def _rebind_receipt(receipt, comparisons):
    digest = _comparison_digest(comparisons)
    receipt_id = _receipt_id(
        receipt.measurement_model_id,
        receipt.measurement_model_version,
        receipt.policy_digest,
        receipt.source_proposal_policy_digest,
        receipt.source_proposal_receipt_id,
        receipt.source_proposal_digest,
        receipt.source_state_before_digest,
        receipt.processing_sequence,
        receipt.cause_occurrence_id,
        receipt.cause_delivery_id,
        receipt.reexposure_of_occurrence_id,
        receipt.cause_occurred_at,
        receipt.became_available_at,
        receipt.processed_at,
        receipt.snapshot.snapshot_id,
        digest,
    )
    return replace(
        receipt,
        receipt_id=receipt_id,
        comparisons=comparisons,
        comparison_digest=digest,
    )


class ReducerProposalEnvelopeComparisonTests(unittest.TestCase):
    def test_envelope_projection_is_explicit_opt_in(self) -> None:
        event = _event("delivery:opt-in", energy_delta=0.20)
        disabled = _run((event,))
        enabled = _run(
            (event,),
            envelope_policy=ReducerProposalEnvelopePolicy(),
        )

        self.assertIsNone(disabled.ledger.reducer_proposal_envelopes)
        self.assertFalse(disabled.summary()["reducer_proposal_envelope_enabled"])
        self.assertIsNotNone(enabled.ledger.reducer_proposal_envelopes)
        self.assertEqual(disabled.final_state, enabled.final_state)
        self.assertEqual(disabled.ledger.tick_traces, enabled.ledger.tick_traces)
        self.assertEqual(disabled.ledger.evidence_links, enabled.ledger.evidence_links)
        self.assertEqual(
            disabled.ledger.action_occurrences,
            enabled.ledger.action_occurrences,
        )
        self.assertEqual(
            disabled.ledger.mental_transitions,
            enabled.ledger.mental_transitions,
        )
        self.assertEqual(
            disabled.ledger.reducer_proposals,
            enabled.ledger.reducer_proposals,
        )
        self.assertEqual(
            disabled.ledger.invariant_errors,
            enabled.ledger.invariant_errors,
        )
        self.assertEqual(
            enabled.summary()["reducer_proposal_envelope_measurement_model"],
            f"{REDUCER_ENVELOPE_COMPARISON_MODEL_ID}@1.0.0",
        )

    def test_same_proposal_under_different_envelopes_yields_different_proxy_excess(self) -> None:
        source = _run(
            (_event("delivery:source", energy_delta=0.25),)
        ).ledger.reducer_proposals
        narrow = _policy_with_band(
            "body.energy", -0.20, 0.08, policy_id="narrow-energy"
        )
        wide = _policy_with_band(
            "body.energy", -0.20, 0.30, policy_id="wide-energy"
        )
        narrow_ledger = build_reducer_proposal_envelope_ledger(source, narrow)
        wide_ledger = build_reducer_proposal_envelope_ledger(source, wide)
        narrow_energy = next(
            item
            for item in narrow_ledger.receipts[0].comparisons
            if item.source_operator_id == "fast.body.energy"
        )
        wide_energy = next(
            item
            for item in wide_ledger.receipts[0].comparisons
            if item.source_operator_id == "fast.body.energy"
        )

        self.assertEqual(
            narrow_ledger.receipts[0].source_proposal_receipt_id,
            wide_ledger.receipts[0].source_proposal_receipt_id,
        )
        self.assertAlmostEqual(narrow_energy.signed_proxy_excess, 0.17)
        self.assertEqual(wide_energy.signed_proxy_excess, 0.0)
        self.assertNotEqual(narrow.policy_digest, wide.policy_digest)
        self.assertNotEqual(
            narrow_ledger.receipts[0].receipt_id,
            wide_ledger.receipts[0].receipt_id,
        )

    def test_same_committed_delta_can_hide_different_proposal_excess(self) -> None:
        policy = _policy_with_band(
            "body.energy", -0.20, 0.02, policy_id="saturation-probe"
        )
        initial = HumanState(body=BodyState(energy=1.0))
        small = _run(
            (_event("delivery:small", energy_delta=0.05),),
            initial_state=initial,
            envelope_policy=policy,
        )
        large = _run(
            (_event("delivery:large", energy_delta=0.25),),
            initial_state=initial,
            envelope_policy=policy,
        )
        small_energy = _energy_component(small)
        large_energy = _energy_component(large)

        self.assertEqual(small_energy.committed_delta, 0.0)
        self.assertEqual(large_energy.committed_delta, 0.0)
        self.assertAlmostEqual(small_energy.signed_proxy_excess, 0.03)
        self.assertAlmostEqual(large_energy.signed_proxy_excess, 0.23)

    def test_equal_transition_counts_can_have_different_proxy_excess_profiles(self) -> None:
        policy = _policy_with_band(
            "body.energy", -0.20, 0.05, policy_id="count-load-probe"
        )
        q_policy = MentalTransitionQualificationPolicy(
            state_fields=("body.energy",),
            minimum_absolute_delta=0.001,
        )
        initial = HumanState(body=BodyState(energy=0.50))
        small = _run(
            (_event("delivery:q-small", energy_delta=0.10),),
            initial_state=initial,
            envelope_policy=policy,
            mental_policy=q_policy,
        )
        large = _run(
            (_event("delivery:q-large", energy_delta=0.25),),
            initial_state=initial,
            envelope_policy=policy,
            mental_policy=q_policy,
        )

        self.assertEqual(len(small.ledger.mental_transitions.transitions), 1)
        self.assertEqual(len(large.ledger.mental_transitions.transitions), 1)
        self.assertAlmostEqual(_energy_component(small).signed_proxy_excess, 0.05)
        self.assertAlmostEqual(_energy_component(large).signed_proxy_excess, 0.20)

    def test_asymmetric_envelope_preserves_direction(self) -> None:
        policy = _policy_with_band(
            "body.energy", -0.20, 0.08, policy_id="directional-probe"
        )
        positive = _run(
            (_event("delivery:positive", energy_delta=0.15),),
            initial_state=HumanState(body=BodyState(energy=0.50)),
            envelope_policy=policy,
        )
        negative_inside = _run(
            (_event("delivery:negative-inside", energy_delta=-0.15),),
            initial_state=HumanState(body=BodyState(energy=0.50)),
            envelope_policy=policy,
        )
        negative_outside = _run(
            (_event("delivery:negative-outside", energy_delta=-0.25),),
            initial_state=HumanState(body=BodyState(energy=0.50)),
            envelope_policy=policy,
        )

        self.assertAlmostEqual(_energy_component(positive).signed_proxy_excess, 0.07)
        self.assertEqual(
            _energy_component(negative_inside).signed_proxy_excess,
            0.0,
        )
        self.assertAlmostEqual(
            _energy_component(negative_outside).signed_proxy_excess,
            -0.05,
        )

    def test_storage_constraint_gap_is_not_envelope_excess(self) -> None:
        policy = _policy_with_band(
            "body.energy", -0.20, 0.30, policy_id="storage-dissociation"
        )
        result = _run(
            (_event("delivery:storage", energy_delta=0.25),),
            initial_state=HumanState(body=BodyState(energy=1.0)),
            envelope_policy=policy,
        )
        energy = _energy_component(result)

        self.assertEqual(energy.committed_delta, 0.0)
        self.assertAlmostEqual(
            energy.requested_delta - energy.committed_delta,
            0.25,
        )
        self.assertEqual(energy.signed_proxy_excess, 0.0)
        self.assertEqual(energy.source_constraint_id, "clamp01")
        self.assertEqual(energy.upper_delta, 0.30)

    def test_snapshot_is_bound_to_pre_update_state_projection_and_source_receipt(self) -> None:
        result = _run(
            (_event("delivery:snapshot", energy_delta=0.20),),
            envelope_policy=ReducerProposalEnvelopePolicy(),
        )
        source = result.ledger.reducer_proposals.receipts[0]
        derived_ledger = result.ledger.reducer_proposal_envelopes
        assert derived_ledger is not None
        derived = derived_ledger.receipts[0]

        self.assertEqual(derived.snapshot.source_proposal_receipt_id, source.receipt_id)
        self.assertEqual(
            derived.snapshot.source_state_before_digest,
            source.state_before_digest,
        )
        self.assertFalse(hasattr(derived.snapshot, "source_state_after_digest"))
        self.assertEqual(derived.snapshot.evaluated_at, source.processed_at)

    def test_repeated_field_writes_remain_separate_ordered_comparisons(self) -> None:
        policy = _policy_with_band(
            "habit.impulsivity",
            -0.00025,
            0.0005,
            policy_id="repeated-write-probe",
        )
        initial = HumanState(
            body=BodyState(energy=1.0, arousal=0.9, action_capacity=1.0),
            associative=AssociativeState(
                rejection_access=0.4,
                ambiguity_sensitivity=0.5,
            ),
            affective=AffectivePrior(residual_distress=1.0, update_rate=0.25),
            habit=HabitPolicy(impulsivity=1.0, withdrawal_bias=0.0),
            relationship=RelationalProfile(
                stake=0.8,
                trust=0.0,
                boundary_strain=0.8,
            ),
        )
        event = ScenarioEvent(
            event_id="delivery:decision",
            tick=0,
            kind="decision_window",
            external=False,
            source_id="self",
            provenance_kind=ProvenanceKind.INFERENCE,
            independence_key="self",
            time_pressure=1.0,
            soothing=1.0,
            action_window=True,
        )
        result = _run(
            (event,),
            initial_state=initial,
            envelope_policy=policy,
        )
        derived_ledger = result.ledger.reducer_proposal_envelopes
        assert derived_ledger is not None
        components = [
            item
            for item in derived_ledger.receipts[0].comparisons
            if item.field == "habit.impulsivity"
        ]

        self.assertEqual(result.ledger.performance_receipts[0].action_kind, "accuse")
        self.assertEqual(len(components), 2)
        self.assertEqual(
            [item.source_operator_id for item in components],
            [
                "slow.action.habit.impulsivity",
                "slow.soothing.habit.impulsivity",
            ],
        )
        self.assertAlmostEqual(components[0].signed_proxy_excess, 0.0005)
        self.assertAlmostEqual(components[1].signed_proxy_excess, -0.00025)

    def test_transport_redelivery_does_not_create_envelope_receipt(self) -> None:
        first = _event(
            "delivery:first",
            occurrence_id="occurrence:source",
            energy_delta=0.20,
        )
        redelivery = _event(
            "delivery:redelivery",
            occurrence_id="occurrence:source",
            available_at=1,
            energy_delta=0.20,
        )
        result = _run(
            (first, first, redelivery),
            envelope_policy=ReducerProposalEnvelopePolicy(),
        )
        derived = result.ledger.reducer_proposal_envelopes
        assert derived is not None

        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(len(result.ledger.reducer_proposals.receipts), 1)
        self.assertEqual(len(derived.receipts), 1)

    def test_reexposure_gets_new_comparison_with_source_provenance(self) -> None:
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
        result = _run(
            (source, reexposure),
            envelope_policy=ReducerProposalEnvelopePolicy(),
        )
        derived = result.ledger.reducer_proposal_envelopes
        assert derived is not None

        self.assertEqual(len(derived.receipts), 2)
        self.assertEqual(
            derived.receipts[1].reexposure_of_occurrence_id,
            "occurrence:source",
        )
        self.assertEqual(
            derived.receipts[1].source_proposal_receipt_id,
            result.ledger.reducer_proposals.receipts[1].receipt_id,
        )

    def test_future_events_cannot_rewrite_comparison_prefix(self) -> None:
        policy = ReducerProposalEnvelopePolicy()
        prefix_events = (
            _event("delivery:prefix-1", occurrence_id="occurrence:prefix-1"),
            _event(
                "delivery:prefix-2",
                occurrence_id="occurrence:prefix-2",
                occurred_at=1,
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
        prefix = _run(
            prefix_events,
            envelope_policy=policy,
        ).ledger.reducer_proposal_envelopes
        extended = _run(
            (*prefix_events, future),
            envelope_policy=policy,
        ).ledger.reducer_proposal_envelopes
        assert prefix is not None and extended is not None

        self.assertEqual(extended.receipts[: len(prefix.receipts)], prefix.receipts)

    def test_policy_variation_has_no_runtime_feedback(self) -> None:
        event = _event("delivery:no-feedback", energy_delta=0.25, soothing=1.0)
        narrow = _policy_with_band(
            "body.energy", -0.10, 0.02, policy_id="no-feedback-narrow"
        )
        wide = _policy_with_band(
            "body.energy", -0.30, 0.30, policy_id="no-feedback-wide"
        )
        first = _run((event,), envelope_policy=narrow)
        second = _run((event,), envelope_policy=wide)

        self.assertEqual(first.final_state, second.final_state)
        self.assertEqual(first.ledger.tick_traces, second.ledger.tick_traces)
        self.assertEqual(first.ledger.evidence_links, second.ledger.evidence_links)
        self.assertEqual(first.ledger.action_occurrences, second.ledger.action_occurrences)
        self.assertEqual(
            first.ledger.mental_transitions,
            second.ledger.mental_transitions,
        )
        self.assertEqual(first.ledger.reducer_proposals, second.ledger.reducer_proposals)
        self.assertNotEqual(
            first.ledger.reducer_proposal_envelopes,
            second.ledger.reducer_proposal_envelopes,
        )
        self.assertNotIn(
            "reducer_proposal_envelopes",
            {item.name for item in fields(HumanState)},
        )

    def test_policy_digest_binds_exact_typed_bands(self) -> None:
        policy = ReducerProposalEnvelopePolicy()
        changed = _policy_with_band(
            "body.energy", -0.09, 0.05, policy_id="changed-band"
        )

        self.assertNotEqual(policy.policy_digest, changed.policy_digest)
        with self.assertRaisesRegex(TypeError, "immutable tuple"):
            replace(policy, field_bands=list(policy.field_bands))  # type: ignore[arg-type]
        mutable_policy_id = ["mutable-policy-id"]
        with self.assertRaisesRegex(TypeError, "immutable string"):
            replace(policy, policy_id=mutable_policy_id)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "exact reducer proposal scope"):
            replace(policy, field_bands=policy.field_bands[:-1])
        with self.assertRaisesRegex(ValueError, "exact reducer proposal scope"):
            replace(
                policy,
                field_bands=(policy.field_bands[1], policy.field_bands[0], *policy.field_bands[2:]),
            )
        with self.assertRaisesRegex(ValueError, "contain zero"):
            replace(policy.field_bands[0], lower_delta=0.01)
        with self.assertRaisesRegex(ValueError, "finite"):
            replace(policy.field_bands[0], upper_delta=math.inf)
        with self.assertRaisesRegex(ValueError, "measurement identity is fixed"):
            replace(policy, measurement_model_id="morphic-load")

    def test_component_arithmetic_and_source_mapping_tampering_is_rejected(self) -> None:
        result = _run(
            (_event("delivery:tamper", energy_delta=0.25),),
            envelope_policy=ReducerProposalEnvelopePolicy(),
        )
        source = result.ledger.reducer_proposals
        derived = result.ledger.reducer_proposal_envelopes
        assert derived is not None
        receipt = derived.receipts[0]
        first = receipt.comparisons[0]

        with self.assertRaisesRegex(ValueError, "band_limited_delta"):
            replace(first, band_limited_delta=0.0)
        with self.assertRaisesRegex(ValueError, "signed_proxy_excess"):
            replace(first, signed_proxy_excess=0.0)
        with self.assertRaisesRegex(ValueError, "non-zero direction"):
            replace(
                first,
                lower_delta=0.0,
                upper_delta=0.0,
                band_limited_delta=0.0,
                signed_proxy_excess=first.requested_delta,
            )
        with self.assertRaisesRegex(ValueError, "comparison_digest"):
            replace(receipt, comparison_digest="0" * 64)
        with self.assertRaisesRegex(TypeError, "immutable string"):
            replace(
                receipt,
                source_proposal_digest=["a"] * 64,  # type: ignore[arg-type]
            )
        with self.assertRaisesRegex(ValueError, "snapshot_id"):
            replace(receipt.snapshot, snapshot_id="forged")

        forged_first = replace(first, source_operator_id="forged.operator")
        forged_receipt = _rebind_receipt(
            receipt,
            (forged_first, *receipt.comparisons[1:]),
        )
        forged_ledger = ReducerProposalEnvelopeLedger(
            policy=derived.policy,
            source_proposal_policy_digest=derived.source_proposal_policy_digest,
            receipts=(forged_receipt,),
        )
        with self.assertRaisesRegex(ValueError, "does not match source proposal"):
            validate_reducer_proposal_envelope_ledger(source, forged_ledger)

    def test_comparison_ledger_requires_complete_ordered_source_mapping(self) -> None:
        result = _run(
            (_event("delivery:complete", energy_delta=0.25),),
            envelope_policy=ReducerProposalEnvelopePolicy(),
        )
        source = result.ledger.reducer_proposals
        derived = result.ledger.reducer_proposal_envelopes
        assert derived is not None
        receipt = derived.receipts[0]
        shortened = tuple(
            replace(item, write_sequence=index)
            for index, item in enumerate(receipt.comparisons[1:], start=1)
        )
        shortened_receipt = _rebind_receipt(receipt, shortened)
        shortened_ledger = ReducerProposalEnvelopeLedger(
            policy=derived.policy,
            source_proposal_policy_digest=derived.source_proposal_policy_digest,
            receipts=(shortened_receipt,),
        )

        with self.assertRaisesRegex(ValueError, "map every ordered proposal"):
            validate_reducer_proposal_envelope_ledger(source, shortened_ledger)
        with self.assertRaisesRegex(ValueError, "map every source proposal receipt"):
            validate_reducer_proposal_envelope_ledger(
                source,
                ReducerProposalEnvelopeLedger(
                    policy=derived.policy,
                    source_proposal_policy_digest=(
                        derived.source_proposal_policy_digest
                    ),
                    receipts=(),
                ),
            )

    def test_invalid_initial_state_keeps_existing_audit_path_when_enabled(self) -> None:
        result = _run(
            (_event("delivery:invalid-initial"),),
            initial_state=HumanState(body=BodyState(energy=1.2)),
            envelope_policy=ReducerProposalEnvelopePolicy(),
        )
        derived = result.ledger.reducer_proposal_envelopes

        self.assertIn(
            "initial:NUMERIC_BOUND:body.energy:1.2",
            result.ledger.invariant_errors,
        )
        self.assertIsNotNone(derived)
        self.assertEqual(_energy_component(result).basis_before, 1.2)


if __name__ == "__main__":
    unittest.main()
