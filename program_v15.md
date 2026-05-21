# program_v15.md
## Niche-Mining Pipeline — v15: Intra-Cluster Diversification

This file extends the **v14 base pipeline** with ONE structural upgrade that addresses the v14 limitation diagnosed in E33: the k-means cluster centers selected by step 05.4 are diverse at the embedding level (large inter-cluster cosine distance) but can collapse onto a SINGLE INVESTIGATIVE niche at the mechanism level. Specifically, E33's 3 INVESTIGATIVE rounds (R805, R814, R823) were all Lie-group based — a single investigative niche that v14's diversity filter could not break apart.

> v14 successfully introduced HTS (heavy-tail 100-pool + k-means diversity filter), ATU (20-slot architecture-tool universe), and CPM (post-epoch coverage profile + Gini + undersaturated-slot feedback). It raised step 14 FIRED count from 2 (E32) to 3 (E33) and added max_over_100_attack_rebuttal_rate = 1.0 (threshold 0.30). But all 3 E33 INVESTIGATIVE rounds (R805 Adjoint, R814 SO(3), R823 SU(3)) are **mechanism-clones from the same investigative niche** (Lie-group equivariance). v15 adds **step 05.45 intra-cluster diversification** to break this collapse: it measures pairwise mechanism-vocabulary distance among the 25 selected candidates and replaces near-duplicates with farther-apart alternatives from the 100-pool.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

FROZEN verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL)
- **Step 12 tree-stream** (v8 helper + per-hint solver + conservative synthesis)
- **Step 13 spec format** (v10 contribution)
- **Step 13.5 attack format** (v11 contribution)
- **Step 14 cross-step coherence** (v13 contribution)
- **Step 14.5 coverage profile** (v14 contribution; v15 reads it but does not modify it)
- **Step 05.4 diversity filter** (v14 contribution; v15 reads it but does not modify it)
- **Step 05.5 anti-R279 mechanical filter** (v12 contribution)
- All v8, v9, v10, v11, v12, v13, v14 verdict labels and PASS criterion.

v15 is **strictly additive**. It ADDS step 05.45 (between step 05.4 and step 05.5). It does NOT modify any prior file, any prior step, or any prior verdict label.

---

## 0. Why intra-cluster diversification

### 0.1 v14's E33 limitation observed

E33 produced 3 INVESTIGATIVE_CANDIDATE rounds: R805 Adjoint-representation, R814 SO(3)-equivariant, R823 SU(3)-equivariant. While the k-means diversity filter spread the 25 selected candidates across 13 distinct architecture_tool_slots, the 3 INVESTIGATIVE rounds collapsed onto a single **investigative niche**: "Lie-group-equivariance-on-LLM-architecture". The +1 INVESTIGATIVE over E32 (R805 vs. nothing) is real but trivial — it's a third Lie-group variant.

The pipeline's diversity is measured at the **embedding level** (cosine distance between BoW representations of llm_application strings). Two Lie-group candidates have HIGH cosine distance at embedding level (SU(3) vs SO(3) use different tokens) but LOW investigative-niche distance (both modify attention via Lie-group equivariance with structurally identical Casimir/commutator rebuttals).

v14's step 05.4 measures EMBEDDING diversity. v15 adds step 05.45 measuring INVESTIGATIVE-NICHE diversity (architecture_tool_slot × mathematical-mechanism-family × attack-rebuttal-archetype).

### 0.2 The v15 upgrade

| Upgrade | Acronym | Source | Step affected | Touches FORBIDDEN? |
|---|---|---|---|---|
| **Intra-cluster diversification filter** | ICD | v15 NEW | step 05.45 NEW | NO (additive between 05.4 and 05.5) |

The single v15 addition. Symmetric with v14's step 05.4 (embedding diversity) and step 14.5 (post-epoch slot coverage); v15's step 05.45 occupies the gap between those two — within-epoch mechanism-family diversity.

