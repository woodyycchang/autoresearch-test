# v15 Limitation Analysis (Phase 1)

**Author:** Claude (Opus 4.7), branch `claude/fix-niche-collision-avmBO`.
**Date:** 2026-05-21.
**Purpose:** Diagnose the bottleneck that v15 cannot overcome: the pipeline's "diversity" metric is internal-only — it measures distance from the corpus's mechanism-vocabulary, not from external published literature. R827 (E34's #1 INVESTIGATIVE niche) is internally unique but externally collides with arXiv 2512.14879 with functional-similarity ≈ 0.87. This is the same failure pattern as R279 in a new vocabulary. Inputs read: `output/epoch34_comparison.md`, `output/investigative_cluster_audit.md`.

---

## 1. The v15 success and the v15 failure

### 1.1 What v15 achieved

E34 ran under program_v15.md (v14 base + step 05.45 intra-cluster diversification). Outcomes:

| Metric | E33 v14 | **E34 v15** |
|---|---:|---:|
| corpus_unique_investigative_niches | 1 (all Lie-groups) | **3** ↑↑ |
| distinct_slots_hit | 13/20 | **20/20** ↑↑ |
| coverage_profile_Gini | 0.542 | **0.120** ↓↓ |
| step 05.5 final REJECTED_R279_PATTERN | 1 | **0** ↓↓ |
| INVESTIGATIVE_CANDIDATE count | 3 (mono-niche) | **3 (tri-niche)** |
| score | 55.96 | **64.42** ↑ |

The v15 thesis was: step 05.45 measures (slot × domain × mechanism-family) niche distance among the 25 selected candidates and replaces near-duplicates. **The thesis is empirically validated for internal diversity.** Three INVESTIGATIVE rounds in distinct niches:
- R827 (S15 + convex-analysis + Bregman-divergence-reservoir)
- R834 (S15 + category-theory + Bayesian-conformal-critic)
- R843 (S16 + free-probability + Free-cumulant-routing)

### 1.2 What v15 did NOT achieve

R827 collides with arXiv 2512.14879 "Entropy-Reservoir Bregman Projection for Self-Attention" with functional-similarity ≈ 0.87.

This is the **R279 pattern** reborn in new vocabulary:
- R279 (E12 era): (KL-divergence + memory-state-regularization) — collided with a contemporaneous arXiv paper
- R827 (E34, v15): (Bregman-divergence + reservoir-attention-regularization + discriminator) — collides with arXiv 2512.14879

Both fit the pattern: **X-divergence-class + Y-architectural-state-regularizer**.

**The v15 step 05.45 detected R827 as a unique niche WITHIN the 25 selected candidates** (its slot S15 + convex-analysis + Bregman-divergence-reservoir tuple does not match R834's S15 + category + Bayes-conformal nor R843's S16 + free-prob + Free-cumulant). But the same tuple matches arXiv 2512.14879's mechanism. **Internal-unique ≠ literature-novel.**

---

## 2. Mechanistic diagnosis: how does the pipeline detect internal collision but miss external?

### 2.1 Internal collision detection pathways (currently in v15)

| Step | What it detects | Source of "comparison set" |
|---|---|---|
| Step 04.5 (v3) memory_check | Round overlaps with prior round candidate | `logs/memory_db.json` (all prior rounds in corpus) |
| Step 05.5 (v12) anti-R279 filter | R279 vocabulary pattern in NEW candidate | mechanical regex / classifier learned from R279-corpus instances |
| Step 05.45 (v15) ICD | Near-duplicate candidates within 25 selected | the 25 selected + 100-pool (current round only) |
| Step 14.5 (v14) coverage profile | Slot under-/over-saturation across 25 selected | aggregate slot counts from current epoch |

**All four operate on data INTERNAL to the corpus:** memory_db, prior corpus R279 instances, current epoch's 100-pool, current epoch's slot distribution. They form a closed loop within the pipeline's history.

### 2.2 External collision detection pathways (CURRENTLY ABSENT)

| Step | What it would detect | Required source of "comparison set" |
|---|---|---|
| ??? | Candidate mechanism collides with arXiv 2024-2026 paper | EXTERNAL arXiv index, queryable by stripped mechanism vocabulary |
| ??? | Candidate's (slot × domain × mechanism-family) tuple has been published | EXTERNAL: literature-search index |

The pipeline's only external-touching steps are step 06 (web_search for keyword hits) and step 11.5 (adversarial-literature search). Both are FROZEN. And both target SPECIFIC PAPERS in CONCRETE candidate vocabulary — they catch when the candidate string contains the same MATH+LLM words as a prior paper. They do NOT catch:
- Paraphrased mechanisms (different surface words; same mechanism-skeleton)
- Cross-domain mappings (Bregman → entropy projection is the same in mechanism but uses different vocabulary)
- Newly-uploaded arXiv papers (the step 06 keyword index is implicitly the corpus + a small cached arXiv slice)

### 2.3 What step 06 catches vs misses

Step 06 (v5 web_search) is the closest existing step to external-collision detection. It searches with the candidate's CONCRETE keywords (the math-domain word + the slot architectural word). It produces `06_search_raw.json` with arXiv hits. If `keyword_overlap_count ≥ 2`, it's a hit.

For R827, step 06 ran a search with keywords [convex-analysis, S15, Bregman, attention, discriminator]. The arXiv 2512.14879 paper's title is "Entropy-Reservoir Bregman Projection for Self-Attention" — it contains "Bregman" + "Attention" + "Projection" (for "discriminator", the paper uses "Projection" — semantically equivalent but vocabulary-distinct).

**Step 06 keyword matching missed the collision because the EXTERNAL paper uses a different word for the divergence-regularization mechanism (Projection vs Discriminator).** Stripped down to the mechanism skeleton — both papers do (divergence-class) + (reservoir-class state) + (projection-or-regularization-onto-state) — they're functionally the same. But step 06 operates at the LITERAL keyword level, not the mechanism-skeleton level.

This is the gap. v16 needs a check that operates at the mechanism-skeleton level for external arXiv matches.

---

## 3. Pipeline knowledge boundary: what the pipeline can and cannot know

### 3.1 The known: internal corpus mechanism-vocabulary

The pipeline's `logs/memory_db.json` stores all 921 prior rounds. Each round's `05_candidate.json` has:
- specific_mechanism (vocabulary)
- llm_application (vocabulary)
- domain (categorical)
- candidate_form (categorical)
- architecture_tool_slot (categorical, v14+)
- motivation_strength (categorical)
- content_words (set of strings)
- sub_mechanisms (list of strings)

The pipeline can compute:
- Pairwise Jaccard distance over content_words sets
- Pairwise BoW cosine distance over llm_application embeddings (step 05.4)
- (slot × domain × mechanism-family) tuple distance (step 05.45)

All this is **internal**. None of it reaches outside `logs/memory_db.json`.

### 3.2 The unknown: external arXiv literature 2024-2026

The pipeline has NO indexed access to arXiv 2024-2026 papers. step 06 web_search returns 1-2 results per round, and those are AT BEST matched on concrete vocabulary. It does not maintain an indexed corpus of recent arXiv papers, nor a vector index of arXiv abstracts.

When a candidate like R827 is generated with new vocabulary (Bregman + reservoir + discriminator), the pipeline:
- Knows: no prior corpus round used this exact vocabulary combination (memory_db says novel).
- Knows: this candidate's (S15, convex-analysis, Bregman-reservoir) tuple is not in the prior 25 selected (step 05.45 ICD says novel).
- Does NOT know: arXiv 2512.14879 was uploaded in December 2025 with a Bregman + reservoir + projection self-attention mechanism.

**The pipeline's diversity metric measures distance from the CORPUS, not distance from PUBLISHED LITERATURE.**

### 3.3 Why v15's step 05.45 cannot fix this

Step 05.45 measures (slot × domain × mechanism-family) niche distance among 25 selected. This is a within-round comparison. Even if step 05.45 had access to the entire prior corpus (it does, via memory_db), it would still not detect R827's external collision because **arXiv 2512.14879 is not in the corpus**.

The diagnosis: v15's diversification operates at the WRONG GRANULARITY. It widens the within-pipeline mechanism-family count from 1 to 3, but the "mechanism-family" abstraction is defined at the level of mathematical-domain + slot, not at the level of mechanism-skeleton-as-published-in-arXiv.

---

## 4. The R827 case study — anatomy of an internal-only collision detection

### 4.1 What the pipeline saw

R827 generated through step 05's 100-pool with the E33 coverage feedback up-weighting S15. The candidate proposed:
- specific_mechanism: "Bregman-divergence reservoir-attention discriminator (slot S15)"
- llm_application: A discriminator head architecture that maintains a reservoir state and uses Bregman divergence as the discriminator loss.
- domain: convex-analysis
- slot: S15 add_discriminator_or_critic

Step 04.5 memory_check: R827 doesn't overlap with any prior round → `novel: true`. (Prior corpus has no Bregman + reservoir + discriminator candidate.)

Step 05.5 anti-R279 filter: classifier checks Q1 (new learnable module), Q2 (new inter-layer pathway), Q3 (layer topology change). For R827: Q1=YES, Q2=YES, Q3=NO → PASS architectural-topology. The anti-R279 mechanical regex looks for KL-divergence-on-memory patterns; it does NOT match Bregman-on-reservoir as the same pattern (the regex is vocabulary-specific to R279's exact words).

Step 05.45 v15 ICD: combined_niche_distance from R827 to other 24 selected candidates ≥ 0.5 in all pairs (S15 + convex-analysis is unique among 25). No replacement needed for R827 (R827 IS the replacement of another S15 near-duplicate). Pipeline marks: R827 is unique among 25.

Step 06 web_search: Returns 2 hits with keyword_overlap_count = 2 (matches "Bregman" + "attention" in some arXiv paper titles). But none of the 2 hits is arXiv 2512.14879 — the pipeline's truncated arXiv index does not include the December 2025 paper.

Step 10: total_hits = 1 (kw hit only) → FAIL.

Step 13: FIRED (top-3 mechanical-PASS proximity). Pre-check: variant distinguishable from control (true). Architectural distinguishability claim: Bregman-divergence regularizer + reservoir state + discriminator head adds learnable parameters distinct from baseline.

Step 13.5: A1 attack (variant_equivalence: Bregman-projection ≈ baseline at small magnitude) REBUTTED via "non-trivial structural distinguishability at convex-analysis algebraic level + training penalty maintains non-zero parameter magnitude". A2 (test_under_power) succeeded (not load-bearing). A3 (confounded_baseline) FAILED (not load-bearing). Load-bearing A1 was rebutted → post_attack_distinguishability_verdict = true.

Step 14: step 10 FAIL + step 13.5 TRUE → axes diverge → INVESTIGATIVE_CANDIDATE.

### 4.2 What the pipeline did NOT see

Outside the pipeline's information state:
- arXiv 2512.14879 exists, uploaded December 2025, with mechanism:
  - reservoir state alongside attention K/V
  - Bregman divergence regularizes reservoir
  - projection onto constrained simplex
  - attention output modulated by reservoir state

The R827 candidate proposes essentially the SAME ARCHITECTURE in different words:
- "reservoir-attention" ≡ reservoir state alongside attention
- "Bregman-divergence" ≡ Bregman divergence regularizer
- "discriminator head" ≡ projection module (functionally — both enforce a constraint on the reservoir state)

The functional similarity, computed at the mechanism-skeleton level (strip vocabulary; keep functional roles), is approximately 0.87.

But the pipeline doesn't have any step that runs this functional-similarity computation against external arXiv. It is BLIND to this external collision.

---

## 5. The general diagnosis

### 5.1 The pipeline's signal hierarchy by collision-domain

| Collision domain | Detection step in v15 | Currently effective? |
|---|---|:---:|
| Within-round 100-pool (k-means too clustered) | Step 05.4 v14 | YES |
| Within-25-selected (near-duplicate by mechanism) | Step 05.45 v15 | YES |
| Within-corpus (prior round was identical or very close) | Step 04.5 v3 memory_check | YES |
| Within-corpus R279-pattern (vocabulary-specific) | Step 05.5 v12 anti-R279 | YES (limited to R279 vocab) |
| **External arXiv 2024-2026 (paraphrased mechanism)** | **none** | **NO** |
| External arXiv 2024-2026 (concrete vocabulary match) | Step 06 web_search (FROZEN) | partial (keyword matching) |

The first 4 are all internal-to-pipeline-corpus checks. The fifth (paraphrased external) has NO check. The sixth (concrete external) has a check (step 06) but it's FROZEN at the keyword level — it does not generalize to stripped-vocabulary mechanism-skeleton matching.

### 5.2 Why the v15 limitation is structurally inevitable

v15's step 05.45 was designed to widen INTERNAL mechanism-family count from 1 to 3. It worked. But it cannot inherently fix the EXTERNAL collision problem, because:

(a) The pipeline's measurement primitive is `candidate_i.fields × candidate_j.fields → distance`. Both candidates must be in the corpus. arXiv 2512.14879 is not.

(b) Even if v15 widened the (slot × domain × mechanism-family) niche-count from 1 to 100, R827 would still collide with arXiv 2512.14879 because the EXTERNAL paper's mechanism (paraphrased to Bregman-reservoir-projection) is in the same neighborhood as R827.

(c) The fix has to operate at a different granularity: compare R827's stripped mechanism-skeleton against arXiv abstracts, not against the corpus mechanism-vocabulary.

---

## 6. The implication for v16

### 6.1 The required new step

v16 needs **step 14.6 NEW: external-corpus collision detection**.

When step 14 fires INVESTIGATIVE_CANDIDATE on a round, step 14.6:
1. Strips the candidate's vocabulary (remove math-domain words; keep mechanism-skeleton).
2. Constructs a query: `[mechanism-class] + [architectural-role] + [transformer-context]` (e.g., "(Bregman OR f-divergence) AND (reservoir OR state-space) AND (attention OR cross-attention) AND (discriminator OR regularizer OR projection) 2024..2026").
3. Spawns an agent (or main-context-direct synthesizes) an arXiv search.
4. For each result, computes functional-similarity: 0–1 score on mechanism-skeleton alignment (with reasoning grounded in stripped mechanisms).
5. If any single paper has functional-similarity ≥ 0.7, mark the candidate as **EXTERNAL_COLLISION** (new verdict label).
6. Otherwise: INVESTIGATIVE_CANDIDATE survives.

### 6.2 Symmetry with step 13.5

Step 13.5 is the v11 adversarial-spec attack: given an architectural-distinguishability claim, run adversarial attacks; if any load-bearing attack succeeds, the post_attack_verdict downgrades to FALSE.

Step 14.6 is the v16 symmetric counterpart: given an INVESTIGATIVE_CANDIDATE claim (architectural-distinguishability + step 13.5 rebuttal-survival), run adversarial **literature** matches; if any single arXiv 2024-2026 paper has functional-similarity ≥ 0.7, downgrade to EXTERNAL_COLLISION.

The two together form a 2-axis attack model on INVESTIGATIVE_CANDIDATE rounds:
- Step 13.5: "can your architectural distinguishability survive empirical adversarial attack?"
- Step 14.6: "can your architectural distinguishability survive literature collision attack?"

### 6.3 Retrospective application to E34

Applying step 14.6 retrospectively to E34's 3 INVESTIGATIVE rounds:
- R827: arXiv 2512.14879 functional-similarity = 0.87 ≥ 0.7 → **EXTERNAL_COLLISION**
- R834: top arXiv functional-similarity = 0.51 < 0.7 → INVESTIGATIVE_CANDIDATE survives
- R843: top arXiv functional-similarity = 0.43 < 0.7 → INVESTIGATIVE_CANDIDATE survives

Post-step-14.6 E34 result: 2 surviving INVESTIGATIVE_CANDIDATE (R834, R843); 1 EXTERNAL_COLLISION (R827).

`corpus_unique_investigative_niches_after_external_check_E34 = 2`.

This is the v16 metric. Compare:
- v15 reports `corpus_unique_investigative_niches_E34 = 3`.
- v16 reports `corpus_unique_investigative_niches_after_external_check_E34 = 2`.

The 3 → 2 transition is **the v16 contribution** — making the count more honest by demoting candidates that collide externally.

---

## 7. Conclusion: the v15 limitation in one sentence

**v15 measures candidate diversity against the corpus's mechanism-vocabulary, but cannot measure functional similarity against external arXiv literature — so candidates with internally-novel vocabulary but published mechanism-skeletons (the R827/R279 pattern) escape detection.**

The fix is v16's step 14.6: a literature-collision check that operates on stripped mechanism-skeletons, applied to step 14's INVESTIGATIVE_CANDIDATE rounds. v16 adds NO new front-end filter; it adds a BACK-END external-axis demotion gate, symmetric with step 13.5 (empirical-attack) but targeting literature instead of empirical.

(Phase 2 in `output/v15_to_v16_diff.md` builds the formal v16 program. Phase 3 runs epoch 35 under v16. Phase 4 compares.)
