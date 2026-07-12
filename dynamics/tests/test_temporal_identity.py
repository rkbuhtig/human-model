from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from dynamics.contract import ProvenanceKind
from dynamics.engine import DynamicsEngine, EngineConfig
from dynamics.models import HumanState
from dynamics.protocol import ClaimSignal, IngressQueue, ScenarioEvent
from dynamics.scenario import load_scenario
from dynamics.temporal import EventTemporalEnvelope, ProcessingStamp, SimTime


def _envelope(
    occurrence_id: str,
    delivery_id: str,
    *,
    occurred_at: int = 0,
    available_at: int = 0,
    delivery_sequence: int | None = None,
    reexposure_of_occurrence_id: str | None = None,
) -> EventTemporalEnvelope:
    return EventTemporalEnvelope(
        occurrence_id=occurrence_id,
        delivery_id=delivery_id,
        occurred_at=SimTime(occurred_at),
        available_at=SimTime(available_at),
        delivery_sequence=delivery_sequence,
        reexposure_of_occurrence_id=reexposure_of_occurrence_id,
    )


def _internal_event(
    delivery_id: str,
    *,
    occurrence_id: str | None = None,
    occurred_at: int = 0,
    available_at: int = 0,
    delivery_sequence: int | None = None,
    reexposure_of_occurrence_id: str | None = None,
    ambiguity: float = 0.0,
    time_pressure: float = 0.0,
    memory_interference: float = 0.0,
    arousal_delta: float = 0.0,
    ingress_priority: float = 0.5,
) -> ScenarioEvent:
    return ScenarioEvent(
        event_id=delivery_id,
        tick=available_at,
        kind="internal_rehearsal",
        external=False,
        source_id="internal",
        provenance_kind=ProvenanceKind.IMAGINATION,
        independence_key="internal",
        ambiguity=ambiguity,
        time_pressure=time_pressure,
        memory_interference=memory_interference,
        arousal_delta=arousal_delta,
        ingress_priority=ingress_priority,
        temporal=_envelope(
            occurrence_id or f"occurrence:{delivery_id}",
            delivery_id,
            occurred_at=occurred_at,
            available_at=available_at,
            delivery_sequence=delivery_sequence,
            reexposure_of_occurrence_id=reexposure_of_occurrence_id,
        ),
    )


def _evidence_event(
    delivery_id: str,
    *,
    occurrence_id: str,
    occurred_at: int = 0,
    available_at: int = 0,
    delivery_sequence: int | None = None,
) -> ScenarioEvent:
    return ScenarioEvent(
        event_id=delivery_id,
        tick=available_at,
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
        temporal=_envelope(
            occurrence_id,
            delivery_id,
            occurred_at=occurred_at,
            available_at=available_at,
            delivery_sequence=delivery_sequence,
        ),
    )


