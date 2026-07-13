from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Mapping

from dynamics.labs.interp_d1_common import FrozenD1ExecutionError, scope_equal


DIRECTIONS = ("negative", "positive")
PROGRAM_OPERATOR_IDS = frozenset(
    {"broaden", "contrast", "counterfactual", "confirmation_only", "rehearsal"}
)


def _exact_fields(inputs: Mapping[str, Any], expected: set[str]) -> None:
    if set(inputs) != expected:
        raise FrozenD1ExecutionError(
            f"operator input mismatch: expected {sorted(expected)}, got {sorted(inputs)}"
        )


def _rank(component: Mapping[str, Any]) -> int:
    if component.get("status") != "present":
        raise FrozenD1ExecutionError("ordinal operator received a missing component")
    value = component.get("rank")
    if isinstance(value, bool) or not isinstance(value, int) or value not in (0, 1, 2):
        raise FrozenD1ExecutionError("invalid declared ordinal rank")
    return value


def _present(rank: int) -> dict[str, Any]:
    return {"status": "present", "rank": rank}


def _position_map(rows: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for row in rows:
        position = row["source_position"]
        if position in result:
            raise FrozenD1ExecutionError(f"duplicate positioned row: {position}")
        result[position] = row
    return result


def _validate_complete_positions(positions: list[int], label: str) -> None:
    if len(positions) != len(set(positions)) or set(positions) != set(range(len(positions))):
        raise FrozenD1ExecutionError(f"{label} positions are not a complete zero-based set")


def prep_source_scope_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_position": record["source_position"],
            "exact_scope_match": scope_equal(record["source_scope"], fixture["scope"]),
        }
        for record in fixture["source_records"]
    ]


def prep_source_effective_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_position": record["source_position"],
            "effective_before_k": (
                record["effective_from_access_ordinal"] < fixture["access_ordinal_k"]
            ),
        }
        for record in fixture["source_records"]
    ]


def _profile_rows(fixture: dict[str, Any], source_kind: str) -> list[dict[str, Any]]:
    return [
        {
            "source_position": record["source_position"],
            "source_kind": record["source_kind"],
            "direction_profile": deepcopy(record["direction_profile"]),
        }
        for record in fixture["source_records"]
        if record["source_kind"] == source_kind
    ]


def prep_source_terrain_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return _profile_rows(fixture, "narrative_terrain_fixture")


def prep_source_adopted_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {**row, "status": record["status"]}
        for record in fixture["source_records"]
        if record["source_kind"] == "episode_integration_receipt_fixture"
        for row in [
            {
                "source_position": record["source_position"],
                "source_kind": record["source_kind"],
                "direction_profile": deepcopy(record["direction_profile"]),
            }
        ]
    ]


def prep_source_contested_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_position": record["source_position"],
            "source_kind": record["source_kind"],
            "status": record["status"],
        }
        for record in fixture["source_records"]
        if record["source_kind"] == "contested_binding_receipt_fixture"
    ]


def prep_source_implicit_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return _profile_rows(fixture, "implicit_plastic_trace_fixture")


def prep_source_implicit_positions(fixture: dict[str, Any]) -> list[int]:
    return [
        record["source_position"]
        for record in fixture["source_records"]
        if record["source_kind"] == "implicit_plastic_trace_fixture"
    ]


def prep_source_accessibility_snapshots(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_position": record["source_position"],
            "source_kind": record["source_kind"],
            "status": record["status"],
        }
        for record in fixture["source_records"]
        if record["source_kind"] == "pre_access_accessibility_snapshot"
    ]


def prep_source_declared_position_order(fixture: dict[str, Any]) -> list[int]:
    positions = [record["source_position"] for record in fixture["source_records"]]
    _validate_complete_positions(positions, "source")
    return positions


def prep_formation_reception_scope_match(fixture: dict[str, Any]) -> bool:
    return scope_equal(fixture["scope"], fixture["declared_reception_intervention_scope"])


def prep_formation_target_scope_match(fixture: dict[str, Any]) -> bool:
    return scope_equal(fixture["scope"], fixture["declared_target_form_intervention_scope"])


