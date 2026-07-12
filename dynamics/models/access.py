"""Descriptive access-capacity hypotheses."""

from __future__ import annotations

from .state import HumanState


def processing_capacity(state: HumanState, base_capacity_per_tick: int) -> int:
    """Capacity is a model output, while queue limits remain protocol policy."""

    attention_factor = 0.35 + 0.65 * state.access.attention_budget
    body_factor = 0.45 + 0.55 * state.body.energy
    return max(1, round(base_capacity_per_tick * attention_factor * body_factor))
