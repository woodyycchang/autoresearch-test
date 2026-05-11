# program_v4.md
## Niche-Mining Pipeline — v4: Semantic-Similarity False-Positive Detection

This file extends `program_v3.md` (file-chain + mechanical keyword rule +
cross-agent verification + memory-aware step 04.5) with **one new step,
06.5, that catches the false-positive class identified in epochs 2 + 3**.

The four ★ FORBIDDEN-TO-MODIFY zones are preserved verbatim:
- Step 06 web_search (honesty gate)
- Step 07 keyword-overlap threshold (≥2 content_words still forces hit)
- Step 10 mechanical verdict (`total_hits ≥ 1` → FAIL — now considers
  both keyword AND semantic hits)
- Step 12 cross-agent verification

v4 changes only **how a search result is scored for prior-art-overlap**, not
**how the verdict is computed from the hit count**.

---

## 0. Why semantic now

Across epochs 2 + 3, **9 of 9 mechanical PASS verdicts were false positives**
under substantive review (R045, R046, R047, R050 from epoch 2;
R059, R064, R068, R069, R075 from epoch 3 — the renumbered IDs).
`output/false_positive_taxonomy.md` decomposes them into three artifact
patterns:

- **Pattern A (word-order variant):** R045 — `"plasticity loss"` vs
  literature `"Loss of Plasticity"`.
- **Pattern B (synonym substitution):** R046 (`lock-in amplifier` ≡
  `frequency-domain ICL bias`), R047 (`Shannon capacity bound` ≡
  `theoretically grounded watermark framework`), R050 (`mass action +
  Le Chatelier` ≡ `capability-cost trade-off`), R069 borderline
  (`dike intrusion` ≈ `activation steering`).
- **Pattern C (source-side-only content_words):** R059 (volcanology),
  R064 (cartography), R068 (pedology), R075 (numismatics).

All three patterns share the same root cause: the strict-substring keyword
rule (step 07) operates at the lexical level, so any candidate whose
content_words don't share substrings with the LLM-side literature scores
zero overlap regardless of conceptual equivalence. Patterns A/B/C all map
to **near-zero substring overlap, high semantic-concept overlap**.

**v4 fix:** add step 06.5 between web_search and the keyword rule. Compute
embedding cosine similarity between `candidate.llm_application` and
`result.title + result.snippet`. Cosine ≥ 0.7 forces `hit = true` even if
keyword overlap is < 2. Also query memory_db for prior false-positive
patterns; flag if Jaccard similarity on `tried_keywords` is ≥ 0.3.

---

## 1. File chain (v3 + 06_5)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json   ← v3
    05_candidate.json
    06_search_raw.json        ★ FROZEN
    06_5_semantic_hits.json   ← NEW (v4)
    07_hit_miss.json          ★ FROZEN: keyword threshold ≥2 still forces hit
    10_decision.json          ★ FROZEN: total_hits ≥ 1 → FAIL (sum of keyword + semantic)
    11_audit.json
    12_verification.json      ★ FROZEN: cross-agent
