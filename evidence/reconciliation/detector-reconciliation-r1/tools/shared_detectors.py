"""A0-equivalent shared E1-E15 detector implementation.

The detector consumes corpus-neutral events produced by adapters.py.  It does
not read corpus-specific fields and does not change the frozen taxonomy.  R1
fixes only implementation drift documented by the independent validation.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

VERSION = "A0-XCORPUS-R1.0.0"
SHAPES = tuple(f"E{i}" for i in range(1, 16))
FULL_NAMES = {
    "E1": "repeated_exact_command",
    "E2": "repeated_similar_command",
    "E3": "same_file_reread",
    "E4": "overlapping_file_read",
    "E5": "same_search",
    "E6": "large_test_success",
    "E7": "large_test_failure",
    "E8": "large_lint_output",
    "E9": "large_build_output",
    "E10": "repeated_validation",
    "E11": "unchanged_validation",
    "E12": "large_diagnostic",
    "E13": "large_output_near_terminal",
    "E14": "output_followed_by_reread",
    "E15": "output_followed_by_rederivation",
}

TEST_PAT = re.compile(
    r"^\s*(pytest|python\s+-m\s+pytest|npm\s+(run\s+)?test|mocha|jest|vitest|"
    r"go\s+test|cargo\s+test|make\s+test|tox|python\s+-m\s+unittest)\b",
    re.I,
)
LINT_PAT = re.compile(r"^\s*(eslint|ruff|flake8|pylint|mypy|tsc|pyright|pre-commit)\b", re.I)
BUILD_PAT = re.compile(
    r"^\s*(make\b(?!.*test)|npm\s+run\s+build|gradle|mvn\b|cmake|cargo\s+build|gcc|g\+\+)",
    re.I,
)
SEARCH_PAT = re.compile(r"^\s*(grep|rg|ag|ack|find)\b", re.I)
VIEW_WORDS = {"view", "open", "cat", "head", "tail", "less", "sed", "str_replace_editor"}
FAIL_PAT = re.compile(r"FAILED|ERROR|Traceback|AssertionError|✖|failing", re.I)
PASS_PAT = re.compile(r"PASSED|passed|all tests passed|✓|ok\.?\s*$|\d+ passed", re.I)
DIAG_PAT = re.compile(r"Traceback|Exception|ERROR:|error:", re.I)
NUMTOK = re.compile(r"\d+")


def normalize_command(value: str) -> str:
    return " ".join((value or "").split()).strip()


def similar_command(value: str) -> str:
    return " ".join(NUMTOK.sub("#", normalize_command(value)).split())


def command_class(command: str) -> str:
    if TEST_PAT.match(command):
        return "test"
    if LINT_PAT.match(command):
        return "lint"
    if BUILD_PAT.match(command):
        return "build"
    if SEARCH_PAT.match(command):
        return "search"
    first = command.split(" ", 1)[0].strip("`")
    return "view" if first in VIEW_WORDS else "other"


def make_event(
    command: str,
    observation: str,
    *,
    path: str | None = None,
    view_range: Any = None,
    exit_code: int | None = None,
) -> dict[str, Any]:
    command = normalize_command(command)
    observation = observation or ""
    return {
        "cmd": command,
        "cnorm": command,
        "csim": similar_command(command),
        "cclass": command_class(command),
        "path": path,
        "vrange": view_range,
        "obs": observation,
        "obs_chars": len(observation),
        "exit": exit_code,
    }


def _normalized_range(raw: Any) -> tuple[int, int] | None:
    if not isinstance(raw, (list, tuple)) or not raw:
        return None
    try:
        start = int(raw[0])
        end = int(raw[1] if len(raw) > 1 else raw[0])
    except (TypeError, ValueError):
        return None
    # Preserve the frozen A0 interval interpretation.  In particular, do not
    # reinterpret corpus-specific sentinels such as an end value of -1.
    return (start, end)


def _jaccard_lines(left: str, right: str) -> float:
    a, b = set(left.splitlines()), set(right.splitlines())
    return len(a & b) / max(1, len(a | b))


def detect(events: list[dict[str, Any]]) -> list[set[str]]:
    """Return event-level A0 shape labels for normalized events.

    Exact-normalized command grouping is used for E1/E5/E10/E11.  Digit-
    normalized grouping is limited to E2 and E15, exactly as in D3-E1.
    """
    masks = [set() for _ in events]
    count = len(events)
    for index, event in enumerate(events):
        event["pos"] = (index + 1) / count if count else 0.0
        event["turns_after"] = count - index - 1

    by_cnorm: dict[str, list[int]] = defaultdict(list)
    by_csim: dict[str, list[int]] = defaultdict(list)
    by_path: dict[str, list[int]] = defaultdict(list)
    for index, event in enumerate(events):
        by_cnorm[event["cnorm"]].append(index)
        by_csim[event["csim"]].append(index)
        if event.get("path"):
            by_path[str(event["path"])].append(index)

    for grouping, shape in ((by_cnorm, "E1"), (by_csim, "E2")):
        for indexes in grouping.values():
            if len(indexes) >= 2:
                for index in indexes:
                    masks[index].add(shape)

    for indexes in by_path.values():
        if len(indexes) < 2:
            continue
        for index in indexes:
            masks[index].add("E3")
        ranged = [(index, _normalized_range(events[index].get("vrange"))) for index in indexes]
        ranged = [(index, value) for index, value in ranged if value is not None]
        for left in range(len(ranged)):
            left_index, left_range = ranged[left]
            for right in range(left + 1, len(ranged)):
                right_index, right_range = ranged[right]
                if left_range[0] <= right_range[1] and right_range[0] <= left_range[1]:
                    masks[left_index].add("E4")
                    masks[right_index].add("E4")

    searches: dict[str, list[int]] = defaultdict(list)
    for index, event in enumerate(events):
        if event["cclass"] == "search":
            searches[event["cnorm"]].append(index)
    for indexes in searches.values():
        if len(indexes) >= 2:
            for index in indexes:
                masks[index].add("E5")

    for index, event in enumerate(events):
        if event["obs_chars"] >= 3000:
            explicit_exit = event.get("exit")
            is_pass = explicit_exit == 0 or (
                explicit_exit is None
                and bool(PASS_PAT.search(event["obs"]))
                and not bool(FAIL_PAT.search(event["obs"]))
            )
            is_fail = (explicit_exit is not None and explicit_exit != 0) or (
                explicit_exit is None and bool(FAIL_PAT.search(event["obs"]))
            )
            if event["cclass"] == "test":
                if is_pass:
                    masks[index].add("E6")
                elif is_fail:
                    masks[index].add("E7")
            elif event["cclass"] == "lint":
                masks[index].add("E8")
            elif event["cclass"] == "build":
                masks[index].add("E9")
            if DIAG_PAT.search(event["obs"]):
                masks[index].add("E12")
        if event["obs_chars"] >= 2000 and event["pos"] >= 0.75 and event["turns_after"] <= 3:
            masks[index].add("E13")

    for indexes in by_cnorm.values():
        if len(indexes) < 2 or events[indexes[0]]["cclass"] not in ("test", "lint"):
            continue
        for index in indexes:
            masks[index].add("E10")
        for left, right in zip(indexes, indexes[1:]):
            if _jaccard_lines(events[left]["obs"], events[right]["obs"]) >= 0.8:
                masks[left].add("E11")
                masks[right].add("E11")

    for index, event in enumerate(events):
        for successor in range(index + 1, min(index + 4, count)):
            if (
                event.get("path")
                and events[successor].get("path") == event["path"]
                and events[successor]["cclass"] == "view"
            ):
                masks[successor].add("E14")
                break
        for successor in range(index + 1, min(index + 4, count)):
            if (
                events[successor]["csim"] == event["csim"]
                and events[successor]["cclass"] in ("test", "lint", "build")
            ):
                masks[successor].add("E15")
                break
    return masks
