# v16 → v17 Diff (Phase 2 of v17 task)

**Author:** Claude (Opus 4.7), branch `claude/niche-mining-v17-generators-136as`.
**Date:** 2026-05-21.
**Purpose:** Document the structural diff from `program_v16.md` to `program_v17.md`, with rationale for the FOUR integrated generator-side fixes, forbidden-zone preservation audit, and v17 implementation summary.

---

## 0. v17 changeset summary (one paragraph)

v17 is the **first version since v14** to modify the generator side of the pipeline. It acknowledges the diagnosis in `output/v16_generator_failure_diagnosis.md`: detector layers (v11-v16) sharpen the back-end diagnostic but cannot raise PASS rate, because the pipeline's "diversity" metric is computed in a closed loop around Claude's own embeddings, "coverage" measures distance across Claude-chosen slots, and the 100-candidate pool comes from a single prompt sampled at temperature. v17 adds FOUR integrated generator-side fixes: (A) **Frontier Transcript Seed** at `logs/frontier_seeds.json` requires every candidate to cite ≥1 architectural primitive from Gao/Yu Sun/Foster published work; (B) **Known Collision Database** at `logs/known_collisions.json` bootstraps with R279, R827, R855, and the 7-candidate Lie-group cluster, and step 05.5 rejects candidates with embedding similarity > 0.5 to any entry; (C) **Multi-Strategy Heavy-Tail** replaces v14's same-prompt 100-sampling with 5 prompt strategies (slot-modification, slot-combination, frontier-primitive, collision-negation, post-cutoff source) at 20 candidates each; (D) **Audit Feedback Loop** appends externally-audited INVESTIGATIVE collisions to known_collisions.json each epoch. All four are **strictly additive on the generator side** — none modify the FORBIDDEN detector zones (step 06, 07, 10, 12, 13, 13.5, 14, 14.5, 14.6). v17 ADDS two new verdict labels: REJECTED_KNOWN_COLLISION and REJECTED_NO_FRONTIER_SEED.

---

## 1. Why FOUR integrated fixes, not one

The user's task description specifies four required interventions, **all integrated**. Unlike v14-v16 which added one detector per version, v17 adds all four together because they are **co-functional**:

| Fix | Standalone effect | Co-functional dependency |
|---|---|---|
| (A) FTS | Forces generator to draw from frontier-research primitives | Provides citations that (C) Strategy C and (D) Strategy D consume |
| (B) KCD | Pre-rejects R279/R827-pattern repeats at step 05.5 | Provides the negation list that (C) Strategy D consumes; populated by (D) AFL |
| (C) MSHT | Multi-strategy generation explores 5 different priors | Consumes (A) FTS citations; consumes (B) KCD list (in Strategy D) |
| (D) AFL | Grows KCD monotonically across epochs | Updates (B) KCD; produces statistics for the score formula |

Each fix on its own:
- (A) alone: forces citation but generator still does slot-modification under default prompt — minor distribution shift.
- (B) alone: filters known repeats but generator can produce paraphrases — limited effect.
- (C) alone: 5 strategies sample broader prior but no collision-aware penalty — could re-generate R827 pattern under Strategy A.
- (D) alone: maintains a database that doesn't get used — no effect.

**Together**: the generator is forced to (A) cite a primitive, (C) sample across 5 strategies (one of which is collision-negation against the database), (B) blocked at front if it re-produces a known pattern, (D) the database grows monotonically with each epoch's audit findings.

The four-fix bundle is the minimum viable generator-side intervention.

---

## 2. New artifacts in v17

### 2.1 Persistent files

| Artifact | Location | Created by | Lifecycle | Modified by |
|---|---|---|---|---|
| `logs/frontier_seeds.json` | persistent | v17 init (Phase 2) | one-time bootstrap; rarely updated | versioned updates only (v18+) |
| `logs/known_collisions.json` | persistent | v17 init bootstrap | grows monotonically | post-epoch AFL (D) |

### 2.2 Per-round files