### 0.3 What v15 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§9) — UNCHANGED.
- v14 step 05.4 k-means filter — UNCHANGED.
- v14 step 14.5 coverage profile — UNCHANGED.
- v14 logs/architecture_tools.json — UNCHANGED.
- PASS criterion floor (still 10 signals) — UNCHANGED.
- Verdict labels — UNCHANGED.

---

## 1. File chain (v14 + one addition)

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
    05_candidates_100.json           (v14 unchanged)
    05_4_diversity_filter.json       (v14 unchanged)
    05_45_intra_cluster_diversification.json   ← NEW v15
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
```

Per-epoch (post-25-rounds):
```
output/14_5_coverage_profile_E{N}.json   (v14)
```

---

## 2. Step 05.45 NEW — intra-cluster diversification (v15)

### 2.1 What step 05.45 does

After step 05.4 selects the 25 most-diverse cluster centers from the 100-pool, step 05.45 computes a **mechanism-niche distance matrix** on the 25 selected:

```
for i,j in range(25):
    distance[i,j] = combined_niche_distance(candidate_i, candidate_j)

combined_niche_distance(c_i, c_j) =
    0.4 * slot_distance(c_i, c_j)                    # 1 if different slot, 0 if same
  + 0.3 * domain_distance(c_i, c_j)                  # 1 if different math domain, 0 if same
  + 0.3 * mechanism_vocab_distance(c_i, c_j)         # Jaccard 1-J between source_words sets

if any pair (i,j) has distance < 0.5:
    keep the candidate with FEWER overlap-rounds in prior corpus (higher novelty signal)
    replace the other with the next-most-diverse from the 100-pool
        that has combined_niche_distance > 0.5 to all current 25
    log the replacement in 05_45_intra_cluster_diversification.json
