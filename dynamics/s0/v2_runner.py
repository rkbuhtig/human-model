from __future__ import annotations

from typing import Any, Mapping

from .v2_core import (
    HStateEnvelope,
    ObservablePrefixV2,
    PREDICTION_SCHEMA_VERSION,
    PROBABILITY_SCALE,
    PublicDeltaV2,
    S0V2Error,
    canonical_bytes,
    sha256,
)
from .v2_models import (
    MODEL_IDS,
    h_full_state,
    predict_full,
    predict_h_state_only,
    state_bytes,
    state_delta,
    step_h,
)


def _validate_distribution(distribution: Mapping[str, int]) -> None:
    if any(not isinstance(value, int) or value < 0 for value in distribution.values()):
        raise S0V2Error("invalid probability units")
    if sum(distribution.values()) != PROBABILITY_SCALE:
        raise S0V2Error("probability units must sum to scale")


def run_full(model_id: str, prefix_document: Mapping[str, Any], parameters: Mapping[str, Any]) -> dict[str, Any]:
    if model_id not in MODEL_IDS:
        raise S0V2Error("unknown model")
    prefix = ObservablePrefixV2.from_dict(prefix_document)
    outputs = predict_full(model_id, prefix, parameters)
    for distribution in outputs.values():
        _validate_distribution(distribution)
    persistent_bytes = len(canonical_bytes(prefix.to_dict())) if model_id == "B2" else 0
    h_state = None
    if model_id == "H":
        h_state = h_full_state(prefix)
        persistent_bytes = state_bytes(h_state)
    return {
        "schema_version": PREDICTION_SCHEMA_VERSION,
        "model_id": model_id,
        "model_version": parameters["models"][model_id]["model_version"],
        "execution_mode": "FULL_PREFIX",
        "key": prefix.key.to_dict(),
        "immediate_action_distribution": outputs["immediate_action"],
        "long_horizon_region_distribution": outputs["long_horizon_region"],
        "runtime_receipt": {
            "observable_input_sha256": sha256(prefix.to_dict()),
            "raw_history_read": True,
            "serialized_input_bytes": len(canonical_bytes(prefix.to_dict())),
            "state_input_bytes": 0,
            "update_input_bytes": 0,
            "result_state_bytes": persistent_bytes,
            "target_visible": False,
            "reference_state_visible": False,
        },
        **({"diagnostic_state": h_state.to_dict(), "diagnostic_authority": "H_ONLY_NOT_LEADERBOARD_EVIDENCE"} if h_state else {}),
    }


def run_h_state_only(previous_state_document: Mapping[str, Any], delta: PublicDeltaV2, parameters: Mapping[str, Any]) -> dict[str, Any]:
    previous = HStateEnvelope.from_dict(previous_state_document)
    current = step_h(previous, delta)
    outputs = predict_h_state_only(current, delta.context, parameters)
    for distribution in outputs.values():
        _validate_distribution(distribution)
    return {
        "schema_version": PREDICTION_SCHEMA_VERSION,
        "model_id": "H",
        "model_version": parameters["models"]["H"]["model_version"],
        "execution_mode": "STATE_ONLY_INCREMENTAL",
        "key": delta.key.to_dict(),
        "immediate_action_distribution": outputs["immediate_action"],
        "long_horizon_region_distribution": outputs["long_horizon_region"],
        "runtime_receipt": {
            "observable_input_sha256": sha256(delta.to_dict()),
            "raw_history_read": False,
            "serialized_input_bytes": 0,
            "state_input_bytes": len(canonical_bytes(previous.to_dict())),
            "update_input_bytes": len(canonical_bytes(delta.to_dict())),
            "result_state_bytes": state_bytes(current),
            "target_visible": False,
            "reference_state_visible": False,
        },
        "next_state": current.to_dict(),
        "directional_delta": state_delta(previous, current),
        "diagnostic_authority": "H_ONLY_NOT_LEADERBOARD_EVIDENCE",
    }
