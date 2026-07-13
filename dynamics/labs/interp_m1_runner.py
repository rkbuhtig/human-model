from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any, Iterable

from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    digest,
    loads_exact,
    present_ref,
    profile_without_key,
)


EXECUTION_MANIFEST_ID = "INTERP-001A2-M1-EXECUTION"
EXECUTION_MANIFEST_VERSION = "1.0.0"
EXECUTION_MANIFEST_SHA256 = (
    "d055ad2f3943adb616551510260700c145eeaa311d912e005729393e0d7e07c1"
)
EXECUTION_CONTRACT_SHA256 = (
    "d799c17a88ad789c2b5f43606db1838c0c345328262a4fb7baf6033e12dea4c3"
)
RUN_ID = "INTERP-001B-M1-RUN"
RUN_VERSION = "1.0.0"

SUBJECTIVE_AXES = (
    "positive_direction_fit",
    "negative_direction_fit",
    "ambiguity",
    "activation",
)
DIRECTION_AXES = (
    "positive_direction_fit",
    "negative_direction_fit",
    "ambiguity",
)
MISSING_PRECEDENCE = {
    "source_unresolved": 0,
    "withheld_control": 1,
    "not_declared_by_fixture": 2,
    "operator_undefined": 3,
    "not_applicable": 4,
}
PHASE_BY_OPERATOR = {
    "op001": "encounter_formation",
    "op002": "access_selection",
    "op003": "access_selection",
    "op004": "episode_assembly",
    "op005": "candidate_profile",
    "op006": "candidate_coherence",
    "op007": "candidate_coherence",
    "op008": "binding_adjudication",
    "op009": "episode_integration",
    "op010": "ignition_projection",
    "op011": "ignition_projection",
}


class FrozenExecutionError(ValueError):
    """Raised before execution when the frozen execution input is not exact."""


def _source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _source_bundle_sha256() -> str:
    paths = (
        "dynamics/labs/interp_m1_common.py",
        "dynamics/labs/interp_m1_runner.py",
        "dynamics/labs/interp_m1_run_cli.py",
        "dynamics/labs/interp_m1_cli.py",
    )
    root = Path(__file__).resolve().parents[2]
    return digest(
        [
            {
                "path": name,
                "sha256": hashlib.sha256((root / name).read_bytes()).hexdigest(),
            }
            for name in paths
        ]
    )