```

The threshold 0.5 is calibrated: two candidates in the same slot AND same domain AND same mechanism-family have distance 0 (always collapses); two candidates in different slots OR different domains OR different mechanism-families have distance ≥ 0.4; two candidates differing on all three axes have distance 1.0.

Threshold 0.5 ensures that 2 of the 3 axes must differ for two candidates to count as "diverse niches". This is the operational definition of an **investigative niche**: (slot × math-domain × mechanism-family) triple.

### 2.2 Step 05.45 trigger logic

```
trigger_step_05_45 = (step_05_4.fired == True)
```

Step 05.45 ALWAYS fires when step 05.4 has produced its 25-selection (every v15 round). Output file `05_45_intra_cluster_diversification.json` is always present.

### 2.3 Step 05.45 output schema

```json
{
  "round": "NNN",
  "epoch": 14 + v_increment,
  "v15_index": true,
  "input_25_selected_from_05_4": [<25 candidate summaries>],
  "intra_cluster_pairwise_distance_matrix_summary": {
    "min_distance": 0.0,
    "mean_distance": 0.0,
    "max_distance": 1.0,
    "pairs_below_threshold_0_5_count": 0,
    "pairs_below_threshold_0_5_list": []
  },
  "near_duplicate_pairs_found": [
    {"i": <idx_in_25>, "j": <idx_in_25>, "distance": 0.0,
     "shared_dimensions": ["slot", "domain"]}
  ],
  "replacements_made": [
    {"original_idx": <idx>, "original_summary": "<text>",
     "replaced_with_pool_idx": <100-pool idx>,
     "replaced_summary": "<text>",
     "post_replacement_min_distance_to_25": 0.5}
  ],
  "primary_candidate_chosen_idx_after_05_45": <idx_in_25_post_replacement>,
  "corpus_unique_investigative_niches_so_far_in_epoch": <int>,
  "honest_detection_note": "Step 05.45 main-context-direct; deterministic from step 05.4 output + 100-pool; no Agent spawn required."
}
```

### 2.4 Constraints on step 05.45

- **Deterministic.** No Agent spawn; combined_niche_distance is a closed formula on three measurable axes.
- **Operates only on the 25 selected from step 05.4 + the 100-pool from step 05.** Does not modify either.
- **Replacement rule preserves the slot universe.** Replaced candidate must also have a valid architecture_tool_slot field.
- **Replacement rule preserves coverage-profile feedback.** If the original is in an undersaturated slot AND its replacement is in a saturated slot, prefer original (preserve CPM bias).
- **Replacement rule preserves max_over_100_attack_rebuttal projection.** Replacement should not decrease the projection.
- **Per HONEST DEVIATION POLICY ≤5 synthesized Agent spawns per epoch, step 05.45 is main-context-direct.** Deterministic; no spawn needed.

### 2.5 Effect on primary candidate selection

After step 05.45 runs, the primary candidate selection in step 05.5 operates on the POST-replacement 25-selection (not the original 25). Otherwise step 05.5 protocol unchanged.

---

## 3. v15 metric definitions

### 3.1 corpus_unique_investigative_niches (the v15 thesis metric)

A **unique investigative niche** is a (slot × domain × mechanism-family) triple from an INVESTIGATIVE_CANDIDATE round, where mechanism-family is the dominant mathematical structure name extracted from the candidate's specific_mechanism string.

```
unique_investigative_niches_E{N} = |{(slot_i, domain_i, mech_family_i) for i in INVESTIGATIVE_rounds_E{N}}|
```

E32 v13 had 2 INVESTIGATIVE (R777 Quiver/alg-geom/Schubert + R787 Crystal-basis/alg-geom/Crystal-basis) — 2 unique niches (different mechanism-families even though same slot+domain). E33 v14 had 3 INVESTIGATIVE all in Lie-groups family — **1 unique investigative niche**.

v15's target: corpus_unique_investigative_niches_E34 ≥ 2 (preferably 3).

### 3.2 step_05_45_replacement_rate

Fraction of rounds where step 05.45 replaced at least 1 of the 25 selected candidates:

```
step_05_45_replacement_rate_E{N} = (count of rounds with replacements_made.length > 0) / 25
```

### 3.3 mean_intra_cluster_niche_distance

Mean of the pairwise combined_niche_distance over the 25 selected (post-replacement) candidates:

```
mean_intra_cluster_niche_distance_E{N} = mean(distance_matrix_post_05_45[i,j] for i<j) over all rounds in E{N}
```

Target: ≥ 0.6 (each pair of selected candidates differs on ≥1.5 axes on average).

---

## 4. v15 score formula

```
score_v15 = score_v14 components (all 30 v1-v14 terms, UNCHANGED)
          + (step_05_45_fired_count / N × 1)            ← NEW v15 (deterministic; always 1.0 in epoch)
          + (mean_intra_cluster_niche_distance × 3)     ← NEW v15
          + (corpus_unique_investigative_niches / 3 × 4)  ← NEW v15 (normalized by target 3)
```

Where:
- `step_05_45_fired_count / N × 1`: confirms the filter fires every round.
- `mean_intra_cluster_niche_distance × 3`: rewards within-epoch mechanism-family diversity.
- `corpus_unique_investigative_niches / 3 × 4`: rewards distinct investigative niches discovered per epoch (target 3).

NO negative terms specific to v15.

**confirmed_substantive_pass under v15** (UNCHANGED from v14): same 10 signals.

---

## 5. Loop control (v15)

```
read logs/policy_state.json
read logs/architecture_tools.json
read prior epoch coverage profile (E33.json under v14)
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute (UNCHANGED)
    execute step 04.5

    generate_100_candidates(prompt_with_slot_universe + coverage_bias)  # v14
    write 05_candidates_100.json

    compute_embeddings(100 candidates)
    cluster_assign = kmeans(embeddings, k=25, seed=epoch)               # v14 step 05.4
    selected_25 = candidates near each cluster center
    write 05_4_diversity_filter.json

    # NEW v15 step 05.45 intra-cluster diversification
    compute_pairwise_niche_distance_matrix(selected_25)
    near_duplicate_pairs = pairs with distance < 0.5
    for (i,j) in near_duplicate_pairs:
        keep one with fewer corpus overlap; replace the other from 100-pool
    write 05_45_intra_cluster_diversification.json

    # Choose primary candidate from POST-REPLACEMENT 25
    for candidate in selected_25_post_replacement:
        run step 05.5
        if architectural_topology_change_TRUE: PRIMARY = candidate; break
    if PRIMARY == None:
        PRIMARY = highest slot-novelty from 25_post_replacement
        run step 05.5 regeneration

    write 05_candidate.json (PRIMARY)
    write 05_5_pattern_filter.json

    execute step 06, 06.5, 06.7, 07
    execute step 08, 09
    execute step 10
    execute step 11, 11.5, 12
    execute step 13, 13.5
    execute step 14

    compute v15_verdict (UNCHANGED from v14)
    update memory_db.json with v15 fields including step_05_45 outputs

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
        compute coverage_profile (v14 step 14.5)
        write output/14_5_coverage_profile_E{N}.json
        compute corpus_unique_investigative_niches_E{N}
        update logs/policy_state.json