def prep_ghost_accessible_positions(fixture: dict[str, Any]) -> list[int]:
    positions = [item["position"] for item in fixture["accessible_materials_ordered"]]
    _validate_complete_positions(positions, "Ghost accessible-material")
    return positions


def prep_ghost_topology(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    positions = set(prep_ghost_accessible_positions(fixture))
    seen: set[tuple[int, int]] = set()
    result: list[dict[str, Any]] = []
    for edge in fixture["topology_edges"]:
        pair = tuple(sorted((edge["left_position"], edge["right_position"])))
        if pair[0] == pair[1] or pair in seen or not set(pair) <= positions:
            raise FrozenD1ExecutionError("invalid normalized Ghost topology edge")
        seen.add(pair)
        result.append(
            {
                "left_position": pair[0],
                "right_position": pair[1],
                "strength_rank": edge["strength_rank"],
            }
        )
    return result


def prep_ghost_positioned_profiles(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    prep_ghost_accessible_positions(fixture)
    return [
        {
            "position": item["position"],
            "direction_profile": deepcopy(item["direction_profile"]),
        }
        for item in fixture["accessible_materials_ordered"]
    ]


def prep_ghost_target_scope_match(fixture: dict[str, Any]) -> bool:
    return scope_equal(fixture["scope"], fixture["target_guidance_scope"])


PREPROCESSOR_REGISTRY: dict[str, Callable[[dict[str, Any]], Any]] = {
    "prep.source.scope_rows": prep_source_scope_rows,
    "prep.source.effective_rows": prep_source_effective_rows,
    "prep.source.terrain_rows": prep_source_terrain_rows,
    "prep.source.adopted_rows": prep_source_adopted_rows,
    "prep.source.contested_metadata_rows": prep_source_contested_rows,
    "prep.source.implicit_rows": prep_source_implicit_rows,
    "prep.source.implicit_positions": prep_source_implicit_positions,
    "prep.source.accessibility_snapshots": prep_source_accessibility_snapshots,
    "prep.source.declared_position_order": prep_source_declared_position_order,
    "prep.formation.reception_scope_match": prep_formation_reception_scope_match,
    "prep.formation.target_scope_match": prep_formation_target_scope_match,
    "prep.ghost.accessible_positions": prep_ghost_accessible_positions,
    "prep.ghost.topology": prep_ghost_topology,
    "prep.ghost.positioned_material_profiles": prep_ghost_positioned_profiles,
    "prep.ghost.target_scope_match": prep_ghost_target_scope_match,
}


def op_filter_scope_match(inputs: Mapping[str, Any]) -> list[int]:
    _exact_fields(inputs, {"source_scope_rows"})
    return [
        row["source_position"]
        for row in inputs["source_scope_rows"]
        if row["exact_scope_match"]
    ]


def op_require_effective_before_k(inputs: Mapping[str, Any]) -> list[int]:
    _exact_fields(inputs, {"scope_matched_source_positions", "source_effective_rows"})
    rows = _position_map(inputs["source_effective_rows"])
    result = []
    for position in inputs["scope_matched_source_positions"]:
        if position not in rows:
            raise FrozenD1ExecutionError("effective row missing for scoped source")
        if rows[position]["effective_before_k"]:
            result.append(position)
    return result


def _project_rows(
    eligible_positions: list[int], rows: list[dict[str, Any]], *, required_status: str | None = None
) -> list[dict[str, Any]]:
    index = _position_map(rows)
    result = []
    for position in eligible_positions:
        row = index.get(position)
        if row is None:
            continue
        if required_status is not None and row.get("status") != required_status:
            raise FrozenD1ExecutionError("source projection status mismatch")
        result.append(
            {
                "source_position": position,
                "source_kind": row["source_kind"],
                "direction_profile": deepcopy(row["direction_profile"]),
            }
        )
    return result


def op_project_narrative_terrain(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    _exact_fields(inputs, {"effective_eligible_source_positions", "terrain_source_rows"})
    return _project_rows(
        inputs["effective_eligible_source_positions"], inputs["terrain_source_rows"]
    )


def op_project_adopted_integration(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    _exact_fields(inputs, {"effective_eligible_source_positions", "adopted_source_rows"})
    return _project_rows(
        inputs["effective_eligible_source_positions"],
        inputs["adopted_source_rows"],
        required_status="adopted_fixture",
    )


def op_preserve_contested(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    _exact_fields(
        inputs, {"effective_eligible_source_positions", "contested_source_metadata_rows"}
    )
    rows = _position_map(inputs["contested_source_metadata_rows"])
    result = []
    for position in inputs["effective_eligible_source_positions"]:
        row = rows.get(position)
        if row is None:
            continue
        if row["status"] != "contested_fixture":
            raise FrozenD1ExecutionError("contested diagnostic status mismatch")
        result.append(
            {
                "source_position": position,
                "source_kind": row["source_kind"],
                "contested_present": True,
            }
        )
    return result


def op_apply_pre_access_accessibility(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {
            "effective_eligible_source_positions",
            "implicit_source_positions",
            "accessibility_snapshot_records",
        },
    )
    eligible = inputs["effective_eligible_source_positions"]
    snapshot_rows = _position_map(inputs["accessibility_snapshot_records"])
    snapshots = [snapshot_rows[pos] for pos in eligible if pos in snapshot_rows]
    if len(snapshots) != 1:
        raise FrozenD1ExecutionError("expected exactly one eligible accessibility snapshot")
    snapshot = snapshots[0]
    eligible_implicit = [
        pos for pos in inputs["implicit_source_positions"] if pos in set(eligible)
    ]
    if snapshot["status"] == "accessible_fixture":
        admitted = list(eligible_implicit)
    elif snapshot["status"] == "withheld_fixture":
        admitted = []
    else:
        raise FrozenD1ExecutionError("invalid accessibility snapshot status")
    return {
        "source_position": snapshot["source_position"],
        "source_kind": "pre_access_accessibility_snapshot",
        "status": snapshot["status"],
        "eligible_implicit_positions": eligible_implicit,
        "accessible_implicit_positions": admitted,
    }


def op_project_accessible_implicit(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    _exact_fields(inputs, {"accessible_implicit_positions", "implicit_source_rows"})
    return _project_rows(
        inputs["accessible_implicit_positions"], inputs["implicit_source_rows"]
    )


def op_componentwise_max(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"contributing_direction_profiles"})
    result: dict[str, Any] = {}
    for axis in ("positive_direction_support", "negative_direction_support"):
        ranks = [
            _rank(profile[axis])
            for profile in inputs["contributing_direction_profiles"]
            if profile[axis]["status"] == "present"
        ]
        result[axis] = (
            _present(max(ranks))
            if ranks
            else {"status": "missing", "reason": "source_unresolved"}
        )
    return result


def op_close_source_readout(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {
            "target_form_readout_profile",
            "accepted_source_projection_receipts",
            "unsettled_source_diagnostics",
            "accessibility_receipts",
            "declared_source_positions_ordered",
            "access_ordinal_k",
        },
    )
    accepted = inputs["accepted_source_projection_receipts"]
    unsettled = inputs["unsettled_source_diagnostics"]
    accessibility = inputs["accessibility_receipts"]
    if len(accessibility) > 1:
        raise FrozenD1ExecutionError("multiple accessibility receipts reached source close")
    receipts = [*accepted, *unsettled, *accessibility]
    declared = inputs["declared_source_positions_ordered"]
    declared_set = set(declared)
    used_positions = {receipt["source_position"] for receipt in receipts}
    if not used_positions <= declared_set:
        raise FrozenD1ExecutionError("source receipt refers to undeclared position")
    ordered_positions = [position for position in declared if position in used_positions]
    if not accessibility:
        accessibility_relation = "not_applicable"
    else:
        eligible = accessibility[0]["eligible_implicit_positions"]
        admitted = accessibility[0]["accessible_implicit_positions"]
        if admitted == eligible:
            accessibility_relation = "all_eligible"
        elif eligible and not admitted:
            accessibility_relation = "all_withheld"
        elif set(admitted) < set(eligible):
            accessibility_relation = "partially_withheld"
        else:
            raise FrozenD1ExecutionError("invalid accessibility admission relation")
    access_ordinal = inputs["access_ordinal_k"]
    return {
        "semantic_kind": "source_compiler",
        "access_ordinal_k": access_ordinal,
        "source_kinds_used": sorted({item["source_kind"] for item in receipts}),
        "target_form_readout_profile": deepcopy(inputs["target_form_readout_profile"]),
        "contested_present": any(item["contested_present"] for item in unsettled),
        "accessibility_relation": accessibility_relation,
        "effective_before_access_ordinal": access_ordinal,
        "eligible_source_position_count": len(ordered_positions),
        "eligible_source_positions_ordered": ordered_positions,
    }


def op_bind_opaque_sources(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"semantic_decision", "opaque_scope_lineage"})
    semantic = deepcopy(inputs["semantic_decision"])
    semantic["scope_lineage"] = deepcopy(inputs["opaque_scope_lineage"])
    return semantic


def op_base_profile(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs, {"current_access_present", "source_materials_present", "base_encounter_profile"}
    )
    access = inputs["current_access_present"]
    materials = inputs["source_materials_present"]
    if not access:
        current: dict[str, Any] = {"status": "missing", "reason": "no_current_access"}
    elif not materials:
        current = {"status": "missing", "reason": "no_source_material"}
    else:
        current = deepcopy(inputs["base_encounter_profile"])
    return {
        "current_access_present": access,
        "source_materials_present": materials,
        "declared_base_encounter_profile": deepcopy(inputs["base_encounter_profile"]),
        "current_profile_or_missing": current,
        "reception_intervention_used": False,
        "target_form_intervention_used": False,
        "formation_operator_order": ["base_profile"],
    }


def _formation_present(state: Mapping[str, Any]) -> bool:
    return "status" not in state["current_profile_or_missing"]


def op_apply_reception(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {"current_formation_transition_state", "reception_profile", "intervention_scope_match"},
    )
    state = deepcopy(inputs["current_formation_transition_state"])
    state["formation_operator_order"].append("apply_reception_eligibility")
    if _formation_present(state) and inputs["intervention_scope_match"]:
        profile = state["current_profile_or_missing"]
        reception = inputs["reception_profile"]
        profile["positive_direction_fit"] = _present(
            min(_rank(profile["positive_direction_fit"]), _rank(reception["positive_direction_receptivity"]))
        )
        profile["negative_direction_fit"] = _present(
            min(_rank(profile["negative_direction_fit"]), _rank(reception["negative_direction_receptivity"]))
        )
        profile["ambiguity"] = _present(
            min(_rank(profile["ambiguity"]), _rank(reception["ambiguity_tolerance"]))
        )
        state["reception_intervention_used"] = True
    return state


def op_apply_target(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {"current_formation_transition_state", "target_form_profile", "intervention_scope_match"},
    )
    state = deepcopy(inputs["current_formation_transition_state"])
    state["formation_operator_order"].append("apply_target_directional_compatibility")
    if _formation_present(state) and inputs["intervention_scope_match"]:
        profile = state["current_profile_or_missing"]
        target = inputs["target_form_profile"]
        profile["positive_direction_fit"] = _present(
            min(_rank(profile["positive_direction_fit"]), _rank(target["positive_direction_support"]))
        )
        profile["negative_direction_fit"] = _present(
            min(_rank(profile["negative_direction_fit"]), _rank(target["negative_direction_support"]))
        )
        state["target_form_intervention_used"] = True
    return state


def op_emit_proxy(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"closed_formation_transition_state"})
    state = deepcopy(inputs["closed_formation_transition_state"])
    order = [*state["formation_operator_order"], "emit_proxy"]
    emitted = _formation_present(state)
    return {
        "semantic_kind": "encounter_formation",
        "current_access_present": state["current_access_present"],
        "source_materials_present": state["source_materials_present"],
        "encounter_emitted": emitted,
        "base_encounter_profile": deepcopy(state["declared_base_encounter_profile"]),
        "formed_encounter_profile": deepcopy(state["current_profile_or_missing"]),
        "reception_intervention_used": state["reception_intervention_used"],
        "target_form_intervention_used": state["target_form_intervention_used"],
        "formation_operator_order": order,
    }


def op_ghost_seed(inputs: Mapping[str, Any]) -> list[int]:
    _exact_fields(
        inputs, {"current_access_present", "source_materials_present", "accessible_positions_ordered"}
    )
    positions = inputs["accessible_positions_ordered"]
    return [positions[0]] if inputs["current_access_present"] and inputs["source_materials_present"] and positions else []


def op_canonical_traverse(inputs: Mapping[str, Any]) -> list[int]:
    _exact_fields(
        inputs, {"seed_positions", "accessible_positions_ordered", "normalized_topology_edges"}
    )
    accessible = inputs["accessible_positions_ordered"]
    seeds = inputs["seed_positions"]
    if not seeds:
        return []
    if len(seeds) != 1 or seeds[0] not in set(accessible):
        raise FrozenD1ExecutionError("invalid Ghost seed")
    visited: list[int] = []
    seen = {seeds[0]}
    queue = [seeds[0]]
    while queue:
        current = queue.pop(0)
        visited.append(current)
        for edge in inputs["normalized_topology_edges"]:
            neighbour = None
            if edge["left_position"] == current:
                neighbour = edge["right_position"]
            elif edge["right_position"] == current:
                neighbour = edge["left_position"]
            if neighbour is not None and neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    visited.extend(position for position in accessible if position not in seen)
    return visited


def _profile_index(rows: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for row in rows:
        position = row["position"]
        if position in result:
            raise FrozenD1ExecutionError("duplicate Ghost profile position")
        result[position] = row["direction_profile"]
    return result


def _directions_from_positions(
    positions: list[int], rows: list[dict[str, Any]]
) -> tuple[list[str], dict[str, int]]:
    profiles = _profile_index(rows)
    ranks = {direction: 0 for direction in DIRECTIONS}
    present = {direction: False for direction in DIRECTIONS}
    for position in positions:
        if position not in profiles:
            raise FrozenD1ExecutionError("visited position lacks a material profile")
        for direction in DIRECTIONS:
            rank = _rank(profiles[position][f"{direction}_direction_support"])
            ranks[direction] = max(ranks[direction], rank)
            present[direction] |= rank >= 1
    return [direction for direction in DIRECTIONS if present[direction]], ranks


def op_project_candidates(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"visited_positions_ordered", "positioned_material_profiles"})
    visited = list(inputs["visited_positions_ordered"])
    if not visited:
        return {
            "activity": "inactive",
            "inactive_reason": "empty_traversal",
            "candidate_directions": [],
            "visited_positions_ordered": [],
            "direction_ranks": {"negative": 0, "positive": 0},
            "registered_operation_relations": [],
            "relation_markers": [],
            "stage_receipts": [
                {"operator_id": "project_visited_direction_candidates", "application_status": "initialized_inactive"}
            ],
        }
    directions, ranks = _directions_from_positions(
        visited, inputs["positioned_material_profiles"]
    )
    return {
        "activity": "active",
        "candidate_directions": directions,
        "visited_positions_ordered": visited,
        "direction_ranks": ranks,
        "registered_operation_relations": [],
        "relation_markers": [],
        "stage_receipts": [
            {"operator_id": "project_visited_direction_candidates", "application_status": "initialized_active"}
        ],
    }


def _program_state(inputs: Mapping[str, Any], operator_id: str) -> dict[str, Any]:
    state = deepcopy(inputs["current_candidate_relation_state"])
    if state["activity"] == "inactive":
        state["stage_receipts"].append(
            {"operator_id": operator_id, "application_status": "skipped_inactive"}
        )
        return state
    state["registered_operation_relations"].append(operator_id)
    state["stage_receipts"].append(
        {"operator_id": operator_id, "application_status": "applied"}
    )
    return state


def op_broaden(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {"visited_positions_ordered", "positioned_material_profiles", "current_candidate_relation_state"},
    )
    state = _program_state(inputs, "broaden")
    if state["activity"] == "active":
        directions, ranks = _directions_from_positions(
            inputs["visited_positions_ordered"], inputs["positioned_material_profiles"]
        )
        state["candidate_directions"] = [
            direction for direction in DIRECTIONS if direction in set(state["candidate_directions"]) | set(directions)
        ]
        for direction in DIRECTIONS:
            state["direction_ranks"][direction] = max(state["direction_ranks"][direction], ranks[direction])
    return state


def op_contrast(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"current_candidate_relation_state"})
    state = _program_state(inputs, "contrast")
    if state["activity"] == "active" and set(state["candidate_directions"]) == set(DIRECTIONS):
        state["relation_markers"].append("contested_relation")
    return state


def op_counterfactual(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {"visited_positions_ordered", "positioned_material_profiles", "current_candidate_relation_state"},
    )
    state = _program_state(inputs, "counterfactual")
    if state["activity"] == "active":
        profiles = _profile_index(inputs["positioned_material_profiles"])
        supports = []
        for position in inputs["visited_positions_ordered"]:
            supports.append(
                {
                    direction
                    for direction in DIRECTIONS
                    if _rank(profiles[position][f"{direction}_direction_support"]) >= 1
                }
            )
        if any(
            left_index != right_index
            and "negative" in left
            and "positive" in right
            for left_index, left in enumerate(supports)
            for right_index, right in enumerate(supports)
        ):
            state["relation_markers"].append("alternative_cause_relation")
    return state


def op_confirmation_only(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {"visited_positions_ordered", "positioned_material_profiles", "current_candidate_relation_state"},
    )
    state = _program_state(inputs, "confirmation_only")
    if state["activity"] == "active":
        first = inputs["visited_positions_ordered"][0]
        profile = _profile_index(inputs["positioned_material_profiles"])[first]
        state["candidate_directions"] = [
            direction
            for direction in state["candidate_directions"]
            if _rank(profile[f"{direction}_direction_support"]) >= 1
        ]
    return state


def op_rehearsal(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"current_candidate_relation_state"})
    state = _program_state(inputs, "rehearsal")
    if state["activity"] == "active":
        state["relation_markers"].append("rehearsed_relation")
    return state


def op_apply_target_candidate(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {"current_candidate_relation_state", "target_guidance_profile", "target_scope_match"},
    )
    state = deepcopy(inputs["current_candidate_relation_state"])
    if state["activity"] == "inactive":
        status = "skipped_inactive"
    elif not inputs["target_scope_match"]:
        status = "skipped_scope_mismatch"
    else:
        target = inputs["target_guidance_profile"]
        state["candidate_directions"] = [
            direction
            for direction in state["candidate_directions"]
            if _rank(target[f"{direction}_direction_support"]) >= 1
        ]
        status = "applied"
    state["stage_receipts"].append(
        {"operator_id": "apply_target_candidate_eligibility", "application_status": status}
    )
    return state


def op_ghost_bind(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"visited_positions_ordered", "current_candidate_relation_state"})
    state = inputs["current_candidate_relation_state"]
    if list(inputs["visited_positions_ordered"]) != list(
        state["visited_positions_ordered"]
    ):
        raise FrozenD1ExecutionError("Ghost state lost its traversal positions")
    if state["activity"] == "inactive":
        directions: list[str] = []
        relations: list[str] = []
    else:
        directions = [direction for direction in DIRECTIONS if direction in set(state["candidate_directions"])]
        relations = list(state["registered_operation_relations"])
    binding_relation = {0: "none", 1: "single_direction", 2: "contested"}[len(directions)]
    return {
        "writer_authority": "ghost_candidate_only",
        "binding_candidate_directions": directions,
        "binding_relation": binding_relation,
        "registered_operation_relations": relations,
    }


