from __future__ import annotations

import ast
from collections import Counter
from copy import deepcopy
import inspect
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from dynamics.labs import interp_m1_evaluator as evaluator
from dynamics.labs import interp_m1_cli
from dynamics.labs.interp_m1_common import (
    canonical_bytes,
    digest,
    file_sha256,
    load_exact,
    loads_exact,
    resolve_local_ref,
    validate_json_schema,
)


ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS = ROOT / "research" / "benchmarks"
EXECUTION_PATH = BENCHMARKS / "interp-001-m1-v1-execution.json"
EVALUATION_PATH = BENCHMARKS / "interp-001-m1-v1-evaluation.json"
CELL_SCHEMA_PATH = BENCHMARKS / "interp-001-m1-v1-result.schema.json"
RUN_SCHEMA_PATH = BENCHMARKS / "interp-001b-m1-run.schema.json"
RUN_PATH = BENCHMARKS / "interp-001-m1-v1-run.json"
POLICY_PATH = BENCHMARKS / "interp-001b-m1-evaluator-policy-v1.json"
REPORT_SCHEMA_PATH = (
    BENCHMARKS / "interp-001b-m1-conformance-report.schema.json"
)
REPORT_PATH = BENCHMARKS / "interp-001-m1-v1-conformance.json"
EVALUATOR_PATH = ROOT / "dynamics" / "labs" / "interp_m1_evaluator.py"
RUNNER_PATH = ROOT / "dynamics" / "labs" / "interp_m1_runner.py"
COMMON_PATH = ROOT / "dynamics" / "labs" / "interp_m1_common.py"
CLI_PATH = ROOT / "dynamics" / "labs" / "interp_m1_cli.py"
RUN_CLI_PATH = ROOT / "dynamics" / "labs" / "interp_m1_run_cli.py"
EVALUATE_CLI_PATH = ROOT / "dynamics" / "labs" / "interp_m1_evaluate_cli.py"


def _bundle_sha256(role: str) -> str:
    return evaluator._source_bundle_sha256(role)


def _resolved_schema_node(
    root_schema: dict[str, object], node: dict[str, object]
) -> dict[str, object]:
    while "$ref" in node:
        node = resolve_local_ref(root_schema, node["$ref"])
    return node


def _schema_node_at_path(
    root_schema: dict[str, object],
    start: dict[str, object],
    path: str,
) -> dict[str, object]:
    node = _resolved_schema_node(root_schema, start)
    for segment in path.removeprefix("/").split("/") if path != "/" else ():
        node = _resolved_schema_node(root_schema, node)
        if segment == "*":
            if node.get("type") != "array" or not isinstance(
                node.get("items"), dict
            ):
                raise AssertionError(f"wildcard does not resolve against array: {path}")
            node = node["items"]
        else:
            properties = node.get("properties")
            if not isinstance(properties, dict) or segment not in properties:
                raise AssertionError(f"schema path does not resolve: {path}")
            node = properties[segment]
    return _resolved_schema_node(root_schema, node)


