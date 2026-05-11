# program_v5.md
## Niche-Mining Pipeline — v5: LLM-Judge Functional-Equivalence Detection

This file extends `program_v4.md` (file-chain + mechanical keyword rule
+ cross-agent verification + memory-aware step 04.5 + semantic-similarity
step 06.5) with **one new step, 06.7, that catches the Pattern D
false-positive class identified in epoch 4**.

The five ★ FORBIDDEN-TO-MODIFY zones are preserved verbatim:
- Step 06 web_search (honesty gate)
- Step 06.5 semantic-similarity check (cosine ≥ 0.7 still forces hit)
- Step 07 keyword-overlap threshold (≥2 content_words still forces hit)
- Step 10 mechanical verdict (`total_hits ≥ 1` → FAIL — now considers
  keyword hits ∪ semantic hits ∪ functional hits)
- Step 12 cross-agent verification

v5 changes only **how a search result is scored for functional-mechanism
overlap**, not **how the verdict is computed from the hit count**.

---

## 0. Why a functional-equivalence judge now

Epoch 4 (R076-R100, program_v4.md) produced 4 mechanical PASS verdicts
that ALSO survived the v4 semantic-similarity check at cosine ≥ 0.7:
**R079** (phyllotaxis), **R085** (tribology), **R091** (tardigrade
cryptobiosis), **R092** (icefish AFGP). All four were initially flagged
as "borderline plausible substantive PASSes." Phase 1 of this session
(see `output/epoch4_functional_audit.md`) web-searched the functional
content of each — stripping the source-domain vocabulary — and found
2024-2026 LLM literature covering the same functional effect for ALL
four:

| Round | Functional effect | 2024-2026 prior art (different metaphor) |
|---|---|---|
| **R079** | minimise inter-head redundancy via angular / subspace criterion | DEACON (Kong et al. MDPI 2024), DEX (2025), SHD (2025), Voita ACL 2019 + 2024 follow-ups |
| **R085** | heavy-tailed phase-transition failure curve under adversarial pressure | JailbreakRadar ACL 2025, SecAlign 2024 (2410.05451), "LLMs know their vulnerabilities" ACL 2025, MDPI 2025 safety-boundary study |
| **R091** | freeze parameters into compressed dormant state; reactivate without retraining | GPTQ/AWQ + ParoQuant/Tequila/Q&C/SliderQuant ICLR 2026; SSU OpenReview 2025; PEFT/LoRA + ICL |
| **R092** | detect correlated gradient noise, cancel with anti-correlated update | 2306.05300 (literally uses "anti-correlated noise"), SPAM 2025, MoLS 2026 (2605.05794), noise-corrected GRPO 2510.18924 |

The v4 semantic check missed all four because the candidate's
`content_words` were entirely source-side (no LLM-vocabulary anchor in
the content_words) AND the candidate's `llm_application` phrasing was
one synonym-hop from the prior-art phrasing — enough to push cosine
below 0.7 against any single search result. This is a new false-positive
**pattern D**:

**Pattern D — functional-equivalence gap.** Candidate and prior art
share **the same end-state mechanism**, but neither share **substring
vocabulary** (defeats step 07) nor share **sentence-level concept
embedding above 0.7** (defeats step 06.5). The bridge is at the level
of *what the mechanism does*, not what it is called or how it is
described.

**v5 fix:** add step 06.7 between semantic check (06.5) and keyword
rule (07). Step 06.7 invokes an LLM-judge over the top-10
`06_search_raw.json` results and asks, per result:

> "Given candidate mechanism X (full text of `candidate.llm_application`),
> here is search result Y (title + snippet + first paragraph of abstract
> when available). Does this paper achieve the same FUNCTIONAL effect
> as the candidate, even with different terminology and metaphor?
> Score from 0.0 (entirely different effect) to 1.0 (identical functional
> effect on the same LLM artefact). Provide one-sentence justification."

If any result scores ≥ 0.7 on this functional-equivalence dimension,
mark `functional_hit = true` and force hit=true regardless of keyword
overlap or semantic cosine.

---

## 1. File chain (v4 + 06.7)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json   ← v3
    05_candidate.json
    06_search_raw.json        ★ FROZEN
    06_5_semantic_hits.json   ★ FROZEN (v4)
    06_7_functional_hits.json ← NEW (v5)
    07_hit_miss.json          ★ FROZEN: keyword threshold ≥2 still forces hit
    10_decision.json          ★ FROZEN: total_hits ≥ 1 → FAIL (keyword ∪ semantic ∪ functional)
    11_audit.json
    12_verification.json      ★ FROZEN: cross-agent
