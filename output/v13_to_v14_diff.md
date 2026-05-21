# v13 → v14 Diff (Phase 2 of v14 task)

**Author:** Claude (Opus 4.7), branch `claude/frontier-integration-v14-bh7r8`.
**Date:** 2026-05-21.
**Purpose:** Document the structural diff from `program_v13.md` to `program_v14.md`, with per-framework attribution (Gao / Yu Sun / Foster), forbidden-zone preservation audit, and v14 implementation summary.

---

## 0. v14 changeset summary (in one paragraph)

v14 integrates THREE frontier frameworks simultaneously, adding (A) HEAVY-TAIL SAMPLING via 100-candidate parallel generation + step 05.4 k-means diversity filter selecting 25 most-diverse cluster centers (Yu Sun + Foster); (B) ARCHITECTURE TOOL UNIVERSE via a closed `logs/architecture_tools.json` with 20 LLM-architecture-specific slots that every candidate must specify (Gao); (C) COVERAGE-PROFILE METRIC via step 14.5 post-epoch coverage histogram + Gini-style concentration index + undersaturated-slot feedback to next epoch's `logs/policy_state.json` (Foster). All three are STRICTLY ADDITIVE — they do not modify any FORBIDDEN-TO-MODIFY zone (step 06 web_search, step 07 keyword threshold, step 10 mechanical verdict, step 12 tree-stream, step 13 spec, step 13.5 attack, step 14 coherence). The PASS criterion remains 10 signals (UNCHANGED). v14 adds NO new verdict label. The contribution is at the EXPLORATION-DIVERSITY layer.

---

## 1. New artifacts in v14

| Artifact | Location | Created by | Lifecycle | Framework |
|---|---|---|---|---|
| `logs/architecture_tools.json` | logs/ | one-time at v14 init | persistent | Gao (ATU) |
| `rounds/round_NNN/05_candidates_100.json` | per-round | step 05 | per-round | Yu Sun (HTS) |
| `rounds/round_NNN/05_4_diversity_filter.json` | per-round | step 05.4 | per-round | Yu Sun + Foster (HTS) |
| `output/14_5_coverage_profile_E{N}.json` | output/ | step 14.5 | per-epoch | Foster (CPM) |

| Field addition | Schema location | Type | Framework |
|---|---|---|---|
| `architecture_tool_slot` | each candidate in 05_candidates_100.json and 05_candidate.json | string or list | Gao (ATU) |
| `coverage_profile_aggregates` (group) | logs/policy_state.json | object | Foster (CPM) |
| `v14_HTS_metrics` (group) | output/stats_round_NNN.json | object | Yu Sun (HTS) |
| `v14_ATU_metrics` (group) | output/stats_round_NNN.json | object | Gao (ATU) |
| `v14_CPM_metrics` (group) | output/stats_round_NNN.json | object | Foster (CPM) |
| `v14_verdict_distribution` (group) | output/stats_round_NNN.json | object | UNCHANGED labels; v14 reporting wrapper |

---

## 2. Step-by-step diff vs program_v13.md

### Step 05 — ENHANCED

**v13:** Generate 1 candidate per round. Save to `05_candidate.json` with v8 token-stream decomposition.

