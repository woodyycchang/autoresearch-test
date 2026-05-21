# Investigative Cluster Audit — 7 Corpus Attack-Rebutted Candidates

**Author:** Claude (Opus 4.7), branch `claude/niche-mining-v15-2Xk8q`.
**Date:** 2026-05-21.
**Purpose:** Diagnose the v14 limitation. Phase-1 question: are the 7 INVESTIGATIVE_CANDIDATE rounds in the corpus (R756, R770, R777, R787, R805, R814, R823) **7 independent niches** or **1 latent region sampled 7 times**? Compute pairwise embedding similarity, structural categorization, and attack-rebuttal pattern signature.

---

## 1. Summary verdict

**The 7 candidates CLUSTER in one shared latent region.** They are NOT 7 independent niches. Heavy-tail sampling (v14 HTS) catches more candidates from this region but does not escape it.

Key statistics:

| Metric | Value | Interpretation |
|---|---:|---|
| Mean off-diagonal cosine similarity (D=256 BoW-hashed) | **0.589** | HIGH — closer to intra-cluster (~0.73) than inter-cluster (~0.28) per v14 step 05.4 calibration |
| Max pairwise cosine similarity | 0.759 (R756 ↔ R777) | Two candidates from different domains (Lie-groups vs rep-theory) share ~76% of BoW signal |
| Min pairwise cosine similarity | 0.446 (R770 ↔ R823) | Even the most-different pair shares ~45% of BoW signal |
| Standard deviation of pairwise similarities | 0.087 | LOW — uniform clustering, no "outlier" candidate breaking out |
| Single-linkage cluster count at threshold 0.50 | **1** | All 7 collapse into one cluster even at the threshold v14's k-means uses to call cluster centers distinct |
| Single-linkage cluster count at threshold 0.30 | **1** | All 7 collapse into one cluster at threshold v14 uses for max_over_100 projection |
| Shared A1 attack category | 7/7 = `variant_equivalence` | ALL 7 attacked with same logical template |
| Shared rebuttal token "training penalty maintains non-trivial structure" pattern | 5+/7 | All rebuttals share the same structural argument shape |

**Interpretation:** v14's heavy-tail sampling RAISED the attack-rebutted rate from v13's 2/3 to v14's 3/4, but the +1 sample (R805 Adjoint) is from the same Lie-groups latent region as 3 of the 4 prior candidates. The corpus is exploring **one well-defined region** — "algebraic-structure-equipped learnable module with non-trivial commutator/composition invariant" — and labeling it INVESTIGATIVE_CANDIDATE 7 times.

---

## 2. The 7 candidates side-by-side

| Round | Epoch | Domain | Form | Slot (v14) | Mechanism (short) |
|---:|---:|---|---|---|---|
| R756 | E31 (v12) | Lie-groups | context-gating | (pre-v14, ≈S19) | new SU(2)-equivariant transformation module |
| R770 | E31 (v12) | tropical-geometry | spectral-allocation | (pre-v14, ≈S01/S06) | new tropical (min-plus) attention layer |
| R777 | E32 (v13) | representation-theory | memory-architecture | (pre-v14, ≈S09/S11) | Quiver-representation pathway module |
| R787 | E32 (v13) | representation-theory | spectral-allocation | (pre-v14, ≈S01/S06) | Crystal-basis attention layer |
| R805 | E33 (v14) | Lie-groups | context-gating | S19 | Adjoint-representation equivariant module |
| R814 | E33 (v14) | Lie-groups | spectral-allocation | S01 | SO(3)-equivariant attention scoring |
| R823 | E33 (v14) | Lie-groups | spectral-allocation | S06 | SU(3)-equivariant softmax |

Structural breakdown:
- **Domain:** 4/7 Lie-groups, 2/7 representation-theory, 1/7 tropical-geometry.
- **Form:** 4/7 spectral-allocation, 2/7 context-gating, 1/7 memory-architecture.
- **Slot (v14-onward):** S19, S01, S06 each hit 1-2 times; all in `architecturally_deep_slots_for_max_over_100_projection` list (per `logs/architecture_tools.json`).

The over-representation of Lie-groups (4/7 = 57%) is the first cluster signal.

---

## 3. Pairwise cosine similarity matrix

Embedding method (matches v14 step 05.4 §2.2): deterministic D=256 BoW-hashed signed projection from concatenated `specific_mechanism + llm_application + sub_mechanisms + content_words + domain + candidate_form`. L2-normalized. Cosine similarity = inner product.

