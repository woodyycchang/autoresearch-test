# v18 Limitation Analysis (v19 Phase 1)

**Author:** Claude (Opus 4.7), branch `claude/niche-mining-v19-AdN0L`.
**Date:** 2026-05-22.
**Purpose:** Identify v18's bottleneck after E37's 6 INVESTIGATIVE_SURVIVING outcome (vs v17's 3). v18 doubled yield via local exploration around the 7-anchor expert path but every INVESTIGATIVE_SURVIVING was still validated by the *unchanged* rule-based detector chain (step 13.5 + step 14 + step 14.6). No learning happens. Stale-drop is reactive, not predictive. Map onto Swamy's remaining frameworks (B learned verifier, C self-play) — pick the one that addresses the right bottleneck for v19.

---

## 0. One-paragraph diagnosis

v18 successfully concentrated mass on the empirical INVESTIGATIVE_SURVIVING manifold (6 of 25 = 24% yield, up from v17's 12%), but two structural limitations remain. **First, anchor productivity is binary and reactive**: at end of E37, 5 of 7 bootstrap anchors fired exactly 1 yield while 2 (ANCHOR_R866, ANCHOR_R895) fired 0 — yet the system has no signal *predicting* which anchors will be sterile until 3 epochs of zero-yield data accumulate (the stale-drop threshold). The two failure modes in E37 (R911 EXTERNAL_COLLISION at sim=0.71, R920 FAIL_EMPIRICAL_ATTACK at A1 success) were both *foreseeable post-hoc*: R911 sat in ANCHOR_R866's "edge" neighborhood (distance 0.45) near published elimination-theory routing; R920 inherited ANCHOR_R895's already-architecturally-fragile complexity-bounded framing. No feature-level prediction flagged either. **Second, the detector chain has no feedback channel**: step 14.6's 4-axis rubric is rule-based and produces the *only* signal on candidate quality, yet the corpus has accumulated 6 confirmed collisions (KCD_R279, R827, R855, R880, R911, plus the 7-cluster macro-entry) and 13 confirmed INVESTIGATIVE_SURVIVING (R834, R843, R863, R866, R883, R891, R895, R902, R905, R908, R914, R917, R922) — 19 labeled examples that no current pipeline component learns from. The bottleneck is **(b) verifier accuracy on local-exploration candidates + (a) predictive anchor productivity** — *both addressable by Swamy framework B (learned verifier)* that consumes the 19 labeled examples and runs at a NEW pre-step-06 gate (step 05.6), cross-validating against step 14.6. **Swamy framework C (self-play) is rejected** because the E37 R920 case proves the same risk the v17 analysis flagged: architecturally collapsible candidates fabricate rebuttals under iteration that don't survive real review.

---

## 1. The 13 INVESTIGATIVE_SURVIVING + 6 known collisions — corpus learning signal

The corpus now has substantial labeled data not used by any pipeline component.

### 1.1 INVESTIGATIVE_SURVIVING (13 entries, positive class)

| Round | Epoch | Slot | Domain | Mechanism | step 14.6 sim | Anchor parent |
|---:|---:|:---:|---|---|---:|---|
| R834 | E34 | S15 | category-theory | Bayes-categorical-posterior conformal critic | 0.51 | — (bootstrap) |
| R843 | E34 | S16 | free-probability | Free-cumulant token routing | 0.43 | — (bootstrap) |
| R863 | E35 | S15 | Hochschild-cohom | Hochschild-cochain critic head | 0.41 | — (bootstrap) |
| R866 | E35 | S16 | elimination-theory | Bezout-resultant token routing | 0.39 | — (bootstrap) |
| R883 | E36 | S20 | test-time-training | TTT inner-loop adapter | 0.55 | — (bootstrap) |
| R891 | E36 | S14 | info-theory | Heavy-tail entropic objective | 0.45 | — (bootstrap) |
| R895 | E36 | S16 | complexity-theory | Polynomial-time-bounded routing | 0.38 | — (bootstrap) |
| **R902** | E37 | S15 | category-theory | Bayesian-posterior dual-critic | 0.51 | ANCHOR_R834 (d=0.38) |
| **R905** | E37 | S16 | free-probability | Non-commutative cumulant routing | 0.43 | ANCHOR_R843 (d=0.45) |
| **R908** | E37 | S15 | Hochschild-cohom | Periodic-cyclic-cochain critic | 0.49 | ANCHOR_R863 (d=0.42) |
| **R914** | E37 | S20 | test-time-training | TTT inner-state adaptive recurrence | 0.58 | ANCHOR_R883 (d=0.38) |
| **R917** | E37 | S14 | info-theory | Long-tail-aware adaptive loss | 0.48 | ANCHOR_R891 (d=0.39) |
| **R922** | E37 | S07 | rep-exploration | Visit-counter sparsity gate | 0.44 | discovery |

**Feature pattern observable:**
- Slot distribution: {S14: 2, S15: 4, S16: 4, S20: 2, S07: 1} — 12/13 in {S14, S15, S16, S20}
- step 14.6 functional similarity range: [0.38, 0.58] — **mean 0.469**, std 0.060, max 0.58 (well below 0.7 threshold)
- All 13 have non-zero `is_architectural_topology_change` (mechanical step 05.5)
- All 13 cite ≥1 frontier_seed primitive (v17 FTS preserved)
- All 13 have rare-math vocabulary or frontier-seed-direct citation (no overlap with KCD vocab)

### 1.2 Known collisions (6 entries, negative class)

| ID | Round | Class | sim | embedding_keys highlight |
|---|---:|---|---:|---|
| KCD_R279 | 279 | X-divergence + Y-state-regularizer | n/a | KL, divergence, memory, state |
| KCD_R827 | 827 | X-divergence + Y-state-regularizer | 0.87 | Bregman, divergence, reservoir, projection |
| KCD_R855 | 855 | X-spectral + Y-residual | 0.83 | L-function, spectral, residual, Selberg |
| KCD_R880 | 880 | X-sparsity + Y-retrieval-memory | 0.72 | sparsity, retrieval, memory, routing |
| KCD_7CLUSTER | 756-823 | Lie-group equivariance macro | n/a | Lie, equivariance, SU(2), quiver, crystal |
| **KCD_R911** | 911 | X-elimination-theory + Y-token-routing | 0.71 | Resultant, Groebner, basis, routing |

**Feature pattern observable:**
- Slot distribution: {S05: 1, S07: 1, S13: 1, S15: 1, S16: 1, attention: 1} — broader
- step 14.6 functional similarity range (where computed): [0.71, 0.87] — **mean 0.78**, all above 0.7 threshold
- All have at least 2 KCD embedding_keys appearing in the candidate
- **The class boundary is sharp**: SURVIVES sim ≤ 0.58; COLLIDES sim ≥ 0.71. Empty zone [0.58, 0.71] (E37 had R914 sim=0.58, R911 sim=0.71 — right at gap edges).

### 1.3 Why this matters for v19

19 labeled examples (13 positive + 6 negative) at a sharp feature boundary is **exactly the regime where a small learned classifier can outperform a fixed rule**:
- The 0.58/0.71 gap is wide enough to provide robust margin training.
- Embedding features (Jaccard against KCD vocab, slot, citation_set) are low-dimensional and discrete.
- Logistic regression with ~5 features and 19 examples is over-determined enough to avoid overfit (degrees of freedom: 19 − 5 = 14, well above 0).
- Cross-validation with step 14.6 (already-running) provides held-out test signal every epoch.

The v17 analysis dismissed this as "too small" (it had 5 + 7 = 12). With **19 examples (+58%)** and a clearer boundary, the training regime is materially better.

---

## 2. v18 E37 failure-mode anatomy — what stale-drop missed

### 2.1 R911 (ANCHOR_R866 neighborhood → EXTERNAL_COLLISION)

The candidate "Resultant-Groebner-basis token routing" was generated at distance 0.45 from ANCHOR_R866 (Bezout-resultant routing). It survived step 05.5 (KCD had no elimination-theory entries pre-E37), step 13.5 (REBUTTED), step 14 (FIRED), and then step 14.6 returned sim=0.71 vs arXiv 2510.04532 — **just above the 0.70 collision threshold**.

**What was missed:** The Groebner-basis vocabulary is a known algebraic-geometry primitive used in MoE routing literature (2024-2025). A learned verifier trained on KCD_R827 (Bregman-divergence "reservoir-projection"-vocabulary) and KCD_R855 (Selberg-trace "L-function eigenvalue"-vocabulary) would have seen a pattern: candidates that introduce 2+ rare-math vocab words from a published-mechanism family (algebraic-geometry, in this case) have elevated collision risk.

**Stale-drop's reaction:** ANCHOR_R866's `epochs_since_yield` → 1. Two more zero-yield epochs needed before stale. Meanwhile, E38 will spend another 3-4 candidates on ANCHOR_R866's neighborhood, likely producing another near-collision.

**Predictive opportunity:** A learned classifier would have output `predicted_collision_prob` for R911 candidate at step 05.6 (a NEW gate before step 06 web_search). If ≥0.3, reject and regenerate. The candidate would never have reached step 06, saving the full pipeline budget.

### 2.2 R920 (ANCHOR_R895 neighborhood → FAIL_EMPIRICAL_ATTACK)

The candidate "Bounded-depth-circuit token routing" was generated at distance 0.40 from ANCHOR_R895 (Polynomial-time-bounded routing). Step 13.5 A1 (variant_equivalence) succeeded — the depth-bound is absorbed at small magnitude as a regularizer-like perturbation.

**What was missed:** ANCHOR_R895's "complexity-bounded" pattern is structurally fragile because complexity constraints become regularizers when relaxed (depth → ∞ recovers baseline; polynomial-time → arbitrary-time recovers baseline). The 6 known collisions don't include this pattern, but the 7 positive INVESTIGATIVE_SURVIVING anchors do encode "architectural module added vs. baseline" (S14/S15/S16/S20 module-add) which the complexity-bound pattern is *adjacent to but distinct from*. A learned verifier might encode that anchors whose mechanism_signature is a "constraint on" rather than "addition to" baseline have lower predicted INVESTIGATIVE probability.

**Stale-drop's reaction:** ANCHOR_R895's `epochs_since_yield` → 1. Two more zero-yield epochs needed.

**Self-play's would-be reaction:** Iterate the candidate: attack → rebut → re-attack → re-rebut. **This is exactly the failure case the v17 analysis warned about**: the candidate is *truly* architecturally collapsible; self-play would produce a fabricated rebuttal that wouldn't survive real review. Self-play converts FAIL_EMPIRICAL_ATTACK into a fake INVESTIGATIVE_SURVIVING, corrupting the corpus.

### 2.3 Aggregate: 8 of 25 (32%) of E37's selected_25 came from sterile anchors

- ANCHOR_R866 neighborhood: 3 selected (R910, R911, R912)
- ANCHOR_R895 neighborhood: 4 selected (R919, R920, R921, R924)
- 1 first-attempt KCD-rejected (R910) — caught
- 1 EXTERNAL_COLLISION (R911) — caught by step 14.6
- 1 FAIL_EMPIRICAL_ATTACK (R920) — caught by step 13.5
- 4 generic FAIL (no step 13 fire) — wasted budget

**32% of E37's selected_25 was spent on neighborhoods that produced 0 INVESTIGATIVE_SURVIVING.** Stale-drop will eventually fix this (E40 if both stay sterile), but the budget loss in E38-E39 is the bottleneck.

---

## 3. Mapping the bottleneck onto Swamy frameworks B and C

### 3.1 Framework B — Learned verifier (LEARNED FROM 19 LABELED EXAMPLES)

**Mechanism:** Train logistic regression at corpus-bootstrap on 6 KCD entries + 13 INVESTIGATIVE_SURVIVING. Features:
- f1: Jaccard similarity to nearest KCD embedding_keys (the existing v17 KCD metric)
- f2: count of rare-math vocabulary words shared with KCD entries (3+ → high risk)
- f3: slot ∈ {S14, S15, S16, S20} indicator (positive class hot zone)
- f4: frontier_seed_citation ∈ {YUSUN_TTT, YUSUN_HEAVY_TAIL_ENTROPIC, FOSTER_SHARPENING_VS_DISCOVERY, GAO_Q_RUBRIC, FOSTER_REP_DIVERSE_SAMPLING, YUSUN_REP_EXPLORATION} indicator
- f5: mechanism_signature contains "constraint on" / "bounded by" / "limit of" (negative class indicator from R895/R920 lesson)

Insert NEW step 05.6 between step 05.5 cascade and step 06 web_search. Compute `predicted_collision_prob = sigmoid(w₁·f1 + w₂·f2 + w₃·f3 + w₄·f4 + w₅·f5 + b)`. If `predicted_collision_prob ≥ 0.3`, reject candidate; regenerate up to 3 times.

Cross-validate against step 14.6: track `learned_verifier_agreement_rate` = agreement(predicted, actual_external_collision_outcome). Bootstrap weights on 19 examples; refit at end of each epoch.

**Why this addresses v18's bottleneck:**
1. **Pre-emptive**: rejects at step 05.6 *before* step 06 budget consumption. Stale-drop is reactive over 3 epochs; learned verifier is predictive per-candidate.
2. **Anchor productivity prediction**: an anchor whose 14-candidate neighborhood produces consistently high `predicted_collision_prob` is *predictively* sterile — the corpus can drop the anchor at E38 end instead of waiting to E40.
3. **Verifier accuracy on local-exploration candidates**: the v18 detector chain is rule-based (step 14.6 is a 4-axis hand-tuned rubric). A learned verifier built from corpus history is **the only feedback-driven verifier signal** in the pipeline. Adding it produces verifier learning, which v18 explicitly lacks.
4. **Cross-validation**: running alongside step 14.6 (not replacing it) lets the corpus measure agreement_rate. High agreement (≥0.85) validates the learned verifier; low agreement (≤0.65) flags a new failure mode the rule-based rubric missed.
5. **Data is just enough**: 19 examples with 5 features = 14 degrees of freedom; the [0.58, 0.71] sim gap provides clean margin training.

**Risks honestly acknowledged:**
- Logistic regression with 19 examples may overfit. Mitigation: low feature count (5), regularization (L2 with λ=1), bootstrap weights re-checked against step 14.6 each epoch.
- The 6 KCD entries are skewed toward "X-divergence" and "Lie-group" classes; a new collision family (e.g., elimination-theory like KCD_R911) may not be in the training distribution. Mitigation: feature f1 (Jaccard) generalizes across vocab; feature f2 (rare-math count) captures the *style* of collision regardless of specific class.
- Predicted_collision_prob ≥ 0.3 threshold may be too aggressive and reject good candidates. Mitigation: track `learned_verifier_false_positive_rate` (predicted collision, but step 14.6 says SURVIVES); if FPR > 0.2, raise threshold to 0.4.

### 3.2 Framework C — Self-play candidate refinement (REJECTED)

**Mechanism:** When step 13.5 attack succeeds, regenerate candidate to specifically rebut the load-bearing attack vector. Iterate attack → rebut → re-attack → re-rebut up to 3 times.

**Why this is rejected for v19:**
1. **E37 R920 proves the v17 analysis correct**: ANCHOR_R895's "complexity-bounded" pattern is *truly* architecturally collapsible. Self-play would generate variants that argue against the depth-bound collapse, but the underlying mechanism really does absorb into baseline at small magnitude. The "rebuttal" would be linguistic, not architectural. **The corpus would gain a fake INVESTIGATIVE_SURVIVING that fails on real review.**
2. **Attack rebuttal rate is already high**: E37 step 13.5 produced 7/8 post_attack_true (87.5%). Self-play would push this to ~95-100% — but the marginal addition would be exactly the architecturally-collapsible candidates that the protocol is *designed to reject*.
3. **Verifier learning bypassed**: self-play uses the same step 13.5 attack format iteratively, with no learned signal. The "learning" is the LLM's ability to argue back — not a corpus-feedback channel.
4. **Mitigates the wrong bottleneck**: self-play targets step 13.5 (already at 87.5%); v18's bottleneck is at step 14.6 (1 EXTERNAL_COLLISION at sim=0.71) and at anchor productivity (R895 sterility prediction). Self-play helps neither directly.

**Predicted v19 outcome under Framework C (if chosen):**
- INVESTIGATIVE_SURVIVING rises to 7/25 (+R920-style fabricated rebuttal). False-positive risk.
- Corpus corruption: future epochs' KCD or anchor_path may build on a candidate that doesn't survive real review.
- Score gain marginal: minimax_convergence_rate adds +1 to +3, but the +1 from a fabricated rebuttal *should* be discounted under honest accounting.

### 3.3 Summary — why B for v19

| Framework | Targets v18 bottleneck? | Predictive vs reactive? | Verifier learning? | Risk |
|---|:---:|:---:|:---:|:---:|
| **B: Learned verifier** | **YES (a + b)** | **predictive (rejects at step 05.6)** | **yes (re-train each epoch)** | LOW (cross-validates with step 14.6) |
| C: Self-play | NO (step 13.5 already at 87.5%) | reactive (only fires on attack success) | no (LLM-argument-only) | HIGH (fabricates rebuttals for architecturally-collapsible candidates) |

**v19 picks Framework B.**

---

## 4. Why Framework B is fundamentally different from v17's KCD pre-check

A reader might object: "v17 already has KCD pre-check at step 05.5 using Jaccard similarity. Is the learned verifier just a fancier KCD?"

**No, three structural differences:**

### 4.1 KCD pre-check is rule-based; learned verifier is fitted

KCD pre-check: if `jaccard(candidate.embedding_keys, kcd_entry.embedding_keys) > 0.5` for any kcd_entry → REJECT.

Learned verifier: predicted_collision_prob is a weighted combination of 5 features fitted on 19 labeled examples. The weights *encode the corpus structure*, not a hand-tuned threshold.

### 4.2 KCD pre-check is positive-only (collision avoidance); learned verifier is two-sided

KCD pre-check only knows what *to avoid*. It has no signal about what makes a candidate *likely to be INVESTIGATIVE_SURVIVING*. The learned verifier is trained on both classes — its weights reflect the *positive structure* of the 13 INVESTIGATIVE_SURVIVING anchors (slot ∈ {S14, S15, S16, S20}, frontier_seed in the "productive" set) as well as the negative collision structure.

### 4.3 KCD pre-check fires once; learned verifier fires + cross-validates

KCD pre-check at step 05.5 produces a verdict and exits. There's no downstream signal that says "KCD was right" or "KCD was wrong." Learned verifier fires at step 05.6, then **step 14.6 produces the ground truth label** on the candidates that pass through. The corpus accumulates `learned_verifier_agreement_rate` data and can re-fit weights, flag drift, or detect new collision classes.

The verifier learning loop is:
```
candidate → step 05.6 predicted_collision_prob → if reject, log + regen
                                                → if pass, continues
                                                → step 14.6 actual external_collision verdict
                                                → end-of-epoch: compute agreement
                                                → re-fit logistic regression weights on (19 + new labels)
```

This is the **first corpus feedback channel since v17's AFL** — and v17's AFL only writes to KCD (negative-class growth), not to a predictive model.

---

## 5. v18 to v19 score formula evolution

v18 added 5 new terms: active_anchor_count, mean_local_exploration_yield_rate, sub_anchors_promoted_count, −stale_anchor_drop_count, discovery_yield_rate.

v19 will add:
- `+ (learned_verifier_agreement_rate × 5)` — headline metric; rewards high agreement with step 14.6
- `+ (learned_verifier_pre_reject_count × 1)` — counts pre-step-06 rejections (saves budget; positive incentive)
- `− (learned_verifier_false_positive_rate × 3)` — penalizes over-rejection
- `+ (learned_verifier_true_positive_count × 2)` — rewards catches that step 14.6 confirms

These produce a balanced incentive: maximize agreement (×5), be willing to reject (×1), avoid over-rejection (×−3), reward confirmed catches (×2). At baseline agreement ≈ 0.85, expect net ~+5 to +9 from these terms.

---

## 6. Predictions for v19 E38 under Framework B

| Metric | v18 E37 actual | v19 E38 predicted | Mechanism |
|---|---:|---:|---|
| substantive_pass_count | 0 | 0 | structural saturation continues |
| INVESTIGATIVE_SURVIVING / 25 | 6 | **6-9** | learned verifier pre-rejects sterile candidates; budget shifts to productive anchors |
| Predicted_collision_prob ≥ 0.3 reject count (step 05.6) | n/a | **2-5** | E38 anchor-local candidates near ANCHOR_R866/R895 neighborhoods get flagged |
| learned_verifier_agreement_rate | n/a | **0.80-0.95** | step 14.6 confirms most predictions |
| learned_verifier_false_positive_rate | n/a | **0.05-0.20** | a few good candidates rejected; threshold tuning |
| learned_verifier_true_positive_count | n/a | **1-2** | catches near-threshold collisions (R911-style) before step 14.6 |
| ANCHOR_R866 + ANCHOR_R895 yield | 0 + 0 | **0 + 0** likely | learned verifier reinforces what stale-drop saw |
| Active anchor count at E38 end | 10 | **10** (still no stale; 2 will be at epochs_since_yield = 2) | E38 outcome |
| collision_addition_rate | 0.04 | **0.0-0.04** | learned verifier rejects pre-step-06; fewer collisions reach step 14.6 |
| KCD database size at E38 end | 6 | **6-7** | bounded growth |
| Score_v19 delta vs v18 | n/a | **+5 to +10** | new learned_verifier terms |
| p(no PASS \| 1% H₀) at N=1046 | n/a | ≈ 0.0000274 | matches user target |

---

## 7. Honest deviation acknowledgment for the Phase 1 analysis

This document is produced in main-context-direct mode (no Agent spawn). The 13-vs-6 labeled data analysis (§1.1, §1.2) is computed from `logs/known_collisions.json` and the cumulative INVESTIGATIVE_SURVIVING list across E34-E37 (rounds 834, 843, 863, 866, 883, 891, 895, 902, 905, 908, 914, 917, 922). The R911 + R920 failure-mode analysis (§2) is from rounds 911 + 920 file contents. The framework-mapping analysis (§3) reasons over v17's Phase 1 + v18 outcomes. No external sources are consulted; consistent with v18's honest deviation policy (<5 synthesized Agent spawns per epoch).

---

## 8. Conclusion

v18's bottleneck is twofold and Swamy-B-shaped: **(a) anchor productivity is reactive** — stale-drop takes 3 epochs while predictive signal could fire per-candidate; **(b) verifier accuracy has no learning channel** — the rule-based step 14.6 is the only signal source, with no feedback from accumulated corpus history. The 19 labeled examples (6 collisions + 13 INVESTIGATIVE_SURVIVING) form an under-utilized training set sitting at a sharp feature boundary (sim gap [0.58, 0.71]). Swamy framework B (learned verifier) introduces the first predictive collision-risk signal, with cross-validation against the unchanged step 14.6 rubric. Swamy framework C (self-play) is rejected because E37's R920 confirms the v17 analysis: iterating attack-rebut on architecturally-collapsible candidates fabricates surviving labels that don't reflect real distinguishability. **v19 picks Framework B**, with a NEW step 05.6 gate predicting collision_prob and a feedback channel measuring agreement with step 14.6.
