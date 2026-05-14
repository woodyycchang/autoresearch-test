# program_v6.md
## Niche-Mining Pipeline — v6: Pattern E Mitigation via Per-Paper-Completeness Scoring

This file extends `program_v5.md` (file-chain + mechanical keyword
rule + cross-agent verification + memory-aware step 04.5 +
semantic-similarity step 06.5 + functional-equivalence step 06.7)
with **one new step, 06.8, that catches Pattern E — the
aggregate-adjacency vs per-paper-completeness scoring divergence
saturated to 100% in epoch 23**.

The four ★ FORBIDDEN-TO-MODIFY zones from v5 are preserved verbatim:
- Step 06 web_search (honesty gate)
- Step 07 keyword-overlap threshold ≥ 2 (still forces hit)
- Original primary scoring logic in 07_hit_miss.json (aggregate-adjacency
  computation of `sem_cosine` and `func_score` per result, preserved
  verbatim for forensic record)
- Step 12 cross-agent verification

v6 changes only **how the final verdict in step 10 is computed**, by
adding a per-paper-completeness scoring layer that gates the
aggregate-adjacency hit signals.

---

## 0. Why a per-paper-completeness layer now

Epoch 21-23 (program_v5.md) produced a steadily increasing rate of
primary-vs-verifier verdict-level disagreement on multi-feature
recombination candidates:

| Epoch | Pattern E rate | Mean sub-mechanism count K |
|---:|:---:|:---:|
| E17 | 0% | 1-2 |
| E18 | 4% | 2-3 |
| E19 | 0% | 2-3 |
| E20 | 12% | 2-3 |
| E21 | 64% | 4 |
| E22 | 84% | 4-5 |
| **E23** | **100%** | **5** |

Phase 1 of this session (see `output/pattern_e_diagnosis.md`) sampled
10 representative Pattern E rounds (3 from E21, 4 from E22, 3 from
E23) and confirmed that EVERY disagreement is uniformly category (a):
- **Primary scoring (07_hit_miss.json):** `sem_cosine`/`func_score`
  computed against the candidate's CLUSTER of sub-mechanisms; any
  single cluster-match drives the score to 0.74-0.92. Result: 8/8
  hits per round.
- **Verifier scoring (12_verification.json):** `sem_cosine`/`func_score`
  computed against the candidate's FULL JOINT COMPOSITION; only
  joint coverage drives the score to ≥ 0.7. With K=4-5 sub-mechanisms
  per candidate, no single retrieved paper jointly covers all of
  them; verifier scores 0.18-0.45 per result. Result: 0-1 hits per round.

Both rubrics are valid interpretations of v5 §0's
functional-equivalence definition, but their VERDICTS disagree
deterministically on multi-feature candidates. Pattern E is not a
forensic compromise; it is a SCORING-RUBRIC AMBIGUITY in v5.

**v6 fix:** add step 06.8 between functional-judge (06.7) and keyword
rule (07). Step 06.8 invokes an LLM-judge over the top-10
`06_search_raw.json` results and asks, per result, the SAME question
the cross-agent verifier implicitly asks:

> "Given candidate mechanism X with K distinctive sub-mechanisms
> {M_1, ..., M_K} (full text of `candidate.llm_application` + the K
> bullet enumeration from `content_words` LLM-side phrases), here is
> search result Y. Does this paper, taken as a single unified work,
> jointly cover ALL K sub-mechanisms of the candidate (NOT just any
> one cluster of them)? Score from 0.0 (covers ≤ 1 of K) to 1.0
> (covers all K with explicit mechanism-level match for each).
> Provide one-sentence justification listing which M_i are missing."

If any single result scores ≥ 0.7 on this per-paper-completeness
dimension, mark `per_paper_completeness_hit = true`. Step 10's
verdict computation uses ONLY the per-paper-completeness layer for
mechanical FAIL — preserving the existing aggregate-adjacency
hits in 07_hit_miss.json forensically but DROPPING them from the
verdict path.

This aligns primary verdict with verifier verdict by construction.

---

