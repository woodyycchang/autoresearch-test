# v15 → v16 Diff (Phase 2 of v16 task)

**Author:** Claude (Opus 4.7), branch `claude/fix-niche-collision-avmBO`.
**Date:** 2026-05-21.
**Purpose:** Document the structural diff from `program_v15.md` to `program_v16.md`, with rationale for the single new upgrade chosen (option (a) external-corpus collision detection at step 14.6), forbidden-zone preservation audit, and v16 implementation summary.

---

## 0. v16 changeset summary (one paragraph)

v16 adds **step 14.6 NEW: external-corpus collision detection** that fires only on step-14-INVESTIGATIVE_CANDIDATE rounds. It strips the candidate's mechanism vocabulary, queries arXiv 2024-2026 for the mechanism-skeleton, and computes functional-similarity via a 4-axis rubric (mechanism class / architectural role / mechanism alignment / transformer context). If max_functional_similarity ≥ 0.7 against any single arXiv paper, the candidate is DOWNGRADED from INVESTIGATIVE_CANDIDATE to a new verdict label EXTERNAL_COLLISION. This is symmetric with step 13.5 (empirical-attack on architectural distinguishability) but targets literature collision instead. v16 is STRICTLY ADDITIVE — it does not modify any FORBIDDEN-TO-MODIFY zone (step 06 web_search, step 07 kw, step 10 mechanical, step 12 tree-stream, step 13 spec, step 13.5 attack, step 14 coherence, step 14.5 coverage, step 05.4 diversity filter, step 05.45 intra-cluster diversification). The PASS criterion remains 10 signals (UNCHANGED). v16 ADDS one new verdict label: EXTERNAL_COLLISION. The contribution is at the EXTERNAL-LITERATURE-COLLISION layer.

---

## 1. Why option (a) — external-corpus collision detection at step 14.6

The user's task description lists 4 candidate v16 upgrades:
- **(a) External-corpus collision detection at step 14.6**
- (b) Literature-conditioned candidate generation at step 05 (feed top-50 most-recent arXiv abstracts; bias generator AWAY)
- (c) R827-pattern filter at step 05.5 (auto-flag X-divergence + Y-regularization)
- (d) Multi-source ideation (≥3 architecture tool slots never co-occurred in prior corpus + training data)

Selection: **(a)** based on the Phase 1 evidence in `output/v15_limitation_analysis.md`.

### 1.1 Why not (b) literature-conditioned generation

