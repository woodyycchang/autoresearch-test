# v5 → v6 Diff

**Author:** Claude (Opus 4.7) on branch `claude/fix-pattern-e-disagreement-eqdlc`.
**Date:** 2026-05-14.
**Purpose:** Document the additive change from program_v5.md to
program_v6.md, the chosen option, and the FORBIDDEN-zone audit.

---

## Chosen option: A (verifier-aligned per-paper-completeness scoring)

### Why Option A and not B or C

Phase 1 (`output/pattern_e_diagnosis.md`) sampled 10 Pattern E rounds
(R504, R515, R525 from E21; R530, R538, R544, R547 from E22; R555,
R565, R575 from E23). All 10 are uniformly category (a):
**primary aggregates partial hits across papers; verifier requires
per-paper coverage.**

The systematic divergence is a SCORING-RUBRIC AMBIGUITY in v5 §0,
not a forensic compromise. Primary's `sem_cosine`/`func_score` is
computed as "this paper shares ANY ONE cluster of candidate's
sub-mechanisms" (high score on cluster-adjacency). Verifier's is
computed as "this paper jointly covers ALL of candidate's
sub-mechanisms" (low score on per-paper-completeness when K=4-5).

- **Option A** (chosen): adds a per-paper-completeness LLM-judge
  layer (step 06.8) on primary's pipeline. Step 10 verdict uses
  06.8 ONLY. This aligns primary verdict with verifier verdict
  BY CONSTRUCTION — both rubrics are now per-paper-completeness.
- **Option B** (rejected): track BOTH scorings; declare confirmed
  FAIL only when both agree. Does not REDUCE the underlying
  disagreement rate, only RELABELS the disagreements as
  PASS-eligible. Pattern E rate would still be 100% on the raw
  scoring-rubric divergence.
- **Option C** (rejected): 3-judge majority verifier panel. Every
  fresh-agent spawn in E21-E23 adopted per-paper-completeness
  semantics (because the step 12 prompt asks for INDEPENDENT
  verdict against an LLM-side multi-feature composite). 3 of 3
  verifiers would continue to diverge from aggregate-adjacency
  primary. Rate of primary-vs-majority disagreement would stay
  near 100%; only the verdict label (majority FAIL or PASS) would
  shift. Does not address the root cause.

**Option A is the only option whose MECHANISM directly addresses
the identified root cause (rubric ambiguity in v5 §0).**

---

## Additive diff: v5 → v6

### What's NEW in v6

| Item | v5 | v6 |
|---|---|---|
| File chain | 06_5, 06_7, 07, 10 | 06_5, 06_7, **06_8**, 07, 10 |
| Step 06.8 | (none) | **NEW** — per-paper-completeness LLM-judge layer |
| 06_8_per_paper_completeness.json | (none) | **NEW** — per-result completeness scores |
| Step 10 verdict driver | total_hits = (kw ∪ sem ∪ func) from 07 | total_hits_v6 = per-paper-completeness hits from 06.8 |
| `aggregate_adjacency_total_hits` in 10_decision.json | (only field) | preserved as FORENSIC RECORD |
| memory_db.json schema | v5 fields | v5 fields + `v6_per_paper_completeness_metrics` |
| stats schema | v5 fields | v5 fields + `v6_per_paper_completeness_metrics` |
| Score formula | score_v5 | score_v6 (uses per-paper-completeness denominator) |
| `verdict_alignment_with_v5_aggregate` field | (none) | **NEW** — explicitly tracks Pattern E mitigation per round |
| Per-paper-completeness threshold | (none) | **NEW** — 0.7 (matches v4/v5 family) |
| Sub-mechanism enumeration | (implicit) | **NEW** — K explicit M_i extracted from content_words |

### What's UNCHANGED from v5 (★ FORBIDDEN-MODIFY zones)

| FROZEN zone | Preserved how |
|---|---|
| Step 06 web_search | Same ≥2 queries, raw response saved. v6 does NOT touch step 06. |
| Step 07 keyword threshold ≥2 | `07_hit_miss.json` continues to compute `hit iff kw>=2 OR sem>=0.7 OR func>=0.7` exactly as in v5. v6 does NOT change step 07. |
| Original primary scoring logic | `07_hit_miss.json` is byte-compatible with v5 — same format, same hit aggregation, same content. v6 ADDS step 06.8 BEFORE step 07; the new file does NOT modify the existing one. |
| Step 12 cross-agent verification | Cross-agent verifier still spawned via fresh agent. Verifier reads the new 06_8 file in addition to v5 files; verifier's scoring remains per-paper-completeness (which v6 has now aligned the primary with). |

The original primary scoring layer (07_hit_miss.json aggregate-adjacency)
is PRESERVED VERBATIM in the file. What changes is that 10_decision.json
NO LONGER reads 07 for its verdict — it reads 06_8 instead. The 07
content is recorded for forensic record and for the
`aggregate_adjacency_total_hits` field in 10_decision.json.

