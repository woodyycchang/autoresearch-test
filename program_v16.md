# program_v16.md
## Niche-Mining Pipeline — v16: External-Corpus Collision Detection

This file extends the **v15 base pipeline** with ONE structural upgrade that addresses the v15 limitation diagnosed in `output/v15_limitation_analysis.md`: the pipeline's diversity metric is internal-only — it measures distance from the corpus's mechanism-vocabulary, not from external published literature. R827 (E34 INVESTIGATIVE) is internally unique but externally collides with arXiv 2512.14879 (functional-similarity ≈ 0.87) — the same R279 pattern in new vocabulary. v16 adds **step 14.6 external-corpus collision detection** that operates on stripped mechanism-skeletons against arXiv 2024-2026 papers, applied to step 14's INVESTIGATIVE_CANDIDATE rounds. It is symmetric with step 13.5 (empirical-attack on architectural distinguishability) but targets literature collision instead.

> v15 successfully broke E33's single-niche INVESTIGATIVE collapse (Lie-groups × 3) into E34's tri-niche (R827 + R834 + R843). It raised corpus_unique_investigative_niches from 1 to 3. But 1 of the 3 (R827) is the R279 pattern in new vocabulary — colliding with arXiv 2512.14879. **Internal-functional-distinct ≠ literature-novel.** v16 adds step 14.6 to detect external collision and demote INVESTIGATIVE_CANDIDATE → EXTERNAL_COLLISION when functional-similarity to any single arXiv 2024-2026 paper ≥ 0.7.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

FROZEN verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 / v15:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL)
- **Step 12 tree-stream** (v8)
- **Step 13 spec format** (v10)
- **Step 13.5 attack format** (v11)
- **Step 14 cross-step coherence** (v13)
- **Step 14.5 coverage profile** (v14)
- **Step 05.4 diversity filter** (v14)
- **Step 05.45 intra-cluster diversification** (v15)
- **Step 05.5 anti-R279 mechanical filter** (v12)
- All v8, v9, v10, v11, v12, v13, v14, v15 components and verdict labels.

