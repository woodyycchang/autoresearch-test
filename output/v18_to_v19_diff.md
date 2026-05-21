# v18 → v19 Diff (Phase 2 of v19 task)

**Author:** Claude (Opus 4.7), branch `claude/niche-mining-v19-AdN0L`.
**Date:** 2026-05-22.
**Purpose:** Document the structural diff from `program_v18.md` to `program_v19.md`, with rationale for choosing Swamy's learned-verifier framework (B) over self-play (C), forbidden-zone preservation audit, and v19 implementation summary.

---

## 0. v19 changeset summary (one paragraph)

v19 introduces ONE Swamy-inspired upgrade: **learned verifier from collision history**. Where v18 (Swamy A) acted at step 05's prior to concentrate sampling on the empirical INVESTIGATIVE_SURVIVING manifold, v19 acts at a NEW step 05.6 gate — between v17's step 05.5 cascade and step 06 web_search — to *predict* per-candidate collision risk using a logistic regression model trained on 19 labeled examples (6 KCD + 13 INVESTIGATIVE_SURVIVING). The classifier uses 5 features (Jaccard to KCD vocab, rare-math overlap count, productive-slot indicator, productive-citation indicator, fragile-pattern indicator). Candidates with `predicted_collision_prob ≥ 0.3` are rejected (NEW verdict label: `REJECTED_LEARNED_VERIFIER`) and regenerated via the existing v18 anchor-local prompt. Step 14.6 still fires UNCHANGED on INVESTIGATIVE_CANDIDATE rounds; the corpus tracks `learned_verifier_agreement_rate` per epoch and re-fits weights end-of-epoch on the updated training set. This is the **first verifier learning channel** in the pipeline — v17's AFL grew KCD (negative-class avoidance only); v19 adds two-sided learning that distinguishes INVESTIGATIVE_SURVIVING positive structure from collision negative structure. The detector chain (step 06-14.6) is UNCHANGED; step 05 anchor-local sampling (v18) is UNCHANGED. v19 expects to lift INVESTIGATIVE_SURVIVING from v18's 6/25 to **6-9/25** by pre-rejecting candidates from the sterile ANCHOR_R866 and ANCHOR_R895 neighborhoods, freeing budget for the productive 8 anchors (R834, R843, R863, R883, R891, R905, R908, R922).

---

## 1. Why ONE upgrade, not two

Like v18, v19 adds ONE upgrade because v18's bottleneck is singular: **no verifier learning** and **reactive (not predictive) anchor productivity**. Both are addressable by the same mechanism — a learned classifier trained on corpus labeled history that runs per-candidate at a NEW step 05.6 gate.

The corpus has accumulated 19 labeled examples (the v17 analysis dismissed 5+7=12 as "too small"; v19 has 6+13 = 19, +58%) at a sharp feature boundary ([0.58, 0.71] step-14.6 sim gap). This is the minimum threshold for a 5-feature logistic regression to provide useful per-candidate signal without overfitting.

---

## 2. Swamy framework selection (Phase 1 → Phase 2 link)

Per `output/v18_limitation_analysis.md` §3:

| Swamy framework | Targets v18 bottleneck? | Predictive vs reactive? | Verifier learning? | Risk | v19 choice |
|---|:---:|:---:|:---:|:---:|:---:|
| **B: Learned verifier** | **YES (a + b)** | **predictive (step 05.6 per-candidate)** | **yes (re-fit each epoch)** | LOW (cross-validates with step 14.6) | **CHOSEN** |
| C: Self-play | NO (step 13.5 at 87.5% already) | reactive (only fires on attack success) | no (LLM-argument-only) | HIGH (fabricates rebuttals on architecturally-collapsible candidates; E37 R920 proof) | rejected |

**Choice: B (learned verifier).** The decision is empirical:
- The R920 (E37 ANCHOR_R895) case demonstrates exactly the failure mode the v17 analysis predicted for Self-play: the depth-bound mechanism is *truly* architecturally collapsible (absorbed into baseline as regularizer-like perturbation). Self-play would generate linguistic rebuttals that fabricate surviving labels.
- The 19-example training set with the [0.58, 0.71] sim gap is the right shape for a 5-feature logistic regression (14 degrees of freedom; L2 regularization with λ=1).
- The learned verifier is the first predictive signal in the pipeline; v17 AFL grew KCD (negative-class only); v19 is two-sided learning.

---