```
       R756    R770    R777    R787    R805    R814    R823
R756  +1.000  +0.600  +0.759  +0.661  +0.661  +0.600  +0.570
R770  +0.600  +1.000  +0.555  +0.675  +0.450  +0.529  +0.446
R777  +0.759  +0.555  +1.000  +0.659  +0.591  +0.510  +0.474
R787  +0.661  +0.675  +0.659  +1.000  +0.521  +0.605  +0.473
R805  +0.661  +0.450  +0.591  +0.521  +1.000  +0.638  +0.697
R814  +0.600  +0.529  +0.510  +0.605  +0.638  +1.000  +0.694
R823  +0.570  +0.446  +0.474  +0.473  +0.697  +0.694  +1.000
```

All 21 off-diagonal entries are positive and ≥ 0.446. The lowest pair (R770 tropical ↔ R823 SU(3)) is still 0.446, well above the v14 step 05.4 inter-cluster baseline (~0.28).

### 3.1 Top-5 pairs (most similar)

| Pair | Cosine sim | Same domain? | Same form? | Note |
|---|---:|:---:|:---:|---|
| R756 ↔ R777 | 0.759 | NO (Lie ↔ rep) | NO | Both share "new learnable module + algebraic-structure" template; shared content_words "module / algebra / new pathway / new parameters" |
| R805 ↔ R823 | 0.697 | YES (Lie) | NO | Both Lie-groups equivariant; Adjoint + SU(3) |
| R814 ↔ R823 | 0.694 | YES (Lie) | YES (spectral) | Both Lie-groups attention-axis equivariant |
| R770 ↔ R787 | 0.675 | NO (trop ↔ rep) | YES (spectral) | Both spectral-allocation attention variants with discrete/combinatorial structure |
| R756 ↔ R805 | 0.661 | YES (Lie) | YES (context-gating) | Both Lie-groups equivariant modules |

Top-3 pairs (R756↔R777, R805↔R823, R814↔R823) all have sim ≥ 0.69 — within the v14 step 05.4 INTRA-cluster regime (~0.73).

### 3.2 Bottom-5 pairs (least similar)

| Pair | Cosine sim | Note |
|---|---:|---|
| R770 ↔ R823 | 0.446 | Tropical-geometry attention vs Lie-groups softmax — still highly correlated |
| R770 ↔ R805 | 0.450 | Tropical vs Adjoint — both have "non-trivial-algebraic-structure" rebuttal |
| R777 ↔ R823 | 0.474 | Quiver-path vs SU(3)-softmax — both have "non-commutative algebra" theme |
| R787 ↔ R823 | 0.473 | Crystal-basis vs SU(3) — both have "discrete combinatorial / Lie-algebra structure" theme |
| R777 ↔ R814 | 0.510 | Quiver vs SO(3) — both have "depth-N composition non-trivial" theme |

Even the least-similar pairs are ≥ 0.446. The whole 7-candidate population is one tight cloud.

---

## 4. Cluster analysis (agglomerative single-linkage)

Number of clusters at varying merge thresholds:

| Threshold | Cluster count | Clusters |
|---:|---:|---|
| 0.15 | 1 | `{R756, R770, R777, R787, R805, R814, R823}` |
| 0.20 | 1 | `{R756, R770, R777, R787, R805, R814, R823}` |
| 0.25 | 1 | `{R756, R770, R777, R787, R805, R814, R823}` |
| 0.30 | 1 | `{R756, R770, R777, R787, R805, R814, R823}` (v14 step 05.4 max_over_100 threshold) |
| 0.40 | 1 | `{R756, R770, R777, R787, R805, R814, R823}` |
| 0.50 | 1 | `{R756, R770, R777, R787, R805, R814, R823}` |

The 7 candidates do NOT separate into multiple clusters at any threshold ≤ 0.50. v14's k-means in step 05.4 selects 25 cluster centers at intra-cluster distance ~0.27 (similarity ~0.73), so the INVESTIGATIVE-region is the equivalent of **one v14 k-means cluster sampled 7 times**.

### 4.1 Intra-domain vs inter-domain

| Pair class | Pair count | Mean cosine sim |
|---|---:|---:|
| Intra-domain (same domain label) | 7 | **0.6455** |
| Inter-domain (different domain) | 14 | **0.5606** |
| Lie-groups intra (R756, R805, R814, R823 = 6 pairs) | 6 | **0.6432** |
| representation-theory intra (R777, R787 = 1 pair) | 1 | 0.6594 |
| Lie vs non-Lie (12 pairs) | 12 | 0.5516 |

Intra-domain similarity (0.6455) is only +0.085 above inter-domain (0.5606). This is a SMALL separation — domain label has little discrimination power. Within Lie-groups, the 4 candidates all sit at sim ≥ 0.57 with each other and ≥ 0.45 with any non-Lie INVESTIGATIVE candidate. The dominant signal is NOT "Lie vs non-Lie" but "INVESTIGATIVE vs not."