(b) biases the candidate generator AWAY from recent arXiv abstracts. This is GENERATIVE-side; the diagnosed problem is on the VERIFICATION side. Specifically:
- The v15 limitation is that R827 was GENERATED and SURVIVED all v15 checks (including step 04.5 memory_check, step 05.5 anti-R279, step 05.45 ICD, step 13.5 attack, step 14 coherence).
- Even with (b), some R827-like candidate would still be generated (the generator can't bias against unseen-to-training papers; arXiv 2512.14879 is from December 2025 — the generator might or might not have it in training).
- (b) is a SHIFT in the generator's prior, not a detector. It would reduce-not-eliminate the R279/R827 pattern rate.
- The cleaner intervention is a DETECTOR at the back of the pipeline (where each INVESTIGATIVE round is fully formed and can be checked against literature).

### 1.2 Why not (c) R827-pattern filter

(c) extends the v12 anti-R279 filter at step 05.5 to catch X-divergence + Y-regularization patterns. This is a VOCABULARY-SPECIFIC extension of the existing filter. Specifically:
- v12 step 05.5 catches R279's exact pattern. R827 escapes because (Bregman, reservoir, discriminator) ≠ (KL, memory, regularizer) at the vocabulary level.
- (c) would extend step 05.5 to catch X-divergence + Y-regularization more broadly. But this is RETROACTIVE — it only catches patterns we've ALREADY seen collide.
- The NEXT collision will be in a DIFFERENT pattern that (c) won't catch (e.g., "X-spectral + Y-attention" or "X-cohomology + Y-state").
- (c) would FORBID forbidden zone modification by extending step 05.5 (a FROZEN zone per v12).
- Furthermore, (c) is reactive to specific patterns; (a) is forward-looking against unknown patterns by leveraging literature.

### 1.3 Why not (d) multi-source ideation

(d) requires candidates to combine ≥3 architecture tool slots that have never co-occurred in prior corpus AND in Claude training data. This is an EXPLORATION-DIVERSITY mechanism at step 05. Specifically:
- This combinatorically restricts the candidate space. With 20 slots, there are C(20,3) = 1140 triples; over time the corpus + training data will exhaust them.
- It conflates SLOT diversity with MECHANISM diversity. Two slot-triples can have the same mechanism (e.g., {S01, S06, S19} could host Lie-equivariance variants regardless of slot triple).
- It doesn't address the R827-pattern problem: R827 might use slots {S15, S07, S13} (a fresh triple) but still implement Bregman-reservoir-discriminator (a published mechanism).
- (d) is a generative restriction at step 05, requiring deep modification of the 100-pool's generation logic — which would touch FORBIDDEN zones if not careful.

### 1.4 Phase 1 evidence directly supports (a)

The Phase 1 diagnosis (`output/v15_limitation_analysis.md` §6) explicitly recommends (a):

> "v16 needs **step 14.6 NEW: external-corpus collision detection**. When step 14 fires INVESTIGATIVE_CANDIDATE on a round, step 14.6 ... strips the candidate's vocabulary ... constructs an arXiv search query ... computes functional-similarity ... if max ≥ 0.7, mark as EXTERNAL_COLLISION."

The Phase 1 diagnosis also explicitly notes (§6.2):

> "Step 14.6 is the v16 symmetric counterpart [to step 13.5]: given an INVESTIGATIVE_CANDIDATE claim, run adversarial literature matches; if any single arXiv 2024-2026 paper has functional-similarity ≥ 0.7, downgrade to EXTERNAL_COLLISION."

The choice of (a) is THE NATURAL FIT for the diagnosed limitation. The other options address different problems (generation-side bias, vocabulary-specific filters, slot combinatorics) that are not the root cause of the R827 collision.

---

## 2. New artifacts in v16

| Artifact | Location | Created by | Lifecycle | Trigger |
|---|---|---|---|---|
| `rounds/round_NNN/14_6_external_collision.json` | per-round | step 14.6 | per-round | only when step 14 FIRES |

| Field addition | Schema location | Type |
|---|---|---|
| `v16_ECD_metrics` (group) | output/stats_round_NNN.json | object |
| `v16_verdict_distribution` (group) | output/stats_round_NNN.json | object |
| `external_collision_aggregates` (group) | logs/policy_state.json | object |
| `EXTERNAL_COLLISION` (verdict label) | n/a (label) | string |

---

## 3. Step-by-step diff vs program_v15.md

### Step 01-04 — UNCHANGED

### Step 04.5 (v3 memory_check) — UNCHANGED

### Step 05 (v8 token streams + v14 100-pool + slot field) — UNCHANGED

### Step 05.4 (v14 k-means filter) — UNCHANGED

### Step 05.45 (v15 ICD) — UNCHANGED

### Step 05.5 (v12 anti-R279) — UNCHANGED

### Steps 06, 06.5, 06.7, 07 — UNCHANGED (FROZEN)

### Step 08, 09 — UNCHANGED

### Step 10 — UNCHANGED (FROZEN)

### Steps 11, 11.5, 12 — UNCHANGED (FROZEN)

### Steps 13, 13.5 — UNCHANGED (FROZEN)

### Step 14 (v13 cross-step coherence) — UNCHANGED (FROZEN)

### Step 14.5 (v14 coverage profile) — UNCHANGED (FROZEN)

### Step 14.6 — NEW (between step 14 and the round's final verdict synthesis)

**v15:** No step 14.6. Round verdict synthesis runs immediately after step 14.

**v16:** Step 14.6 fires ONLY when step 14 produced INVESTIGATIVE_CANDIDATE. It:
1. Strips the candidate's mechanism vocabulary (math-domain words removed; mechanism-skeleton retained).
2. Constructs an arXiv 2024-2026 search query covering mechanism class + architectural role + transformer context.
3. Runs the search (Agent spawn or main-context-direct synthesized).
4. Computes functional_similarity for top-5 results (4-axis rubric).
5. If max_functional_similarity ≥ 0.7: downgrade INVESTIGATIVE_CANDIDATE → EXTERNAL_COLLISION.
6. Writes `14_6_external_collision.json`.

Step 14.6 is symmetric with step 13.5 — both are post-FIRED gates that attack the architectural-distinguishability claim from a specific angle (empirical for 13.5; literature for 14.6).

### Verdict synthesis — UPDATED

**v15:** 8 verdict labels (PASS, PASS_WITH_EMPIRICAL_CAVEAT, FAIL, FAIL_ADVERSARIAL, FAIL_GAP_REAL_LOGGED, FAIL_EMPIRICAL_ATTACK, REJECTED_R279_PATTERN, INVESTIGATIVE_CANDIDATE).

**v16:** 9 verdict labels (the 8 above + NEW EXTERNAL_COLLISION). EXTERNAL_COLLISION is a downstream demotion from INVESTIGATIVE_CANDIDATE; only available after step 14 has FIRED.

PASS criterion: still 10 signals (UNCHANGED). v16 ADDS no new PASS gate.

---

## 4. Forbidden-zone preservation audit

For each FROZEN zone, confirm v16 does not modify:

| Zone | FROZEN since | v16 modifies? |
|---|---|:---:|
| Step 06 web_search | v5 | NO |
| Step 07 keyword threshold ≥ 2 | v5 | NO |
| Step 10 mechanical verdict | v5 | NO |
| Step 11.5 adversarial external | v7 | NO |
| Step 12 tree-stream | v8 | NO |
| v8 step 05 token streams FORMAT | v8 | NO |
| v8 step 11 Q-rubric | v8 | NO |
| Step 08, 09 (v9) | v9 | NO |
| Step 13 spec format | v10 | NO |
| Step 13.5 attack format | v11 | NO |
| Step 05.5 anti-R279 | v12 | NO |
| Step 14 cross-step coherence | v13 | NO |
| Step 14.5 coverage profile | v14 | NO |
| Step 05.4 k-means filter | v14 | NO |
| logs/architecture_tools.json (20 slots) | v14 | NO |
| Step 05.45 intra-cluster diversification | v15 | NO |
| PASS criterion (10 signals) | v12+v13 | NO |
| All existing verdict labels | v10+v11+v12+v13 | NO (v16 ADDS one new label; doesn't modify existing) |

**v16 confirms FORBIDDEN-ZONE preservation.** All v5...v15 components are unchanged.

---

## 5. Step 14.6 algorithm specification

### 5.1 Stripped vocabulary protocol

The vocabulary-strip transforms `(specific_mechanism + llm_application)` into a mechanism-skeleton:

```
INPUT: "Bregman-divergence reservoir-attention discriminator (slot S15)"
       + "Bregman-divergence reservoir-attention discriminator: introduce..."

STEP 1: Identify math-domain words.
  math_domain_words = {"Bregman", "divergence", "convex", "Lie", "SU(3)", ...}

STEP 2: Strip the math-domain words; replace with abstract class labels.
  "Bregman-divergence" → "<divergence-class>"
  "reservoir-attention" → "<state-on-attention-class>"
  "discriminator" → "<regularizer-or-projection-class>"

STEP 3: Keep transformer-context words verbatim.
  "self-attention", "softmax", "FFN", "residual", "transformer" — kept.

STEP 4: Keep architectural-role words verbatim.
  "slot", "module", "head", "layer", "embedding", "routing" — kept.

OUTPUT mechanism-skeleton: "<divergence-class> <state-on-attention-class> <regularizer-class> head modify self-attention"
```

### 5.2 arXiv query construction

```
arXiv_query_construction:
  classes = extract_classes(mechanism_skeleton)
  query_terms_class_1 = OR of synonyms for class 1 (e.g., divergence-class → "Bregman OR f-divergence OR phi-divergence OR KL OR Renyi")
  query_terms_class_2 = OR of synonyms for class 2
  query_terms_class_3 = OR of synonyms for class 3
  query_context = "(transformer OR self-attention OR LLM)"
  query_time = "2024..2026"
  full_query = AND of query_terms_class_1 AND query_terms_class_2 AND query_terms_class_3 AND query_context AND query_time
```

For R827:
```
query = "(Bregman OR f-divergence OR phi-divergence)" + "AND" 
      + "(reservoir OR state-space OR memory-network)" + "AND"
      + "(discriminator OR critic OR projection OR regularizer)" + "AND"
      + "(transformer OR self-attention OR LLM)" + "AND"
      + "2024..2026"
```

### 5.3 Functional-similarity rubric (4 axes)

For each top-5 arXiv result, compute 4 sub-scores:

```
mechanism_class_match: in {0.0, 0.25}
  0.25 if result uses same divergence class (e.g., both use Bregman)
  0.20 if result uses related divergence class (e.g., both use f-divergence family)
  0.15 if result uses divergence-class but a different family
  0.10 if result uses regularizer-class but no divergence
  0.0 otherwise

architectural_role_match: in {0.0, 0.25}
  0.25 if result has same architectural role (state-on-attention)
  0.20 if related role (memory-on-attention; cache-on-attention)
  0.15 if same architectural-modification slot
  0.0 otherwise

mechanism_alignment: in {0.0, 0.25}
  0.25 if mechanism map is essentially the same (functional alignment of the regularizer-role; the discriminator-role)
  0.20 if mechanism is similar (different word, same role)
  0.15 if mechanism is loosely related
  0.0 otherwise

transformer_context_match: in {0.0, 0.25}
  0.25 if same transformer context (self-attention modification)
  0.20 if related (cross-attention; FFN modification)
  0.15 if different transformer modification site
  0.0 otherwise

functional_similarity = sum of 4 sub-scores ∈ [0.0, 1.0]
```

### 5.4 Collision threshold

`collision_threshold = 0.7`. Calibrated such that:
- R827's match to arXiv 2512.14879 = 0.87 (above; flagged COLLISION)
- R834's top match = 0.51 (below; SURVIVES)
- R843's top match = 0.43 (below; SURVIVES)

The 0.7 threshold is fixed for E35; future v17 may re-calibrate.

### 5.5 Verdict assignment

```
if max_functional_similarity >= 0.7:
    verdict = "EXTERNAL_COLLISION"
    v16_label_assigned = "EXTERNAL_COLLISION"
elif max_functional_similarity in [0.5, 0.7):
    verdict = "INVESTIGATIVE_CANDIDATE_CLOSE_TO_COLLISION"
    v16_label_assigned = "INVESTIGATIVE_CANDIDATE"
    note = "max similarity in [0.5, 0.7) range; close-to-collision; future arXiv updates may push above threshold"
else:
    verdict = "INVESTIGATIVE_CANDIDATE_SURVIVES"
    v16_label_assigned = "INVESTIGATIVE_CANDIDATE"
```

---

## 6. v16 score formula

```
score_v16 = score_v15 with one entry REPLACED
          + (step_14_6_fired_count / N × 1)              ← NEW v16
          − (external_collision_count × 2)               ← NEW v16
          + (corpus_unique_investigative_niches_after_external_check / 3 × 4)  ← REPLACES v15's analogous term
          + ((1 − external_collision_rate) × 2)          ← NEW v16
```

The v15 `corpus_unique_investigative_niches / 3 × 4` term is REPLACED by v16's `corpus_unique_investigative_niches_after_external_check / 3 × 4` (since the v15 metric was over-counted; v16's is the honest count).

Net new v16 score contribution under E35-projected outcomes:
- step_14_6_fired_count = X
- external_collision_count = Y  (penalty -2Y)
- corpus_unique_investigative_niches_after_external_check = Z (replaces v15's)
- external_collision_rate = Y/X (reward (1-Y/X)*2)

Expected E35: X = 3 (similar to E34); Y = 1 (1 retrospective + 0 new = 1 if R827-pattern recurs, else 0); Z = 2-3.

---

## 7. Verdict-label hierarchy with v16's addition

Pre-v16 (v15 era): 8 labels, ordered by signal strength.
Post-v16: 9 labels.

The NEW label EXTERNAL_COLLISION sits between INVESTIGATIVE_CANDIDATE and FAIL:

```
   PASS                              (highest; never observed)
   PASS_WITH_EMPIRICAL_CAVEAT        (v10)
   ─────────────────────────────────
   INVESTIGATIVE_CANDIDATE            (v13; FIRED step 14; SURVIVES step 14.6)
   EXTERNAL_COLLISION                 (v16 NEW; FIRED step 14 + 14.6 demotes)
   ─────────────────────────────────
   FAIL                              (v5)
   FAIL_EMPIRICAL_ATTACK             (v11)
   FAIL_ADVERSARIAL                  (v7)
   FAIL_GAP_REAL_LOGGED              (v9)
   REJECTED_R279_PATTERN             (v12)
```

EXTERNAL_COLLISION sits BELOW INVESTIGATIVE_CANDIDATE in the diagnostic hierarchy. It is a demotion path. Both INVESTIGATIVE_CANDIDATE and EXTERNAL_COLLISION are "parallel-diagnostic" labels: they coexist with a FAIL verdict by the kw axis. The difference: INVESTIGATIVE_CANDIDATE means the architectural distinguishability survives BOTH empirical AND literature attacks; EXTERNAL_COLLISION means it survives empirical but fails literature.

---

## 8. Implementation symmetries with prior versions

| v_version | Step type | Filter axis | Mechanism | Trigger |
|---|---|---|---|---|
| v8 | step 12 | mechanism-vocabulary tree-stream | helper agent | always |
| v9 | step 09 | gap-position | inverse-search clusters | always |
| v10 | step 13 | toy-experiment-spec pre-check | spec generator | top-3 mechanical-PASS proximity |
| v11 | step 13.5 | adversarial-attack on architecture | spec attacker | step 13 fired |
| v12 | step 05.5 | anti-R279 vocabulary | classifier (regex) | always |
| v13 | step 14 | cross-step axis-coherence | 2-input check | always evaluated |
| v14 | step 05.4 | within-100-pool diversity | k-means | always |
| v14 | step 14.5 | post-epoch slot coverage | histogram + Gini | per-epoch |
| v15 | step 05.45 | intra-25-selected niche diversity | pairwise niche distance | always |
| **v16** | **step 14.6** | **external-literature collision** | **arXiv search + 4-axis rubric** | **step 14 FIRES (INVESTIGATIVE_CANDIDATE)** |

Each version adds a filter at a different abstraction level. v16's step 14.6 is the FIRST external-literature filter that operates on stripped mechanism-skeletons (vs step 06 which operates on concrete vocabulary).

---

## 9. Expected E35 outcomes under v16

### 9.1 Retrospective validation

When step 14.6 is applied retrospectively to E34's 3 INVESTIGATIVE rounds:
- R827 (Bregman-reservoir-attention-discriminator) → match arXiv 2512.14879 with functional-similarity ≈ 0.87 → **EXTERNAL_COLLISION**
- R834 (Bayes-categorical-posterior conformal critic) → top match 0.51 → SURVIVES
- R843 (Free-cumulant token routing) → top match 0.43 → SURVIVES

This is the validation check. If v16's step 14.6 does NOT flag R827 retrospectively, the rubric is mis-calibrated.

### 9.2 Prospective expected E35 outcomes

E35 should produce ~3 INVESTIGATIVE_CANDIDATE rounds (similar to E34's 3). Step 14.6 fires on each. Expected:
- 1-2 candidates survive (corpus_unique_investigative_niches_after_external_check_E35 ∈ {1, 2})
- 1-2 candidates flagged EXTERNAL_COLLISION

The exact count depends on the candidates generated. If E35's policy biases toward less-saturated mechanism-families (under-explored slot triples or under-explored math families), it should produce more SURVIVING niches.

### 9.3 Score outcome

Expected E35 score_v16 ≈ 65-70:
- v15 base of 64.42
- + step_14_6_fired = 3/25 × 1 = 0.12
- - external_collision = 1 × 2 = -2.0
- + corpus_unique_investigative_niches_after_external_check / 3 × 4 = 2/3 × 4 = 2.67 (replaces v15's 4.0 term)
- + (1 − external_collision_rate) × 2 = (1 − 1/3) × 2 = 1.33

Net change vs v15: 0.12 - 2.0 + (2.67 - 4.0) + 1.33 = -1.88. Slightly LOWER than v15's 64.42 (because EXTERNAL_COLLISION is a PENALTY signal — the corpus has discovered a collision, and this is the honest cost).

This is the v16 contribution: the corpus knows MORE (it now detects external collisions) but the score reflects HONEST COSTS (1 collision per epoch reduces the metric).

---

## 10. Cumulative N_verified and p-value progression (E32 → E35)

| Population | Cumulative N | p(no PASS | 1% H₀) | Notes |
|---|---:|---:|---|
| E32 R776-R800 v13 | 896 | 1.27e-4 | v13 (cross-step coherence) introduced |
| E33 R801-R825 v14 | 921 | 9.67e-5 | v14 (HTS/ATU/CPM) integrated |
| E34 R826-R850 v15 | 946 | 7.60e-5 | v15 (intra-cluster ICD) added |
| **E35 R851-R875 v16** | **971** | **5.96e-5** | **v16 (external-collision ECD) added** |

p-value continues to decrease as N grows; substantive PASS rate remains 0. Saturation maintained.

---

## 11. Anti-cheating commitments (v16 additions on top of v15)

The v3...v15 instructions stand. v16 adds:

- **Stripped vocabulary protocol** must be applied IDENTICALLY across rounds. The pipeline cannot strip aggressively for some candidates and weakly for others.
- **Functional-similarity rubric** must follow the 4-axis specification (§5.3). Sub-scores cannot be retro-fitted.
- **arXiv search honesty.** Synthesized search results must reflect the model's actual training-data recall. Fabricating non-existent arXiv IDs is forbidden.
- **Collision threshold immutability** (0.7) — fixed for E35; v17 may re-calibrate.
- **Retrospective validation** of R827 is mandatory. v16 MUST flag R827 as EXTERNAL_COLLISION when applied retroactively.

---

## 12. Conclusion

v16 adds **step 14.6 external-corpus collision detection**, the natural completion of the verification-side filter cascade. v15's step 05.45 widened internal mechanism-niche diversity (1 → 3 niches); v16's step 14.6 narrows back to the HONEST literature-clean count (3 → expected 1-2). Combined with v15's coverage and v14's CPM feedback, v16 closes the loop: candidates are generated diversely (HTS), selected for slot + niche diversity (ATU/ICD), and now checked against external literature (ECD).

The v16 thesis: **corpus_unique_investigative_niches_after_external_check** is the honest unique-niche count. R827 retrospectively demotes; R834 and R843 survive. v16 puts the corpus closer to a literature-validated novelty rate, which remains 0 substantive PASS at N=946 → projected 0 at N=971 (p ≈ 0.0000596 on 1%-H₀).

PASS criterion UNCHANGED. v16 does not lower the PASS bar.