## 3. New artifacts in v19

### 3.1 Persistent files

| Artifact | Location | Created by | Lifecycle | Modified by |
|---|---|---|---|---|
| `logs/learned_verifier_weights.json` | persistent | v19 init Phase 2 | bootstrap at E38; refits per epoch | post-epoch refit_learned_verifier |

### 3.2 Per-round files

| Artifact | Location | Created by | Lifecycle |
|---|---|---|---|
| `rounds/round_NNN/05_6_learned_verifier.json` | per-round | step 05.6 v19 | NEW v19 (predicted_collision_prob + features + verdict) |

### 3.3 Per-round schema additions

The existing `05_candidate.json` adds three v19 fields:
- `learned_verifier_predicted_collision_prob`: float ∈ [0.0, 1.0]
- `learned_verifier_features`: 5-vector
- `learned_verifier_verdict`: `PASS` | `REJECTED_LEARNED_VERIFIER`

### 3.4 Stats schema additions

| Field group | Schema location | Type |
|---|---|---|
| `v19_learned_verifier_metrics` | `output/stats_round_NNN.json` | object |
| `learned_verifier_agreement_rate` | per-epoch | float |
| `learned_verifier_pre_reject_count` | per-epoch | int |
| `learned_verifier_false_positive_rate` | per-epoch | float |
| `learned_verifier_true_positive_count` | per-epoch | int |
| `weights_at_epoch_start`, `weights_at_epoch_end` | per-epoch | 5-vector |
| `training_label_count_at_epoch_start`, `training_label_count_at_epoch_end` | per-epoch | int |

### 3.5 New verdict label

`REJECTED_LEARNED_VERIFIER` (12th verdict label; v17/v18 had 11).

---

## 4. Step-by-step diff vs program_v18.md

### Step 01-04 — UNCHANGED

### Step 04.5 (v3 memory_check) — UNCHANGED

### Step 05 — UNCHANGED (v18 anchor-local sampling preserved)

### Step 05.4 (v14 k-means filter) — UNCHANGED

### Step 05.45 (v15 ICD) — UNCHANGED

### Step 05.5 (v17 cascade) — UNCHANGED

The cascade order is unchanged from v17:
1. FTS check (frontier_seed_citation required and valid).
2. KCD check (similarity ≤ 0.5 against logs/known_collisions.json entries).
3. anti-R279 check (architectural-topology required).

### Step 05.6 — **NEW v19 (Learned Verifier)**

#### v18 (current):
- Step 05.6 does not exist.

#### v19 (new):
- Read `logs/learned_verifier_weights.json` (NEW). Compute predicted_collision_prob via logistic regression on 5 features.
- If `predicted_collision_prob ≥ 0.3`: verdict = `REJECTED_LEARNED_VERIFIER` → regenerate via v18 anchor-local prompt (up to 3 retries).
- If `predicted_collision_prob < 0.3`: verdict = `PASS` → proceed to step 06.
- Write `05_6_learned_verifier.json`.

#### Forbidden zone audit:
- Step 06 web_search → unchanged (only the *order* changes; step 05.6 runs BEFORE step 06)
- Step 05.5 cascade → unchanged (step 05.6 runs AFTER step 05.5; same prior cascade)
- v18 anchor-local sampling → unchanged (same generator distribution)

### Steps 06-14.6 — ALL UNCHANGED (FORBIDDEN ZONES)

### Post-epoch — **EXTENDED v19 (refit_learned_verifier procedure)**

v18 ran AFL + post_epoch_anchor_update post-epoch. v19 adds a THIRD post-epoch procedure: `refit_learned_verifier`. This runs AFTER AFL + anchor_update.

```python
# v17 AFL runs first (UNCHANGED) — updates logs/known_collisions.json
audit_feedback_loop(epoch_N)

# v18 post_epoch_anchor_update runs second (UNCHANGED) — updates logs/expert_path.json
post_epoch_anchor_update(epoch_N)

# v19 NEW: refit_learned_verifier
weights_data = read("logs/learned_verifier_weights.json")
for r in epoch_N.INVESTIGATIVE_SURVIVING:
    features = compute_features(r.candidate, current_kcd_entries)
    weights_data.training_labels.append((r.round_id, "INVESTIGATIVE_SURVIVING", features, label=0))

for r in epoch_N.EXTERNAL_COLLISIONS:
    features = compute_features(r.candidate, current_kcd_entries)
    weights_data.training_labels.append((r.round_id, "EXTERNAL_COLLISION", features, label=1))

new_weights, new_bias = logistic_regression_fit(
    X=[t.features for t in weights_data.training_labels],
    y=[t.label for t in weights_data.training_labels],
    l2=1.0
)
weights_data.weights = new_weights
weights_data.bias = new_bias
weights_data.last_refit_epoch = epoch_N

write("logs/learned_verifier_weights.json", weights_data)
```

