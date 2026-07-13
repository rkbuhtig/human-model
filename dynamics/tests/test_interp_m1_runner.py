from __future__ import annotations

import ast
from contextlib import ExitStack
from copy import deepcopy
import inspect
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from dynamics.labs import interp_m1_runner as runner
from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    digest,
    file_sha256,
    load_exact,
    loads_exact,
    validate_json_schema,
)


ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS = ROOT / "research" / "benchmarks"
EXECUTION_PATH = BENCHMARKS / "interp-001-m1-v1-execution.json"
EVALUATION_PATH = BENCHMARKS / "interp-001-m1-v1-evaluation.json"
RESULT_SCHEMA_PATH = BENCHMARKS / "interp-001-m1-v1-result.schema.json"
RUN_SCHEMA_PATH = BENCHMARKS / "interp-001b-m1-run.schema.json"
RUNNER_PATH = ROOT / "dynamics" / "labs" / "interp_m1_runner.py"
COMMON_PATH = ROOT / "dynamics" / "labs" / "interp_m1_common.py"
RUN_CLI_PATH = ROOT / "dynamics" / "labs" / "interp_m1_run_cli.py"
CLI_PATH = ROOT / "dynamics" / "labs" / "interp_m1_cli.py"

MODELS = ("R0", "R1", "R2", "R3")
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
MISSING_REF = {"status": "missing", "reason": "not_applicable"}


def _all_models(signature: str) -> dict[str, tuple[str, ...]]:
    return {model: (signature,) for model in MODELS}


EXPECTED_SIGNATURES: dict[str, dict[str, tuple[str, ...]]] = {
    "fx001": _all_models("sig-adopt-positive-new"),
    "fx002": _all_models("sig-adopt-negative-new"),
    "fx003": {
        "R0": ("sig-adopt-positive-new",),
        "R1": ("sig-no-access",),
        "R2": ("sig-defer-positive-new",),
        "R3": ("sig-no-access",),
    },
    "fx004": {
        "R0": ("sig-adopt-negative-new",),
        "R1": ("sig-no-access",),
        "R2": ("sig-defer-negative-new",),
        "R3": ("sig-no-access",),
    },
    "fx005": {
        "R0": ("sig-adopt-positive-new",),
        "R1": ("sig-adopt-positive-new",),
        "R2": ("sig-defer-positive-new",),
        "R3": ("sig-defer-positive-new",),
    },
    "fx006": {
        "R0": ("sig-adopt-negative-new",),
        "R1": ("sig-adopt-negative-new",),
        "R2": ("sig-defer-negative-new",),
        "R3": ("sig-defer-negative-new",),
    },
    "fx007": _all_models("sig-adopt-positive-new"),
    "fx008": _all_models("sig-adopt-negative-new"),
    "fx009": _all_models("sig-contested-new"),
    "fx010": _all_models("sig-contested-new"),
    "fx011": _all_models("sig-empty-access"),
    "fx012": _all_models("sig-empty-access"),
    "fx013": {
        model: ("sig-adopt-positive-new", "sig-noop") for model in MODELS
    },
    "fx014": {
        model: ("sig-adopt-negative-new", "sig-noop") for model in MODELS
    },
    "fx015": {
        "R0": (
            "sig-adopt-positive-new",
            "sig-noop",
            "sig-adopt-positive-existing",
        ),
        "R1": ("sig-no-access", "sig-noop", "sig-adopt-positive-new"),
        "R2": (
            "sig-defer-positive-new",
            "sig-noop",
            "sig-adopt-positive-existing",
        ),
        "R3": ("sig-no-access", "sig-noop", "sig-adopt-positive-new"),
    },
    "fx016": {
        "R0": (
            "sig-adopt-negative-new",
            "sig-noop",
            "sig-adopt-negative-existing",
        ),
        "R1": ("sig-no-access", "sig-noop", "sig-adopt-negative-new"),
        "R2": (
            "sig-defer-negative-new",
            "sig-noop",
            "sig-adopt-negative-existing",
        ),
        "R3": ("sig-no-access", "sig-noop", "sig-adopt-negative-new"),
    },
}


def _present_ref(key: str | None) -> dict[str, object]:
    if key is None:
        return deepcopy(MISSING_REF)
    return {"status": "present", "key": key}


def _component_max(
    profiles: tuple[dict[str, object], ...],
    axes: tuple[str, ...],
) -> dict[str, object]:
    return {
        axis: {
            "status": "present",
            "rank": max(profile[axis]["rank"] for profile in profiles),
        }
        for axis in axes
    }


