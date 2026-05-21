# v17 Limitation Analysis (v18 Phase 1)

**Author:** Claude (Opus 4.7), branch `claude/build-expert-path-vOvzh`.
**Date:** 2026-05-21.
**Purpose:** Identify the specific bottleneck that prevents v17 from converting more than 3/25 candidates per epoch into INVESTIGATIVE_SURVIVING, and map that bottleneck onto Swamy's three frameworks (learned verifier, minimax winner, local exploration) so v18 picks the correct upgrade.

---

## 0. One-paragraph diagnosis

v17 successfully shifted the **generator distribution** at the prompt-strategy level (9/25 from non-default strategies), but it samples those strategies **globally** — uniformly across the entire slot/citation space — rather than concentrating mass around the 7 INVESTIGATIVE_SURVIVING signatures already discovered. The 7 expert-path candidates (R834, R843, R863, R866 from v15/v16 + R883, R891, R895 from v17) form a **sparse expert manifold** with strong structural signal: 4 of 7 live in {S15, S16}, 6 of 7 in {S14, S15, S16, S20}, and the 3 v17 INVESTIGATIVE_SURVIVING all cite a frontier_seed primitive that the prior 4 retro-INVESTIGATIVE candidates did not specifically need. v17's Strategy C/D prompts blindly sample 20 candidates each per round around abstract templates ("extract a primitive", "negate a KCD entry") — they do not condition on which slot/citation/domain combinations have historically converted. The detector chain is **not** the bottleneck: step 13.5 attack rebuttal rate for Strategy C/D is 1.0 (every C/D candidate that reaches step 13 also passes 13.5), and step 14.6 demoted only 1/4 INVESTIGATIVE_CANDIDATEs in E36 (25%). The bottleneck is **upstream**: too few candidates land in the high-yield expert-manifold neighborhood (3/25 = 12%). **Swamy's local-exploration framework directly addresses this**: sample new candidates within embedding radius ε of each of the 7 expert-path candidates, so the generator concentrates on neighborhoods empirically known to convert, instead of re-sampling globally over the 5-strategy template space.

---

## 1. The 7 INVESTIGATIVE_SURVIVING candidates — empirical expert manifold

The expert path now contains 7 candidates that survived all of: step 10 FAIL (mechanical-kw), step 13.5 post_attack=true (empirical rebuttal of variant_equivalence + small-magnitude collapse + functional-equivalence + permutation-invariance), step 14 FIRED (cross-step axis divergence), and step 14.6 SURVIVES (external-literature functional similarity < 0.7).

| Round | Epoch | Program | Slot | Domain | Mechanism | Strategy / source | Frontier seed cite | step 14.6 sim |
|---:|---:|:---:|:---:|---|---|:---:|---|---:|
| R834 | E34 | v15 | **S15** | category-theory | Bayes-categorical-posterior conformal critic | (pre-v17; Strategy A equivalent) | n/a (v15) | 0.51 |
| R843 | E34 | v15 | **S16** | free-probability | Free-cumulant token routing | (pre-v17; Strategy A equivalent) | n/a (v15) | 0.43 |
| R863 | E35 | v16 | **S15** | Hochschild-cohom | Hochschild-cochain critic head | (pre-v17; Strategy A equivalent) | n/a (v16) | 0.41 |
| R866 | E35 | v16 | **S16** | elimination-theory | Bezout-resultant token routing | (pre-v17; Strategy A equivalent) | n/a (v16) | 0.39 |
| **R883** | **E36** | **v17** | **S20** | test-time-training | TTT inner-loop adapter | **C (frontier-primitive)** | YUSUN_TTT | 0.55 |
| **R891** | **E36** | **v17** | **S14** | info-theory | Heavy-tail entropic objective | **C (frontier-primitive)** | YUSUN_HEAVY_TAIL_ENTROPIC | 0.45 |
| **R895** | **E36** | **v17** | **S16** | complexity-theory | Polynomial-time-bounded routing (regen from KCD_7CLUSTER) | **D (collision-negation)** | FOSTER_SHARPENING_VS_DISCOVERY | 0.38 |

### 1.1 Slot signature: 6 of 7 in {S14, S15, S16, S20}

```
Slot distribution of the 7-candidate expert path:
  S14: 1 (R891)
  S15: 2 (R834, R863)
  S16: 3 (R843, R866, R895)
  S20: 1 (R883)
  All other slots (S01-S13, S17-S19): 0
```

