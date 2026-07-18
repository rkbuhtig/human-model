from __future__ import annotations

from collections import Counter
from dataclasses import replace
import math
from typing import Any, Mapping, Sequence

from .v2_core import (
    CONTINUATION_CONDITIONS,
    HStateEnvelope,
    IMMEDIATE_ACTIONS,
    LONG_HORIZON_REGIONS,
    ObservablePrefixV2,
    PredictiveHState,
    PublicContext,
    PublicDeltaV2,
    S0V2Error,
    TypedReceipt,
    canonical_bytes,
    clamp,
    update_chain,
)

MODEL_IDS = ("B0", "B1", "B2", "H")
STATE_VERSION = "s0-h-incremental-2"
PARAMETER_SCHEMA = "s0-v2-counted-naive-bayes/1.0.0"
CHANNELS = {
    "immediate_action": IMMEDIATE_ACTIONS,
    "long_horizon_region": LONG_HORIZON_REGIONS,
}

FeatureVector = dict[str, int]


def _add(features: Counter[str], name: str, count: int = 1) -> None:
    if count > 0:
        features[name] += int(count)


def b0_features(prefix: ObservablePrefixV2) -> FeatureVector:
    features: Counter[str] = Counter()
    current = prefix.receipts[-1].event_kind if prefix.receipts else "NO_NEW_INFORMATION"
    _add(features, f"event={current}")
    _add(features, f"continuation={prefix.context.continuation_condition}")
    _add(features, f"role={prefix.context.role_context}")
    _add(features, f"audience={prefix.context.audience_context}")
    return dict(sorted(features.items()))


_EVENT_SCALAR_EFFECTS = {
    "CURRENT_COMMITMENT_MISSED": (-250, -300),
    "COUNTERPART_ACKNOWLEDGES_IMPACT": (80, 120),
    "COUNTERPART_ACCEPTS_RESPONSIBILITY": (120, 140),
    "COUNTERPART_OFFERS_COSTLY_REPAIR": (220, 260),
    "COUNTERPART_MINIMIZES_IMPACT": (-160, -180),
    "COUNTERPART_SHIFTS_RESPONSIBILITY": (-180, -220),
    "SIMILAR_VIOLATION_REPEATED": (-300, -330),
    "SELF_RESPONSIBILITY_ACCEPTED": (0, 40),
    "SELF_ENDORSEMENT_EXPRESSED": (0, 30),
    "SELF_REPUDIATION_EXPRESSED": (0, -30),
}


def b1_accumulators(prefix: ObservablePrefixV2) -> tuple[int, int]:
    trust = 700 if prefix.context.history_condition == "H-STABLE" else 250
    valence = 200 if prefix.context.history_condition == "H-STABLE" else -250
    # Sum first and clamp once so the intended two-scalar baseline is order-insensitive.
    trust_delta = 0
    valence_delta = 0
    for receipt in prefix.receipts:
        d_trust, d_valence = _EVENT_SCALAR_EFFECTS.get(receipt.event_kind, (0, 0))
        trust_delta += d_trust
        valence_delta += d_valence
    return clamp(trust + trust_delta), clamp(valence + valence_delta)


def b1_features(prefix: ObservablePrefixV2) -> FeatureVector:
    trust, valence = b1_accumulators(prefix)
    return {
        f"trust_bin={trust // 200}": 1,
        f"valence_bin={math.floor(valence / 250)}": 1,
        f"continuation={prefix.context.continuation_condition}": 1,
        f"role={prefix.context.role_context}": 1,
        f"audience={prefix.context.audience_context}": 1,
    }


def b2_features(prefix: ObservablePrefixV2) -> FeatureVector:
    features: Counter[str] = Counter()
    receipts = prefix.receipts
    _add(features, f"history={prefix.context.history_condition}")
    _add(features, f"continuation={prefix.context.continuation_condition}")
    _add(features, f"role={prefix.context.role_context}")
    _add(features, f"audience={prefix.context.audience_context}")
    _add(features, f"receipt_count={len(receipts)}")
    for index, receipt in enumerate(receipts, start=1):
        _add(features, f"event={receipt.event_kind}")
        _add(features, f"event@{index}={receipt.event_kind}")
        distance = len(receipts) - index
        distance_bucket = min(distance, 4)
        _add(features, f"event_from_end@{distance_bucket}={receipt.event_kind}")
        _add(features, f"scope_event={receipt.scope}:{receipt.event_kind}")
        _add(features, f"actor_target={receipt.actor}>{receipt.target}")
        _add(features, f"typed_event={receipt.scope}:{receipt.actor}:{receipt.target}:{receipt.event_kind}")
    events = [item.event_kind for item in receipts]
    for left, right in zip(events, events[1:]):
        _add(features, f"bigram={left}>{right}")
    for first, second, third in zip(events, events[1:], events[2:]):
        _add(features, f"trigram={first}>{second}>{third}")
    for index, action in enumerate(prefix.public_actions, start=1):
        _add(features, f"action={action}")
        _add(features, f"action@{index}={action}")
    for index, feedback in enumerate(prefix.counterpart_feedback, start=1):
        _add(features, f"feedback={feedback}")
        _add(features, f"feedback@{index}={feedback}")
    return dict(sorted(features.items()))


