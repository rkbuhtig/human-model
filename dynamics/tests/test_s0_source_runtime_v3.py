from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from dynamics.s0.source_common_v3 import canonical_bytes
from dynamics.s0.source_family_v2 import generate_instance
from dynamics.s0.source_runtime_v3 import (
    derive_split_seed,
    materialize_split,
    materialize_trajectory,
)

ROOT = Path(__file__).resolve().parents[2]
HYPERPRIOR = json.loads(
    (ROOT / "research/benchmarks/sources/sim-rel-boundary-family-002-hyperprior.json").read_text()
)


class SourceRuntimeV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.family_seed = hashlib.sha256(b"runtime-family").hexdigest()
        cls.instance = generate_instance(HYPERPRIOR, family_seed_hex=cls.family_seed, instance_index=0)
        cls.split_seed = derive_split_seed(cls.family_seed, cls.instance["instance_id"], "development")

    def _trajectory(self, branch: str):
        return materialize_trajectory(
            self.instance,
            split_seed_hex=self.split_seed,
            split="development",
            history_condition="H-STABLE",
            continuation_condition=branch,
            sample_index=0,
        )

    def test_trajectory_is_byte_stable(self) -> None:
        left = self._trajectory("F-REPAIR")
        right = self._trajectory("F-REPAIR")
        self.assertEqual(canonical_bytes(left.to_dict()), canonical_bytes(right.to_dict()))

    def test_p1_visible_prefix_and_target_are_matched_across_hidden_branches(self) -> None:
        trajectories = [self._trajectory(branch) for branch in ("F-REPAIR", "F-DEFLECT", "F-REPEAT", "F-PUBLIC")]
        digests = {item.prediction_records[0].observable_prefix.digest() for item in trajectories}
        actions = {item.prediction_records[0].immediate_target for item in trajectories}
        self.assertEqual(len(digests), 1)
        self.assertEqual(len(actions), 1)

    def test_branch_is_revealed_only_by_public_cues_after_p1(self) -> None:
        repair = self._trajectory("F-REPAIR")
        public = self._trajectory("F-PUBLIC")
        self.assertEqual(
            repair.prediction_records[0].observable_prefix.digest(),
            public.prediction_records[0].observable_prefix.digest(),
        )
        self.assertNotEqual(
            repair.prediction_records[1].observable_prefix.digest(),
            public.prediction_records[1].observable_prefix.digest(),
        )
        visible = str(repair.prediction_records[0].observable_prefix.to_dict())
        self.assertNotIn("F-REPAIR", visible)

    def test_terminal_target_is_shared_across_prediction_points(self) -> None:
        trajectory = self._trajectory("F-DEFLECT")
        self.assertEqual(
            len({record.terminal_target for record in trajectory.prediction_records}),
            1,
        )

    def test_runtime_has_no_hidden_p3_feedback_event(self) -> None:
        trajectory = self._trajectory("F-REPAIR")
        p3_events = trajectory.prediction_records[2].observable_prefix.events
        self.assertEqual(len(p3_events), 7)
        self.assertEqual([event.ordinal for event in p3_events], list(range(1, 8)))

    def test_split_streams_are_domain_separated(self) -> None:
        evaluation_seed = derive_split_seed(self.family_seed, self.instance["instance_id"], "evaluation")
        self.assertNotEqual(self.split_seed, evaluation_seed)

    def test_development_split_is_balanced_and_canonical(self) -> None:
        second = generate_instance(HYPERPRIOR, family_seed_hex=self.family_seed, instance_index=1)
        trajectories = materialize_split([second, self.instance], family_seed_hex=self.family_seed, split="development")
        self.assertEqual(len(trajectories), 32)
        counts = {}
        for item in trajectories:
            key = (item.source_instance_id, item.history_condition, item.evaluator_continuation_condition)
            counts[key] = counts.get(key, 0) + 1
        self.assertTrue(all(value == 2 for value in counts.values()))
        instance_indices = [item.source_instance_id for item in trajectories]
        self.assertEqual(instance_indices, sorted(instance_indices))


if __name__ == "__main__":
    unittest.main()
