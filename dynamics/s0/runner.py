from __future__ import annotations

from pathlib import Path
import json
from typing import Any, Mapping

from .core import (
    DIRECTION_FIELDS,
    DIRECTION_VALUES,
    IMMEDIATE_ACTIONS,
    LONG_HORIZON_REGIONS,
    OBSERVABLE_PREFIX_FIELDS,
    ObservableEpisodePrefix,
    S0ValidationError,
    canonical_bytes,
    digest,
    normalize_probability_units,
    reject_hidden_fields,
)
from .models import (
    MODEL_IDS,
    directional_readout,
    persistent_state_payload,
    predict_distributions,
    state_byte_size,
)

RUN_SCHEMA_VERSION = "s0-prediction-bundle/1.0.0"


def _card(model_id: str, model_cards: Mapping[str, Any]) -> Mapping[str, Any]:
    cards = {item["model_id"]: item for item in model_cards["models"]}
    if model_id not in cards:
        raise S0ValidationError(f"model card not found: {model_id}")
    card = cards[model_id]
    if tuple(card["allowed_input_fields"]) != OBSERVABLE_PREFIX_FIELDS:
        raise S0ValidationError(f"model card input surface mismatch: {model_id}")
    return card


def run_model(
    model_id: str,
    prefix_document: Mapping[str, Any],
    parameter_document: Mapping[str, Any],
    model_cards: Mapping[str, Any],
    *,
    seed: int = 0,
    include_h_diagnostics: bool = False,
) -> dict[str, Any]:
    if model_id not in MODEL_IDS:
        raise S0ValidationError(f"unknown model: {model_id}")
    reject_hidden_fields(prefix_document)
    prefix = ObservableEpisodePrefix.from_dict(prefix_document)
    card = _card(model_id, model_cards)
    model_parameters = parameter_document["models"].get(model_id)
    if model_parameters is None:
        raise S0ValidationError(f"parameters missing for model: {model_id}")
    if card["model_version"] != model_parameters["model_version"]:
        raise S0ValidationError("model card and parameter version mismatch")
    outputs = predict_distributions(model_id, prefix, parameter_document)
    immediate = normalize_probability_units(outputs["immediate_action"], IMMEDIATE_ACTIONS)
    horizon = normalize_probability_units(outputs["long_horizon_region"], LONG_HORIZON_REGIONS)
    directions = directional_readout(model_id, prefix)
    if set(directions) != set(DIRECTION_FIELDS) or any(
        value not in DIRECTION_VALUES for value in directions.values()
    ):
        raise S0ValidationError("invalid directional readout")
    prefix_bytes = canonical_bytes(prefix.to_dict())
    receipt = {
        "model_id": model_id,
        "model_version": card["model_version"],
        "seed": int(seed),
        "prefix_sha256": digest(prefix.to_dict()),
        "visible_field_names": list(OBSERVABLE_PREFIX_FIELDS),
        "serialized_input_bytes": len(prefix_bytes),
        "persistent_state_bytes": state_byte_size(model_id, prefix),
        "information_boundary": "PUBLIC_OBSERVABLE_PREFIX_ONLY",
        "target_visible": False,
        "reference_state_visible": False,
    }
    document: dict[str, Any] = {
        "schema_version": RUN_SCHEMA_VERSION,
        "trajectory_id": prefix.trajectory_id,
        "step_ordinal": prefix.step_ordinal,
        "immediate_action_distribution": immediate,
        "long_horizon_region_distribution": horizon,
        "directional_readout": directions,
        "runtime_receipt": receipt,
    }
    if include_h_diagnostics:
        if model_id != "H":
            raise S0ValidationError("state diagnostics are H-only")
        document["diagnostic_state"] = persistent_state_payload(model_id, prefix)
        document["diagnostic_authority"] = "H_ONLY_NOT_LEADERBOARD_EVIDENCE"
    return document


def encode_prediction(document: Mapping[str, Any]) -> bytes:
    return canonical_bytes(document) + b"\n"


def load_json_object(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise S0ValidationError(f"expected JSON object: {path}")
    return value