def initial_predictive_state(context: PublicContext) -> PredictiveHState:
    stable = context.history_condition == "H-STABLE"
    return PredictiveHState(
        threat=150 if stable else 500,
        approach=550 if stable else 300,
        control_capacity=700,
        unresolved_breach=100 if stable else 550,
        repair_progress=100,
        trust_expectation=700 if stable else 250,
        continuation_commitment=700,
        counterpart_reliability=700 if stable else 250,
        expected_repair=500 if stable else 250,
        causal_attribution=0,
        control_attribution=0,
        reflective_ownership=0,
        endorsement=0,
        responsibility_acceptance=0,
    )


def initialize_h(context: PublicContext, source_instance_id: str, trajectory_id: str) -> HStateEnvelope:
    return HStateEnvelope.build(
        state_version=STATE_VERSION,
        source_instance_id=source_instance_id,
        trajectory_id=trajectory_id,
        last_step_ordinal=0,
        receipt_chain_sha256="0" * 64,
        predictive_state=initial_predictive_state(context),
    )


def _decay_fast(state: PredictiveHState, gap: int) -> PredictiveHState:
    result = state
    for _ in range(max(0, gap)):
        result = replace(
            result,
            threat=clamp(result.threat - min(40, max(0, result.threat - 100))),
            approach=clamp(result.approach + (20 if result.approach < 500 else -10 if result.approach > 500 else 0)),
            control_capacity=clamp(result.control_capacity + (15 if result.control_capacity < 700 else -5 if result.control_capacity > 700 else 0)),
            unresolved_breach=clamp(result.unresolved_breach - 8),
            repair_progress=clamp(result.repair_progress - 4),
        )
    return result


def _receipt_weight(receipt: TypedReceipt) -> tuple[int, int]:
    # A report can affect interpretation, but certification gives stronger world-event weight.
    if receipt.scope == "CERTIFIED_WORLD_OCCURRENCE":
        return (100, 100)
    if receipt.scope == "REGISTERED_REPORT":
        return (65, 65)
    return (45, 20)


