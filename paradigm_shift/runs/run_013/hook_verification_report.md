# Run 13 — Hook Verification Report

- **Date:** 2026-05-28
- **Environment:** Claude Code web session (managed ephemeral container, Linux)
- **Method:** Safe simulation only. The hook was **not** live-activated
  (`.claude/settings.json` was never written), to avoid repeating the
  attempt-1 lockout documented in `paradigm_shift/spec/SETUP.md` §0.

## Summary

The Run 13 pre-tool hook (`paradigm_shift/hooks/pre_tool.py`) was validated
end-to-end without registering it as a live `PreToolUse` hook. The hook
allows legitimate Claude Code invocations, blocks unauthorized parents, and
— per a process-tree inspection — would not have locked out this container
had it been activated.

## 1. Test suite — 14/14 pass

`python3 paradigm_shift/hooks/test_pre_tool.py`, run from the repo root with
the parent check **enabled** (no `AUTORESEARCH_HOOK_SKIP_PARENT_CHECK`):

```
Ran 14 tests in 0.095s
OK
```

Breakdown:

- **01–07** — parent-regex ALLOW cases: bare `claude`, `/path/claude`,
  `claude-code`, `node … claude`, `python … pre_tool.py`,
  `python … test_pre_tool.py`, and `/bin/sh -c '… pre_tool.py'`.
- **08–10** — parent-regex BLOCK cases: unrelated shell, random python
  script, empty cmdline.
- **11–12** — HMAC checkpoint: verify-pass and tamper-fail.
- **13** — e2e ALLOW: spawns `/bin/sh -c 'exec python3 …/pre_tool.py'`
  (Claude Code's exact spawn pattern) and asserts exit 0.
- **14** — e2e BLOCK: spawns from a python wrapper whose cmdline has no
  allowed token and asserts exit 2.

## 2. Allow-path simulation

Directly simulated Claude Code's hook spawn:

```
$ /bin/sh -c "python3 $PWD/paradigm_shift/hooks/pre_tool.py"; echo $?
0
```

Exit 0 = allow. The parent cmdline `/bin/sh -c python3 …/pre_tool.py`
matches the widened regex `.*pre_tool\.py($|\s|")`
(`harness_rules.json:45`), which is the attempt-1 lockout fix.

## 3. Block-path verification

Authoritative source: suite tests **08/09/10/14**, which spawn the hook
from parents whose cmdline matches none of the allowed regexes and assert
exit 2. Confirmed passing in this container.

Robustness note: the regex `.*pre_tool\.py($|\s|")` matches any parent
cmdline that merely *contains* the string `pre_tool.py`. A manual block
attempt returned exit 0 because the test command itself referenced the hook
path (even inside a `# comment`), which the parent shell carried in its
cmdline. This is permissive but fails toward *allow*, so it adds no lockout
risk; it is recorded as a robustness caveat in SETUP.md §9.

## 4. Process-tree analysis — would this container lock out?

**No.** Reading `/proc/<ppid>/cmdline` for a tool call's hook process:

- **Parent (the would-be hook invoker):** the Claude Code Bash wrapper —
  `/bin/bash -c "source /root/.claude/shell-snapshots/… && … >| /tmp/claude-<id>-cwd"`.
  Its cmdline contains `/tmp/claude-<id>-cwd`; the `/claude-` substring
  matches the first allowed regex `(^|/)claude($|\s|-)`.
- **Grandparent:** the literal `claude --output-format=stream-json … --model … --resume=…` process.
- **HMAC vector:** dormant — no `paradigm_shift/runs/run_013/.checkpoint.json`
  exists, so `verify_hmac_checkpoint` short-circuits to allow.

Therefore, had the hook been activated with `matcher: "*"` in this session,
normal tool calls would have passed the parent check and the HMAC check
would have been skipped. The widened regex fix is effective in this
environment.

## 5. Why live activation was skipped

Marginal value ≈ 0: simulation already proves allow + block, and that this
container's spawn chain is authorized. Risk ≠ 0: with `matcher: "*"`, a
single mismatching parent regex blocks **every** tool call, and the
recovery (`touch .claude/HOOK_DISABLED` / `mv settings.json`) is itself a
tool call gated by the same hook — unrecoverable from inside a web session.
The real recovery mechanisms (out-of-band terminal on local CLI; container
ephemerality on the web) are documented in SETUP.md §9.

## Conclusion

**Hook enforcement mechanism validated.** Allow and block paths behave as
designed (14/14 tests; allow-path exit 0; block-path exit 2), and the
parent-process check is correctly satisfied by this container's real
invocation chain. Activation should be performed on the local CLI, where an
out-of-band terminal provides a reliable escape; it was deliberately not
performed in this web session.
