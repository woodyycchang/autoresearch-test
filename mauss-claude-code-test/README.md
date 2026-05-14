# Mauss × Claude Code Production Test

Test whether Mauss-style obligations injected via `CLAUDE.md` improve task completion when Claude Code spawns multiple subagents.

## Hypothesis

Based on prior work (gpt-4o-mini, N=530, +19.2pp), Mauss obligations (ACCEPT/GIVE/RECIPROCATE) reduce multi-agent coordination failures. This test extends to a production multi-agent system (Claude Code).

## Setup

- `project_A_baseline/`: Claude Code default behavior, no CLAUDE.md modification
- `project_B_mauss/`: Same tasks + Mauss CLAUDE.md auto-loaded

## Methodology

For each of 10 Python coding tasks, a two-stage multi-agent pipeline is run in
both projects:

1. **Implementer** subagent — reads task, writes solution + unit tests.
2. **Validator** subagent — reads implementer's output, runs tests, fixes
   failures if any, writes a 1-line summary to `output.txt`.

The validator does NOT see the original task description. It only sees the
implementer's handoff. This forces the implementer to communicate context
forward — exactly the situation where Mauss obligations (GIVE, RECIPROCATE)
should help.

The pipeline is identical in both projects. The ONLY difference is that
project_B subagents are instructed to follow the Mauss obligations from
`CLAUDE.md`.

## Expected outcomes

- Δ > +20pp → strong production validation
- Δ +5 to +20pp → measurable signal
- Δ ~0pp → strong model immune to Mauss (consistent with our gpt-4o finding)
- Δ < 0 → Mauss interferes

## Reference

- Prior empirical validation: see https://github.com/woodyycchang/autoresearch-test/blob/main/RESULTS.md (if exists)
- Theoretical basis: Marcel Mauss, *The Gift* (1925) — three obligations of cooperation
- Comparison baseline: MAST paper (Cemri et al., NeurIPS 2025) +15.6pp via topology change
