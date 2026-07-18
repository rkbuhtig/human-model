from __future__ import annotations

from collections import defaultdict
import math
from typing import Any, Mapping, Sequence

from .source_common_v3 import (
    CONTINUATION_CONDITIONS,
    FEEDBACK_CATEGORIES,
    HISTORY_CONDITIONS,
    IMMEDIATE_ACTIONS,
    LATENT_STATES,
    LONG_HORIZON_REGIONS,
    PROBABILITY_SCALE,
    SourceProcessError,
    total_variation,
)


def _probabilities(units: Sequence[int]) -> list[float]:
    if len(units) == 0 or min(units) < 0 or sum(units) != PROBABILITY_SCALE:
        raise SourceProcessError("diagnostic received invalid probability units")
    return [value / PROBABILITY_SCALE for value in units]


def _matrix(units: Sequence[Sequence[int]]) -> list[list[float]]:
    return [_probabilities(row) for row in units]


def _mix(state: Sequence[float], matrix: Sequence[Sequence[float]]) -> list[float]:
    return [
        sum(state[source] * matrix[source][target] for source in range(len(state)))
        for target in range(len(matrix[0]))
    ]


def _emit(state: Sequence[float], emissions: Sequence[Sequence[float]]) -> list[float]:
    return [
        sum(state[latent] * emissions[latent][category] for latent in range(len(state)))
        for category in range(len(emissions[0]))
    ]


def _kl(left: Sequence[float], right: Sequence[float]) -> float:
    value = 0.0
    for p, q in zip(left, right):
        if p <= 0.0:
            continue
        if q <= 0.0:
            raise SourceProcessError("predictive-memory reference distribution has zero support")
        value += p * math.log(p / q)
    return value


def dobrushin_coefficient(matrix_units: Sequence[Sequence[int]]) -> float:
    rows = list(matrix_units)
    if not rows:
        raise SourceProcessError("Dobrushin coefficient requires a matrix")
    return max(total_variation(left, right) for left in rows for right in rows)


def _normalize_joint_state(weights: Sequence[float]) -> tuple[float, list[float]]:
    mass = sum(weights)
    if mass <= 0.0:
        raise SourceProcessError("zero-mass observation history")
    return mass, [value / mass for value in weights]