def _strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            yield from _strings(item)


class InterpM1RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_bytes = EXECUTION_PATH.read_bytes()
        cls.execution = loads_exact(cls.execution_bytes)
        cls.contract = cls.execution["manifest"]["execution_contract"]
        cls.result_schema = load_exact(RESULT_SCHEMA_PATH)
        cls.run_schema = load_exact(RUN_SCHEMA_PATH)
        cls.run_envelope = runner.run_m1(cls.execution_bytes)
        cls.run_payload = cls.run_envelope["run"]
        cls.cells = {
            (cell["fixture_key"], cell["model_id"]): cell
            for cell in cls.run_payload["cells"]
        }
        cls.fixtures = {
            item["fixture_key"]: item
            for item in cls.contract["fixture_declarations"]
        }
        cls.models = {
            item["model_id"]: item for item in cls.contract["model_declarations"]
        }
        cls.materials = {
            item["material_key"]: item for item in cls.contract["materials"]
        }
        cls.profiles = {
            item["profile_key"]: item
            for item in cls.contract["source_encounter_profiles"]
        }
        cls.occurrences = {
            item["occurrence_key"]: item
            for item in cls.contract["source_occurrences"]
        }
        cls.topologies = {
            item["topology_key"]: item for item in cls.contract["topologies"]
        }
        cls.operators = {
            item["operator_id"]: item
            for item in cls.contract["operator_declarations"]
        }
        cls.views = {
            item["view_id"]: item
            for item in cls.contract["operator_input_views"]
        }

    def _access_evidence_keys(self, access: dict[str, object]) -> list[str]:
        result: list[str] = []
        if not access["present"]:
            return result
        for material_key in access["source_material_keys_ordered"]:
            material = self.materials[material_key]
            occurrence = self.occurrences[material["source_occurrence_key"]]
            key = occurrence["evidence_projection_key"]
            if key not in result:
                result.append(key)
        return result

    def _subjective_profile(self, material_keys: tuple[str, ...]) -> dict[str, object]:
        if not material_keys:
            return {
                key: deepcopy(value)
                for key, value in self.profiles["sp005"].items()
                if key != "profile_key"
            }
        profiles = tuple(
            {
                key: value
                for key, value in self.profiles[
                    self.materials[material_key]["source_encounter_profile_key"]
                ].items()
                if key != "profile_key"
            }
            for material_key in material_keys
        )
        return _component_max(profiles, SUBJECTIVE_AXES)

    def _raw_candidate(self, material_keys: tuple[str, ...]) -> dict[str, object]:
        profiles = tuple(
            {
                key: value
                for key, value in self.profiles[
                    self.materials[material_key]["source_encounter_profile_key"]
                ].items()
                if key != "profile_key"
            }
            for material_key in material_keys
        )
        raw = _component_max(profiles, DIRECTION_AXES)
        return {
            "raw_positive_support": raw["positive_direction_fit"],
            "raw_negative_support": raw["negative_direction_fit"],
            "raw_ambiguity": raw["ambiguity"],
        }

    def _normalized_fixture_edges(
        self,
        protocol_step: dict[str, object],
        material_keys: tuple[str, ...],
    ) -> list[dict[str, object]]:
        positions = {key: position for position, key in enumerate(material_keys)}
        result = []
        for edge in self.topologies[protocol_step["topology_key"]]["edges"]:
            left_key = edge["left_material_key"]
            right_key = edge["right_material_key"]
            if left_key not in positions or right_key not in positions:
                continue
            left, right = sorted((positions[left_key], positions[right_key]))
            result.append(
                {
                    "left_order": left,
                    "right_order": right,
                    "strength": deepcopy(edge["strength"]),
                }
            )
        result.sort(
            key=lambda edge: (
                edge["left_order"],
                edge["right_order"],
                canonical_bytes(edge["strength"]),
            )
        )
        return result

    def _lineage(
        self,
        access: dict[str, object],
        material_keys: tuple[str, ...],
    ) -> list[dict[str, object]]:
        source_keys: list[str] = []
        for material_key in material_keys:
            key = self.materials[material_key]["source_occurrence_key"]
            if key not in source_keys:
                source_keys.append(key)
        return [
            {
                "current_occurrence_key": access["current_occurrence_key"],
                "source_occurrence_keys_ordered": source_keys,
                "relation": (
                    "reexposure_to_prior_access_sources"
                    if access.get("reaccess_of_access_key") is not None
                    else "new_access_to_sources"
                ),
            }
        ]

    def _expected_semantic(
        self,
        fixture_key: str,
        protocol_step_index: int,
        signature: str,
    ) -> dict[str, object]:
        fixture = self.fixtures[fixture_key]
        protocol_step = fixture["protocol_steps"][protocol_step_index]
        evidence_keys = self._access_evidence_keys(protocol_step["access"])
        if signature == "sig-noop":
            return {
                "access_ordinal_delta": 0,
                "current_access_count_delta": 0,
                "encounter_count_delta": 0,
                "subjective_form_profile": deepcopy(MISSING_REF),
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
                "evidence_projection_keys_ordered": evidence_keys,
                "prior_prefix_relation": "unchanged",
            }

        access = protocol_step["access"]
        self.assertTrue(access["present"])
        material_keys = tuple(access["source_material_keys_ordered"])
        semantic: dict[str, object] = {
            "access_ordinal_delta": 1,
            "current_access_count_delta": 1,
            "encounter_count_delta": 1,
            "subjective_form_profile": self._subjective_profile(material_keys),
            "encounter_source_lineage": self._lineage(access, material_keys),
            "accessed_material_keys_ordered": [],
            "not_accessed_material_keys_ordered": [],
            "assemblies": [],
            "binding_candidates": [],
            "adjudications": [],
            "settlement_relations": [],
            "episode_integration_count": 0,
            "assembly_ignition_count": 0,
            "binding_ignition_count": 0,
            "evidence_projection_keys_ordered": evidence_keys,
            "prior_prefix_relation": "initial",
        }
        if signature == "sig-empty-access":
            self.assertEqual(material_keys, ())
            return semantic
        if signature == "sig-no-access":
            semantic["not_accessed_material_keys_ordered"] = list(material_keys)
            semantic["settlement_relations"] = [
                {"material_key": key, "relation": "not_accessed_currently"}
                for key in material_keys
            ]
            return semantic

        semantic["accessed_material_keys_ordered"] = list(material_keys)
        is_new = signature.endswith("-new")
        edges = self._normalized_fixture_edges(protocol_step, material_keys)
        semantic["assemblies"] = [
            {
                "memberships": [
                    {"material_key": key, "role": "member", "order": order}
                    for order, key in enumerate(material_keys)
                ],
                "induced_topology_edges": edges,
                "assembly_ignition_present": is_new,
            }
        ]
        raw = self._raw_candidate(material_keys)
        if signature.startswith("sig-adopt-positive"):
            eligible = ["positive"]
            outcome = "adopted_positive"
            integrated = 1
        elif signature.startswith("sig-adopt-negative"):
            eligible = ["negative"]
            outcome = "adopted_negative"
            integrated = 1
        elif signature.startswith("sig-defer-"):
            eligible = []
            outcome = "deferred"
            integrated = 0
        elif signature == "sig-contested-new":
            eligible = ["negative", "positive"]
            outcome = "contested"
            integrated = 0
        else:
            self.fail(f"unknown frozen signature: {signature}")
        semantic["binding_candidates"] = [
            {**raw, "eligible_directions": eligible}
        ]
        semantic["adjudications"] = [{"outcome": outcome}]
        semantic["episode_integration_count"] = integrated
        semantic["assembly_ignition_count"] = int(is_new)
        semantic["binding_ignition_count"] = integrated
        if access["access_ordinal"] > 1:
            semantic["prior_prefix_relation"] = (
                "extended" if is_new else "unchanged"
            )
        if not integrated:
            semantic["settlement_relations"] = [
                {
                    "material_key": key,
                    "relation": "assembled_without_adopted_binding",
                }
                for key in material_keys
            ]
        return semantic

    def _expected_transport_audit(
        self,
        protocol_step: dict[str, object],
    ) -> dict[str, object]:
        access = protocol_step["access"]
        redelivery = protocol_step.get("transport_redelivery")
        if access["present"]:
            return {
                "access_present": True,
                "transport_redelivery_present": False,
                "access_key": _present_ref(access["access_key"]),
                "current_occurrence_key": _present_ref(
                    access["current_occurrence_key"]
                ),
                "current_delivery_key": _present_ref(access["current_delivery_key"]),
                "transport_delivery_key": _present_ref(None),
                "redelivery_of_delivery_key": _present_ref(None),
                "reaccess_of_access_key": _present_ref(
                    access.get("reaccess_of_access_key")
                ),
                "reexposure_of_occurrence_key": _present_ref(
                    access.get("reexposure_of_occurrence_key")
                ),
            }
        return {
            "access_present": False,
            "transport_redelivery_present": redelivery is not None,
            "access_key": _present_ref(None),
            "current_occurrence_key": _present_ref(
                redelivery["occurrence_key"] if redelivery else None
            ),
            "current_delivery_key": _present_ref(None),
            "transport_delivery_key": _present_ref(
                redelivery["delivery_key"] if redelivery else None
            ),
            "redelivery_of_delivery_key": _present_ref(
                redelivery["redelivery_of_delivery_key"] if redelivery else None
            ),
            "reaccess_of_access_key": _present_ref(None),
            "reexposure_of_occurrence_key": _present_ref(None),
        }

    def test_complete_matrix_step_count_schema_and_determinism(self) -> None:
        self.assertEqual(len(self.run_payload["cells"]), 64)
        self.assertEqual(
            sum(len(cell["steps"]) for cell in self.run_payload["cells"]), 88
        )
        self.assertEqual(len(self.cells), 64)
        expected_cell_order = [
            (fixture_key, model_id)
            for fixture_key in self.contract["execution_matrix"]["fixture_keys"]
            for model_id in self.contract["execution_matrix"]["model_ids"]
        ]
        self.assertEqual(
            [
                (cell["fixture_key"], cell["model_id"])
                for cell in self.run_payload["cells"]
            ],
            expected_cell_order,
        )
        for cell in self.run_payload["cells"]:
            validate_json_schema(cell, self.result_schema)
        validate_json_schema(self.run_envelope, self.run_schema)
        repeated = runner.run_m1(self.execution_bytes)
        self.assertEqual(repeated, self.run_envelope)
        self.assertEqual(
            runner.encode_run(repeated),
            canonical_bytes(repeated) + b"\n",
        )
        self.assertEqual(loads_exact(runner.encode_run(repeated)), repeated)
        self.assertEqual(
            self.run_envelope["integrity"]["run_sha256"], digest(self.run_payload)
        )
        self.assertEqual(
            self.run_payload["runner_implementation_sha256"],
            file_sha256(RUNNER_PATH),
        )
        self.assertEqual(
            self.run_payload["runner_bundle_sha256"],
            digest(
                [
                    {
                        "path": "dynamics/labs/interp_m1_common.py",
                        "sha256": file_sha256(COMMON_PATH),
                    },
                    {
                        "path": "dynamics/labs/interp_m1_runner.py",
                        "sha256": file_sha256(RUNNER_PATH),
                    },
                    {
                        "path": "dynamics/labs/interp_m1_run_cli.py",
                        "sha256": file_sha256(RUN_CLI_PATH),
                    },
                    {
                        "path": "dynamics/labs/interp_m1_cli.py",
                        "sha256": file_sha256(CLI_PATH),
                    },
                ]
            ),
        )
        self.assertEqual(
            self.run_payload["fixed_factor_sha256"],
            digest(self.contract["fixed_factors"]),
        )
        self.assertEqual(
            self.run_payload["execution_manifest_sha256"],
            self.execution["integrity"]["manifest_sha256"],
        )
        self.assertEqual(
            self.run_payload["execution_contract_sha256"],
            self.execution["integrity"]["contract_sha256"],
        )
        self.assertEqual(
            self.run_payload["runner_input_kind"], "execution_manifest_only"
        )
        self.assertIs(self.run_payload["evaluation_manifest_visible"], False)

    def test_all_f1_through_f8_cells_have_exact_closed_semantics(self) -> None:
        self.assertEqual(set(EXPECTED_SIGNATURES), set(self.fixtures))
        for fixture_key, expected_by_model in EXPECTED_SIGNATURES.items():
            for model_id, signatures in expected_by_model.items():
                cell = self.cells[(fixture_key, model_id)]
                self.assertEqual(len(cell["steps"]), len(signatures))
                for index, signature in enumerate(signatures):
                    with self.subTest(
                        fixture=fixture_key,
                        model=model_id,
                        step=index + 1,
                        signature=signature,
                    ):
                        self.assertEqual(
                            cell["steps"][index]["semantic"],
                            self._expected_semantic(fixture_key, index, signature),
                        )

    def test_transport_audit_lineage_redelivery_reaccess_and_prefix(self) -> None:
        for fixture_key, fixture in self.fixtures.items():
            for model_id in MODELS:
                cell = self.cells[(fixture_key, model_id)]
                for index, protocol_step in enumerate(fixture["protocol_steps"]):
                    self.assertEqual(
                        cell["steps"][index]["transport_access_audit"],
                        self._expected_transport_audit(protocol_step),
                    )

        for fixture_key, prior_occurrence, prior_delivery, redelivery, reaccess in (
            ("fx015", "co015", "cd015", "cd016", "a015"),
            ("fx016", "co017", "cd018", "cd019", "a017"),
        ):
            for model_id in MODELS:
                steps = self.cells[(fixture_key, model_id)]["steps"]
                redelivery_audit = steps[1]["transport_access_audit"]
                self.assertEqual(
                    redelivery_audit["current_occurrence_key"],
                    _present_ref(prior_occurrence),
                )
                self.assertEqual(
                    redelivery_audit["transport_delivery_key"],
                    _present_ref(redelivery),
                )
                self.assertEqual(
                    redelivery_audit["redelivery_of_delivery_key"],
                    _present_ref(prior_delivery),
                )
                self.assertEqual(steps[1]["semantic"]["prior_prefix_relation"], "unchanged")
                reaccess_audit = steps[2]["transport_access_audit"]
                self.assertEqual(
                    reaccess_audit["reaccess_of_access_key"], _present_ref(reaccess)
                )
                self.assertEqual(
                    steps[2]["semantic"]["prior_prefix_relation"],
                    "extended" if model_id in {"R1", "R3"} else "unchanged",
                )
                self.assertEqual(
                    steps[0]["semantic"]["encounter_source_lineage"][0][
                        "source_occurrence_keys_ordered"
                    ],
                    steps[2]["semantic"]["encounter_source_lineage"][0][
                        "source_occurrence_keys_ordered"
                    ],
                )
                self.assertEqual(
                    steps[2]["semantic"]["encounter_source_lineage"][0]["relation"],
                    "reexposure_to_prior_access_sources",
                )

        expected_reaccess_ignition = {"R0": 0, "R1": 1, "R2": 0, "R3": 1}
        for fixture_key in ("fx015", "fx016"):
            for model_id, expected in expected_reaccess_ignition.items():
                self.assertEqual(
                    self.cells[(fixture_key, model_id)]["steps"][2]["semantic"][
                        "assembly_ignition_count"
                    ],
                    expected,
                )

    def test_operator_logs_are_active_only_and_follow_phase_order(self) -> None:
        phase_order = self.contract["phase_contract"]["phase_order"]
        phase_index = {phase: index for index, phase in enumerate(phase_order)}
        for (fixture_key, model_id), cell in self.cells.items():
            expected_ids = self.models[model_id]["ordered_operator_refs"]
            self.assertEqual(len(expected_ids), 9)
            fixture = self.fixtures[fixture_key]
            for index, step_result in enumerate(cell["steps"]):
                log = step_result["operator_invocations"]
                self.assertEqual([row["operator_id"] for row in log], expected_ids)
                expected_count = int(fixture["protocol_steps"][index]["access"]["present"])
                self.assertEqual(
                    [row["invocation_count"] for row in log],
                    [expected_count] * 9,
                )
                self.assertEqual(
                    [phase_index[row["phase"]] for row in log],
                    sorted(phase_index[row["phase"]] for row in log),
                )
                for row in log:
                    declaration = self.operators[row["operator_id"]]
                    view = self.views[declaration["input_view_id"]]
                    self.assertEqual(row["input_view_id"], view["view_id"])
                    self.assertEqual(
                        row["inspected_fields"],
                        [
                            field["field_id"]
                            for field in view["fields"]
                            if field["operator_use"] == "inspect"
                        ],
                    )
                    self.assertEqual(
                        row["pass_through_fields"],
                        [
                            field["field_id"]
                            for field in view["fields"]
                            if field["operator_use"] == "pass_through_only"
                        ],
                    )

    def test_operator_api_and_runtime_calls_never_receive_raw_identity_keys(self) -> None:
        expected_parameters = {
            "_op001_encounter": ("source_profiles", "neutral_profile"),
            "_op002_access": ("material_profiles", "relevant_flags"),
            "_op003_access": ("material_profiles", "relevant_flags", "reception"),
            "_op004_assemblies": ("accessible_positions", "position_edges"),
            "_op005_candidate": ("member_profiles",),
            "_op006_eligible": ("candidate",),
            "_op007_eligible": (
                "candidate",
                "reception",
                "member_profiles",
                "member_edges",
            ),
            "_op008_adjudicate": ("directions",),
            "_op009_integrate": ("outcome",),
            "_op010_assembly_ignition": (
                "current_pairs",
                "prior_pairs",
                "frozen_edge_present",
            ),
            "_op011_binding_ignition": ("outcome", "integration_present"),
        }
        for name, parameters in expected_parameters.items():
            self.assertEqual(
                tuple(inspect.signature(getattr(runner, name)).parameters), parameters
            )

        raw_ids: set[str] = set()
        for profile in self.contract["source_encounter_profiles"]:
            raw_ids.add(profile["profile_key"])
        for profile in self.contract["reception_profiles"]:
            raw_ids.add(profile["profile_key"])
        for material in self.contract["materials"]:
            raw_ids.add(material["material_key"])
        for occurrence in self.contract["source_occurrences"]:
            raw_ids.add(occurrence["occurrence_key"])
        for topology in self.contract["topologies"]:
            raw_ids.add(topology["topology_key"])
        for fixture in self.contract["fixture_declarations"]:
            raw_ids.update(
                {
                    fixture["fixture_key"],
                    fixture["isolated_ledger_key"],
                    fixture["actor_key"],
                    fixture["interpreted_target_scope_key"],
                    fixture["target_form_fixture_key"],
                    fixture["ghost_fixture_key"],
                }
            )
            for protocol_step in fixture["protocol_steps"]:
                access = protocol_step["access"]
                if access["present"]:
                    raw_ids.update(
                        {
                            access["access_key"],
                            access["current_occurrence_key"],
                            access["current_delivery_key"],
                        }
                    )
                if "transport_redelivery" in protocol_step:
                    redelivery = protocol_step["transport_redelivery"]
                    raw_ids.update(
                        {
                            redelivery["occurrence_key"],
                            redelivery["delivery_key"],
                            redelivery["redelivery_of_delivery_key"],
                        }
                    )
        raw_ids.update(self.models)
        raw_ids.update(self.operators)
        raw_ids.update(self.views)

        mocks = {}
        with ExitStack() as stack:
            for name in expected_parameters:
                mocks[name] = stack.enter_context(
                    patch.object(runner, name, wraps=getattr(runner, name))
                )
            runner.run_m1(self.execution_bytes)
        for name, mock in mocks.items():
            self.assertGreater(mock.call_count, 0, name)
            for call in mock.call_args_list:
                observed = set(_strings(call.args)) | set(_strings(call.kwargs))
                self.assertFalse(observed & raw_ids, (name, observed & raw_ids))

    def test_guard_digests_are_real_recomputed_before_after_projections(self) -> None:
        expected_projection = {
            "action_occurrences": [],
            "authority_outputs": [],
            "evidence_assessment": [],
            "evidence_links": [],
            "narrative_writes": [],
            "observation_artifacts": [],
            "source_encounters": self.contract["source_encounter_profiles"],
            "source_materials": self.contract["materials"],
            "source_occurrences": self.contract["source_occurrences"],
            "world_outcomes": [],
        }
        self.assertEqual(runner._guard_projection(self.contract), expected_projection)
        expected_names = set(self.contract["output_guard_contract"]["guard_ledger_names"])
        self.assertEqual(set(expected_projection), expected_names)
        for cell in self.run_payload["cells"]:
            for step in cell["steps"]:
                guards = step["guard_ledgers"]
                self.assertEqual(set(guards), expected_names)
                for name, projection in expected_projection.items():
                    expected_digest = digest(projection)
                    self.assertEqual(guards[name]["before_sha256"], expected_digest)
                    self.assertEqual(guards[name]["after_sha256"], expected_digest)
                    self.assertEqual(guards[name]["delta_count"], 0)

        original = runner._guard_projection
        calls = 0

        def changes_between_reads(contract):
            nonlocal calls
            projection = deepcopy(original(contract))
            calls += 1
            if calls == 2:
                projection["source_materials"].append({"mutation": "after"})
            return projection

        with patch.object(runner, "_guard_projection", side_effect=changes_between_reads):
            with self.assertRaisesRegex(
                runner.FrozenExecutionError, "guard projection changed"
            ):
                runner.run_m1(self.execution_bytes)
        self.assertEqual(calls, 2)

    def test_evaluation_manifest_poison_or_absence_cannot_affect_runner(self) -> None:
        original_read_bytes = Path.read_bytes
        for mode in ("poison", "missing"):
            touched: list[Path] = []

            def guarded_read_bytes(path: Path, *, _mode=mode):
                if path.name == EVALUATION_PATH.name:
                    touched.append(path)
                    if _mode == "missing":
                        raise FileNotFoundError(path)
                    return b'{"poison":true}'
                return original_read_bytes(path)

            with self.subTest(mode=mode), patch.object(
                Path, "read_bytes", guarded_read_bytes
            ):
                self.assertEqual(
                    runner.run_m1(self.execution_bytes), self.run_envelope
                )
            self.assertEqual(touched, [])

    def test_assembly_normalization_and_content_digest_are_deterministic(self) -> None:
        for cell in self.run_payload["cells"]:
            for step in cell["steps"]:
                for assembly in step["semantic"]["assemblies"]:
                    memberships = assembly["memberships"]
                    self.assertEqual(
                        [item["order"] for item in memberships],
                        list(range(len(memberships))),
                    )
                    self.assertEqual(
                        len({item["material_key"] for item in memberships}),
                        len(memberships),
                    )
                    edge_keys = []
                    for edge in assembly["induced_topology_edges"]:
                        self.assertLess(edge["left_order"], edge["right_order"])
                        edge_keys.append(
                            (
                                edge["left_order"],
                                edge["right_order"],
                                canonical_bytes(edge["strength"]),
                            )
                        )
                    self.assertEqual(edge_keys, sorted(edge_keys))
                    self.assertEqual(len(edge_keys), len(set(edge_keys)))

        self.assertEqual(
            [
                item["material_key"]
                for item in self.cells[("fx009", "R0")]["steps"][0]["semantic"][
                    "assemblies"
                ][0]["memberships"]
            ],
            ["m001", "m003"],
        )
        self.assertEqual(
            [
                item["material_key"]
                for item in self.cells[("fx010", "R0")]["steps"][0]["semantic"][
                    "assemblies"
                ][0]["memberships"]
            ],
            ["m003", "m001"],
        )

        fixture = self.fixtures["fx015"]
        first_access = fixture["protocol_steps"][0]["access"]
        later_access = fixture["protocol_steps"][2]["access"]
        membership_keys = ("m001", "m002")
        edges = ((0, 1, deepcopy(self.topologies["t001"]["edges"][0]["strength"])),)
        content_digest = runner._detached_assembly_content_digest(
            fixture,
            first_access,
            membership_keys,
            edges,
            self.operators["op004"],
        )
        self.assertEqual(
            content_digest,
            runner._detached_assembly_content_digest(
                deepcopy(fixture),
                deepcopy(first_access),
                tuple(membership_keys),
                deepcopy(edges),
                deepcopy(self.operators["op004"]),
            ),
        )
        self.assertRegex(content_digest, r"^[0-9a-f]{64}$")
        self.assertNotEqual(
            content_digest,
            runner._detached_assembly_content_digest(
                fixture,
                later_access,
                membership_keys,
                edges,
                self.operators["op004"],
            ),
        )
        self.assertNotEqual(
            content_digest,
            runner._detached_assembly_content_digest(
                fixture,
                first_access,
                tuple(reversed(membership_keys)),
                edges,
                self.operators["op004"],
            ),
        )
        self.assertEqual(
            digest(self.operators["op004"]),
            "65daa0a3483434b24c78d95065ea04ad225499d2b8fdabfab50254269bf8604f",
        )

    def test_cell_state_and_returned_mutables_are_isolated(self) -> None:
        expected = {"R0": 0, "R1": 1, "R2": 0, "R3": 1}
        for fixture_key in ("fx015", "fx016"):
            self.assertEqual(
                {
                    model: self.cells[(fixture_key, model)]["steps"][2]["semantic"][
                        "assembly_ignition_count"
                    ]
                    for model in MODELS
                },
                expected,
            )

        mutated = runner.run_m1(self.execution_bytes)
        mutated_cells = {
            (cell["fixture_key"], cell["model_id"]): cell
            for cell in mutated["run"]["cells"]
        }
        control_before = deepcopy(
            mutated_cells[("fx015", "R1")]["steps"][0]["semantic"]
        )
        mutated_cells[("fx015", "R0")]["steps"][0]["semantic"][
            "accessed_material_keys_ordered"
        ].append("poison")
        self.assertEqual(
            mutated_cells[("fx015", "R1")]["steps"][0]["semantic"],
            control_before,
        )
        self.assertEqual(runner.run_m1(self.execution_bytes), self.run_envelope)

    def test_frozen_digest_corruption_and_retuned_rehash_are_rejected(self) -> None:
        corrupt = deepcopy(self.execution)
        corrupt["manifest"]["execution_contract"]["reception_profiles"][0][
            "positive_direction_receptivity"
        ]["rank"] = 1
        with self.assertRaisesRegex(
            runner.FrozenExecutionError, "integrity mismatch"
        ):
            runner.run_m1(canonical_bytes(corrupt))

        retuned = deepcopy(corrupt)
        retuned["integrity"]["manifest_sha256"] = digest(retuned["manifest"])
        retuned["integrity"]["contract_sha256"] = digest(
            retuned["manifest"]["execution_contract"]
        )
        with self.assertRaisesRegex(
            runner.FrozenExecutionError, "not the frozen M1 v1"
        ):
            runner.run_m1(canonical_bytes(retuned))

    def test_boolean_is_not_accepted_as_an_ordinal_integer(self) -> None:
        with self.assertRaisesRegex(
            runner.FrozenExecutionError, "invalid ordinal component"
        ):
            runner._rank({"status": "present", "rank": True})
        with self.assertRaisesRegex(ValueError, "schema type mismatch"):
            validate_json_schema(True, {"type": "integer"})
        invalid_cell = deepcopy(self.run_payload["cells"][0])
        invalid_cell["steps"][0]["semantic"]["access_ordinal_delta"] = True
        with self.assertRaisesRegex(ValueError, "schema enum mismatch"):
            validate_json_schema(invalid_cell, self.result_schema)

    def test_missingness_is_axis_local_ordered_and_never_zero_imputed(self) -> None:
        first = {
            "positive_direction_fit": {
                "status": "missing",
                "reason": "not_applicable",
            },
            "negative_direction_fit": {"status": "present", "rank": 2},
            "ambiguity": {"status": "present", "rank": 0},
            "activation": {"status": "present", "rank": 1},
        }
        second = {
            "positive_direction_fit": {
                "status": "missing",
                "reason": "source_unresolved",
            },
            "negative_direction_fit": {
                "status": "missing",
                "reason": "withheld_control",
            },
            "ambiguity": {"status": "present", "rank": 2},
            "activation": {"status": "present", "rank": 2},
        }
        result = runner._componentwise_max((first, second), SUBJECTIVE_AXES)
        self.assertEqual(
            result["positive_direction_fit"],
            {"status": "missing", "reason": "source_unresolved"},
        )
        self.assertEqual(
            result["negative_direction_fit"],
            {"status": "missing", "reason": "withheld_control"},
        )
        self.assertEqual(result["ambiguity"], {"status": "present", "rank": 2})
        self.assertEqual(result["activation"], {"status": "present", "rank": 2})
        self.assertNotIn("rank", result["positive_direction_fit"])

        invalid_reason = deepcopy(first)
        invalid_reason["positive_direction_fit"]["reason"] = "invented_reason"
        with self.assertRaisesRegex(runner.FrozenExecutionError, "invalid missing reason"):
            runner._componentwise_max((invalid_reason,), SUBJECTIVE_AXES)

        missing_activation = deepcopy(first)
        missing_activation["activation"] = {
            "status": "missing",
            "reason": "source_unresolved",
        }
        with self.assertRaisesRegex(runner.FrozenExecutionError, "missing component"):
            runner._op002_access((missing_activation,), (True,))
        candidate = {
            "raw_positive_support": {
                "status": "missing",
                "reason": "operator_undefined",
            },
            "raw_negative_support": {"status": "present", "rank": 0},
            "raw_ambiguity": {"status": "present", "rank": 0},
        }
        with self.assertRaisesRegex(runner.FrozenExecutionError, "missing component"):
            runner._op006_eligible(candidate)

    def test_runner_ast_has_no_evaluator_or_runtime_model_dependency(self) -> None:
        source = RUNNER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_modules: set[str] = set()
        dynamic_import_calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "__import__":
                    dynamic_import_calls.append(node)
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "import_module"
                ):
                    dynamic_import_calls.append(node)
        dynamics_imports = {
            module for module in imported_modules if module.startswith("dynamics")
        }
        self.assertEqual(
            dynamics_imports, {"dynamics.labs.interp_m1_common"}
        )
        forbidden_fragments = {
            "evaluator",
            "dynamics.engine",
            "dynamics.models",
            "dynamics.routing",
            "dynamics.epistemics",
            "dynamics.mental_transitions",
        }
        for module in imported_modules:
            self.assertFalse(
                any(fragment in module for fragment in forbidden_fragments), module
            )
        self.assertEqual(dynamic_import_calls, [])
        self.assertNotIn(EVALUATION_PATH.name, source)
        self.assertEqual(tuple(inspect.signature(runner.run_m1).parameters), (
            "execution_manifest_bytes",
        ))


if __name__ == "__main__":
    unittest.main()