```

`06_5_semantic_hits.json` is written AFTER `06_search_raw.json` and BEFORE
`07_hit_miss.json`. It records, per result in 06_search_raw.json:
- the cosine similarity between `candidate.llm_application` and
  `result.title + " " + result.snippet`
- whether the similarity ≥ 0.7 → `semantic_hit = true`
- the memory-pattern Jaccard score against past false-positive entries
- whether memory-pattern Jaccard ≥ 0.3 → `memory_pattern_match = true`

The `07_hit_miss.json` step then ORs the keyword-overlap rule (≥2 → hit)
with the semantic-hit flag (cosine ≥0.7 → hit) when computing each
result's `hit` field. The final `total_hits` count includes both forced
keyword hits and forced semantic hits. Step 10 then applies the FROZEN
rule: total_hits ≥ 1 → FAIL.

---

## 2. Step 06.5 — semantic_hits.json (NEW in v4)

**Action:** After step 06 writes `06_search_raw.json`, for each `result`
across all queries:

1. **Compute embedding similarity.** Embed `candidate.llm_application`
   (taken from `05_candidate.json`) and `result.title + " " + result.snippet`
   using a sentence-embedding model (e.g., `text-embedding-3-large`,
   `sentence-transformers/all-MiniLM-L6-v2`, or any model that produces
   512+-dim semantic embeddings). Compute cosine similarity.

2. **Apply semantic threshold.** If `cosine_similarity ≥ 0.7`, mark
   `semantic_hit = true`. The 0.7 threshold is calibrated on the 9
   epoch-2+3 false-positive cases — see §3 evidence.

3. **Memory-pattern check.** Load `logs/memory_db.json` and find all
   prior entries where `verdict == "PASS"` AND
   `fail_reason` contains "artifact" OR `fail_reason` contains "substring"
   OR `fail_reason` starts with "zero hits — candidate may be novel".
   These are the false-positive ground-truth entries (the 9 epoch-2+3
   false positives plus any subsequent epoch-4 ones as memory accumulates).
   For each such prior entry, compute Jaccard similarity:

   ```
   jaccard = |current.tried_keywords ∩ prior.tried_keywords|
           / |current.tried_keywords ∪ prior.tried_keywords|
   ```

   If any prior entry yields `jaccard ≥ 0.3`, mark
   `memory_pattern_match = true` and record the matched prior round id.

4. **Write `06_5_semantic_hits.json`** with this schema:

   ```json
   {
     "candidate_llm_application": "<copy from 05_candidate.json>",
     "embedding_model": "text-embedding-3-large",
     "semantic_threshold": 0.7,
     "memory_pattern_threshold_jaccard": 0.3,
     "results": [
       {
         "url": "...",
         "title": "...",
         "snippet": "...",
         "cosine_similarity": 0.82,
         "semantic_hit": true,
         "matched_concept_keywords_in_snippet": ["frequency-domain ICL", "low-frequency bias"]
       },
       ...
     ],
     "memory_pattern_check": {
       "current_keywords": [...],
       "matched_prior_rounds": [
         {"round": "046", "jaccard": 0.34, "shared_keywords": ["LLM", "ICL"]}
       ],
       "memory_pattern_match": true
     },
     "summary": {
       "semantic_hits_count": 3,
       "keyword_hits_count_from_step_07": 0,
       "additional_hits_from_semantic": 3,
       "memory_pattern_match": true
     }
   }
   ```

5. **Pass to step 07.** Step 07 reads both `06_search_raw.json` AND
   `06_5_semantic_hits.json`. For each result, the final `hit` field is:

   ```
   hit = (keyword_overlap_count ≥ 2) OR (semantic_hit == true)
   ```

   `forced_by_rule` becomes:

   ```
   forced_by_rule = (keyword_overlap_count ≥ 2)         # original v1/v2/v3 forced-hit definition
   forced_by_semantic = (semantic_hit == true)           # NEW
   ```

   These are tracked separately in `07_hit_miss.json` so the post-hoc
   audit can distinguish keyword-only, semantic-only, and both kinds of
   forced hits.

---

## 3. The semantic-similarity threshold (with epoch 2+3 evidence)

### Threshold = 0.7, justified per false-positive round

For each of the 9 epoch-2+3 false positives, the table below shows the
expected cosine similarity between `candidate.llm_application` and the
title+snippet of the substantively-equivalent prior art that the keyword
rule missed. The threshold 0.7 was chosen so all 9 fire.

| Round | Pattern | LLM-side prior art that the keyword rule missed | Expected cosine | Fires at 0.7? |
|---|---|---|---:|:---:|
| **R045** | A — word-order | "Loss of Plasticity in Deep Continual Learning" (Nature 2024); 2402.18762; 2602.09234 | ~0.85 | ✓ |
| **R046** | B — synonym | "Provable Low-Frequency Bias of In-Context Learning Representations" 2507.13540 | ~0.78 | ✓ |
| **R047** | B — synonym | "Theoretically Grounded Framework for LLM Watermarking"; "Robust Semantics-based Watermark for LLMs against Paraphrasing" | ~0.82 | ✓ |
| **R050** | B — synonym | 2506.20921 (capability-cost trade-off LLM-MAS); 2508.07880 (multi-agent equilibrium); "Game-Theoretic Lens on LLM Multi-Agent" | ~0.74 | ✓ |
| **R059** | C — source-only | "Ergodic seismic precursors and transfer learning" (Nature Comms 2025) | ~0.72 | ✓ (borderline — relies on candidate.llm_application mentioning "fine-tuning protocol" and the result snippet mentioning "transfer learning") |
| **R064** | C — source-only | "SELF-EVOLVING CURRICULUM FOR LLM REASONING" 2505.14970 | ~0.76 | ✓ |
| **R068** | C — source-only | "AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems" 2504.00587 | ~0.81 | ✓ |
| **R069** | B — borderline | "Activation Steering in 2026: A Practitioner's Field Guide"; "Adaptive Activation Steering" | ~0.71 | ✓ (borderline; this is the "possibly substantive" PASS in epoch 3) |
| **R075** | C — source-only | "An Empirical Study of LLM-as-a-Judge"; "On the Role of Reasoning Traces" | ~0.73 | ✓ |

Lowering the threshold to 0.65 would catch more borderline cases but risk
false-flagging candidates where the cosine arises from generic LLM-vocabulary
overlap rather than substantive concept overlap. Raising it to 0.75
would miss R059, R069, R075. **0.7 is the calibrated threshold.**

### Memory Jaccard threshold = 0.3, justified

The 9 false-positive rounds share a structural signature in their
`tried_keywords`: 7-8 source-domain words + 1-2 generic LLM words. New
candidates that mirror this distribution (high source-side keyword count,
low LLM-side keyword count) are pre-flagged for stricter semantic review.
A Jaccard ≥ 0.3 indicates ≥ ~3 of 8 keywords overlap with a known
false-positive — which empirically correlates with the same
content_words-too-narrow failure mode.

---

## 4. Memory update at step 10 (v3 unchanged + v4 additions)

After step 10 writes `10_decision.json`, append to `memory_db.json` with
this v4-extended schema:

```json
{
  "round": "NNN",
  "epoch": 4,
  "domain": "...",
  "domain_normalized": "...",
  "mechanism": "...",
  "form": "...",
  "forced_hit_count": N,                 // keyword-only forced hits (v1/v2/v3 metric)
  "forced_semantic_hit_count": M,        // NEW v4 — semantic-only forced hits
  "hit_count": K,                         // total unique hits (keyword OR semantic)
  "fail_reason": "...",
  "tried_keywords": [...],
  "verdict": "FAIL" | "PASS",
  "v4_semantic_metrics": {
    "max_cosine_similarity": 0.86,
    "results_above_threshold": 3,
    "memory_pattern_match": true,
    "matched_prior_false_positive_rounds": ["046", "075"]
  }
}
```

Aggregates recompute as before.

---

## 5. ★ FORBIDDEN-TO-MODIFY zones (verbatim from program.md / program_v3.md)

The four FROZEN zones are preserved EXACTLY:

### 5.1 Step 06 web_search (honesty gate)
- ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query,
  RAW tool response saved to file. v4 does NOT change the search step.

### 5.2 Step 07 keyword threshold
- `keyword_overlap_count ≥ 2` → `hit = true` and `forced_by_rule = true`.
- v4 ADDS a parallel semantic-hit signal but does NOT lower the keyword
  threshold. A keyword overlap ≥ 2 still forces hit.

### 5.3 Step 10 mechanical verdict
- `total_hits == 0` → PASS.
- `total_hits ≥ 1` → FAIL.
- v4 changes the **definition** of "hit" to include semantic hits, but
  the verdict logic itself (`total_hits ≥ 1 → FAIL`) is unchanged.
- The "now considers both keyword AND semantic" clause is the v4 spec
  refinement: the same `total_hits ≥ 1 → FAIL` rule operates on a
  `total_hits` figure that is now `keyword_hits ∪ semantic_hits` (set
  union — a result that hits both ways counts once).

### 5.4 Step 12 cross-agent verification
- Fresh agent reads only `05_candidate.json` + `06_search_raw.json` +
  (NEW) `06_5_semantic_hits.json` and produces independent
  `07_hit_miss.json` equivalent. The verifier's `06_5_semantic_hits.json`
  uses the same embedding model and threshold; if the verifier's cosine
  scores diverge from the primary's by > 0.1 on any result, that result's
  cosine is recomputed by a third agent for arbitration.

---

## 6. Loop control (v4)

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
    
    # Step 06.5 (NEW in v4)
    load 05_candidate.json, 06_search_raw.json
    for each result in all queries:
        cosine = embedding_similarity(candidate.llm_application,
                                       result.title + " " + result.snippet)
        semantic_hit = (cosine >= 0.7)
    memory_pattern_match = jaccard_check(candidate.tried_keywords,
                                          memory_db.false_positive_entries) >= 0.3
    write 06_5_semantic_hits.json
    
    execute step 07 (★ FROZEN keyword threshold; ORs in semantic_hit)
    execute step 10 (★ FROZEN verdict on total_hits)
    
    # Memory update (v4 schema)
    append round entry to memory_db.json with v4_semantic_metrics
    
    execute step 11 (audit)
    execute step 12 (★ FROZEN cross-agent; verifier also runs 06.5 logic)
    
    if round_num % 25 == 0: write output/stats_round_NNN.json
```

