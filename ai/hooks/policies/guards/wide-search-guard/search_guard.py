#!/usr/bin/env python3
"""Guard against broad grep-style searches in large personal trees."""

from __future__ import annotations

import os
import posixpath
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


for parent in Path(__file__).resolve().parents:
    if (parent / "lib" / "hook_runtime.py").exists():
        sys.path.insert(0, str(parent))
        break

from lib.hook_runtime import Decision, decide_shell_payload, load_json_config, run_cli


HOOK_ID = "wide-search-guard"
SEARCH_TOOLS = {"rg", "grep", "ugrep"}
SHELLS = {"bash", "zsh", "sh"}
CONTROL_TOKENS = {"|", "||", "&&", ";"}
SHORT_VALUE_OPTIONS = {
    "A",
    "B",
    "C",
    "D",
    "M",
    "e",
    "f",
    "g",
    "m",
    "t",
    "T",
}
LONG_VALUE_OPTIONS = {
    "--after-context",
    "--before-context",
    "--binary-files",
    "--colors",
    "--context",
    "--context-separator",
    "--dfa-size-limit",
    "--encoding",
    "--engine",
    "--field-context-separator",
    "--field-match-separator",
    "--file",
    "--glob",
    "--iglob",
    "--max-columns",
    "--max-count",
    "--max-depth",
    "--path-separator",
    "--pre",
    "--regexp",
    "--regex-size-limit",
    "--sort",
    "--sortr",
    "--threads",
    "--type",
    "--type-add",
    "--type-clear",
}
RECURSIVE_LONG_OPTIONS = {"--recursive", "--dereference-recursive"}


@dataclass(frozen=True)
class ParsedSearch:
    tool: str
    targets: list[str]
    pathless: bool
    recursive: bool


def load_config() -> dict[str, Any]:
    return load_json_config(__file__, HOOK_ID)


def basename(token: str) -> str:
    return posixpath.basename(token.rstrip("/"))


def is_assignment(token: str) -> bool:
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", token))


def token_sets_bypass(token: str, bypass_env: str) -> bool:
    return token == f"{bypass_env}=1" or token.startswith(f"{bypass_env}=1 ")


def split_segments(tokens: list[str]) -> list[list[str]]:
    segments: list[list[str]] = []
    current: list[str] = []
    for token in tokens:
        if token in CONTROL_TOKENS:
            if current:
                segments.append(current)
                current = []
        else:
            current.append(token)
    if current:
        segments.append(current)
    return segments


def strip_invocation_prefixes(tokens: list[str], bypass_env: str) -> tuple[list[str], bool]:
    remaining = list(tokens)
    bypass = False

    while remaining and is_assignment(remaining[0]):
        bypass = bypass or token_sets_bypass(remaining[0], bypass_env)
        remaining.pop(0)

    if remaining and basename(remaining[0]) == "env":
        remaining.pop(0)
        while remaining and (is_assignment(remaining[0]) or remaining[0].startswith("-")):
            bypass = bypass or token_sets_bypass(remaining[0], bypass_env)
            remaining.pop(0)

    while remaining and basename(remaining[0]) == "command":
        remaining.pop(0)

    return remaining, bypass


def parse_search(tokens: list[str], config: dict[str, Any]) -> tuple[ParsedSearch | None, bool]:
    bypass_env = config["bypassEnv"]
    tokens, bypass = strip_invocation_prefixes(tokens, bypass_env)
    if not tokens:
        return None, bypass

    tool = basename(tokens[0])
    if tool not in set(config["tools"]):
        return None, bypass

    positionals: list[str] = []
    pattern_from_option = False
    files_mode = False
    recursive = tool in {"rg", "ugrep"}
    index = 1
    args = tokens[1:]

    while index <= len(args):
        if index > len(args):
            break
        arg = args[index - 1]
        if arg == "--":
            positionals.extend(args[index:])
            break
        if arg == "--files":
            files_mode = True
            index += 1
            continue
        if arg in RECURSIVE_LONG_OPTIONS:
            recursive = True
            index += 1
            continue
        if arg.startswith("--"):
            name = arg.split("=", 1)[0]
            if name in {"--regexp", "--file"}:
                pattern_from_option = True
            if name in LONG_VALUE_OPTIONS and "=" not in arg:
                index += 2
            else:
                index += 1
            continue
        if arg.startswith("-") and arg != "-":
            chars = arg[1:]
            if tool == "grep" and any(char in chars for char in ("r", "R")):
                recursive = True
            if "e" in chars or "f" in chars:
                pattern_from_option = True
            if chars in SHORT_VALUE_OPTIONS:
                index += 2
            else:
                index += 1
            continue
        positionals.append(arg)
        index += 1

    if tool == "grep" and not recursive:
        return ParsedSearch(tool=tool, targets=[], pathless=False, recursive=False), bypass

    if files_mode or pattern_from_option:
        targets = positionals
    else:
        targets = positionals[1:] if positionals else []

    return ParsedSearch(tool=tool, targets=targets, pathless=not targets, recursive=recursive), bypass