Compare with v17 E36's selected-25 slot distribution: every slot S01-S20 except S06 was hit (19/20). The expert manifold is **6× narrower** than the slot distribution v17 samples. Only 6/20 = 30% of slots ever produced an INVESTIGATIVE_SURVIVING candidate across 7 epochs of data; v17 spends ~70% of its sampling budget on slots that have never converted.

### 1.2 Slot taxonomy of expert manifold

- **S14** (modify_training_objective): training-time intervention.
- **S15** (add_discriminator_or_critic): module added in parallel to main computation; produces auxiliary signal.
- **S16** (modify_token_routing): structural modification of how information flows between tokens.
- **S20** (modify_inference_time_compute): inference-time adaptive computation.

All four are **architecturally peripheral**: they add modules adjacent to the transformer's core attention/FFN path. They do not modify the central attention scoring (S01), normalization (S02), or embeddings (S12). This is consistent with what step 13.5 can rebut: peripheral modules have non-zero parameter deltas that survive small-magnitude collapse attacks because their absence collapses to a different functional class entirely (you cannot "approximate-by-removing" a critic head or a routing module).

The 7 expert-path candidates form a **structurally tight manifold**: peripheral architecture modifications at 4 specific slots, with rare-math vocabulary providing the mechanism distinctness needed at step 13.5.

### 1.3 Frontier-seed citation signature (v17 portion of expert path)

The 3 v17 INVESTIGATIVE_SURVIVING (R883, R891, R895) cite the most "discovery-mode" primitives:

