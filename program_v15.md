# program_v15.md
## Niche-Mining Pipeline — v15: Intra-Cluster Diversification (Anti-INVESTIGATIVE-Cluster Penalty)

This file extends the **v14 base pipeline** with ONE new structural upgrade that directly addresses the v14 limitation diagnosed in `output/investigative_cluster_audit.md`: the 7 corpus INVESTIGATIVE_CANDIDATE rounds (R756, R770, R777, R787, R805, R814, R823) form **ONE latent cluster** (mean off-diagonal cosine similarity 0.589; single-linkage cluster count = 1 at all thresholds ≤ 0.50; ALL 7 share the same `variant_equivalence` A1 attack category and the same "training penalty maintains non-trivial structure" rebuttal template) — not 7 independent niches.

> v14 successfully raised attack-rebuttal rate from v13's 2/3 to 3/4 (E33 R805/R814/R823) via heavy-tail sampling. But the +1 candidate (R805 Adjoint) is from the SAME Lie-groups latent region as 3 of the 4 prior INVESTIGATIVE candidates. v14 over-mines one region; it does not diversify across regions. The corpus INVESTIGATIVE-coverage is ONE cluster sampled 7 times. v15 introduces an **anti-cluster diversity penalty at step 05.45** (additive between v14's step 05.4 and v12's step 05.5) that penalizes embedding proximity to ALL prior INVESTIGATIVE_CANDIDATE — forcing the generator to find candidates in DIFFERENT latent regions.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

The following zones are **FROZEN** verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14:

- **Step 06 web_search** (honesty gate; forbidden per v15 task)
- **Step 07 keyword threshold ≥ 2** (forbidden per v15 task)
- **Step 10 mechanical verdict** (forbidden per v15 task)
- **Step 12 tree-stream** (forbidden per v15 task)
- **Step 13 spec format** (forbidden per v15 task)
- **Step 13.5 attack format** (forbidden per v15 task)
- **Step 14 cross-step coherence** (forbidden per v15 task)
- **Step 14.5 coverage profile** (forbidden per v15 task)
- **Step 05.4 diversity filter** (forbidden per v15 task)
- **Step 05.5 anti-R279 mechanical filter** (v12 contribution; v15 reads it but does not modify it)
- **All v8 components** (step 05 token streams FORMAT, step 11 Q-rubric)
- **All v9 components** (step 08 inverse-search, step 09 gap-position)
- **All v10 components** (step 13 spec generation, logs/policy_state.json policy update, PASS_WITH_EMPIRICAL_CAVEAT verdict label)
- **All v11 components** (step 13.5 attack, FAIL_EMPIRICAL_ATTACK verdict label)
- **All v12 components** (step 05.5 anti-R279 filter, REJECTED_R279_PATTERN verdict label)
- **All v13 components** (step 14 coherence detector, INVESTIGATIVE_CANDIDATE verdict label)
- **All v14 components** (step 05 100-candidate ENHANCED, step 05.4 k-means diversity filter, step 14.5 coverage profile + Gini, logs/architecture_tools.json)

v15 is **strictly additive**. It ADDS step 05.45 (between v14's step 05.4 and v12's step 05.5). It does NOT modify any prior file, any prior step, or any prior verdict label. v14's heavy-tail 100-pool generation, k-means clustering, and coverage profile remain intact.

The step 05 token streams FORMAT is preserved; v15 ENHANCES nothing in step 05 itself. v15 adds an additive `cluster_proximity_to_prior_investigative` field on the primary `05_candidate.json` (additive — old readers ignore it).

---

## 0. Why intra-cluster diversification at step 05.45 and not the other options

### 0.1 The four options enumerated in the v15 task

The Phase-2 task gave four options:
- **(a) Intra-cluster diversification at step 05** — penalize embedding proximity to ALL prior INVESTIGATIVE_CANDIDATE.
- **(b) Per-candidate empirical priority via runnable Stage-1.5 toy spec** (extend step 13).
- **(c) Cross-investigative ablation at step 14.5** (flag duplicates post-hoc).
- **(d) Reverse-engineer step 10 detector boundary** (use kw near-miss to bias step 05).

### 0.2 Why (a) is the direct evidence-driven choice

The cluster audit (`output/investigative_cluster_audit.md`) shows:
- 7 corpus INVESTIGATIVE candidates form ONE single-linkage cluster at all thresholds ≤ 0.50.
- Mean off-diagonal pairwise cosine similarity = 0.589 (close to v14 step 05.4 INTRA-cluster regime ~0.73; far from inter-cluster ~0.28).
- ALL 7 use `variant_equivalence` as the load-bearing A1 attack category (1/4 of available categories).
- ALL 7 use the same "training penalty maintains non-trivial algebraic structure" rebuttal template.
- 4/7 are in the Lie-groups domain (over-represented).
- 7/7 are in `architecturally_deep_slots_for_max_over_100_projection` (architecturally-deep slot subset only).

The corpus is exploring ONE region and labeling it INVESTIGATIVE 7 times. Heavy-tail sampling (v14) raised the SAMPLES-PER-EPOCH from this region; it did not find samples OUTSIDE the region. (a) directly fixes this by penalizing candidate proximity to the 7 known cluster members at generation time, forcing the generator into LATENT REGIONS not yet INVESTIGATIVE-labeled.

### 0.3 Why not (b)

(b) generates Stage-1.5 runnable toy experiment specs per INVESTIGATIVE candidate. Useful for downstream validation; does NOT change candidate distribution. The 7 we'd run experiments on are the same 7 in the same cluster. (b) is a downstream-prioritization tool, not a diversification tool. Defer to v16 once intra-cluster diversification (v15) has surfaced multi-cluster INVESTIGATIVE coverage.

### 0.4 Why not (c)

(c) flags structural duplicates post-hoc at step 14.5. The cluster audit shows the 7 ARE structural duplicates — (c) would label them as such but generate nothing new. (a) is the generative counterpart of (c): instead of flagging duplicates post-hoc, prevent them at generation. Critically, (a) subsumes part of (c): v15's step 05.45 writes a `cluster_proximity_to_prior_investigative` field per candidate, which IS the duplicate-flag computed at generation time. So (c)'s diagnostic content is captured by (a)'s implementation.

