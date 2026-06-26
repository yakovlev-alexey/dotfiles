from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class Decision:
    decision: str
    reason: str = ""

    @property
    def denied(self) -> bool:
        return self.decision == "deny"


def load_json_config(handler_file: str, hook_id: str) -> dict[str, Any]:
    config_path = Path(handler_file).with_name(f"{hook_id}.json")
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def extract_first_string(data: Any, paths: list[tuple[str, ...]]) -> str | None:
    for path in paths:
        current = data
        for key in path:
            if not isinstance(current, dict) or key not in current:
                break
            current = current[key]
        else:
            if isinstance(current, str) and current:
                return current
    return None


def find_string_key(data: Any, key_names: set[str]) -> str | None:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in key_names and isinstance(value, str) and value:
                return value
        for value in data.values():
            found = find_string_key(value, key_names)
            if found:
                return found
    elif isinstance(data, list):
        for value in data:
            found = find_string_key(value, key_names)
            if found:
                return found
    return None


def extract_command(payload: dict[str, Any]) -> str | None:
    direct = extract_first_string(
        payload,
        [
            ("command",),
            ("tool_input", "command"),
            ("toolInput", "command"),
            ("args", "command"),
            ("output", "args", "command"),
        ],
    )
    return direct or find_string_key(payload, {"command", "cmd"})


def extract_cwd(payload: dict[str, Any]) -> str:
    cwd = extract_first_string(
        payload,
        [
            ("cwd",),
            ("currentWorkingDirectory",),
            ("working_directory",),
            ("workingDirectory",),
            ("workspaceRoot",),
            ("args", "cwd"),
            ("output", "args", "cwd"),
        ],
    )
    return cwd or os.getcwd()


def decide_shell_payload(
    payload: dict[str, Any],
    config: dict[str, Any],
    decide_command: Callable[[str, str, dict[str, Any]], Decision],
) -> Decision:
    if os.environ.get(config["bypassEnv"]) == "1":
        return Decision("allow")

    command = extract_command(payload)
    if not command:
        return Decision("allow")

    return decide_command(command, extract_cwd(payload), config)


def emit_native(client: str, decision: Decision, hook_event_name: str = "PreToolUse") -> int:
    if not decision.denied:
        print("{}")
        return 0

    if client == "cursor":
        print(decision.reason, file=sys.stderr)
        return 2

    if client in {"codex", "claude"}:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": hook_event_name,
                        "permissionDecision": "deny",
                        "permissionDecisionReason": decision.reason,
                    }
                },
                separators=(",", ":"),
            )
        )
        return 0

    print(json.dumps({"decision": "deny", "reason": decision.reason}, separators=(",", ":")))
    return 0


def run_cli(
    *,
    hook_id: str,
    decide_payload: Callable[[dict[str, Any]], Decision],
    clients: tuple[str, ...] = ("cursor", "codex", "claude", "opencode"),
    hook_event_name: str = "PreToolUse",
) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, choices=clients)
    parser.add_argument("--format", choices=["native", "decision"], default="native")
    parser.add_argument("--hook-id", default=hook_id)
    args = parser.parse_args()

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    try:
        decision = decide_payload(payload)
    except Exception as error:  # Fail open on implementation errors.
        print(f"{args.hook_id} failed open: {error}", file=sys.stderr)
        return 0

    if args.format == "decision":
        print(json.dumps({"decision": decision.decision, "reason": decision.reason}, separators=(",", ":")))
        return 0

    return emit_native(args.client, decision, hook_event_name)
