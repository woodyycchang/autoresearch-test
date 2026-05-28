#!/usr/bin/env python3
"""Pre-tool hook for Run 13's file-driven hook-enforced pipeline.

Validates two things on every tool call:
  1. Parent process is an allowed invoker (Claude Code, the hook test
     harness, or a /bin/sh wrapper that ultimately executes this hook).
  2. The HMAC checkpoint for the current run state still verifies — if a
     checkpoint exists it must match a MAC computed with the per-session
     key at `.claude/.checkpoint-key`.

Exit codes:
  0  allow the tool call
  2  block the tool call (with the reason printed to stderr)

Configuration: read from `paradigm_shift/spec/harness_rules.json`. Override
the path with the `AUTORESEARCH_RULES_PATH` env var. The
`AUTORESEARCH_HOOK_SKIP_PARENT_CHECK` env var is intentionally NOT honored
in the test suite — see `test_pre_tool.py`.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_RULES_PATH = Path("paradigm_shift/spec/harness_rules.json")
SKIP_PARENT_CHECK_ENV = "AUTORESEARCH_HOOK_SKIP_PARENT_CHECK"


def _read_rules(rules_path: Path) -> dict:
    if not rules_path.exists():
        return {}
    try:
        return json.loads(rules_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[pre_tool] could not read {rules_path}: {exc}", file=sys.stderr)
        return {}


def _parent_cmdline(ppid: int) -> str:
    """Return the parent process command line, cross-platform.

    Linux: read /proc/<ppid>/cmdline (NUL-separated argv).
    macOS / BSD fallback: `ps -p <ppid> -o command=`.
    """
    proc_cmdline = Path(f"/proc/{ppid}/cmdline")
    if proc_cmdline.exists():
        raw = proc_cmdline.read_bytes()
        return raw.replace(b"\x00", b" ").decode("utf-8", errors="replace").strip()
    try:
        out = subprocess.check_output(
            ["ps", "-p", str(ppid), "-o", "command="],
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8", errors="replace").strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def parent_process_allowed(cmdline: str, allowed_regexes: Iterable[str]) -> bool:
    for pattern in allowed_regexes:
        if re.search(pattern, cmdline):
            return True
    return False


def _checkpoint_key(key_path: Path) -> bytes | None:
    if not key_path.exists():
        return None
    try:
        return key_path.read_bytes().strip()
    except OSError as exc:
        print(f"[pre_tool] could not read key {key_path}: {exc}", file=sys.stderr)
        return None


def verify_hmac_checkpoint(checkpoint_path: Path, key: bytes) -> bool:
    if not checkpoint_path.exists():
        return True
    try:
        payload = json.loads(checkpoint_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[pre_tool] checkpoint unreadable: {exc}", file=sys.stderr)
        return False
    stored_mac = payload.pop("hmac", None)
    if not stored_mac:
        return False
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    expected = hmac.new(key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, stored_mac)


def main(argv: list[str]) -> int:
    rules_path = Path(os.environ.get("AUTORESEARCH_RULES_PATH", str(DEFAULT_RULES_PATH)))
    rules = _read_rules(rules_path)

    parent_cfg = rules.get("parent_process_check", {})
    if parent_cfg.get("enabled", True) and not os.environ.get(SKIP_PARENT_CHECK_ENV):
        ppid = os.getppid()
        cmdline = _parent_cmdline(ppid)
        allowed = parent_cfg.get("allowed_regexes", [])
        if not parent_process_allowed(cmdline, allowed):
            print(
                f"[pre_tool] BLOCK: parent process (pid={ppid}) cmdline "
                f"{cmdline!r} did not match any allowed regex.",
                file=sys.stderr,
            )
            return 2

    hmac_cfg = rules.get("hmac_checkpoint", {})
    if hmac_cfg.get("enabled"):
        key_path = Path(hmac_cfg.get("key_path", ".claude/.checkpoint-key"))
        key = _checkpoint_key(key_path)
        if key is not None:
            checkpoint_path = Path(
                rules.get(
                    "checkpoint_path",
                    "paradigm_shift/runs/run_013/.checkpoint.json",
                )
            )
            if not verify_hmac_checkpoint(checkpoint_path, key):
                print(
                    f"[pre_tool] BLOCK: HMAC checkpoint verification failed "
                    f"for {checkpoint_path}",
                    file=sys.stderr,
                )
                return 2

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
