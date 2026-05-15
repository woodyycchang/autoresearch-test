# How to run the frontier test

## Goal

Test if Mauss prompt obligations improve Opus 4.7 (or any frontier model) on cross-file coordination tasks where simple single-agent thinking might miss dependencies.

## Setup

10 scenarios, each in `scenarios/scenario_NN_*/`. Each scenario has:
- `README.md` — task description (what Claude Code sees)
- `src/` — initial code
- `tests/test_visible.py` — passes initially (don't break)
- `hidden_tests/test_hidden.py` — kept hidden from Claude Code; we run AFTER

## Two conditions per scenario

### Baseline run

1. Open Claude Code in `scenarios/scenario_NN_*/`
2. Tell it:
   > Read README.md and complete the task. Run `pytest tests/` to verify the visible test passes. Don't read hidden_tests/.

3. After Claude Code finishes, YOU run:
   ```bash
   cd scenarios/scenario_NN_*/
   pytest tests/ hidden_tests/
   ```
4. Record: pass count for hidden tests.

### Mauss run

1. **Same scenario folder, but copy `CLAUDE_MAUSS.md` to `CLAUDE.md` first:**
   ```bash
   cp CLAUDE_MAUSS.md scenarios/scenario_NN_*/CLAUDE.md
   ```
2. Open Claude Code in scenario folder (it will auto-read CLAUDE.md)
3. **If you find subagent prompts don't pick up CLAUDE.md** (Claude Code Task tool issue), tell Claude Code:
   > Read CLAUDE.md. When you spawn subagents, inject those Mauss obligations into their prompts manually.
4. Same task instructions as baseline.
5. Run hidden tests. Record.

## Critical: reset between conditions

Between baseline and Mauss runs of the same scenario:
```bash
cd scenarios/scenario_NN_*/
git checkout -- src/ tests/
rm -f CLAUDE.md
```

## Scoring

For each scenario:
- **Visible tests** must always pass (otherwise it's a basic failure, doesn't count)
- **Hidden tests**: count which pass. Score = hidden_pass / total_hidden.

## Expected outcomes

- **Δ > +20pp average** → strong frontier validation (paper-worthy)
- **Δ +5-20pp** → measurable effect
- **Δ ~0pp** → frontier model immune even to coordination forcing
- **Δ < 0** → Mauss interferes
