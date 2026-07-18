from __future__ import annotations

import unittest

from dynamics.s0.source_common_v3 import SourceProcessError
from dynamics.s0.source_runtime_v3 import (
    ActionEvent,
    FeedbackEvent,
    ModelVisibleContextV3,
    NoEvent,
    ObservablePrefixV3,
    OccurrenceEvent,
    public_event_from_dict,
)


class PublicEventV3Tests(unittest.TestCase):
    def test_discriminated_union_rejects_wrong_payload(self) -> None:
        with self.assertRaises(SourceProcessError):
            public_event_from_dict(
                {
                    "schema_version": "s0-public-event-v3/1.0.0",
                    "event_type": "ACTION",
                    "ordinal": 1,
                    "feedback_category": "ACKNOWLEDGED_IMPACT",
                    "actor": "focal",
                    "target": "interaction",
                }
            )

    def test_action_and_feedback_have_distinct_typed_fields(self) -> None:
        action = ActionEvent(1, "ASSERT_BOUNDARY").to_dict()
        feedback = FeedbackEvent(1, "ACKNOWLEDGED_IMPACT").to_dict()
        self.assertIn("action_category", action)
        self.assertNotIn("feedback_category", action)
        self.assertIn("feedback_category", feedback)
        self.assertNotIn("action_category", feedback)

    def test_prefix_requires_continuous_ordinals(self) -> None:
        context = ModelVisibleContextV3("H-STABLE")
        with self.assertRaises(SourceProcessError):
            ObservablePrefixV3(
                context=context,
                events=(
                    OccurrenceEvent(1, "CURRENT_COMMITMENT_MISSED", "REGISTERED_REPORT", "counterpart", "focal"),
                    NoEvent(3),
                ),
            )

    def test_no_event_is_exactly_one_canonical_tick(self) -> None:
        with self.assertRaises(SourceProcessError):
            NoEvent(1, canonical_tick_count=2)

    def test_continuation_branch_is_not_an_observable_field(self) -> None:
        prefix = ObservablePrefixV3(
            context=ModelVisibleContextV3("H-BREACH"),
            events=(
                OccurrenceEvent(1, "CURRENT_COMMITMENT_MISSED", "REGISTERED_REPORT", "counterpart", "focal"),
            ),
        ).to_dict()
        encoded = str(prefix)
        self.assertNotIn("continuation_condition", encoded)
        self.assertNotIn("F-REPAIR", encoded)


if __name__ == "__main__":
    unittest.main()
