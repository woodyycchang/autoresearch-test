# Run 13 — Mac Setup

This run uses a hook-enforced pipeline. Every tool call goes through
`paradigm_shift/hooks/pre_tool.py`, which validates the parent process
and the HMAC checkpoint before letting the call proceed. The hook lives
in the repo; the activation (`~/.claude/settings.json`) lives on your
Mac. This doc covers the install, reset, verify, and emergency-disable
flows.

## 0. The lockout incident (read this first)

Run 13 attempt 1 wrote `parent_process_check.allowed_regexes` too
narrowly — it whitelisted `claude` and `node` but not the
`/bin/sh -c 'python3 .../pre_tool.py'` wrapper that Claude Code
actually uses to spawn hooks. The hook blocked itself on the first
tool call after activation, and we could not commit a fix from inside
the locked container.

The fix shipped in this run:
- adds the regex `.*pre_tool\.py($|\s|")` to `harness_rules.json`
- ships the activation as an installer script (`setup_hook.sh`), so
  you can revert by `mv`-ing one file (see §5).
- ships a test that simulates Claude Code's exact invocation pattern
  (`test_pre_tool.py::test_13`) — that test now runs on every CI / local
  test pass with the parent check enabled.

## 1. Prerequisites
- Python 3.10+ (`python3 --version`)
- Claude Code CLI installed and on `$PATH`
- A clone of this repo somewhere local (path doesn't matter — the
  installer reads its own location)

## 2. Install the hook (one command)

```bash
cd ~/code/autoresearch-test          # or wherever you cloned
./paradigm_shift/hooks/setup_hook.sh
```

The installer:
1. Copies `paradigm_shift/hooks/pre_tool.py` to
   `~/.claude/hooks/pre_tool.py`.
2. Writes `~/.claude/settings.json` wiring the hook into the
   `PreToolUse` matcher (`*` — every tool call).
3. Generates a per-session 32-byte HMAC key at
   `.claude/.checkpoint-key` inside the repo (gitignored; mode 0400).
4. Backs up any pre-existing `~/.claude/settings.json` and
   `~/.claude/hooks/pre_tool.py` with a timestamped `.bak.<ts>`
   suffix.

Re-running is safe. Each run backs up the previous state before
writing.

## 3. Alternative: symlink instead of copy

If you'd rather keep the hook live-editable from the repo:

```bash
mkdir -p ~/.claude/hooks
ln -sf "$(pwd)/paradigm_shift/hooks/pre_tool.py" ~/.claude/hooks/pre_tool.py
./paradigm_shift/hooks/setup_hook.sh    # still writes settings.json + key
```

`setup_hook.sh` happily overwrites the symlink target check — it `cp`s
the file. If you want to keep the symlink, skip the installer for the
hook copy and let it handle `settings.json` only by removing the
`cp` line, or just `ln -sf` again after each install.

## 4. Verify the hook is active

Open a Claude Code session in this repo and run any read-only tool call
(e.g., `ls`). The hook runs silently on allow. For a direct check:

```bash
/bin/sh -c "python3 ~/.claude/hooks/pre_tool.py" && echo "hook allow OK"
```

Exit 0 means allow; exit 2 prints the block reason on stderr.

You can also tail the hook by temporarily inserting
`print("...", file=sys.stderr)` near the top of `main()` in
`~/.claude/hooks/pre_tool.py`.

## 5. Emergency disable

If the hook locks you out:

```bash
mv ~/.claude/settings.json ~/.claude/settings.json.disabled
```

That's it — Claude Code stops invoking the hook on the next tool call.
Re-enable by reversing the move, or by re-running the installer.

**Caveat — this only works from a real terminal.** The `PreToolUse`
hook gates *Claude Code's* tool calls, not your shell. On the local CLI
you recover by running the `mv` in a separate OS terminal (or by killing
the Claude Code process); neither path goes through the hook. A
repo-level `.claude/HOOK_DISABLED`-style bypass that you create *with
Claude's own Bash tool* is **not** a reliable escape: with `matcher: "*"`
that `touch`/`mv` is itself a tool call and is blocked by the same hook.
In a web/cloud session there is no out-of-band terminal, so a true block
is unrecoverable from inside the session — see §9.

## 6. Reset state between runs

```bash
# Wipe round logs but keep the spec
rm -rf paradigm_shift/runs/run_013/logs/*
rm -f  paradigm_shift/runs/run_013/.checkpoint.json

# Rotate the HMAC key for a fresh session (installer regenerates it)
rm -f .claude/.checkpoint-key
./paradigm_shift/hooks/setup_hook.sh
```

The installer regenerates the key only if it's missing — that's what
`rm` first triggers.

## 7. Run the tests

```bash
python3 paradigm_shift/hooks/test_pre_tool.py
```

All 14 tests run with the parent-process check **enabled** to catch a
real regression of the lockout. There is intentionally no skip-env
shortcut for the test suite.

## 8. File map

