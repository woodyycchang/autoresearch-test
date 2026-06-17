"""Tests for paradigm_shift/hooks/post_tool.py ([REPORT] injection).

Verifies the two-part output design:
  - PostToolUse emits hookSpecificOutput.additionalContext with a
    `[REPORT N]` marker wrapping the current round log VERBATIM (not
    truncated, not paraphrased), and report_counter increments in
    task_state.json.
  - Stop emits a one-shot decision:block carrying `[REPORT FINAL]` with every
    round log verbatim, then allows subsequent stops.

The hook is run as a subprocess with the event JSON on stdin, exactly how
Claude Code invokes it.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

HOOK_DIR = Path(__file__).resolve().parent
HOOK = HOOK_DIR / "post_tool.py"


def _make_rules(workspace: Path, logs_dir: Path, state_path: Path) -> Path:
    rules = {
        "logs_dir": str(logs_dir),
        "task_state_path": str(state_path),
        "report_injection": {
            "enabled": True,
            "round_glob": "round_*.json",
            "final_marker": "FINAL",
        },
    }
    rules_path = workspace / "harness_rules.json"
    rules_path.write_text(json.dumps(rules))
    return rules_path


def _run(rules_path: Path, event: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(event).encode(),
        capture_output=True,
        env={"AUTORESEARCH_RULES_PATH": str(rules_path), "PATH": "/usr/bin:/bin"},
    )


def _stdout_json(result: subprocess.CompletedProcess) -> dict | None:
    out = result.stdout.decode().strip()
    return json.loads(out) if out else None


class PostToolUseInjectionTests(unittest.TestCase):
    def test_01_emits_report_marker_with_verbatim_content(self):
        with TemporaryDirectory() as tmp:
            ws = Path(tmp)
            logs = ws / "logs"
            logs.mkdir()
            raw = '{"round": 1, "survivors": ["E1_A01"],\n "note": "he said \\"hi\\""}\n'
            (logs / "round_1.json").write_text(raw)
            rules = _make_rules(ws, logs, ws / "task_state.json")

            result = _run(rules, {"hook_event_name": "PostToolUse"})
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = _stdout_json(result)
            self.assertIsNotNone(payload)
            hso = payload["hookSpecificOutput"]
            self.assertEqual(hso["hookEventName"], "PostToolUse")
            # Exact wrapper + byte-for-byte log content (no paraphrase).
            self.assertEqual(hso["additionalContext"], f"[REPORT 1]\n{raw}\n[END REPORT 1]")
            self.assertIn(raw, hso["additionalContext"])

    def test_02_counter_increments_across_calls(self):
        with TemporaryDirectory() as tmp:
            ws = Path(tmp)
            logs = ws / "logs"
            logs.mkdir()
            (logs / "round_1.json").write_text('{"round":1}')
            state_path = ws / "task_state.json"
            rules = _make_rules(ws, logs, state_path)

            first = _stdout_json(_run(rules, {"hook_event_name": "PostToolUse"}))
            second = _stdout_json(_run(rules, {"hook_event_name": "PostToolUse"}))
            self.assertTrue(
                first["hookSpecificOutput"]["additionalContext"].startswith("[REPORT 1]")
            )
            self.assertTrue(
                second["hookSpecificOutput"]["additionalContext"].startswith("[REPORT 2]")
            )
            self.assertEqual(json.loads(state_path.read_text())["report_counter"], 2)

    def test_03_verbatim_is_not_truncated(self):
        with TemporaryDirectory() as tmp:
            ws = Path(tmp)
            logs = ws / "logs"
            logs.mkdir()
            # Large multi-line body with a unique tail sentinel.
            body = "\n".join(f'{{"line":{i},"payload":"{"x"*40}"}}' for i in range(500))
            raw = body + '\n{"TAIL_SENTINEL":"end-of-log-marker-9f3a"}\n'
            (logs / "round_1.json").write_text(raw)
            rules = _make_rules(ws, logs, ws / "task_state.json")

            payload = _stdout_json(_run(rules, {"hook_event_name": "PostToolUse"}))
            ctx = payload["hookSpecificOutput"]["additionalContext"]
            self.assertIn("end-of-log-marker-9f3a", ctx)  # tail survived
            self.assertEqual(ctx, f"[REPORT 1]\n{raw}\n[END REPORT 1]")
            self.assertGreater(len(ctx), len(raw))

    def test_04_picks_highest_numbered_round_as_current(self):
        with TemporaryDirectory() as tmp:
            ws = Path(tmp)
            logs = ws / "logs"
            logs.mkdir()
            (logs / "round_1.json").write_text('{"round":1}')
            (logs / "round_2.json").write_text('{"round":2}')
            (logs / "round_10.json").write_text('{"round":10,"current":true}')  # numeric, not lexical
            rules = _make_rules(ws, logs, ws / "task_state.json")

            ctx = _stdout_json(_run(rules, {"hook_event_name": "PostToolUse"}))[
                "hookSpecificOutput"
            ]["additionalContext"]
            self.assertIn('"round":10', ctx)
            self.assertNotIn('"round":1}', ctx.replace('"round":10', ""))

    def test_05_no_round_log_no_injection_no_increment(self):
        with TemporaryDirectory() as tmp:
            ws = Path(tmp)
            logs = ws / "logs"
            logs.mkdir()  # empty
            state_path = ws / "task_state.json"
            rules = _make_rules(ws, logs, state_path)

            result = _run(rules, {"hook_event_name": "PostToolUse"})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.decode().strip(), "")  # no injection
            self.assertFalse(state_path.exists())  # counter untouched


class StopFinalReportTests(unittest.TestCase):
    def test_06_stop_injects_final_once_then_allows(self):
        with TemporaryDirectory() as tmp:
            ws = Path(tmp)
            logs = ws / "logs"
            logs.mkdir()
            (logs / "round_1.json").write_text('{"round":1,"s":"ALPHA_SENTINEL"}')
            (logs / "round_2.json").write_text('{"round":2,"s":"BETA_SENTINEL"}')
            state_path = ws / "task_state.json"
            rules = _make_rules(ws, logs, state_path)

            first = _stdout_json(_run(rules, {"hook_event_name": "Stop"}))
            self.assertEqual(first["decision"], "block")
            self.assertIn("[REPORT FINAL]", first["reason"])
            self.assertIn("[END REPORT FINAL]", first["reason"])
            self.assertIn("ALPHA_SENTINEL", first["reason"])  # round 1 verbatim
            self.assertIn("BETA_SENTINEL", first["reason"])  # round 2 verbatim
            self.assertTrue(json.loads(state_path.read_text())["final_report_injected"])

            # Second stop attempt must NOT block (no infinite loop).
            second = _run(rules, {"hook_event_name": "Stop"})
            self.assertEqual(second.returncode, 0)
            self.assertEqual(second.stdout.decode().strip(), "")

    def test_07_stop_with_no_logs_allows_stop(self):
        with TemporaryDirectory() as tmp:
            ws = Path(tmp)
            logs = ws / "logs"
            logs.mkdir()  # empty
            rules = _make_rules(ws, logs, ws / "task_state.json")

            result = _run(rules, {"hook_event_name": "Stop"})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.decode().strip(), "")  # agent may stop


if __name__ == "__main__":
    unittest.main(verbosity=2)
