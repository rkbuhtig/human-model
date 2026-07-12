"""Dependency-neutral values exchanged between protocol and human models."""

from __future__ import annotations

from dataclasses import dataclass
import math


def clamp01(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError(f"non-finite simulation value: {value!r}")
    return min(1.0, max(0.0, float(value)))


@dataclass(frozen=True, slots=True)
class ModelInput:
    """An encoded model-facing input, not a raw protocol event or evidence."""

    event_id: str
    kind: str
    source_is_external: bool
    ambiguity: float = 0.0
    salience: float = 0.5
    time_pressure: float = 0.0
    memory_interference: float = 0.0
    candidate_fanout: float = 0.0
    energy_delta: float = 0.0
    arousal_delta: float = 0.0
    capacity_delta: float = 0.0
    attention_delta: float = 0.0
    soothing: float = 0.0
    trust_delta: float = 0.0
    boundary_delta: float = 0.0
    coercion: float = 0.0