def expand_path(path_value: str, cwd: str, home: str) -> str:
    value = path_value
    value = value.replace("${HOME}", home).replace("$HOME", home)
    if value == "~":
        value = home
    elif value.startswith("~/"):
        value = home + value[1:]
    if not value.startswith("/"):
        value = posixpath.join(cwd, value)
    return posixpath.normpath(value)


def classify_broad_path(path_value: str, cwd: str, config: dict[str, Any]) -> str | None:
    home = posixpath.normpath(os.path.expanduser("~"))
    path = expand_path(path_value, cwd, home)
    home_min_depth = int(config.get("homeMinDepth", 2))
    arcadia_min_depth = int(config.get("arcadiaMinDepth", 1))
    arcadia_roots = {
        posixpath.normpath(posixpath.join(home, "arcadia")),
        "/arcadia",
    }

    for arcadia_root in arcadia_roots:
        if path == arcadia_root:
            return arcadia_root
        if path.startswith(arcadia_root + "/"):
            rel = path.removeprefix(arcadia_root + "/")
            if len([part for part in rel.split("/") if part]) < arcadia_min_depth:
                return arcadia_root
            return None

    if path == home:
        return home
    if path.startswith(home + "/"):
        rel = path.removeprefix(home + "/")
        parts = [part for part in rel.split("/") if part]
        if len(parts) < home_min_depth:
            return home

    return None


def analyze_tokens(tokens: list[str], cwd: str, config: dict[str, Any]) -> Decision:
    current_cwd = posixpath.normpath(cwd)
    bypass_env = config["bypassEnv"]

    for segment in split_segments(tokens):
        normalized_segment, bypass = strip_invocation_prefixes(segment, bypass_env)
        if bypass:
            return Decision("allow")
        if not normalized_segment:
            continue

        command_name = basename(normalized_segment[0])
        if command_name == "cd":
            target = normalized_segment[1] if len(normalized_segment) > 1 else "~"
            current_cwd = expand_path(target, current_cwd, posixpath.normpath(os.path.expanduser("~")))
            continue

        if command_name in SHELLS:
            for index, token in enumerate(normalized_segment[1:], start=1):
                if "c" in token.lstrip("-") and index + 1 < len(normalized_segment):
                    nested = normalized_segment[index + 1]
                    nested_decision = decide_command(nested, current_cwd, config)
                    if nested_decision.denied:
                        return nested_decision
                    break
            continue

        parsed, bypass = parse_search(segment, config)
        if bypass:
            return Decision("allow")
        if not parsed or not parsed.recursive:
            continue

        targets = ["."] if parsed.pathless else parsed.targets
        for target in targets:
            broad_root = classify_broad_path(target, current_cwd, config)
            if broad_root:
                reason = (
                    f"Blocked broad {parsed.tool} search under {broad_root}. "
                    "Narrow the path to a repo/service subdirectory, or set "
                    f"{config['bypassEnv']}=1 only for an explicit broad inventory."
                )
                return Decision("deny", reason)

    return Decision("allow")


def decide_command(command: str, cwd: str, config: dict[str, Any]) -> Decision:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return Decision("allow")
    return analyze_tokens(tokens, cwd, config)


def decide_payload(payload: dict[str, Any], config: dict[str, Any] | None = None) -> Decision:
    return decide_shell_payload(payload, config or load_config(), decide_command)


def main() -> int:
    return run_cli(hook_id=HOOK_ID, decide_payload=decide_payload)


if __name__ == "__main__":
    raise SystemExit(main())