```

`06_7_functional_hits.json` is written AFTER `06_5_semantic_hits.json`
and BEFORE `07_hit_miss.json`. It records, per result in
06_search_raw.json (top 10 by relevance rank):
- the LLM-judge functional-equivalence score (0.0-1.0)
- the one-sentence justification produced by the judge
- whether the score ≥ 0.7 → `functional_hit = true`
- the matched function-effect cluster (e.g., "head-redundancy
  minimization", "alignment-failure heavy tail", "post-training
  quantization", "anti-correlated gradient noise")

The `07_hit_miss.json` step then ORs the keyword-overlap rule
(≥2 → hit) with the semantic-hit flag (cosine ≥0.7 → hit) AND the
functional-hit flag (judge ≥0.7 → hit) when computing each result's
`hit` field. The final `total_hits` count includes all three sources.
Step 10 then applies the FROZEN rule: total_hits ≥ 1 → FAIL.

---

## 2. Step 06.7 — functional_hits.json (NEW in v5)

**Action:** After step 06.5 writes `06_5_semantic_hits.json`, for the
top-10 `result` entries by relevance rank across all queries
(deduplicated by URL):

1. **Compose judge prompt.** For each result, construct:

   ```
   System: You are a research-niche-novelty judge.
   You will be shown a candidate research mechanism and one prior-art
   search result. Your job is to determine whether the search result
   describes a published mechanism that achieves THE SAME FUNCTIONAL
   EFFECT as the candidate, regardless of vocabulary or metaphor.

   Function-equivalence definition:
   Two mechanisms are functionally equivalent if, when applied to the
   same LLM artefact (attention heads, gradient updates, parameter
   storage, alignment surface, etc.), they produce the same observable
   change in that artefact's behaviour or quantitative property.
   Vocabulary differences do not block equivalence.
   Metaphor differences do not block equivalence.
   Only the operational mechanism matters.

   Score from 0.0 to 1.0:
     0.0  Entirely different effect on different LLM artefact.
     0.3  Different effect on same artefact (e.g., both touch attention
          heads, but one prunes and one regularizes).
     0.5  Same artefact, partially overlapping effect.
     0.7  Same artefact, functionally same effect, different mechanism
          for achieving it (e.g., both reduce head redundancy, one via
          PCA constraint and one via angular distribution).
     0.9  Same artefact, same effect, mechanism is conceptually identical
          modulo metaphor (e.g., "anti-correlated noise" candidate vs
          "anti-correlated noise" prior art).
     1.0  Same artefact, identical mechanism, identical formal description.

   Output a JSON object: {"score": <float>, "justification": "<one sentence>",
                         "matched_effect_cluster": "<3-5 word phrase>"}

   User: Candidate mechanism (llm_application from 05_candidate.json):
   <full text of candidate.llm_application>

   Search result:
     title: <result.title>
     url: <result.url>
     snippet: <result.snippet>

   Score:
   ```

2. **Invoke LLM-judge.** Use the same Claude model running the pipeline
   (Opus 4.7 by default) in a FRESH context — i.e., no prior round
   memory — to avoid PASS-bias contamination. Record the model and
   prompt-hash in `06_7_functional_hits.json` for reproducibility.

3. **Apply functional threshold.** If `judge_score ≥ 0.7`, mark
   `functional_hit = true`. The 0.7 threshold is calibrated on the 4
   epoch-4 false positives — see §3 evidence.

4. **Aggregate effect clusters.** Across the 10 results, count distinct
   `matched_effect_cluster` values. If ≥ 2 distinct clusters score ≥ 0.7,
   the candidate is functionally occupied across multiple sub-regions of
   the prior art — record this as `multi_cluster_match = true`.

5. **Write `06_7_functional_hits.json`** with this schema:

   ```json
   {
     "candidate_llm_application": "<copy from 05_candidate.json>",
     "judge_model": "claude-opus-4-7",
     "judge_prompt_hash": "sha256:abcd...",
     "functional_threshold": 0.7,
     "results": [
       {
         "rank": 1,
         "url": "...",
         "title": "...",
         "snippet": "...",
         "judge_score": 0.85,
         "judge_justification": "Both apply an angular/subspace criterion to multi-head attention to reduce inter-head redundancy.",
         "matched_effect_cluster": "head-redundancy minimization",
         "functional_hit": true
       },
       ...
     ],
     "summary": {
       "functional_hits_count": 4,
       "keyword_hits_count_from_step_07": 0,
       "semantic_hits_count_from_step_06_5": 0,
       "additional_hits_from_functional": 4,
       "distinct_effect_clusters_above_threshold": 2,
       "multi_cluster_match": true
     }
   }
   ```

6. **Pass to step 07.** Step 07 reads `06_search_raw.json` AND
   `06_5_semantic_hits.json` AND `06_7_functional_hits.json`. For each
   result, the final `hit` field is:

   ```
   hit = (keyword_overlap_count ≥ 2)
       OR (semantic_hit == true)
       OR (functional_hit == true)
   ```

   `forced_by_rule` family:

   ```
   forced_by_rule       = (keyword_overlap_count ≥ 2)   # v1/v2/v3 definition
   forced_by_semantic   = (semantic_hit == true)         # v4 definition
   forced_by_functional = (functional_hit == true)       # NEW v5
   ```

   All three are tracked separately in `07_hit_miss.json` so the post-hoc
   audit can distinguish keyword-only, semantic-only, functional-only,
   and combined forced hits.

---

## 3. The functional-equivalence threshold (with epoch 4 evidence)

### Threshold = 0.7, justified per false-positive round

For each of the 4 epoch-4 PASSes, the table below shows the expected
LLM-judge score against the substantively-equivalent prior art that
the keyword AND semantic rules both missed.

| Round | Candidate llm_application (paraphrased) | Top prior-art result | Expected judge score | Fires at 0.7? |
|---|---|---|---:|:---:|
| **R079** | "LLM attention head positioning via golden-angle distribution to minimise head redundancy" | Kong et al., "Diversifying Multi-Head Attention in the Transformer Model" (DEACON, MDPI 2024) — head diversification via PCA constraint, explicitly reducing inter-head redundancy | ~0.85 | ✓ — both apply angular/subspace criterion to reduce head redundancy |
| **R085** | "Alignment 'lubrication' transitions under prompt-injection pressure; failure follows stress-cracking distribution" | "Jailbreaking LLMs: A Survey of Attacks, Defenses and Evaluation" (TechRxiv 2026) — taxonomy of attack-success-rate distributions over violation categories | ~0.78 | ✓ — both model alignment failure as a distribution-over-pressure, with phase-transition between regimes |
| **R091** | "Vitrify a model's parameters into a low-energy frozen state for cold storage; rehydrate via context without retraining" | "A Survey of Quantization in LLM" Springer JCST 2026 + GPTQ/AWQ + PEFT/LoRA + ICL | ~0.82 | ✓ — both freeze parameters into compressed dormant state and reactivate without full retraining |
| **R092** | "Detect early-stage gradient 'crystal nuclei' (correlated noise patterns) and bind them with anti-correlated update vectors" | "Anti-Correlated Noise in Epoch-Based Stochastic Gradient Descent" (2306.05300) | ~0.92 | ✓ — explicitly the same mechanism, same phrase, applied to same artefact (SGD gradient updates) |

Lowering the threshold to 0.6 would risk false-flagging candidates
where the judge is uncertain but the mechanism is genuinely different
(e.g., "both touch attention heads" → 0.55 baseline). Raising to 0.8
would miss R085 (0.78). **0.7 is the calibrated threshold for
Pattern D detection.**

### Multi-cluster match threshold = 2 distinct effect clusters, justified

A candidate that has functional-equivalent prior art in ≥ 2 distinct
effect clusters (e.g., both "head redundancy minimization" and
"head pruning" clusters fire for R079) is harder to defend as novel
than a candidate that has one functional collision. The
`multi_cluster_match` flag is an additional signal for the cross-agent
verifier in step 12 to weigh.

---

## 4. Memory update at step 10 (v4 unchanged + v5 additions)

After step 10 writes `10_decision.json`, append to `memory_db.json`
with this v5-extended schema:

```json
{
  "round": "NNN",
  "epoch": 5,
  "domain": "...",
  "domain_normalized": "...",
  "mechanism": "...",
  "form": "...",
  "forced_hit_count": N,                 // keyword-only forced hits (v1-v4 metric)
  "forced_semantic_hit_count": M,        // semantic-only forced hits (v4 metric)
  "forced_functional_hit_count": L,      // NEW v5 — functional-only forced hits
  "hit_count": K,                         // total unique hits (keyword ∪ semantic ∪ functional)
  "fail_reason": "...",
  "tried_keywords": [...],
  "verdict": "FAIL" | "PASS",
  "v4_semantic_metrics": {
    "max_cosine_similarity": 0.49,
    "results_above_threshold": 0,
    "memory_pattern_match": false,
    "matched_prior_false_positive_rounds": []
  },
  "v5_functional_metrics": {
    "max_judge_score": 0.85,
    "results_above_threshold": 4,
    "distinct_effect_clusters": 2,
    "multi_cluster_match": true,
    "matched_effect_clusters": ["head-redundancy minimization", "head pruning"]
  }
}
```

Aggregates recompute as before plus:
`aggregates.epoch_5_pattern_d_caught_count` = total rounds where
`forced_functional_hit_count ≥ 1` AND `forced_hit_count == 0` AND
`forced_semantic_hit_count == 0`.

---

## 5. ★ FORBIDDEN-TO-MODIFY zones (verbatim from program.md / program_v3.md / program_v4.md)

The five FROZEN zones are preserved EXACTLY:

### 5.1 Step 06 web_search (honesty gate)
- ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query,
  RAW tool response saved to file. v5 does NOT change the search step.

### 5.2 Step 06.5 semantic-similarity check
- Cosine ≥ 0.7 between `candidate.llm_application` and
  `result.title + " " + result.snippet` → `semantic_hit = true`.
- v5 does NOT raise or lower this threshold and does NOT replace the
  semantic check. The functional-judge layer is ADDITIVE.

### 5.3 Step 07 keyword threshold
- `keyword_overlap_count ≥ 2` → `hit = true` and `forced_by_rule = true`.
- v5 adds the functional-hit channel but does NOT lower the keyword
  threshold. A keyword overlap ≥ 2 still forces hit.

### 5.4 Step 10 mechanical verdict
- `total_hits == 0` → PASS.
- `total_hits ≥ 1` → FAIL.
- v5 expands the **definition** of "hit" to include functional hits,
  but the verdict logic itself (`total_hits ≥ 1 → FAIL`) is unchanged.
- `total_hits` is now `keyword_hits ∪ semantic_hits ∪ functional_hits`
  (set union — a result that hits multiple ways counts once).

### 5.5 Step 12 cross-agent verification
- Fresh agent reads only `05_candidate.json` + `06_search_raw.json` +
  `06_5_semantic_hits.json` + (NEW) `06_7_functional_hits.json` and
  produces independent `07_hit_miss.json` equivalent.
- The verifier reruns 06.5 AND 06.7 with the same thresholds; if the
  verifier's functional_judge scores diverge from the primary's by
  > 0.15 on any result, that result's score is reconciled by recording
  both and flagging the round for human review.

---

## 6. Loop control (v5)

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
    
    # Step 06.7 (NEW in v5)
    load 05_candidate.json, 06_search_raw.json
    for each result in top-10 (by relevance rank):
        construct judge prompt
        invoke LLM-judge in fresh context
        record score, justification, effect_cluster
    aggregate effect_clusters; compute multi_cluster_match
    write 06_7_functional_hits.json
    
    execute step 07 (★ FROZEN keyword threshold; ORs in semantic_hit AND functional_hit)
    execute step 10 (★ FROZEN verdict on total_hits)
    
    # Memory update (v5 schema)
    append round entry to memory_db.json with v5_functional_metrics
    
    execute step 11 (audit)
    execute step 12 (★ FROZEN cross-agent; verifier reruns 06.5 + 06.7)
    
    if round_num % 25 == 0: write output/stats_round_NNN.json
```

