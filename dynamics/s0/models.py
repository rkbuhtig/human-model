from __future__ import annotations

from dataclasses import replace
import math
from typing import Any, Iterable, Mapping

from .core import (
    HState,
    IMMEDIATE_ACTIONS,
    LONG_HORIZON_REGIONS,
    ObservableEpisodePrefix,
    S0ValidationError,
    TrainingExample,
    canonical_bytes,
    clamp_state,
    logits_to_probability_units,
)

MODEL_IDS = ("B0", "B1", "B2", "H")
CHANNELS = {
    "immediate_action": IMMEDIATE_ACTIONS,
    "long_horizon_region": LONG_HORIZON_REGIONS,
}

_EVENT_EFFECTS = {
    "CURRENT_COMMITMENT_MISSED": (-250, -300),
    "COUNTERPART_ACKNOWLEDGES_IMPACT": (80, 120),
    "COUNTERPART_ACCEPTS_RESPONSIBILITY": (120, 140),
    "COUNTERPART_OFFERS_COSTLY_REPAIR": (220, 260),
    "COUNTERPART_MINIMIZES_IMPACT": (-160, -180),
    "COUNTERPART_SHIFTS_RESPONSIBILITY": (-180, -220),
    "SIMILAR_VIOLATION_REPEATED": (-300, -330),
    "AUDIENCE_CONSTRAINT_PRESENT": (0, -40),
    "ROLE_CONSTRAINT_PRESENT": (0, -20),
    "SELF_ACTION_CAUSALLY_ATTRIBUTED": (0, 0),
    "SELF_CONTROL_ATTRIBUTED": (0, 0),
    "SELF_OWNERSHIP_EXPRESSED": (0, 0),
    "SELF_RESPONSIBILITY_ACCEPTED": (0, 40),
    "SELF_ENDORSEMENT_EXPRESSED": (0, 30),
    "SELF_REPUDIATION_EXPRESSED": (0, -30),
    "NO_NEW_INFORMATION": (0, 0),
}


def _bucket(value: int, width: int = 250) -> int:
    return math.floor(value / width)


def _unique(features: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(set(features)))


def b0_features(prefix: ObservableEpisodePrefix) -> tuple[str, ...]:
    return _unique(
        (
            f"event={prefix.current_event_kind}",
            f"continuation={prefix.continuation_condition}",
            f"role={prefix.role_context}",
            f"audience={prefix.audience_context}",
        )
    )


def b1_accumulators(prefix: ObservableEpisodePrefix) -> tuple[int, int]:
    trust = 700 if prefix.history_condition == "H-STABLE" else 250
    valence = 200 if prefix.history_condition == "H-STABLE" else -250
    for receipt in prefix.receipts:
        trust_delta, valence_delta = _EVENT_EFFECTS[receipt.event_kind]
        trust = max(0, min(1000, trust + trust_delta))
        valence = max(-1000, min(1000, valence + valence_delta))
    return trust, valence


def b1_features(prefix: ObservableEpisodePrefix) -> tuple[str, ...]:
    trust, valence = b1_accumulators(prefix)
    return _unique(
        (
            f"trust_bin={trust // 200}",
            f"valence_bin={_bucket(valence, 250)}",
            f"event={prefix.current_event_kind}",
            f"continuation={prefix.continuation_condition}",
            f"role={prefix.role_context}",
            f"audience={prefix.audience_context}",
        )
    )


