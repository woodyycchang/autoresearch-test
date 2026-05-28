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