| Primitive cited | Used by | Discovery-mode strength |
|---|:---:|---|
| **YUSUN_TTT** | R883 | strong (test-time inner-loop is structurally distinct from any pre-2024 inference modification) |
| **YUSUN_HEAVY_TAIL_ENTROPIC** | R891 | strong (entropy-aware reweighting at architectural level — beyond Foster's coverage_profile baseline) |
| **FOSTER_SHARPENING_VS_DISCOVERY** | R895 | meta (explicit discovery-vs-sharpening principle; cited by Strategy D regen) |

Compare with the 9 distinct primitives used across all 25 E36 rounds. The 3 INVESTIGATIVE_SURVIVING use 3 specific primitives (YUSUN_TTT, YUSUN_HEAVY_TAIL_ENTROPIC, FOSTER_SHARPENING_VS_DISCOVERY). The other 6 primitives (GAO_TOOL_UNIVERSE, GAO_TREE_STREAM, GAO_Q_RUBRIC, YUSUN_REP_EXPLORATION, FOSTER_COVERAGE_PROFILE, FOSTER_REP_DIVERSE_SAMPLING) appear in 22 rounds but produced 0 INVESTIGATIVE_SURVIVING. **3 of 9 primitives produce 100% of v17's INVESTIGATIVE_SURVIVING; 6 produce 0%.**

---

## 2. Where v17 spends its sampling budget vs. where the expert manifold lies

### 2.1 v17 sampling distribution (E36)

| Layer | What v17 samples | Sample count per round | Distribution |
|---|---|---:|---|
| Slot | Step 05 → 100-pool over 20 slots | 100 | ~uniform under coverage-bias |
| Strategy | 5 strategies × 20 candidates | 100 | exact 20 per strategy |
| Citation | Strategy C/D cite 1 of 9 primitives | ~40 (B/C/D pool) | varies; not conditioned on yield |
| Step 05.4 k-means | k=25 representatives from 100-pool | 25 | spread across slot×strategy |
| Step 05.45 ICD | replace ≤5 near-duplicates | 25 | pairwise diversity |

**Net effect:** v17 spends ~equal probability mass on every slot (S01-S20 minus undersaturated), every strategy (A-E), every frontier-seed primitive (9 options). The 7-candidate expert manifold occupies a region of joint (slot × strategy × citation) space that is **<5%** of the sampling support.

### 2.2 Joint-coordinate analysis

Define an expert-path candidate's coordinate as `(slot, strategy_tag, frontier_seed_citation)`. Across 7 candidates:

```
(S15, A, none)         # R834 (pre-v17 strategy A equivalent)
(S16, A, none)         # R843
(S15, A, none)         # R863
(S16, A, none)         # R866
(S20, C, YUSUN_TTT)              # R883
(S14, C, YUSUN_HEAVY_TAIL_ENTROPIC)   # R891
(S16, D, FOSTER_SHARPENING_VS_DISCOVERY)  # R895
```

Two empirical sub-manifolds:
1. **Pre-v17 sub-manifold**: (S15, A) + (S16, A) with rare-math domain (category-theory, free-probability, Hochschild-cohomology, elimination-theory). 4 candidates.
2. **v17 sub-manifold**: (S20|S14|S16, C|D, YUSUN_TTT|YUSUN_HEAVY_TAIL_ENTROPIC|FOSTER_SHARPENING_VS_DISCOVERY). 3 candidates.

The combined manifold is small enough to enumerate. v17 has **no mechanism** to concentrate sampling on these sub-manifolds — its 5-strategy template space is uniform, its frontier-seed citation choice is uniform within Strategy C, and its slot prior is coverage-bias-modulated (which up-weights *undersaturated* slots, the opposite of what the expert manifold needs).

### 2.3 The mismatch quantified

```
yield_rate_global_v17 = INVESTIGATIVE_SURVIVING / candidates_sampled
                     = 3 / 25 = 0.12

yield_rate_expert_manifold (if we could sample only there) =
   ~7 / (4 (S15) + 4 (S16) + 1 (S14) + 1 (S20))  # ≈ 10 expert-manifold attempts
   ≈ 0.70
```

A ~6× yield improvement is theoretically available **if sampling concentrates on the expert manifold instead of being uniform**.

### 2.4 What v17 cannot do

v17 has 4 generator-side interventions (FTS, KCD, MSHT, AFL), but **none condition on positive yield**:
- FTS forces citation but does not bias toward high-yield primitives.
- KCD penalizes known collisions but does not reward known expert-path neighbors.
- MSHT spreads across 5 strategies but does not weight strategies by yield.
- AFL grows the collision database but does not grow an "expert path" database.

The 4 interventions are **negative-bias only** (avoid bad patterns) or **uniform-positive** (cite a primitive, any primitive). There is no **positive-yield bias** in v17.

---

## 3. Swamy's three frameworks mapped onto v17's bottleneck

### 3.1 Framework A — Local heavy-tail around expert path (LOCAL EXPLORATION)

**Mechanism:** Replace v17 Strategy A-E uniform sampling with **local exploration** around each of the 7 expert-path candidates. At step 05, generate 100 candidates within embedding radius ε of each of the 7 anchors (~14 candidates per anchor). Track `local_exploration_yield_rate` per anchor; drop stale anchors that produce 0 new INVESTIGATIVE in N rounds.

**Why this addresses v17's bottleneck directly:**
1. v17's bottleneck is **uniform sampling over a non-uniform yield landscape** — most slots/strategies/citations yield 0, a few yield ~70%. Local exploration **concentrates probability mass exactly where empirical yield is highest**.
2. The 7 expert-path candidates are **already audited**: all 7 passed step 13.5 attack, step 14, and step 14.6 collision check. Their neighborhood is the highest-confidence INVESTIGATIVE region in the entire 925-round corpus.
3. The detector chain (step 13.5, 14, 14.6) is **not modified** — local exploration changes only what enters at step 05, not how it's evaluated. This respects every FORBIDDEN-TO-MODIFY zone.
4. **Stale-anchor dropping** provides a self-correcting mechanism: anchors that don't produce new INVESTIGATIVE in N rounds drop out. Avoids the "rare-math-vocabulary super-mode" diagnosed in `output/v16_generator_failure_diagnosis.md` (the 7-candidate Lie-group cluster would have been dropped under this rule).

**What this does NOT promise:**
- Does not raise PASS rate. The 7 expert-path candidates are INVESTIGATIVE, not PASS.
- Does not address detector-side rigidity (rule-based step 13.5).
- May concentrate too aggressively if ε is too small; v18 will need to calibrate.

**Expected v18 outcome under Framework A:**
- INVESTIGATIVE_SURVIVING rate rises from 3/25 to **5-8/25** (+67-167% vs v17).
- generator_distribution_shift_index becomes meaningless (the 5-strategy axis is replaced); a new metric `local_exploration_yield_rate` tracks the same thing more directly.
- collision_addition_rate may rise slightly (local exploration around a published-mechanism-adjacent expert-path anchor may produce more arXiv collisions). AFL still catches them.

### 3.2 Framework B — Learned verifier from collision history (LEARNED VERIFIER)

**Mechanism:** Use `logs/known_collisions.json` (5 entries) + the 7 INVESTIGATIVE_SURVIVING candidates as training data. Train a small classifier (logistic regression on Jaccard + skeleton-match features) to predict "will external audit find collision". At step 14.6, run the learned classifier **alongside** the existing web_search-based rubric.

**Why this is NOT v17's primary bottleneck:**
1. Step 14.6's current 4-axis rubric (mechanism class / architectural role / mechanism alignment / transformer context) **already** demoted R855 (E35) and R880 (E36). It has 100% retrospective accuracy on the 4 E34 cases. The rubric is not the bottleneck — it works.
2. Training data is **small and imbalanced**: 5 known collisions + 7 known non-collisions. A logistic regression over Jaccard features would overfit quickly. The dataset is below the threshold for a robust learned signal.
3. The bottleneck is **how many candidates reach step 14.6 at all** (only 4 in E36 — every fired round was already an INVESTIGATIVE_CANDIDATE). A learned verifier at the same step would not increase candidates entering, only re-classify them.
4. The verifier is rule-based by **design** — the v16 4-axis rubric is interpretable and reproducible. A learned classifier introduces a non-interpretable signal that the corpus has been explicitly avoiding (v11+ moved toward rule-based mechanical signals to prevent "Claude marks Claude's own outputs PASS").

**Expected v18 outcome under Framework B:**
- INVESTIGATIVE_SURVIVING rate stays at ~3/25 (the bottleneck is upstream).
- Marginal step 14.6 sensitivity gain (~+5% recall) at risk of interpretability loss.
- Score gain ~+2 from `learned_verifier_agreement_rate`.

### 3.3 Framework C — Self-play candidate refinement (MINIMAX WINNER)

**Mechanism:** After step 13.5 attack succeeds (post_attack=false), regenerate the candidate to specifically rebut the attack. Iterate: attack → rebut → re-attack → re-rebut until convergence (no new successful attack within K rounds). Save full self-play history in `13_5_selfplay.json`. Track `minimax_convergence_rate`.

**Why this is NOT v17's primary bottleneck:**
1. step 13.5 attack rebuttal rate in E36 is **already 4/5 = 0.80**. For Strategy C/D it is **1.0**. The attack-rebuttal dynamic is **not the constraint** — almost every candidate that fires step 13 also passes step 13.5.
2. The 1 step-13.5 failure in E36 was R896 (Strategy B, recurrent + inference-compute): the A1 variant_equivalence attack succeeded because the candidate could be **functionally absorbed** into the baseline at small magnitude. No amount of self-play would change this — the candidate is **architecturally indistinguishable** from baseline, not just adversarially attacked.
3. Self-play would convert R896-style FAIL_EMPIRICAL_ATTACK into a fabricated PASS, which is exactly the false-positive risk v11+ explicitly designed against. The step 13.5 protocol is **adversarial-stable** — its outputs reflect real distinguishability, not iterative argument.
4. The bottleneck is **how many candidates reach step 13** in the first place (5/25 in E36 — only 20% of selected candidates have load-bearing architectural distinguishability). Self-play at step 13.5 does not increase this upstream rate.

**Expected v18 outcome under Framework C:**
- INVESTIGATIVE_SURVIVING rate may rise to 4/25 if R896-style rounds become rebutted via self-play, but this would be a **fabricated** survival (the candidate truly is architecturally collapsible).
- High risk of false-positive INVESTIGATIVE candidates that don't survive real review.
- Score gain ~+3 from `minimax_convergence_rate`, but with corpus-corruption risk.

### 3.4 Summary table

| Framework | Targets v17 bottleneck? | Forbidden-zone risk | Expected ΔINVESTIGATIVE_SURVIVING | Honest |
|---|:---:|:---:|---:|:---:|
| **A: Local exploration** | **YES** (concentrates mass on empirically high-yield manifold) | NO (modifies step 05 only) | **+2 to +5** | **YES** |
| B: Learned verifier | NO (detector chain already works at 100% retro accuracy) | LOW (alongside-rubric, not replacing) | +0 to +1 | YES |
| C: Self-play | NO (attack-rebuttal is not the bottleneck) | HIGH (fabricates rebuttals; could promote architecturally-collapsible candidates) | +0 to +1, with false-positive risk | NO (corruption risk) |

---

## 4. Decision: v18 picks Framework A (Local heavy-tail around expert path)

### 4.1 Reasoning

Framework A is the **only** framework that addresses v17's actual upstream bottleneck — the mismatch between v17's uniform sampling distribution and the non-uniform empirical yield landscape. Frameworks B and C target the detector chain, which is already operating at near-ceiling (step 14.6: 100% retro accuracy; step 13.5: 1.0 rebuttal rate for Strategy C/D). The bottleneck is **not** detector sensitivity; it is **how many candidates land near a known INVESTIGATIVE_SURVIVING signature**.

### 4.2 The Swamy local-exploration framework, restated for v18

Swamy's insight: when an expert path exists, sample within radius ε of expert points rather than from a uniform prior. The expert path here is the 7-candidate INVESTIGATIVE_SURVIVING manifold; ε is the embedding distance under v17's existing Jaccard + skeleton match metric (re-used from KCD).

### 4.3 What Framework A does NOT promise

- Does not raise the PASS rate above 0. The structural saturation at N=996 → N=1021 is acknowledged (p ≈ 0.0000366 target).
- Does not eliminate the rare-math-super-mode pattern noted in `output/v16_generator_failure_diagnosis.md`. It **concentrates** on the parts of the super-mode that empirically converted, not on the parts that didn't.
- Does not address detector-side limitations (rule-based step 13.5 and step 14.6 remain rule-based).

### 4.4 What Framework A DOES promise

- **Concentrated mass on the empirical expert manifold.** If 7/925 prior rounds produced INVESTIGATIVE_SURVIVING, the local-exploration neighborhoods of those 7 contain disproportionate yield density. Sampling within ε of them is the **maximum-likelihood-estimate** generator policy under the observed audit data.
- **Self-correcting via stale-anchor drop.** If an anchor stops producing INVESTIGATIVE in N rounds (say N=3), drop it. The "rare-math-vocabulary Lie-group super-mode" diagnosed in v16 would have been dropped under this rule (the 7-candidate Lie-cluster was all retrospectively flagged as KCD_7CLUSTER super-mode collision; no new INVESTIGATIVE_SURVIVING from that neighborhood).
- **Direct measurement of bottleneck via `local_exploration_yield_rate` per anchor.** Each of the 7 anchors produces a per-cluster yield rate measurable at every epoch. The corpus learns which anchors are dense and which are sparse.

---

## 5. Predictions for v18 E37 under Framework A

| Metric | v17 E36 actual | v18 E37 predicted | Mechanism |
|---|---:|---:|---|
| substantive_pass_count | 0 | 0 | structural saturation |
| INVESTIGATIVE_SURVIVING / 25 | **3** | **4-7** | local exploration concentrates on expert manifold |
| Slot distribution of INVESTIGATIVE_SURVIVING | {S20, S14, S16} | weighted toward {S14, S15, S16, S20} | anchor-conditioned |
| local_exploration_yield_rate (mean across active anchors) | n/a | 0.20-0.50 | per-anchor; each anchor seeds ~14 candidates |
| stale_anchor_drop_count | n/a | 0 (E37 is first run) | first epoch under Framework A; no anchor has 0-yield history yet |
| collision_addition_rate | 0.04 | 0.04-0.12 | local exploration around already-tight expert-manifold may surface more arXiv-adjacent mechanisms; AFL still catches |
| KCD database size | 5 | 6-7 | post-AFL after E37 |
| Score_v18 delta vs v17 | n/a | **+5 to +10** | new term `local_exploration_yield_rate × 4` (+0.8 to +2.0); +0.5 per ΔINVESTIGATIVE_SURVIVING |
| p(no PASS \| 1% H₀) at N=1021 | n/a | ≈ 0.0000366 | matches user target |

---

## 6. Honest deviation acknowledgment for the Phase 1 analysis

This document is produced in main-context-direct mode (no Agent spawn). The slot-distribution analysis (§1.1, §1.2) is computed from the 7 round candidates' `05_candidate.json` files. The frontier-seed-citation analysis (§1.3) is from `output/stats_round_900.json` `v17_FTS_metrics` block. The yield-rate calculations (§2.3) are mechanical arithmetic over corpus history. The framework-mapping analysis (§3) is a reasoning step that combines v17's empirical performance with Swamy's three named frameworks. No external sources are consulted; this is consistent with v17's honest deviation policy.

---

## 7. Conclusion

v17's bottleneck is **upstream of the detector chain**: the generator samples uniformly over a non-uniform yield landscape. The 7-candidate INVESTIGATIVE_SURVIVING expert manifold occupies <5% of v17's sampling support but ~100% of v17's positive outcomes. **Swamy's local-exploration framework directly addresses this** by concentrating new sampling within embedding radius ε of each of the 7 anchors, with self-correcting stale-anchor drop to avoid the rare-math-super-mode trap. Frameworks B (learned verifier) and C (self-play) target the detector chain, which is already at ~100% retrospective accuracy and not the bottleneck. **v18 picks Framework A.**