### 0.5 Why not (d)

(d) reverse-engineers step 10's keyword detector boundary. The cluster axis (intra-cluster proximity) is ORTHOGONAL to the step-10-kw axis. (d) would be useful in a v16+ that wants to bias TOWARD-PASS candidates; the present problem is bias AWAY-FROM-OVER-MINED-CLUSTER. Different axes. Also: the cluster audit shows the 7 INVESTIGATIVE candidates all have step-10 total_hits ∈ {1, 2} — they ARE already near the kw boundary. Pushing closer to kw=0 doesn't help if the latent region is already over-mined.

### 0.6 v15 implementation summary

| Upgrade | Acronym | Source | Step affected | Touches FORBIDDEN? |
|---|---|---|---|---|
| **A. INTRA-CLUSTER DIVERSIFICATION** | ICD | this v15; cluster audit | step 05.45 NEW (between step 05.4 and step 05.5) | NO (step 05.4 and step 05.5 are FROZEN; step 05.45 is purely additive) |

v15 adopts ONE upgrade. The closed loop: v14 generates 100 candidates and selects 25 via k-means cluster centers; v15 reorders / filters the 25 by embedding distance from the corpus's prior INVESTIGATIVE candidates. This ensures the primary candidate chosen for downstream pipeline execution is NEW relative to the existing cluster.

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
    05_candidates_100.json           ★ FROZEN (v14 contribution)
    05_4_diversity_filter.json       ★ FROZEN (v14 contribution)
    05_45_anti_cluster_score.json    ← NEW v15 (ICD): per-candidate cluster proximity to prior INVESTIGATIVE; primary selection re-ranking
    05_candidate.json                (UNCHANGED schema + NEW additive cluster_proximity_to_prior_investigative + cluster_distance_rank fields)
    05_5_pattern_filter.json         ★ FROZEN (v12 contribution)

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN
    06_7_functional_hits.json        ★ FROZEN
    07_hit_miss.json                 ★ FROZEN

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json                 ★ FROZEN

    11_qrubric.json
    11_audit.json
    12_tree_stream.json              ★ FROZEN
    12_verification.json
    11_5_adversarial.json            ★ FROZEN

    13_experiment_spec.json          ★ FROZEN
    13_5_adversarial_spec.json       ★ FROZEN

    14_cross_step_coherence.json     ★ FROZEN (v13)