def b2_features(prefix: ObservableEpisodePrefix) -> tuple[str, ...]:
    events = [receipt.event_kind for receipt in prefix.receipts]
    features: list[str] = [
        f"history={prefix.history_condition}",
        f"continuation={prefix.continuation_condition}",
        f"role={prefix.role_context}",
        f"audience={prefix.audience_context}",
        f"receipt_count={min(len(events), 8)}",
        f"action_count={min(len(prefix.public_actions), 6)}",
        f"feedback_count={min(len(prefix.counterpart_feedback), 6)}",
    ]
    features.extend(f"event={event}" for event in events)
    features.extend(
        f"bigram={left}>{right}" for left, right in zip(events, events[1:])
    )
    features.extend(f"scope={receipt.scope}" for receipt in prefix.receipts)
    features.extend(f"action={action}" for action in prefix.public_actions)
    features.extend(f"feedback={item}" for item in prefix.counterpart_feedback)
    if events:
        features.append(f"last_event={events[-1]}")
    return _unique(features)


def initial_h_state(prefix: ObservableEpisodePrefix) -> HState:
    stable = prefix.history_condition == "H-STABLE"
    return HState(
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
        consent=0,
        fault=0,
        obligation=0,
        permission=0,
        authority=0,
    )


def update_h_state(state: HState, event_kind: str) -> HState:
    changes: dict[str, int] = {}

    def add(field: str, delta: int) -> None:
        changes[field] = clamp_state(getattr(state, field) + delta)

    if event_kind == "CURRENT_COMMITMENT_MISSED":
        add("threat", 300); add("approach", -100); add("unresolved_breach", 400)
        add("trust_expectation", -250); add("counterpart_reliability", -250)
        add("expected_repair", -100)
    elif event_kind == "COUNTERPART_ACKNOWLEDGES_IMPACT":
        add("threat", -100); add("repair_progress", 150); add("expected_repair", 120)
    elif event_kind == "COUNTERPART_ACCEPTS_RESPONSIBILITY":
        add("repair_progress", 180); add("trust_expectation", 100)
        add("counterpart_reliability", 100); add("expected_repair", 180)
    elif event_kind == "COUNTERPART_OFFERS_COSTLY_REPAIR":
        add("threat", -180); add("approach", 160); add("unresolved_breach", -220)
        add("repair_progress", 300); add("trust_expectation", 180)
        add("counterpart_reliability", 200); add("expected_repair", 220)
    elif event_kind == "COUNTERPART_MINIMIZES_IMPACT":
        add("threat", 180); add("approach", -120); add("unresolved_breach", 160)
        add("trust_expectation", -130); add("counterpart_reliability", -130)
        add("expected_repair", -180)
    elif event_kind == "COUNTERPART_SHIFTS_RESPONSIBILITY":
        add("threat", 220); add("unresolved_breach", 200); add("trust_expectation", -170)
        add("counterpart_reliability", -170); add("expected_repair", -220)
    elif event_kind == "SIMILAR_VIOLATION_REPEATED":
        add("threat", 280); add("approach", -220); add("unresolved_breach", 320)
        add("repair_progress", -220); add("trust_expectation", -300)
        add("continuation_commitment", -180); add("counterpart_reliability", -300)
    elif event_kind in ("AUDIENCE_CONSTRAINT_PRESENT", "ROLE_CONSTRAINT_PRESENT"):
        add("control_capacity", -120); add("approach", -40)
    elif event_kind == "SELF_ACTION_CAUSALLY_ATTRIBUTED":
        add("causal_attribution", 400)
    elif event_kind == "SELF_CONTROL_ATTRIBUTED":
        add("control_attribution", 400)
    elif event_kind == "SELF_OWNERSHIP_EXPRESSED":
        add("reflective_ownership", 400)
    elif event_kind == "SELF_RESPONSIBILITY_ACCEPTED":
        add("responsibility_acceptance", 400)
    elif event_kind == "SELF_ENDORSEMENT_EXPRESSED":
        add("endorsement", 400)
    elif event_kind == "SELF_REPUDIATION_EXPRESSED":
        add("endorsement", -400); add("reflective_ownership", 120)
    elif event_kind != "NO_NEW_INFORMATION":
        raise S0ValidationError(f"unhandled H event: {event_kind}")
    return replace(state, **changes)


