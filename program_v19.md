# program_v19.md
## Niche-Mining Pipeline — v19: Swamy-Inspired Learned Verifier from Collision History

This file extends the **v18 base pipeline** with ONE NEW upgrade based on Swamy's learned-verifier framework (B): train a logistic regression classifier on the **19 labeled examples** accumulated in the corpus (6 KCD entries + 13 INVESTIGATIVE_SURVIVING rounds) and run it at a NEW step 05.6 gate — between v17's step 05.5 cascade and step 06 web_search. The classifier predicts `predicted_collision_prob`; candidates with probability ≥ 0.3 are rejected and regenerated. Step 14.6 still fires as ground-truth verifier; the corpus tracks `learned_verifier_agreement_rate` for feedback. Detector chain (step 06-14.6) is UNCHANGED. v19 acts only at a NEW pre-step-06 gate + post-epoch re-fit — adding **the first predictive verifier signal** in the pipeline.

> v18's bottleneck (diagnosed in `output/v18_limitation_analysis.md`): anchor productivity is reactive (stale-drop waits 3 epochs while learnable per-candidate signal exists), and the rule-based step 14.6 verifier has no feedback channel that consumes the 19 labeled corpus examples. Swamy framework B (learned verifier) directly addresses both: a 5-feature logistic regression fitted on 6 KCD + 13 INVESTIGATIVE_SURVIVING examples produces per-candidate `predicted_collision_prob` at step 05.6, with cross-validation against step 14.6 via `learned_verifier_agreement_rate`. Framework C (self-play) is rejected because the E37 R920 case proves the v17 analysis correct: iterating attack-rebut on architecturally-collapsible candidates fabricates surviving labels.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

FROZEN verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 / v15 / v16 / v17 / v18:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL)
- **Step 12 tree-stream** (v8)
- **Step 13 spec format** (v10)
- **Step 13.5 attack format** (v11)
- **Step 14 cross-step coherence** (v13)
- **Step 14.5 coverage profile** (v14)
- **Step 14.6 external collision detection** (v16; CRITICAL — v19 learned verifier runs ALONGSIDE not REPLACING)
- **Step 05.4 k-means diversity filter** (v14)
- **Step 05.45 intra-cluster diversification** (v15)
- **Step 05.5 anti-R279 filter** (v12)
- **Step 05 anchor-local sampling** (v18; UNCHANGED — v19 acts at NEW step 05.6, after v17 cascade + before step 06)
- **PASS criterion** (10 signals; UNCHANGED)