```

Per-epoch (post-25-rounds):
```
output/14_5_coverage_profile_E34.json         ★ FROZEN (v14 schema)
output/15_intra_cluster_diversity_E34.json    ← NEW v15 (ICD): epoch-level intra-cluster-diversity report
```

Logs (additions):
```
logs/architecture_tools.json             ★ FROZEN (v14)
logs/policy_state.json                   (UNCHANGED schema + NEW additive intra_cluster_diversity_aggregates field group)
logs/investigative_cluster_state.json    ← NEW v15 (ICD): corpus-wide list of prior INVESTIGATIVE candidates with their cached BoW embedding; read by step 05.45
```

A v15 round MUST contain all v14 files PLUS `05_45_anti_cluster_score.json`. A v15 epoch MUST produce `output/15_intra_cluster_diversity_E{epoch}.json` after the 25-th round AND maintain `logs/investigative_cluster_state.json` (append each new INVESTIGATIVE round).

---

## 2. Step 05.45 NEW — anti-cluster diversity penalty (v15 ICD)

### 2.1 What step 05.45 does

After v14's step 05.4 selects 25 most-diverse candidates from the 100-pool, step 05.45 computes each of the 25 candidates' EMBEDDING DISTANCE from EVERY prior corpus INVESTIGATIVE_CANDIDATE. This produces a per-candidate `cluster_proximity_to_prior_investigative` score (max cosine similarity across all prior INVESTIGATIVE) and a `cluster_distance_rank` (rank among the 25).

The downstream primary-selection rule (originally "first to pass step 05.5") is REPLACED with a two-stage rule:
1. **Filter:** discard any of the 25 candidates with `cluster_proximity_to_prior_investigative ≥ CLUSTER_PROXIMITY_THRESHOLD` (default = 0.60, calibrated from cluster audit mean intra-corpus sim 0.589 + safety margin).
2. **Select:** of the remaining (after filter), choose the FIRST that passes step 05.5 (v12 anti-R279 mechanical classifier). If 0 of the filtered remain, fall back to v14's choice rule (highest slot-novelty among the original 25) and apply v12 regeneration.

This routes the heavy-tail's k-means cluster centers toward candidates DISTANT from the existing 7 INVESTIGATIVE cluster, while preserving v12's architectural-topology filter.

### 2.2 Embedding source for step 05.45

Step 05.45 uses the SAME deterministic BoW-hashed embedding as v14's step 05.4 (D=256; signed md5 projection; L2-normalized). This guarantees:
- Reproducibility (deterministic).
- Consistency with v14's k-means cluster centers (same embedding space; cluster centers stable across runs).
- No additional Agent spawn (computation is mechanical).

The embedding input per candidate is the concatenation:
```
specific_mechanism + " " + llm_application + " " + sub_mechanisms + " " + content_words + " " + domain + " " + candidate_form
```
(same as the cluster audit; see `output/investigative_cluster_audit.md` §3.)

### 2.3 Prior INVESTIGATIVE candidates list

`logs/investigative_cluster_state.json` stores the corpus-wide INVESTIGATIVE list:

```json
{
  "version": "1.0",
  "created": "2026-05-21T18:00:00Z",
  "created_by": "v15 init",
  "description": "Corpus-wide list of every INVESTIGATIVE_CANDIDATE round with cached embedding for step 05.45 anti-cluster diversity penalty.",
  "embedding_dim": 256,
  "embedding_method": "deterministic_bow_md5_signed_l2",
  "corpus_investigative_rounds": [
    {"round": "756", "epoch": 31, "domain": "Lie-groups", "form": "context-gating", "slot": "S19", "specific_mechanism": "SU(2)-equivariant transformation module", "embedding": [<256 floats>]},
    {"round": "770", "epoch": 31, "domain": "tropical-geometry", "form": "spectral-allocation", "slot": "S01", "specific_mechanism": "tropical attention layer", "embedding": [<256 floats>]},
    {"round": "777", "epoch": 32, "domain": "representation-theory", "form": "memory-architecture", "slot": "S09", "specific_mechanism": "Quiver-representation pathway module", "embedding": [<256 floats>]},
    {"round": "787", "epoch": 32, "domain": "representation-theory", "form": "spectral-allocation", "slot": "S01", "specific_mechanism": "Crystal-basis attention layer", "embedding": [<256 floats>]},
    {"round": "805", "epoch": 33, "domain": "Lie-groups", "form": "context-gating", "slot": "S19", "specific_mechanism": "Adjoint-representation equivariant module", "embedding": [<256 floats>]},
    {"round": "814", "epoch": 33, "domain": "Lie-groups", "form": "spectral-allocation", "slot": "S01", "specific_mechanism": "SO(3)-equivariant attention scoring", "embedding": [<256 floats>]},
    {"round": "823", "epoch": 33, "domain": "Lie-groups", "form": "spectral-allocation", "slot": "S06", "specific_mechanism": "SU(3)-equivariant softmax", "embedding": [<256 floats>]}
  ],
  "last_updated": "2026-05-21T18:00:00Z",
  "expected_corpus_unique_niches_at_threshold_0_40": 1,
  "rationale_per_audit": "All 7 corpus INVESTIGATIVE candidates form ONE single-linkage cluster at thresholds <=0.50; mean pairwise cosine 0.589. See output/investigative_cluster_audit.md."
}
```

The file is maintained APPEND-ONLY. Each new INVESTIGATIVE round (as labeled by step 14) is added to the list at end-of-round. The embedding is computed once and cached.

### 2.4 Step 05.45 output file

`05_45_anti_cluster_score.json` per round:

```json
{
  "round": "NNN",
  "epoch": <int>,
  "v15_index": true,
  "input_25_candidates_count": 25,
  "prior_investigative_count": <int>,  // 7 at start of E34; grows with each new INVESTIGATIVE
  "cluster_proximity_threshold": 0.60,
  "per_candidate_scores": [
    {
      "candidate_idx_in_25": 0,
      "specific_mechanism": "<short title>",
      "architecture_tool_slot": "<slot ID>",
      "cluster_proximity_to_prior_investigative_max": <float 0-1>,  // max cosine similarity to any of the 7+
      "cluster_proximity_to_prior_investigative_argmax_round": "<round of nearest prior INVESTIGATIVE>",
      "cluster_proximity_to_prior_investigative_mean": <float 0-1>,
      "cluster_distance_rank": <int 1-25>,  // 1 = most distant from prior cluster
      "is_filtered_by_cluster_threshold": <bool>  // true if cluster_proximity_max >= threshold
    },
    ...
  ],
  "filtered_candidate_indices": [<list of indices passing the threshold filter>],
  "filter_pass_count": <int 0-25>,
  "filter_pass_rate": <float 0-1>,
  "primary_selection_path": "filtered_first_to_pass_05_5 | fallback_highest_slot_novelty",
  "primary_candidate_idx_in_25": <int>,
  "primary_candidate_cluster_proximity_to_prior_investigative_max": <float>,
  "primary_candidate_cluster_distance_rank": <int>,
  "v15_diagnostic": "<one paragraph: how many of 25 pass; which prior INVESTIGATIVE was the closest; whether primary is from a new region>",
  "real_step_05_45_Agent_spawn": false,
  "main_context_direct_step_05_45_count": 1,
  "honest_computation_note": "Step 05.45 is deterministic from logs/investigative_cluster_state.json + 25 BoW embeddings; no Agent spawn required."
}
```

### 2.5 Step 05.45 trigger logic

```
trigger_step_05_45 = (step_05_4 has selected 25 candidates) AND (logs/investigative_cluster_state.json exists with at least 1 prior INVESTIGATIVE)
```

If `logs/investigative_cluster_state.json` is empty (no prior INVESTIGATIVE; would only happen if v15 were run from scratch before any INVESTIGATIVE), step 05.45 outputs a no-op record with `prior_investigative_count = 0` and the filter is a NO-OP (all 25 pass; v14 selection rule applies unchanged).

At the start of E34, `corpus_investigative_rounds` contains 7 entries (R756, R770, R777, R787, R805, R814, R823). After each new INVESTIGATIVE round in E34, the entry is appended (so step 05.45 in later E34 rounds sees more priors).

### 2.6 Primary candidate selection algorithm (v15)

```python
def select_primary_v15(candidates_25, cluster_state, threshold=0.60):
    # Compute proximity for each of 25
    scored = []
    for idx, c in enumerate(candidates_25):
        emb_c = embed(c.specific_mechanism + " " + c.llm_application + ...)
        max_sim = max(cosine(emb_c, prior.embedding) for prior in cluster_state.corpus_investigative_rounds)
        argmax_prior = argmax(...)
        scored.append((idx, c, max_sim, argmax_prior))

    # Sort by cluster_distance_rank (most distant first; tiebreak: candidate_idx_in_25)
    scored.sort(key=lambda x: (x[2], x[0]))  # ascending similarity
    for rank, (idx, c, max_sim, argmax_prior) in enumerate(scored, 1):
        c.cluster_distance_rank = rank
        c.cluster_proximity_to_prior_investigative = max_sim

    # Filter
    filtered = [s for s in scored if s[2] < threshold]
    if len(filtered) == 0:
        # Fallback: v14 rule applies (highest slot novelty)
        return v14_fallback_select(candidates_25), "fallback_highest_slot_novelty"

    # Filtered: choose FIRST to pass step 05.5 (v12 anti-R279)
    for idx, c, max_sim, argmax_prior in filtered:
        if step_05_5_classifier(c).architectural_topology_change_TRUE:
            return c, "filtered_first_to_pass_05_5"

    # If 0 in filtered pass step 05.5: regen via v12 on the most-distant filtered candidate
    most_distant = filtered[0][1]
    return v12_regenerate(most_distant), "filtered_regenerate"