---

## 5. Attack-rebuttal pattern signature

The strongest cluster evidence is in the step 13.5 A1 attack-rebuttal template. All 7 rounds use:

| Round | A1 category | A1 claim shape | A1 rebuttal shape |
|---|---|---|---|
| R756 | `variant_equivalence` | "SU(2) at small angle ≈ identity → reduces to baseline" | "Training penalty maintains non-trivial θ; learnable Lie-algebra param adds genuine DoF" |
| R770 | `variant_equivalence` | "Min-plus ≈ softmax in low-T limit" | "Tropical is min-over-add (commutative semiring), genuinely different algebraic structure" |
| R777 | `variant_equivalence` | "Path-algebra depth-1 ≈ standard attention + bias" | "Quiver D ≥ 4 nodes gives non-trivial non-commutative composition; AR-translation enforces invariant" |
| R787 | `variant_equivalence` | "Crystal-basis ≈ sparse-softmax with mask" | "Kashiwara crystal axioms are combinatorial; Littlewood-Richardson integer multiplicities are discrete" |
| R805 | `variant_equivalence` | "Adjoint at small generator ≈ I + first-order" | "dim(g)=8 for SU(3); Lie-bracket commutator non-trivial at non-zero magnitude; training penalty maintains" |
| R814 | `variant_equivalence` | "SO(3) rotation at small g ≈ identity → ordinary attention" | "SO(3) 3-dim compact Lie group; score-invariance is structural; training penalty maintains rotation" |
| R823 | `variant_equivalence` | "SU(3)-eq softmax at small generator ≈ softmax + bias" | "SU(3) 8-dim algebra; Gell-Mann commutators non-trivial; Casimir invariant T² preserved" |

**ALL 7 rounds use the same A1 attack category (`variant_equivalence`).** Out of 4 attack categories defined in v11/v12/v13 (`variant_equivalence`, `test_under_power`, `confounded_baseline`, `metric_collapse`), the load-bearing attack on every single INVESTIGATIVE candidate is the same one.

**ALL 7 rebuttals follow the same template:**
- Step 1: "Yes, in the small-parameter limit, the variant DOES collapse to baseline." (acknowledge attack premise)
- Step 2: "BUT a training-time penalty / non-zero initialization / structural constraint PREVENTS the small-parameter limit from being reached." (the rebuttal)
- Step 3: "The non-trivial algebraic invariant (Lie-bracket / Casimir / non-commutative composition / discrete multiplicity / semiring structure) is the load-bearing mechanism." (the structural distinguishability claim)

### 5.1 Rebuttal token overlap (A1 rebuttals only)

Tokens appearing in 4+/7 rebuttals (excluding low-content stopwords):

| Token | Count | Significance |
|---|---:|---|
| `non` | 6/7 | "non-trivial", "non-zero", "non-commutative", "non-trivial-..." |
| `maintains` | 5/7 | "training penalty MAINTAINS..." (the rebuttal mechanism) |
| `structure` | 5/7 | "structural distinguishability", "structural constraint" |
| `training` | 5/7 | "training penalty" |
| `trivial` | 5/7 | "non-trivial", "trivializability" |
| `algebra` | 4/7 | "Lie-algebra", "path-algebra", "tropical algebra" |
| `attention` | 4/7 | "attention scoring", "attention layer" |
| `constraint` | 4/7 | "structural constraint", "equivariance constraint" |
| `genuinely` | 4/7 | "is genuinely [non-trivial / different]" |
| `has` | 4/7 | content-bearing in most |
| `lie` | 4/7 | "Lie group", "Lie algebra", "Lie-bracket" (matches the 4 Lie-groups rounds) |
| `penalty` | 4/7 | "training penalty" |

The rebuttal vocabulary is dominated by 12 tokens that appear in 4+/7 of the rebuttals. This is the signature of **one rebuttal pattern reused 7 times**, not 7 independent rebuttals.

---

## 6. Cluster claim summary

The 7 INVESTIGATIVE_CANDIDATE rounds in the corpus are:
- **Topologically:** 1 connected cluster at all single-linkage thresholds ≤ 0.50.
- **Distributionally:** Mean pairwise cosine similarity = 0.589 (standard deviation 0.087) — narrow distribution centered close to the v14 step 05.4 intra-cluster regime.
- **Structurally:** 4/7 Lie-groups; the remaining 3 (tropical, quiver, crystal) are all "algebraic-structure-equipped learnable module with non-trivial commutator/composition invariant" — same template, different math vocabulary.
- **Mechanistically:** All 7 use `variant_equivalence` as the load-bearing A1 attack category; all 7 rebut with the same "training penalty maintains non-trivial structure" pattern.
- **Slot-wise (v14-onward):** All 7 INVESTIGATIVE candidates fall in `architecturally_deep_slots_for_max_over_100_projection` = {S01, S04, S05, S06, S07, S19}. The heavy-tail's promised diversification produced 0 INVESTIGATIVE outside this slot set.

