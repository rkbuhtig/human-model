from __future__ import annotations

import ast
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

from dynamics.labs import interp_d1_cli
from dynamics.labs import interp_d1_evaluator as evaluator
from dynamics.labs.interp_d1_challengers import (
    D1ChallengerContractError,
    adapt_challenger,
)
from dynamics.labs.interp_d1_common import (
    FrozenD1ExecutionError,
    canonical_bytes,
    digest_without_nested_member,
    load_exact,
    validate_json_schema,
)
from dynamics.labs.interp_d1_runner import encode_run, run_d1


ROOT = Path(__file__).resolve().parents[2]
BENCHMARKS = ROOT / "research" / "benchmarks"
EXECUTION = BENCHMARKS / "interp-001d1-v1-execution.json"
EVALUATION = BENCHMARKS / "interp-001d1-v1-evaluation.json"
RESULT_SCHEMA = BENCHMARKS / "interp-001d1-v1-result.schema.json"
RUN_SCHEMA = BENCHMARKS / "interp-001d1-v1-run.schema.json"
POLICY = BENCHMARKS / "interp-001d1-v1-evaluator-policy.json"
REPORT_SCHEMA = BENCHMARKS / "interp-001d1-v1-conformance-report.schema.json"
RUN_ARTIFACT = BENCHMARKS / "interp-001d1-v1-run.json"
CONFORMANCE_REPORT = BENCHMARKS / "interp-001d1-v1-conformance.json"