```

The selection rule is deterministic given the 25 candidates and the cluster state. Real Agent spawn: 0.

### 2.7 Constraints on step 05.45

- **Deterministic from `logs/investigative_cluster_state.json` + 25 candidate embeddings.** No Agent spawn.
- **CLUSTER_PROXIMITY_THRESHOLD = 0.60** (default; calibrated from cluster audit). v15 freezes this at 0.60 for E34. v16 may calibrate based on observed E34 cluster_diversity metrics.
- **The 25 candidate set is NOT modified.** Step 05.45 only re-orders / filters at the PRIMARY-SELECTION level. The 25 in `05_4_diversity_filter.json` are preserved (v14 frozen).
- **Cluster state file is APPEND-ONLY.** Each new INVESTIGATIVE round adds an entry. No deletions; no edits.
- **Embedding method is FROZEN at deterministic BoW md5 D=256.** Switching embedding methods mid-corpus would invalidate the cluster state's cached embeddings.
- **The threshold filter MAY produce 0 valid candidates** (filter_pass_count = 0). In that case the fallback (v14 rule) preserves pipeline continuity. The diagnostic field `primary_selection_path` records which path was taken.

---

## 3. Logs/investigative_cluster_state.json maintenance protocol

### 3.1 Initialization (one-time at v15 start)

Before E34 begins, initialize `logs/investigative_cluster_state.json` with the 7 corpus INVESTIGATIVE rounds and their cached BoW embeddings. Read each of the 7 candidates' `05_candidate.json`, compute the embedding once, save in JSON. This is a one-time bootstrap.

### 3.2 Per-INVESTIGATIVE append rule

After step 14 in each round, if the round is labeled INVESTIGATIVE_CANDIDATE:
1. Compute the round's candidate embedding (same method).
2. Append to `corpus_investigative_rounds` list with fields {round, epoch, domain, form, slot, specific_mechanism, embedding}.
3. Update `last_updated` timestamp.

### 3.3 Read protocol for step 05.45

Step 05.45 reads `logs/investigative_cluster_state.json` ONCE at the start of each round (after the 25-candidate selection completes). The list MAY have grown since the prior round (if the prior round was INVESTIGATIVE). This ensures step 05.45 in later E34 rounds sees the latest cluster state.

### 3.4 Cross-investigative ablation diagnostic at step 14.5 (v15 ICD wrapping v14 CPM)

After v14's step 14.5 fires (post-25-rounds), v15 ADDS a coverage-profile-equivalent for INVESTIGATIVE candidates: `output/15_intra_cluster_diversity_E{N}.json`:

```json
{
  "epoch": <int>,
  "rounds_range": "RXXX-RYYY",
  "prior_investigative_count_at_epoch_start": 7,
  "new_investigative_in_epoch_count": <int>,
  "corpus_investigative_count_at_epoch_end": <int>,
  "intra_corpus_pairwise_cosine_mean": <float>,
  "intra_corpus_pairwise_cosine_max": <float>,
  "intra_corpus_pairwise_cosine_min": <float>,
  "single_linkage_cluster_count_at_threshold_0_40": <int>,
  "single_linkage_cluster_count_at_threshold_0_50": <int>,
  "single_linkage_cluster_count_at_threshold_0_60": <int>,
  "epoch_new_investigative_max_proximity_to_prior": [
    {"round": "<RXXX>", "max_proximity": <float>, "argmax_prior_round": "<RYYY>", "is_structural_duplicate_of_prior": <bool>}
  ],
  "epoch_new_investigative_passes_diversification_test": <bool>,
  "diversification_test_criterion": "new INVESTIGATIVE max_proximity < 0.40 to all prior",
  "v15_diagnostic": "<one paragraph: did v15 produce INVESTIGATIVE candidates outside the prior cluster?>",
  "honest_computation_note": "Deterministic from 25 candidates + cluster state; no Agent spawn."
}
```

This is the CROSS-INVESTIGATIVE ABLATION diagnostic from option (c) — provided as a SUB-feature of (a). It records both: per-new-INVESTIGATIVE structural-duplicate flag AND the corpus-wide intra-cluster diversity metric.

---

## 4. v15 metric definitions

### 4.1 cluster_proximity_to_prior_investigative_mean (v15 ICD primary metric)

Computed per round:
```
cluster_proximity_to_prior_investigative_mean = mean over 25 candidates of max cosine similarity to any of the prior INVESTIGATIVE
```

LOW values indicate the 25 are far from the existing cluster (v15's ICD is working — generator is producing novel-region candidates). HIGH values indicate the 25 still center on the cluster (ICD is fighting an attractor).

### 4.2 filter_pass_rate (v15 ICD primary metric)

```
filter_pass_rate = (count of candidates with cluster_proximity_max < 0.60) / 25
```

This is the fraction of v14's k-means cluster centers that ALREADY are distant from the prior INVESTIGATIVE cluster. v15 wants this HIGH (most of the 25 are novel; v15 only needs to filter the few in-cluster candidates).

### 4.3 primary_candidate_cluster_distance_rank (v15 ICD per-round)

The rank (1 = most distant) of the chosen primary candidate within the 25. With v15 ICD active, this is biased toward LOWER ranks (more distant). v14 would have produced rank ≈ 13 on average (middle of pack); v15 targets rank ≤ 8 on average.

### 4.4 corpus_unique_investigative_niches (v15 ICD corpus-wide metric)

Number of single-linkage clusters across ALL corpus INVESTIGATIVE rounds at threshold 0.40. v14 baseline = 1 (single cluster from cluster audit). v15 target = ≥ 2 (multi-cluster INVESTIGATIVE coverage).

This is the corpus-wide deduped INVESTIGATIVE niche count. Each cluster represents a distinct latent region the corpus has detected as architecturally-distinct attack-rebutted.

### 4.5 epoch_new_investigative_passes_diversification_test (v15 ICD success criterion)

For each NEW INVESTIGATIVE round in the epoch, check whether its max proximity to prior INVESTIGATIVE is < 0.40. If ALL new INVESTIGATIVE rounds pass this test, the epoch passes diversification.

```
epoch_passes_diversification = all(new_INVESTIGATIVE_round.max_proximity_to_prior < 0.40)
```

This is the v15 ICD's binary success criterion at the epoch level.

---

## 5. v15 score formula

```
score_v15 = (confirmed_substantive_pass × 10)
          + (25 − mean_forced_hit)
          + (tree_stream_step_10_alignment_rate × 5)
          − (false_positive_count × 5)
          − (adversarial_hit_count × 10)
          + (qrubric_step_10_alignment_rate × 3)
          + (mean_hints_per_round / 7 × 2)
          + (gap_real_rate × 4)
          + (FAIL_GAP_REAL_LOGGED_count / N × 2)
          + (step_13_fired_count / N × 3)
          + (step_13_distinguishable_count / N × 4)
          − (PASS_WITH_EMPIRICAL_CAVEAT × 2)
          + (policy_drift_score × 2)
          + (step_13_5_fired_count / N × 3)
          + (step_13_5_attack_success_rate × 3)
          − (FAIL_EMPIRICAL_ATTACK × 1)
          + (verdict_shift_v10_to_v11_count × 1)
          + (step_05_5_rejection_rate × 3)
          + (architectural_topology_change_rate × 4)
          + (regeneration_success_rate × 2)
          − (REJECTED_R279_PATTERN_count × 1)
          + (step_14_fired_count / N × 3)
          + (INVESTIGATIVE_CANDIDATE_count / N × 4)
          + (cross_step_axis_divergence_rate × 2)
          + (max_over_100_attack_rebuttal_rate × 5)             // v14 HTS
          + (architecture_slot_assignment_rate × 3)             // v14 ATU
          + (distinct_slots_hit / 20 × 4)                       // v14 CPM
          + ((1 − coverage_profile_concentration_index) × 4)    // v14 CPM
          + (undersaturated_slot_biased_count / N × 2)          // v14 CPM
          + ((1 − cluster_proximity_to_prior_investigative_mean) × 5)   ← NEW v15 ICD primary
          + (filter_pass_rate × 3)                                       ← NEW v15 ICD
          + (corpus_unique_investigative_niches / 5 × 4)                 ← NEW v15 ICD (normalized; cap at 5 niches)
          + (epoch_passes_diversification × 2)                           ← NEW v15 ICD binary
          − (mean_primary_candidate_cluster_proximity_max × 3)           ← NEW v15 ICD penalty
