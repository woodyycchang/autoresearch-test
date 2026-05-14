# Mauss × Claude Code Production Test (HARD TASKS v2)

## Why v2

v1 result was Δ=0pp because tasks were too easy for Sonnet 4.5 — both projects scored 10/10. We need tasks HARD enough that coordination failures actually cause test failures.

## v2 Tasks

10 multi-file, multi-component tasks designed to FORCE coordination:
- Each task needs 3+ files that must agree on types/contracts
- Each has 15-30 unit tests with edge cases
- Failure modes are listed in each task description (these are the modes Mauss should reduce)

## Setup (same as v1)

```
project_A_baseline/   ← no CLAUDE.md modification
project_B_mauss/      ← + Mauss CLAUDE.md auto-loaded by Claude Code
```

## Critical fix from v1

In v1 the Task tool subagents didn't auto-read CLAUDE.md — the prompt had to be manually injected. **In v2 we must verify this works.** If CLAUDE.md auto-loading fails on subagents:
- Either spawn child `claude` processes via Bash (those WILL read CLAUDE.md)
- Or document that production CLAUDE.md doesn't propagate to subagents (itself a finding)

## Hypothesis

If Mauss really works:
- Δ > +10pp on these HARD tasks → strong production validation
- Δ +5 to +10pp → measurable
- Δ ~0pp on hard tasks too → effect is mini-model specific only

## Reporting

Same SCORING.md format. Score each task ✅/⚠️/❌ based on pytest output.