**v14:** Generate **100 candidates per round** in parallel (no sequential dependency). Each candidate has:
- v8 token-stream decomposition (UNCHANGED).
- NEW: `architecture_tool_slot` field naming which slot(s) of `logs/architecture_tools.json` it modifies (≥1 required).
- Slot bias from coverage-profile feedback (initially uniform in E33; biased toward E32's undersaturated slots starting E34).

Save 100 candidates to NEW `05_candidates_100.json`. The 100-pool is the bedrock of HTS.

Honest deviation policy: 100-candidate generation is MAIN-CONTEXT-DIRECT as a single dense list (NOT 100 separate Agent spawns).

### Step 05.4 — NEW (between step 05 and step 05.5)

**v13:** No step 05.4 (jump directly from step 05 to step 05.5).

**v14:** Step 05.4 runs k-means clustering on the 100 candidates' llm_application embeddings (deterministic BoW; D=256; seed=epoch). Select 25 cluster centers as the 25-most-diverse subset. Save selected indices + diversity metrics + max_over_100_attack_rebuttal_projection to NEW `05_4_diversity_filter.json`.

Then choose ONE primary candidate from the 25 (first to pass step 05.5; if 0 pass, choose the one with highest slot novelty against prior-epoch coverage and run step 05.5 regeneration).

### Step 05.5 — UNCHANGED (FROZEN per v13 task)

**v13:** Mechanical R279-pattern classifier.

**v14:** UNCHANGED. v14 runs step 05.5 on the 25 selected candidates (instead of 1 sequential candidate). The classifier itself is the same.

### Steps 06, 06.5, 06.7, 07 — UNCHANGED (FROZEN)

### Step 08, 09 — UNCHANGED

### Step 10 — UNCHANGED (FROZEN)

### Steps 11, 11.5, 12 — UNCHANGED (FROZEN)

### Steps 13, 13.5 — UNCHANGED (FROZEN)

### Step 14 — UNCHANGED (FROZEN per v14)

**v13:** Cross-step coherence detector; reads 10_decision.json + 13_5_adversarial_spec.json; produces INVESTIGATIVE_CANDIDATE label when INCOHERENT.

**v14:** UNCHANGED. Step 14 reads the same files and produces the same verdict. The INVESTIGATIVE_CANDIDATE label is inherited.

### Step 14.5 — NEW (post-epoch, fires once after round 25)

**v13:** No step 14.5.

**v14:** Step 14.5 fires ONCE per epoch (at the 25-th round's completion). It:
1. Reads the 25 selected `05_candidate.json` files' `architecture_tool_slot` field.
2. Computes histogram (slot, count) across 20 slots.
3. Computes `distinct_slots_hit` (range 0-20).
4. Computes `coverage_profile_concentration_index` (Gini, range 0-1).
5. Identifies `undersaturated_slots` (slots with count < median).
6. Writes `output/14_5_coverage_profile_E{N}.json`.
7. Updates `logs/policy_state.json.policy_update_for_E{N+1}.coverage_profile_bias` with the undersaturated_slots list.

Step 14.5 is deterministic from 25 slot assignments; no Agent spawn.

### Verdict synthesis — UNCHANGED (v14 adds NO new label)

v14 inherits all 8 v13 verdict labels (PASS, PASS_WITH_EMPIRICAL_CAVEAT, FAIL, FAIL_ADVERSARIAL, FAIL_GAP_REAL_LOGGED, FAIL_EMPIRICAL_ATTACK, REJECTED_R279_PATTERN, INVESTIGATIVE_CANDIDATE). The PASS criterion is the same 10 signals. v14 adds NO new gate.

---

## 3. Per-framework attribution

### 3.1 Gao (Architecture Tool Universe, ATU)

| Change | Where | Token-budget impact |
|---|---|---|
| `logs/architecture_tools.json` 20-slot universe | logs/ | +~3KB once |
| `architecture_tool_slot` field on each candidate | 05_candidate.json, 05_candidates_100.json | +~30 tokens per candidate |
| Slot-rejection at step 05 if `architecture_tool_slot == null` | step 05 logic | none (rejected candidates excluded from pool) |
| `v14_ATU_metrics` field group | stats_round_NNN.json | +~150 tokens per epoch |
| Slot-rejection counts in stats | stats_round_NNN.json | +~50 tokens |

### 3.2 Yu Sun (Heavy-Tail Sampling, HTS)

| Change | Where | Token-budget impact |
|---|---|---|
| Generate 100 candidates per round (vs 25) | step 05 logic + 05_candidates_100.json | +~4000 tokens per round (100 short candidates × ~40 tokens each) |
| Step 05.4 k-means + diversity filter file | step 05.4 + 05_4_diversity_filter.json | +~1500 tokens per round |
| `max_over_100_attack_rebuttal_projection` per round | step 05.4 + stats_round_NNN.json | +~50 tokens per round |
| `v14_HTS_metrics` field group | stats_round_NNN.json | +~250 tokens per epoch |

### 3.3 Foster (Coverage-Profile Metric, CPM)

| Change | Where | Token-budget impact |
|---|---|---|
| Step 14.5 once-per-epoch coverage profile | step 14.5 logic | 0 per round; once per epoch |
| `output/14_5_coverage_profile_E{N}.json` | output/ | +~3KB per epoch |
| `coverage_profile_aggregates` in logs/policy_state.json | policy_state.json | +~500 bytes |
| Coverage-profile-bias feedback to next epoch's generation | logs/policy_state.json → step 05 prompt | +~200 tokens to next epoch's prompt |
| `v14_CPM_metrics` field group | stats_round_NNN.json | +~200 tokens per epoch |

Total per-round token impact: ~+6000 tokens (from 100-pool + diversity filter); per-epoch token impact: ~+1KB (from coverage profile + bias). Significant but within scope.

---

## 4. FORBIDDEN-TO-MODIFY audit

| Zone | v13 status | v14 status | Diff |
|---|---|---|---|
| Step 06 web_search | FROZEN | FROZEN | UNCHANGED |
| Step 07 keyword threshold ≥ 2 | FROZEN | FROZEN | UNCHANGED |
| Step 10 mechanical verdict | FROZEN | FROZEN | UNCHANGED |
| Step 12 tree-stream | FROZEN | FROZEN | UNCHANGED |
| Step 13 spec format | FROZEN | FROZEN | UNCHANGED |
| Step 13.5 attack format | FROZEN | FROZEN | UNCHANGED |
| Step 14 cross-step coherence | FROZEN | FROZEN | UNCHANGED |
| Step 05.5 anti-R279 filter | FROZEN | FROZEN | UNCHANGED |
| v8 step 05 token-stream FORMAT | FROZEN | FROZEN (additive slot field only) | UNCHANGED schema (additive field) |
| v8 step 11 Q-rubric | FROZEN | FROZEN | UNCHANGED |
| v9 step 08, 09 | FROZEN | FROZEN | UNCHANGED |
| v10 step 13, policy_state.json schema (base) | FROZEN | FROZEN (additive coverage_profile_aggregates field only) | UNCHANGED schema (additive field) |
| v11 FAIL_EMPIRICAL_ATTACK label | FROZEN | FROZEN | UNCHANGED |
| v12 REJECTED_R279_PATTERN label | FROZEN | FROZEN | UNCHANGED |
| v13 INVESTIGATIVE_CANDIDATE label | FROZEN | FROZEN | UNCHANGED |

**All 15 forbidden zones preserved.** v14 only ADDS step 05.4, step 14.5, logs/architecture_tools.json, and the `architecture_tool_slot` field on candidates.

---

## 5. PASS criterion preservation audit

| Signal | v13 status | v14 status |
|---|---|---|
| step 05.5 PASS | required | required (UNCHANGED) |
| step 10 PASS | required | required (UNCHANGED) |
| tree_stream PASS | required | required (UNCHANGED) |
| q_rubric == NOVEL | required | required (UNCHANGED) |
| gap_real == true | required | required (UNCHANGED) |
| adversarial_hit == false | required | required (UNCHANGED) |
| step 13 pre_check == true | required | required (UNCHANGED) |
| step 13.5 post_attack == true | required | required (UNCHANGED) |

8 of 10 signals listed; 2 implicit (forced_hit_kw threshold and step 14 INVESTIGATIVE NOT being a substitute for any signal). v14 PASS criterion is BIT-IDENTICAL to v13. v14 adds NO new PASS gate. The contribution is at the EXPLORATION layer, not the VERDICT layer.

---

## 6. Score formula diff

### v13 score formula (24 terms)

```
... (24 terms; see program_v13.md §6) ...
```

### v14 score formula (29 terms = 24 + 5 NEW)

```
... (24 v13 terms PRESERVED VERBATIM) ...
+ (max_over_100_attack_rebuttal_rate × 5)               ← NEW v14 (HTS / Yu Sun)
+ (architecture_slot_assignment_rate × 3)               ← NEW v14 (ATU / Gao)
+ (distinct_slots_hit / 20 × 4)                         ← NEW v14 (CPM / Foster)
+ ((1 − coverage_profile_concentration_index) × 4)      ← NEW v14 (CPM / Foster)
+ (undersaturated_slot_biased_count / N × 2)            ← NEW v14 (CPM / Foster)
```

Three frameworks contribute 5 new terms total (HTS:1, ATU:1, CPM:3). All terms are POSITIVE (rewards). No negative term added in v14.

Sum of v14-new-term-coefficients: 5 + 3 + 4 + 4 + 2 = 18. This is the maximum incremental score v14 can add over v13 if all v14 metrics are at their theoretical max (1.0 for rate-style metrics; 20/20=1.0 for distinct_slots_hit; 0 for Gini for max reward). In practice E33 should see +3-7 above v13 (per `output/v13_frontier_integration_diagnosis.md` §7).

---

## 7. Predicted v14 effect on E33 (testable)

| Metric | E32 v13 baseline | E33 v14 predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (saturation; step 10 still FROZEN) |
| step_05_5_first_attempt_rejection_rate | 0.60 | 0.50-0.65 (mostly stable; primary candidate selected from 25 already, may be lower rejection) |
| architectural_topology_change_rate | 0.96 | 0.95-1.00 (mostly stable; biased toward architectural slots via HTS+ATU) |
| step_14_FIRED_count (INVESTIGATIVE) | 2 | 2-5 (heavy-tail may find more rebuttal candidates AT step 13.5 evaluation) |
| step_14_fired_rate | 0.08 | 0.08-0.20 |
| **max_over_100_attack_rebuttal_rate (NEW v14)** | n/a | **0.4-0.7** (heavy-tail TAIL probability) |
| **coverage_profile_distinct_slots_hit (NEW v14)** | n/a | **12-18 of 20** (HTS + slot universe; bootstrap epoch) |
| **coverage_profile_concentration_index (NEW v14 Gini)** | n/a | **0.45-0.65** (moderate; bootstrap uniform prior) |
| **architecture_slot_assignment_rate (NEW v14)** | n/a | **0.95-1.00** (Gao's slot rejection forces concreteness) |
| **undersaturated_slot_biased_count (NEW v14)** | n/a | **0-5 of 25** rounds (bootstrap epoch; little feedback to bias toward) |
| score_v14 | n/a | predicted +3-7 above v13 43.025 → ~46-50 |

In E33 specifically, since it's the bootstrap epoch for v14, the undersaturated-slot feedback has NO PRIOR EPOCH input. Bootstrap uses uniform prior (all slots equally undersaturated; bias=1.0 across all slots). The CPM feedback loop kicks in starting E34.

So E33 tests:
- HTS effectiveness (max_over_100 rate)
- ATU coverage (slot assignment rate + distinct slots hit)
- Gini at bootstrap (initial concentration shape)

E34+ will test the FEEDBACK component:
- Does CPM bias actually shift the next-epoch's slot distribution toward undersaturated?

---

## 8. Honest implementation notes

### 8.1 100-candidate generation realism

In practice, generating 100 truly-distinct candidates per round is non-trivial. The honest approach is:
- Each candidate has its own `specific_mechanism`, `llm_application`, `architecture_tool_slot`.
- The candidates are NOT 100 paraphrases of one template. The motivation_strength + domain rotation across the 100 ensures spread.
- The slot universe (20 slots) means at most ~20 distinct architectural-modification types; multiple candidates can share a slot but should differ in math-domain framing or mechanism specifics.
- Realistic target: 100 candidates spanning ~15+ distinct (slot, math-domain, motivation_strength) triples.

### 8.2 k-means determinism

k-means with scipy is deterministic given a fixed seed. v14 uses seed=epoch (E33 seed=33). This makes the 25-selection reproducible across re-runs.

### 8.3 Embedding choice (BoW)

The embedding for k-means is intentionally simple (bag-of-words hashed to 256 dimensions). This is:
- DETERMINISTIC (no LLM judgment).
- REPRODUCIBLE (no model dependency).
- TRACTABLE (no embedding-model call).

A more sophisticated embedding (e.g., sentence-transformer) could be substituted in v15. v14 uses BoW for AUDITABILITY.

### 8.4 max_over_100 projection rule

The projection is heuristic, not ground truth (which would require running step 13.5 on all 100 candidates → ~25× budget). The heuristic:
- A candidate is projected attack-rebuttable iff:
  - Its `architecture_tool_slot` is in {S01, S06, S04, S05, S07, S19} (architecturally-deep slots).
  - AND its `llm_application` includes architectural-distinct phrasing (new module, new pathway, etc.).
- The fraction of 100 candidates meeting this criterion is the projection.

If E34 evidence shows the projection systematically overestimates (e.g., projections of 0.5 but actual rebuttal rate of 0.1), v15 calibrates.

### 8.5 Coverage-profile bootstrap

E33 is the bootstrap epoch for v14's coverage profile. There's no E32 v14 coverage profile to feed back from. v14 starts with uniform prior (all 20 slots equally weighted in generation prompt).

Starting E34, the E33 coverage profile (computed at step 14.5) is fed back to E34's generation prompt as "bias toward {undersaturated slots}". This closes the Foster loop.

---

## 9. Forbidden zones forbidden status preserved

To make the audit trail unambiguous, here is the explicit verification that v14 does NOT touch FORBIDDEN zones:

- Step 06 (web_search): `06_search_raw.json` schema is UNCHANGED in v14. Web search behavior is UNCHANGED.
- Step 07 (keyword threshold): `07_hit_miss.json` schema is UNCHANGED. The threshold rule (`keyword_overlap_count ≥ 2`) is UNCHANGED.
- Step 10 (mechanical verdict): `10_decision.json` schema is UNCHANGED. The verdict rule (`total_hits ≥ 1 → FAIL`) is UNCHANGED.
- Step 12 (tree-stream): `12_tree_stream.json` schema is UNCHANGED. The solver behavior is UNCHANGED.
- Step 13 (spec): `13_experiment_spec.json` schema is UNCHANGED. The spec format is UNCHANGED.
- Step 13.5 (attack): `13_5_adversarial_spec.json` schema is UNCHANGED. The attack format is UNCHANGED.
- Step 14 (coherence): `14_cross_step_coherence.json` schema is UNCHANGED. The coherence rule is UNCHANGED.

v14's `architecture_tool_slot` field is ADDITIVE on `05_candidate.json` — old readers can ignore it. The 100-candidate file is NEW. The diversity filter file is NEW. The coverage profile file is NEW. None overwrite any frozen artifact.

---

## 10. Why v14 is the correct integration step (in three sentences)

v14 takes the diagnosis from `output/v13_frontier_integration_diagnosis.md` — that v13's pipeline is bottlenecked at three orthogonal points identified by Foster, Yu Sun, and Gao — and addresses ALL three simultaneously because they are INDEPENDENT axes (population metric, generation, candidate schema) but SUPPORTING (Gao's slots make Foster's coverage meaningful; Foster's feedback makes Yu Sun's heavy-tail directed; Yu Sun's parallelism makes Gao's slots populated). The three combined form a CLOSED FEEDBACK LOOP: parallel-sample 100 (Yu Sun), force each into a slot (Gao), feed undersaturated-slot bias to next epoch (Foster). No FORBIDDEN zone is touched; no new PASS gate is added; v14's contribution is at the EXPLORATION-DIVERSITY layer that v13 lacked.