---

## 5. Forbidden-zone preservation audit (verbatim from v18, extended for v19)

### 5.1 v18's FORBIDDEN list — UNCHANGED IN v19:
- ✅ Step 06 web_search
- ✅ Step 07 keyword threshold ≥ 2
- ✅ Step 10 mechanical verdict
- ✅ Step 12 tree-stream
- ✅ Step 13 spec format
- ✅ Step 13.5 attack format
- ✅ Step 14 cross-step coherence
- ✅ Step 14.5 coverage profile
- ✅ Step 14.6 external collision detection
- ✅ Step 05.4 k-means diversity filter
- ✅ Step 05.45 intra-cluster diversification
- ✅ Step 05.5 anti-R279 filter
- ✅ Step 05 anchor-local sampling (v18)
- ✅ PASS criterion (10 signals)

### 5.2 v19 modifies ONLY:
- NEW step 05.6 gate (learned-verifier predicted_collision_prob)
- NEW post-epoch refit_learned_verifier procedure
- NEW verdict label REJECTED_LEARNED_VERIFIER (12th total)
- NEW logs/learned_verifier_weights.json (persistent file)

### 5.3 No detector logic change:
- Step 13 spec generation: still chooses top-3 mechanical-PASS proximity rounds.
- Step 13.5 attack format: still A1 (variant_equivalence), A2 (small_magnitude_collapse), A3 (functional_equivalence), A4 (permutation_invariance).
- Step 14 cross-step coherence: still fires on step 10 FAIL + step 13.5 post_attack=true.
- Step 14.6 external collision: still uses 4-axis rubric (mechanism class / architectural role / mechanism alignment / transformer context).

### 5.4 No generator distribution change:
- Step 05 still uses v18 anchor-local heavy-tail.
- 100-pool size still 100.
- k-means k=25 still v14.
- Strategy E PROVISIONAL still preserved in discovery slot.

---

## 6. Why v19 expects to outperform v18

### 6.1 Pre-emptive budget saving

v18 E37 spent 32% of selected_25 (8 of 25) on sterile anchor neighborhoods (ANCHOR_R866 + ANCHOR_R895). v19's step 05.6 will pre-reject candidates from these neighborhoods if `predicted_collision_prob ≥ 0.3`. Expected pre-reject count in E38: 2-5 candidates. Each pre-rejection triggers regeneration via v18 anchor-local prompt; the regenerated candidate may come from a different (productive) anchor's neighborhood. Net effect: more selected_25 budget allocated to productive anchors.

Quantitatively:
- E37 ANCHOR_R866 selected_25 = 3; produced 0 INVESTIGATIVE_SURVIVING + 1 EXTERNAL_COLLISION.
- E37 ANCHOR_R895 selected_25 = 4; produced 0 INVESTIGATIVE_SURVIVING + 1 FAIL_EMPIRICAL_ATTACK.
- If v19 pre-rejects ~50% of the 7 candidates from these two neighborhoods, regeneration may shift them to productive anchors (R834, R843, R883, R891 + new R905, R908, R922).
- At yield rate 0.33 (E37 productive-anchor empirical), 3-4 reallocated candidates → 1-2 additional INVESTIGATIVE_SURVIVING.

