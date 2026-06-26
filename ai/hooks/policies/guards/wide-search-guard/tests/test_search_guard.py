import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


GUARD_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = GUARD_DIR / "search_guard.py"
spec = importlib.util.spec_from_file_location("search_guard", MODULE_PATH)
search_guard = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = search_guard
spec.loader.exec_module(search_guard)


class WideSearchGuardTests(unittest.TestCase):
    def setUp(self):
        self.home = "/Users/tester"
        self.config = {
            "tools": ["rg", "grep", "ugrep"],
            "bypassEnv": "AGENT_HOOK_ALLOW_WIDE_SEARCH",
            "homeMinDepth": 2,
            "arcadiaMinDepth": 1,
        }

    def decide(self, command, cwd="/Users/tester/Repos/project"):
        with patch.dict(os.environ, {"HOME": self.home}, clear=False):
            with patch("os.path.expanduser", lambda value: self.home if value == "~" else value):
                return search_guard.decide_command(command, cwd, self.config)

    def assertDenied(self, command, cwd="/Users/tester/Repos/project"):
        decision = self.decide(command, cwd)
        self.assertEqual("deny", decision.decision, decision.reason)
        self.assertTrue(decision.reason)

    def assertAllowed(self, command, cwd="/Users/tester/Repos/project"):
        decision = self.decide(command, cwd)
        self.assertEqual("allow", decision.decision, decision.reason)

    def test_blocks_home_root(self):
        self.assertDenied("rg foo ~")
        self.assertDenied("rg foo $HOME")
        self.assertDenied("rg foo /Users/tester")

    def test_blocks_arcadia_root(self):
        self.assertDenied("rg foo ~/arcadia")
        self.assertDenied("rg foo /Users/tester/arcadia")

    def test_blocks_pathless_search_after_cd_to_arcadia(self):
        self.assertDenied("cd ~/arcadia && rg foo")

    def test_blocks_pathless_search_from_home(self):
        self.assertDenied("rg foo .", cwd="/Users/tester")

    def test_blocks_recursive_grep_in_home(self):
        self.assertDenied("grep -R foo /Users/tester")
        self.assertDenied("grep --recursive foo ~/arcadia")
        self.assertDenied("grep -R -E foo ~")

    def test_blocks_ripgrep_flags_without_values(self):
        self.assertDenied("rg -F foo ~")
        self.assertDenied("rg --files-with-matches foo ~")

    def test_allows_scoped_searches(self):
        self.assertAllowed("rg foo .")
        self.assertAllowed("rg foo ~/Repos/dotfiles")
        self.assertAllowed("rg foo ~/arcadia/frontend")
        self.assertAllowed("grep foo file.txt")

    def test_allows_explicit_bypass(self):
        self.assertAllowed("AGENT_HOOK_ALLOW_WIDE_SEARCH=1 rg foo ~/arcadia")
        self.assertAllowed("env AGENT_HOOK_ALLOW_WIDE_SEARCH=1 rg foo ~")

    def test_handles_shell_wrappers_and_command_prefix(self):
        self.assertDenied("bash -lc 'rg foo ~/arcadia'")
        self.assertDenied("command rg foo ~")

    def test_client_payload_extraction(self):
        with patch.dict(os.environ, {"HOME": self.home}, clear=False):
            with patch("os.path.expanduser", lambda value: self.home if value == "~" else value):
                decision = search_guard.decide_payload(
                    {"tool_input": {"command": "rg foo ~/arcadia"}, "cwd": "/Users/tester/Repos/project"},
                    self.config,
                )
        self.assertEqual("deny", decision.decision)


if __name__ == "__main__":
    unittest.main()
