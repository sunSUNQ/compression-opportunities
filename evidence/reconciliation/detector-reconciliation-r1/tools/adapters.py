"""Corpus adapters for the A0 shared detector event contract."""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

from shared_detectors import command_class, make_event, normalize_command

EXIT_PAT = re.compile(r"\[The command completed with exit code (\d+)[^\]]*\]")
RC_PAT = re.compile(r"<returncode>(\d+)</returncode>")
OUT_PAT = re.compile(r"<output>\n?(.*?)\n?</output>\s*$", re.S)


def _calls(raw: Any) -> list[dict[str, Any]]:
    try:
        value = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return []
    if isinstance(value, dict):
        return [value]
    return value if isinstance(value, list) else []


def _args(call: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    fn = call.get("function") or {}
    name = str(fn.get("name") or "")
    raw = fn.get("arguments") or "{}"
    try:
        args = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return name, {}
    return name, args if isinstance(args, dict) else {}


def parse_tw(messages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    events: list[dict[str, Any]] = []
    pending: dict[str, Any] | None = None
    audit: Counter[str] = Counter()
    for message_index, message in enumerate(messages):
        role = message.get("role")
        content = str(message.get("content") or "")
        if role == "assistant":
            command = path = view_range = None
            for call in _calls(message.get("tool_calls_json")):
                audit["tool_calls"] += 1
                name, args = _args(call)
                raw_command = args.get("command")
                if isinstance(raw_command, str) and raw_command.strip():
                    command = normalize_command(raw_command.splitlines()[0])
                elif "view" in name.lower() or raw_command in ("view", "open"):
                    command = normalize_command(str(raw_command or name))
                if args.get("path"):
                    path = str(args["path"])
                if args.get("view_range") is not None:
                    view_range = args["view_range"]
                    audit["view_range_present"] += 1
            if command is None:
                match = re.search(r"```[a-z]*\s*\n(.+?)\n```", content, re.S)
                if match:
                    first = match.group(1).strip().splitlines()[0]
                    command = normalize_command(first)
                    if first.strip().startswith(("view ", "open ")):
                        parts = first.split()
                        if len(parts) > 1:
                            path = parts[1]
                        range_match = re.search(r"\[(\d+),\s*(\d+)\]", first)
                        if range_match:
                            view_range = [int(range_match.group(1)), int(range_match.group(2))]
                            audit["view_range_present"] += 1
                    else:
                        path_match = re.search(r"(/[^\s`]+)", first)
                        if path_match and command_class(first) == "view":
                            path = path_match.group(1)
            if command:
                pending = {
                    "command": command,
                    "path": path,
                    "view_range": view_range,
                    "message_index": message_index,
                }
                if path:
                    audit["path_present"] += 1
                if command_class(command) == "view":
                    audit["view_commands"] += 1
        elif role == "tool" and pending is not None:
            exit_match = EXIT_PAT.search(content)
            exit_code = int(exit_match.group(1)) if exit_match else None
            audit["explicit_exit"] += int(exit_code is not None)
            audit["missing_exit"] += int(exit_code is None)
            events.append(
                make_event(
                    pending["command"],
                    content,
                    path=pending["path"],
                    view_range=pending["view_range"],
                    exit_code=exit_code,
                )
            )
            pending = None
        elif role == "user":
            if pending is None:
                audit["orphan_user"] += 1
                continue
            observation = content if content.startswith("OBSERVATION:") else (
                content[content.find("OBSERVATION:") :] if "OBSERVATION:" in content[:200] else None
            )
            exit_code = None
            body = None
            if observation is not None:
                body = observation[len("OBSERVATION:") :].strip()
            else:
                return_match, output_match = RC_PAT.search(content), OUT_PAT.search(content)
                if return_match and output_match:
                    exit_code = int(return_match.group(1))
                    body = output_match.group(1)
                    audit["klear_adapter"] += 1
            if body is not None:
                audit["explicit_exit"] += int(exit_code is not None)
                audit["missing_exit"] += int(exit_code is None)
                events.append(
                    make_event(
                        pending["command"],
                        body,
                        path=pending["path"],
                        view_range=pending["view_range"],
                        exit_code=exit_code,
                    )
                )
                pending = None
    return events, dict(audit)


def parse_osw(messages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    events: list[dict[str, Any]] = []
    pending: dict[str, Any] | None = None
    audit: Counter[str] = Counter()
    for message_index, message in enumerate(messages):
        role = message.get("role")
        content = str(message.get("content") or "")
        if role == "assistant":
            for call in _calls(message.get("tool_calls")):
                audit["tool_calls"] += 1
                name, args = _args(call)
                raw_command = args.get("command")
                if not isinstance(raw_command, str) or not raw_command.strip():
                    audit["unsupported_missing_command"] += 1
                    continue
                command = raw_command.splitlines()[0]
                path = str(args["path"]) if args.get("path") else None
                view_range = args.get("view_range")
                if view_range is not None:
                    audit["view_range_present"] += 1
                if path:
                    audit["path_present"] += 1
                if command_class(normalize_command(command)) == "view":
                    audit["view_commands"] += 1
                pending = {
                    "command": command,
                    "path": path,
                    "view_range": view_range,
                    "message_index": message_index,
                    "tool_name": name,
                }
        elif role == "tool" and pending is not None:
            audit["missing_exit"] += 1
            events.append(
                make_event(
                    pending["command"],
                    content,
                    path=pending["path"],
                    view_range=pending["view_range"],
                    exit_code=None,
                )
            )
            pending = None
    return events, dict(audit)
