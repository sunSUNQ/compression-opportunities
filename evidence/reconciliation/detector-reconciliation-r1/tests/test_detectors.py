from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TOOLS = BASE / "tools"
sys.path.insert(0, str(TOOLS))

from adapters import parse_osw, parse_tw  # noqa: E402
from shared_detectors import VERSION, detect, make_event  # noqa: E402


class GoldenDetectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads((BASE / "fixtures/golden-fixtures.json").read_text(encoding="utf-8"))

    def test_version_pin(self) -> None:
        self.assertEqual(self.fixture["detector_version"], VERSION)

    def test_golden_cases(self) -> None:
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                events = []
                for raw in case["events"]:
                    raw = dict(raw)
                    repeat = raw.pop("observation_repeat", None)
                    observation = raw.pop("observation", "")
                    if repeat:
                        observation = repeat["text"] * repeat["count"]
                    command = raw.pop("command")
                    events.append(make_event(command, observation, **raw))
                original = copy.deepcopy(events)
                masks = detect(events)
                self.assertEqual(masks, detect(original), case["id"])
                for index, labels in case.get("contains", {}).items():
                    self.assertTrue(set(labels) <= masks[int(index)], (case["id"], index, masks[int(index)]))
                for index, labels in case.get("excludes", {}).items():
                    self.assertTrue(set(labels).isdisjoint(masks[int(index)]), (case["id"], index, masks[int(index)]))

    def test_osw_adapter_reads_view_range(self) -> None:
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"function": {"name": "str_replace_editor", "arguments": json.dumps({"command": "view", "path": "/x.py", "view_range": [2, 8]})}}],
            },
            {"role": "tool", "content": "abcdef"},
        ]
        events, audit = parse_osw(messages)
        self.assertEqual(events[0]["vrange"], [2, 8])
        self.assertEqual(events[0]["path"], "/x.py")
        self.assertEqual(audit["view_range_present"], 1)

    def test_tw_and_osw_adapter_contract_equivalence(self) -> None:
        call = {"function": {"name": "str_replace_editor", "arguments": json.dumps({"command": "view", "path": "/x.py", "view_range": [2, 8]})}}
        tw_messages = [
            {"role": "assistant", "content": "", "tool_calls_json": json.dumps([call])},
            {"role": "tool", "content": "abcdef"},
        ]
        osw_messages = [
            {"role": "assistant", "content": "", "tool_calls": [call]},
            {"role": "tool", "content": "abcdef"},
        ]
        tw_events, _ = parse_tw(tw_messages)
        osw_events, _ = parse_osw(osw_messages)
        keys = ("cnorm", "csim", "cclass", "path", "vrange", "obs", "obs_chars")
        self.assertEqual({key: tw_events[0][key] for key in keys}, {key: osw_events[0][key] for key in keys})


if __name__ == "__main__":
    unittest.main()