---

## 7. Stats schema additions in v5

`output/stats_round_NNN.json` adds these v5-specific fields on top of v4:

```json
{
  ... (all v1/v2/v3/v4 fields) ...,
  "v5_functional_metrics": {
    "functional_hits_caught_total": 0,                  // additional hits step 06.7 catches that keyword AND semantic missed
    "functional_only_forced_hits_total": 0,              // functional_hit=true AND keyword<2 AND semantic<0.7
    "rounds_flipped_v4_pass_to_v5_fail_by_functional": 0,// would-be PASS under v4 but FAIL under v5
    "rounds_with_multi_cluster_match": 0,                // distinct effect clusters above threshold ≥ 2
    "substantive_pass_count_v5": 0,                      // PASSes that survive v5 (keyword <2 AND semantic <0.7 AND functional <0.7 across all results)
    "mechanical_pass_count_v4_definition": 0             // PASSes under v4 (keyword <2 AND semantic <0.7) for comparison
  },
  "v5_score_components": {
    "substantive_pass_count_x_10": 0,
    "twenty_five_minus_mean_forced_hit": 0.0,
    "disagreement_rate_x_5": 0.0,
    "false_positive_count_x_5_negative": 0,
    "score_v5": 0.0
  }
}
```

---

## 8. v5 score formula