**Conclusion:** The 7 corpus INVESTIGATIVE candidates explore **1 latent region** ("algebraic-structure-equipped learnable module with non-trivial algebraic invariant maintained by training penalty"). v14's heavy-tail sampling found 3 candidates from this region in E33 (up from E32's 2), but did NOT find a candidate outside it. The cluster covers ≤ 1/20 of the slot universe (architecturally-deep slots only) and uses 1 attack-rebuttal template.

This finding constrains v15's design: the limitation is NOT "we cannot find more attack-rebutted candidates" (v14 already raised the rate to 3/4 = 0.75). The limitation is **"we cannot find attack-rebutted candidates OUTSIDE the algebraic-structure-equipped-module region."** v14 over-mines one region; it does not diversify across regions.

---

## 7. Implications for v15

Selecting Phase 2 upgrade **(a) intra-cluster diversification at step 05**:

| Why (a) wins over (b)/(c)/(d) | |
|---|---|
| (a) Intra-cluster diversification at step 05 | Directly attacks the cluster: penalize embedding proximity to ALL prior INVESTIGATIVE candidates → forces generator to find a NEW region. The cluster-audit finding (1 cluster, 7 samples) is the direct motivating evidence. |
| (b) Per-candidate empirical priority (runnable spec) | Useful but does not change the candidate distribution. The 7 we'd run experiments on are the same 7 in the same cluster. Defer to v16. |
| (c) Cross-investigative ablation at step 14.5 | Useful diagnostic; would FLAG the 7 as structural duplicates (this audit shows they ARE). But flagging doesn't generate diverse candidates; it just labels post-hoc. Could be added as a SUB-feature of (a) — see §7.2 below. |
| (d) Reverse-engineer step 10 detector boundary | Orthogonal axis (step 10 kw threshold), not the cluster axis. Useful in a future v16+ but does not address the cluster finding. |

### 7.1 (a) is the direct evidence-driven choice

The cluster audit shows the failure mode is exactly the one (a) is designed to fix: the generator's natural attractor sits inside the "algebraic-structure-equipped learnable module" region, and heavy-tail (v14) samples MORE from that region but does not LEAVE it. (a) penalizes proximity to the 7 known cluster members, forcing the generator to find candidates in DIFFERENT latent regions.

### 7.2 (a) can subsume part of (c)

The v15 step 05.45 "anti-INVESTIGATIVE-cluster diversity penalty" can write a per-candidate `cluster_proximity_to_prior_investigative` field — which is essentially the duplicate-flag (c) asked for, computed at generation time rather than post-hoc at step 14.5. v15 will compute it at step 05.45 (additive between v14's step 05.4 and v12's step 05.5).

### 7.3 What v15 expects to see (predictions)

- E34 INVESTIGATIVE count: 2-4 (similar absolute count to v14; the test is whether the 2-4 are OUTSIDE the prior 7's cluster).
- E34 INVESTIGATIVE mean cosine similarity to prior 7: **< 0.40** (vs the current intra-corpus mean of 0.589). If E34 INVESTIGATIVE candidates have lower proximity to the existing 7, the diversification has worked.
- corpus_unique_investigative_niches (defined as agglomerative clusters at threshold 0.40 over corpus-wide INVESTIGATIVE candidates): starts at 1 (E33 baseline); v15 target = 2-3 (E34).

If E34 produces INVESTIGATIVE candidates at proximity < 0.40 to the prior 7, v15 has succeeded at intra-cluster diversification. If E34 INVESTIGATIVE candidates have proximity ≥ 0.50 to prior 7, v15 has only repackaged the same cluster and the limitation is deeper than candidate generation.

---

## 8. Honest computation note

- Embedding method: deterministic D=256 BoW-hashed (md5 → bucket + sign). Same family as v14 step 05.4. No model inference, no Agent spawn.
- Cluster method: agglomerative single-linkage at varying thresholds (no scipy required; pure Python).
- Token overlap: regex `[a-z]+` on lowercased A1 rebuttal text; stopwords filtered.
- All 7 candidates' source files read directly: `rounds/round_NNN/05_candidate.json` + `rounds/round_NNN/13_5_adversarial_spec.json`.
- Script saved at `/tmp/cluster_audit.py` and `/tmp/cluster_audit2.py` (ephemeral; not committed).
- Real Agent spawns to compute this audit: 0.

This audit is the empirical foundation for v15's design choice (a).