class TemporalValueTests(unittest.TestCase):
    def test_sim_time_and_temporal_ordering_are_strict(self) -> None:
        self.assertEqual(SimTime(0), 0)
        self.assertLess(SimTime(1), SimTime(2))
        for invalid in (True, 1.0, "1"):
            with self.subTest(sim_time=invalid), self.assertRaises(TypeError):
                SimTime(invalid)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            SimTime(-1)

        with self.assertRaises(ValueError):
            _envelope("occ", "delivery", occurred_at=2, available_at=1)
        with self.assertRaises(ValueError):
            _envelope(
                "occ",
                "delivery",
                delivery_sequence=-1,
            )
        with self.assertRaises(TypeError):
            _envelope(
                "occ",
                "delivery",
                delivery_sequence=True,  # type: ignore[arg-type]
            )

        envelope = _envelope("occ", "delivery", available_at=2)
        with self.assertRaises(ValueError):
            ProcessingStamp(
                envelope=envelope,
                processed_at=SimTime(1),
                processing_sequence=1,
            )
        with self.assertRaises(ValueError):
            ProcessingStamp(
                envelope=envelope,
                processed_at=SimTime(2),
                processing_sequence=0,
            )
        with self.assertRaises(TypeError):
            ProcessingStamp(
                envelope=envelope,
                processed_at=SimTime(2),
                processing_sequence=True,  # type: ignore[arg-type]
            )

    def test_legacy_event_id_and_tick_map_to_one_occurrence_and_delivery(self) -> None:
        event = ScenarioEvent(
            event_id="legacy",
            tick=3,
            kind="internal_rehearsal",
            external=False,
            source_id="internal",
            provenance_kind=ProvenanceKind.IMAGINATION,
            independence_key="internal",
        )
        self.assertEqual(event.occurrence_id, "legacy")
        self.assertEqual(event.delivery_id, "legacy")
        self.assertEqual(event.occurred_at, SimTime(3))
        self.assertEqual(event.available_at, SimTime(3))

        duplicate = DynamicsEngine().run(HumanState(), (event, event))
        self.assertEqual(duplicate.ledger.duplicate_event_ids, ["legacy"])
        self.assertEqual(
            [decision.disposition for decision in duplicate.ledger.ingress_decisions],
            ["accepted", "duplicate"],
        )

        collision_event = replace(event, ambiguity=0.7)
        collision = DynamicsEngine().run(
            HumanState(),
            (event, collision_event),
        )
        self.assertEqual(collision.ledger.collision_event_ids, ["legacy"])
        self.assertEqual(collision.ledger.delivery_collision_ids, ["legacy"])

    def test_explicit_temporal_envelope_must_match_legacy_surface(self) -> None:
        envelope = _envelope("occ", "delivery", available_at=4)
        with self.assertRaises(ValueError):
            ScenarioEvent(
                event_id="different-delivery",
                tick=4,
                kind="internal_rehearsal",
                external=False,
                source_id="internal",
                provenance_kind=ProvenanceKind.IMAGINATION,
                independence_key="internal",
                temporal=envelope,
            )
        with self.assertRaises(ValueError):
            ScenarioEvent(
                event_id="delivery",
                tick=3,
                kind="internal_rehearsal",
                external=False,
                source_id="internal",
                provenance_kind=ProvenanceKind.IMAGINATION,
                independence_key="internal",
                temporal=envelope,
            )

    def test_reexposure_protocol_rejects_external_or_grounding_payloads(self) -> None:
        envelope = _envelope(
            "occurrence:reexposure",
            "delivery:reexposure",
            reexposure_of_occurrence_id="occurrence:source",
        )
        with self.assertRaisesRegex(ValueError, "must be internal"):
            ScenarioEvent(
                event_id="delivery:reexposure",
                tick=0,
                kind="internal_rehearsal",
                external=True,
                source_id="internal",
                provenance_kind=ProvenanceKind.IMAGINATION,
                independence_key="internal",
                temporal=envelope,
            )
        with self.assertRaisesRegex(ValueError, "cannot carry evidence"):
            ScenarioEvent(
                event_id="delivery:reexposure",
                tick=0,
                kind="platform_online_indicator",
                external=False,
                source_id="internal",
                provenance_kind=ProvenanceKind.IMAGINATION,
                independence_key="internal",
                supports=(
                    ClaimSignal(
                        "C1_platform_displayed_online",
                        0.8,
                        "observe-platform-online",
                    ),
                ),
                temporal=envelope,
            )
    def test_v02_scenario_loader_preserves_source_fields_and_rejects_engine_stamp(self) -> None:
        event = {
            "delivery_id": "delivery:late",
            "occurrence_id": "occurrence:past",
            "occurred_at": 2,
            "available_at": 7,
            "kind": "internal_rehearsal",
            "external": False,
            "source_id": "internal",
            "provenance_kind": "imagination",
        }
        document = {
            "schema_version": "human-model-scenario/0.2",
            "scenario_id": "temporal-loader",
            "events": [
                event,
                {
                    **event,
                    "delivery_id": "delivery:late-retry",
                    "available_at": 8,
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenario.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            scenario = load_scenario(path)
            loaded = scenario.events[0]
            self.assertEqual(loaded.occurred_at, SimTime(2))
            self.assertEqual(loaded.available_at, SimTime(7))
            result = scenario.run(DynamicsEngine(EngineConfig(drain_ticks=0)))
            self.assertEqual(result.ledger.processed, 1)
            self.assertEqual(
                result.ledger.redundant_delivery_ids,
                ["delivery:late-retry"],
            )
            observation = result.ledger.observations[0]
            self.assertEqual(observation.occurred_at, SimTime(2))
            self.assertEqual(observation.available_at, SimTime(7))
            self.assertEqual(observation.processed_at, SimTime(7))

            for field in ("processed_at", "processing_sequence", "final_sim_time"):
                invalid = json.loads(json.dumps(document))
                invalid["events"][0][field] = 7
                path.write_text(json.dumps(invalid), encoding="utf-8")
                with self.subTest(field=field), self.assertRaisesRegex(
                    ValueError, "engine-owned"
                ):
                    load_scenario(path)

            nested = json.loads(json.dumps(document))
            nested["events"][0]["temporal"] = {}
            path.write_text(json.dumps(nested), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "flat canonical"):
                load_scenario(path)


class TemporalIngressTests(unittest.TestCase):
    def test_sparse_canonical_time_skips_empty_protocol_ticks(self) -> None:
        event = _internal_event(
            "delivery:sparse",
            occurrence_id="occurrence:sparse",
            occurred_at=1_000_000_000,
            available_at=1_000_000_000,
        )
        result = DynamicsEngine(EngineConfig(drain_ticks=0)).run(
            HumanState(),
            (event,),
        )
        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(
            result.ledger.tick_traces[0].observation.processed_at,
            SimTime(1_000_000_000),
        )

    def test_only_a_leased_matching_delivery_can_be_committed(self) -> None:
        queue = IngressQueue(queue_limit=2)
        event = _internal_event(
            "delivery:leased",
            occurrence_id="occurrence:leased",
        )
        with self.assertRaisesRegex(ValueError, "processing lease"):
            queue.mark_processed(event)
        self.assertEqual(queue.accept(event).disposition, "accepted")
        with self.assertRaisesRegex(ValueError, "processing lease"):
            queue.mark_processed(event)

        leased = queue.take(1).processing[0]
        with self.assertRaisesRegex(ValueError, "accepted delivery"):
            queue.mark_processed(replace(leased, ambiguity=0.9))
        queue.mark_processed(leased, processed_at=SimTime(0))

    def test_temporal_ordering_and_engine_owned_processing(self) -> None:
        events = tuple(
            _internal_event(
                f"delivery-{sequence}",
                occurrence_id=f"occurrence-{sequence}",
                delivery_sequence=sequence,
            )
            for sequence in (1, 2, 3)
        )
        result = DynamicsEngine(
            EngineConfig(base_capacity_per_tick=1, drain_ticks=3)
        ).run(HumanState(), reversed(events))

        self.assertEqual(
            [trace.observation.delivery_id for trace in result.ledger.tick_traces],
            ["delivery-1", "delivery-2", "delivery-3"],
        )
        self.assertEqual(
            [trace.observation.processed_at for trace in result.ledger.tick_traces],
            [SimTime(0), SimTime(1), SimTime(2)],
        )
        self.assertEqual(
            [trace.processing_sequence for trace in result.ledger.tick_traces],
            [1, 2, 3],
        )
        for trace in result.ledger.tick_traces:
            stamp = trace.observation.processing_stamp
            self.assertIsNotNone(stamp)
            assert stamp is not None
            self.assertEqual(stamp.processing_sequence, trace.processing_sequence)
            self.assertGreaterEqual(stamp.processed_at, stamp.envelope.available_at)
        self.assertIsInstance(result.ledger.final_sim_time, SimTime)
        self.assertGreaterEqual(
            result.ledger.final_sim_time,
            result.ledger.tick_traces[-1].observation.processed_at,
        )

    def test_transport_redelivery_is_idempotent(self) -> None:
        first = _evidence_event(
            "delivery:first",
            occurrence_id="occurrence:online",
        )
        redelivery = _evidence_event(
            "delivery:retry",
            occurrence_id="occurrence:online",
            available_at=1,
        )
        engine = DynamicsEngine(EngineConfig(drain_ticks=2))
        once = engine.run(HumanState(), (first,))
        twice = engine.run(HumanState(), (first, redelivery))

        self.assertEqual(twice.ledger.processed, 1)
        self.assertEqual(
            twice.ledger.redundant_delivery_ids,
            ["delivery:retry"],
        )
        self.assertEqual(
            [decision.disposition for decision in twice.ledger.ingress_decisions],
            ["accepted", "redundant_delivery"],
        )
        self.assertEqual(twice.final_state, once.final_state)
        self.assertEqual(twice.ledger.observations, once.ledger.observations)
        self.assertEqual(twice.ledger.episode_traces, once.ledger.episode_traces)
        self.assertEqual(twice.ledger.tick_traces, once.ledger.tick_traces)
        self.assertEqual(twice.ledger.evidence_links, once.ledger.evidence_links)
        self.assertTrue(twice.input_accounting_ok)

    def test_same_delivery_with_changed_payload_is_a_delivery_collision(self) -> None:
        first = _internal_event(
            "delivery:one",
            occurrence_id="occurrence:one",
        )
        collision = replace(first, ambiguity=1.0)
        result = DynamicsEngine().run(HumanState(), (first, collision))

        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(result.ledger.delivery_collision_ids, ["delivery:one"])
        self.assertIn(
            "delivery:one:EVENT_ID_PAYLOAD_COLLISION",
            result.ledger.invariant_errors,
        )
        self.assertTrue(result.input_accounting_ok)
        self.assertEqual(
            [decision.disposition for decision in result.ledger.ingress_decisions],
            ["accepted", "delivery_collision"],
        )

    def test_occurrence_payload_collision_is_hard_error(self) -> None:
        first = _internal_event(
            "delivery:one",
            occurrence_id="occurrence:one",
        )
        collision = _internal_event(
            "delivery:two",
            occurrence_id="occurrence:one",
            available_at=1,
            ambiguity=1.0,
        )
        result = DynamicsEngine().run(HumanState(), (first, collision))

        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(result.ledger.occurrence_collision_ids, ["occurrence:one"])
        self.assertIn(
            "occurrence:one:OCCURRENCE_ID_PAYLOAD_COLLISION",
            result.ledger.invariant_errors,
        )
        self.assertTrue(result.input_accounting_ok)
        self.assertEqual(
            [decision.disposition for decision in result.ledger.ingress_decisions],
            ["accepted", "occurrence_collision"],
        )

    def test_dropped_occurrence_can_be_retried_under_a_new_delivery(self) -> None:
        queue = IngressQueue(queue_limit=1, policy="priority")
        events = tuple(
            _internal_event(
                f"delivery:{sequence}",
                occurrence_id=f"occurrence:{sequence}",
                delivery_sequence=sequence,
            )
            for sequence in (1, 2, 3)
        )
        for event in events:
            self.assertEqual(queue.accept(event).disposition, "accepted")

        first_batch = queue.take(1)
        self.assertEqual(
            tuple(event.delivery_id for event in first_batch.processing),
            ("delivery:1",),
        )
        queue.mark_processed(first_batch.processing[0])
        self.assertEqual(first_batch.dropped_event_ids, ("delivery:3",))

        retry = _internal_event(
            "delivery:3-retry",
            occurrence_id="occurrence:3",
            available_at=1,
            delivery_sequence=3,
        )
        self.assertEqual(queue.accept(retry).disposition, "accepted")
        second_batch = queue.take(2)
        self.assertEqual(
            {event.delivery_id for event in second_batch.processing},
            {"delivery:2", "delivery:3-retry"},
        )

    def test_engine_accounts_drop_then_new_delivery_retry_exactly_once(self) -> None:
        original = tuple(
            _internal_event(
                f"delivery:engine-{sequence}",
                occurrence_id=f"occurrence:engine-{sequence}",
                delivery_sequence=sequence,
            )
            for sequence in (1, 2, 3)
        )
        retry = _internal_event(
            "delivery:engine-3-retry",
            occurrence_id="occurrence:engine-3",
            occurred_at=0,
            available_at=1,
            delivery_sequence=3,
        )
        result = DynamicsEngine(
            EngineConfig(
                base_capacity_per_tick=1,
                queue_limit=1,
                drain_ticks=1,
            )
        ).run(HumanState(), (*original, retry))

        self.assertEqual(result.ledger.dropped_event_ids, ["delivery:engine-3"])
        self.assertEqual(result.ledger.processed, 3)
        self.assertEqual(
            [artifact.occurrence_id for artifact in result.ledger.observations],
            [
                "occurrence:engine-1",
                "occurrence:engine-2",
                "occurrence:engine-3",
            ],
        )
        self.assertEqual(result.ledger.raw_received, 4)
        self.assertEqual(result.ledger.unique_received, 4)
        self.assertTrue(result.input_accounting_ok)

    def test_backlog_preserves_occurrence_time(self) -> None:
        blocker = _internal_event(
            "delivery:blocker",
            occurrence_id="occurrence:blocker",
            occurred_at=4,
            available_at=4,
            delivery_sequence=1,
        )
        event = _internal_event(
            "delivery:late",
            occurrence_id="occurrence:past",
            occurred_at=1,
            available_at=4,
            delivery_sequence=2,
        )
        result = DynamicsEngine(
            EngineConfig(base_capacity_per_tick=1, drain_ticks=1)
        ).run(
            HumanState(),
            (blocker, event),
        )
        observation = result.ledger.tick_traces[1].observation

        self.assertEqual(observation.occurred_at, SimTime(1))
        self.assertEqual(observation.source_tick, 1)
        self.assertEqual(observation.available_at, SimTime(4))
        self.assertEqual(observation.processed_at, SimTime(5))
        self.assertEqual(
            observation.processing_stamp.envelope,
            event.temporal,
        )

    def test_current_reexposure_changes_state_not_evidence(self) -> None:
        source = _evidence_event(
            "delivery:source",
            occurrence_id="occurrence:source",
        )
        reexposure = _internal_event(
            "delivery:reexposure",
            occurrence_id="occurrence:reexposure",
            available_at=1,
            reexposure_of_occurrence_id="occurrence:source",
            ambiguity=1.0,
            time_pressure=1.0,
            memory_interference=1.0,
            arousal_delta=0.4,
        )
        engine = DynamicsEngine(EngineConfig(drain_ticks=2))
        source_only = engine.run(HumanState(), (source,))
        replayed = engine.run(HumanState(), (source, reexposure))

        self.assertEqual(replayed.ledger.processed, 2)
        self.assertNotEqual(replayed.final_state, source_only.final_state)
        self.assertEqual(
            replayed.final_state.evidence_assessment,
            source_only.final_state.evidence_assessment,
        )
        self.assertEqual(
            replayed.ledger.evidence_links,
            source_only.ledger.evidence_links,
        )
        self.assertEqual(
            replayed.ledger.tick_traces[-1].observation.occurrence_id,
            "occurrence:reexposure",
        )

    def test_dangling_reexposure_is_rejected(self) -> None:
        dangling = _internal_event(
            "delivery:dangling",
            occurrence_id="occurrence:dangling",
            reexposure_of_occurrence_id="occurrence:missing",
        )
        result = DynamicsEngine().run(HumanState(), (dangling,))

        self.assertEqual(result.ledger.processed, 0)
        self.assertEqual(result.ledger.tick_traces, [])
        self.assertEqual(
            [decision.disposition for decision in result.ledger.ingress_decisions],
            ["dangling_reexposure"],
        )
        self.assertIn(
            "delivery:dangling:DANGLING_REEXPOSURE_SOURCE",
            result.ledger.invariant_errors,
        )
        self.assertTrue(result.input_accounting_ok)

    def test_all_ingress_identity_dispositions_share_one_accounting_partition(self) -> None:
        source = _internal_event(
            "delivery:source",
            occurrence_id="occurrence:source",
        )
        delivery_collision = replace(source, ambiguity=0.3)
        redundant = _internal_event(
            "delivery:redundant",
            occurrence_id="occurrence:source",
            available_at=1,
        )
        occurrence_collision = _internal_event(
            "delivery:occurrence-collision",
            occurrence_id="occurrence:source",
            available_at=2,
            ambiguity=0.7,
        )
        dangling = _internal_event(
            "delivery:dangling-accounting",
            occurrence_id="occurrence:dangling-accounting",
            available_at=3,
            reexposure_of_occurrence_id="occurrence:missing",
        )
        result = DynamicsEngine(EngineConfig(drain_ticks=0)).run(
            HumanState(),
            (
                source,
                source,
                delivery_collision,
                redundant,
                occurrence_collision,
                dangling,
            ),
        )

        self.assertEqual(result.ledger.raw_received, 6)
        self.assertEqual(result.ledger.unique_received, 1)
        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(len(result.ledger.duplicate_event_ids), 1)
        self.assertEqual(len(result.ledger.redundant_delivery_ids), 1)
        self.assertEqual(len(result.ledger.collision_event_ids), 2)
        self.assertEqual(len(result.ledger.dangling_reexposure_ids), 1)
        self.assertTrue(result.input_accounting_ok)
        summary = result.summary()
        self.assertEqual(summary["transport_redeliveries_ignored"], 1)
        self.assertEqual(summary["delivery_id_collisions"], 1)
        self.assertEqual(summary["occurrence_id_collisions"], 1)
        self.assertEqual(summary["dangling_reexposures"], 1)

    def test_reexposure_cannot_be_backdated_before_source_access(self) -> None:
        source = _internal_event(
            "delivery:source-late",
            occurrence_id="occurrence:source-late",
            occurred_at=5,
            available_at=5,
        )
        backdated = _internal_event(
            "delivery:backdated-reexposure",
            occurrence_id="occurrence:backdated-reexposure",
            occurred_at=4,
            available_at=6,
            reexposure_of_occurrence_id="occurrence:source-late",
        )
        result = DynamicsEngine(EngineConfig(drain_ticks=1)).run(
            HumanState(),
            (source, backdated),
        )

        self.assertEqual(result.ledger.processed, 1)
        self.assertEqual(
            result.ledger.invalid_reexposure_time_ids,
            ["delivery:backdated-reexposure"],
        )
        self.assertEqual(
            result.ledger.ingress_decisions[-1].disposition,
            "invalid_reexposure_time",
        )
        self.assertTrue(result.input_accounting_ok)

    def test_delivery_sequence_orders_same_time_and_unsequenced_input_records_debt(self) -> None:
        second = _internal_event(
            "delivery:second",
            occurrence_id="occurrence:second",
            delivery_sequence=2,
        )
        first = _internal_event(
            "delivery:first",
            occurrence_id="occurrence:first",
            delivery_sequence=1,
        )
        ordered = DynamicsEngine(
            EngineConfig(base_capacity_per_tick=10, drain_ticks=0)
        ).run(HumanState(), (second, first))
        self.assertEqual(
            [trace.observation.delivery_id for trace in ordered.ledger.tick_traces],
            ["delivery:first", "delivery:second"],
        )
        self.assertFalse(ordered.ledger.same_timestamp_order_debts)

        unsequenced_b = _internal_event(
            "delivery:unsequenced-b",
            occurrence_id="occurrence:unsequenced-b",
        )
        unsequenced_a = _internal_event(
            "delivery:unsequenced-a",
            occurrence_id="occurrence:unsequenced-a",
        )
        advisory = DynamicsEngine(
            EngineConfig(base_capacity_per_tick=10, drain_ticks=0)
        ).run(HumanState(), (unsequenced_b, unsequenced_a))
        debt_ids = {
            delivery_id
            for debt in advisory.ledger.same_timestamp_order_debts
            for delivery_id in debt
        }
        self.assertEqual(
            debt_ids,
            {"delivery:unsequenced-a", "delivery:unsequenced-b"},
        )
        self.assertEqual(advisory.ledger.invariant_errors, [])

        duplicate_sequence = DynamicsEngine(
            EngineConfig(base_capacity_per_tick=10, drain_ticks=0)
        ).run(
            HumanState(),
            (
                _internal_event(
                    "delivery:sequence-a",
                    occurrence_id="occurrence:sequence-a",
                    delivery_sequence=1,
                ),
                _internal_event(
                    "delivery:sequence-b",
                    occurrence_id="occurrence:sequence-b",
                    delivery_sequence=1,
                ),
            ),
        )
        self.assertTrue(duplicate_sequence.ledger.same_timestamp_order_debts)
        self.assertEqual(duplicate_sequence.ledger.invariant_errors, [])

        fifo_priority_difference = DynamicsEngine(
            EngineConfig(
                base_capacity_per_tick=10,
                drain_ticks=0,
                ingress_policy="fifo",
            )
        ).run(
            HumanState(),
            (
                _internal_event(
                    "delivery:fifo-low",
                    occurrence_id="occurrence:fifo-low",
                    ingress_priority=0.1,
                ),
                _internal_event(
                    "delivery:fifo-high",
                    occurrence_id="occurrence:fifo-high",
                    ingress_priority=0.9,
                ),
            ),
        )
        self.assertTrue(
            fifo_priority_difference.ledger.same_timestamp_order_debts
        )


if __name__ == "__main__":
    unittest.main()