def apply_receipt(state: PredictiveHState, receipt: TypedReceipt) -> PredictiveHState:
    event = receipt.event_kind
    event_weight, world_weight = _receipt_weight(receipt)
    scale = lambda value, weight=event_weight: int(round(value * weight / 100))
    changes: dict[str, int] = {}

    def add(field: str, delta: int) -> None:
        changes[field] = clamp(getattr(state, field) + delta)

    if event == "CURRENT_COMMITMENT_MISSED":
        add("threat", scale(300)); add("approach", scale(-100)); add("unresolved_breach", scale(400, world_weight))
    elif event == "COUNTERPART_ACKNOWLEDGES_IMPACT":
        add("threat", scale(-100)); add("repair_progress", scale(150)); add("expected_repair", scale(80))
    elif event == "COUNTERPART_ACCEPTS_RESPONSIBILITY":
        add("repair_progress", scale(180)); add("expected_repair", scale(150))
    elif event == "COUNTERPART_OFFERS_COSTLY_REPAIR":
        add("threat", scale(-180)); add("approach", scale(160)); add("unresolved_breach", scale(-220, world_weight)); add("repair_progress", scale(300))
    elif event == "COUNTERPART_MINIMIZES_IMPACT":
        add("threat", scale(180)); add("approach", scale(-120)); add("unresolved_breach", scale(160, world_weight)); add("expected_repair", scale(-160))
    elif event == "COUNTERPART_SHIFTS_RESPONSIBILITY":
        add("threat", scale(220)); add("unresolved_breach", scale(200, world_weight)); add("expected_repair", scale(-200))
    elif event == "SIMILAR_VIOLATION_REPEATED":
        add("threat", scale(280)); add("approach", scale(-220)); add("unresolved_breach", scale(320, world_weight)); add("repair_progress", scale(-220))
    elif event in ("AUDIENCE_CONSTRAINT_PRESENT", "ROLE_CONSTRAINT_PRESENT"):
        add("control_capacity", scale(-120)); add("approach", scale(-40))
    elif event == "SELF_ACTION_CAUSALLY_ATTRIBUTED":
        add("causal_attribution", scale(400))
    elif event == "SELF_CONTROL_ATTRIBUTED":
        add("control_attribution", scale(400))
    elif event == "SELF_OWNERSHIP_EXPRESSED":
        add("reflective_ownership", scale(400))
    elif event == "SELF_RESPONSIBILITY_ACCEPTED":
        add("responsibility_acceptance", scale(400))
    elif event == "SELF_ENDORSEMENT_EXPRESSED":
        add("endorsement", scale(400))
    elif event == "SELF_REPUDIATION_EXPRESSED":
        add("endorsement", scale(-400)); add("reflective_ownership", scale(120))
    elif event != "NO_NEW_INFORMATION":
        raise S0V2Error(f"unhandled H event {event}")

    interim = replace(state, **changes)
    # Slow-state consolidation: only threshold-crossing repair/repeat evidence changes it.
    if event == "COUNTERPART_OFFERS_COSTLY_REPAIR" and interim.repair_progress >= 350:
        interim = replace(
            interim,
            trust_expectation=clamp(interim.trust_expectation + scale(90)),
            counterpart_reliability=clamp(interim.counterpart_reliability + scale(100)),
            continuation_commitment=clamp(interim.continuation_commitment + scale(40)),
        )
    elif event == "SIMILAR_VIOLATION_REPEATED" and interim.unresolved_breach >= 600:
        interim = replace(
            interim,
            trust_expectation=clamp(interim.trust_expectation + scale(-170)),
            counterpart_reliability=clamp(interim.counterpart_reliability + scale(-190)),
            continuation_commitment=clamp(interim.continuation_commitment + scale(-120)),
        )
    return interim


def step_h(previous: HStateEnvelope, delta: PublicDeltaV2) -> HStateEnvelope:
    previous.verify()
    if delta.key.source_instance_id != previous.source_instance_id:
        raise S0V2Error("cannot apply delta from another source instance")
    if delta.key.trajectory_id != previous.trajectory_id:
        raise S0V2Error("cannot apply delta from another trajectory")
    if delta.key.step_ordinal != previous.last_step_ordinal + 1:
        raise S0V2Error("H state requires exactly next ordinal")
    state = _decay_fast(previous.predictive_state, delta.key.step_ordinal - previous.last_step_ordinal)
    state = apply_receipt(state, delta.receipt)
    return HStateEnvelope.build(
        state_version=previous.state_version,
        source_instance_id=previous.source_instance_id,
        trajectory_id=previous.trajectory_id,
        last_step_ordinal=delta.key.step_ordinal,
        receipt_chain_sha256=update_chain(previous.receipt_chain_sha256, delta.receipt),
        predictive_state=state,
    )


def h_full_state(prefix: ObservablePrefixV2) -> HStateEnvelope:
    state = initialize_h(prefix.context, prefix.key.source_instance_id, prefix.key.trajectory_id)
    for receipt in prefix.receipts:
        key = type(prefix.key)(prefix.key.source_instance_id, prefix.key.trajectory_id, receipt.ordinal, f"state:{receipt.ordinal}")
        state = step_h(state, PublicDeltaV2(
            schema_version=prefix.schema_version,
            key=key,
            context=prefix.context,
            receipt=receipt,
        ))
    return state


def h_features_from_state(state: HStateEnvelope, context: PublicContext) -> FeatureVector:
    state.verify()
    values = state.predictive_state.to_dict()
    features: Counter[str] = Counter()
    for name, value in values.items():
        _add(features, f"state:{name}:bin={math.floor(value / 200)}")
    _add(features, f"continuation={context.continuation_condition}")
    _add(features, f"role={context.role_context}")
    _add(features, f"audience={context.audience_context}")
    return dict(sorted(features.items()))


def h_full_features(prefix: ObservablePrefixV2) -> FeatureVector:
    return h_features_from_state(h_full_state(prefix), prefix.context)


FEATURE_EXTRACTORS = {
    "B0": b0_features,
    "B1": b1_features,
    "B2": b2_features,
    "H": h_full_features,
}