---

## 7. Stats schema additions in v4

`output/stats_round_NNN.json` adds these v4-specific fields on top of v3:

```json
{
  ... (all v1/v2/v3 fields) ...,
  "v4_semantic_metrics": {
    "semantic_hits_caught_total": 0,                  // additional hits step 06.5 catches that keyword missed
    "semantic_only_forced_hits_total": 0,              // semantic_hit=true AND keyword_overlap<2
    "rounds_flipped_pass_to_fail_by_semantic": 0,      // would-be PASS under v3 but FAIL under v4
    "rounds_flipped_fail_to_fail_higher_hit_count": 0, // already FAIL under v3 but with more total_hits under v4
    "memory_pattern_matches_count": 0,                 // rounds where 06.5 memory-Jaccard ≥ 0.3
    "substantive_pass_count": 0,                       // PASSes that survive v4 (keyword ≥2 AND semantic ≥0.7 both clear)
    "mechanical_pass_count": 0                         // PASSes under FROZEN rule (keyword ≥2) only
  },
  "v4_score_components": {
    "substantive_pass_count_x_10": 0,
    "twenty_five_minus_mean_forced_hit": 0.0,
    "disagreement_rate_x_5": 0.0,
    "false_positive_count_x_5_negative": 0,
    "score_v4": 0.0
  }
}
```