def predictive_memory_metrics(instance: Mapping[str, Any]) -> dict[str, float]:
    """Exact finite-horizon filtering without reading any benchmark model.

    The hidden continuation branch is marginalized until its first public cue. At P2/P3
    each branch has a distinct current public cue, so the current-only comparator may
    condition on that visible cue but not on prior action/feedback history.
    """

    initial = {
        history: _probabilities(instance["initial_state_probabilities"][history])
        for history in HISTORY_CONDITIONS
    }
    transitions = {
        branch: _matrix(instance["conditioned_transition_matrices"][branch])
        for branch in CONTINUATION_CONDITIONS
    }
    immediate = _matrix(instance["emission_parameters"]["immediate_action"])
    horizon = _matrix(instance["emission_parameters"]["long_horizon_region"])
    feedback = {
        action: _matrix(instance["emission_parameters"]["action_conditioned_feedback"][action])
        for action in IMMEDIATE_ACTIONS
    }

    p2_action_gain = 0.0
    p2_terminal_gain = 0.0
    p3_action_gain = 0.0
    p3_terminal_gain = 0.0
    cell_weight = 1.0 / (len(HISTORY_CONDITIONS) * len(CONTINUATION_CONDITIONS))

    for history in HISTORY_CONDITIONS:
        for branch in CONTINUATION_CONDITIONS:
            prior0 = initial[history]
            transition = transitions[branch]
            current_z1 = _mix(prior0, transition)
            current_p2_action = _emit(current_z1, immediate)
            current_p2_terminal = _emit(_mix(_mix(current_z1, transition), transition), horizon)
            current_z2 = _mix(current_z1, transition)
            current_p3_action = _emit(current_z2, immediate)
            current_p3_terminal = _emit(_mix(current_z2, transition), horizon)

            p2_histories: dict[tuple[int, int], list[float]] = defaultdict(
                lambda: [0.0] * len(LATENT_STATES)
            )
            for z0, p_z0 in enumerate(prior0):
                for action1 in range(len(IMMEDIATE_ACTIONS)):
                    p_action1 = immediate[z0][action1]
                    action_name = IMMEDIATE_ACTIONS[action1]
                    for feedback1 in range(len(FEEDBACK_CATEGORIES)):
                        p_feedback1 = feedback[action_name][z0][feedback1]
                        observation_mass = p_z0 * p_action1 * p_feedback1
                        if observation_mass == 0.0:
                            continue
                        for z1, p_transition in enumerate(transition[z0]):
                            p2_histories[(action1, feedback1)][z1] += observation_mass * p_transition

            p3_histories: dict[tuple[int, int, int, int], list[float]] = defaultdict(
                lambda: [0.0] * len(LATENT_STATES)
            )
            for p2_key, z1_joint in p2_histories.items():
                p2_mass, posterior_z1 = _normalize_joint_state(z1_joint)
                full_p2_action = _emit(posterior_z1, immediate)
                full_p2_terminal = _emit(_mix(_mix(posterior_z1, transition), transition), horizon)
                p2_action_gain += cell_weight * p2_mass * _kl(full_p2_action, current_p2_action)
                p2_terminal_gain += cell_weight * p2_mass * _kl(full_p2_terminal, current_p2_terminal)

                for z1, joint_z1 in enumerate(z1_joint):
                    if joint_z1 == 0.0:
                        continue
                    for action2 in range(len(IMMEDIATE_ACTIONS)):
                        p_action2 = immediate[z1][action2]
                        action_name = IMMEDIATE_ACTIONS[action2]
                        for feedback2 in range(len(FEEDBACK_CATEGORIES)):
                            p_feedback2 = feedback[action_name][z1][feedback2]
                            mass_before_transition = joint_z1 * p_action2 * p_feedback2
                            if mass_before_transition == 0.0:
                                continue
                            for z2, p_transition in enumerate(transition[z1]):
                                p3_histories[(*p2_key, action2, feedback2)][z2] += (
                                    mass_before_transition * p_transition
                                )

            for z2_joint in p3_histories.values():
                p3_mass, posterior_z2 = _normalize_joint_state(z2_joint)
                full_p3_action = _emit(posterior_z2, immediate)
                full_p3_terminal = _emit(_mix(posterior_z2, transition), horizon)
                p3_action_gain += cell_weight * p3_mass * _kl(full_p3_action, current_p3_action)
                p3_terminal_gain += cell_weight * p3_mass * _kl(
                    full_p3_terminal, current_p3_terminal
                )

    coefficients = [
        dobrushin_coefficient(instance["conditioned_transition_matrices"][branch])
        for branch in CONTINUATION_CONDITIONS
    ]
    return {
        "p2_immediate_predictive_memory_gain_nats": p2_action_gain,
        "p2_terminal_predictive_memory_gain_nats": p2_terminal_gain,
        "p3_immediate_predictive_memory_gain_nats": p3_action_gain,
        "p3_terminal_predictive_memory_gain_nats": p3_terminal_gain,
        "minimum_transition_dobrushin": min(coefficients),
        "maximum_transition_dobrushin": max(coefficients),
    }


def process_adequacy_report(
    instance: Mapping[str, Any], contract: Mapping[str, Any]
) -> dict[str, Any]:
    metrics = predictive_memory_metrics(instance)
    failures: list[str] = []
    thresholds = {
        "p2_immediate_predictive_memory_gain_nats": float(
            contract["minimum_p2_immediate_predictive_memory_gain_nats"]
        ),
        "p3_immediate_predictive_memory_gain_nats": float(
            contract["minimum_p3_immediate_predictive_memory_gain_nats"]
        ),
        "p3_terminal_predictive_memory_gain_nats": float(
            contract["minimum_p3_terminal_predictive_memory_gain_nats"]
        ),
    }
    for name, threshold in thresholds.items():
        if metrics[name] < threshold:
            failures.append(f"{name.upper()}_TOO_SMALL")
    minimum_delta = float(contract["minimum_transition_dobrushin"])
    maximum_delta = float(contract["maximum_transition_dobrushin"])
    if metrics["minimum_transition_dobrushin"] < minimum_delta:
        failures.append("TRANSITION_MIXES_TOO_FAST")
    if metrics["maximum_transition_dobrushin"] > maximum_delta:
        failures.append("TRANSITION_EFFECTIVELY_FROZEN")
    return {"metrics": metrics, "failures": failures}