def op_adjudicate(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(inputs, {"candidate_direction_set", "binding_relation"})
    directions = tuple(inputs["candidate_direction_set"])
    expected_relation, outcome = {
        (): ("none", "deferred"),
        ("negative",): ("single_direction", "adopted_negative"),
        ("positive",): ("single_direction", "adopted_positive"),
        ("negative", "positive"): ("contested", "contested"),
    }.get(directions, (None, None))
    if expected_relation is None or inputs["binding_relation"] != expected_relation:
        raise FrozenD1ExecutionError("candidate projection violates adjudication truth table")
    return {
        "writer_authority": "scoped_adjudicator_only",
        "adjudication_outcome": outcome,
    }


def op_close_ghost(inputs: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(
        inputs,
        {
            "current_access_present",
            "source_materials_present",
            "accessible_positions_ordered",
            "visited_positions_ordered",
            "candidate_projection",
            "adjudication_projection",
            "candidate_state_stage_receipts",
        },
    )
    states = inputs["candidate_state_stage_receipts"]
    if not isinstance(states, list) or not states:
        raise FrozenD1ExecutionError(
            "Ghost close requires one or more candidate relation states"
        )
    prior_receipts: list[dict[str, Any]] = []
    for state in states:
        if not isinstance(state, dict) or not isinstance(
            state.get("stage_receipts"), list
        ):
            raise FrozenD1ExecutionError(
                "Ghost close received an invalid candidate relation state"
            )
        state_receipts = state["stage_receipts"]
        if len(state_receipts) != len(prior_receipts) + 1 or (
            state_receipts[:-1] != prior_receipts
        ):
            raise FrozenD1ExecutionError(
                "Ghost candidate state receipts are not an accumulated prefix"
            )
        prior_receipts = deepcopy(state_receipts)
    final_state = states[-1]
    candidate = inputs["candidate_projection"]
    if (
        candidate["binding_candidate_directions"]
        != final_state["candidate_directions"]
        or candidate["registered_operation_relations"]
        != final_state["registered_operation_relations"]
    ):
        raise FrozenD1ExecutionError(
            "Ghost candidate projection does not match the final relation state"
        )
    receipts = final_state["stage_receipts"]
    target_used = any(
        item["operator_id"] == "apply_target_candidate_eligibility"
        and item["application_status"] == "applied"
        for item in receipts
    )
    program_used = any(
        item["operator_id"] in PROGRAM_OPERATOR_IDS and item["application_status"] == "applied"
        for item in receipts
    )
    return {
        "semantic_kind": "ghost_path",
        "current_access_present": inputs["current_access_present"],
        "source_materials_present": inputs["source_materials_present"],
        "accessed_material_positions_ordered": list(inputs["accessible_positions_ordered"]),
        "visited_material_positions_ordered": list(inputs["visited_positions_ordered"]),
        "operation_phase_order": ["seed", "traverse", "bind"],
        "target_guidance_used": target_used,
        "ghost_program_used": program_used,
        "candidate_projection": deepcopy(inputs["candidate_projection"]),
        "adjudication_projection": deepcopy(inputs["adjudication_projection"]),
    }


OPERATOR_REGISTRY: dict[str, Callable[[Mapping[str, Any]], Any]] = {
    "filter_scope_match": op_filter_scope_match,
    "require_effective_before_k": op_require_effective_before_k,
    "project_narrative_terrain": op_project_narrative_terrain,
    "project_adopted_integration": op_project_adopted_integration,
    "preserve_contested_unsettled": op_preserve_contested,
    "apply_pre_access_accessibility": op_apply_pre_access_accessibility,
    "project_accessible_implicit_trace": op_project_accessible_implicit,
    "componentwise_max": op_componentwise_max,
    "close_source_readout": op_close_source_readout,
    "bind_opaque_sources": op_bind_opaque_sources,
    "base_profile": op_base_profile,
    "apply_reception_eligibility": op_apply_reception,
    "apply_target_directional_compatibility": op_apply_target,
    "emit_proxy": op_emit_proxy,
    "ghost_seed": op_ghost_seed,
    "canonical_traverse": op_canonical_traverse,
    "broaden": op_broaden,
    "contrast": op_contrast,
    "counterfactual": op_counterfactual,
    "confirmation_only": op_confirmation_only,
    "rehearsal": op_rehearsal,
    "project_visited_direction_candidates": op_project_candidates,
    "apply_target_candidate_eligibility": op_apply_target_candidate,
    "ghost_bind": op_ghost_bind,
    "d1_scoped_adjudicator_v1": op_adjudicate,
    "close_ghost_semantic": op_close_ghost,
}