def empty_parameters() -> dict[str, Any]:
    return {
        "schema_version": PARAMETER_SCHEMA,
        "status": "INITIAL_UNFIT_V2",
        "shared_learner": "COUNTED_MULTINOMIAL_NAIVE_BAYES_NO_MODEL_SPECIFIC_BASE_LOGITS",
        "models": {
            model_id: {
                "model_version": "s0-initial-2",
                "channels": {
                    channel: {
                        "example_count": 0,
                        "category_counts": {category: 0 for category in categories},
                        "feature_totals": {category: {} for category in categories},
                        "total_feature_mass": {category: 0 for category in categories},
                        "vocabulary": [],
                    }
                    for channel, categories in CHANNELS.items()
                },
            }
            for model_id in MODEL_IDS
        },
    }


def fit_parameters(model_id: str, examples: Sequence[tuple[ObservablePrefixV2, str, str]], parameter_document: Mapping[str, Any]) -> dict[str, Any]:
    if model_id not in MODEL_IDS:
        raise S0V2Error("unknown model")
    result = json_clone(parameter_document)
    extractor = FEATURE_EXTRACTORS[model_id]
    for prefix, immediate_label, horizon_label in examples:
        features = extractor(prefix)
        for channel, label in (("immediate_action", immediate_label), ("long_horizon_region", horizon_label)):
            if label not in CHANNELS[channel]:
                raise S0V2Error("unknown training label")
            learned = result["models"][model_id]["channels"][channel]
            learned["example_count"] += 1
            learned["category_counts"][label] += 1
            feature_map = learned["feature_totals"][label]
            for feature, count in features.items():
                feature_map[feature] = feature_map.get(feature, 0) + count
                learned["total_feature_mass"][label] += count
            learned["vocabulary"] = sorted(set(learned["vocabulary"]) | set(features))
    result["models"][model_id]["model_version"] = "s0-initial-2-fitted-development"
    return result


def json_clone(value: Mapping[str, Any]) -> dict[str, Any]:
    import json
    return json.loads(json.dumps(value))


def _channel_logits(model_id: str, features: FeatureVector, channel: str, parameters: Mapping[str, Any]) -> dict[str, float]:
    categories = CHANNELS[channel]
    learned = parameters["models"][model_id]["channels"][channel]
    example_count = learned["example_count"]
    vocabulary = learned["vocabulary"]
    vocab_size = max(1, len(vocabulary))
    logits: dict[str, float] = {}
    for category in categories:
        category_count = learned["category_counts"][category]
        logits[category] = math.log((category_count + 1) / (example_count + len(categories)))
        denominator = learned["total_feature_mass"][category] + vocab_size
        feature_totals = learned["feature_totals"][category]
        for feature, multiplicity in features.items():
            logits[category] += multiplicity * math.log((feature_totals.get(feature, 0) + 1) / denominator)
    return logits


def logits_to_units(logits: Mapping[str, float], categories: tuple[str, ...]) -> dict[str, int]:
    maximum = max(logits.values())
    weights = [math.exp(logits[category] - maximum) for category in categories]
    total = sum(weights)
    raw = [weight / total * 1_000_000 for weight in weights]
    units = [int(item) for item in raw]
    remainder = 1_000_000 - sum(units)
    order = sorted(range(len(categories)), key=lambda i: (raw[i] - units[i], -i), reverse=True)
    for index in order[:remainder]:
        units[index] += 1
    return dict(zip(categories, units))


def predict_from_features(model_id: str, features: FeatureVector, parameters: Mapping[str, Any]) -> dict[str, dict[str, int]]:
    return {
        channel: logits_to_units(_channel_logits(model_id, features, channel, parameters), categories)
        for channel, categories in CHANNELS.items()
    }


def predict_full(model_id: str, prefix: ObservablePrefixV2, parameters: Mapping[str, Any]) -> dict[str, dict[str, int]]:
    return predict_from_features(model_id, FEATURE_EXTRACTORS[model_id](prefix), parameters)


def predict_h_state_only(state: HStateEnvelope, context: PublicContext, parameters: Mapping[str, Any]) -> dict[str, dict[str, int]]:
    return predict_from_features("H", h_features_from_state(state, context), parameters)


def state_delta(previous: HStateEnvelope, current: HStateEnvelope) -> dict[str, str]:
    previous.verify(); current.verify()
    result = {}
    for field in PredictiveHState.__dataclass_fields__:
        before = getattr(previous.predictive_state, field)
        after = getattr(current.predictive_state, field)
        result[field] = "increase" if after > before else "decrease" if after < before else "stable"
    return result


def state_bytes(state: HStateEnvelope) -> int:
    return len(canonical_bytes(state.to_dict()))
