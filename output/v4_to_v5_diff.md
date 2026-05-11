# v4 → v5 Diff

**Author:** Claude (Opus 4.7)
**Date:** 2026-05-11
**Branch:** `claude/continue-niche-mining-research-OxqsL`

This document summarises the differences between `program_v4.md` and
`program_v5.md`. v5 adds **one new step (06.7)** plus a new metric
field on `memory_db.json` entries and a new score-formula term. The
five FORBIDDEN-TO-MODIFY zones are preserved exactly.

---

## 1. Single new step: 06.7 (LLM-judge functional equivalence)

### Position in file chain

```
v4: 06_search_raw → 06_5_semantic_hits → 07_hit_miss → 10_decision
v5: 06_search_raw → 06_5_semantic_hits → 06_7_functional_hits → 07_hit_miss → 10_decision
                                          ^^^^^^^^^^^^^^^^^^^^
                                          NEW
```

### What 06.7 does

For each of the top-10 results in `06_search_raw.json` (by relevance
rank, deduplicated by URL), invoke an LLM-judge in a fresh context.
The judge sees:
- `candidate.llm_application` (full text)
- one search result (title + URL + snippet)

And returns:
```json
{"score": 0.0..1.0, "justification": "<one sentence>",
 "matched_effect_cluster": "<3-5 word phrase>"}
```

A `judge_score ≥ 0.7` forces `functional_hit = true` for that result.

### Why this is needed (epoch 4 evidence)

All 4 epoch-4 PASSes (R079, R085, R091, R092) were:
- `forced_hit_count == 0` (keyword rule missed them — all 8 content_words
  were source-side, no LLM-vocabulary anchor)
- `forced_semantic_hit_count == 0` (semantic cosine < 0.7 against all
  results — one synonym-hop gap)
- Yet web_search for the FUNCTIONAL content (not the source vocabulary)
  returns multiple 2024-2026 LLM papers covering the same end-state
  mechanism

See `output/epoch4_functional_audit.md` for the per-round audit.

### How 06.7 catches what 06.5 misses

`06.5` computes cosine between `candidate.llm_application` and
`result.title + " " + result.snippet`. This is a single-shot
sentence-embedding distance that fails when:
- The candidate phrases the LLM-side mechanism differently from the
  prior art (e.g., "vitrify parameters" vs "4-bit quantization")
- The prior art mentions only one half of the candidate's bridge
  (the candidate spans source+LLM; the prior art uses only LLM
  terminology)
- The embedding model has poor cross-domain alignment between source
  vocabulary and LLM vocabulary (e.g., "antifreeze glycoprotein" and
  "anti-correlated SGD noise" are far apart in any general-purpose
  embedding)

`06.7` asks an LLM explicitly: "does this paper achieve the same
FUNCTIONAL effect, regardless of vocabulary or metaphor?" This is a
reasoning task that an embedding cannot solve, but a language model can.

---

## 2. New schema field on `06_7_functional_hits.json`

Brand-new file. Schema:

```json
{
  "candidate_llm_application": "<copy from 05_candidate.json>",
  "judge_model": "claude-opus-4-7",
  "judge_prompt_hash": "sha256:...",
  "functional_threshold": 0.7,
  "results": [
    {
      "rank": 1, "url": "...", "title": "...", "snippet": "...",
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

---

## 3. Step 07 reads three input files instead of two

### v4
```
step 07 inputs: 05_candidate.json, 06_search_raw.json, 06_5_semantic_hits.json
hit = (keyword_overlap_count ≥ 2) OR (semantic_hit == true)
```

### v5
```
step 07 inputs: 05_candidate.json, 06_search_raw.json,
                06_5_semantic_hits.json, 06_7_functional_hits.json
hit = (keyword_overlap_count ≥ 2)
   OR (semantic_hit == true)
   OR (functional_hit == true)