```
score_v5 = (substantive_pass_count × 10)
         + (25 − mean_forced_hit)
         + (disagreement_rate × 5)
         − (false_positive_count × 5)
```

`mean_forced_hit` is the mean of `forced_hit_count` (keyword only,
v1-v4 definition retained for backward comparison).

`substantive_pass_count` requires:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- verifier confirms substantive PASS.

This is strictly more demanding than v4's substantive_pass_count.

`false_positive_count` is the count of rounds where mechanical PASS
fires but ANY of the three signals (semantic_hit ≥ 0.7, functional_hit
≥ 0.7, verifier disagreement) indicates substantive prior art.

---

## 9. Inherited history (v1 → v2 → v3 → v4 → v5)

- **v1** (program.md): file-chain + mechanical keyword rule + cross-agent
  verification. **R001-R025** ran under v1.
- **v2** (program_v2.md): Form A/B/C/D rotation + query/composition
  rules. **R026-R050** ran under v2. Exposed mechanical-PASS artifacts
  on narrow content_words (R045-R050).
- **v3** (program_v3.md): step 04.5 memory check; persistent failure
  memory in `logs/memory_db.json`. **R051-R075** ran under v3. Exposed
  the same mechanical-PASS artifact pattern with source-only content_words
  (R059-R075).