```

Where:
- `(1 − cluster_proximity_to_prior_investigative_mean) × 5`: rewards LOW mean proximity (25 candidates are FAR from prior cluster). HIGHEST v15 term; central thesis.
- `filter_pass_rate × 3`: rewards heavy-tail's k-means already producing many distant candidates (v15 has less work to do).
- `corpus_unique_investigative_niches / 5 × 4`: rewards multi-cluster INVESTIGATIVE coverage corpus-wide. Capped at 5 niches (normalize to [0, 1]).
- `epoch_passes_diversification × 2`: binary bonus when ALL new INVESTIGATIVE in epoch pass max_proximity < 0.40 threshold.
- `−(mean_primary_candidate_cluster_proximity_max × 3)`: PENALTY for the chosen primary being close to prior cluster. Pushes the SELECTION to bias toward distant candidates even more.

v15 adds NO new substantive-PASS gate. The 10-signal PASS criterion is preserved.

**confirmed_substantive_pass under v15** (UNCHANGED from v14): step 05.5 PASS, step 10 PASS, tree_stream PASS, q_rubric=NOVEL, gap_real=true, no adversarial hit, step 13 pre_check=true, step 13.5 post_attack=true.

---

## 6. Loop control (v15)

```
# v15 initialization (one-time before E34)
if not exists logs/investigative_cluster_state.json:
    bootstrap from 7 corpus INVESTIGATIVE candidates (R756, R770, R777, R787, R805, R814, R823)
    compute deterministic BoW embedding for each
    write logs/investigative_cluster_state.json