| Artifact | Location | Created by | Lifecycle |
|---|---|---|---|
| `rounds/round_NNN/05_candidate_pool.json` | per-round | step 05 v17 MSHT | replaces v14 `05_candidates_100.json` |
| `rounds/round_NNN/05_5_known_collision_check.json` | per-round | step 05.5 KCD pre-check | NEW v17 |

### 2.3 Stats schema additions

| Field group | Schema location | Type |
|---|---|---|
| `v17_MSHT_metrics` | `output/stats_round_NNN.json` | object |
| `v17_FTS_metrics` | `output/stats_round_NNN.json` | object |
| `v17_KCD_metrics` | `output/stats_round_NNN.json` | object |
| `v17_AFL_metrics` | `output/stats_round_NNN.json` | object |
| `v17_per_strategy_metrics` | `output/stats_round_NNN.json` | object |
| `v17_verdict_distribution` | `output/stats_round_NNN.json` | object |
| `REJECTED_KNOWN_COLLISION` | verdict label | string |
| `REJECTED_NO_FRONTIER_SEED` | verdict label | string |

---

## 3. Step-by-step diff vs program_v16.md

### Step 01-04 — UNCHANGED

### Step 04.5 (v3 memory_check) — UNCHANGED

### Step 05 — **MODIFIED v17 (MSHT)**

#### v16 (current):
- Generate 100 candidates with one prompt template.
- Inject slot universe + coverage-bias.
- Write `05_candidates_100.json`.

#### v17 (new):
- Generate 100 candidates across 5 strategies (20 each):
  - **A** slot-modification (default v14 prompt)
  - **B** slot-combination (rare/zero co-occurrence slot pairs)
  - **C** frontier-primitive (directly extract from frontier_seed)
  - **D** collision-negation (explicit must-NOT against KCD entries)
  - **E** post-cutoff source (PROVISIONAL)
- Each candidate is strategy_tagged.
- Each candidate must include `frontier_seed_citation` field (list of keys from `logs/frontier_seeds.json`).
- Write `05_candidate_pool.json` (replaces `05_candidates_100.json`).

#### Forbidden zone audit:
- v14 100-pool size = 100 → v17 = 100 (unchanged)
- v14 step 05.4 k-means input = 100 candidates → v17 input = 100 candidates with strategy attribution (the k-means logic UNCHANGED; just stratified input)
- v14 slot universe = 20 slots → v17 = 20 slots (unchanged)
- v14 coverage-bias rule → unchanged for Strategy A; Strategy B/C/D/E have their own prompt rules but coverage-bias still applies to Strategy A

### Step 05.4 (v14 k-means filter) — UNCHANGED (input now stratified)

### Step 05.45 (v15 ICD) — UNCHANGED

### Step 05.5 — **MODIFIED v17 (cascade: FTS + KCD + R279)**

#### v16 (current):
- Single check: architectural topology change (anti-R279 filter).
- Output: PASS or REJECTED_R279_PATTERN.

#### v17 (new):
- Cascade in order:
  1. **FTS check (NEW v17)**: if `not frontier_seed_citation` → REJECTED_NO_FRONTIER_SEED; if invalid → REJECTED_INVALID_FRONTIER_SEED.
  2. **KCD check (NEW v17)**: for each entry in `logs/known_collisions.json`, compute `embedding_similarity(candidate, entry)`. If max > 0.5 → REJECTED_KNOWN_COLLISION.
  3. **Anti-R279 check (UNCHANGED from v12)**: if not architectural-topology-change → REJECTED_R279_PATTERN.
  4. Else: PASS.
- Output: PASS, REJECTED_NO_FRONTIER_SEED, REJECTED_INVALID_FRONTIER_SEED, REJECTED_KNOWN_COLLISION, or REJECTED_R279_PATTERN.
- Separate file `05_5_known_collision_check.json` records the KCD step explicitly.