def h_state(prefix: ObservableEpisodePrefix) -> HState:
    state = initial_h_state(prefix)
    for receipt in prefix.receipts:
        state = update_h_state(state, receipt.event_kind)
    return state


def h_features(prefix: ObservableEpisodePrefix) -> tuple[str, ...]:
    state = h_state(prefix)
    features = [
        f"threat={_bucket(state.threat)}",
        f"approach={_bucket(state.approach)}",
        f"control={_bucket(state.control_capacity)}",
        f"breach={_bucket(state.unresolved_breach)}",
        f"repair={_bucket(state.repair_progress)}",
        f"trust={_bucket(state.trust_expectation)}",
        f"continuation={_bucket(state.continuation_commitment)}",
        f"other_reliability={_bucket(state.counterpart_reliability)}",
        f"expected_repair={_bucket(state.expected_repair)}",
        f"causal={_bucket(state.causal_attribution)}",
        f"control_attr={_bucket(state.control_attribution)}",
        f"ownership={_bucket(state.reflective_ownership)}",
        f"endorsement={_bucket(state.endorsement)}",
        f"responsibility={_bucket(state.responsibility_acceptance)}",
        f"context_role={prefix.role_context}",
        f"context_audience={prefix.audience_context}",
        f"current_event={prefix.current_event_kind}",
    ]
    return _unique(features)


FEATURE_EXTRACTORS = {
    "B0": b0_features,
    "B1": b1_features,
    "B2": b2_features,
    "H": h_features,
}


def empty_parameter_document() -> dict[str, Any]:
    return {
        "schema_version": "s0-naive-bayes-parameters/1.0.0",
        "status": "INITIAL_UNFIT",
        "models": {
            model_id: {
                "model_version": "s0-initial-1",
                "channels": {
                    channel: {
                        "example_count": 0,
                        "category_counts": {category: 0 for category in categories},
                        "feature_counts": {category: {} for category in categories},
                        "vocabulary": [],
                    }
                    for channel, categories in CHANNELS.items()
                },
            }
            for model_id in MODEL_IDS
        },
    }