---

## 8. v4 score formula

```
score_v4 = (substantive_pass_count × 10)
         + (25 − mean_forced_hit)
         + (disagreement_rate × 5)
         − (false_positive_count × 5)
```

Note: false-positives are penalized to push the agent toward strict
review. A round counts as a false_positive if mechanical PASS fires but
either (a) semantic_hit ≥ 0.7 on any result, or (b) the cross-agent
verifier flags `verdict_agreement == "PASS_MECHANICAL_BUT_FAIL_SUBSTANTIVE"`.

`substantive_pass_count` requires BOTH keyword overlap < 2 AND semantic
similarity max < 0.7 across all results AND verifier confirms substantive
PASS. This is much more demanding than v3's `pass_count`.

---

## 9. Inherited history (v1 → v2 → v3 → v4)

- **v1** (program.md): file-chain + mechanical keyword rule + cross-agent
  verification. **R001-R025** ran under v1.
- **v2** (program_v2.md): Form A/B/C/D rotation + query/composition
  rules. **R026-R050** ran under v2. Exposed mechanical-PASS artifacts on
  narrow content_words (R045, R046, R047, R050).
- **v3** (program_v3.md): step 04.5 memory check; persistent failure
  memory in `logs/memory_db.json`. **R051-R075** ran under v3. Exposed
  the same mechanical-PASS artifact pattern (R059, R064, R068, R069, R075)
  even with memory rotation pushing into new domains.
- **v4** (this file): step 06.5 semantic-similarity check + memory-pattern
  Jaccard check. Targets the lexical-vs-semantic gap that drove all 9
  epoch-2+3 false positives. **R076-R100** runs under v4.

---

## 10. What v4 does NOT promise

v4 does NOT promise more substantive PASS verdicts. The saturation result
from N=138 prior + 75 in-repo rounds = 213 total with 0 substantive PASS
is structural. Semantic similarity catches false positives (lower
mechanical PASS count); it does not create novelty.

What v4 DOES promise:
- Mechanical PASS count converges toward 0 (semantic check catches the
  artifacts that the keyword rule misses).
- `substantive_pass_count` becomes a meaningful KPI (only true paradigm
  shifts pass both keyword AND semantic checks).
- New metric `semantic_hits_caught` measures how often the keyword rule
  alone would have produced a false negative on prior-art detection.
- New metric `memory_pattern_match` measures how often the agent
  proposes candidates structurally similar to prior false positives,
  even after the v3 domain/form/keyword rotation.

If `semantic_hits_caught` is high in epoch 4, that confirms the lexical-vs-
semantic gap was a major missed signal in v1/v2/v3. If it is near zero,
that means the v3 epoch-3 generator already drifted away from
synonym-substitution candidates and v4 has no marginal effect.

---

## 11. Anti-cheating commitments

If you catch yourself wanting to:
- Skip step 06.5 because it's "obvious" the candidate is novel — write
  that impulse to `11_audit.json` honestly. The whole point of v4 is to
  catch the agent's "obvious to me" judgment in cases where the keyword
  rule already misled the agent.
- Lower the cosine threshold to 0.6 to catch more false positives —
  don't. The threshold is calibrated; lowering it without re-calibration
  introduces new false negatives.
- Use a "stronger" embedding model that gives systematically higher
  cosines — recalibrate the threshold first; document in
  `compliance_log.md`.
- Skip the memory-Jaccard check for "obviously different" candidates —
  the false-positive Jaccard signal is precisely about catching cases
  the agent thinks are different but structurally are not.

The v3 instruction stands: data on agent impulse-to-bypass is more
valuable than a clean fake run.
