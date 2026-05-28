# Niche Find Check — End-of-Task Verdict

## Purpose
Final aggregation pass after every epoch completes. Loads all round logs,
re-applies the four gates globally (to catch cross-round duplicates and
borderline aggregates), and writes a single machine-readable verdict.

## Inputs
- Every file matching `paradigm_shift/runs/run_013/logs/round_*.json`
- Rules: `paradigm_shift/spec/harness_rules.json`

## Procedure
1. Load every round log.
2. Concatenate all atoms that passed Gates 1-4 within their round.
3. Re-apply the 4-gate filter globally:
   - Gate 1: composite ≥ `harness_rules.composite_threshold`
   - Gate 2: `atom_id`/`source_atom_id` not in `harness_rules.quarantined_atoms`
   - Gate 3: ≥ `min_web_search_per_candidate` distinct verification sources,
     unanimous on the core claim
   - Gate 4: Belinda-strict mechanism check
4. Deduplicate by `atom_id`; if two rounds produced the same atom, keep
   the one with the higher composite score.
5. If ≥ 1 atom survives → verdict `NICHE_FOUND`.
6. Else → verdict `NICHE_NOT_FOUND`.

## Output
Write to `paradigm_shift/runs/run_013/niche_find_check.json`:

```json
{
  "verdict": "NICHE_FOUND",
  "survivors": [
    {
      "atom_id": "E3_A01",
      "composite": 0.87,
      "operator": "INDUCES",
      "mechanism": "...",
      "primary_quote": "..."
    }
  ],
  "drop_counts": {
    "gate_1_threshold": 12,
    "gate_2_quarantine": 3,
    "gate_3_cross_llm": 7,
    "gate_4_belinda": 5
  },
  "rounds_scanned": 7,
  "timestamp": "2026-05-27T12:34:56Z"
}
```

For `NICHE_NOT_FOUND`, `survivors` is `[]` and the agent must include
`drop_counts` plus a short prose summary in a top-level `notes` field
explaining why no atom passed all four gates.

## Archive
After writing the verdict:
1. Copy every `round_*.json` log to
   `paradigm_shift/runs/run_013/archive/<UTC-timestamp>/`.
2. Truncate `paradigm_shift/runs/run_013/logs/` so the next run starts
   clean.
3. Update the HMAC checkpoint (`.checkpoint.json`) with `phase:
   "niche_find_check"` and `completed: true`.

The hook's HMAC verification will refuse to mark the run as complete
unless the verdict file exists and the checkpoint MAC verifies.

## [REPORT FINAL] and your final summary

When you attempt to end the task, the Stop hook
(`paradigm_shift/hooks/post_tool.py`) injects **once**:

```
[REPORT FINAL]
--- round_1.json ---
<verbatim>
--- round_2.json ---
<verbatim>
...
[END REPORT FINAL]
```

This aggregates every round log byte-for-byte — code-injected ground truth.
After it appears, write your **final summary** of the whole run. That summary
is **not** verified against the `[REPORT FINAL]` data and may diverge — the
user compares the two to judge whether your end-of-run narrative matches the
raw logs. The hook blocks the stop only once (a `final_report_injected` flag
in `task_state.json` prevents a continue loop); after you write the summary,
the next stop succeeds.
