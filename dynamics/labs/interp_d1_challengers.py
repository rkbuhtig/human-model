from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any, Callable


class D1ChallengerContractError(ValueError):
    """A challenger or adapter cannot satisfy its frozen closed-world contract."""


_DIRECTIONS = ("negative", "positive")


def _rank(component: dict[str, Any]) -> int:
    if (
        not isinstance(component, dict)
        or component.get("status") != "present"
        or isinstance(component.get("rank"), bool)
        or component.get("rank") not in (0, 1, 2)
    ):
        raise D1ChallengerContractError("challenger received a non-present ordinal component")
    return component["rank"]


def _optional_rank(component: dict[str, Any]) -> int | None:
    if not isinstance(component, dict):
        raise D1ChallengerContractError("challenger received a malformed component")
    if component.get("status") == "missing":
        if set(component) != {"status", "reason"}:
            raise D1ChallengerContractError("malformed tagged-missing component")
        return None
    return _rank(component)


def _scope_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Full scope equality, including the complete target-resolution object."""
    return left == right


def _available(fixture: dict[str, Any]) -> bool:
    return bool(
        fixture["current_access_present"]
        and fixture["source_materials_present"]
    )


def _formation_target(emitted: bool, directions: list[str]) -> dict[str, Any]:
    canonical = [direction for direction in _DIRECTIONS if direction in directions]
    if len(canonical) != len(set(directions)) or set(canonical) != set(directions):
        raise D1ChallengerContractError("formation challenger emitted a malformed direction set")
    if not emitted and canonical:
        raise D1ChallengerContractError("absent formation emitted directions")
    return {"encounter_emitted": emitted, "eligible_directions": canonical}


def _candidate_target(directions: list[str]) -> dict[str, Any]:
    canonical = [direction for direction in _DIRECTIONS if direction in directions]
    if len(canonical) != len(set(directions)) or set(canonical) != set(directions):
        raise D1ChallengerContractError("Ghost challenger emitted a malformed direction set")
    relation, outcome = {
        (): ("none", "deferred"),
        ("negative",): ("single_direction", "adopted_negative"),
        ("positive",): ("single_direction", "adopted_positive"),
        ("negative", "positive"): ("contested", "contested"),
    }[tuple(canonical)]
    return {
        "binding_candidate_directions": canonical,
        "binding_relation": relation,
        "adjudication_outcome": outcome,
    }


def _source_records(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        record
        for record in fixture["source_records"]
        if _scope_equal(record["source_scope"], fixture["scope"])
        and record["effective_from_access_ordinal"] < fixture["access_ordinal_k"]
    ]


def _source_kind_blind_max(
    fixture: dict[str, Any], parameters: dict[str, Any]
) -> dict[str, Any]:
    if parameters:
        raise D1ChallengerContractError("kind-blind max has undeclared parameters")
    records = _source_records(fixture)
    profile: dict[str, Any] = {}
    for direction in ("positive", "negative"):
        axis = f"{direction}_direction_support"
        values = [
            rank
            for rank in (
                _optional_rank(record["direction_profile"][axis])
                for record in records
            )
            if rank is not None
        ]
        profile[axis] = (
            {"status": "present", "rank": max(values)}
            if values
            else {"status": "missing", "reason": "source_unresolved"}
        )
    return {"target_form_readout_profile": profile}


def _material_count_profile(
    fixture: dict[str, Any], parameters: dict[str, Any]
) -> dict[str, Any]:
    if parameters != {"count_cap": 2, "support_threshold": 1}:
        raise D1ChallengerContractError("material-count parameters changed")
    records = _source_records(fixture)
    profile: dict[str, Any] = {}
    for direction in ("positive", "negative"):
        axis = f"{direction}_direction_support"
        count = sum(
            rank is not None and rank >= parameters["support_threshold"]
            for rank in (
                _optional_rank(record["direction_profile"][axis])
                for record in records
            )
        )
        profile[axis] = {
            "status": "present",
            "rank": min(parameters["count_cap"], count),
        }
    return {"target_form_readout_profile": profile}


def _base_formation(
    fixture: dict[str, Any], parameters: dict[str, Any]
) -> dict[str, Any]:
    if parameters:
        raise D1ChallengerContractError("base-only challenger has parameters")
    if not _available(fixture):
        return _formation_target(False, [])
    base = fixture["base_encounter_profile"]
    return _formation_target(
        True,
        [
            direction
            for direction in _DIRECTIONS
            if _rank(base[f"{direction}_direction_fit"]) >= 1
        ],
    )


def _dominant_formation(
    fixture: dict[str, Any], parameters: dict[str, Any]
) -> dict[str, Any]:
    if parameters:
        raise D1ChallengerContractError("dominant-direction challenger has parameters")
    if not _available(fixture):
        return _formation_target(False, [])
    base = fixture["base_encounter_profile"]
    ranks = {
        direction: _rank(base[f"{direction}_direction_fit"])
        for direction in _DIRECTIONS
    }
    maximum = max(ranks.values())
    return _formation_target(
        True,
        [direction for direction in _DIRECTIONS if ranks[direction] == maximum],
    )


def _fixed_rank_formation(
    fixture: dict[str, Any], parameters: dict[str, Any]
) -> dict[str, Any]:
    if parameters != {"fit_threshold": 2, "activation_threshold": 2}:
        raise D1ChallengerContractError("fixed-rank parameters changed")
    if not _available(fixture):
        return _formation_target(False, [])
    base = fixture["base_encounter_profile"]
    directions = []
    if _rank(base["activation"]) >= parameters["activation_threshold"]:
        directions = [
            direction
            for direction in _DIRECTIONS
            if _rank(base[f"{direction}_direction_fit"])
            >= parameters["fit_threshold"]
        ]
    return _formation_target(True, directions)


def _rt_formation(
    fixture: dict[str, Any], parameters: dict[str, Any], *, lookup: bool
) -> dict[str, Any]:
    expected = (
        {
            "lookup_version": "d1_rt_ordinal_lookup_v1",
            "algebraic_alias_of": "CH_RT_CONGRUENCE",
            "control_role": "adapter_equivalence_negative_control",
        }
        if lookup
        else {"rank_threshold": 1}
    )
    if parameters != expected:
        raise D1ChallengerContractError("R/T challenger parameters changed")
    if not _available(fixture):
        return _formation_target(False, [])
    reception_matches = _scope_equal(
        fixture["declared_reception_intervention_scope"], fixture["scope"]
    )
    target_matches = _scope_equal(
        fixture["declared_target_form_intervention_scope"], fixture["scope"]
    )
    directions: list[str] = []
    for direction in _DIRECTIONS:
        ranks = [
            _rank(
                fixture["base_encounter_profile"][
                    f"{direction}_direction_fit"
                ]
            )
        ]
        if reception_matches:
            ranks.append(
                _rank(
                    fixture["declared_reception_intervention"][
                        f"{direction}_direction_receptivity"
                    ]
                )
            )
        if target_matches:
            ranks.append(
                _rank(
                    fixture["declared_target_form_intervention"][
                        f"{direction}_direction_support"
                    ]
                )
            )
        eligible = min(ranks) >= 1 if lookup else all(rank >= 1 for rank in ranks)
        if eligible:
            directions.append(direction)
    return _formation_target(True, directions)


def _canonical_visit(fixture: dict[str, Any]) -> list[int]:
    positions = [item["position"] for item in fixture["accessible_materials_ordered"]]
    if not positions:
        return []
    adjacency = {position: [] for position in positions}
    for edge in fixture["topology_edges"]:
        left, right = edge["left_position"], edge["right_position"]
        if left in adjacency and right in adjacency:
            adjacency[left].append(right)
            adjacency[right].append(left)
    visited: list[int] = []
    seen = {positions[0]}
    queue: deque[int] = deque([positions[0]])
    while queue:
        current = queue.popleft()
        visited.append(current)
        for neighbour in adjacency[current]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    visited.extend(position for position in positions if position not in seen)
    return visited


def _visited_set_ghost(
    fixture: dict[str, Any], parameters: dict[str, Any]
) -> dict[str, Any]:
    if parameters != {"rank_threshold": 1}:
        raise D1ChallengerContractError("visited-set parameters changed")
    if not _available(fixture) or not fixture["accessible_materials_ordered"]:
        return {"binding_candidate_directions": []}
    visited = _canonical_visit(fixture)
    materials = {
        item["position"]: item for item in fixture["accessible_materials_ordered"]
    }
    directions = [
        direction
        for direction in _DIRECTIONS
        if any(
            _optional_rank(
                materials[position]["direction_profile"][
                    f"{direction}_direction_support"
                ]
            )
            is not None
            and _rank(
                materials[position]["direction_profile"][
                    f"{direction}_direction_support"
                ]
            )
            >= parameters["rank_threshold"]
            for position in visited
        )
    ]
    return {"binding_candidate_directions": directions}


def _fixed_ghost(
    fixture: dict[str, Any], parameters: dict[str, Any]
) -> dict[str, Any]:
    if parameters != {"baseline_direction": "positive"}:
        raise D1ChallengerContractError("fixed-Ghost parameters changed")
    directions = (
        [parameters["baseline_direction"]]
        if _available(fixture) and fixture["accessible_materials_ordered"]
        else []
    )
    return {"binding_candidate_directions": directions}


_EXECUTORS: dict[str, Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]] = {
    "source_kind_blind_componentwise_max": _source_kind_blind_max,
    "material_count_or_max_profile": _material_count_profile,
    "base_encounter_passthrough": _base_formation,
    "dominant_direction_category": _dominant_formation,
    "fixed_rank_activation_threshold": _fixed_rank_formation,
    "reception_target_congruence_boolean": lambda fixture, parameters: _rt_formation(
        fixture, parameters, lookup=False
    ),
    "declared_rt_lookup": lambda fixture, parameters: _rt_formation(
        fixture, parameters, lookup=True
    ),
    "visited_direction_set_only": _visited_set_ghost,
    "fixed_ghost_baseline": _fixed_ghost,
}


def execute_challenger(
    declaration: dict[str, Any], fixture: dict[str, Any]
) -> dict[str, Any]:
    """Execute one frozen challenger without run or expected-output access."""
    try:
        executor = _EXECUTORS[declaration["opcode"]]
    except KeyError as error:
        raise D1ChallengerContractError(
            f"unknown challenger opcode: {declaration.get('opcode')}"
        ) from error
    if declaration.get("randomness_policy") != "none":
        raise D1ChallengerContractError("challenger randomness is not forbidden")
    return executor(fixture, deepcopy(declaration["parameters"]))


def adapt_challenger(
    declaration: dict[str, Any], raw: dict[str, Any]
) -> dict[str, Any]:
    """Apply the exact frozen common-target adapter for a challenger."""
    target = declaration["comparison_target_id"]
    if target == "SOURCE_READOUT_TARGET":
        if set(raw) != {"target_form_readout_profile"}:
            raise D1ChallengerContractError("source challenger adapter shape mismatch")
        return deepcopy(raw)
    if target == "FORMATION_DIRECTION_TARGET":
        if set(raw) != {"encounter_emitted", "eligible_directions"}:
            raise D1ChallengerContractError("formation challenger adapter shape mismatch")
        return _formation_target(raw["encounter_emitted"], raw["eligible_directions"])
    if target == "GHOST_CANDIDATE_TARGET":
        if set(raw) != {"binding_candidate_directions"}:
            raise D1ChallengerContractError("Ghost challenger may not supply adjudication")
        return _candidate_target(raw["binding_candidate_directions"])
    raise D1ChallengerContractError(f"unknown comparison target: {target}")


def execute_and_adapt_challenger(
    declaration: dict[str, Any], fixture: dict[str, Any]
) -> dict[str, Any]:
    return adapt_challenger(declaration, execute_challenger(declaration, fixture))


def adapt_model_result(
    comparison_target: dict[str, Any], cell: dict[str, Any]
) -> dict[str, Any]:
    """Adapt one raw D1 model result to an exact declared common target."""
    semantic = cell["semantic"]
    target_id = comparison_target["comparison_target_id"]
    if target_id == "SOURCE_READOUT_TARGET":
        return {
            "target_form_readout_profile": deepcopy(
                semantic["target_form_readout_profile"]
            )
        }
    if target_id == "FORMATION_DIRECTION_TARGET":
        if not semantic["encounter_emitted"]:
            return _formation_target(False, [])
        profile = semantic["formed_encounter_profile"]
        if profile.get("status") == "missing":
            raise D1ChallengerContractError("emitted encounter has a missing profile")
        return _formation_target(
            True,
            [
                direction
                for direction in _DIRECTIONS
                if _optional_rank(profile[f"{direction}_direction_fit"])
                is not None
                and _rank(profile[f"{direction}_direction_fit"]) >= 1
            ],
        )
    if target_id == "GHOST_CANDIDATE_TARGET":
        candidate = semantic["candidate_projection"]
        adjudication = semantic["adjudication_projection"]
        actual = {
            "binding_candidate_directions": deepcopy(
                candidate["binding_candidate_directions"]
            ),
            "binding_relation": candidate["binding_relation"],
            "adjudication_outcome": adjudication["adjudication_outcome"],
        }
        expected = _candidate_target(actual["binding_candidate_directions"])
        if actual != expected:
            raise D1ChallengerContractError("model target violates fixed adjudication table")
        return actual
    raise D1ChallengerContractError(f"unknown comparison target: {target_id}")