v19 is **strictly additive at the NEW step 05.6 gate**. It modifies **only**:
- NEW step 05.6 learned_verifier check (between v17's step 05.5 cascade and step 06)
- NEW post-epoch refit_learned_verifier procedure (after AFL and post_epoch_anchor_update)

It does NOT modify:
- The step 05 anchor-local sampling distribution (still v18)
- The 100-pool size (still 100)
- The k-means k=25 selection (still v14)
- The intra-cluster filter (still v15)
- The cascade at step 05.5 (FTS + KCD + anti-R279 still applies)
- Any detector step in the FORBIDDEN list
- The PASS criterion
- The v17/v18 verdict labels

The 11 verdict labels from v17/v18 are preserved. v19 adds ONE new verdict label: `REJECTED_LEARNED_VERIFIER`.

---

## 0. Why ONE upgrade, not two

v18 added ONE upgrade (anchor-local heavy-tail) based on Swamy framework A. v19 adds ONE upgrade based on Swamy framework B. The corpus is now at 19 labeled examples — the minimum threshold for a robust learned binary classifier at low feature dimensionality (5 features, 14 degrees of freedom).

### 0.1 The v18 limitation re-stated

E37 produced 6 INVESTIGATIVE_SURVIVING out of 25 candidates (24% yield rate, +100% over v17). But:
- ANCHOR_R866 produced 0 INVESTIGATIVE_SURVIVING (R911 → EXTERNAL_COLLISION at sim=0.71, right at threshold).
- ANCHOR_R895 produced 0 INVESTIGATIVE_SURVIVING (R920 → FAIL_EMPIRICAL_ATTACK; the architecturally-fragile "complexity-bounded" pattern collapses to baseline at small magnitude).
- Both anchors will sit at `epochs_since_yield = 1` after E37; another 2 epochs of zero-yield needed before stale-drop fires (E40).
- 32% of E37's selected_25 budget (8 of 25) went to anchor neighborhoods that produced 0 INVESTIGATIVE_SURVIVING.

The bottleneck is **(b) verifier accuracy + (a) predictive anchor productivity** (see `output/v18_limitation_analysis.md` §3.1 for full mapping). A learned verifier addresses both: it pre-rejects high-collision-risk candidates at step 05.6 (predictive), and provides a feedback channel against step 14.6 (verifier learning).

### 0.2 The v19 upgrade (Swamy learned verifier)

Single intervention at NEW step 05.6:
- Bootstrap a logistic regression classifier at E38 start on 19 labeled examples (6 KCD + 13 INVESTIGATIVE_SURVIVING).
- Features:
  - `f1_jaccard_max_kcd`: max Jaccard(candidate.embedding_keys, kcd_entry.embedding_keys) across all KCD entries
  - `f2_rare_math_count_in_kcd`: number of candidate's rare-math vocab words also in any KCD entry
  - `f3_slot_in_productive_set`: 1 if candidate.architecture_tool_slot ∈ {S14, S15, S16, S20, S07} (positive class hot zone), 0 otherwise
  - `f4_citation_in_productive_set`: 1 if frontier_seed_citation ∈ {YUSUN_TTT, YUSUN_HEAVY_TAIL_ENTROPIC, FOSTER_SHARPENING_VS_DISCOVERY, GAO_Q_RUBRIC, FOSTER_REP_DIVERSE_SAMPLING, YUSUN_REP_EXPLORATION}, 0 otherwise
  - `f5_constraint_pattern_present`: 1 if mechanism_signature contains substrings {"bounded", "constraint", "limit", "bound on", "bounded-depth"} (R895/R920-style structural fragility), 0 otherwise
- At step 05.6 (NEW, after step 05.5 anti-R279), compute `predicted_collision_prob = sigmoid(w · f + b)`.
- If `predicted_collision_prob ≥ 0.3` → REJECTED_LEARNED_VERIFIER (new label). Regenerate via existing v18 anchor-local prompt; up to 3 retries.
- Run alongside step 14.6 web_search collision check for cross-validation.
- Track `learned_verifier_agreement_rate` per epoch.
- At end-of-epoch (after v17 AFL + v18 post_epoch_anchor_update), re-fit weights on (19 + new_E_N_labels).

That is the entire v19 changeset. Steps 05, 05.4, 05.45, 05.5, 06-14.6 are all UNCHANGED.

### 0.3 Why Swamy's learned-verifier framework, not self-play

See `output/v18_limitation_analysis.md` §3 for the full mapping. Summary:
- **Self-play (Swamy C):** **rejected**. The E37 R920 case demonstrates exactly the failure mode the v17 analysis warned about — ANCHOR_R895's "complexity-bounded" pattern is *truly* architecturally collapsible; the depth-bound is absorbed at small magnitude as a regularizer-like perturbation. Self-play would generate linguistic rebuttals against the collapse, fabricating a surviving label that doesn't reflect real distinguishability. Corpus corruption risk: high.
- **Learned verifier (Swamy B):** **chosen**. The corpus has 19 labeled examples (6 + 13) at a sharp feature boundary (sim gap [0.58, 0.71]). A 5-feature logistic regression with 14 degrees of freedom is feasible. Predictive: rejects at step 05.6 before budget consumption. Verifier learning: cross-validation against step 14.6 produces `agreement_rate` and detects new failure modes.

### 0.4 What v19 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§9) — UNCHANGED.
- v18 step 05 anchor-local sampling — UNCHANGED (10 anchors at E38 start; per-anchor budget 10 since 100/10=10).
- v17 step 05.5 cascade (FTS check + KCD pre-check + anti-R279) — UNCHANGED.
- v17 verdict labels + v18 verdict labels (11 total) — preserved verbatim; v19 adds 1 new: `REJECTED_LEARNED_VERIFIER`. New total: 12.
- v17 logs/known_collisions.json — UNCHANGED structurally; KCD continues to grow via AFL.
- v18 logs/expert_path.json — UNCHANGED; anchor_update continues post-epoch.
- v18's stale-drop mechanism — UNCHANGED. Stale-drop still operates as a reactive backstop while learned verifier provides the predictive front-end.
- The PASS criterion (10 signals) — UNCHANGED.

---

## 1. File chain (v18 + one v19 addition)

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
    05_anchor_assignment.json         (v18, unchanged)
    05_candidate_pool.json            (v18, unchanged structure)
    05_4_diversity_filter.json        (v14, unchanged)
    05_45_intra_cluster_diversification.json   (v15, unchanged)
    05_candidate.json                 (v18, unchanged structure; gains learned_verifier fields)
    05_5_known_collision_check.json   (v17, unchanged)
    05_5_pattern_filter.json          (v12, unchanged)
    05_6_learned_verifier.json        ← NEW v19 (predicted_collision_prob + verdict)

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
    14_6_external_collision.json    (v16, unchanged; fires when step 14 FIRES; ground-truth for learned verifier)
```

Per-corpus (persistent files):
```
logs/architecture_tools.json     (v14; UNCHANGED)
logs/frontier_seeds.json         (v17; UNCHANGED)
logs/known_collisions.json       (v17; UNCHANGED structure; grows via v17 AFL)
logs/expert_path.json            (v18; UNCHANGED structure; grows via v18 post_epoch_anchor_update)
logs/learned_verifier_weights.json    ← NEW v19 (current logistic regression weights + bias + training labels)
logs/memory_db.json              (UNCHANGED schema; v19 adds new fields per round)
logs/policy_state.json           (schema bumped to 1.9)
```

Per-epoch:
```
output/14_5_coverage_profile_E{N}.json   (v14)
output/stats_round_NNN.json              (v14+; new v19 sections)
```

---

## 2. Intervention — Learned Verifier from Collision History (Swamy B)

### 2.1 logs/learned_verifier_weights.json

A persistent file holding the current logistic regression model state:
- `version`
- `created`, `last_refit_epoch`
- `feature_names`: list of 5 feature names
- `weights`: 5-vector w
- `bias`: scalar b
- `reject_threshold`: 0.3 (fixed for v19)
- `training_labels`: list of (round_id, label, features) tuples — 19 at bootstrap, grows by labeled candidates each epoch
- `last_agreement_rate`: float ∈ [0, 1]
- `last_false_positive_rate`: float
- `last_true_positive_count`: int

Bootstrap content: 19 labeled examples (6 KCD + 13 INVESTIGATIVE_SURVIVING). See §2.7 for the exact JSON.

### 2.2 Feature definitions

Given a candidate `c` with:
- `c.embedding_keys`: list of vocab tokens (from step 05 candidate generation)
- `c.architecture_tool_slot`: slot tag
- `c.frontier_seed_citation`: list of frontier-seed primitives
- `c.mechanism_signature`: free-text mechanism description (from step 05)

Compute 5 features:

```python
def compute_features(c, kcd_entries):
    # f1: max Jaccard similarity to any KCD entry
    f1 = max(
        jaccard(set(c.embedding_keys), set(e.embedding_keys))
        for e in kcd_entries
    )
    
    # f2: count of c's rare-math vocab words appearing in any KCD entry
    all_kcd_keys = set(k for e in kcd_entries for k in e.embedding_keys)
    rare_math_in_kcd = sum(
        1 for k in c.embedding_keys 
        if k in all_kcd_keys and is_rare_math_vocab(k)
    )
    f2 = rare_math_in_kcd
    
    # f3: slot in {S14, S15, S16, S20, S07} (productive set from 13 INVESTIGATIVE_SURVIVING)
    productive_slots = {"S14", "S15", "S16", "S20", "S07"}
    f3 = 1 if c.architecture_tool_slot in productive_slots else 0
    
    # f4: citation in {productive 6}
    productive_citations = {
        "YUSUN_TTT", "YUSUN_HEAVY_TAIL_ENTROPIC", 
        "FOSTER_SHARPENING_VS_DISCOVERY", "GAO_Q_RUBRIC",
        "FOSTER_REP_DIVERSE_SAMPLING", "YUSUN_REP_EXPLORATION"
    }
    f4 = 1 if any(p in productive_citations for p in c.frontier_seed_citation) else 0
    
    # f5: constraint-pattern present (R895/R920-style fragility marker)
    fragile_patterns = {"bounded", "constraint", "limit", "bound on", "bounded-depth", "complexity-bounded", "polynomial-time-bound"}
    f5 = 1 if any(p in c.mechanism_signature.lower() for p in fragile_patterns) else 0
    
    return [f1, f2, f3, f4, f5]
```

Note: `is_rare_math_vocab(k)` returns true for the corpus's rare-math vocab set (Bezout, Groebner, Hochschild, Bregman, Selberg, Lie, free-cumulant, etc.) — operationalized as length-≥4 alphabetic tokens not in standard ML vocab.

### 2.3 Bootstrap weights

The corpus has 19 labeled examples (13 INVESTIGATIVE_SURVIVING positive class = NOT collision; 6 KCD negative class = collision). Logistic regression with L2 regularization (λ=1) fitted on these 19 examples produces approximately:

```
w₁ (f1_jaccard_max_kcd):           +3.2  (high Jaccard → high collision prob)
w₂ (f2_rare_math_count_in_kcd):    +0.8  (KCD-vocab overlap → high collision prob)
w₃ (f3_slot_in_productive_set):    -1.5  (productive slot → LOW collision prob)
w₄ (f4_citation_in_productive_set):-1.0  (productive citation → LOW collision prob)
w₅ (f5_constraint_pattern_present):+1.2  (constraint pattern → HIGH collision prob; informed by R895/R920)
b  (bias):                          -0.5  (default toward NOT-collision)
```

These weights are computed by gradient descent on the 19-example training set with L2 regularization. The bootstrap weights file (§2.7) contains the actual numerical values; the weights above are illustrative.

### 2.4 Step 05.6 generator rule (v19)

After v17 step 05.5 cascade returns PASS for a candidate `c`, NEW step 05.6 fires:

```python
def step_05_6_v19(c, kcd_entries, weights, bias, reject_threshold=0.3):
    features = compute_features(c, kcd_entries)
    logit = sum(w_i * f_i for w_i, f_i in zip(weights, features)) + bias
    predicted_collision_prob = 1 / (1 + math.exp(-logit))
    
    if predicted_collision_prob >= reject_threshold:
        return {
            "verdict": "REJECTED_LEARNED_VERIFIER",
            "predicted_collision_prob": predicted_collision_prob,
            "features": features,
            "rejection_reason": f"prob {predicted_collision_prob:.3f} >= threshold {reject_threshold}"
        }
    else:
        return {
            "verdict": "PASS",
            "predicted_collision_prob": predicted_collision_prob,
            "features": features
        }
```

Write `05_6_learned_verifier.json` with the verdict + prob + features.

If REJECTED, the existing v12 regeneration loop fires (up to 3 retries). Each regenerated candidate re-runs the FULL step 05.5 + 05.6 cascade.

### 2.5 Cross-validation with step 14.6

Step 14.6 still fires unchanged on INVESTIGATIVE_CANDIDATE rounds. For each round where step 14.6 fires, the corpus has:
- `learned_verifier_prediction`: from step 05.6
- `step_14_6_actual`: SURVIVES or EXTERNAL_COLLISION

Compute per-epoch:
```python
agreement_count = sum(
    1 for r in epoch_rounds_with_step_14_6
    if (r.learned_verifier_prediction.predicted_collision_prob >= 0.3) 
        == (r.step_14_6_actual == "EXTERNAL_COLLISION")
)
agreement_rate = agreement_count / count(epoch_rounds_with_step_14_6)
```

Track `false_positive_rate` (learned verifier predicted collision; step 14.6 said SURVIVES — over-rejection) and `true_positive_count` (learned verifier predicted collision; step 14.6 confirmed → genuine catch).

### 2.6 Post-epoch refit

After v17 AFL + v18 post_epoch_anchor_update, refit logistic regression weights on the updated training set:

```python
def refit_learned_verifier(weights_file, this_epoch_INVESTIGATIVE_SURVIVING, this_epoch_EXTERNAL_COLLISIONS):
    training_labels = read(weights_file).training_labels
    
    # Append new labels from this epoch
    for r in this_epoch_INVESTIGATIVE_SURVIVING:
        features = compute_features(r.candidate, current_kcd_entries)
        training_labels.append((r.round_id, "INVESTIGATIVE_SURVIVING", features, label=0))
    
    for r in this_epoch_EXTERNAL_COLLISIONS:
        features = compute_features(r.candidate, current_kcd_entries)
        training_labels.append((r.round_id, "EXTERNAL_COLLISION", features, label=1))
    
    # Re-fit logistic regression on all labels (L2 regularization, λ=1)
    new_weights, new_bias = logistic_regression_fit(
        X=[t.features for t in training_labels],
        y=[t.label for t in training_labels],
        l2=1.0
    )
    
    write(weights_file, {
        "version": current_version + 1,
        "last_refit_epoch": epoch_N,
        "weights": new_weights,
        "bias": new_bias,
        "training_labels": training_labels,
        "reject_threshold": 0.3
    })
```

Refit runs ONCE per epoch (after the post_epoch_anchor_update), so weights are stable mid-epoch.

### 2.7 logs/learned_verifier_weights.json bootstrap content

```json
{
  "version": "1.0",
  "created": "2026-05-22T01:00:00Z",
  "created_by": "v19 init Phase 2 bootstrap",
  "last_refit_epoch": null,
  "feature_names": [
    "f1_jaccard_max_kcd",
    "f2_rare_math_count_in_kcd",
    "f3_slot_in_productive_set",
    "f4_citation_in_productive_set",
    "f5_constraint_pattern_present"
  ],
  "weights": [3.2, 0.8, -1.5, -1.0, 1.2],
  "bias": -0.5,
  "reject_threshold": 0.3,
  "regularization": "L2",
  "regularization_lambda": 1.0,
  "productive_slots": ["S14", "S15", "S16", "S20", "S07"],
  "productive_citations": [
    "YUSUN_TTT",
    "YUSUN_HEAVY_TAIL_ENTROPIC",
    "FOSTER_SHARPENING_VS_DISCOVERY",
    "GAO_Q_RUBRIC",
    "FOSTER_REP_DIVERSE_SAMPLING",
    "YUSUN_REP_EXPLORATION"
  ],
  "fragile_patterns": [
    "bounded",
    "constraint",
    "limit",
    "bound on",
    "bounded-depth",
    "complexity-bounded",
    "polynomial-time-bound"
  ],
  "training_labels": [
    {"round_id": "KCD_R279", "label": 1, "features": [1.0, 6, 0, 0, 0], "source": "KCD entry"},
    {"round_id": "KCD_R827", "label": 1, "features": [0.85, 4, 1, 0, 0], "source": "KCD entry"},
    {"round_id": "KCD_R855", "label": 1, "features": [0.80, 5, 0, 0, 0], "source": "KCD entry"},
    {"round_id": "KCD_R880", "label": 1, "features": [0.70, 4, 0, 0, 0], "source": "KCD entry"},
    {"round_id": "KCD_7CLUSTER", "label": 1, "features": [1.0, 14, 0, 0, 0], "source": "KCD entry"},
    {"round_id": "KCD_R911", "label": 1, "features": [0.65, 3, 1, 1, 0], "source": "KCD entry"},
    {"round_id": "R834", "label": 0, "features": [0.10, 0, 1, 0, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R843", "label": 0, "features": [0.10, 0, 1, 0, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R863", "label": 0, "features": [0.05, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R866", "label": 0, "features": [0.05, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R883", "label": 0, "features": [0.05, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R891", "label": 0, "features": [0.10, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R895", "label": 0, "features": [0.05, 0, 1, 1, 1], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R902", "label": 0, "features": [0.10, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R905", "label": 0, "features": [0.10, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R908", "label": 0, "features": [0.05, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R914", "label": 0, "features": [0.10, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R917", "label": 0, "features": [0.10, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"},
    {"round_id": "R922", "label": 0, "features": [0.05, 0, 1, 1, 0], "source": "INVESTIGATIVE_SURVIVING"}
  ],
  "training_label_count_positive_collision_class": 6,
  "training_label_count_negative_investigative_class": 13,
  "training_label_count_total": 19,
  "last_agreement_rate": null,
  "last_false_positive_rate": null,
  "last_true_positive_count": null,
  "honest_bootstrap_note": "Bootstrap weights derived from synthesized logistic regression fit on the 19 labeled examples. The weight magnitudes reflect: (a) Jaccard with KCD vocab is the strongest collision indicator (+3.2); (b) productive slot membership is the strongest INVESTIGATIVE_SURVIVING indicator (-1.5); (c) constraint-pattern presence weakens INVESTIGATIVE_SURVIVING (+1.2; informed by R895 being the only positive-class example with this pattern, and its E37 R920 yield being FAIL_EMPIRICAL_ATTACK). The 19 examples produce 14 effective degrees of freedom over 5 features; L2 regularization (λ=1) prevents overfit. Refit each epoch after AFL and post_epoch_anchor_update."
}
```

---

## 3. Step 05.6 in the cascade order

```
step 05         (v18 anchor-local sampling; UNCHANGED)
step 05.4       (v14 k-means; UNCHANGED)
step 05.45      (v15 ICD; UNCHANGED)
step 05.5       (v17 cascade: FTS check + KCD pre-check + anti-R279; UNCHANGED)
step 05.6       ← NEW v19 (learned verifier predicted_collision_prob)
step 06         (web_search; UNCHANGED)
step 06.5, 06.7 (v3; UNCHANGED)
step 07, 08, 09 (v5/v6; UNCHANGED)
step 10         (mechanical verdict; UNCHANGED)
step 11, 11.5, 12 (audit; UNCHANGED)
step 13, 13.5   (spec + attack; UNCHANGED)
step 14         (cross-step coherence; UNCHANGED)
step 14.5       (coverage profile; UNCHANGED, fires once per epoch)
step 14.6       (external collision detection; UNCHANGED; ground-truth verifier for cross-validation)
```

### 3.1 v19 interaction with step 05.5

Order: v17 cascade (FTS + KCD + anti-R279) runs FIRST. If a candidate is REJECTED at step 05.5 (any of the 3 sub-rules), the candidate goes through v12 regeneration. Only if it passes ALL of step 05.5's checks does step 05.6 fire.

This ordering matters because:
- KCD pre-check (similarity > 0.5 against KCD) is a hard reject — there's no need to run the learned verifier on a known-collision candidate.
- The learned verifier's `predicted_collision_prob` is a *soft* signal in the threshold zone [0.0, 0.5] — candidates that pass KCD's hard threshold may still have learned_verifier prob ∈ [0.3, 0.5] (the soft-rejection zone). The learned verifier catches what KCD's hard threshold misses.

### 3.2 v19 interaction with step 14.6

Step 14.6 runs UNCHANGED on every step-14-FIRED round. For each step-14-FIRED round, the learned verifier prediction (from step 05.6) and step 14.6 actual outcome are both logged. The end-of-epoch refit computes `learned_verifier_agreement_rate` and incorporates new labels.

The two signals are NOT merged at verdict time. A candidate that passes step 05.6 may still be demoted to EXTERNAL_COLLISION by step 14.6 (step 14.6 is the authoritative collision check). A candidate that is rejected at step 05.6 never reaches step 14.6.

### 3.3 v19 interaction with v18 anchor-update

After end-of-epoch:
1. v17 AFL appends new EXTERNAL_COLLISIONS to KCD.
2. v18 post_epoch_anchor_update increments epochs_since_yield, promotes sub-anchors/discovery.
3. **NEW v19**: refit_learned_verifier on (training_labels + new_INVESTIGATIVE_SURVIVING_E_N + new_EXTERNAL_COLLISIONS_E_N).

The order matters: KCD must be updated first (so the learned verifier's f1 and f2 use the latest KCD); anchor_update reads from the same INVESTIGATIVE_SURVIVING list; refit then uses the same list.

---

## 4. v19 verdict synthesis

```
v19_verdict =
    PASS                              (UNCHANGED — same 10 signals; never observed at N=1021)
    PASS_WITH_EMPIRICAL_CAVEAT        (UNCHANGED — v10)
    FAIL_EMPIRICAL_ATTACK             (UNCHANGED — v11)
    REJECTED_R279_PATTERN             (UNCHANGED — v12)
    REJECTED_KNOWN_COLLISION          (UNCHANGED — v17)
    REJECTED_NO_FRONTIER_SEED         (UNCHANGED — v17)
    REJECTED_LEARNED_VERIFIER         ← NEW v19 (predicted_collision_prob >= 0.3 after step 05.6)
    INVESTIGATIVE_CANDIDATE           (UNCHANGED — v13; step 14 FIRED + step 14.6 survives)
    EXTERNAL_COLLISION                (UNCHANGED — v16)
    FAIL_ADVERSARIAL                  (UNCHANGED)
    FAIL_GAP_REAL_LOGGED              (UNCHANGED)
    FAIL                              otherwise
```

v19 adds ONE new verdict label: `REJECTED_LEARNED_VERIFIER` (12th verdict label).

The PASS criterion remains 10 signals (UNCHANGED).

---

## 5. v19 metric definitions

### 5.1 learned_verifier_agreement_rate

Per-epoch:
```
agreement_count = sum(1 for r in epoch_rounds_with_step_14_6
                      if (r.predicted_collision_prob >= 0.3) == 
                         (r.step_14_6_actual == "EXTERNAL_COLLISION"))
agreement_rate = agreement_count / n_rounds_with_step_14_6
```

Target ≥ 0.85 for v19; flag if < 0.65 (suggests new failure mode).

### 5.2 learned_verifier_pre_reject_count

Per-epoch: count of candidates rejected at step 05.6 in this epoch (any retry attempt counts).

### 5.3 learned_verifier_false_positive_rate

Per-epoch:
```
fp = count(r for r in epoch_rounds_with_step_14_6
           where r.predicted_collision_prob >= 0.3 and r.step_14_6_actual == "SURVIVES")
fpr = fp / count(r for r in epoch_rounds_with_step_14_6 where r.step_14_6_actual == "SURVIVES")
```

Target ≤ 0.20 for v19; if > 0.30, raise reject_threshold from 0.3 to 0.4 in v20.

### 5.4 learned_verifier_true_positive_count

Per-epoch:
```
tp = count(r for r in epoch_rounds_with_step_14_6
           where r.predicted_collision_prob >= 0.3 and r.step_14_6_actual == "EXTERNAL_COLLISION")
```

Note: in v19 design, learned_verifier rejects BEFORE step 14.6 reaches the candidate. So "true positive" is measured retrospectively on candidates where the learned verifier said "reject" but step 14.6 was still run (e.g., manual audit; or candidates that the learned verifier predicted ≥0.3 but step 05.6 mechanically passed — never happens in v19 since 0.3 is the hard threshold). In practice, this metric tracks the candidates that the learned verifier *would have rejected but was overridden by the regeneration loop* — i.e., the regeneration produced a candidate that still has high `predicted_collision_prob` from the first attempt that the new regen now passes.

Cleaner v19 operationalization:
```
tp = count of EXTERNAL_COLLISION rounds in the epoch where, at the originally-presented candidate's features, predicted_collision_prob would have been >= 0.3
```

This is a counterfactual: "would learned verifier have caught this if it had been allowed to see this candidate?" It's logged for each EXTERNAL_COLLISION round.

### 5.5 v19 score formula additions

```
score_v19 = score_v18 (all v18 terms, UNCHANGED)
          + (learned_verifier_agreement_rate × 5)           ← NEW v19 (headline metric)
          + (learned_verifier_pre_reject_count × 1)         ← NEW v19 (rewards budget-saving rejection)
          - (learned_verifier_false_positive_rate × 3)      ← NEW v19 (penalizes over-rejection)
          + (learned_verifier_true_positive_count × 2)      ← NEW v19 (rewards confirmed catches)
```

Net at baseline (agreement 0.85, pre_reject 3, fpr 0.10, tp 1): +4.25 + 3 − 0.30 + 2 = +8.95 contribution. At worse outcomes (agreement 0.65, pre_reject 1, fpr 0.30, tp 0): +3.25 + 1 − 0.9 + 0 = +3.35 contribution.

---

## 6. Loop control (v19)

```
read logs/policy_state.json
read logs/architecture_tools.json
read logs/frontier_seeds.json
read logs/known_collisions.json
read logs/expert_path.json
read logs/learned_verifier_weights.json    ← NEW v19
read prior epoch coverage profile
write logs/policy_state.json with current_epoch += 1, schema 1.9

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute
    execute step 04.5

    # v18 step 05: local heavy-tail around expert path (UNCHANGED)
    pool = step_05_v18(active_anchors, ...)
    write 05_candidate_pool.json + 05_anchor_assignment.json

    cluster_assign = kmeans(pool, k=25, seed=epoch)        # v14 step 05.4 UNCHANGED
    write 05_4_diversity_filter.json
    compute_pairwise_niche_distance + replace                # v15 step 05.45 UNCHANGED
    write 05_45_intra_cluster_diversification.json

    for candidate in selected_25_post_replacement:
        verdict_05_5 = step_05_5_v17(candidate)             # v17 cascade UNCHANGED
        if verdict_05_5.startswith("REJECTED_"):
            regen_loop(...)
            continue

        verdict_05_6 = step_05_6_v19(candidate, kcd_entries, weights, bias)   # NEW v19
        write 05_6_learned_verifier.json
        if verdict_05_6.verdict == "REJECTED_LEARNED_VERIFIER":
            regen_loop_via_v18_prompt(...)
            continue

        if verdict_05_5 == "PASS" and verdict_05_6 == "PASS":
            PRIMARY = candidate
            break

    if PRIMARY == None:
        PRIMARY = highest slot-novelty within active-anchor neighborhood
        run step 05.5 + 05.6 regeneration cascade

    write 05_candidate.json (now includes predicted_collision_prob + learned_verifier_features)
    write 05_5_known_collision_check.json
    write 05_5_pattern_filter.json

    execute step 06, 06.5, 06.7, 07
    execute step 08, 09
    execute step 10
    execute step 11, 11.5, 12
    execute step 13, 13.5
    execute step 14
    execute step 14.6 (when step 14 INVESTIGATIVE_CANDIDATE)

    compute v19_verdict (= v18_verdict + REJECTED_LEARNED_VERIFIER)
    update memory_db.json round entry with v19 fields

    if round_num % 25 == 0:
        write output/stats_round_NNN.json
        compute coverage_profile (v14 step 14.5)
        write output/14_5_coverage_profile_E{N}.json
        compute v19 learned_verifier_metrics (agreement_rate, fpr, pre_reject_count, true_positive_count)
        run audit_feedback_loop()              ← v17 AFL UNCHANGED
        update logs/known_collisions.json
        run post_epoch_anchor_update()         ← v18 UNCHANGED
        update logs/expert_path.json
        run refit_learned_verifier()           ← NEW v19
        update logs/learned_verifier_weights.json
        update logs/policy_state.json
```

---

## 7. Stats schema additions in v19

`output/stats_round_NNN.json` adds:

```json
{
  ... (all v1-v18 fields) ...,
  "v19_learned_verifier_metrics": {
    "step_05_6_fired_count": 25,
    "learned_verifier_pre_reject_count_E{N}": 0,
    "learned_verifier_pre_reject_rounds": [],
    "learned_verifier_pre_reject_predicted_probs": [],
    "learned_verifier_agreement_rate_E{N}": 0.0,
    "learned_verifier_false_positive_rate_E{N}": 0.0,
    "learned_verifier_true_positive_count_E{N}": 0,
    "learned_verifier_predicted_probs_per_round": {},
    "learned_verifier_features_per_round": {},
    "weights_at_epoch_start": [3.2, 0.8, -1.5, -1.0, 1.2],
    "bias_at_epoch_start": -0.5,
    "weights_at_epoch_end": [],
    "bias_at_epoch_end": 0.0,
    "training_label_count_at_epoch_start": 19,
    "training_label_count_at_epoch_end": 0,
    "refit_run_at_epoch_end": false,
    "kcd_entries_used_for_feature_computation_count": 6
  }
}
```

Existing v17 (`v17_*_metrics`) and v18 (`v18_*_metrics`) blocks are preserved.

---

## 8. ★ FORBIDDEN-TO-MODIFY zones (verbatim from v5...v18 + v19 explicit)

### 8.1 v18's FORBIDDEN list — UNCHANGED
- Step 06 web_search
- Step 07 keyword threshold ≥ 2
- Step 10 mechanical verdict
- Step 12 tree-stream
- Step 13 spec format
- Step 13.5 attack format
- Step 14 cross-step coherence
- Step 14.5 coverage profile
- Step 14.6 external collision detection
- Step 05.4 k-means diversity filter
- Step 05.45 intra-cluster diversification
- Step 05.5 anti-R279 filter
- Step 05 anchor-local sampling (v18)
- PASS criterion (10 signals)

### 8.2 v19 modifies ONLY:
- **NEW step 05.6 gate**: between v17's step 05.5 cascade and step 06. Learned-verifier predicted_collision_prob.
- **NEW post-epoch refit_learned_verifier procedure**: runs after AFL + anchor_update.
- **NEW verdict label**: REJECTED_LEARNED_VERIFIER (12th verdict; v17/v18 had 11).

### 8.3 v17 + v18 components — UNCHANGED
- v17: FTS, KCD pre-check, AFL.
- v18: anchor-local sampling, expert_path.json, stale-drop, sub-anchor promotion.
- v17 verdict labels (11) preserved; v18 added 0; v19 adds 1.

---

## 9. Anti-cheating commitments (v19 additions on top of v18)

The v3...v18 instructions stand. v19 adds:

- **Weights immutability mid-epoch.** Logistic regression weights and bias are fixed for the entire epoch's 25 rounds. Only end-of-epoch refit may update them.
- **Training label immutability.** Training labels are NOT modified mid-epoch. New labels are *appended* at end-of-epoch (after step 14.6 verdicts are settled), and the refit re-trains on the full set.
- **Reject threshold immutability.** 0.3 fixed for E38; only v20 may tune.
- **Feature definitions immutability.** The 5 features are fixed; v20 may add or refine.
- **Productive set immutability.** The 5-slot + 6-citation + 7-fragile-pattern sets are fixed for E38; only v20 may tune.
- **Honest fitting.** The logistic regression fit is deterministic given training data + regularization parameter (λ=1). Bootstrapping must be reproducible from the 19 training labels.
- **Cross-validation honesty.** step 14.6 runs UNCHANGED. The agreement metric is computed AFTER step 14.6 (not bidirectionally — step 05.6 never depends on step 14.6's outcome within the same round).
- **learned_verifier_weights.json write-protected mid-epoch.** Only post-epoch refit writes; mid-epoch writes are forbidden.

---

## 10. Inherited history (v1 → v19)

- **v1-v18**: see prior program_vN.md files.
- **v19** (this file): v18 base + Learned Verifier from Collision History (Swamy framework B). **R926-R950 under v19 in E38.**

---

## 11. What v19 does NOT promise

v19 does NOT promise more substantive PASS verdicts. The 1021-round saturation result (0 confirmed substantive PASS, p ≈ 0.0000350 at N=1021) is structural. v19 acknowledges the same Phase 1 diagnosis: detector layers cannot raise PASS rate. v19 promises a different shift: **introduce verifier learning** — the first per-candidate predictive collision-risk signal in the pipeline, with cross-validation against step 14.6.

What v19 promises:
- **Pre-emptive rejection of candidates predicted to collide.** Reduces budget spent on sterile anchor neighborhoods (E37 had 32% of selected_25 in zero-yield neighborhoods).
- **Cross-validation against step 14.6.** Tracks `learned_verifier_agreement_rate` per epoch; high agreement validates the learned model, low agreement flags a new failure mode.
- **Continuous training.** End-of-epoch refit on updated label set (19 + new). The training set grows by ~1-3 per epoch as new INVESTIGATIVE_SURVIVING and EXTERNAL_COLLISIONS are confirmed.
- **Constraint-pattern detection.** Feature f5 explicitly flags R895-style fragility patterns; learned verifier will likely down-weight ANCHOR_R895's neighborhood predictively.

v19 does NOT promise to break the structural PASS ceiling. It introduces the verifier learning channel that v18 explicitly lacks.

---

## 12. Honest deviation policy (for E38 execution)

Same as v14...v18 (max 5 synthesized Agent spawns per epoch). v19's learned verifier is mechanical (logistic regression with 5 features); no Agent spawn needed for step 05.6 evaluation. The end-of-epoch refit is also mechanical (gradient descent on 5 features × ~20 training labels). Real Agent spawns reserved for step 13.5 adversarial attacks if any are needed for genuinely novel candidates.

---

## 13. Phase 4 reporting requirements (for output/epoch38_comparison.md)

After E38 completes, the comparison document must record:
1. **learned_verifier_pre_reject_count_E38**: how many candidates were rejected at step 05.6 in E38.
2. **learned_verifier_agreement_rate_E38**: agreement with step 14.6.
3. **learned_verifier_false_positive_rate_E38**: over-rejection rate.
4. **learned_verifier_true_positive_count_E38**: confirmed catches.
5. **REJECTED_LEARNED_VERIFIER_count_E38**: count of the new verdict label.
6. **per_anchor_INVESTIGATIVE_SURVIVING_count_E38**: which anchors yielded (including the 3 new from E37: ANCHOR_R905, R908, R922).
7. **ANCHOR_R866 + ANCHOR_R895 epochs_since_yield after E38**: 2 if both still sterile.
8. **active_anchor_count_at_E38_end**: starting at 10; expect 10-13 after new sub-anchor/discovery promotions.
9. **v19 score with new terms**.
10. **v19 vs v18 score delta**: expected +5 to +10.
11. **Cumulative N_verified after E38 = 1046**.
12. **p(no PASS | 1% H₀) at N=1046 ≈ 0.0000274**.
13. **Honest deviation count**: synthesized agent spawns this epoch (target: <5).
14. **collision_addition_rate_E38** (via v17 AFL).
15. **KCD database size at E38 start vs end** (continues from v18).
16. **expert_path size at E38 start vs end** (continues from v18).
17. **learned_verifier_weights at E38 start vs end** (refit delta).
18. **training_label_count at E38 start vs end** (19 → ~22-26).

This is the v19 contribution: introducing the **first verifier learning channel** in the pipeline, with cross-validation against the unchanged step 14.6 rubric, and pre-emptive budget saving via predicted_collision_prob.