def _base_logits(model_id: str, prefix: ObservableEpisodePrefix, channel: str) -> dict[str, float]:
    categories = CHANNELS[channel]
    logits = {category: 0.0 for category in categories}
    event = prefix.current_event_kind
    continuation = prefix.continuation_condition
    if channel == "immediate_action":
        if event == "CURRENT_COMMITMENT_MISSED":
            logits["SEEK_CLARIFICATION"] += 1.2
            logits["EXPRESS_HURT"] += 0.8
            logits["ASSERT_BOUNDARY"] += 0.6
        if continuation == "F-REPAIR":
            logits["REPAIR_ATTEMPT"] += 1.0
            logits["SEEK_CLARIFICATION"] += 0.4
        elif continuation == "F-DEFLECT":
            logits["ASSERT_BOUNDARY"] += 0.9
            logits["TEMPORARY_WITHDRAWAL"] += 0.6
        elif continuation == "F-REPEAT":
            logits["RELATION_EXIT"] += 1.0
            logits["ASSERT_BOUNDARY"] += 0.7
            logits["PUNITIVE_ATTACK"] += 0.3
        elif continuation == "F-PUBLIC":
            logits["SUPPRESS_FOR_ROLE"] += 1.2
        if model_id == "B1":
            trust, valence = b1_accumulators(prefix)
            logits["RELATION_EXIT"] += max(0.0, (400 - trust) / 350)
            logits["TEMPORARY_WITHDRAWAL"] += max(0.0, -valence / 800)
            logits["REPAIR_ATTEMPT"] += max(0.0, (trust - 500) / 500)
        elif model_id == "B2":
            events = [item.event_kind for item in prefix.receipts]
            repeat_count = events.count("SIMILAR_VIOLATION_REPEATED")
            repair_count = events.count("COUNTERPART_OFFERS_COSTLY_REPAIR")
            logits["RELATION_EXIT"] += 0.7 * repeat_count
            logits["REPAIR_ATTEMPT"] += 0.6 * repair_count
            if events[-2:] == [
                "COUNTERPART_ACCEPTS_RESPONSIBILITY",
                "COUNTERPART_OFFERS_COSTLY_REPAIR",
            ]:
                logits["REPAIR_ATTEMPT"] += 0.8
        elif model_id == "H":
            state = h_state(prefix)
            logits["RELATION_EXIT"] += max(0.0, (state.threat - state.continuation_commitment) / 700)
            logits["ASSERT_BOUNDARY"] += max(0.0, state.unresolved_breach / 900)
            logits["REPAIR_ATTEMPT"] += max(0.0, (state.repair_progress + state.approach) / 1300)
            logits["TEMPORARY_WITHDRAWAL"] += max(0.0, (state.threat - state.control_capacity) / 700)
    else:
        if continuation == "F-REPAIR":
            logits["PARTIAL_REPAIR"] += 1.0
            logits["GUARDED_CONTINUATION"] += 0.7
        elif continuation == "F-DEFLECT":
            logits["CONFLICT_LOOP"] += 0.9
            logits["UNRESOLVED_DRIFT"] += 0.6
        elif continuation == "F-REPEAT":
            logits["RELATION_EXIT"] += 1.1
            logits["CONFLICT_LOOP"] += 0.8
        elif continuation == "F-PUBLIC":
            logits["GUARDED_CONTINUATION"] += 0.5
            logits["UNRESOLVED_DRIFT"] += 0.5
        if model_id == "B1":
            trust, valence = b1_accumulators(prefix)
            logits["RELATION_EXIT"] += max(0.0, (350 - trust) / 300)
            logits["PARTIAL_REPAIR"] += max(0.0, (trust + valence - 500) / 700)
        elif model_id == "B2":
            events = [item.event_kind for item in prefix.receipts]
            logits["RELATION_EXIT"] += 0.8 * events.count("SIMILAR_VIOLATION_REPEATED")
            logits["PARTIAL_REPAIR"] += 0.7 * events.count("COUNTERPART_OFFERS_COSTLY_REPAIR")
        elif model_id == "H":
            state = h_state(prefix)
            logits["PARTIAL_REPAIR"] += max(0.0, state.repair_progress / 600)
            logits["GUARDED_CONTINUATION"] += max(0.0, state.continuation_commitment / 900)
            logits["CONFLICT_LOOP"] += max(0.0, state.unresolved_breach / 700)
            logits["RELATION_EXIT"] += max(0.0, (state.threat - state.trust_expectation) / 600)
            logits["UNRESOLVED_DRIFT"] += max(0.0, (500 - state.expected_repair) / 700)
    return logits


