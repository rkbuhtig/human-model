"""v0.1 compatibility façade for descriptive candidate routing."""

from __future__ import annotations

from .models.routing import BASE_ACTIONS, FANOUT_ACTIONS
from .models.routing import route_candidates as route_model_candidates
from .models.state import HumanState, PhenomenalActivation, RoutedCandidate
from .protocol.events import ScenarioEvent, encode_model_input


def route_candidates(
    state: HumanState,
    event: ScenarioEvent,
    phenomenal: PhenomenalActivation,
    *,
    temperature: float,
) -> tuple[RoutedCandidate, ...]:
    return route_model_candidates(
        state,
        encode_model_input(event),
        phenomenal,
        temperature=temperature,
    )


__all__ = ["BASE_ACTIONS", "FANOUT_ACTIONS", "route_candidates"]