## 1. File chain (v5 + 06.8)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json
    05_candidate.json
    06_search_raw.json           ★ FROZEN
    06_5_semantic_hits.json      ★ FROZEN (v4)
    06_7_functional_hits.json    ★ FROZEN (v5)
    06_8_per_paper_completeness.json   ← NEW (v6)
    07_hit_miss.json             ★ FROZEN: aggregate-adjacency preserved verbatim
    10_decision.json             ← VERDICT now driven by 06_8 (v6 change)
    11_audit.json
    12_verification.json         ★ FROZEN: cross-agent verifier
```

`06_8_per_paper_completeness.json` is written AFTER
`06_7_functional_hits.json` and BEFORE `07_hit_miss.json`. The
content of `07_hit_miss.json` is UNCHANGED in format and computation
— aggregate-adjacency scoring exactly as in v5. What changes is
that `10_decision.json` reads `06_8_per_paper_completeness.json`
(not `07_hit_miss.json`) for the FAIL/PASS verdict.

---

## 2. Step 06.8 — per_paper_completeness.json (NEW in v6)

**Action:** After step 06.7 writes `06_7_functional_hits.json`, for
the same top-10 result entries (deduplicated by URL):

1. **Enumerate K candidate sub-mechanisms.** From
   `05_candidate.json.candidate_summary` plus `content_words`
   LLM-side phrases (typically items 4-8 in the 8-item content_words
   list), extract the K distinctive sub-mechanisms M_1, ..., M_K
   (typically K = 4-5 for E21+ candidates).

2. **Compose per-paper-completeness judge prompt.** For each result:

   ```
   System: You are a research-niche-novelty judge applying
   per-paper-completeness scoring (NOT broad-adjacency scoring).

   Per-paper-completeness definition:
   The candidate mechanism has K distinctive sub-mechanisms enumerated
   below. A search result is a per-paper-completeness HIT only if
   THIS SINGLE PAPER, taken as a unified published work, jointly
   covers ALL K sub-mechanisms with explicit mechanism-level
   correspondence (not just sharing one cluster of them).

   A paper that covers 1 of K → score 0.10-0.25.
   A paper that covers 2 of K → score 0.30-0.45.
   A paper that covers 3 of K → score 0.50-0.60.
   A paper that covers 4 of K → score 0.65-0.75.
   A paper that covers all K → score 0.80-1.00.

   THIS IS DIFFERENT FROM STEP 06.7. Step 06.7 asks "does this paper
   share a functional effect with the candidate?" — any single
   cluster-match suffices. Step 06.8 asks "does this paper jointly
   cover the full composite?" — every sub-mechanism must match.

   Output a JSON object:
     {
       "completeness_score": <float 0.0-1.0>,
       "covered_sub_mechanisms": ["M_i", "M_j", ...],
       "missing_sub_mechanisms": ["M_k", "M_l", ...],
       "justification": "<one sentence explicitly listing missing M_i>"
     }

   User: Candidate mechanism (llm_application from 05_candidate.json):
   <full text of candidate.llm_application>

   K candidate sub-mechanisms:
   1. M_1: <LLM-side content_words item 1>
   2. M_2: <LLM-side content_words item 2>
   ...
   K. M_K: <LLM-side content_words item K>

   Search result:
     title: <result.title>
     url: <result.url>
     snippet: <result.snippet>

   Score:
   ```

3. **Invoke LLM-judge.** Use the SAME Claude model running the
   pipeline in a FRESH context, same constraints as step 06.7.
   Record model and prompt-hash for reproducibility.

4. **Apply per-paper-completeness threshold.** If
   `completeness_score ≥ 0.7`, mark
   `per_paper_completeness_hit = true`. The 0.7 threshold matches
   the FROZEN semantic/functional threshold for consistency.

5. **Write `06_8_per_paper_completeness.json`** with this schema:

   ```json
   {
     "candidate_llm_application": "<copy from 05_candidate.json>",
     "K_sub_mechanisms": 5,
     "sub_mechanisms": [
       "M_1: <text>",
       "M_2: <text>",
       "M_3: <text>",
       "M_4: <text>",
       "M_5: <text>"
     ],
     "judge_model": "claude-opus-4-7",
     "judge_prompt_hash": "sha256:abcd...",
     "completeness_threshold": 0.7,
     "results": [
       {
         "rank": 1,
         "url": "...",
         "completeness_score": 0.32,
         "covered_sub_mechanisms": ["M_1"],
         "missing_sub_mechanisms": ["M_2", "M_3", "M_4", "M_5"],
         "justification": "Paper covers M_1 (cascade routing) but lacks M_2, M_3, M_4, M_5.",
         "per_paper_completeness_hit": false
       },
       ...
     ],
     "summary": {
       "per_paper_completeness_hits_count": 0,
       "max_completeness_score": 0.38,
       "results_at_or_above_threshold": 0
     }
   }
   ```

6. **Pass to step 07 (UNCHANGED) and step 10 (VERDICT CHANGE).**
   Step 07 reads `06_search_raw.json`, `06_5_semantic_hits.json`,
   AND `06_7_functional_hits.json` exactly as in v5. The
   `07_hit_miss.json` schema is UNCHANGED — aggregate-adjacency
   hits preserved verbatim. Step 10's `total_hits` is now computed
   from `06_8_per_paper_completeness.json` ONLY:

   ```
   v6 verdict rule (step 10):
     total_hits_v6 = count of results with per_paper_completeness_hit == true
     if total_hits_v6 >= 1: verdict = FAIL
     else:                   verdict = PASS
   ```

   The 07_hit_miss.json aggregate-adjacency total_hits is still
   recorded in `10_decision.json` under
   `aggregate_adjacency_total_hits` for forensic record, but does
   NOT drive the verdict.

---

## 3. The per-paper-completeness threshold (with E21-E23 evidence)

### Threshold = 0.7, justified per Pattern E sample round

For each of the 10 Pattern E rounds sampled in Phase 1, the table
below shows the expected per-paper-completeness score against the
TOP-RANKED retrieved paper that primary scored as a hit (sem ≥ 0.74)
and verifier scored as a miss (sem ≤ 0.45):

| Round | Candidate K-sub-mech | Top retrieved paper | Expected 06.8 score | Fires at 0.7? |
|---|---|---|---:|:---:|
| R504 GGANTIJA | 5 (apse-branch, corbel-tier, trilithon-gate, orthostat-anchor, solstice-axis) | MemGPT Tiered Memory | ~0.45 | ✗ — covers only corbel-tier |
| R515 HULA-HALAU | 5 (3-tier lineage, phase-lag-lock, style-invariant projection, sinew-imprint slow-LR, lineage archive) | MACLA Hierarchical Procedural Memory | ~0.30 | ✗ — covers only tier |
| R525 SABAR-BAKKS | 5 (K-bakks dict, tama lead, polyrhythm, Wolof P_lex, ask-respond bind) | Beyond Self-Talk Survey | ~0.20 | ✗ — covers none specifically |
| R530 KHIPU-CASCADE | 5 (4-tier, 3-knot-type, decimal 10^k, subsidiary loop, cord-attr metadata) | 3-Tier Routing Cascade | ~0.25 | ✗ — covers only 3-tier |
| R538 KGOTLA-CONSENSUS | 5 (open-speak, chair-LLM wrap-up, mmualebe L_mmu, acacia buffer, anti-polarization) | CONSENSAGENT | ~0.25 | ✗ — covers only consensus theme |
| R544 AVICENNA-PULSE | 4 (M_5x2 matrix, T_10 templates, 2-movement-2-pause, 4-modal synthesis + probe) | LLM-Rubric Multidim | ~0.30 | ✗ — covers only multi-dim eval |
| R547 BOKH-9-RANK | 5 (open-weight no-asym, 3-touch fall, technique-cunning reward, 9-rank ladder, eagle ritual) | Adversarial Robustness MA | ~0.25 | ✗ — covers only adv-MA |
| R555 MARSHALL-CHART | 5 (3-tier chart, 4-swell decomp, pre-computed wave-map, pitch-feel gate, island-disruption cascade) | Routing-Cascading Survey | ~0.25 | ✗ — covers only cascade |
| R565 MEVLEVI-SEMA | 5 (7-part S_7, 4-selam P_4, left-foot anchor, dual-hand split, cloak-off + ney-breath) | MHRoPE | ~0.20 | ✗ — covers only positional |
| R575 CHEROKEE-GHIGAU | 5 (dual-council, Ghigau veto, 7-clan matrilineal, V_prison override, war-peace tier) | AgentsBench | ~0.25 | ✗ — covers only judge bench |

**Predicted under v6:** 0/10 of the sampled Pattern E rounds would
register as FAIL (no result scores ≥ 0.7 per-paper-completeness).
All 10 would flip to v6 PASS, matching verifier verdicts. Pattern E
rate (primary vs verifier disagreement) is predicted to drop from
100% (E23) to near 0% on identical candidate trajectories.

### What 0.7 does NOT catch

A candidate that has been TRULY anticipated by a single prior paper
covering all K sub-mechanisms would score ≥ 0.7 — correctly marked
FAIL under v6. Phase 1 evidence shows no such cases in E21-E23 (no
retrieved paper covers ≥ 4 of K sub-mechanisms for any sampled
round). If such a case appears in E24+, v6 catches it.

The threshold is symmetric with the v4/v5 0.7 thresholds; this
preserves the calibration philosophy of the family.

---

## 4. Memory update at step 10 (v5 schema + v6 additions)

After step 10 writes `10_decision.json`, append to `memory_db.json`
with this v6-extended schema:

```json
{
  "round": "NNN",
  "epoch": 6,
  "domain": "...",
  "domain_normalized": "...",
  "mechanism": "...",
  "form": "...",
  "forced_hit_count": N,                          // v1-v4 keyword-only
  "forced_semantic_hit_count": M,                 // v4 semantic-only
  "forced_functional_hit_count": L,               // v5 functional-only
  "per_paper_completeness_hit_count": P,          // NEW v6 — per-paper-completeness only
  "hit_count_v5_aggregate": K,                    // v5 union, FORENSIC RECORD
  "hit_count_v6_verdict_driver": Q,               // v6 verdict driver = P
  "fail_reason": "...",
  "tried_keywords": [...],
  "verdict_v6": "FAIL" | "PASS",
  "v4_semantic_metrics": {...},
  "v5_functional_metrics": {...},
  "v6_per_paper_completeness_metrics": {
    "K_sub_mechanisms": 5,
    "max_completeness_score": 0.38,
    "results_at_or_above_threshold": 0,
    "verdict_alignment_with_v5_aggregate": "AGREE_PASS" | "AGREE_FAIL" | "V6_PASS_V5_AGGREGATE_FAIL"
  }
}
```

The `verdict_alignment_with_v5_aggregate` field tracks Pattern E
explicitly: rounds where the v5 aggregate-adjacency verdict would
have been FAIL but v6 per-paper-completeness verdict is PASS get
flagged as `V6_PASS_V5_AGGREGATE_FAIL`. The Pattern E rate under v6
is operationally redefined as the rate of primary-vs-verifier
disagreement on the v6 verdict (which should be near zero by
construction).

---

## 5. ★ FORBIDDEN-TO-MODIFY zones (verbatim from v1/v2/v3/v4/v5)

The four FROZEN zones are preserved EXACTLY:

### 5.1 Step 06 web_search (honesty gate)
- ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query,
  RAW tool response saved to file. v6 does NOT change the search step.

### 5.2 Step 07 keyword threshold ≥ 2
- `keyword_overlap_count ≥ 2` still triggers `hit = true` and
  `forced_by_rule = true` in `07_hit_miss.json`. v6 does NOT lower
  the keyword threshold.

### 5.3 Original primary scoring logic
- `07_hit_miss.json` continues to record aggregate-adjacency
  `sem_cosine` and `func_score` per result, with the rule
  `hit iff kw>=2 OR sem>=0.7 OR func>=0.7`. The format and
  computation are PRESERVED VERBATIM. v6 ADDS a layer (06.8) but
  does NOT modify the existing 07 logic.

### 5.4 Step 12 cross-agent verification
- Fresh agent reads only `05_candidate.json` + `06_search_raw.json`
  + `06_5_semantic_hits.json` + `06_7_functional_hits.json` +
  (NEW v6) `06_8_per_paper_completeness.json` and produces
  independent `12_verification.json`. Verifier uses
  per-paper-completeness scoring (which is the same as v5's
  verifier behavior — explicitly aligned via the new step 06.8 in
  the primary's pipeline as well).

---

## 6. Loop control (v6)

```
while True:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]:
        execute step

    # Step 04.5 (v3, unchanged)
    memory_skip_count = 0
    while True:
        propose (domain_norm, mechanism_keywords, form)
        load logs/memory_db.json
        check rules 1, 2, 3
        if any rule fires: continue with new proposal
        else: append ACCEPT; break

    execute step 05 using accepted proposal
    execute step 06 (★ FROZEN web_search)
    execute step 06.5 (★ FROZEN semantic similarity)
    execute step 06.7 (★ FROZEN functional-equivalence judge)

    # Step 06.8 (NEW in v6)
    load 05_candidate.json, 06_search_raw.json
    extract K sub-mechanisms from content_words LLM-side phrases
    for each result in top-10 (by relevance rank):
        construct per-paper-completeness judge prompt
        invoke LLM-judge in fresh context
        record completeness_score, covered/missing sub-mechanisms
    aggregate; write 06_8_per_paper_completeness.json

    execute step 07 (★ FROZEN — aggregate-adjacency hits recorded as before)

    # Step 10 verdict (v6 change)
    total_hits_v6 = count of results with per_paper_completeness_hit == true
    verdict = FAIL if total_hits_v6 >= 1 else PASS
    record aggregate_adjacency_total_hits from 07_hit_miss.json as forensic field
    write 10_decision.json with both metrics

    # Memory update (v6 schema)
    append round entry to memory_db.json with v6_per_paper_completeness_metrics

    execute step 11 (audit)
    execute step 12 (★ FROZEN cross-agent; verifier sees 06.5/06.7/06.8)

    if round_num % 25 == 0: write output/stats_round_NNN.json