```

`07_hit_miss.json` adds a `forced_by_functional` field per-result.

---

## 4. Memory-DB entry adds `v5_functional_metrics` field

### v4 entry
```json
{
  "round": "NNN", "epoch": 4, ...
  "forced_hit_count": N,
  "forced_semantic_hit_count": M,
  "hit_count": K,
  "v4_semantic_metrics": {...}
}
```

### v5 entry
```json
{
  "round": "NNN", "epoch": 5, ...
  "forced_hit_count": N,
  "forced_semantic_hit_count": M,
  "forced_functional_hit_count": L,        // NEW
  "hit_count": K,                           // now keyword ∪ semantic ∪ functional
  "v4_semantic_metrics": {...},
  "v5_functional_metrics": {                 // NEW
    "max_judge_score": 0.85,
    "results_above_threshold": 4,
    "distinct_effect_clusters": 2,
    "multi_cluster_match": true,
    "matched_effect_clusters": [...]
  }
}
```

---

## 5. Score formula: same shape, expanded `substantive_pass_count` and `false_positive_count` definitions

### v4
```
score_v4 = (substantive_pass_count × 10) + (25 − mean_forced_hit) + (disagreement_rate × 5) − (false_positive_count × 5)
where:
  substantive_pass_count counts rounds with keyword <2 AND semantic <0.7 AND verifier-confirmed
  false_positive_count counts rounds with mechanical PASS but semantic ≥0.7 or verifier disagreement
```

### v5
```
score_v5 = (substantive_pass_count × 10) + (25 − mean_forced_hit) + (disagreement_rate × 5) − (false_positive_count × 5)
where:
  substantive_pass_count counts rounds with keyword <2 AND semantic <0.7 AND functional <0.7 AND verifier-confirmed
  false_positive_count counts rounds with mechanical PASS but ANY of (semantic ≥0.7, functional ≥0.7, verifier disagreement)
```

The formula's shape is unchanged. Only the predicates feeding
`substantive_pass_count` and `false_positive_count` are tightened by
the new functional channel.

---

## 6. Forbidden zones unchanged

| Zone | v4 status | v5 status |
|---|---|---|
| Step 06 web_search honesty gate | FROZEN | FROZEN |
| Step 06.5 semantic threshold (cosine ≥0.7 → forced hit) | FROZEN | FROZEN — v5 does NOT lower or replace |
| Step 07 keyword threshold (≥2 → forced hit) | FROZEN | FROZEN |
| Step 10 mechanical verdict (total_hits ≥1 → FAIL) | FROZEN | FROZEN — verdict logic identical; only the definition of "hit" expanded to include functional hits |
| Step 12 cross-agent verification | FROZEN | FROZEN — verifier now also reruns 06.7 |

---

## 7. Per-round artifact list (v4 vs v5)

```
v4 round outputs:
  01_future.md
  02_decomposition.json
  03_papers.json
  04_life_analogy.md
  04_5_memory_check.json
  05_candidate.json
  06_search_raw.json        ★
  06_5_semantic_hits.json
  07_hit_miss.json          ★
  10_decision.json          ★
  11_audit.json
  12_verification.json      ★

v5 round outputs (+ one file):
  01_future.md
  02_decomposition.json
  03_papers.json
  04_life_analogy.md
  04_5_memory_check.json
  05_candidate.json
  06_search_raw.json        ★
  06_5_semantic_hits.json   ★
  06_7_functional_hits.json ← NEW (v5)
  07_hit_miss.json          ★
  10_decision.json          ★
  11_audit.json
  12_verification.json      ★
```

---

## 8. Calibration evidence for the 0.7 functional threshold

The threshold is calibrated on the 4 epoch-4 false positives from
`output/epoch4_functional_audit.md`:

| Round | Expected judge score on best prior art | Fires at 0.7? |
|---|---:|:---:|
| R079 (phyllotaxis) | 0.85 | ✓ |
| R085 (tribology) | 0.78 | ✓ |
| R091 (tardigrade) | 0.82 | ✓ |
| R092 (icefish AFGP) | 0.92 | ✓ |

All four fire. Lowering to 0.6 would risk false-flagging genuinely
different mechanisms (where the judge is uncertain but the function is
not actually identical). Raising to 0.8 would miss R085.

---

## 9. Compatibility note

v5 is fully backward-compatible with v1-v4 artifacts in the rounds/
folder. The new file `06_7_functional_hits.json` is only present for
R101+. Aggregates over R001-R100 ignore the new field. The score
formula is shape-identical and uses the same `forced_hit_count`
notion (keyword-only) for `mean_forced_hit`, so cross-epoch comparison
remains direct.