class InterpM1EvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_bytes = EXECUTION_PATH.read_bytes()
        cls.evaluation_bytes = EVALUATION_PATH.read_bytes()
        cls.cell_schema_bytes = CELL_SCHEMA_PATH.read_bytes()
        cls.run_schema_bytes = RUN_SCHEMA_PATH.read_bytes()
        cls.run_bytes = RUN_PATH.read_bytes()
        cls.policy_bytes = POLICY_PATH.read_bytes()
        cls.report_schema_bytes = REPORT_SCHEMA_PATH.read_bytes()
        cls.committed_report_bytes = REPORT_PATH.read_bytes()
        cls.run_document = loads_exact(cls.run_bytes)
        cls.cell_schema = load_exact(CELL_SCHEMA_PATH)
        cls.policy_document = load_exact(POLICY_PATH)
        cls.report_schema = load_exact(REPORT_SCHEMA_PATH)
        cls.valid_report_envelope = evaluator.evaluate_m1(
            cls.execution_bytes,
            cls.evaluation_bytes,
            cls.cell_schema_bytes,
            cls.run_schema_bytes,
            cls.run_bytes,
            cls.policy_bytes,
            cls.report_schema_bytes,
        )

    def _evaluate(self, **overrides: bytes) -> dict[str, object]:
        values = {
            "execution_manifest_bytes": self.execution_bytes,
            "evaluation_manifest_bytes": self.evaluation_bytes,
            "cell_result_schema_bytes": self.cell_schema_bytes,
            "run_artifact_schema_bytes": self.run_schema_bytes,
            "run_artifact_bytes": self.run_bytes,
            "evaluator_policy_bytes": self.policy_bytes,
            "conformance_report_schema_bytes": self.report_schema_bytes,
        }
        values.update(overrides)
        return evaluator.evaluate_m1(**values)

    def _mutated_run_bytes(self, mutate, *, rehash: bool = True) -> bytes:
        document = deepcopy(self.run_document)
        mutate(document)
        if rehash:
            document["integrity"]["run_sha256"] = digest(document["run"])
        return canonical_bytes(document)

    @staticmethod
    def _cell(
        document: dict[str, object], fixture_key: str, model_id: str
    ) -> dict[str, object]:
        return next(
            cell
            for cell in document["run"]["cells"]
            if cell["fixture_key"] == fixture_key and cell["model_id"] == model_id
        )

    def _assert_input_error(self, expected_code: str, **overrides: bytes) -> None:
        with self.assertRaises(evaluator.FrozenEvaluationInputError) as caught:
            self._evaluate(**overrides)
        self.assertEqual(caught.exception.code, expected_code)

    @staticmethod
    def _failed_assertions(report_envelope: dict[str, object]) -> set[str]:
        return {
            item["assertion_id"]
            for item in report_envelope["report"]["assertion_results"]
            if item["status"] == "FAIL"
        }

    def test_valid_run_passes_schema_integrity_and_exact_frozen_counts(self) -> None:
        envelope = self.valid_report_envelope
        validate_json_schema(envelope, self.report_schema)
        self.assertEqual(
            envelope["integrity"],
            {
                "algorithm": "sha256",
                "canonicalization_id": "interp-canonical-json-v1",
                "report_sha256": digest(envelope["report"]),
            },
        )
        report = envelope["report"]
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["failure_codes"], [])
        self.assertEqual(
            report["input_summary"],
            {
                "declared_fixture_count": 16,
                "declared_model_count": 4,
                "expected_cell_count": 64,
                "reported_cell_count": 64,
                "reported_step_count": 88,
            },
        )
        self.assertEqual(
            report["schema_validation"],
            {
                "status": "PASS",
                "validated_cell_count": 64,
                "failure_codes": [],
            },
        )
        self.assertEqual(len(report["signature_results"]), 88)
        self.assertTrue(
            all(item["status"] == "PASS" for item in report["signature_results"])
        )
        self.assertEqual(len(report["assertion_results"]), 54)
        self.assertTrue(
            all(item["status"] == "PASS" for item in report["assertion_results"])
        )
        self.assertEqual(len(report["retirement_results"]), 6)
        self.assertEqual(
            Counter(item["status"] for item in report["retirement_results"]),
            Counter({"NOT_TRIGGERED": 5, "NOT_EVALUABLE": 1}),
        )
        self.assertEqual(
            Counter(item["assertion_group"] for item in report["assertion_results"]),
            Counter(
                {
                    "mirror": 8,
                    "cell": 16,
                    "pair": 11,
                    "matrix": 5,
                    "global": 14,
                }
            ),
        )
        self.assertEqual(
            report["summary"],
            {
                "signature_pass_count": 88,
                "signature_fail_count": 0,
                "assertion_pass_count": 54,
                "assertion_fail_count": 0,
                "retirement_triggered_count": 0,
                "retirement_not_triggered_count": 5,
                "retirement_not_evaluable_count": 1,
            },
        )
        self.assertEqual(
            report["implementation_bindings"]["evaluator"]["source_sha256"],
            file_sha256(EVALUATOR_PATH),
        )
        self.assertEqual(
            report["implementation_bindings"]["runner"]["source_sha256"],
            file_sha256(RUNNER_PATH),
        )
        self.assertEqual(
            report["implementation_bindings"]["runner"]["bundle_sha256"],
            _bundle_sha256("runner"),
        )
        self.assertEqual(
            report["implementation_bindings"]["evaluator"]["bundle_sha256"],
            _bundle_sha256("evaluator"),
        )
        bindings = report["artifact_bindings"]
        self.assertEqual(
            bindings["run_sha256"], self.run_document["integrity"]["run_sha256"]
        )
        self.assertEqual(
            bindings["evaluator_policy_sha256"],
            digest(self.policy_document["policy"]),
        )
        self.assertEqual(
            bindings["run_artifact_schema_sha256"], file_sha256(RUN_SCHEMA_PATH)
        )

    def test_evaluation_is_byte_reproducible(self) -> None:
        first = self._evaluate()
        second = self._evaluate()
        self.assertEqual(first, second)
        self.assertEqual(
            evaluator.encode_report(first), canonical_bytes(first) + b"\n"
        )
        self.assertEqual(loads_exact(evaluator.encode_report(first)), first)

    def test_policy_pins_complete_process_source_bundles_and_entrypoints(self) -> None:
        identities = self.policy_document["policy"]["implementation_identities"]
        for role in ("runner", "evaluator"):
            binding = identities[role]["source_bundle"]
            self.assertEqual(
                binding["canonicalization_id"], evaluator.BUNDLE_CANONICALIZATION_ID
            )
            self.assertEqual(binding["paths"], list(evaluator.BUNDLE_PATHS[role]))
            self.assertEqual(binding["bundle_sha256"], _bundle_sha256(role))
            self.assertIn("dynamics/labs/interp_m1_cli.py", binding["paths"])
        self.assertIn(
            "dynamics/labs/interp_m1_run_cli.py",
            identities["runner"]["source_bundle"]["paths"],
        )
        self.assertIn(
            "dynamics/labs/interp_m1_evaluate_cli.py",
            identities["evaluator"]["source_bundle"]["paths"],
        )
        versioning = self.policy_document["policy"]["evaluation_contract"][
            "implementation_binding_versioning"
        ]
        self.assertIn("new_implementation_version", versioning["change_rule"])
        self.assertIn("new_evaluator_policy_version", versioning["change_rule"])

        original_read_bytes = Path.read_bytes

        def mutate_orchestrator(path: Path) -> bytes:
            source = original_read_bytes(path)
            return source + b"\n# source mutation\n" if path.resolve() == CLI_PATH.resolve() else source

        with patch.object(Path, "read_bytes", mutate_orchestrator):
            self.assertNotEqual(_bundle_sha256("runner"), identities["runner"]["source_bundle"]["bundle_sha256"])
            self.assertNotEqual(_bundle_sha256("evaluator"), identities["evaluator"]["source_bundle"]["bundle_sha256"])
            self._assert_input_error("IMPLEMENTATION_BINDING_MISMATCH")

    def test_invalid_inputs_fail_closed_without_an_invalid_input_report_domain(self) -> None:
        status_schema = self.report_schema["$defs"]["report"]["properties"]["status"]
        self.assertEqual(status_schema, {"enum": ["PASS", "FAIL"]})
        contract = self.policy_document["policy"]["evaluation_contract"]
        self.assertEqual(
            contract["raw_result_validation"]["failure_disposition"],
            "FAIL_CLOSED_EXCEPTION_NO_REPORT",
        )
        self.assertEqual(
            contract["assertion_aggregation"]["pre_report_failure_rule"]["disposition"],
            "raise_FrozenEvaluationInputError_and_return_no_report_envelope",
        )
        with self.assertRaises(evaluator.FrozenEvaluationInputError):
            self._evaluate(run_artifact_bytes=b"{}")
        with tempfile.TemporaryDirectory() as directory:
            invalid_run = Path(directory) / "invalid-run.json"
            output = Path(directory) / "must-not-exist.json"
            invalid_run.write_bytes(b"{}")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dynamics.labs.interp_m1_evaluate_cli",
                    "--execution",
                    str(EXECUTION_PATH),
                    "--evaluation",
                    str(EVALUATION_PATH),
                    "--cell-schema",
                    str(CELL_SCHEMA_PATH),
                    "--run-schema",
                    str(RUN_SCHEMA_PATH),
                    "--run",
                    str(invalid_run),
                    "--policy",
                    str(POLICY_PATH),
                    "--report-schema",
                    str(REPORT_SCHEMA_PATH),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())

    def test_raw_schema_rejects_bool_integer_and_unknown_field_before_evaluation(self) -> None:
        def boolean_delta(document):
            self._cell(document, "fx001", "R0")["steps"][0]["semantic"][
                "access_ordinal_delta"
            ] = True

        def boolean_rank(document):
            self._cell(document, "fx001", "R0")["steps"][0]["semantic"][
                "subjective_form_profile"
            ]["activation"]["rank"] = True

        def unknown_field(document):
            self._cell(document, "fx001", "R0")["steps"][0]["semantic"][
                "not_in_frozen_schema"
            ] = 0

        for name, mutation in (
            ("boolean_delta", boolean_delta),
            ("boolean_rank", boolean_rank),
            ("unknown_field", unknown_field),
        ):
            with self.subTest(name=name), patch.object(
                evaluator, "_evaluate_signatures"
            ) as evaluate_signatures:
                self._assert_input_error(
                    "RESULT_SCHEMA_FAILURE",
                    run_artifact_bytes=self._mutated_run_bytes(mutation),
                )
                evaluate_signatures.assert_not_called()

    def test_run_integrity_implementation_and_cell_bindings_are_enforced(self) -> None:
        def body_without_rehash(document):
            document["run"]["status"] = "tampered"

        self._assert_input_error(
            "INPUT_INTEGRITY_FAILURE",
            run_artifact_bytes=self._mutated_run_bytes(
                body_without_rehash, rehash=False
            ),
        )

        def wrong_integrity(document):
            document["integrity"]["run_sha256"] = "0" * 64

        self._assert_input_error(
            "INPUT_INTEGRITY_FAILURE",
            run_artifact_bytes=self._mutated_run_bytes(
                wrong_integrity, rehash=False
            ),
        )

        def wrong_runner_source(document):
            document["run"]["runner_implementation_sha256"] = "0" * 64

        self._assert_input_error(
            "IMPLEMENTATION_BINDING_MISMATCH",
            run_artifact_bytes=self._mutated_run_bytes(wrong_runner_source),
        )

        def wrong_runner_bundle(document):
            document["run"]["runner_bundle_sha256"] = "0" * 64

        self._assert_input_error(
            "IMPLEMENTATION_BINDING_MISMATCH",
            run_artifact_bytes=self._mutated_run_bytes(wrong_runner_bundle),
        )

        def wrong_cell_binding(document):
            self._cell(document, "fx001", "R0")[
                "execution_contract_sha256"
            ] = "0" * 64

        self._assert_input_error(
            "ARTIFACT_BINDING_MISMATCH",
            run_artifact_bytes=self._mutated_run_bytes(wrong_cell_binding),
        )

    def test_run_schema_rejects_missing_duplicate_and_evaluator_rejects_reordering(self) -> None:
        def missing(document):
            document["run"]["cells"].pop(0)

        def duplicate(document):
            document["run"]["cells"].append(
                deepcopy(document["run"]["cells"][0])
            )

        def reordered(document):
            cells = document["run"]["cells"]
            cells[0], cells[1] = cells[1], cells[0]

        for name, code, mutation in (
            ("missing", "INPUT_INTEGRITY_FAILURE", missing),
            ("duplicate", "INPUT_INTEGRITY_FAILURE", duplicate),
            ("reordered", "RUN_MATRIX_MISMATCH", reordered),
        ):
            with self.subTest(name=name):
                self._assert_input_error(
                    code,
                    run_artifact_bytes=self._mutated_run_bytes(mutation),
                )

    def test_run_schema_rejects_missing_and_extra_metadata_before_evaluation(self) -> None:
        def missing_metadata(document):
            del document["run"]["runner_input_kind"]

        def extra_metadata(document):
            document["run"]["undeclared_metadata"] = "must-not-normalize-away"

        for name, mutation in (
            ("missing", missing_metadata),
            ("extra", extra_metadata),
        ):
            with self.subTest(name=name), patch.object(
                evaluator, "_evaluate_signatures"
            ) as evaluate_signatures:
                self._assert_input_error(
                    "INPUT_INTEGRITY_FAILURE",
                    run_artifact_bytes=self._mutated_run_bytes(mutation),
                )
                evaluate_signatures.assert_not_called()

    def test_protocol_step_sequence_mismatch_is_rejected_before_semantics(self) -> None:
        def wrong_step(document):
            self._cell(document, "fx013", "R0")["steps"][1][
                "protocol_step"
            ] = 3

        with patch.object(evaluator, "_evaluate_signatures") as evaluate_signatures:
            self._assert_input_error(
                "RUN_MATRIX_MISMATCH",
                run_artifact_bytes=self._mutated_run_bytes(wrong_step),
            )
            evaluate_signatures.assert_not_called()

    def test_frozen_evaluation_policy_and_schema_file_bindings_reject_mutation(self) -> None:
        for parameter, source in (
            ("execution_manifest_bytes", self.execution_bytes),
            ("evaluation_manifest_bytes", self.evaluation_bytes),
            ("evaluator_policy_bytes", self.policy_bytes),
            ("cell_result_schema_bytes", self.cell_schema_bytes),
            ("run_artifact_schema_bytes", self.run_schema_bytes),
            ("conformance_report_schema_bytes", self.report_schema_bytes),
        ):
            with self.subTest(parameter=parameter):
                self._assert_input_error(
                    "ARTIFACT_BINDING_MISMATCH", **{parameter: source + b" "}
                )

    def test_schema_valid_semantic_mutation_is_fail_with_named_assertions(self) -> None:
        def mutation(document):
            self._cell(document, "fx001", "R0")["steps"][0]["semantic"][
                "adjudications"
            ][0]["outcome"] = "adopted_negative"

        envelope = self._evaluate(
            run_artifact_bytes=self._mutated_run_bytes(mutation)
        )
        validate_json_schema(envelope, self.report_schema)
        report = envelope["report"]
        self.assertEqual(report["status"], "FAIL")
        self.assertNotEqual(report["status"], "INVALID_INPUT")
        self.assertEqual(report["summary"]["signature_fail_count"], 1)
        self.assertEqual(report["summary"]["assertion_fail_count"], 3)
        failed_signature = next(
            item for item in report["signature_results"] if item["status"] == "FAIL"
        )
        self.assertEqual(
            (
                failed_signature["fixture_key"],
                failed_signature["model_id"],
                failed_signature["protocol_step"],
            ),
            ("fx001", "R0", 1),
        )
        self.assertEqual(
            failed_signature["failed_relation_paths"],
            ["/semantic/adjudications/*/outcome"],
        )
        self.assertEqual(
            self._failed_assertions(envelope),
            {"mirror-f1", "cell-fx001", "r0-reception-blind-positive"},
        )
        self.assertEqual(
            set(report["failure_codes"]),
            {
                "ASSERTION_FAILURE",
                "MIRROR_TRANSFORM_FAILURE",
                "SIGNATURE_RELATION_FAILURE",
            },
        )

    def test_guard_digest_mutation_fails_prefix_and_guard_assertions(self) -> None:
        def mutation(document):
            self._cell(document, "fx001", "R0")["steps"][0]["guard_ledgers"][
                "source_materials"
            ]["after_sha256"] = "0" * 64

        envelope = self._evaluate(
            run_artifact_bytes=self._mutated_run_bytes(mutation)
        )
        report = envelope["report"]
        self.assertEqual(report["status"], "FAIL")
        failed_signature = next(
            item for item in report["signature_results"] if item["status"] == "FAIL"
        )
        self.assertEqual(
            failed_signature["failed_relation_paths"],
            ["/semantic/prior_prefix_relation"],
        )
        self.assertEqual(
            self._failed_assertions(envelope),
            {
                "mirror-f1",
                "cell-fx001",
                "r0-reception-blind-positive",
                "no-authority-writes",
            },
        )

    def test_order_mirror_mutation_fails_named_f5_mirror_assertion(self) -> None:
        def mutation(document):
            semantic = self._cell(document, "fx010", "R0")["steps"][0][
                "semantic"
            ]
            semantic["accessed_material_keys_ordered"].reverse()
            memberships = semantic["assemblies"][0]["memberships"]
            memberships.reverse()
            for order, membership in enumerate(memberships):
                membership["order"] = order

        envelope = self._evaluate(
            run_artifact_bytes=self._mutated_run_bytes(mutation)
        )
        report = envelope["report"]
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("mirror-f5", self._failed_assertions(envelope))
        mirror = next(
            item
            for item in report["assertion_results"]
            if item["assertion_id"] == "mirror-f5"
        )
        self.assertEqual(mirror["failure_codes"], ["MIRROR_TRANSFORM_FAILURE"])
        failed_signature = next(
            item for item in report["signature_results"] if item["status"] == "FAIL"
        )
        self.assertEqual(
            failed_signature["failed_relation_paths"],
            ["/semantic/accessed_material_keys_ordered"],
        )

    def test_operator_log_leakage_and_cardinality_are_detected_as_assertion_failures(self) -> None:
        def leakage(document):
            self._cell(document, "fx001", "R0")["steps"][0][
                "operator_invocations"
            ][0]["inspected_fields"].append("fixture_key")

        def cardinality(document):
            self._cell(document, "fx001", "R0")["steps"][0][
                "operator_invocations"
            ].pop()

        for name, mutation in (("leakage", leakage), ("cardinality", cardinality)):
            with self.subTest(name=name):
                envelope = self._evaluate(
                    run_artifact_bytes=self._mutated_run_bytes(mutation)
                )
                report = envelope["report"]
                self.assertEqual(report["status"], "FAIL")
                self.assertEqual(report["summary"]["signature_fail_count"], 0)
                self.assertEqual(report["summary"]["assertion_fail_count"], 3)
                self.assertEqual(
                    self._failed_assertions(envelope),
                    {
                        "mirror-f1",
                        "no-same-ordinal-recursion",
                        "no-fixture-branching",
                    },
                )

    def test_policy_projection_catalog_is_rooted_at_step_result_and_resolves(self) -> None:
        catalogs = self.policy_document["policy"]["evaluation_contract"][
            "projection_catalogs"
        ]
        self.assertEqual(catalogs["projection_base"], "/steps/*")
        self.assertEqual(catalogs["projection_schema_ref"], "#/$defs/stepResult")

        base_node = _schema_node_at_path(
            self.cell_schema, self.cell_schema, catalogs["projection_base"]
        )
        declared_base = _resolved_schema_node(
            self.cell_schema,
            {"$ref": catalogs["projection_schema_ref"]},
        )
        self.assertEqual(base_node, declared_base)

        projection_paths: list[str] = []
        for key, value in catalogs.items():
            if key in {"projection_base", "projection_schema_ref"}:
                continue
            if isinstance(value, str):
                projection_paths.append(value)
            else:
                projection_paths.extend(value)
        self.assertEqual(len(projection_paths), len(set(projection_paths)))
        for path in projection_paths:
            with self.subTest(path=path):
                self.assertTrue(path.startswith("/"))
                resolved = _schema_node_at_path(
                    self.cell_schema, declared_base, path
                )
                self.assertIsInstance(resolved, dict)
                self.assertTrue(resolved)

    def test_runner_evaluator_ast_separation_and_no_runtime_imports(self) -> None:
        imported_by_file: dict[Path, set[str]] = {}
        for path in (RUNNER_PATH, EVALUATOR_PATH):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            modules: set[str] = set()
            dynamic_imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules.add(node.module)
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == "__import__":
                        dynamic_imports.append(node)
                    if (
                        isinstance(node.func, ast.Attribute)
                        and node.func.attr == "import_module"
                    ):
                        dynamic_imports.append(node)
            imported_by_file[path] = modules
            self.assertEqual(dynamic_imports, [])
            forbidden_runtime = {
                "dynamics.engine",
                "dynamics.models",
                "dynamics.routing",
                "dynamics.epistemics",
                "dynamics.mental_transitions",
                "dynamics.reducer_proposals",
                "dynamics.reducer_envelope_comparisons",
            }
            self.assertFalse(modules & forbidden_runtime, (path, modules & forbidden_runtime))

        self.assertEqual(
            {
                module
                for module in imported_by_file[EVALUATOR_PATH]
                if module.startswith("dynamics")
            },
            {"dynamics.labs.interp_m1_common"},
        )
        self.assertEqual(
            {
                module
                for module in imported_by_file[RUNNER_PATH]
                if module.startswith("dynamics")
            },
            {"dynamics.labs.interp_m1_common"},
        )
        self.assertNotIn(
            "dynamics.labs.interp_m1_runner", imported_by_file[EVALUATOR_PATH]
        )
        self.assertNotIn(
            "dynamics.labs.interp_m1_evaluator", imported_by_file[RUNNER_PATH]
        )
        self.assertEqual(
            tuple(inspect.signature(evaluator.evaluate_m1).parameters),
            (
                "execution_manifest_bytes",
                "evaluation_manifest_bytes",
                "cell_result_schema_bytes",
                "run_artifact_schema_bytes",
                "run_artifact_bytes",
                "evaluator_policy_bytes",
                "conformance_report_schema_bytes",
            ),
        )

    def test_orchestrator_has_no_runner_or_evaluator_import_and_orders_processes(self) -> None:
        modules_by_path: dict[Path, set[str]] = {}
        for path in (CLI_PATH, RUN_CLI_PATH, EVALUATE_CLI_PATH):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            modules = {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            modules.update(
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            )
            modules_by_path[path] = modules

        self.assertNotIn("dynamics.labs.interp_m1_runner", modules_by_path[CLI_PATH])
        self.assertNotIn("dynamics.labs.interp_m1_evaluator", modules_by_path[CLI_PATH])
        self.assertIn(
            "dynamics.labs.interp_m1_runner", modules_by_path[RUN_CLI_PATH]
        )
        self.assertNotIn(
            "dynamics.labs.interp_m1_evaluator", modules_by_path[RUN_CLI_PATH]
        )
        self.assertIn(
            "dynamics.labs.interp_m1_evaluator", modules_by_path[EVALUATE_CLI_PATH]
        )
        self.assertNotIn(
            "dynamics.labs.interp_m1_runner", modules_by_path[EVALUATE_CLI_PATH]
        )

        with patch.object(interp_m1_cli.subprocess, "run") as run_process:
            interp_m1_cli.generate_artifacts(ROOT)
        self.assertEqual(run_process.call_count, 2)
        run_command = run_process.call_args_list[0].args[0]
        evaluate_command = run_process.call_args_list[1].args[0]
        self.assertEqual(
            run_command[:3],
            [sys.executable, "-m", "dynamics.labs.interp_m1_run_cli"],
        )
        self.assertEqual(
            evaluate_command[:3],
            [sys.executable, "-m", "dynamics.labs.interp_m1_evaluate_cli"],
        )
        self.assertIn("--run-schema", evaluate_command)
        self.assertEqual(
            run_process.call_args_list[0].kwargs,
            {"cwd": ROOT, "check": True},
        )
        self.assertEqual(
            run_process.call_args_list[1].kwargs,
            {"cwd": ROOT, "check": True},
        )

    def test_committed_run_and_report_reproduce_exactly_from_current_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            generated_run = Path(directory) / "run.json"
            generated_report = Path(directory) / "report.json"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dynamics.labs.interp_m1_run_cli",
                    "--execution",
                    str(EXECUTION_PATH),
                    "--output",
                    str(generated_run),
                ],
                cwd=ROOT,
                check=True,
            )
            self.assertEqual(generated_run.read_bytes(), self.run_bytes)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dynamics.labs.interp_m1_evaluate_cli",
                    "--execution",
                    str(EXECUTION_PATH),
                    "--evaluation",
                    str(EVALUATION_PATH),
                    "--cell-schema",
                    str(CELL_SCHEMA_PATH),
                    "--run-schema",
                    str(RUN_SCHEMA_PATH),
                    "--run",
                    str(generated_run),
                    "--policy",
                    str(POLICY_PATH),
                    "--report-schema",
                    str(REPORT_SCHEMA_PATH),
                    "--output",
                    str(generated_report),
                ],
                cwd=ROOT,
                check=True,
            )
            self.assertEqual(
                generated_report.read_bytes(), self.committed_report_bytes
            )


if __name__ == "__main__":
    unittest.main()