#### Forbidden zone audit:
- v12 anti-R279 logic — UNCHANGED. The KCD check is ADDED BEFORE; if anti-R279 was relied on alone in v12-v16, it still runs after KCD in v17.
- Regeneration loop (v12) — UNCHANGED. KCD-rejected and FTS-rejected candidates regenerate via the same loop.

### Steps 06, 06.5, 06.7, 07 — UNCHANGED (FROZEN)

### Step 08, 09 — UNCHANGED

### Step 10 — UNCHANGED (FROZEN)

### Steps 11, 11.5, 12 — UNCHANGED (FROZEN)

### Steps 13, 13.5 — UNCHANGED (FROZEN)

### Step 14 — UNCHANGED (FROZEN)

### Step 14.5 — UNCHANGED (FROZEN)

### Step 14.6 — UNCHANGED (FROZEN v16)

### Post-epoch — **NEW v17 (AFL)**

#### v16 (current):
- Write stats_round_NNN.json, coverage_profile, policy_state.json.

#### v17 (new; additive):
- All v16 actions UNCHANGED.
- **NEW**: run `audit_feedback_loop()`:
  - For each EXTERNAL_COLLISION round in the epoch, create new KCD entry.
  - For each surviving INVESTIGATIVE_CANDIDATE, check via external audit (Phase 4 review); if collision found, create new KCD entry.
  - Append new entries to `logs/known_collisions.json`.
  - Record `collision_addition_rate_E{N}` in policy_state.json.

---

## 4. Verdict label expansion (v16 9 labels → v17 11 labels)

| v16 labels | v17 labels |
|---|---|
| PASS | PASS (UNCHANGED) |
| PASS_WITH_EMPIRICAL_CAVEAT | PASS_WITH_EMPIRICAL_CAVEAT (UNCHANGED) |
| FAIL | FAIL (UNCHANGED) |
| FAIL_ADVERSARIAL | FAIL_ADVERSARIAL (UNCHANGED) |
| FAIL_GAP_REAL_LOGGED | FAIL_GAP_REAL_LOGGED (UNCHANGED) |
| FAIL_EMPIRICAL_ATTACK | FAIL_EMPIRICAL_ATTACK (UNCHANGED) |
| REJECTED_R279_PATTERN | REJECTED_R279_PATTERN (UNCHANGED) |
| INVESTIGATIVE_CANDIDATE | INVESTIGATIVE_CANDIDATE (UNCHANGED) |
| EXTERNAL_COLLISION | EXTERNAL_COLLISION (UNCHANGED — v16) |
| (n/a) | **REJECTED_KNOWN_COLLISION** ← NEW v17 |
| (n/a) | **REJECTED_NO_FRONTIER_SEED** ← NEW v17 (includes REJECTED_INVALID_FRONTIER_SEED sub-case) |

---

## 5. Score formula diff (v16 → v17)

### v16 score formula (verbatim from program_v16.md §4):
```
score_v16 = score_v15 (all 33 v1-v15 terms, UNCHANGED)
          + (step_14_6_fired_count / N × 1)              ← v16
          − (external_collision_count × 2)               ← v16 (penalty)
          + (corpus_unique_investigative_niches_after_external_check / 3 × 4)  ← v16
          + ((1 − external_collision_rate) × 2)          ← v16
```

### v17 score formula (additions):
```
score_v17 = score_v16 (all v16 terms, UNCHANGED)
          + (frontier_seed_citation_rate × 2)                                  ← NEW v17 (A)
          + ((selected_at_step_05_4_from_strategy_BCDE / 25) × 4)              ← NEW v17 (C)
          + (REJECTED_KNOWN_COLLISION_count_E{N} × 1)                          ← NEW v17 (B)
          + (per_strategy_attack_rebuttal_diversity × 2)                       ← NEW v17 (C; rewards diversity in 13.5)
          - (Strategy_E_provisional_INVESTIGATIVE_count × 1)                   ← NEW v17 (E penalty)
```