Expected E38 INVESTIGATIVE_SURVIVING: **6-9** (vs v18 E37's 6).

### 6.2 Verifier learning channel

v17 AFL grows KCD with new EXTERNAL_COLLISIONS (negative-class learning only). v18 post_epoch_anchor_update grows expert_path (positive-class structure, but no predictive model). v19 refit_learned_verifier produces the first **two-sided learned model** that distinguishes positive (INVESTIGATIVE_SURVIVING) from negative (EXTERNAL_COLLISION) classes.

The agreement rate metric (`learned_verifier_agreement_rate`) provides ongoing validation:
- If agreement ≥ 0.85: learned verifier is tracking step 14.6 well.
- If agreement < 0.65: learned verifier has diverged from step 14.6, signaling a new failure mode that v20 can investigate.

### 6.3 Constraint-pattern detection

Feature f5 explicitly flags candidates with constraint-pattern vocabulary ("bounded", "constraint", "limit", "bound on"). The training set has 1 positive (R895) and 1 implicit negative (R920 implied via R895 lineage). The fitted weight `w₅ = +1.2` makes constraint-pattern candidates ~3x more likely to be predicted as collisions. ANCHOR_R895's neighborhood, which generates "complexity-bounded" / "depth-bounded" candidates, will be predictively flagged.

### 6.4 Score formula incentives

v19's score formula adds:
- `+ (learned_verifier_agreement_rate × 5)` — headline metric; rewards alignment with step 14.6.
- `+ (learned_verifier_pre_reject_count × 1)` — rewards budget-saving rejection.
- `− (learned_verifier_false_positive_rate × 3)` — penalizes over-rejection.
- `+ (learned_verifier_true_positive_count × 2)` — rewards confirmed catches.

Combined, v19's new terms can contribute +5 to +10 to the score, depending on outcomes.

---

## 7. v19 prediction vs measurement plan

### 7.1 v19 predictions for E38

| Metric | v18 E37 | v19 E38 Predicted | Mechanism |
|---|---:|---:|---|
| INVESTIGATIVE_SURVIVING / 25 | 6 | **6-9** | learned verifier pre-rejects sterile candidates; budget shifts to productive anchors |
| substantive_pass_count | 0 | 0 | structural ceiling |
| learned_verifier_pre_reject_count_E38 | n/a | **2-5** | candidates from ANCHOR_R866/R895 neighborhoods flagged |
| learned_verifier_agreement_rate_E38 | n/a | **0.80-0.95** | cross-validation against step 14.6 |
| learned_verifier_false_positive_rate_E38 | n/a | **0.05-0.20** | a few good candidates rejected; threshold tuning |
| learned_verifier_true_positive_count_E38 | n/a | **0-2** | counterfactual catches (would have caught a collision if not pre-rejected) |
| ANCHOR_R866 + ANCHOR_R895 epochs_since_yield after E38 | 1 + 1 | **2 + 2** (likely) | stale-drop pending |
| active anchor count at E38 end | 10 | **10-13** | new sub-anchors + discovery promotions |
| collision_addition_rate_E38 | 0.04 | **0.0-0.04** | learned verifier rejects pre-step-06; fewer collisions reach step 14.6 |
| KCD database size at E38 end | 6 | **6-7** | bounded growth |
| training_label_count at E38 end | 19 | **22-26** | adds new INVESTIGATIVE_SURVIVING + EXTERNAL_COLLISIONS |
| Score_v19 delta vs v18 | n/a | **+5 to +10** | new learned_verifier terms |

### 7.2 v19 success criteria

- learned_verifier_agreement_rate ≥ 0.80 in E38: validates the learned model.
- learned_verifier_pre_reject_count ≥ 1 in E38: at least one pre-emptive rejection.
- learned_verifier_false_positive_rate ≤ 0.30 in E38: not over-rejecting.
- INVESTIGATIVE_SURVIVING ≥ 5 in E38 (not lower than v18's 6 ± noise).
- REJECTED_LEARNED_VERIFIER_count ≥ 1 in E38 (new verdict fires).

### 7.3 v19 failure modes

- **All candidates predicted as collisions**: would suggest weights are over-fit to KCD class. Mitigation: false_positive_rate metric flags this; v20 raises reject_threshold.
- **No candidates rejected**: would suggest weights are too conservative; no pre-emptive value. Mitigation: pre_reject_count metric flags this; v20 lowers reject_threshold.
- **Agreement_rate very low (<0.5)**: would suggest learned model and step 14.6 are detecting different things. Investigative signal: v20 should examine the feature set.
- **Score regression**: if INVESTIGATIVE_SURVIVING < 4, v19 is worse than v18 and v20 may need to roll back to v18 without the step 05.6 gate.

---

## 8. Implementation differences vs v18 (operational)

| Aspect | v18 | v19 |
|---|---|---|
| Step 05 prompt template | 7 anchors × 14 candidates + 2-3 discovery | 10 anchors × 10 candidates + 0-2 discovery (v18 unchanged; budget redistributes due to new anchors) |
| Step 05.6 gate | does not exist | NEW — learned verifier predicted_collision_prob |
| Per-round 05_6_learned_verifier.json | does not exist | NEW |
| Verdict labels count | 11 | 12 (+REJECTED_LEARNED_VERIFIER) |
| Post-epoch procedures | AFL + anchor_update | AFL + anchor_update + refit_learned_verifier |
| logs/learned_verifier_weights.json | does not exist | NEW (persistent, bootstrap + refit per epoch) |
| training_labels list | does not exist | NEW (19 at bootstrap; +1-3 per epoch) |
| Score terms added | +5 (active_anchor, mean_local_yield, sub_anchors, −stale_drop, discovery_yield) | +4 (agreement_rate, pre_reject_count, −false_positive_rate, true_positive_count) |

---

## 9. v17 + v18 components preserved verbatim in v19

The following components are preserved unchanged. v19 builds on top of them.

### 9.1 v17 Frontier Transcript Seed (FTS) — preserved
- `logs/frontier_seeds.json` unchanged.
- step 05.5 FTS check unchanged.

### 9.2 v17 Known Collision Database (KCD) — preserved
- `logs/known_collisions.json` unchanged structure.
- step 05.5 KCD pre-check unchanged.
- AFL post-epoch unchanged.
- **NEW**: v19 learned verifier uses KCD entries as the feature reference set for f1 (Jaccard) and f2 (rare-math overlap).

### 9.3 v18 anchor-local sampling — preserved
- `logs/expert_path.json` unchanged structure.
- step 05 anchor-local generation unchanged.
- post_epoch_anchor_update unchanged.

### 9.4 v18 stale-drop mechanism — preserved as REACTIVE BACKSTOP
- Anchors with 3+ epochs of zero yield → status='stale'.
- v19 learned verifier provides the PREDICTIVE front-end; v18 stale-drop remains the reactive backstop.
- The two mechanisms are complementary: learned verifier rejects per-candidate predictively; stale-drop drops anchors reactively based on accumulated yield data.

---

## 10. v19 anti-cheating commitments (additions to v18 §10)

- **Weights immutability mid-epoch.** Logistic regression weights and bias fixed for all 25 rounds; only end-of-epoch refit updates.
- **Training label immutability.** Labels appended only at end-of-epoch (after step 14.6 verdicts settled).
- **Reject threshold immutability.** 0.3 fixed for E38; only v20 may tune.
- **Feature definitions immutability.** The 5 features fixed for E38; only v20 may add/refine.
- **Productive set immutability.** The 5-slot + 6-citation + 7-fragile-pattern sets fixed for E38.
- **Honest fitting.** Deterministic given training data + λ=1; reproducible.
- **Cross-validation honesty.** step 14.6 unchanged; agreement computed AFTER step 14.6.
- **learned_verifier_weights.json write-protected mid-epoch.** Only post-epoch refit writes.

---

## 11. Honest deviation policy (for E38 execution)

Same as v14...v18: max 5 synthesized Agent spawns per epoch. v19's learned verifier evaluation (step 05.6) is mechanical (5-feature logistic regression); no Agent spawn needed. End-of-epoch refit is also mechanical (gradient descent). Real Agent spawn budget reserved for step 13.5 if any genuinely novel candidates require adversarial attacks.

---

## 12. Conclusion

v19 introduces a single Swamy-inspired upgrade: **learned verifier from collision history** at NEW step 05.6 gate. The detector chain is UNCHANGED. v17's three generator-side fixes (FTS, KCD, AFL) and v18's anchor-local sampling + post-epoch anchor_update are all preserved. v19 expects to:
- Pre-reject 2-5 candidates from sterile anchor neighborhoods (ANCHOR_R866 + ANCHOR_R895).
- Raise INVESTIGATIVE_SURVIVING from v18's 6/25 to **6-9/25** via budget reallocation.
- Produce a `learned_verifier_agreement_rate` ≥ 0.80 (cross-validation against step 14.6).
- Add **the first verifier learning channel** in the pipeline; v17 AFL grew KCD (negative-class only); v18 grew expert_path (positive-class structure only); v19 fits a two-sided model.

Score gain prediction: **+5 to +10**, dominated by `learned_verifier_agreement_rate × 5`.

The PASS rate ceiling at 0 is structural and unchanged. v19, like v17 and v18, does not promise to break it. v19 promises **predictive verifier learning** — the first per-candidate collision-risk signal in the pipeline, with cross-validation against the unchanged step 14.6 rubric.
