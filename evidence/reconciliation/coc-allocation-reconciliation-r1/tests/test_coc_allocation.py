import sys
import unittest
from fractions import Fraction
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from frozen_detector import detect_event_shapes, parse_events  # noqa: E402
from recalculate_coc import (  # noqa: E402
    LEGACY_CANDIDATE,
    LEGACY_EXCLUDED,
    PRIMARY_CANDIDATE,
    PRIMARY_EXCLUDED,
    SHIPPED,
    event_allocations,
)


def call(command, output, path=None):
    args = {"command": command}
    if path is not None:
        args["path"] = path
    return [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"function": {"arguments": __import__("json").dumps(args)}}
            ],
        },
        {"role": "tool", "content": output},
    ]


class FrozenDetectorFixtureTests(unittest.TestCase):
    def test_repeat_and_reread_overlap_fixture(self):
        messages = []
        messages += call("view", "α" * 2200, "/repo/a.py")
        messages += call("view", "beta", "/repo/a.py")
        events = parse_events(messages, "qwen")
        labels = detect_event_shapes(events)
        self.assertEqual(len(events[0]["obs"].encode("utf-8")), 4400)
        self.assertEqual(
            labels[0],
            [
                "E1_repeated_exact_command",
                "E2_repeated_similar_command",
                "E3_same_file_reread",
            ],
        )
        self.assertEqual(
            set(labels[1]),
            {
                "E1_repeated_exact_command",
                "E2_repeated_similar_command",
                "E3_same_file_reread",
                "E14_output_followed_by_reread",
            },
        )

    def test_validation_overlap_fixture(self):
        output = "PASSED\n" + ("line\n" * 700)
        messages = call("pytest -q", output) + call("pytest -q", output)
        labels = detect_event_shapes(parse_events(messages, "osw"))
        self.assertIn("E6_large_test_success", labels[0])
        self.assertIn("E10_repeated_validation", labels[0])
        self.assertNotIn("E11_unchanged_validation", labels[0])
        self.assertIn("E11_unchanged_validation", labels[1])


class AllocationTests(unittest.TestCase):
    def test_equal_split_overlap_control(self):
        shapes = ["E1_repeated_exact_command", "E7_large_test_failure", "E10_repeated_validation"]
        denominator, numerator = event_allocations(10, shapes, PRIMARY_EXCLUDED, SHIPPED)
        self.assertEqual(denominator, Fraction(20, 3))
        self.assertEqual(numerator, Fraction(10, 3))
        self.assertLessEqual(denominator, 10)

    def test_capability_mapping_is_not_legacy_mapping(self):
        self.assertNotIn("E9_large_build_output", set(PRIMARY_CANDIDATE))
        self.assertIn("E9_large_build_output", PRIMARY_EXCLUDED)
        self.assertIn("E15_output_followed_by_rederivation", LEGACY_CANDIDATE)
        self.assertNotIn("E15_output_followed_by_rederivation", PRIMARY_CANDIDATE)
        self.assertNotEqual(PRIMARY_EXCLUDED, LEGACY_EXCLUDED)

    def test_supported_mass_never_exceeds_qualified_mass(self):
        for shapes in (
            ["E5_same_search"],
            ["E1_repeated_exact_command", "E12_large_diagnostic"],
            ["E6_large_test_success", "E13_large_output_near_terminal"],
        ):
            denominator, shipped = event_allocations(101, shapes, PRIMARY_EXCLUDED, SHIPPED)
            _, candidate = event_allocations(101, shapes, PRIMARY_EXCLUDED, PRIMARY_CANDIDATE)
            self.assertLessEqual(shipped, denominator)
            self.assertLessEqual(candidate, denominator)


if __name__ == "__main__":
    unittest.main()