```

---

## 6. v15 verdict synthesis

v15_verdict = v14_verdict (UNCHANGED).

v15 adds NO new verdict label. Contribution is at the candidate-selection level (step 05.45), upstream of all verdict-producing steps.

---

## 7. ★ FORBIDDEN-TO-MODIFY zones — verbatim from v5...v14

### 7.1 Step 06, 07, 10, 11.5, 12, 13, 13.5, 14, 14.5 — UNCHANGED
### 7.2 v8, v9, v10, v11, v12, v13, v14 components — UNCHANGED
### 7.3 Step 05.4 k-means filter — UNCHANGED

v15 is purely ADDITIVE: step 05.45 NEW between step 05.4 and step 05.5.

---

## 8. Stats schema additions in v15

`output/stats_round_NNN.json` adds:

```json
{
  ... (all v1-v14 fields) ...,
  "v15_ICD_metrics": {
    "step_05_45_fired_count": 25,
    "step_05_45_rounds_with_replacements_count": 0,
    "step_05_45_total_replacements_count": 0,
    "step_05_45_replacement_rate": 0.0,
    "mean_intra_cluster_niche_distance_E{N}": 0.0,
    "mean_pairs_below_threshold_per_round": 0.0,
    "corpus_unique_investigative_niches_E{N}": 0,
    "investigative_niche_tuples_E{N}": [],
    "real_step_05_45_Agent_spawns": 0,
    "main_context_direct_step_05_45_count": 25
  }
}
```

---

## 9. Inherited history (v1 → v15)

- **v1-v14**: see prior program_vN.md files.
- **v15** (this file): v14 base + step 05.45 intra-cluster diversification. **R826-R850 under v15 in E34.**

---

## 10. What v15 does NOT promise

v15 does NOT promise more substantive PASS verdicts. The 921-round saturation result (0 confirmed substantive PASS, p ≈ 0.0000967 on 1%-novelty H₀ at N=921) stands.

What v15 promises:
- **Within-epoch mechanism-family diversity** at the 25-selection level.
- A breakup of the E33 single-niche INVESTIGATIVE collapse (all Lie-groups).
- corpus_unique_investigative_niches ≥ 2 in E34 (preferably 3).

v15 cannot detect external collision with literature. **That is a v16 concern.** v15's diversity is **internal** (within-pipeline among the 100-pool's selection).

---

## 11. Honest deviation policy (for E34 execution)

Same as v14 (max 5 synthesized Agent spawns per epoch). Step 05.45 is main-context-direct (deterministic).

---

## 12. Phase 4 reporting requirements (for output/epoch34_comparison.md)

After E34 completes, the comparison document must record:
1. step 05.45 replacement statistics (rate, mean replacements per round).
2. mean_intra_cluster_niche_distance_E34.
3. corpus_unique_investigative_niches_E34 + the tuples.
4. v15 score with the 3 new terms.
5. cumulative N_verified after E34 = 946.
6. p(no PASS | 1% H₀) at N=946 ≈ 0.0000760.
7. Comparison of INVESTIGATIVE niches: E33 all Lie-groups (1 niche); E34 → multiple niches expected.