# Epoch start (UNCHANGED from v14 + NEW v15 cluster-state init)
read logs/policy_state.json
update policy aggregates from prior epoch
inject E{N-1}.undersaturated_slots into E{N} step 05 generator prompt  (v14 CPM)
read logs/architecture_tools.json  (v14 ATU)
read logs/investigative_cluster_state.json  (v15 ICD)
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute (UNCHANGED)
    execute step 04.5 (v10 policy-augmented)

    # Step 05 ENHANCED (v14 HTS + ATU): generate 100 candidates with slot assignment + ICD-aware bias
    generate_100_candidates(prompt_with_slot_universe, undersaturated_slot_bias, anti_cluster_bias=prior_investigative_text_summary)
    write 05_candidates_100.json
    write 05_prompt_tokens.json / 05_sample_tokens.json / 05_task_tokens.json

    # Step 05.4 ★ FROZEN (v14): k-means diversity selection of 25
    compute_embeddings(100 candidates)
    cluster_assign = kmeans(embeddings, k=25, seed=epoch)
    selected_25 = candidates near each cluster center
    write 05_4_diversity_filter.json

    # Step 05.45 NEW (v15 ICD): anti-cluster diversity penalty
    read logs/investigative_cluster_state.json (with prior INVESTIGATIVE rounds + cached embeddings)
    for c in selected_25:
        c.embedding = embed(c.specific_mechanism + " " + c.llm_application + ...)
        c.cluster_proximity_max = max(cosine(c.embedding, prior.embedding) for prior in corpus_investigative)
        c.cluster_distance_rank = rank in 25 by ascending proximity
    filtered_25 = [c for c in selected_25 if c.cluster_proximity_max < 0.60]
    write 05_45_anti_cluster_score.json with full schema

    # Primary candidate selection (v15 ICD-aware)
    if len(filtered_25) > 0:
        for c in filtered_25 (sorted by cluster_distance_rank ASC):
            run step 05.5 mechanical classifier
            if architectural_topology_change_TRUE:
                PRIMARY = c
                primary_selection_path = "filtered_first_to_pass_05_5"
                break
        else:
            # 0 of filtered passed step 05.5
            PRIMARY = filtered_25[0]  # most distant
            run step 05.5 regeneration per v12 protocol
            primary_selection_path = "filtered_regenerate"
    else:
        # 0 of 25 passed cluster proximity filter
        PRIMARY = v14_fallback_highest_slot_novelty(selected_25)
        primary_selection_path = "fallback_v14_rule"
        run step 05.5 regeneration per v12 protocol if needed

    write 05_candidate.json (PRIMARY, with v15 fields cluster_proximity_to_prior_investigative + cluster_distance_rank)
    write 05_5_pattern_filter.json (UNCHANGED schema)

    execute step 06 (★ FROZEN) on PRIMARY
    execute step 06.5 / 06.7 (★ FROZEN)
    execute step 07 (★ FROZEN)
    execute step 08 (v9 inverse-search) (UNCHANGED)
    execute step 09 (v9 gap-position) (UNCHANGED)
    execute step 10 (★ FROZEN)
    execute step 11 (v8 Q-rubric) (UNCHANGED)
    execute step 12 (v8 tree-stream) (★ FROZEN)
    execute step 11.5 (v7 adversarial) (★ FROZEN)
    execute step 13 (v10 spec) (★ FROZEN)
    execute step 13.5 (v11 attack) (★ FROZEN)
    execute step 14 (v13 cross-step coherence) (★ FROZEN)

    if step_14_verdict == INVESTIGATIVE_CANDIDATE:
        # v15 ICD append rule: update cluster state immediately
        compute embedding of PRIMARY
        append to logs/investigative_cluster_state.json.corpus_investigative_rounds
        update last_updated timestamp

    # v15 verdict synthesis (per §7)
    compute v15_verdict per §7
    update memory_db.json round entry with v15 fields including cluster_proximity_to_prior_investigative + cluster_distance_rank + filter_pass_rate

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
        # Step 14.5 ★ FROZEN (v14): coverage profile
        coverage_profile = histogram(25 selected candidates' architecture_tool_slot)
        gini = compute_gini(coverage_profile)
        undersaturated = [s for s in S01..S20 if coverage_profile[s] < median]
        write output/14_5_coverage_profile_E{N}.json
        update logs/policy_state.json.policy_update_for_E{N+1}.coverage_profile_bias

        # v15 ICD post-epoch diagnostic
        compute corpus_unique_investigative_niches at threshold 0.40
        compute intra_corpus_pairwise_cosine stats
        for each new INVESTIGATIVE in epoch: compute max_proximity_to_prior_INVESTIGATIVE
        compute epoch_passes_diversification = all(max_proximity < 0.40)
        write output/15_intra_cluster_diversity_E{N}.json

# Epoch end (UNCHANGED + v15 ICD output)
compute candidate_distribution_drift_score
update logs/policy_state.json with new aggregates + step_14_aggregates + coverage_profile_aggregates + intra_cluster_diversity_aggregates
```

---

## 7. v15 verdict synthesis

```
v15_verdict =
    PASS                          (UNCHANGED — same 10 signals as v14; never observed at N=921)

    PASS_WITH_EMPIRICAL_CAVEAT    (UNCHANGED — v10)

    FAIL_EMPIRICAL_ATTACK         (UNCHANGED — v11)

    REJECTED_R279_PATTERN         (UNCHANGED — v12)

    INVESTIGATIVE_CANDIDATE       (UNCHANGED — v13; step 14 FIRED)

    FAIL_ADVERSARIAL              (UNCHANGED)
    FAIL_GAP_REAL_LOGGED          (UNCHANGED)
    FAIL                          otherwise
```

v15 adds NO new verdict label. The PASS criterion remains 10 signals (same as v14). v15's contribution is at the GENERATION-DIVERSITY layer — pre-verdict.

---

## 8. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7+v8+v9+v10+v11+v12+v13+v14)

### 8.1 Step 06 web_search — UNCHANGED
### 8.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
### 8.3 Step 10 mechanical verdict — UNCHANGED
### 8.4 Step 11.5 adversarial external — UNCHANGED
### 8.5 Step 12 tree-stream — UNCHANGED (★ FROZEN)
### 8.6 v8 components (step 05 token-stream FORMAT, step 11 Q-rubric) — UNCHANGED
### 8.7 v9 components — UNCHANGED
### 8.8 v10 step 13 spec format — UNCHANGED (★ FROZEN)
### 8.9 v11 step 13.5 attack format — UNCHANGED (★ FROZEN)
### 8.10 v12 step 05.5 anti-R279 filter — UNCHANGED (★ FROZEN)
### 8.11 v13 step 14 cross-step coherence detector — UNCHANGED (★ FROZEN)
### 8.12 v14 step 05.4 k-means diversity filter — UNCHANGED (★ FROZEN per v15 task)
### 8.13 v14 step 14.5 coverage profile + Gini — UNCHANGED (★ FROZEN per v15 task)
### 8.14 v14 logs/architecture_tools.json 20-slot universe — UNCHANGED (★ FROZEN)
### 8.15 v10/v11/v12/v13/v14 policy state schema — UNCHANGED (additive intra_cluster_diversity_aggregates field group only)

v15 is purely ADDITIVE: step 05.45 NEW (between v14 step 05.4 and v12 step 05.5) + logs/investigative_cluster_state.json NEW + output/15_intra_cluster_diversity_E{N}.json NEW + additive fields on 05_candidate.json + additive fields on stats_round_NNN.json.

---

## 9. Stats schema additions in v15

`output/stats_round_NNN.json` adds these v15-specific fields on top of v14:

```json
{
  ... (all v1-v14 fields) ...,
  "v15_ICD_metrics": {
    "step_05_45_fired_count": 25,
    "cluster_proximity_threshold": 0.60,
    "prior_investigative_count_at_epoch_start": 7,
    "new_investigative_in_epoch_count": 0,
    "corpus_investigative_count_at_epoch_end": 7,
    "cluster_proximity_to_prior_investigative_mean_per_round_mean": 0.0,
    "cluster_proximity_to_prior_investigative_mean_per_round_min": 0.0,
    "cluster_proximity_to_prior_investigative_mean_per_round_max": 0.0,
    "filter_pass_rate_per_round_mean": 0.0,
    "filter_pass_rate_per_round_min": 0.0,
    "filter_pass_rate_per_round_max": 0.0,
    "primary_candidate_cluster_distance_rank_per_round_mean": 0.0,
    "primary_selection_path_distribution": {"filtered_first_to_pass_05_5": 0, "filtered_regenerate": 0, "fallback_v14_rule": 0},
    "corpus_unique_investigative_niches_at_threshold_0_40": 1,
    "intra_corpus_pairwise_cosine_mean_at_epoch_end": 0.589,
    "epoch_new_investigative_max_proximity_to_prior_per_round": [],
    "epoch_passes_diversification": false,
    "real_step_05_45_Agent_spawns": 0,
    "main_context_direct_step_05_45_count": 25,
    "real_step_15_diagnostic_Agent_spawns": 0,
    "main_context_direct_step_15_diagnostic_count": 1
  },
  "v15_verdict_distribution": {
    "v15_PASS_count": 0,
    "v15_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v15_FAIL_count": 0,
    "v15_FAIL_ADVERSARIAL_count": 0,
    "v15_FAIL_GAP_REAL_LOGGED_count": 0,
    "v15_FAIL_EMPIRICAL_ATTACK_count": 0,
    "v15_REJECTED_R279_PATTERN_count": 0,
    "v15_INVESTIGATIVE_CANDIDATE_count": 0
  }
}
```

---

## 10. Anti-cheating commitments (v15 additions on top of v14)

The v3...v14 instructions stand. v15 adds:

- **Cluster state honesty.** `logs/investigative_cluster_state.json` is APPEND-ONLY. Entries are never deleted or edited; new INVESTIGATIVE rounds are added at end-of-round. The cached embeddings are computed ONCE per round and never regenerated (deterministic from text).
- **Embedding consistency.** The step 05.45 embedding method (D=256 deterministic BoW md5 signed L2) MUST match v14's step 05.4 method exactly. Switching embedding methods mid-corpus would invalidate cached embeddings and break cluster-distance comparisons.
- **Filter threshold honesty.** CLUSTER_PROXIMITY_THRESHOLD = 0.60 is FROZEN for E34. v15 does not retroactively adjust the threshold. If E34 produces filter_pass_rate ≈ 0 (all 25 are in the cluster) or ≈ 1 (none in cluster), v16 may calibrate the threshold — but only in v16, not mid-E34.
- **Primary selection determinism.** Given the 25 candidates, the cluster state, and the threshold, the primary candidate selection is DETERMINISTIC. Multiple-run reproducibility is required.
- **Diversification test rigor.** epoch_passes_diversification is a STRICT criterion: ALL new INVESTIGATIVE in epoch must have max_proximity < 0.40. If even ONE new INVESTIGATIVE has max_proximity ≥ 0.40, the test FAILS. The criterion is not soft-averaged.
- **No mid-corpus embedding migration.** v15 freezes the BoW md5 embedding. If a future v16 wants a different embedding (e.g., sentence-transformers), the cluster state must be REBUILT from scratch AND the threshold must be RECALIBRATED.
- **Cross-investigative ablation diagnostic is part of v15 (subsuming option c).** The `output/15_intra_cluster_diversity_E{N}.json` file IS the structural-duplicate flag report. We do NOT need a separate option-c step.

---

## 11. Inherited history (v1 → ... → v15)

- **v1**: file-chain + mechanical keyword rule + cross-agent verification. R001-R025.
- **v2**: Form A/B/C/D rotation. R026-R050.
- **v3**: step 04.5 memory check. R051-R075.
- **v4**: step 06.5 semantic-similarity. R076-R100.
- **v5**: step 06.7 functional-equivalence judge. R101-R575.
- **v6**: step 06.8 per-paper-completeness. R576-R600 (DEPRECATED).
- **v7**: v5 base + step 11.5 adversarial-literature. R601-R650.
- **v8**: v7 base + token streams + Q-rubric + tree-stream. R651-R675.
- **v9**: v8 base + inverse-search + gap-position. R676-R700.
- **v10**: v9 base + step 13 experiment-spec + policy_state.json. R701-R725.
- **v11**: v10 base + step 13.5 adversarial spec attack. R726-R750.
- **v12**: v11 base + step 05.5 anti-R279 filter. R751-R775.
- **v13**: v12 base + step 14 cross-step coherence detector. R776-R800.
- **v14**: v13 base + Heavy-Tail Sampling (HTS) + Architecture Tool Universe (ATU) + Coverage-Profile Metric (CPM). R801-R825.
- **v15** (this file): v14 base + Intra-Cluster Diversification (ICD). **R826-R850 under v15 in E34.**

---

## 12. What v15 does NOT promise

v15 does NOT promise more substantive PASS verdicts. The 921-round saturation result (0 confirmed substantive PASS, p ≈ 0.0000967 on 1%-novelty H₀ at N=921) stands. v15 does NOT touch step 10. v15's contribution is at the GENERATION-DIVERSITY layer.

v15 does NOT promise more INVESTIGATIVE candidates. v14's E33 produced 3 INVESTIGATIVE (corpus 7). v15 may produce 2-4 INVESTIGATIVE in E34 (similar absolute count). What v15 promises is that those new INVESTIGATIVE candidates, if any, will be DISTANT from the existing 7-candidate cluster (max_proximity < 0.40 target).

v15 does NOT promise the cluster will dissolve. If the generator's natural attractor is the "algebraic-structure-equipped learnable module with non-trivial commutator invariant" region, the attack-rebuttal mechanism may be inherent to that region. v15 will surface whether THIS is the case — if even with anti-cluster pressure, the new INVESTIGATIVE candidates STILL fall in the same cluster, then v16+ must address the deeper question of WHY this region is uniquely attack-rebuttable.

What v15 promises:
- The first **anti-cluster diversity penalty** in the corpus.
- The first **corpus-wide INVESTIGATIVE cluster state** (logs/investigative_cluster_state.json).
- The first **per-candidate cluster-proximity score** at generation time (step 05.45).
- The first **cross-investigative structural-duplicate flag** in the corpus (subsuming option c at step 14.5).
- PASS criterion UNCHANGED at 10 signals.
- Symmetric with v12 step 05.5 (R279-pattern filter) — both v12 and v15 filter at generation; v12 filters R279-pattern, v15 filters INVESTIGATIVE-cluster-near.
- A signal at the corpus-level "how many unique attack-rebuttable niches does the corpus have?" (corpus_unique_investigative_niches).

v15 cannot make step 10 say PASS. v15 can ensure the INVESTIGATIVE-labeled candidates diversify across multiple latent regions.

---

## 13. Honest deviation policy (for E34 execution)

Per the v15 task description:
- Real WebSearch in step 06 (mandatory; same as v5-v14).
- Real Agent spawn for step 08 (inverse-search) and step 12 (helper) WHERE FEASIBLE.
- Step 13 spec generation runs in MAIN CONTEXT.
- Step 13.5 adversarial-spec attack runs in MAIN CONTEXT or Agent spawn; ≤3 spawns.
- Step 05.5 mechanical filter runs in MAIN CONTEXT (v12 default).
- Step 14 cross-step coherence detector runs in MAIN CONTEXT (v13 default).
- Step 05 100-candidate generation runs in MAIN CONTEXT (v14 default).
- Step 05.4 diversity filter runs in MAIN CONTEXT (v14 default; deterministic k-means).
- Step 14.5 coverage profile runs in MAIN CONTEXT (v14 default; deterministic histogram).
- **Step 05.45 anti-cluster filter runs in MAIN CONTEXT** (deterministic embedding + cosine; no Agent spawn).
- **Cross-investigative-ablation diagnostic at step 14.5 wrapper runs in MAIN CONTEXT** (deterministic; no Agent spawn).
- Per epoch, ≤5 synthesized Agent spawns across all steps. v15 task target is honest deviation <5 spawns.
- Wall-clock timestamps ≥ 3-min logical gap per round (continued from E29-E33).

No R279 retrofit needed for v15. No mid-epoch threshold calibration.

---

## 14. Phase 4 reporting requirements (for output/epoch34_comparison.md)

After E34 completes, the comparison document must record:
1. step 05.45 per-round metrics: cluster_proximity_to_prior_investigative_mean / min / max, filter_pass_rate, primary_selection_path distribution.
2. v14 unchanged metrics (HTS: max_over_100; ATU: slot assignment; CPM: distinct_slots_hit, Gini).
3. NEW INVESTIGATIVE rounds in E34 (if any): max_proximity_to_prior, argmax_prior_round, is_structural_duplicate flag.
4. epoch_passes_diversification (binary success criterion).
5. corpus_unique_investigative_niches at threshold 0.40 (was 1 at E33 end; v15 target ≥ 2).
6. intra_corpus_pairwise_cosine_mean at epoch end (was 0.589 at E33 end; v15 target < 0.55 if new INVESTIGATIVE are diverse).
7. score_v15 with the 5 new ICD terms.
8. cumulative N_verified after E34 = 946.
9. p(no PASS | 1% H₀) at N=946 ≈ 0.0000756 (per v15 task target).
10. Per-framework attribution (v15 ICD vs v14 HTS/ATU/CPM vs v13 cross-step vs v12 anti-R279 vs v11 attack vs v10 spec vs v8 Q-rubric/tree-stream).
11. Does v15 increase INVESTIGATIVE cluster diversity? (intra_corpus_pairwise_cosine_mean comparison)
12. Does cross-investigative ablation flag duplicates? (per-new-INVESTIGATIVE is_structural_duplicate flag count)
13. Total unique investigative niches (corpus-wide deduped).

The v15 channel's contribution is best seen at the CORPUS-WIDE NICHE-DIVERSITY level, not the per-round PASS-rate level.

---

## 15. v15 predictions (testable at E34)

| Metric | E33 v14 baseline | E34 v15 predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (saturation; step 10 still FROZEN) |
| step 14 FIRED count | 3 | 1-4 (similar order; ICD may or may not change INVESTIGATIVE rate) |
| **cluster_proximity_to_prior_investigative_mean (per round)** | n/a | **0.45-0.60** (the 25 cluster centers naturally have mixed distance to existing cluster) |
| **filter_pass_rate (per round)** | n/a | **0.30-0.70** (mixed; some k-means centers in-cluster, some not) |
| **primary_candidate_cluster_distance_rank (mean over 25 rounds)** | n/a (would be ~13 under v14) | **3-7** (selection biased to most-distant) |
| **mean primary cluster_proximity_max (across 25 rounds)** | n/a (would be ~0.55 under v14) | **0.30-0.50** (primaries are distant) |
| **new INVESTIGATIVE max_proximity_to_prior (per new INVESTIGATIVE)** | n/a | **0.25-0.55** target (< 0.40 for diversification pass) |
| **corpus_unique_investigative_niches at threshold 0.40** | 1 | **1-3** (depends on new INVESTIGATIVE diversity) |
| **intra_corpus_pairwise_cosine_mean (corpus end of E34)** | 0.589 | **0.50-0.58** (diluted if new INVESTIGATIVE are distant) |
| **epoch_passes_diversification (binary)** | n/a | **40-60% chance of TRUE** (depends on generator + ICD interaction) |
| score_v15 | n/a (v14 score = 55.96) | **+3-8 over v14 (~58-63)** |

E34 will be the FIRST EPOCH where the corpus has explicit anti-INVESTIGATIVE-cluster generation pressure. The test: does v15 produce INVESTIGATIVE candidates outside the existing cluster, or does the generator collapse back to the same attractor under the new pressure?

Outcomes:
- **If new INVESTIGATIVE max_proximity < 0.40 (all new):** v15 ICD validated; corpus_unique_niches grows; v16+ can build on multi-cluster coverage.
- **If new INVESTIGATIVE max_proximity ≥ 0.50 (all new):** v15 ICD fails to escape the cluster; the algebraic-structure region is an inherent attractor — v16 needs structural changes (e.g., different attack categories at step 13.5, or different rebuttal templates).
- **If 0 new INVESTIGATIVE in E34:** v15's anti-cluster pressure may have over-restricted (filtering out too many architectural candidates). v16 may need a softer threshold or a per-category cluster (separate Lie-groups cluster state from quiver state).
