"""Unit + end-to-end tests for paradigm_shift/hooks/pre_tool.py.

Every test runs WITHOUT the AUTORESEARCH_HOOK_SKIP_PARENT_CHECK env var
to exercise the real parent-process detection path, including the regex
that was widened after the Run 13 lockout incident (parent /bin/sh -c
python3 .../pre_tool.py).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

HOOK_DIR = Path(__file__).resolve().parent
HOOK = HOOK_DIR / "pre_tool.py"
REPO_ROOT = HOOK_DIR.parent.parent
SPEC_RULES = REPO_ROOT / "paradigm_shift" / "spec" / "harness_rules.json"

sys.path.insert(0, str(HOOK_DIR))
import pre_tool  # noqa: E402


def _allowed_regexes() -> list[str]:
    rules = json.loads(SPEC_RULES.read_text())
    return rules["parent_process_check"]["allowed_regexes"]


def _clean_env() -> dict:
    env = os.environ.copy()
    env.pop("AUTORESEARCH_HOOK_SKIP_PARENT_CHECK", None)
    return env


class ParentRegexUnitTests(unittest.TestCase):
    """Pure-regex tests against the shipped harness_rules.json patterns."""

    def setUp(self) -> None:
        self.regexes = _allowed_regexes()

    def test_01_allows_bare_claude(self):
        self.assertTrue(pre_tool.parent_process_allowed("claude", self.regexes))

    def test_02_allows_claude_with_path(self):
        self.assertTrue(
            pre_tool.parent_process_allowed("/usr/local/bin/claude --foo", self.regexes)
        )

    def test_03_allows_claude_code(self):
        self.assertTrue(
            pre_tool.parent_process_allowed(
                "/opt/homebrew/bin/claude-code --serve", self.regexes
            )
        )

    def test_04_allows_node_running_claude(self):
        self.assertTrue(
            pre_tool.parent_process_allowed(
                "node /usr/lib/claude/cli.js", self.regexes
            )
        )

    def test_05_allows_python_running_pre_tool(self):
        self.assertTrue(
            pre_tool.parent_process_allowed(
                "python3 paradigm_shift/hooks/pre_tool.py", self.regexes
            )
        )

    def test_06_allows_python_running_test_pre_tool(self):
        self.assertTrue(
            pre_tool.parent_process_allowed(
                "python3.11 paradigm_shift/hooks/test_pre_tool.py", self.regexes
            )
        )

    def test_07_allows_shell_invoking_pre_tool(self):
        """The lockout-fixing regex: /bin/sh -c '... pre_tool.py'."""
        cmdline = "/bin/sh -c python3 paradigm_shift/hooks/pre_tool.py"
        self.assertTrue(pre_tool.parent_process_allowed(cmdline, self.regexes))

    def test_08_blocks_unrelated_shell(self):
        self.assertFalse(pre_tool.parent_process_allowed("/bin/sh -c ls", self.regexes))

    def test_09_blocks_random_python_script(self):
        self.assertFalse(
            pre_tool.parent_process_allowed("python3 /tmp/attacker.py", self.regexes)
        )

    def test_10_blocks_empty_cmdline(self):
        self.assertFalse(pre_tool.parent_process_allowed("", self.regexes))


class HMACCheckpointTests(unittest.TestCase):
    def test_11_hmac_verify_passes_for_valid_checkpoint(self):
        with TemporaryDirectory() as tmp:
            key = b"x" * 32
            ckpt = Path(tmp) / "checkpoint.json"
            body = {"step": "atom_filter", "round": 3}
            payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
            mac = hmac.new(key, payload, hashlib.sha256).hexdigest()
            ckpt.write_text(json.dumps({**body, "hmac": mac}))
            self.assertTrue(pre_tool.verify_hmac_checkpoint(ckpt, key))

    def test_12_hmac_verify_fails_for_tampered_checkpoint(self):
        with TemporaryDirectory() as tmp:
            key = b"x" * 32
            ckpt = Path(tmp) / "checkpoint.json"
            body = {"step": "atom_filter", "round": 3}
            payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
            mac = hmac.new(key, payload, hashlib.sha256).hexdigest()
            body["round"] = 999  # tamper
            ckpt.write_text(json.dumps({**body, "hmac": mac}))
            self.assertFalse(pre_tool.verify_hmac_checkpoint(ckpt, key))


class EndToEndInvocationTests(unittest.TestCase):
    """Spawn the hook the way Claude Code actually spawns it.

    Reads /proc/PPID/cmdline (Linux). The container is Linux, so these
    tests exercise the same code path that triggered the Run 13 lockout.
    """

    def test_13_shell_wrapper_invocation_is_allowed(self):
        """Simulates: Claude Code → /bin/sh -c 'python3 .../pre_tool.py'."""
        env = _clean_env()
        result = subprocess.run(
            ["/bin/sh", "-c", f"exec python3 {HOOK}"],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"hook should allow real Claude invocation; stderr={result.stderr!r}",
        )

    def test_14_blocks_unauthorized_python_wrapper(self):
        """Spawn the hook from a python wrapper whose cmdline does not
        contain 'claude', 'pre_tool.py', or 'node ... claude'. The hook
        must refuse."""
        env = _clean_env()
        with TemporaryDirectory() as tmp:
            wrapper = Path(tmp) / "attacker_wrapper.py"
            wrapper.write_text(
                textwrap.dedent(
                    f"""
                    import subprocess, sys
                    r = subprocess.run(
                        [sys.executable, "{HOOK}"],
                        capture_output=True,
                    )
                    sys.stderr.buffer.write(r.stderr)
                    sys.exit(r.returncode)
                    """
                ).strip()
            )
            result = subprocess.run(
                [sys.executable, str(wrapper)],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
            )
        self.assertEqual(
            result.returncode,
            2,
            msg=f"hook should block attacker wrapper; stderr={result.stderr!r}",
        )
        self.assertIn(b"BLOCK", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
