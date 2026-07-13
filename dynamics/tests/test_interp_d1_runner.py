from __future__ import annotations

import ast
from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from dynamics.labs import interp_d1_runner as runner
from dynamics.labs.interp_d1_common import (
    FrozenD1ExecutionError,
    canonical_bytes,
    digest,
    digest_without_nested_member,
    file_sha256,
    load_exact,
    loads_exact,
    validate_json_schema,
)


ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS = ROOT / "research" / "benchmarks"
EXECUTION_PATH = BENCHMARKS / "interp-001d1-v1-execution.json"
EVALUATION_PATH = BENCHMARKS / "interp-001d1-v1-evaluation.json"
RESULT_SCHEMA_PATH = BENCHMARKS / "interp-001d1-v1-result.schema.json"
RUN_SCHEMA_PATH = BENCHMARKS / "interp-001d1-v1-run.schema.json"


def _pointer(value: object, path: str) -> object:
    current = value
    for segment in path.lstrip("/").split("/"):
        if not isinstance(current, dict):
            raise AssertionError(f"path does not resolve: {path}")
        current = current[segment]
    return current


class InterpD1RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_bytes = EXECUTION_PATH.read_bytes()
        cls.execution = loads_exact(cls.execution_bytes)
        cls.contract = cls.execution["manifest"]["execution_contract"]
        cls.evaluation = load_exact(EVALUATION_PATH)["manifest"][
            "evaluation_contract"
        ]
        cls.result_schema = load_exact(RESULT_SCHEMA_PATH)
        cls.run_schema = load_exact(RUN_SCHEMA_PATH)
        cls.run_document = runner.run_d1(cls.execution_bytes)

    def test_exact_88_cell_run_conforms_to_frozen_schemas_and_bindings(self) -> None:
        self.assertEqual(self.run_document["run_id"], "INTERP-001D1-V1-RUN-001")
        self.assertEqual(self.run_document["runner_input_kind"], "execution_manifest_only")
        self.assertFalse(self.run_document["evaluation_manifest_visible"])
        self.assertEqual(
            Counter(cell["block_id"] for cell in self.run_document["cells"]),
            Counter({"SOURCE_COMPILER": 24, "ENCOUNTER_FORMATION": 32, "GHOST_PATH": 32}),
        )
        expected_keys = [
            f"{matrix['block_id']}:{fixture}:{model}"
            for matrix in self.contract["execution_matrices"]
            for fixture in matrix["fixture_keys"]
            for model in matrix["model_ids"]
        ]
        self.assertEqual([cell["cell_key"] for cell in self.run_document["cells"]], expected_keys)
        self.assertEqual(len(expected_keys), len(set(expected_keys)))
        for cell in self.run_document["cells"]:
            validate_json_schema(cell, self.result_schema)
            self.assertEqual(
                cell["integrity"]["cell_content_sha256"],
                digest_without_nested_member(cell, "integrity", "cell_content_sha256"),
            )
        validate_json_schema(
            self.run_document,
            self.run_schema,
            external_schemas={
                "./interp-001d1-v1-result.schema.json": self.result_schema
            },
        )
        self.assertEqual(
            self.run_document["integrity"]["run_sha256"],
            digest_without_nested_member(self.run_document, "integrity", "run_sha256"),
        )
        self.assertEqual(self.run_document["execution_manifest_sha256"], runner.EXECUTION_MANIFEST_SHA256)
        self.assertEqual(self.run_document["execution_contract_sha256"], runner.EXECUTION_CONTRACT_SHA256)
        self.assertEqual(self.run_document["result_schema_sha256"], file_sha256(RESULT_SCHEMA_PATH))

    def test_all_88_cells_match_frozen_test_only_semantic_signatures(self) -> None:
        signatures = {
            item["signature_id"]: item
            for item in self.evaluation["semantic_signatures"]
        }
        expected = {
            (assertion["block_id"], assertion["fixture_key"], model_id): signature_id
            for assertion in self.evaluation["cell_assertions"]
            for model_id, signature_id in assertion["expected_by_model"].items()
        }
        self.assertEqual(len(expected), 88)
        for cell in self.run_document["cells"]:
            signature = signatures[
                expected[(cell["block_id"], cell["fixture_key"], cell["model_id"])]
            ]
            for relation in signature["expected_relations"]:
                actual = _pointer(cell, relation["path"])
                if relation["predicate"] == "set_eq":
                    self.assertEqual(
                        {canonical_bytes(item) for item in actual},
                        {canonical_bytes(item) for item in relation["value"]},
                        (cell["cell_key"], relation["path"]),
                    )
                else:
                    self.assertEqual(
                        canonical_bytes(actual),
                        canonical_bytes(relation["value"]),
                        (cell["cell_key"], relation["path"]),
                    )

    def test_execution_and_encoding_are_byte_reproducible(self) -> None:
        second = runner.run_d1(self.execution_bytes)
        self.assertEqual(self.run_document, second)
        self.assertEqual(runner.encode_run(self.run_document), runner.encode_run(second))
        self.assertEqual(loads_exact(runner.encode_run(self.run_document)), self.run_document)

    def test_runner_never_reads_evaluation_or_result_expectations(self) -> None:
        original = Path.read_bytes

        def guarded(path: Path) -> bytes:
            if "evaluation" in path.name or "conformance" in path.name:
                raise AssertionError(f"runner attempted evaluator read: {path}")
            return original(path)

        with patch.object(Path, "read_bytes", guarded):
            guarded_run = runner.run_d1(self.execution_bytes)
        self.assertEqual(guarded_run, self.run_document)

    def test_every_operator_receives_exactly_its_frozen_input_view(self) -> None:
        declarations = {
            item["operator_id"]: item for item in self.contract["operator_declarations"]
        }
        adjudicator = self.contract["adjudicator_contract"]
        expected = {
            operator_id: set(item["exact_inspected_field_ids"])
            | set(item["exact_opaque_pass_through_field_ids"])
            for operator_id, item in declarations.items()
        }
        expected[adjudicator["policy_id"]] = set(adjudicator["exact_inspected_field_ids"])
        observed: dict[str, list[set[str]]] = defaultdict(list)
        replacements = {}
        for operator_id, implementation in runner.OPERATOR_REGISTRY.items():
            def wrapper(inputs, *, _id=operator_id, _impl=implementation):
                observed[_id].append(set(inputs))
                return _impl(inputs)
            replacements[operator_id] = wrapper
        with patch.dict(runner.OPERATOR_REGISTRY, replacements, clear=True):
            runner.run_d1(self.execution_bytes)
        self.assertEqual(set(observed), set(expected))
        for operator_id, invocations in observed.items():
            self.assertTrue(invocations)
            self.assertTrue(all(fields == expected[operator_id] for fields in invocations))

    def test_ghost_close_receives_declared_candidate_state_list(self) -> None:
        observed: list[list[dict[str, object]]] = []
        implementation = runner.OPERATOR_REGISTRY["close_ghost_semantic"]

        def inspect_close(inputs):
            states = inputs["candidate_state_stage_receipts"]
            observed.append(deepcopy(states))
            return implementation(inputs)

        with patch.dict(
            runner.OPERATOR_REGISTRY,
            {"close_ghost_semantic": inspect_close},
        ):
            runner.run_d1(self.execution_bytes)
        self.assertEqual(len(observed), 32)
        for states in observed:
            self.assertTrue(states)
            self.assertTrue(all("stage_receipts" in state for state in states))
            self.assertEqual(len(states[-1]["stage_receipts"]), len(states))
            for prior, current in zip(states, states[1:]):
                self.assertEqual(
                    current["stage_receipts"][:-1], prior["stage_receipts"]
                )

    def test_raw_fixture_binding_map_is_complete_and_has_no_extra_authority(self) -> None:
        declared = {
            (binding["operator_id"], field_id)
            for binding in self.contract["operator_typed_dataflow_contract"]["raw_input_bindings"]
            for field_id in binding["field_ids"]
        }
        self.assertEqual(declared, set(runner.RAW_FIXTURE_BINDINGS))
        self.assertEqual(
            runner.RAW_FIXTURE_BINDINGS[
                ("apply_reception_eligibility", "reception_profile")
            ],
            ("declared_reception_intervention",),
        )
        self.assertEqual(
            runner.RAW_FIXTURE_BINDINGS[
                ("apply_target_directional_compatibility", "target_form_profile")
            ],
            ("declared_target_form_intervention",),
        )

    def test_source_order_scope_future_and_contested_controls(self) -> None:
        cells = {cell["cell_key"]: cell for cell in self.run_document["cells"]}
        reversed_order = cells["SOURCE_COMPILER:srcfx002:TF2"]["semantic"]
        self.assertEqual(reversed_order["eligible_source_positions_ordered"], [4, 0])
        prefix_left = cells["SOURCE_COMPILER:srcfx007:TF2"]["semantic"]
        prefix_right = cells["SOURCE_COMPILER:srcfx008:TF2"]["semantic"]
        self.assertEqual(prefix_left, prefix_right)
        contested = cells["SOURCE_COMPILER:srcfx003:TF1"]["semantic"]
        self.assertTrue(contested["contested_present"])
        self.assertEqual(
            contested["target_form_readout_profile"],
            {
                "positive_direction_support": {"status": "present", "rank": 2},
                "negative_direction_support": {"status": "present", "rank": 1},
            },
        )
        withheld = cells["SOURCE_COMPILER:srcfx006:TF2"]["semantic"]
        self.assertEqual(withheld["accessibility_relation"], "all_withheld")
        self.assertNotIn("implicit_plastic_trace_fixture", withheld["source_kinds_used"])

    def test_formation_missing_scope_and_operator_order_controls(self) -> None:
        cells = {cell["cell_key"]: cell for cell in self.run_document["cells"]}
        no_access = cells["ENCOUNTER_FORMATION:encfx007:ERT"]["semantic"]
        self.assertFalse(no_access["encounter_emitted"])
        self.assertEqual(
            no_access["formed_encounter_profile"],
            {"status": "missing", "reason": "no_current_access"},
        )
        self.assertFalse(no_access["reception_intervention_used"])
        self.assertFalse(no_access["target_form_intervention_used"])
        source_free = cells["ENCOUNTER_FORMATION:encfx008:ERT"]["semantic"]
        self.assertEqual(
            source_free["formed_encounter_profile"],
            {"status": "missing", "reason": "no_source_material"},
        )
        scope_mismatch = cells["ENCOUNTER_FORMATION:encfx005:ERT"]["semantic"]
        self.assertTrue(scope_mismatch["reception_intervention_used"])
        self.assertFalse(scope_mismatch["target_form_intervention_used"])
        self.assertEqual(
            cells["ENCOUNTER_FORMATION:encfx001:ERT"]["semantic"]["formation_operator_order"],
            [
                "base_profile",
                "apply_target_directional_compatibility",
                "apply_reception_eligibility",
                "emit_proxy",
            ],
        )

    def test_ghost_traversal_inactive_scope_and_truth_table_controls(self) -> None:
        cells = {cell["cell_key"]: cell for cell in self.run_document["cells"]}
        self.assertEqual(
            cells["GHOST_PATH:ghfx001:G0"]["semantic"]["visited_material_positions_ordered"],
            [0, 1, 3, 2],
        )
        scope_mismatch = cells["GHOST_PATH:ghfx006:GTP"]["semantic"]
        self.assertFalse(scope_mismatch["target_guidance_used"])
        self.assertTrue(scope_mismatch["ghost_program_used"])
        self.assertEqual(
            scope_mismatch["candidate_projection"]["binding_candidate_directions"],
            ["positive"],
        )
        for fixture in ("ghfx007", "ghfx008"):
            inactive = cells[f"GHOST_PATH:{fixture}:GTP"]
            semantic = inactive["semantic"]
            self.assertFalse(semantic["target_guidance_used"])
            self.assertFalse(semantic["ghost_program_used"])
            self.assertEqual(semantic["candidate_projection"]["binding_candidate_directions"], [])
            self.assertEqual(semantic["candidate_projection"]["registered_operation_relations"], [])
            traced = [item["operator_id"] for item in inactive["operator_trace"]]
            self.assertIn("confirmation_only", traced)
            self.assertIn("rehearsal", traced)
            self.assertIn("apply_target_candidate_eligibility", traced)
        truth = {
            (): ("none", "deferred"),
            ("negative",): ("single_direction", "adopted_negative"),
            ("positive",): ("single_direction", "adopted_positive"),
            ("negative", "positive"): ("contested", "contested"),
        }
        for cell in self.run_document["cells"]:
            if cell["block_id"] != "GHOST_PATH":
                continue
            semantic = cell["semantic"]
            candidate = semantic["candidate_projection"]
            expected_relation, expected_outcome = truth[
                tuple(candidate["binding_candidate_directions"])
            ]
            self.assertEqual(candidate["binding_relation"], expected_relation)
            self.assertEqual(
                semantic["adjudication_projection"]["adjudication_outcome"],
                expected_outcome,
            )

    def test_detached_guards_are_fresh_empty_and_unchanged(self) -> None:
        empty_sha = digest([])
        expected_names = set(self.contract["output_guard_contract"]["guard_ledger_names"])
        for cell in self.run_document["cells"]:
            self.assertEqual(set(cell["guard_ledgers"]), expected_names)
            self.assertTrue(
                all(
                    ledger == {"before_sha256": empty_sha, "after_sha256": empty_sha}
                    for ledger in cell["guard_ledgers"].values()
                )
            )

    def test_strict_parser_rejects_noncanonical_domains_before_execution(self) -> None:
        invalid_documents = (
            b'{"a":1,"a":2}',
            b'{"a":null}',
            b'{"a":1.0}',
            b'{"a":9007199254740992}',
            b'{"a":-0}',
            b'{"a":"\\ud800"}',
            b'{"a":"\\udfff"}',
            b'{"a":' + (b"9" * 5000) + b"}",
            '{"a":"e\u0301"}'.encode("utf-8"),
        )
        for document in invalid_documents:
            with self.subTest(document=document):
                with self.assertRaises(FrozenD1ExecutionError):
                    runner.run_d1(document)

    def test_schema_validator_enforces_frozen_min_properties_keyword(self) -> None:
        with self.assertRaisesRegex(FrozenD1ExecutionError, "minProperties"):
            validate_json_schema({}, {"type": "object", "minProperties": 1})

    def test_rehashed_manifest_tampering_still_fails_frozen_identity(self) -> None:
        document = deepcopy(self.execution)
        document["manifest"]["frozen_at"] = "2026-07-13T07:24:37Z"
        document["integrity"]["manifest_sha256"] = digest(document["manifest"])
        with self.assertRaisesRegex(FrozenD1ExecutionError, "not frozen D1"):
            runner.run_d1(canonical_bytes(document))

    def test_execution_envelope_rejects_injected_evaluator_and_schema_drift(self) -> None:
        injected = deepcopy(self.execution)
        injected["injected_evaluation_manifest"] = {
            "expected_signature": "forbidden"
        }
        wrong_schema = deepcopy(self.execution)
        wrong_schema["$schema"] = "./attacker.schema.json"
        missing_schema = deepcopy(self.execution)
        del missing_schema["$schema"]
        extra_integrity = deepcopy(self.execution)
        extra_integrity["integrity"]["expected_output"] = "forbidden"
        list_manifest = deepcopy(self.execution)
        list_manifest["manifest"] = []
        scalar_manifest = deepcopy(self.execution)
        scalar_manifest["manifest"] = 1
        for document in (
            injected,
            wrong_schema,
            missing_schema,
            extra_integrity,
            list_manifest,
            scalar_manifest,
        ):
            with self.subTest(keys=sorted(document)):
                with self.assertRaises(FrozenD1ExecutionError):
                    runner.run_d1(canonical_bytes(document))

    def test_source_bundle_is_closed_and_deterministic(self) -> None:
        expected = digest(
            [
                {
                    "path": path,
                    "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
                }
                for path in runner.BUNDLE_PATHS
            ]
        )
        self.assertEqual(
            runner.BUNDLE_CANONICALIZATION_ID,
            "interp-d1-source-bundle-v1-policy-bindings-elided",
        )
        self.assertEqual(self.run_document["runner_bundle_sha256"], expected)
        self.assertEqual(
            self.run_document["runner_implementation_sha256"],
            file_sha256(ROOT / "dynamics/labs/interp_d1_runner.py"),
        )
        self.assertNotIn("dynamics/tests/test_interp_d1_runner.py", runner.BUNDLE_PATHS)

    def test_runner_modules_do_not_import_runtime_or_evaluator_layers(self) -> None:
        forbidden_prefixes = (
            "dynamics.engine",
            "dynamics.models",
            "dynamics.contract",
            "dynamics.protocol",
            "dynamics.labs.interp_d1_evaluator",
        )
        for relative in runner.BUNDLE_PATHS:
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            imported = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.append(node.module)
            self.assertFalse(
                any(name.startswith(forbidden_prefixes) for name in imported),
                (relative, imported),
            )

    def test_detached_module_import_does_not_bootstrap_runtime(self) -> None:
        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; "
                    "import dynamics.labs.interp_d1_run_cli; "
                    "blocked = sorted(name for name in "
                    "('dynamics.engine','dynamics.models','dynamics.protocol') "
                    "if name in sys.modules); "
                    "assert not blocked, blocked"
                ),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)

    def test_run_cli_requires_only_execution_and_output_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            execution = root / "execution.json"
            output = root / "run.json"
            execution.write_bytes(self.execution_bytes)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dynamics.labs.interp_d1_run_cli",
                    "--execution",
                    str(execution),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                check=True,
            )
            self.assertEqual(loads_exact(output.read_bytes()), self.run_document)


if __name__ == "__main__":
    unittest.main()