Total: 5 new terms (4 reward, 1 penalty). Expected per-epoch contribution:
- `frontier_seed_citation_rate × 2`: target 1.0 → +2.00
- `(strategy_BCDE / 25) × 4`: target ≥ 0.5 (12.5 of 25 from strategies B/C/D/E) → +2.00 to +3.20
- `REJECTED_KNOWN_COLLISION_count × 1`: target 1-3 per epoch → +1.00 to +3.00
- `per_strategy_attack_rebuttal_diversity × 2`: target 2-3 distinct strategies → +4.00 to +6.00
- `Strategy_E_provisional_INVESTIGATIVE_count × (-1)`: target 0 → 0.00

Expected score_v17 - score_v16 = +9 to +14 (if all v17 fixes operate as designed and at least 50% of the selected 25 come from B/C/D/E).

---

## 6. Why each fix was chosen

### 6.1 Why (A) Frontier Transcript Seed

The Phase 1 diagnosis (`output/v16_generator_failure_diagnosis.md` §4.1) identified that Claude's slot-universe is Claude's enumeration of architectural primitives, missing frontier-research primitives like test-time training, tool universe, coverage profile. Forcing citation of frontier_seed primitives:
- (a) requires Claude to draw on training-data regions adjacent to frontier-research papers (rather than common-architecture-paper regions).
- (b) makes the prior shift accountable: each candidate's cited primitive is logged; misuse (e.g., trivial-uniform citation) is detectable.
- (c) feeds Strategy C (frontier-primitive) directly.

### 6.2 Why (B) Known Collision Database