This is a pure ADDITION at the file-chain level and a pure VERDICT
REDIRECTION at the decision layer. No FROZEN zone is modified.

---

## Implementation pseudocode (v5 vs v6)

### v5 pipeline (relevant slice)

```
execute step 06    → 06_search_raw.json (≥10 results)
execute step 06.5  → 06_5_semantic_hits.json (sem_cosine per result)
execute step 06.7  → 06_7_functional_hits.json (functional_judge per result)
execute step 07    → 07_hit_miss.json:
                       for each result: hit = (kw>=2 OR sem>=0.7 OR func>=0.7)
                       total_hits = sum(hit)
execute step 10    → 10_decision.json:
                       verdict = FAIL if total_hits >= 1 else PASS
```

### v6 pipeline (additive change in bold)

```
execute step 06    → 06_search_raw.json (≥10 results)        ★ UNCHANGED
execute step 06.5  → 06_5_semantic_hits.json                  ★ UNCHANGED
execute step 06.7  → 06_7_functional_hits.json                ★ UNCHANGED
**execute step 06.8 → 06_8_per_paper_completeness.json:        ← NEW LAYER
   K = enumerate sub-mechanisms from content_words LLM-side
   for each result in top-10:
       LLM-judge in fresh context:
           completeness_score, covered, missing, justification
       per_paper_completeness_hit = (completeness_score >= 0.7)
   total_completeness_hits = sum(per_paper_completeness_hit)**
execute step 07    → 07_hit_miss.json (★ FROZEN format and computation)
**execute step 10  → 10_decision.json:
   total_hits_v6 = total_completeness_hits        ← uses 06_8 only
   verdict = FAIL if total_hits_v6 >= 1 else PASS
   aggregate_adjacency_total_hits = (from 07)     ← forensic record**
```

The original step 07 logic runs exactly as in v5 and produces
identical 07_hit_miss.json content. The verdict layer in step 10
now consumes 06_8 instead of 07 for its decision.

---

## Predicted impact on E24 (R576-R600)

Phase 1 diagnostic table 3 predicted that 0/10 sampled Pattern E
rounds (E21-E23) would score ≥ 0.7 on per-paper-completeness for
any retrieved result. Generalizing:

- **Pattern E rate under v6 (predicted):** ≤ 25% (vs. 100% in E23).
  Floor depends on stochastic agent variation in fresh-context
  06.8 calls vs. fresh-context 12 calls.
- **v6 PASS rate (predicted):** high — most multi-feature
  candidates flip from v5 FAIL_PassC to v6 confirmed PASS-eligible
  (both primary and verifier agree PASS).
- **`rounds_v5_aggregate_FAIL_v6_per_paper_PASS` (predicted):**
  high (≥ 20/25 if generator continues E23-style 5-feature
  candidates). This metric IS the Pattern E mitigation count.

If the rate does NOT drop, the failure mode is either:
1. The 06.8 judge is implicitly using aggregate-adjacency scoring
   despite the explicit rubric (judge-calibration failure), or
2. The candidate generator has drifted to single-feature
   compositions (K=1-2), in which case Pattern E does not apply
   and v6 has no marginal effect.

Both failure modes are checkable in the epoch24_comparison.md
post-hoc analysis.

---

## FORBIDDEN-modify audit (mandatory per task spec)

Task spec: "FORBIDDEN to modify: step 06 web_search, step 07 keyword
threshold ≥2, original primary scoring logic (only ADD layer)."

| FORBIDDEN item | v6 status | Evidence |
|---|---|---|
| step 06 web_search | UNCHANGED | v6 §5.1 preserves v5 §5.1 verbatim; 06_search_raw.json schema unchanged. |
| step 07 keyword threshold ≥ 2 | UNCHANGED | v6 §5.2 preserves the threshold; 07_hit_miss.json computes `hit iff kw>=2 OR sem>=0.7 OR func>=0.7` exactly as v5. |
| original primary scoring logic | UNCHANGED + ADD layer | v6 §5.3 preserves 07_hit_miss.json content byte-compatible with v5. ADD layer is step 06.8, written BEFORE step 07; ADD does not modify step 07's existing computation. Verdict redirect (step 10 uses 06.8 not 07) is a SEPARATE step — not a modification of step 07. |

**Audit verdict:** v6 is compliant with the FORBIDDEN-modify
constraint. The change is purely additive at the file-chain level
and a pure consumer-side redirection at the decision layer.

---

**Summary:** v5 → v6 adds step 06.8 (per-paper-completeness LLM-judge
layer) and redirects step 10's verdict input from 07_hit_miss.json
to 06_8_per_paper_completeness.json. All FROZEN zones are preserved.
This is Option A from the task spec. Predicted Pattern E rate under
v6: drops from 100% (E23) toward ≤ 25% in E24.