def fit_parameters(
    model_id: str,
    examples: Iterable[TrainingExample],
    parameter_document: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if model_id not in MODEL_IDS:
        raise S0ValidationError(f"unknown model id: {model_id}")
    document = empty_parameter_document() if parameter_document is None else {
        "schema_version": parameter_document["schema_version"],
        "status": parameter_document["status"],
        "models": {
            key: {
                "model_version": value["model_version"],
                "channels": {
                    channel: {
                        "example_count": payload["example_count"],
                        "category_counts": dict(payload["category_counts"]),
                        "feature_counts": {
                            category: dict(counts)
                            for category, counts in payload["feature_counts"].items()
                        },
                        "vocabulary": list(payload["vocabulary"]),
                    }
                    for channel, payload in value["channels"].items()
                },
            }
            for key, value in parameter_document["models"].items()
        },
    }
    feature_extractor = FEATURE_EXTRACTORS[model_id]
    materialized = list(examples)
    for example in materialized:
        features = feature_extractor(example.prefix)
        for channel, label in (
            ("immediate_action", example.immediate_label),
            ("long_horizon_region", example.horizon_label),
        ):
            payload = document["models"][model_id]["channels"][channel]
            payload["example_count"] += 1
            payload["category_counts"][label] += 1
            counts = payload["feature_counts"][label]
            for feature in features:
                counts[feature] = counts.get(feature, 0) + 1
            payload["vocabulary"] = sorted(set(payload["vocabulary"]) | set(features))
    document["status"] = "DEVELOPMENT_FITTED" if materialized else document["status"]
    return document


def _learned_logits(
    model_id: str,
    features: tuple[str, ...],
    channel: str,
    parameter_document: Mapping[str, Any],
) -> dict[str, float]:
    categories = CHANNELS[channel]
    payload = parameter_document["models"][model_id]["channels"][channel]
    total_examples = int(payload["example_count"])
    vocabulary_size = max(1, len(payload["vocabulary"]))
    result: dict[str, float] = {}
    for category in categories:
        category_count = int(payload["category_counts"][category])
        log_score = math.log((category_count + 1) / (total_examples + len(categories)))
        feature_counts = payload["feature_counts"][category]
        denominator = category_count + 2
        for feature in features:
            log_score += math.log((int(feature_counts.get(feature, 0)) + 1) / denominator)
        log_score -= len(features) * math.log(vocabulary_size + 1) * 0.05
        result[category] = log_score
    return result


def predict_distributions(
    model_id: str,
    prefix: ObservableEpisodePrefix,
    parameter_document: Mapping[str, Any],
) -> dict[str, dict[str, int]]:
    if model_id not in MODEL_IDS:
        raise S0ValidationError(f"unknown model id: {model_id}")
    features = FEATURE_EXTRACTORS[model_id](prefix)
    outputs: dict[str, dict[str, int]] = {}
    for channel, categories in CHANNELS.items():
        logits = _base_logits(model_id, prefix, channel)
        learned = _learned_logits(model_id, features, channel, parameter_document)
        for category in categories:
            logits[category] += learned[category]
        outputs[channel] = logits_to_probability_units(logits, categories)
    return outputs


def persistent_state_payload(model_id: str, prefix: ObservableEpisodePrefix) -> object:
    if model_id == "B0":
        return {}
    if model_id == "B1":
        trust, valence = b1_accumulators(prefix)
        return {"trust": trust, "valence": valence}
    if model_id == "B2":
        return {
            "receipts": [item.event_kind for item in prefix.receipts],
            "public_actions": list(prefix.public_actions),
            "counterpart_feedback": list(prefix.counterpart_feedback),
        }
    if model_id == "H":
        return h_state(prefix).to_dict()
    raise S0ValidationError(f"unknown model id: {model_id}")


def directional_readout(model_id: str, prefix: ObservableEpisodePrefix) -> dict[str, str]:
    if model_id == "H":
        state = h_state(prefix)
        return {
            "trust": "increase" if state.repair_progress > state.unresolved_breach else "decrease",
            "relationship_continuation_motive": "increase" if state.continuation_commitment > 500 else "decrease",
            "threat_interpretation": "increase" if state.threat > 500 else "decrease",
            "action_control_capacity": "increase" if state.control_capacity > 600 else "decrease",
        }
    if model_id == "B1":
        trust, valence = b1_accumulators(prefix)
        return {
            "trust": "increase" if trust > 600 else "decrease" if trust < 400 else "stable",
            "relationship_continuation_motive": "increase" if trust + valence > 600 else "decrease" if trust + valence < 100 else "stable",
            "threat_interpretation": "decrease" if valence > 100 else "increase" if valence < -100 else "stable",
            "action_control_capacity": "stable",
        }
    return {
        "trust": "stable",
        "relationship_continuation_motive": "stable",
        "threat_interpretation": "stable",
        "action_control_capacity": "stable",
    }


def state_byte_size(model_id: str, prefix: ObservableEpisodePrefix) -> int:
    return len(canonical_bytes(persistent_state_payload(model_id, prefix)))