class InterpD1EvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_bytes = EXECUTION.read_bytes()
        cls.evaluation_bytes = EVALUATION.read_bytes()
        cls.result_schema_bytes = RESULT_SCHEMA.read_bytes()
        cls.run_schema_bytes = RUN_SCHEMA.read_bytes()
        cls.policy_bytes = POLICY.read_bytes()
        cls.report_schema_bytes = REPORT_SCHEMA.read_bytes()
        cls.run_document = run_d1(cls.execution_bytes)
        cls.run_bytes = encode_run(cls.run_document)
        cls.report = cls._evaluate_class(cls.run_bytes)

    @classmethod
    def _evaluate_class(cls, run_bytes: bytes):
        return evaluator.evaluate_d1(
            cls.execution_bytes,
            cls.evaluation_bytes,
            cls.result_schema_bytes,
            cls.run_schema_bytes,
            run_bytes,
            cls.policy_bytes,
            cls.report_schema_bytes,
        )

    def _evaluate(self, run: dict[str, object] | None = None):
        return self._evaluate_class(
            self.run_bytes if run is None else canonical_bytes(run)
        )

    @staticmethod
    def _rehash(run: dict[str, object], cell: dict[str, object] | None = None) -> None:
        if cell is not None:
            cell["integrity"]["cell_content_sha256"] = digest_without_nested_member(
                cell, "integrity", "cell_content_sha256"
            )
        run["integrity"]["run_sha256"] = digest_without_nested_member(
            run, "integrity", "run_sha256"
        )

    @staticmethod
    def _cell(run: dict[str, object], fixture: str, model: str):
        return next(
            item
            for item in run["cells"]
            if item["fixture_key"] == fixture and item["model_id"] == model
        )

    def test_clean_run_reports_all_frozen_counts_and_only_two_alias_rules(self) -> None:
        report = self.report["report"]
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["failure_codes"], [])
        self.assertEqual(len(report["signature_results"]), 88)
        self.assertEqual(len(report["cell_assertion_results"]), 24)
        self.assertEqual(len(report["pair_assertion_results"]), 30)
        self.assertEqual(len(report["global_assertion_results"]), 37)
        self.assertEqual(len(report["challenger_results"]), 72)
        self.assertEqual(len(report["retirement_results"]), 16)
        self.assertEqual(
            Counter(item["evaluation_role"] for item in report["signature_results"]),
            Counter({"development": 44, "sealed": 44}),
        )
        self.assertTrue(all(item["status"] == "PASS" for item in report["signature_results"]))
        self.assertTrue(
            all(
                item["status"] == "PASS"
                for item in report["cell_assertion_results"]
                + report["pair_assertion_results"]
                + report["global_assertion_results"]
            )
        )
        self.assertEqual(
            {
                item["rule_id"]
                for item in report["retirement_results"]
                if item["condition_status"] == "TRIGGERED"
            },
            {
                "retire.challenger.ch_rt_congruence",
                "retire.challenger.ch_declared_rt_lookup",
            },
        )
        self.assertEqual(report["summary"]["retirement_triggered_count"], 2)
        self.assertEqual(report["summary"]["rt_equivalence_family_count"], 1)
        self.assertEqual(report["summary"]["rt_alias_control_confirmation_count"], 1)
        self.assertEqual(report["summary"]["distinct_challenger_reduction_count"], 0)

    def test_evaluation_is_byte_deterministic_and_schema_valid(self) -> None:
        second = self._evaluate()
        self.assertEqual(second, self.report)
        self.assertEqual(evaluator.encode_report(second), canonical_bytes(second) + b"\n")
        validate_json_schema(second, load_exact(REPORT_SCHEMA))

    def test_committed_run_and_report_reproduce_exactly(self) -> None:
        self.assertEqual(RUN_ARTIFACT.read_bytes(), self.run_bytes)
        self.assertEqual(
            CONFORMANCE_REPORT.read_bytes(), evaluator.encode_report(self.report)
        )

    def test_challenger_fixture_equivalence_matrix_is_exact(self) -> None:
        grouped: dict[str, dict[bool, set[str]]] = defaultdict(
            lambda: defaultdict(set)
        )
        for item in self.report["report"]["challenger_results"]:
            grouped[item["challenger_id"]][item["targets_equal"]].add(
                item["fixture_key"]
            )
        self.assertEqual(
            grouped["CH_RT_CONGRUENCE"][True],
            {f"encfx{index:03d}" for index in range(1, 9)},
        )
        self.assertEqual(
            grouped["CH_DECLARED_RT_LOOKUP"][True],
            grouped["CH_RT_CONGRUENCE"][True],
        )
        self.assertEqual(
            grouped["CH_GHOST_FIXED_BASELINE"][False], {"ghfx002", "ghfx004"}
        )
        self.assertEqual(grouped["CH_MATERIAL_COUNT_OR_MAX"][True], set())

    def test_schema_valid_semantic_mutation_produces_fail_report(self) -> None:
        run = deepcopy(self.run_document)
        cell = self._cell(run, "srcfx003", "TF1")
        cell["semantic"]["target_form_readout_profile"][
            "positive_direction_support"
        ]["rank"] = 1
        self._rehash(run, cell)
        report = self._evaluate(run)["report"]
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("SIGNATURE_RELATION_FAILURE", report["failure_codes"])
        failed = [item for item in report["signature_results"] if item["status"] == "FAIL"]
        self.assertEqual([(item["fixture_key"], item["model_id"]) for item in failed], [("srcfx003", "TF1")])
        self.assertTrue(
            any(
                item["assertion_id"] == "global.dataflow.source"
                and item["status"] == "FAIL"
                for item in report["global_assertion_results"]
            )
        )

    def test_invalid_run_shape_fails_closed_without_report(self) -> None:
        run = deepcopy(self.run_document)
        run["undeclared"] = "forbidden"
        self._rehash(run)
        with self.assertRaises(evaluator.FrozenD1EvaluationInputError) as caught:
            self._evaluate(run)
        self.assertEqual(caught.exception.code, "INPUT_INTEGRITY_FAILURE")

    def test_placeholder_binding_literals_cannot_disable_frozen_checks(self) -> None:
        for name in (
            "POLICY_FILE_SHA256",
            "POLICY_SHA256",
            "POLICY_CONTRACT_SHA256",
            "REPORT_SCHEMA_SHA256",
        ):
            with self.subTest(binding=name), patch.object(
                evaluator, name, f"REFREEZE_{name}"
            ):
                with self.assertRaises(evaluator.FrozenD1EvaluationInputError):
                    self._evaluate()

    def test_trace_mutation_is_a_named_semantic_failure(self) -> None:
        run = deepcopy(self.run_document)
        cell = self._cell(run, "ghfx001", "GTP")
        cell["operator_trace"][0]["phase"] = "traverse"
        self._rehash(run, cell)
        report = self._evaluate(run)["report"]
        self.assertEqual(report["status"], "FAIL")
        failed = {
            item["assertion_id"]
            for item in report["global_assertion_results"]
            if item["status"] == "FAIL"
        }
        self.assertIn("global.trace.ghost", failed)
        self.assertIn("global.dataflow.ghost", failed)

    def test_adapter_shape_error_never_becomes_substantive_difference(self) -> None:
        declaration = {
            "comparison_target_id": "GHOST_CANDIDATE_TARGET"
        }
        with self.assertRaises(D1ChallengerContractError):
            adapt_challenger(
                declaration,
                {
                    "binding_candidate_directions": ["positive"],
                    "adjudication_outcome": "adopted_negative",
                },
            )

    def test_observability_never_claims_intermediate_or_cryptographic_proof(self) -> None:
        value = self.report["report"]["observability"]
        self.assertFalse(value["intermediate_typed_values_serialized"])
        self.assertFalse(value["runtime_ledgers_observed"])
        self.assertFalse(value["human_empirical_evidence"])
        self.assertFalse(value["predictive_support"])
        self.assertIn("not_cryptographic", value["runner_blinding_claim"])

    def test_ghost_close_edge_is_declared_candidate_state_list_not_extracted_receipts(self) -> None:
        execution = load_exact(EXECUTION)
        contract = execution["manifest"]["execution_contract"]
        cell = self._cell(self.run_document, "ghfx001", "GTP")
        self.assertTrue(evaluator._typed_dataflow_static_exact(contract, cell))
        stage_edge = next(
            edge
            for edge in contract["operator_typed_dataflow_contract"]["edges"]
            if edge["edge_id"] == "edge.ghost.stages_to_close"
        )
        self.assertEqual(stage_edge["producer_output_kinds"], ["candidate_relation_state"])
        self.assertEqual(stage_edge["consumer_value_kind"], "candidate_relation_state_list")
        self.assertEqual(stage_edge["transfer_policy"], "collect_receipts")

        extracted_receipt_contract = deepcopy(contract)
        mutated_edge = next(
            edge
            for edge in extracted_receipt_contract["operator_typed_dataflow_contract"]["edges"]
            if edge["edge_id"] == "edge.ghost.stages_to_close"
        )
        mutated_edge["consumer_value_kind"] = "ghost_stage_receipt_list"
        self.assertFalse(
            evaluator._typed_dataflow_static_exact(extracted_receipt_contract, cell)
        )

    def test_evaluator_identity_binds_normalized_not_circular_actual_source(self) -> None:
        policy = load_exact(POLICY)["policy"]
        identity = policy["implementation_identities"]["evaluator"]
        self.assertNotIn("source_sha256", identity)
        self.assertEqual(
            identity["source_normalization"],
            evaluator.EVALUATOR_SOURCE_NORMALIZATION_CONTRACT,
        )
        frozen = identity["normalized_source_sha256"]
        self.assertFalse(frozen.startswith("REFREEZE_"))
        self.assertEqual(
            frozen,
            evaluator._bundle_file_sha256("dynamics/labs/interp_d1_evaluator.py"),
        )

    def test_evaluator_and_challengers_do_not_import_runner_or_runtime(self) -> None:
        forbidden = {
            "dynamics.labs.interp_d1_runner",
            "dynamics.engine",
            "dynamics.models",
            "dynamics.routing",
            "dynamics.epistemics",
            "dynamics.mental_transitions",
        }
        for name in ("interp_d1_evaluator.py", "interp_d1_challengers.py"):
            tree = ast.parse((ROOT / "dynamics" / "labs" / name).read_text())
            imports = {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            imports.update(
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            )
            self.assertFalse(imports & forbidden, (name, imports & forbidden))

    def test_orchestrator_orders_separate_processes_without_role_imports(self) -> None:
        tree = ast.parse(
            (ROOT / "dynamics/labs/interp_d1_cli.py").read_text(encoding="utf-8")
        )
        imports = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        imports.update(
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        )
        self.assertNotIn("dynamics.labs.interp_d1_runner", imports)
        self.assertNotIn("dynamics.labs.interp_d1_evaluator", imports)

        with patch.object(interp_d1_cli.subprocess, "run") as execute:
            run_path, report_path = interp_d1_cli.generate_artifacts(ROOT)
        self.assertEqual(execute.call_count, 2)
        runner_args = execute.call_args_list[0].args[0]
        evaluator_args = execute.call_args_list[1].args[0]
        self.assertIn("dynamics.labs.interp_d1_run_cli", runner_args)
        self.assertNotIn("--evaluation", runner_args)
        self.assertIn("dynamics.labs.interp_d1_evaluate_cli", evaluator_args)
        self.assertIn("--evaluation", evaluator_args)
        self.assertEqual(run_path, RUN_ARTIFACT)
        self.assertEqual(report_path, CONFORMANCE_REPORT)

    def test_common_validator_enforces_min_properties(self) -> None:
        with self.assertRaises(FrozenD1ExecutionError):
            validate_json_schema({}, {"type": "object", "minProperties": 1})


if __name__ == "__main__":
    unittest.main()