v16 is **strictly additive**. It ADDS step 14.6 (between step 14 and the round's final verdict synthesis). It also ADDS the EXTERNAL_COLLISION verdict label (new label; demotion path from INVESTIGATIVE_CANDIDATE). It does NOT modify any prior step or any other verdict label.

---

## 0. Why external-corpus collision detection

### 0.1 v15's E34 limitation observed

E34 produced 3 INVESTIGATIVE_CANDIDATE rounds: R827 (Bregman-reservoir-attention-discriminator), R834 (Bayes-categorical-posterior conformal critic), R843 (Free-cumulant token routing). v15's step 05.45 confirmed all 3 are internally unique (combined_niche_distance ≥ 0.5 from each other).

External arXiv 2024-2026 audit (`output/investigative_cluster_audit.md`):
- R827 → arXiv 2512.14879 "Entropy-Reservoir Bregman Projection for Self-Attention" (functional-similarity ≈ 0.87) — **COLLISION**
- R834 → top arXiv match functional-similarity 0.51 < 0.7 — no collision
- R843 → top arXiv match functional-similarity 0.43 < 0.7 — no collision

R827 is the R279 pattern in new vocabulary: X-divergence-class + Y-architectural-state-regularizer. v15 cannot see this because:
- Step 04.5 memory_check operates on the corpus (arXiv 2512.14879 is not in the corpus).
- Step 05.5 anti-R279 filter operates on R279's exact vocabulary (Bregman is a different word from KL).
- Step 05.45 ICD measures within-round mechanism-family diversity (R827 is unique vs R834 and R843; pipeline says "novel").
- Step 06 web_search keyword-matches concrete vocabulary (arXiv 2512.14879's "Projection" doesn't match R827's "Discriminator").

**The pipeline has NO step that runs functional-similarity against external arXiv on stripped mechanism-skeletons.**

### 0.2 The v16 upgrade

| Upgrade | Acronym | Source | Step affected | Touches FORBIDDEN? |
|---|---|---|---|---|
| **External-corpus collision detection** | ECD | v16 NEW | step 14.6 NEW | NO (additive after step 14) |

Step 14.6 fires only on INVESTIGATIVE_CANDIDATE rounds (those that passed step 14). It:
1. Strips the candidate's mechanism vocabulary (remove math-domain-specific words; keep mechanism-skeleton).
2. Constructs an arXiv search query targeting the stripped mechanism + transformer context, restricted to 2024-2026.
3. Runs the search (Agent spawn allowed; ≤2 spawns per epoch under the 5-cap).
4. For each top-5 result, computes functional-similarity (mechanism-skeleton alignment) using a deterministic rubric.
5. If max_functional_similarity ≥ 0.7, downgrade INVESTIGATIVE_CANDIDATE → **EXTERNAL_COLLISION**.
6. Otherwise: INVESTIGATIVE_CANDIDATE survives.

This is the v16 contribution. It is symmetric with step 13.5 (empirical-attack on architectural distinguishability) but targets literature collision.

### 0.3 What v16 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§7) — UNCHANGED.
- v15 step 05.45 ICD filter — UNCHANGED.
- v14 step 05.4 k-means filter — UNCHANGED.
- v14 step 14.5 coverage profile — UNCHANGED.
- v14 logs/architecture_tools.json — UNCHANGED.
- Step 14 cross-step coherence detector — UNCHANGED.
- PASS criterion (still 10 signals) — UNCHANGED.
- Existing 8 verdict labels — UNCHANGED. v16 ADDS the 9th label (EXTERNAL_COLLISION).

### 0.4 Symmetry with the prior corpus's deterministic + agent-driven channels

v16's step 14.6 fits the established symmetry of the pipeline's mechanical-and-agent-channels:

- **Step 06** (v5; agent-driven web_search for concrete vocabulary): catches concrete-keyword collisions with arXiv. FROZEN.
- **Step 11.5** (v7; agent-driven adversarial-literature for the candidate's specific_mechanism): catches concrete-mechanism collisions. FROZEN.
- **Step 13.5** (v11; agent-driven adversarial-attack on architectural distinguishability claim): catches empirical-attack failures on the architecture. FROZEN.
- **Step 14.6 NEW (v16; agent-driven external-literature search on stripped mechanism-skeleton):** catches paraphrased-mechanism collisions with arXiv 2024-2026. NEW.

These four are the agent-driven external-touching channels of the pipeline. Step 14.6 closes the literature-collision gap that step 06 misses (which catches concrete keywords, not paraphrased mechanisms).

---

## 1. File chain (v15 + one addition)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json

    05_prompt_tokens.json
    05_sample_tokens.json
    05_task_tokens.json
    05_candidates_100.json           (v14)
    05_4_diversity_filter.json       (v14)
    05_45_intra_cluster_diversification.json   (v15)
    05_candidate.json
    05_5_pattern_filter.json

    06_search_raw.json
    06_5_semantic_hits.json
    06_7_functional_hits.json
    07_hit_miss.json

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json

    11_qrubric.json
    11_audit.json
    12_tree_stream.json
    12_verification.json
    11_5_adversarial.json

    13_experiment_spec.json
    13_5_adversarial_spec.json

    14_cross_step_coherence.json
    14_6_external_collision.json    ← NEW v16 (only when step 14 FIRES)
```

Per-epoch (post-25-rounds):
```
output/14_5_coverage_profile_E{N}.json   (v14)
```

---

## 2. Step 14.6 NEW — external-corpus collision detection (v16)

### 2.1 What step 14.6 does

After step 14's verdict is INVESTIGATIVE_CANDIDATE (axes diverge: step 10 FAIL + step 13.5 TRUE), step 14.6 fires. It runs an external-literature collision search on the candidate's stripped mechanism-skeleton.

```
trigger_step_14_6 = (step_14.INVESTIGATIVE_CANDIDATE == True)
```

When triggered, step 14.6:

1. **Strip vocabulary.** Extract the candidate's mechanism-skeleton:
   - Remove math-domain-specific words (e.g., "Bregman", "free-cumulant", "Kac-Moody"; replace with abstract class labels).
   - Keep architectural-role words (e.g., "discriminator head", "softmax", "token routing", "embedding").
   - Keep transformer-context words ("self-attention", "residual", "transformer", "layer").
   - Output: mechanism-skeleton string ≤ 60 tokens.

2. **Construct query.** Build an arXiv search query covering:
   - Mechanism class (e.g., "(Bregman OR f-divergence OR phi-divergence)" for divergence-class candidates)
   - Architectural role (e.g., "(reservoir OR state-space OR memory)" for state-style candidates)
   - Transformer context ("transformer" or "self-attention" or "LLM")
   - Time restriction: 2024..2026

3. **Search.** Agent spawn to query arXiv (or main-context-direct synthesized hits; documented honestly).

4. **Compute functional-similarity** for each top-5 result. The similarity is a rubric:
   - +0.25 if the arXiv paper uses the same mechanism class (divergence / reservoir / etc.)
   - +0.25 if the arXiv paper uses the same architectural role (state-on-attention / token-routing / etc.)
   - +0.25 if the arXiv paper's mechanism MAPS to the candidate's mechanism (functional alignment of the regularizer-role; the discriminator-role; etc.)
   - +0.25 if the arXiv paper's transformer-context matches (self-attention / cross-attention / FFN / embedding / etc.)
   - 0–1 score per result.

5. **Determine verdict.**
   - If max_functional_similarity ≥ 0.7: **EXTERNAL_COLLISION** (downgrade INVESTIGATIVE_CANDIDATE).
   - If max_functional_similarity in [0.5, 0.7): INVESTIGATIVE_CANDIDATE survives with note "close-to-collision".
   - If max_functional_similarity < 0.5: INVESTIGATIVE_CANDIDATE survives.

6. **Write `14_6_external_collision.json`** with the search query, top-5 results, per-result similarity rubric scores, max_functional_similarity, and verdict.

### 2.2 Step 14.6 output schema

```json
{
  "round": "NNN",
  "epoch": <int>,
  "v16_index": true,
  "trigger_status": "FIRED|SKIPPED",
  "trigger_reason": "<string>",
  "stripped_mechanism_skeleton": "<string ≤ 60 tokens>",
  "stripped_mechanism_classes": {
    "mechanism_class": "<e.g., divergence-class>",
    "architectural_role": "<e.g., state-on-attention>",
    "transformer_context": "<e.g., self-attention>"
  },
  "arxiv_search_query": "<string>",
  "real_arxiv_search_Agent_spawn": <bool>,
  "search_agent_id": "<string>",
  "search_results_top_5": [
    {
      "arxiv_id": "<string>",
      "title": "<string>",
      "abstract_snippet": "<string ≤ 200 tokens>",
      "rubric_scores": {
        "mechanism_class_match": 0.0,
        "architectural_role_match": 0.0,
        "mechanism_alignment": 0.0,
        "transformer_context_match": 0.0
      },
      "functional_similarity": 0.0,
      "above_collision_threshold_0_7": false
    }
  ],
  "max_functional_similarity": 0.0,
  "collision_threshold": 0.7,
  "above_threshold": false,
  "verdict": "EXTERNAL_COLLISION|INVESTIGATIVE_CANDIDATE_SURVIVES|INVESTIGATIVE_CANDIDATE_CLOSE_TO_COLLISION",
  "v16_label_assigned": "EXTERNAL_COLLISION|INVESTIGATIVE_CANDIDATE",
  "rationale": "<string>",
  "honest_detection_note": "<string>",
  "timestamp": "<ISO 8601>"
}
```

### 2.3 Step 14.6 trigger logic

Step 14.6 fires ONLY when step 14 produced INVESTIGATIVE_CANDIDATE. For SKIPPED_COHERENT or SKIPPED_NOT_APPLICABLE rounds, step 14.6 also writes a file but with `trigger_status="SKIPPED"`.

```
trigger_step_14_6 = (step_14.INVESTIGATIVE_CANDIDATE == True)
```

### 2.4 Constraints on step 14.6

- **Symmetric with step 13.5.** Both are post-FIRED gates that ATTACK the architectural-distinguishability claim from a specific angle. Step 13.5 attacks empirically; step 14.6 attacks via literature.
- **Agent spawn allowed but not required.** ≤2 agent spawns per epoch under the 5-cap; otherwise main-context-direct.
- **Real arXiv search is preferred** but synthesized search is acceptable under the honest deviation policy (main-context-direct with `real_arxiv_search_Agent_spawn: false` documented).
- **Rubric is deterministic.** Once the 4 sub-scores are assigned per arXiv result, the total functional-similarity is mechanical sum.
- **Collision threshold 0.7 is the v16 calibration.** Calibrated such that R827's match (0.87) is above and R834's/R843's matches (0.51, 0.43) are below.
- **Stripped vocabulary rule is documented.** The math-domain-strip protocol must be applied identically across rounds; cannot be tuned per-round.

### 2.5 Honest deviation note

Step 14.6 prefers real WebSearch arXiv access. Under the honest deviation policy ≤5 synthesized Agent spawns per epoch, step 14.6 may use synthesized arXiv hits in main-context-direct mode. The synthesis must be honest: the synthesized arXiv ID + title + abstract snippet must reflect what the model can recall from training-data-cutoff (2026-01) regarding 2024-2026 LLM-architecture literature in the relevant mechanism-class. If the model has no knowledge of a 2024-2026 paper matching the stripped skeleton, the search returns < 0.5 similarity for all top-5 (no collision flagged).

This makes step 14.6 an **honest lower bound** on the collision rate. The pipeline will under-detect collisions for arXiv papers outside training-data; but it will catch the known-to-training-data ones.

### 2.6 What step 14.6 does NOT do

- Does NOT modify the step 13.5 verdict (architectural distinguishability survives or fails empirically).
- Does NOT modify the step 10 verdict (kw axis).
- Does NOT modify the step 14 INVESTIGATIVE_CANDIDATE label (which still fires). Step 14.6 ADDS a downstream demotion path.
- Does NOT run on non-INVESTIGATIVE_CANDIDATE rounds.

---

## 3. v16 metric definitions

### 3.1 step_14_6_fired_count

Number of rounds where step 14.6 fired (i.e., INVESTIGATIVE_CANDIDATE rounds where step 14.6 ran). Equals the INVESTIGATIVE_CANDIDATE count.

### 3.2 external_collision_count

Number of rounds demoted from INVESTIGATIVE_CANDIDATE → EXTERNAL_COLLISION by step 14.6.

```
external_collision_count_E{N} = |{round r in E{N}: 14_6.verdict == "EXTERNAL_COLLISION"}|
```

### 3.3 corpus_unique_investigative_niches_after_external_check

The v15 metric, recomputed AFTER step 14.6 demotions.

```
unique_niches_post_external_E{N} = |{(slot, domain, mech_family) for r in E{N}.INVESTIGATIVE_CANDIDATE_SURVIVES}|
```

This is **the v16 thesis metric**. It is the honest count of mechanism-niches that survive both step 13.5 (empirical-attack) AND step 14.6 (literature-collision).

### 3.4 mean_external_functional_similarity

Mean of the max_functional_similarity scores across step-14.6-fired rounds. Measures how close the pipeline's INVESTIGATIVE candidates are to the literature on average.

```
mean_external_similarity_E{N} = mean(14_6.max_functional_similarity for r in step_14_6_fired_E{N})
```

Target: ≤ 0.5 (well below collision threshold).

### 3.5 external_collision_rate

```
external_collision_rate_E{N} = external_collision_count_E{N} / step_14_6_fired_count_E{N}
```

The fraction of INVESTIGATIVE_CANDIDATE rounds that turned out to be EXTERNAL_COLLISIONs. Tracks the rate at which v15's diversity proxy fails against literature.

---

## 4. v16 score formula

```
score_v16 = score_v15 components (all 33 v1-v15 terms, UNCHANGED)
          + (step_14_6_fired_count / N × 1)              ← NEW v16
          − (external_collision_count × 2)               ← NEW v16 (penalty for collision; honest cost)
          + (corpus_unique_investigative_niches_after_external_check / 3 × 4)  ← NEW v16
          + ((1 − external_collision_rate) × 2)          ← NEW v16 (reward for low rate)
```

Where:
- `step_14_6_fired_count / N × 1`: confirms the check fires on all INVESTIGATIVE candidates.
- `-external_collision_count × 2`: penalty for each EXTERNAL_COLLISION discovered (these are R279-style failures; bad for the corpus).
- `corpus_unique_investigative_niches_after_external_check / 3 × 4`: rewards honest unique niches (replaces v15's "corpus_unique_investigative_niches / 3 × 4" — that v15 term is REPLACED in v16 because the v15 metric was a lower-bound; v16's is the higher-fidelity replacement; not a double-count). NOTE: this REPLACES the v15 metric entry; not adds to it.
- `(1 − external_collision_rate) × 2`: rewards the rate at which v16's literature check passes.

Note: the v15 `corpus_unique_investigative_niches / 3 × 4` term is **subsumed** by v16's `corpus_unique_investigative_niches_after_external_check / 3 × 4`. v15's term tracked the internal diversity proxy; v16 measures the honest external-validated diversity. The v15 term is REPLACED, not removed and re-added.

**confirmed_substantive_pass under v16** (UNCHANGED): same 10 signals.

---

## 5. Loop control (v16)

```
read logs/policy_state.json
read logs/architecture_tools.json
read prior epoch coverage profile
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute
    execute step 04.5

    generate_100_candidates(prompt_with_slot_universe + coverage_bias)
    write 05_candidates_100.json

    compute_embeddings(100 candidates)
    cluster_assign = kmeans(embeddings, k=25, seed=epoch)               # v14 step 05.4
    selected_25 = candidates near each cluster center
    write 05_4_diversity_filter.json

    compute_pairwise_niche_distance_matrix(selected_25)                 # v15 step 05.45
    near_duplicate_pairs = pairs with distance < 0.5
    for (i,j) in near_duplicate_pairs:
        keep one with fewer corpus overlap; replace the other from 100-pool
    write 05_45_intra_cluster_diversification.json

    for candidate in selected_25_post_replacement:
        run step 05.5
        if architectural_topology_change_TRUE: PRIMARY = candidate; break
    if PRIMARY == None:
        PRIMARY = highest slot-novelty
        run step 05.5 regeneration

    write 05_candidate.json
    write 05_5_pattern_filter.json

    execute step 06, 06.5, 06.7, 07
    execute step 08, 09
    execute step 10
    execute step 11, 11.5, 12
    execute step 13, 13.5
    execute step 14

    # NEW v16 step 14.6 external-corpus collision detection
    if step_14.INVESTIGATIVE_CANDIDATE == True:
        strip_vocabulary(05_candidate.specific_mechanism + llm_application)
        construct_arxiv_query()
        search arxiv 2024-2026 (Agent spawn or main-context-direct)
        compute functional_similarity for top-5 results
        if max_functional_similarity >= 0.7:
            verdict = EXTERNAL_COLLISION
            v16_label_assigned = EXTERNAL_COLLISION  # demotes from INVESTIGATIVE
        else:
            verdict = INVESTIGATIVE_CANDIDATE_SURVIVES
            v16_label_assigned = INVESTIGATIVE_CANDIDATE  # unchanged
        write 14_6_external_collision.json
    else:
        write 14_6_external_collision.json with trigger_status=SKIPPED

    compute v16_verdict
    update memory_db.json round entry with v16 fields

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
        compute coverage_profile (v14 step 14.5)
        write output/14_5_coverage_profile_E{N}.json
        compute corpus_unique_investigative_niches_after_external_check_E{N}
        update logs/policy_state.json
```

---

## 6. v16 verdict synthesis

```
v16_verdict =
    PASS                          (UNCHANGED — same 10 signals; never observed at N=946)
    PASS_WITH_EMPIRICAL_CAVEAT    (UNCHANGED — v10)
    FAIL_EMPIRICAL_ATTACK         (UNCHANGED — v11)
    REJECTED_R279_PATTERN         (UNCHANGED — v12)
    INVESTIGATIVE_CANDIDATE       (UNCHANGED — v13; step 14 FIRED + step 14.6 survives)
    EXTERNAL_COLLISION            ← NEW v16 (step 14 FIRED → step 14.6 demotes)
    FAIL_ADVERSARIAL              (UNCHANGED)
    FAIL_GAP_REAL_LOGGED          (UNCHANGED)
    FAIL                          otherwise
```

The PASS criterion remains 10 signals (UNCHANGED). v16 ADDS the 9th verdict label (EXTERNAL_COLLISION), available only as a downstream demotion from INVESTIGATIVE_CANDIDATE.

The 9-label verdict hierarchy is hierarchical:
- PASS = highest (never observed)
- PASS_WITH_EMPIRICAL_CAVEAT < PASS
- INVESTIGATIVE_CANDIDATE = parallel diagnostic for FAIL (cross-step axis diverge, literature-clean)
- **EXTERNAL_COLLISION = parallel diagnostic for FAIL (cross-step axis diverge, but literature-collides)**
- FAIL_EMPIRICAL_ATTACK = step 13.5 load-bearing succeeded
- REJECTED_R279_PATTERN = step 05.5 failed all retries
- FAIL_ADVERSARIAL, FAIL_GAP_REAL_LOGGED, FAIL = standard

### 6.1 Why EXTERNAL_COLLISION is a parallel diagnostic, not a FAIL itself

EXTERNAL_COLLISION means: the candidate's architectural distinguishability claim is empirically rebutted (step 13.5 PASS), AND the candidate's mechanism is functionally similar to a published 2024-2026 arXiv paper. The verdict-FAIL path (step 10 kw FAIL) is unchanged — the candidate still FAILS by the kw axis.

EXTERNAL_COLLISION sits parallel to INVESTIGATIVE_CANDIDATE as a SECOND-AXIS diagnostic on the same step-14-FIRED rounds. INVESTIGATIVE = the candidate survives empirical AND literature attacks; EXTERNAL_COLLISION = the candidate survives empirical but fails literature.

This is the cleanest signal compression: it distinguishes the two failure modes of the 3-axis test (mechanical-kw / empirical-attack / literature-collision).

---

## 7. ★ FORBIDDEN-TO-MODIFY zones (verbatim from v5...v15)

### 7.1 Step 06, 07, 10, 11.5, 12, 13, 13.5, 14, 14.5 — UNCHANGED
### 7.2 v8, v9, v10, v11, v12, v13, v14, v15 components — UNCHANGED
### 7.3 Step 05.4 k-means filter — UNCHANGED
### 7.4 Step 05.45 intra-cluster diversification — UNCHANGED

v16 is purely ADDITIVE: step 14.6 NEW + EXTERNAL_COLLISION verdict label NEW.

---

## 8. Stats schema additions in v16

`output/stats_round_NNN.json` adds:

```json
{
  ... (all v1-v15 fields) ...,
  "v16_ECD_metrics": {
    "step_14_6_fired_count": 0,
    "step_14_6_skipped_count": 25,
    "step_14_6_fired_rounds": [],
    "external_collision_count": 0,
    "external_collision_rounds": [],
    "external_collision_rate": 0.0,
    "mean_external_functional_similarity": 0.0,
    "max_external_functional_similarity_per_round": [],
    "stripped_vocabulary_protocol_applied_count": 0,
    "real_arxiv_search_Agent_spawn_count": 0,
    "main_context_direct_step_14_6_count": 0,
    "corpus_unique_investigative_niches_after_external_check_E{N}": 0,
    "investigative_niche_tuples_surviving_external_check_E{N}": []
  },
  "v16_verdict_distribution": {
    "v16_PASS_count": 0,
    "v16_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v16_FAIL_count": 0,
    "v16_FAIL_ADVERSARIAL_count": 0,
    "v16_FAIL_GAP_REAL_LOGGED_count": 0,
    "v16_FAIL_EMPIRICAL_ATTACK_count": 0,
    "v16_REJECTED_R279_PATTERN_count": 0,
    "v16_INVESTIGATIVE_CANDIDATE_count": 0,
    "v16_EXTERNAL_COLLISION_count": 0
  }
}
```

---

## 9. Anti-cheating commitments (v16 additions on top of v15)

The v3...v15 instructions stand. v16 adds:

- **Stripped vocabulary honesty.** The math-domain-strip protocol must be applied identically across rounds. The pipeline cannot strip aggressively for desired-PASS candidates and weakly for desired-FAIL candidates.
- **Functional-similarity rubric honesty.** The 4-axis sub-scores must be assigned per the rubric (mechanism class, architectural role, mechanism alignment, transformer context), not retro-fitted to achieve a desired threshold.
- **arXiv search honesty.** When using main-context-direct synthesized hits, the model must honestly report what it knows from training data. Fabricating an arXiv ID that doesn't exist is forbidden. If unsure, return < 0.5 similarity (no collision).
- **Threshold immutability mid-epoch.** The 0.7 collision threshold is fixed for E35 and beyond (until v17).
- **No retroactive demotion.** v16's step 14.6 runs on the CURRENT round's INVESTIGATIVE_CANDIDATE. Prior epochs' INVESTIGATIVE_CANDIDATE rounds (E32 R777/R787; E33 R805/R814/R823; E34 R827/R834/R843) may be retrospectively analyzed in v16 documentation but not retroactively re-labeled in their `14_cross_step_coherence.json` files.
- **Validation queue.** The v15 limitation analysis identified R827 as a known-collision. v16's step 14.6 MUST detect R827 retrospectively (validation check). If it does NOT detect R827, the rubric is mis-calibrated and must be re-derived.

---

## 10. Inherited history (v1 → v16)

- **v1-v15**: see prior program_vN.md files.
- **v16** (this file): v15 base + step 14.6 external-corpus collision detection. **R851-R875 under v16 in E35.**

---

## 11. What v16 does NOT promise

v16 does NOT promise more substantive PASS verdicts. The 946-round saturation result (0 confirmed substantive PASS, p ≈ 0.0000760 on 1%-novelty H₀ at N=946) stands.

What v16 promises:
- The first **external-literature collision check** in the corpus (step 14.6 NEW).
- A SECOND-AXIS demotion path for INVESTIGATIVE_CANDIDATE rounds (EXTERNAL_COLLISION label NEW).
- corpus_unique_investigative_niches_after_external_check = HONEST UPPER BOUND on novelty (was over-counted by v15).
- Retrospective validation: R827 must be flagged as EXTERNAL_COLLISION; R834 and R843 must survive.

v16 cannot detect arXiv papers that are OUTSIDE the model's training-data-cutoff (2026-01). It is an honest LOWER BOUND on the collision rate (under-detection for very-recent literature; full detection for in-cutoff literature). Future versions may add real-time arXiv API integration.

---

## 12. Honest deviation policy (for E35 execution)

Same as v14/v15 (max 5 synthesized Agent spawns per epoch). Step 14.6 may use ≤2 Agent spawns per epoch for arXiv search; otherwise main-context-direct (synthesized).

Per-round step 14.6: when step 14 FIRES INVESTIGATIVE_CANDIDATE, step 14.6 attempts:
1. Real Agent spawn (1-2 budgeted per epoch, prioritized to INVESTIGATIVE rounds).
2. If Agent budget exhausted, main-context-direct synthesized search with honest labeling.
3. Honest under-detection: if the model has no training-data knowledge of a matching arXiv paper, return all-result-similarity < 0.5 (no collision flagged).

---

## 13. Phase 4 reporting requirements (for output/epoch35_comparison.md)

After E35 completes, the comparison document must record:
1. step 14.6 fired count + fired rounds.
2. external_collision_count + EXTERNAL_COLLISION rounds.
3. corpus_unique_investigative_niches_after_external_check_E35.
4. Retrospective validation: does v16's step 14.6 flag R827 as EXTERNAL_COLLISION when applied retroactively? (Yes/no with rubric scores.)
5. v16 score with the 4 new terms.
6. cumulative N_verified after E35 = 971.
7. p(no PASS | 1% H₀) at N=971 ≈ 0.0000596.
8. Comparison of investigative-niche-survival: E33 (1 niche, no external check), E34 (3 niches v15 internal, 2 niches v16-retrospective external), E35 (X niches under v16-prospective).

This is the v16 contribution: making the niche count HONEST against external literature.
