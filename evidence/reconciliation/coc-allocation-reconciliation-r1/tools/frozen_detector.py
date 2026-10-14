"""Independent, side-effect-free copy of the frozen OSW/Qwen detector semantics.

This module intentionally preserves historical behavior, including E4 being
unmeasurable. It does not import the historical scripts because those scripts
execute full censuses at import time.
"""

from __future__ import annotations

import json
import re
from typing import Any


TEST_PAT = re.compile(
    r"^\s*(pytest|python\s+-m\s+pytest|npm\s+(run\s+)?test|mocha|jest|vitest|go\s+test|cargo\s+test|make\s+test|tox)\b",
    re.I,
)
LINT_PAT = re.compile(r"^\s*(eslint|ruff|flake8|pylint|pre-commit)\b", re.I)
BUILD_PAT = re.compile(
    r"^\s*(make\b(?!.*test)|npm\s+run\s+build|gradle|mvn\b|cmake|cargo\s+build|gcc|g\+\+)",
    re.I,
)
SEARCH_PAT = re.compile(r"^\s*(grep|rg|ag|ack|find)\b", re.I)
VIEW_WORDS = {"view", "open", "cat", "head", "tail", "less", "sed", "str_replace_editor"}
NUMTOK = re.compile(r"\d+")
PASS_PAT = re.compile(r"PASSED|passed|all tests passed|✓", re.I)
FAIL_PAT = re.compile(r"FAILED|AssertionError|Traceback|✖|failing", re.I)
DIAG_PAT = re.compile(r"Traceback|Exception|ERROR:|error:", re.I)


def norm_cmd(command: str) -> str:
    return " ".join(command.split()).strip()


def sim_cmd(command: str) -> str:
    return " ".join(NUMTOK.sub("#", norm_cmd(command)).split())


def cmd_class(command: str) -> str:
    if TEST_PAT.match(command):
        return "test"
    if LINT_PAT.match(command):
        return "lint"
    if BUILD_PAT.match(command):
        return "build"
    if SEARCH_PAT.match(command):
        return "search"
    if command.split(" ", 1)[0].strip("`") in VIEW_WORDS:
        return "view"
    return "other"


def _messages(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, str):
        value = json.loads(value)
    return value or []


def parse_events(messages: Any, adapter: str) -> list[dict[str, Any]]:
    """Pair each tool observation with the latest parsable assistant command."""
    events: list[dict[str, Any]] = []
    pending: dict[str, Any] | None = None
    for message in _messages(messages):
        role = message.get("role")
        content = message.get("content") or ""
        if role == "assistant":
            tool_calls = message.get("tool_calls")
            if tool_calls:
                try:
                    calls = json.loads(tool_calls) if isinstance(tool_calls, str) else tool_calls
                    if isinstance(calls, dict):
                        calls = [calls]
                    for call in calls:
                        function = call.get("function") or {}
                        try:
                            args = json.loads(function.get("arguments") or "{}")
                        except Exception:
                            args = {}
                        command = args.get("command")
                        if isinstance(command, str) and command.strip():
                            command_line = command.splitlines()[0]
                            path = args.get("path")
                            first = command_line.split(" ", 1)[0]
                            if adapter == "qwen":
                                first = first.strip("`")
                            # OSW historical code used strip(''), i.e. no stripping.
                            if path and first in {"view", "open", "str_replace_editor", "create"}:
                                command_line = command_line + " " + str(path)
                            pending = {
                                "cmd": norm_cmd(command_line),
                                "csim": sim_cmd(command_line),
                                "cclass": cmd_class(command_line),
                                "path": path,
                            }
                except Exception:
                    if adapter == "qwen":
                        pending = None
        elif role == "tool" and pending is not None:
            event = dict(pending)
            event["obs"] = content
            event["obs_chars"] = len(content)
            event["obs_utf8_bytes"] = len(content.encode("utf-8"))
            event["event_index"] = len(events)
            events.append(event)
            pending = None
    count = len(events)
    for index, event in enumerate(events):
        event["pos"] = (index + 1) / count if count else 0
        event["turns_after"] = count - (index + 1)
    return events


def detect_event_shapes(events: list[dict[str, Any]]) -> list[list[str]]:
    labels: list[set[str]] = [set() for _ in events]
    count = len(events)
    if not count:
        return []

    def mark(shape: str, index: int) -> None:
        labels[index].add(shape)

    by_csim: dict[str, list[int]] = {}
    by_cnorm: dict[str, list[int]] = {}
    by_path: dict[str, list[int]] = {}
    for index, event in enumerate(events):
        by_csim.setdefault(event["csim"], []).append(index)
        by_cnorm.setdefault(event["cmd"], []).append(index)
        if event["path"]:
            by_path.setdefault(event["path"], []).append(index)

    for indexes in by_cnorm.values():
        if len(indexes) >= 2:
            for index in indexes:
                mark("E1_repeated_exact_command", index)
    for indexes in by_csim.values():
        if len(indexes) >= 2:
            for index in indexes:
                mark("E2_repeated_similar_command", index)

    for indexes in by_path.values():
        if len(indexes) >= 2:
            for index in indexes:
                mark("E3_same_file_reread", index)
            for left, right in zip(indexes, indexes[1:]):
                if right - left <= 3:
                    mark("E14_output_followed_by_reread", right)

    searches: dict[str, list[int]] = {}
    for index, event in enumerate(events):
        if event["cclass"] == "search":
            searches.setdefault(event["csim"], []).append(index)
    for indexes in searches.values():
        if len(indexes) >= 2:
            for index in indexes:
                mark("E5_same_search", index)

    for index, event in enumerate(events):
        if event["cclass"] == "test" and event["obs_chars"] >= 3000:
            if FAIL_PAT.search(event["obs"]):
                mark("E7_large_test_failure", index)
            elif PASS_PAT.search(event["obs"]):
                mark("E6_large_test_success", index)
        if event["obs_chars"] >= 3000:
            if event["cclass"] == "lint":
                mark("E8_large_lint_output", index)
            elif event["cclass"] == "build":
                mark("E9_large_build_output", index)
            if DIAG_PAT.search(event["obs"]):
                mark("E12_large_diagnostic", index)

    validations: dict[str, list[int]] = {}
    for index, event in enumerate(events):
        if event["cclass"] in ("test", "lint"):
            validations.setdefault(event["csim"], []).append(index)
    for indexes in validations.values():
        if len(indexes) >= 2:
            for index in indexes:
                mark("E10_repeated_validation", index)
            for left, right in zip(indexes, indexes[1:]):
                left_lines = set(events[left]["obs"].replace("\r\n", "\n").split("\n"))
                right_lines = set(events[right]["obs"].replace("\r\n", "\n").split("\n"))
                similarity = len(left_lines & right_lines) / max(1, len(left_lines | right_lines))
                if similarity >= 0.8:
                    mark("E11_unchanged_validation", right)

    for index, event in enumerate(events):
        if event["obs_chars"] >= 2000 and event["pos"] >= 0.75 and event["turns_after"] <= 3:
            mark("E13_large_output_near_terminal", index)

    for index, event in enumerate(events):
        for later in range(index + 1, min(index + 4, count)):
            if events[later]["csim"] == event["csim"] and events[later]["cclass"] in (
                "test",
                "lint",
                "build",
            ):
                mark("E15_output_followed_by_rederivation", later)
                break

    return [sorted(event_labels) for event_labels in labels]


def session_shapes(event_shapes: list[list[str]]) -> list[str]:
    return sorted({shape for shapes in event_shapes for shape in shapes})