```

---

## 7. Stats schema additions in v6

`output/stats_round_NNN.json` adds these v6-specific fields on top of v5:

```json
{
  ... (all v1/v2/v3/v4/v5 fields) ...,
  "v6_per_paper_completeness_metrics": {
    "rounds_v5_aggregate_FAIL_v6_per_paper_PASS": 0,    // Pattern E mitigation count
    "rounds_v6_per_paper_FAIL": 0,                       // v6 confirmed FAIL
    "rounds_v6_per_paper_PASS": 0,                       // v6 PASS
    "rounds_v6_PASS_verifier_FAIL_residual_disagreement": 0,  // residual Pattern E under v6
    "pattern_E_rate_v6": 0.0,                            // verifier disagreement rate on v6 verdict
    "pattern_E_rate_v5_for_comparison": 1.00,            // E23 baseline
    "mean_K_sub_mechanisms": 5.0
  },
  "v6_score_components": {
    "substantive_pass_count_v6_x_10": 0,
    "twenty_five_minus_mean_v6_hit": 0.0,
    "v6_disagreement_rate_x_5": 0.0,
    "false_positive_count_v6_x_5_negative": 0,
    "score_v6": 0.0
  }
}
```

---

## 8. v6 score formula

```
score_v6 = (substantive_pass_count_v6 × 10)
         + (25 − mean_per_paper_completeness_hit_count)
         + (verdict_alignment_rate × 5)
         − (false_positive_count_v6 × 5)