- **v4** (program_v4.md): step 06.5 semantic-similarity check +
  memory-pattern Jaccard check. **R076-R100** ran under v4. Caught
  10 rounds of Pattern A/B/C false positives but produced 4 new
  Pattern D false positives (R079, R085, R091, R092) — functional
  collisions across vocabulary gaps.
- **v5** (this file): step 06.7 LLM-judge functional-equivalence check.
  Targets the functional-equivalence gap that drove the 4 epoch-4
  false positives. **R101-R125** runs under v5.

---

## 10. What v5 does NOT promise

v5 does NOT promise more substantive PASS verdicts. The saturation
result from N=138 prior + 100 in-repo rounds = 238 total with 0
*surviving-functional-audit* substantive PASS (after Phase 1 of this
session reclassified all 4 epoch-4 PASSes as functional false positives)
is structural. The LLM-judge layer catches functional false positives
(lower mechanical+semantic-cleared PASS count); it does not create
novelty.

What v5 DOES promise:
- Mechanical+semantic-cleared PASS count converges toward 0 (functional
  check catches the artifacts that BOTH keyword AND semantic miss).
- `substantive_pass_count_v5` becomes the most stringent KPI: only
  candidates clearing keyword < 2 AND semantic < 0.7 AND functional < 0.7
  AND verifier-confirmed.
- New metric `functional_hits_caught` measures how often the
  keyword+semantic rules together would have produced a false negative
  on prior-art detection.
- New metric `multi_cluster_match` measures whether the prior art
  occupies the same niche from multiple sub-regions, strengthening
  the functional-collision signal.

If `functional_hits_caught` is high in epoch 5, that confirms the
functional-equivalence gap was a major missed signal in v1-v4. If it
is near zero, that means epoch 5's generator already drifted away from
single-synonym-hop candidates and v5 has no marginal effect.

---

## 11. Anti-cheating commitments

If you catch yourself wanting to:
- Skip step 06.7 because it's "obvious" the candidate is novel — write
  that impulse to `11_audit.json` honestly. The whole point of v5 is to
  catch the agent's "obvious to me" judgment in cases where keyword AND
  semantic both misled the agent.
- Lower the judge threshold to 0.6 to catch more false positives —
  don't. The threshold is calibrated; lowering it without re-calibration
  introduces new false negatives on novel candidates.
- Use a different judge model (e.g., GPT-4) to systematically get
  lower scores — recalibrate the threshold first; document in
  `compliance_log.md`.
- Skip the LLM-judge for "obviously different" candidates — the
  functional-equivalence signal is precisely about catching cases the
  agent thinks are different but functionally are not (R079, R085,
  R091, R092 all looked novel to the v4 verifier).
- Run the judge with prior round context to bias toward continuity —
  always invoke the judge in a fresh context with only the candidate
  and one result.

The v3/v4 instructions stand: data on agent impulse-to-bypass is more
valuable than a clean fake run.
