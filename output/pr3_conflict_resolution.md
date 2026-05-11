# PR #3 Conflict Resolution

**Author:** Claude (Opus 4.7), conflict resolution + epoch-4 session
**Date:** 2026-05-11
**Branch:** `claude/resolve-epoch-conflicts-ZwDrf`

---

## Why this resolution was needed

PR #3 ("Epoch 3: memory-aware self-improving pipeline") was authored when only R001–R025 existed in the repo. It added rounds **R026–R050** plus `program_v3.md`, `logs/memory_db.json`, `output/v2_to_v3_diff.md`, and `output/epoch3_comparison.md`.

Before PR #3 could merge, PR #2 ("Epoch 2: self-improving pipeline experiment") landed on `main` and added its own **R026–R050** under `program_v2.md` (Form A/B/C/D rotation + query/composition rules). The two PRs collided on every `rounds/round_026/`…`rounds/round_050/` path plus the four shared log files.

Resolution policy: **PR #2's epoch 2 stays at R026–R050; PR #3's epoch 3 is renumbered to R051–R075** so all 75 rounds sit cleanly on `main` in chronological order (epoch 1 → epoch 2 → epoch 3).

## What was renamed / merged

### Rounds (rename)

PR #3's `rounds/round_026/` … `rounds/round_050/` → `rounds/round_051/` … `rounds/round_075/`. 25 directories × ~11 files each = 275 files moved. Inside each round file, every textual reference to its own round id was updated:

- `"round": "026"` → `"round": "051"` (in `11_audit.json`)
- `fresh-subagent-round-026` → `fresh-subagent-round-051` (in `12_verification.json`)
- `rounds/round_026/...` path strings → `rounds/round_051/...` (any cross-references)

Cross-references to other rounds (e.g., R005 cited in a candidate's prior-art discussion) were intentionally **not** rewritten — they refer to R001–R025 evidence which is unchanged.

### Logs (concatenate + dedupe by round number)

| File | Strategy |
|------|----------|
| `logs/candidate_pool.md` | Kept main's R001–R050 entries (epoch 1 + epoch 2). Appended PR #3's R026–R050 entries renumbered to R051–R075 under a new `## Epoch 3 (R051-R075, program_v3.md memory-aware)` heading. |
| `logs/compliance_log.md` | Kept main's full content (epoch 1 + epoch 2 entries). Appended PR #3's epoch-3-specific compliance entries renumbered to R051–R075 under a new heading. |
| `logs/session_log.md` | Same: kept main; appended PR #3's epoch-3 session record under a new heading. |
| `logs/disagreement_log.md` | Kept main as-is (PR #3 didn't add to this file because epoch 3 had 0 disagreements by methodology). Appended a brief epoch-3 explanatory note. |

### Stats

| File | Action |
|------|--------|
| `output/stats_round_050.json` | **Kept main's version** (PR #2 epoch 2 stats). |
| `output/stats_round_075.json` | **NEW** — built from PR #3's `stats_round_050.json` data with `rounds_completed: 75`, `pass_rounds` renumbered (`034→059`, `039→064`, `043→068`, `044→069`, `050→075`), and a new `cross_epoch_summary` block describing all three epochs. |

### Program / diff / comparison docs

| File | Action |
|------|--------|
| `program_v3.md` | Copied from PR #3. §9 ("Inherited history") rewritten to reflect actual epoch-1 (R001–R025, v1), epoch-2 (R026–R050, v2), epoch-3 (R051–R075, v3) chronology. |
| `output/v2_to_v3_diff.md` | Copied from PR #3. Header note rewritten: this diff is now between `program_v2.md` and `program_v3.md`, no longer between `program.md` and `program_v3.md`. The lever changes themselves are unchanged. |
| `output/epoch3_comparison.md` | Copied from PR #3 with §0 fully rewritten to describe the conflict resolution. All R026–R050 references in the body that refer to PR #3's epoch-3 rounds renumbered to R051–R075 (the "designed for" round range). References to R001–R025 (epoch 1 evidence) left unchanged. |

### Memory DB (rebuilt with all three epochs)

`logs/memory_db.json` rebuilt from scratch:

- **R001–R025 (epoch 1, v1)** — kept verbatim from PR #3's memory_db (PR #3 had built these from the actual epoch-1 round files).
- **R026–R050 (epoch 2, v2)** — **newly added.** Built from main's actual epoch-2 round files (`05_candidate.json` + `10_decision.json` per round). Schema matches the existing entries: `{round, epoch, domain, domain_normalized, mechanism, form, forced_hit_count, hit_count, fail_reason, tried_keywords, verdict}`. Form derived from epoch-2's A/B/C/D candidate_form taxonomy (A=conjunction, B=negation-impossibility, C=quantitative-prediction, D=reverse-direction). Domain normalization re-applied with the same rule set.
- **R051–R075 (epoch 3, v3)** — taken from PR #3's R026–R050 epoch-3 entries with `round` renumbered (`+25`) and `epoch` set to 3.
- **Aggregates recomputed** across all 75 entries: `domain_fail_counts`, `form_fail_counts`, `blocked_domains_threshold_3_or_more`, `blocked_forms_threshold_5_or_more`, `frequently_tried_keywords_top_15`, `mean_forced_hit`, `mean_hit_count`. Schema bumped to `1.1`.
- **`epoch_index`** updated: epoch_1 (R001-R025, program.md), epoch_2 (R026-R050, program_v2.md), epoch_3 (R051-R075, program_v3.md). epoch_4 will be appended by this session.

## What was NOT changed

- Round files for R001–R050 in main (epoch 1 + epoch 2) — untouched.
- `program.md` and `program_v2.md` — untouched.
- `output/stats_round_025.json`, `output/epoch1_analysis.md`, `output/epoch_comparison.md`, `output/v1_to_v2_diff.md`, `output/final_report.md` — untouched.
- The 4 ★ FORBIDDEN-TO-MODIFY zones in `program_v3.md` (steps 06, 07, 10, 12) — preserved verbatim.

## Sanity check after resolution

```
rounds/         75 dirs (round_001 .. round_075)
logs/           5 files (candidate_pool, compliance, disagreement, session, memory_db)
program*.md     3 files (v1=program.md, program_v2.md, program_v3.md)
output/         8+ files including epoch3_comparison.md + stats_round_075.json
memory_db       75 round entries (epoch_1: 25, epoch_2: 25, epoch_3: 25)
```

PR #3's open state on GitHub will be superseded by this single combined PR ("Epoch 4: semantic-similarity detection (with PR #3 conflict resolution)") which carries both the conflict resolution and the epoch-4 work. PR #3 should be closed without merge.