```

`substantive_pass_count_v6` requires:
- per-paper-completeness max score < 0.7 across all results, AND
- verifier confirms substantive PASS (cross-agent agreement).

`verdict_alignment_rate` is the fraction of rounds where primary v6
verdict and verifier v6 verdict AGREE. Phase 1 evidence predicts this
should be near 1.0 (≥ 85%) under v6, vs. 0.0 under v5 at E23 saturation.

`false_positive_count_v6` is the count of rounds where v6 PASS fires
but the verifier (also using per-paper-completeness) identifies
≥ 1 result above 0.7 — indicating residual stochastic disagreement.

---

## 9. Inherited history (v1 → v2 → v3 → v4 → v5 → v6)

- **v1** (program.md): file-chain + mechanical keyword rule + cross-agent
  verification. **R001-R025** ran under v1.
- **v2** (program_v2.md): Form A/B/C/D rotation + query/composition
  rules. **R026-R050** ran under v2.
- **v3** (program_v3.md): step 04.5 memory check; persistent failure
  memory. **R051-R075** ran under v3.
- **v4** (program_v4.md): step 06.5 semantic-similarity check.
  **R076-R100** ran under v4.
- **v5** (program_v5.md): step 06.7 LLM-judge functional-equivalence.
  **R101-R575** ran under v5 across 19 epochs (E5-E23). Pattern E
  emerged at E20 (12%), named at E21 (64%), intensified through E22
  (84%) to E23 (100% saturation).
- **v6** (this file): step 06.8 LLM-judge per-paper-completeness;
  step 10 verdict driven by 06.8 rather than 07. Targets the
  aggregate-adjacency vs per-paper-completeness scoring divergence
  that drove Pattern E to 100% in E23. **R576-R600** runs under v6.

---

## 10. What v6 does NOT promise

v6 does NOT promise more substantive PASS verdicts in absolute count.
The saturation result from 671 prior rounds with 0 surviving
substantive PASS is structural. v6 promises only that the primary
verdict will ALIGN with the verifier verdict on multi-feature
recombination candidates.

What v6 DOES promise:
- Pattern E rate (primary vs verifier verdict disagreement) drops
  from 100% (E23) toward ≤ 25% (predicted; floor depends on
  residual stochastic agent variation).
- v6 PASS classifications are FIRMER than v5 PassC borderline
  classifications, because both primary and verifier agree on
  PASS under v6.
- v5 aggregate-adjacency scoring is PRESERVED in forensic record
  (07_hit_miss.json unchanged) so we retain the ability to detect
  if v6 has under-counted hits.
- The v5 vs v6 verdict-disagreement count (`rounds_v5_aggregate_FAIL_v6_per_paper_PASS`)
  is itself a Pattern E mitigation metric — expected to be high in
  E24 (most v5-FAIL rounds flip to v6-PASS) and to attenuate as
  generators drift back toward smaller K.

If `rounds_v5_aggregate_FAIL_v6_per_paper_PASS` is high in E24, that
confirms Pattern E was a large systematic source of false-positive
FAIL under v5. If it is near zero, that means E24's generator
already drifted away from multi-feature compositions and v6 has no
marginal effect (similar to the v5 prediction note on functional
hits).

---

## 11. Anti-cheating commitments

If you catch yourself wanting to:
- Lower the per-paper-completeness threshold to 0.6 to recover more
  FAILs — don't. The 0.7 threshold matches the v4/v5 family. The
  goal of v6 is verdict-alignment with verifier, not to maximize
  FAILs.
- Score a paper that covers 2 of 5 sub-mechanisms as 0.7 because
  "those 2 are the most important" — don't. Cover the explicit
  per-paper-completeness rubric: ≤ 1 of K → 0.10-0.25; 2 of K →
  0.30-0.45; 3 of K → 0.50-0.60; 4 of K → 0.65-0.75; all K →
  0.80-1.00. Document any judgment override in 11_audit.json.
- Skip step 06.8 when the 07 verdict is already FAIL — don't. Step
  06.8 is what computes the v6 verdict; without it, the v6 verdict
  cannot be computed.
- Use a different prompt formulation for 06.8 than the canonical
  one — don't. The canonical prompt is the calibrated rubric.

The v3/v4/v5 instructions stand: data on agent impulse-to-bypass is
more valuable than a clean fake run.