| Path                                          | Purpose                                |
| --------------------------------------------- | -------------------------------------- |
| `paradigm_shift/spec/harness_rules.json`      | Source of truth for the four gates,    |
|                                               | parent regex list, HMAC config         |
| `paradigm_shift/spec/few_shot_prompt.md`      | What the agent should do each epoch    |
| `paradigm_shift/spec/niche_find_check.md`     | End-of-task verdict procedure          |
| `paradigm_shift/spec/SETUP.md`                | This document                          |
| `paradigm_shift/hooks/pre_tool.py`            | The hook itself                        |
| `paradigm_shift/hooks/test_pre_tool.py`       | 10 unit tests + 4 e2e tests            |
| `paradigm_shift/hooks/setup_hook.sh`          | Mac installer                          |
| `~/.claude/settings.json` (on your Mac)       | Activation — NOT in the repo           |
| `~/.claude/hooks/pre_tool.py` (on your Mac)   | Active hook copy — written by installer|
| `.claude/.checkpoint-key` (in the repo)       | Per-session HMAC key, gitignored       |

## 9. Verification status (Run 13)

The hook was validated in a Claude Code **web** session on 2026-05-28 **by
safe simulation only — it was never live-activated** (`.claude/settings.json`
was never written), to avoid repeating the attempt-1 lockout (§0).

| Check | Method | Result |
|-------|--------|--------|
| Unit + e2e tests | `python3 paradigm_shift/hooks/test_pre_tool.py` | 14/14 pass (parent check enabled) |
| Allow path | spawned `/bin/sh -c "python3 …/pre_tool.py"` | exit 0 |
| Block path | suite tests 08/09/10/14 (non-matching parents) | exit 2 |
| Container lockout? | read `/proc/<ppid>/cmdline` of a tool call | No (see below) |

**Process-tree analysis.** In this container a tool call's parent is the
Claude Code Bash wrapper, a `/bin/bash -c "source …/.claude/shell-snapshots/…
&& … >| /tmp/claude-<id>-cwd"`. Its cmdline contains `/tmp/claude-<id>-cwd`,
whose `/claude-` substring matches the first allowed regex
`(^|/)claude($|\s|-)`. The grandparent is the literal `claude …` process.
The HMAC vector was dormant (no `runs/run_013/.checkpoint.json`, so the
checkpoint check short-circuits to allow). Net: a real `matcher: "*"`
activation here would have **allowed** normal tool calls — the widened
regex fix (§0) is effective in this environment.

**Robustness caveat.** The fifth regex `.*pre_tool\.py($|\s|")` matches
*any* parent cmdline that merely contains the string `pre_tool.py`. That is
the safe direction for lockout-avoidance, but it is permissive: a shell
whose command line happens to reference the hook path is treated as
authorized.

### Recovery: what actually works

Attempt 1's recovery story — and this run's originally-proposed
`.claude/HOOK_DISABLED` file — assumed you can disable the hook from inside
the locked session. **You cannot, with `matcher: "*"`**: the disabling
`touch`/`mv` is itself a tool call, blocked by the same hook. The
mechanisms that *do* work:

1. **Local CLI:** run `mv ~/.claude/settings.json …disabled` from a
   *separate* OS terminal, or kill the Claude Code process. The hook gates
   Claude Code's tools, not your shell.
2. **Web/cloud session:** rely on **container ephemerality**. `.claude/` is
   gitignored and never committed, so a fresh session clones `main` without
   the activation and the hook is simply inactive. No work is lost, because
   the hook itself lives in `main`.

### Recommendation

**Activate the hook on the local CLI, not in a web/cloud session.** The
local terminal provides an out-of-band escape (separate terminal / kill the
process); a cloud session does not, so a misconfigured regex there is
unrecoverable until the container is recycled.

## 10. [REPORT] injection — code-truth vs LLM-interpretation

Run 13 also ships a second hook, `paradigm_shift/hooks/post_tool.py`, wired by
`setup_hook.sh` on two events:

| Event | Mechanism | Emits |
| ----- | --------- | ----- |
| PostToolUse | `hookSpecificOutput.additionalContext` | `[REPORT N]` + current round log, verbatim |
| Stop / SubagentStop | `decision:"block"` + `reason` (one-shot) | `[REPORT FINAL]` + all round logs, verbatim |

**Design — two-part output.**

- The `[REPORT N]` / `[REPORT FINAL]` blocks are **code-injected ground
  truth**: `post_tool.py` reads the round logs byte-for-byte and wraps them in
  the marker. They cannot be paraphrased or hallucinated by the model.
- The model's prose summary written *after* each block is **interpretation**:
  it is never checked against the block, so it *can* drift or hallucinate —
  intentionally. Comparing the two shows whether the model reads its own logs
  accurately.
- `report_counter` in `task_state.json` increments once per injection, so the
  markers form a strictly increasing `[REPORT 1]`, `[REPORT 2]`, … that the
  model sees as exact literal tokens.

**Schema reality (why the code differs from the original sketch).** The sketch
used `{"decision":"approve","additionalContext":…}`. The actual Claude Code
contract is: PostToolUse adds context only via
`hookSpecificOutput.additionalContext` (no `approve`), and Stop has **no**
`additionalContext` field — the only way to inject text at Stop is
`decision:"block"` + `reason`, which *forces one more turn*. `post_tool.py`
therefore blocks the stop exactly once (guarded by `final_report_injected`) to
deliver `[REPORT FINAL]`, then lets the agent stop.

**Safety.** PostToolUse cannot block a tool call (the tool already ran), so it
adds no lockout risk. The Stop hook's one-shot guard prevents an infinite
continue loop; if `task_state.json` is not writable the hook declines to block
rather than risk a loop. As with the enforcement hook, **activation happens on
the local CLI via `setup_hook.sh`, never in a web/cloud session** (§9). It was
not activated here — only verified by simulation
(`paradigm_shift/hooks/test_post_tool.py`, 7/7 passing).