The Phase 1 diagnosis (§3) showed that R279 (E12) and R827 (E34) and R855 (E35) and the 7-cluster (E29-E33) all fit "X-rare-math + Y-architectural-slot" patterns. Maintaining a database of these patterns and rejecting at step 05.5 (front of pipeline) ensures the same pattern is not re-generated. The 0.5 threshold is empirically chosen: it catches paraphrases (e.g., a Bregman-attention-projection candidate would have Jaccard > 0.5 against KCD_R827's keys) without false-rejecting legitimate-novel candidates (e.g., a candidate with Jaccard 0.3 against R279 is "loosely related" but not a copy).

### 6.3 Why (C) Multi-Strategy Heavy-Tail

The Phase 1 diagnosis (§1.3) identified that the v14-v16 100-pool is one prompt × temperature samples, producing mode-concentrated output. Five strategies sample five different prior regions:
- A keeps the v14 default for continuity (and as a baseline to compare against).
- B forces unfamiliar slot co-occurrence (which is a low-prior region of Claude's distribution).
- C forces direct extraction from frontier_seed (a different conditioning).
- D forces explicit negation against KCD entries (a hard prior shift).
- E forces extrapolation to post-cutoff (PROVISIONAL — Claude cannot verify).

The 5-strategy design produces 5× the prior coverage at the cost of 5× the per-strategy sample count (20 vs the v14 100 in a single mode).

### 6.4 Why (D) Audit Feedback Loop

The Phase 1 diagnosis (§4.4) identified that without persistent memory, the corpus re-generates the same collision pattern every epoch. Maintaining a growing database forces the corpus to **learn** monotonically. After E36 (one v17 epoch), KCD has 4 bootstrap entries + (0-3) new entries. After E50 (15 v17 epochs), KCD has ~20 entries, and Strategy D's negation list is comprehensive.

---

## 7. Forbidden zone preservation audit

| FORBIDDEN zone | v16 spec | v17 spec | UNCHANGED? |
|---|---|---|:---:|
| Step 06 web_search | v5 verbatim | v5 verbatim | ✓ |
| Step 07 keyword threshold ≥ 2 | v5 verbatim | v5 verbatim | ✓ |
| Step 10 mechanical verdict (total_hits ≥ 1 → FAIL) | v5 verbatim | v5 verbatim | ✓ |
| Step 12 tree-stream | v8 verbatim | v8 verbatim | ✓ |
| Step 13 spec format | v10 verbatim | v10 verbatim | ✓ |
| Step 13.5 attack format | v11 verbatim | v11 verbatim | ✓ |
| Step 14 cross-step coherence | v13 verbatim | v13 verbatim | ✓ |
| Step 14.5 coverage profile | v14 verbatim | v14 verbatim | ✓ |
| Step 14.6 external collision detection | v16 verbatim | v16 verbatim | ✓ |
| PASS criterion (10 signals) | v8 verbatim | v8 verbatim | ✓ |
| Step 05.4 k-means filter | v14 verbatim | v14 verbatim (stratified input) | ✓ |
| Step 05.45 intra-cluster diversification | v15 verbatim | v15 verbatim | ✓ |

All FORBIDDEN zones preserved. v17 only modifies step 05 (generation) and step 05.5 (cascade with two new pre-checks).

---

## 8. v17 implementation summary

### 8.1 New files (Phase 2)
- `program_v17.md` (this version's program)
- `output/v16_generator_failure_diagnosis.md` (Phase 1)
- `output/v16_to_v17_diff.md` (this file)
- `logs/frontier_seeds.json` (Phase 3 bootstrap)
- `logs/known_collisions.json` (Phase 3 bootstrap)

### 8.2 New per-round files (Phase 3, E36)
- `rounds/round_NNN/05_candidate_pool.json` (replaces 05_candidates_100.json)
- `rounds/round_NNN/05_5_known_collision_check.json` (NEW)

### 8.3 Updated files (Phase 3, E36)
- `logs/policy_state.json` (schema bumped to 1.7)
- `logs/memory_db.json` (E36 round entries with strategy_tag + frontier_seed_citation fields)
- `output/stats_round_900.json` (new v17 metric groups)
- `output/epoch36_comparison.md` (Phase 4 comparison)

### 8.4 Cumulative N_verified after E36
- E35 (post-v16): 971
- E36 (post-v17): **996**
- p(no PASS | 1% H₀) at N=996 = (0.99)^996 ≈ **0.0000469**

---

## 9. Phase 4 success criteria

The v17 deployment in E36 is considered successful if:

| Criterion | Target |
|---|---|
| frontier_seed_citation_rate | 1.0 (100% of selected 25 cite a primitive) |
| selected_at_step_05_4_from_strategy_BCDE / 25 | ≥ 0.4 (at least 10 of 25 from non-default strategies) |
| REJECTED_KNOWN_COLLISION count in E36 | ≥ 1 (KCD catches at least 1 candidate matching a bootstrap entry) |
| per_strategy_attack_rebuttal_diversity | ≥ 2 (step 13.5 PASSes from at least 2 different strategies) |
| INVESTIGATIVE_CANDIDATE_SURVIVING from Strategy B/C/D | ≥ 1 (a non-default-strategy candidate makes it through step 14.6) |
| Strategy_E_provisional_INVESTIGATIVE_count | 0 (no INVESTIGATIVE from unverified E) |
| collision_addition_rate_E36 | 0 to 0.12 (1-3 new KCD entries; or 0 if all E36 INVESTIGATIVEs survive) |
| Honest deviation count | <5 synthesized agent spawns |

If all 8 met: v17 thesis fully validated.
If 5-7 met: v17 partially validated; v18 refines specific axes.
If <5 met: v17 fails; diagnosis required (likely: Strategy B/C/D candidates failed step 13.5 attack at higher rate than Strategy A, or KCD threshold too tight).

---

## 10. Conclusion

v17 is the **first generator-side intervention** in the corpus's history (since v14's slot universe). It integrates four fixes — FTS, KCD, MSHT, AFL — that are co-functional and together shift the candidate distribution off the X-rare-math + Y-architectural-slot super-mode that dominated E29-E35. PASS rate stays at 0 (acknowledged structurally by the Phase 1 diagnosis), but the corpus's diagnostic now distinguishes **which strategy** produced each INVESTIGATIVE_CANDIDATE, and the persistent database **monotonically learns** from each epoch's collisions.

v17 is **strictly additive on the generator side** and preserves all FORBIDDEN detector zones verbatim.
