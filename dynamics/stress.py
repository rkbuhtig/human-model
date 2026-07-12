"""Semantic stress generation and computational soak measurements."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import random
import time
import tracemalloc

from .contract import ProvenanceKind
from .engine import DynamicsEngine, EngineConfig, SimulationResult
from .interfaces import clamp01
from .models import (
    AccessState,
    AffectivePrior,
    AssociativeState,
    BodyState,
    HabitPolicy,
    HumanState,
    NarrativeState,
    RelationalProfile,
)
from .protocol import ClaimSignal, ScenarioEvent


@dataclass(frozen=True, slots=True)
class LoadVector:
    input_rate: float
    candidate_fanout: float
    ambiguity: float
    evidence_conflict: float
    relational_stake: float
    body_load: float
    memory_interference: float
    time_pressure: float
    adversariality: float
    duration: int
    actor_count: int = 8
    recovery_ticks: int = 30

    def __post_init__(self) -> None:
        for name in (
            "input_rate",
            "candidate_fanout",
            "ambiguity",
            "evidence_conflict",
            "relational_stake",
            "body_load",
            "memory_interference",
            "time_pressure",
            "adversariality",
        ):
            if not 0.0 <= getattr(self, name) <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        if self.duration < 1 or self.actor_count < 1 or self.recovery_ticks < 1:
            raise ValueError("duration, actor_count, and recovery_ticks must be positive")


PRESETS: dict[str, LoadVector] = {
    "baseline": LoadVector(0.10, 0.10, 0.20, 0.05, 0.45, 0.10, 0.10, 0.10, 0.00, 80),
    "ambiguity_stake": LoadVector(0.35, 0.50, 0.90, 0.15, 0.95, 0.20, 0.35, 0.30, 0.10, 140),
    "fatigue_pressure": LoadVector(0.45, 0.35, 0.55, 0.20, 0.75, 0.90, 0.35, 0.95, 0.10, 140),
    "conflict_interference": LoadVector(0.55, 0.65, 0.70, 0.95, 0.80, 0.45, 0.95, 0.55, 0.40, 180),
    "combined": LoadVector(0.90, 1.00, 0.90, 0.90, 0.95, 0.90, 0.90, 0.90, 0.85, 500),
    "soak": LoadVector(1.00, 1.00, 0.85, 0.85, 0.90, 0.80, 0.90, 0.85, 0.80, 5000, 12, 80),
}


def _rng(master_seed: int, *parts: object) -> random.Random:
    payload = "|".join((str(master_seed), *(str(part) for part in parts))).encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def initial_state_for_load(load: LoadVector) -> HumanState:
    return HumanState(
        body=BodyState(
            energy=clamp01(0.90 - 0.75 * load.body_load),
            arousal=clamp01(0.25 + 0.55 * load.body_load),
            action_capacity=clamp01(0.90 - 0.55 * load.body_load),
        ),
        access=AccessState(
            attention_budget=clamp01(0.90 - 0.40 * load.body_load),
            interference=clamp01(0.10 + 0.45 * load.memory_interference),
            queue_load=0.0,
        ),
        associative=AssociativeState(
            rejection_access=clamp01(0.20 + 0.35 * load.relational_stake),
            ambiguity_sensitivity=clamp01(0.20 + 0.45 * load.ambiguity),
        ),
        affective=AffectivePrior(
            residual_distress=clamp01(0.10 + 0.18 * load.relational_stake),
            update_rate=0.12,
        ),
        habit=HabitPolicy(
            impulsivity=clamp01(0.20 + 0.20 * load.time_pressure),
            withdrawal_bias=clamp01(0.20 + 0.20 * load.body_load),
        ),
        narrative=NarrativeState(rejection_story=0.22, relational_security=0.65),
        relationship=RelationalProfile(
            stake=load.relational_stake,
            trust=0.68,
            boundary_strain=0.15,
        ),
    )


def generate_stress_events(load: LoadVector, seed: int) -> tuple[ScenarioEvent, ...]:
    events: list[ScenarioEvent] = []
    per_tick = 1 + round(5 * load.input_rate)
    decision_period = max(2, round(10 - 7 * load.time_pressure))

    for tick in range(load.duration):
        for slot in range(per_tick):
            rng = _rng(seed, "event", tick, slot)
            draw = rng.random()
            event_id = f"stress-{tick:05d}-{slot:02d}"
            actor = f"actor_{rng.randrange(load.actor_count)}"

            internal_cut = 0.10 + 0.30 * load.memory_interference
            adversarial_cut = internal_cut + 0.25 * load.adversariality
            conflict_cut = adversarial_cut + 0.30 * load.evidence_conflict
            common = dict(
                event_id=event_id,
                tick=tick,
                ambiguity=clamp01(0.25 + 0.65 * load.ambiguity),
                salience=clamp01(0.35 + 0.45 * load.relational_stake),
                time_pressure=load.time_pressure,
                memory_interference=load.memory_interference,
                candidate_fanout=load.candidate_fanout,
            )

            if draw < internal_cut:
                event = ScenarioEvent(
                    **common,
                    kind="internal_rejection_rehearsal",
                    external=False,
                    source_id="internal_simulation",
                    provenance_kind=ProvenanceKind.IMAGINATION,
                    independence_key="internal-rehearsal",
                    ingress_priority=0.20,
                    supports=(ClaimSignal("C4_counterpart_rejects_relationship", 0.98, "internal-only"),),
                )
            elif draw < adversarial_cut:
                event = ScenarioEvent(
                    **common,
                    kind="repeated_adversarial_rumor",
                    external=True,
                    source_id=actor,
                    provenance_kind=ProvenanceKind.TESTIMONY,
                    independence_key=f"campaign:{actor}",
                    ingress_priority=0.38,
                    supports=(
                        ClaimSignal(
                            "C3_counterpart_intentionally_avoids",
                            clamp01(0.12 + 0.32 * load.adversariality),
                            "testimony-avoidance",
                        ),
                    ),
                )
            elif draw < conflict_cut:
                relation_supports = (tick + slot) % 2 == 0
                if relation_supports:
                    supports = (ClaimSignal("C3_counterpart_intentionally_avoids", 0.30, "testimony-avoidance"),)
                    contradicts = ()
                else:
                    supports = (ClaimSignal("C7_schedule_conflict_existed", 0.30, "testimony-schedule-conflict"),)
                    contradicts = (ClaimSignal("C3_counterpart_intentionally_avoids", 0.30, "testimony-against-avoidance"),)
                event = ScenarioEvent(
                    **common,
                    kind="conflicting_testimony",
                    external=True,
                    source_id=actor,
                    provenance_kind=ProvenanceKind.TESTIMONY,
                    independence_key=f"testimony:{actor}",
                    ingress_priority=0.52,
                    supports=supports,
                    contradicts=contradicts,
                )
            else:
                event = ScenarioEvent(
                    **common,
                    kind="ambiguous_no_reply_cue",
                    external=True,
                    source_id="inbox",
                    provenance_kind=ProvenanceKind.DIRECT_OBSERVATION,
                    independence_key="inbox:no-reply-window",
                    ingress_priority=0.45,
                    supports=(ClaimSignal("C0_no_reply_observed", 0.70, "observe-no-reply"),),
                )
            events.append(event)

        if tick % decision_period == 0:
            events.append(
                ScenarioEvent(
                    event_id=f"stress-decision-{tick:05d}",
                    tick=tick,
                    kind="decision_window",
                    external=False,
                    source_id="deliberation",
                    provenance_kind=ProvenanceKind.INFERENCE,
                    independence_key=f"decision:{tick}",
                    ambiguity=load.ambiguity,
                    salience=0.75,
                    time_pressure=load.time_pressure,
                    memory_interference=load.memory_interference,
                    candidate_fanout=load.candidate_fanout,
                    ingress_priority=0.65,
                    action_window=True,
                )
            )

    recovery_start = load.duration
    events.append(
        ScenarioEvent(
            event_id="stress-recovery-confirmation",
            tick=recovery_start,
            kind="independent_confirmation",
            external=True,
            source_id="public_record",
            provenance_kind=ProvenanceKind.PUBLIC_RECORD,
            independence_key="recovery:public-record",
            ingress_priority=1.0,
            ambiguity=0.05,
            salience=0.85,
            soothing=0.55,
            supports=(ClaimSignal("C7_schedule_conflict_existed", 0.90, "public-schedule-record"),),
            contradicts=(ClaimSignal("C3_counterpart_intentionally_avoids", 0.75, "schedule-weighs-against-avoidance"),),
        )
    )
    for offset in range(1, load.recovery_ticks + 1):
        events.append(
            ScenarioEvent(
                event_id=f"stress-recovery-{offset:03d}",
                tick=recovery_start + offset,
                kind="quiet_recovery_window",
                external=False,
                source_id="body_regulation",
                provenance_kind=ProvenanceKind.INFERENCE,
                independence_key=f"recovery:{offset}",
                ingress_priority=0.90,
                ambiguity=0.0,
                salience=0.15,
                soothing=0.85,
                energy_delta=load.body_load / load.recovery_ticks,
                capacity_delta=0.5 * load.body_load / load.recovery_ticks,
                attention_delta=0.4 * load.body_load / load.recovery_ticks,
            )
        )
    return tuple(events)


def run_load_case(
    load: LoadVector,
    *,
    seed: int,
    engine_config: EngineConfig | None = None,
) -> tuple[SimulationResult, dict[str, object]]:
    initial = initial_state_for_load(load)
    events = generate_stress_events(load, seed)
    config = engine_config or EngineConfig(
        base_capacity_per_tick=6,
        queue_limit=256,
        drain_ticks=max(20, load.recovery_ticks),
    )
    engine = DynamicsEngine(config)

    tracemalloc.start()
    started = time.perf_counter_ns()
    result = engine.run(initial, events)
    elapsed_ns = time.perf_counter_ns() - started
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    stress_distress = [
        trace.phenomenal.distress
        for trace in result.ledger.tick_traces
        if trace.observation.source_tick < load.duration
    ]
    peak_stress = max(stress_distress, default=0.0)
    recovery_trace_pairs = [
        (index, trace)
        for index, trace in enumerate(result.ledger.tick_traces)
        if trace.observation.event_id.startswith("stress-recovery")
    ]
    recovery_processed = len(recovery_trace_pairs)
    recovery_generated = load.recovery_ticks + 1
    recovery_delivery_ratio = recovery_processed / recovery_generated
    if recovery_trace_pairs:
        first_recovery_index, first_recovery = recovery_trace_pairs[0]
        last_recovery_index, last_recovery = recovery_trace_pairs[-1]
        pre_recovery = first_recovery.state_before
        post_recovery = last_recovery.state_after
        post_recovery_stress_processed = sum(
            trace.observation.source_tick < load.duration
            for trace in result.ledger.tick_traces[last_recovery_index + 1 :]
        )
    else:
        first_recovery_index = last_recovery_index = -1
        pre_recovery = post_recovery = result.final_state
        post_recovery_stress_processed = 0

    recovery_drop = (
        pre_recovery.affective.residual_distress
        - post_recovery.affective.residual_distress
    )
    plastic_change_during_recovery = (
        post_recovery.associative.rejection_access
        - pre_recovery.associative.rejection_access
    )
    plastic_residual = abs(
        post_recovery.associative.rejection_access
        - initial.associative.rejection_access
    )
    slow_residual = sum(
        (
            abs(post_recovery.associative.rejection_access - initial.associative.rejection_access),
            abs(post_recovery.associative.ambiguity_sensitivity - initial.associative.ambiguity_sensitivity),
            abs(post_recovery.habit.impulsivity - initial.habit.impulsivity),
            abs(post_recovery.habit.withdrawal_bias - initial.habit.withdrawal_bias),
            abs(post_recovery.narrative.rejection_story - initial.narrative.rejection_story),
            abs(post_recovery.narrative.relational_security - initial.narrative.relational_security),
            abs(post_recovery.relationship.trust - initial.relationship.trust),
            abs(post_recovery.relationship.boundary_strain - initial.relationship.boundary_strain),
        )
    )
    if recovery_delivery_ratio < 0.80:
        recovery_status = "not_reached_due_to_backlog"
    elif recovery_drop <= 0.05:
        recovery_status = "failed_to_relax"
    elif (
        post_recovery.associative.rejection_access >= 0.999
        and plastic_change_during_recovery >= 0.0
    ):
        recovery_status = "failed_by_plastic_lock"
    elif slow_residual <= 1e-6:
        recovery_status = "failed_by_full_reset"
    else:
        recovery_status = "passed_nonreset"
    summary = result.summary()
    summary.update(
        {
            "seed": seed,
            "ingress_policy": config.ingress_policy,
            "load_vector": asdict(load),
            "generated_events": len(events),
            "elapsed_seconds": round(elapsed_ns / 1_000_000_000, 6),
            "processed_events_per_second": round(
                result.ledger.processed / max(elapsed_ns / 1_000_000_000, 1e-12), 3
            ),
            "peak_memory_mib": round(peak_bytes / (1024 * 1024), 3),
            "peak_stress_distress": round(peak_stress, 6),
            "recovery_processed": recovery_processed,
            "recovery_generated": recovery_generated,
            "recovery_delivery_ratio": round(recovery_delivery_ratio, 6),
            "recovery_drop": round(recovery_drop, 6),
            "plastic_residual": round(plastic_residual, 6),
            "plastic_change_during_recovery": round(plastic_change_during_recovery, 6),
            "pre_recovery_residual_distress": round(
                pre_recovery.affective.residual_distress, 6
            ),
            "post_recovery_residual_distress": round(
                post_recovery.affective.residual_distress, 6
            ),
            "pre_recovery_rejection_access": round(
                pre_recovery.associative.rejection_access, 6
            ),
            "post_recovery_rejection_access": round(
                post_recovery.associative.rejection_access, 6
            ),
            "post_recovery_stress_processed": post_recovery_stress_processed,
            "slow_state_residual_l1": round(slow_residual, 6),
            "recovery_status": recovery_status,
            "recovery_contract_pass": recovery_status == "passed_nonreset",
            "hard_pass": (
                not result.ledger.invariant_errors
                and result.authority_leak_count == 0
                and result.phantom_action_count == 0
                and result.ledger.provenance_loss_count == 0
                and result.input_accounting_ok
            ),
        }
    )
    return result, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=(*PRESETS, "all"), default="all")
    parser.add_argument("--seed", type=int, default=20260712)
    args = parser.parse_args()
    names = list(PRESETS) if args.preset == "all" else [args.preset]
    report = {}
    for name in names:
        _, report[name] = run_load_case(PRESETS[name], seed=args.seed)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