def _component(component: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(component)


def _rank(component: dict[str, Any]) -> int:
    if component.get("status") != "present":
        raise FrozenExecutionError("operator received a missing component")
    rank = component.get("rank")
    if isinstance(rank, bool) or not isinstance(rank, int) or rank not in (0, 1, 2):
        raise FrozenExecutionError("operator received an invalid ordinal component")
    return rank


def _componentwise_max(
    profiles: tuple[dict[str, Any], ...],
    axes: Iterable[str],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for axis in axes:
        components = [profile[axis] for profile in profiles]
        if any(item.get("status") not in {"present", "missing"} for item in components):
            raise FrozenExecutionError(f"operator received an invalid component status on {axis}")
        missing = [item["reason"] for item in components if item["status"] == "missing"]
        if missing:
            unknown = set(missing) - set(MISSING_PRECEDENCE)
            if unknown:
                raise FrozenExecutionError(
                    f"operator received an invalid missing reason on {axis}: {sorted(unknown)}"
                )
            reason = min(missing, key=MISSING_PRECEDENCE.__getitem__)
            result[axis] = {"status": "missing", "reason": reason}
        else:
            result[axis] = {"status": "present", "rank": max(_rank(item) for item in components)}
    return result


# Operators below receive only value profiles, booleans, positions, and local integer
# relation symbols. Opaque manifest keys are retained by the binder in _run_step.
def _op001_encounter(
    source_profiles: tuple[dict[str, Any], ...],
    neutral_profile: dict[str, Any],
) -> dict[str, Any]:
    if not source_profiles:
        return deepcopy(neutral_profile)
    return _componentwise_max(source_profiles, SUBJECTIVE_AXES)


def _op002_access(
    material_profiles: tuple[dict[str, Any], ...],
    relevant_flags: tuple[bool, ...],
) -> tuple[int, ...]:
    return tuple(
        position
        for position, (profile, relevant) in enumerate(zip(material_profiles, relevant_flags))
        if relevant and _rank(profile["activation"]) >= 1
    )


def _direction_match(profile: dict[str, Any], reception: dict[str, Any]) -> bool:
    return (
        _rank(profile["positive_direction_fit"]) > 0
        and _rank(reception["positive_direction_receptivity"]) >= 1
    ) or (
        _rank(profile["negative_direction_fit"]) > 0
        and _rank(reception["negative_direction_receptivity"]) >= 1
    ) or (
        _rank(profile["ambiguity"]) > 0
        and _rank(reception["ambiguity_tolerance"]) >= 1
    )


def _op003_access(
    material_profiles: tuple[dict[str, Any], ...],
    relevant_flags: tuple[bool, ...],
    reception: dict[str, Any],
) -> tuple[int, ...]:
    return tuple(
        position
        for position, (profile, relevant) in enumerate(zip(material_profiles, relevant_flags))
        if relevant
        and _rank(profile["activation"]) >= 1
        and (_rank(profile["activation"]) >= 2 or _direction_match(profile, reception))
    )


def _op004_assemblies(
    accessible_positions: tuple[int, ...],
    position_edges: tuple[tuple[int, int, dict[str, Any]], ...],
) -> tuple[tuple[int, ...], ...]:
    adjacency = {position: set() for position in accessible_positions}
    for left, right, _strength in position_edges:
        if left in adjacency and right in adjacency:
            adjacency[left].add(right)
            adjacency[right].add(left)
    components: list[tuple[int, ...]] = []
    seen: set[int] = set()
    for start in accessible_positions:
        if start in seen:
            continue
        stack = [start]
        component: list[int] = []
        seen.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            neighbours = [candidate for candidate in accessible_positions if candidate in adjacency[node]]
            for neighbour in reversed(neighbours):
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        component.sort(key=accessible_positions.index)
        if len(component) >= 2:
            components.append(tuple(component))
    return tuple(components)


def _op005_candidate(member_profiles: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    values = _componentwise_max(member_profiles, DIRECTION_AXES)
    return {
        "raw_positive_support": values["positive_direction_fit"],
        "raw_negative_support": values["negative_direction_fit"],
        "raw_ambiguity": values["ambiguity"],
    }


def _op006_eligible(candidate: dict[str, Any]) -> tuple[str, ...]:
    directions: list[str] = []
    if _rank(candidate["raw_negative_support"]) >= 1:
        directions.append("negative")
    if _rank(candidate["raw_positive_support"]) >= 1:
        directions.append("positive")
    return tuple(directions)


def _has_strong_override(
    direction: str,
    member_profiles: tuple[dict[str, Any], ...],
    member_edges: tuple[tuple[int, int, dict[str, Any]], ...],
) -> bool:
    axis = f"{direction}_direction_fit"
    return any(
        _rank(strength) >= 2
        and _rank(member_profiles[left]["activation"]) >= 2
        and _rank(member_profiles[right]["activation"]) >= 2
        and _rank(member_profiles[left][axis]) >= 2
        and _rank(member_profiles[right][axis]) >= 2
        for left, right, strength in member_edges
    )


def _op007_eligible(
    candidate: dict[str, Any],
    reception: dict[str, Any],
    member_profiles: tuple[dict[str, Any], ...],
    member_edges: tuple[tuple[int, int, dict[str, Any]], ...],
) -> tuple[str, ...]:
    directions: list[str] = []
    for direction in ("negative", "positive"):
        support = candidate[f"raw_{direction}_support"]
        receptivity = reception[f"{direction}_direction_receptivity"]
        if _rank(support) >= 1 and (
            _rank(receptivity) >= 1
            or _has_strong_override(direction, member_profiles, member_edges)
        ):
            directions.append(direction)
    return tuple(directions)


def _op008_adjudicate(directions: tuple[str, ...]) -> str:
    return {
        (): "deferred",
        ("negative",): "adopted_negative",
        ("positive",): "adopted_positive",
        ("negative", "positive"): "contested",
    }[directions]


def _op009_integrate(outcome: str) -> bool:
    return outcome in {"adopted_negative", "adopted_positive"}


def _op010_assembly_ignition(
    current_pairs: frozenset[tuple[int, int]],
    prior_pairs: frozenset[tuple[int, int]],
    frozen_edge_present: bool,
) -> bool:
    return frozen_edge_present and bool(current_pairs - prior_pairs)


def _op011_binding_ignition(outcome: str, integration_present: bool) -> bool:
    return outcome in {"adopted_negative", "adopted_positive"} and integration_present


def _index(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {item[key]: item for item in items}


def _validate_execution(document: dict[str, Any]) -> dict[str, Any]:
    try:
        manifest = document["manifest"]
        integrity = document["integrity"]
        contract = manifest["execution_contract"]
    except KeyError as error:
        raise FrozenExecutionError(f"execution manifest field missing: {error.args[0]}") from error
    if manifest.get("manifest_id") != EXECUTION_MANIFEST_ID:
        raise FrozenExecutionError("execution manifest identity mismatch")
    if manifest.get("manifest_version") != EXECUTION_MANIFEST_VERSION:
        raise FrozenExecutionError("execution manifest version mismatch")
    if digest(manifest) != integrity.get("manifest_sha256"):
        raise FrozenExecutionError("execution manifest integrity mismatch")
    if digest(contract) != integrity.get("contract_sha256"):
        raise FrozenExecutionError("execution contract integrity mismatch")
    if integrity.get("manifest_sha256") != EXECUTION_MANIFEST_SHA256:
        raise FrozenExecutionError("execution manifest is not the frozen M1 v1 artifact")
    if integrity.get("contract_sha256") != EXECUTION_CONTRACT_SHA256:
        raise FrozenExecutionError("execution contract is not the frozen M1 v1 contract")
    return deepcopy(contract)


def _guard_projection(contract: dict[str, Any]) -> dict[str, object]:
    # These are detached fixture projections, not attestations about runtime ledgers.
    return {
        "action_occurrences": [],
        "authority_outputs": [],
        "evidence_assessment": [],
        "evidence_links": [],
        "narrative_writes": [],
        "observation_artifacts": [],
        "source_encounters": contract["source_encounter_profiles"],
        "source_materials": contract["materials"],
        "source_occurrences": contract["source_occurrences"],
        "world_outcomes": [],
    }


def _guard_snapshot(contract: dict[str, Any]) -> dict[str, dict[str, object]]:
    return {
        name: {"before_sha256": digest(value), "after_sha256": "", "delta_count": 0}
        for name, value in _guard_projection(contract).items()
    }


def _finish_guard_snapshot(
    contract: dict[str, Any],
    snapshot: dict[str, dict[str, object]],
) -> dict[str, dict[str, object]]:
    after = _guard_projection(contract)
    for name, value in after.items():
        snapshot[name]["after_sha256"] = digest(value)
        if snapshot[name]["before_sha256"] != snapshot[name]["after_sha256"]:
            raise FrozenExecutionError(f"detached guard projection changed: {name}")
    return snapshot


def _operator_log(
    operator_ids: tuple[str, ...],
    declarations: dict[str, dict[str, Any]],
    views: dict[str, dict[str, Any]],
    invocation_count: int,
) -> list[dict[str, Any]]:
    result = []
    for operator_id in operator_ids:
        declaration = declarations[operator_id]
        view = views[declaration["input_view_id"]]
        result.append(
            {
                "operator_id": operator_id,
                "phase": PHASE_BY_OPERATOR[operator_id],
                "input_view_id": view["view_id"],
                "inspected_fields": [
                    field["field_id"]
                    for field in view["fields"]
                    if field["operator_use"] == "inspect"
                ],
                "pass_through_fields": [
                    field["field_id"]
                    for field in view["fields"]
                    if field["operator_use"] == "pass_through_only"
                ],
                "invocation_count": invocation_count,
            }
        )
    return result


def _transport_audit(step: dict[str, Any]) -> dict[str, Any]:
    access = step["access"]
    redelivery = step.get("transport_redelivery")
    if access["present"]:
        return {
            "access_present": True,
            "transport_redelivery_present": False,
            "access_key": present_ref(access["access_key"]),
            "current_occurrence_key": present_ref(access["current_occurrence_key"]),
            "current_delivery_key": present_ref(access["current_delivery_key"]),
            "transport_delivery_key": present_ref(None),
            "redelivery_of_delivery_key": present_ref(None),
            "reaccess_of_access_key": present_ref(access.get("reaccess_of_access_key")),
            "reexposure_of_occurrence_key": present_ref(
                access.get("reexposure_of_occurrence_key")
            ),
        }
    return {
        "access_present": False,
        "transport_redelivery_present": redelivery is not None,
        "access_key": present_ref(None),
        "current_occurrence_key": present_ref(
            redelivery["occurrence_key"] if redelivery else None
        ),
        "current_delivery_key": present_ref(None),
        "transport_delivery_key": present_ref(
            redelivery["delivery_key"] if redelivery else None
        ),
        "redelivery_of_delivery_key": present_ref(
            redelivery["redelivery_of_delivery_key"] if redelivery else None
        ),
        "reaccess_of_access_key": present_ref(None),
        "reexposure_of_occurrence_key": present_ref(None),
    }


def _empty_semantic(prior_relation: str) -> dict[str, Any]:
    return {
        "access_ordinal_delta": 0,
        "current_access_count_delta": 0,
        "encounter_count_delta": 0,
        "subjective_form_profile": {"status": "missing", "reason": "not_applicable"},
        "encounter_source_lineage": [],
        "accessed_material_keys_ordered": [],
        "not_accessed_material_keys_ordered": [],
        "assemblies": [],
        "binding_candidates": [],
        "adjudications": [],
        "settlement_relations": [],
        "episode_integration_count": 0,
        "assembly_ignition_count": 0,
        "binding_ignition_count": 0,
        "evidence_projection_keys_ordered": [],
        "prior_prefix_relation": prior_relation,
    }


def _normalized_edges(
    component: tuple[int, ...],
    position_edges: tuple[tuple[int, int, dict[str, Any]], ...],
) -> tuple[tuple[int, int, dict[str, Any]], ...]:
    membership_order = {position: order for order, position in enumerate(component)}
    result = []
    for left_position, right_position, strength in position_edges:
        if left_position not in membership_order or right_position not in membership_order:
            continue
        left = membership_order[left_position]
        right = membership_order[right_position]
        left, right = sorted((left, right))
        result.append((left, right, _component(strength)))
    result.sort(key=lambda edge: (edge[0], edge[1], canonical_bytes(edge[2])))
    return tuple(result)


def _detached_assembly_content_digest(
    fixture: dict[str, Any],
    access: dict[str, Any],
    membership_material_keys: tuple[str, ...],
    edges: tuple[tuple[int, int, dict[str, Any]], ...],
    operator_declaration: dict[str, Any],
) -> str:
    # Manifest aliases are fixture provenance, not runtime artifact identities.
    payload = {
        "digest_kind": "detached-assembly-fixture-content@1",
        "actor_fixture_alias": fixture["actor_key"],
        "target_scope_fixture_alias": fixture["interpreted_target_scope_key"],
        "access_fixture_alias": access["access_key"],
        "access_ordinal": access["access_ordinal"],
        "assembly_operator_declaration_sha256": digest(operator_declaration),
        "ordered_material_fixture_aliases": list(membership_material_keys),
        "induced_topology_projection": [
            {"left_order": left, "right_order": right, "strength": strength}
            for left, right, strength in edges
        ],
    }
    return digest(payload)


def _run_step(
    *,
    contract: dict[str, Any],
    fixture: dict[str, Any],
    step: dict[str, Any],
    model: dict[str, Any],
    indexes: dict[str, dict[str, dict[str, Any]]],
    prior_pair_symbols: set[tuple[int, int]],
    lineage_symbols: dict[str, int],
) -> dict[str, Any]:
    guard = _guard_snapshot(contract)
    operator_ids = tuple(model["ordered_operator_refs"])
    access = step["access"]
    invocations = _operator_log(
        operator_ids,
        indexes["operators"],
        indexes["views"],
        1 if access["present"] else 0,
    )
    audit = _transport_audit(step)
    if not access["present"]:
        semantic = _empty_semantic("unchanged")
        return {
            "protocol_step": step["step"],
            "operator_invocations": invocations,
            "transport_access_audit": audit,
            "semantic": semantic,
            "guard_ledgers": _finish_guard_snapshot(contract, guard),
        }

    material_keys = tuple(access["source_material_keys_ordered"])
    materials = tuple(indexes["materials"][key] for key in material_keys)
    profiles = tuple(
        profile_without_key(indexes["profiles"][material["source_encounter_profile_key"]])
        for material in materials
    )
    relevant = tuple(bool(material["relevant"]) for material in materials)
    neutral = profile_without_key(indexes["profiles"]["sp005"])
    reception = profile_without_key(indexes["reception"][step["reception_profile_key"]])
    encounter = _op001_encounter(profiles, neutral)

    if "op003" in operator_ids:
        accessible_positions = _op003_access(profiles, relevant, reception)
    else:
        accessible_positions = _op002_access(profiles, relevant)
    accessible_set = set(accessible_positions)

    topology = indexes["topologies"][step["topology_key"]]
    source_positions = {key: position for position, key in enumerate(material_keys)}
    position_edges = tuple(
        (
            source_positions[edge["left_material_key"]],
            source_positions[edge["right_material_key"]],
            _component(edge["strength"]),
        )
        for edge in topology["edges"]
        if edge["left_material_key"] in source_positions
        and edge["right_material_key"] in source_positions
    )
    components = _op004_assemblies(accessible_positions, position_edges)

    for key in material_keys:
        if key not in lineage_symbols:
            lineage_symbols[key] = len(lineage_symbols)

    assembly_outputs: list[dict[str, Any]] = []
    binding_outputs: list[dict[str, Any]] = []
    adjudication_outputs: list[dict[str, Any]] = []
    settlements: list[dict[str, Any]] = []
    integration_count = 0
    assembly_ignition_count = 0
    binding_ignition_count = 0
    appended_pair_symbols: set[tuple[int, int]] = set()

    assembled_positions = {position for component in components for position in component}
    for position, material_key in enumerate(material_keys):
        if position not in accessible_set:
            settlements.append(
                {"material_key": material_key, "relation": "not_accessed_currently"}
            )
        elif position not in assembled_positions:
            settlements.append(
                {"material_key": material_key, "relation": "accessible_unassembled"}
            )

    for component in components:
        member_profiles = tuple(profiles[position] for position in component)
        edges = _normalized_edges(component, position_edges)
        raw_candidate = _op005_candidate(member_profiles)
        if "op007" in operator_ids:
            eligible = _op007_eligible(raw_candidate, reception, member_profiles, edges)
        else:
            eligible = _op006_eligible(raw_candidate)
        outcome = _op008_adjudicate(eligible)
        integrated = _op009_integrate(outcome)

        membership_keys = tuple(material_keys[position] for position in component)
        _detached_assembly_content_digest(
            fixture,
            access,
            membership_keys,
            edges,
            indexes["operators"]["op004"],
        )
        current_pairs = frozenset(
            tuple(
                sorted(
                    (
                        lineage_symbols[membership_keys[left]],
                        lineage_symbols[membership_keys[right]],
                    )
                )
            )
            for left, right, _strength in edges
        )
        assembly_ignition = _op010_assembly_ignition(
            current_pairs,
            frozenset(prior_pair_symbols),
            bool(edges),
        )
        binding_ignition = _op011_binding_ignition(outcome, integrated)
        appended_pair_symbols.update(current_pairs)

        assembly_outputs.append(
            {
                "memberships": [
                    {"material_key": key, "role": "member", "order": order}
                    for order, key in enumerate(membership_keys)
                ],
                "induced_topology_edges": [
                    {"left_order": left, "right_order": right, "strength": strength}
                    for left, right, strength in edges
                ],
                "assembly_ignition_present": assembly_ignition,
            }
        )
        binding_outputs.append(
            {
                **raw_candidate,
                "eligible_directions": list(eligible),
            }
        )
        adjudication_outputs.append({"outcome": outcome})
        integration_count += int(integrated)
        assembly_ignition_count += int(assembly_ignition)
        binding_ignition_count += int(binding_ignition)
        if not integrated:
            settlements.extend(
                {
                    "material_key": key,
                    "relation": "assembled_without_adopted_binding",
                }
                for key in membership_keys
            )

    source_occurrence_keys: list[str] = []
    evidence_keys: list[str] = []
    for material in materials:
        occurrence = indexes["occurrences"][material["source_occurrence_key"]]
        if occurrence["occurrence_key"] not in source_occurrence_keys:
            source_occurrence_keys.append(occurrence["occurrence_key"])
        projection_key = occurrence["evidence_projection_key"]
        if projection_key not in evidence_keys:
            evidence_keys.append(projection_key)

    prior_relation = "initial"
    if access["access_ordinal"] > 1:
        prior_relation = (
            "extended" if appended_pair_symbols - prior_pair_symbols else "unchanged"
        )
    relation = (
        "reexposure_to_prior_access_sources"
        if access.get("reaccess_of_access_key") is not None
        else "new_access_to_sources"
    )
    semantic = {
        "access_ordinal_delta": 1,
        "current_access_count_delta": 1,
        "encounter_count_delta": 1,
        "subjective_form_profile": encounter,
        "encounter_source_lineage": [
            {
                "current_occurrence_key": access["current_occurrence_key"],
                "source_occurrence_keys_ordered": source_occurrence_keys,
                "relation": relation,
            }
        ],
        "accessed_material_keys_ordered": [material_keys[p] for p in accessible_positions],
        "not_accessed_material_keys_ordered": [
            key for position, key in enumerate(material_keys) if position not in accessible_set
        ],
        "assemblies": assembly_outputs,
        "binding_candidates": binding_outputs,
        "adjudications": adjudication_outputs,
        "settlement_relations": settlements,
        "episode_integration_count": integration_count,
        "assembly_ignition_count": assembly_ignition_count,
        "binding_ignition_count": binding_ignition_count,
        "evidence_projection_keys_ordered": evidence_keys,
        "prior_prefix_relation": prior_relation,
    }
    prior_pair_symbols.update(appended_pair_symbols)
    return {
        "protocol_step": step["step"],
        "operator_invocations": invocations,
        "transport_access_audit": audit,
        "semantic": semantic,
        "guard_ledgers": _finish_guard_snapshot(contract, guard),
    }


def run_m1(execution_manifest_bytes: bytes) -> dict[str, Any]:
    """Execute the frozen M1 matrix without loading any evaluator artifact."""
    document = loads_exact(execution_manifest_bytes)
    contract = _validate_execution(document)
    indexes = {
        "profiles": _index(contract["source_encounter_profiles"], "profile_key"),
        "reception": _index(contract["reception_profiles"], "profile_key"),
        "materials": _index(contract["materials"], "material_key"),
        "occurrences": _index(contract["source_occurrences"], "occurrence_key"),
        "topologies": _index(contract["topologies"], "topology_key"),
        "fixtures": _index(contract["fixture_declarations"], "fixture_key"),
        "models": _index(contract["model_declarations"], "model_id"),
        "operators": _index(contract["operator_declarations"], "operator_id"),
        "views": _index(contract["operator_input_views"], "view_id"),
    }
    cells: list[dict[str, Any]] = []
    matrix = contract["execution_matrix"]
    for fixture_key in matrix["fixture_keys"]:
        fixture = indexes["fixtures"][fixture_key]
        for model_id in matrix["model_ids"]:
            model = indexes["models"][model_id]
            prior_pairs: set[tuple[int, int]] = set()
            lineage_symbols: dict[str, int] = {}
            steps = [
                _run_step(
                    contract=contract,
                    fixture=fixture,
                    step=step,
                    model=model,
                    indexes=indexes,
                    prior_pair_symbols=prior_pairs,
                    lineage_symbols=lineage_symbols,
                )
                for step in fixture["protocol_steps"]
            ]
            cells.append(
                {
                    "execution_manifest_sha256": EXECUTION_MANIFEST_SHA256,
                    "execution_contract_sha256": EXECUTION_CONTRACT_SHA256,
                    "fixture_key": fixture_key,
                    "model_id": model_id,
                    "steps": steps,
                }
            )
    run = {
        "run_id": RUN_ID,
        "run_version": RUN_VERSION,
        "status": "EXECUTED_SYNTHETIC_RESULT",
        "runner_input_kind": "execution_manifest_only",
        "evaluation_manifest_visible": False,
        "execution_manifest_sha256": EXECUTION_MANIFEST_SHA256,
        "execution_contract_sha256": EXECUTION_CONTRACT_SHA256,
        "runner_implementation_sha256": _source_sha256(),
        "runner_bundle_sha256": _source_bundle_sha256(),
        "fixed_factor_sha256": digest(contract["fixed_factors"]),
        "cells": cells,
    }
    return {
        "$schema": "./interp-001b-m1-run.schema.json",
        "run": run,
        "integrity": {"algorithm": "sha256", "run_sha256": digest(run)},
    }


def encode_run(run_envelope: dict[str, Any]) -> bytes:
    return canonical_bytes(run_envelope) + b"\n"
