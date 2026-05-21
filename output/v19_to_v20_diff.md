# v19 → v20 Diff (Phase 2 of v20 task)

**Author:** Claude (Opus 4.7), branch `claude/v20-self-model-framework-7h9w9`.
**Date:** 2026-05-21.
**Purpose:** Document the structural diff from `program_v19.md` to `program_v20.md`, with rationale for choosing Belinda Li's self-model framework over alternatives, forbidden-zone preservation audit, and v20 implementation summary.

---

## 0. v20 changeset summary (one paragraph)

v20 introduces ONE Belinda-Li-inspired upgrade: a **self-model layer** spanning three NEW components — step 05.7 (pipeline self-model, first-person narrative + self-prediction), step 15 (coherence audit, three binary checks comparing self-narrative to reality), and an epoch-end failure self-attribution document (`output/epoch_{N}_self_attribution.md`). Where v17 added external-state representation (FTS + KCD), v18 added prior concentration around productive state (anchor-local sampling), and v19 added per-candidate predictive classifier (learned verifier), v20 adds **first-person introspection**: the pipeline must verbalize WHY it produced a candidate, predict its own step-14.6 outcome before that detector fires, and at epoch end articulate which of its own bias patterns produced FAIL verdicts. The detector chain (step 06-14.6) is UNCHANGED. v18 anchor-local sampling is UNCHANGED. v19 learned verifier is UNCHANGED (weights, threshold, features all frozen). v20 expects to surface bias patterns invisible in `epoch_N_comparison.md` — patterns the rule-based and learned-classifier components cannot articulate because they lack first-person access to generator state. v20 does NOT add a new verdict label; the self-model layer produces signal (coherence score, self-prediction accuracy, bias pattern narrative), not new pass/fail categorization.

---

## 1. Why ONE upgrade, not three

The v20 task description lists three components (step 05.7, step 15, epoch-end self-attribution), but conceptually these are ONE Belinda-Li self-model intervention spanning three insertion points:
- step 05.7 is where the *self-narrative is produced* (per-candidate).
- step 15 is where the *self-narrative is audited* (per-round).
- epoch-end self-attribution is where the *failures are verbalized* (per-epoch).

Together they form the self-model loop:
```
generate → narrate → predict → external evaluate → audit coherence → self-attribute failure → close loop on next-epoch generation
```

This single loop is the v20 upgrade. Each component is structurally necessary; removing any one breaks the loop.

The corpus is now at 20 INVESTIGATIVE_SURVIVING + 6 KCD = 26 labeled examples, and the diagnostic data show v19's 1.0 agreement_rate is redundancy (not learning) and the pipeline cannot articulate why it converges to {TTT, Hochschild, free-prob, heavy-tail, complexity, elimination, visit-counter, category} families with 0 PASS. This is the bottleneck for which Belinda Li's framework is designed.

---

## 2. Belinda Li framework selection (Phase 1 → Phase 2 link)

Per `output/v19_limitation_analysis.md` §1:

| Belinda framework | Targets v19 bottleneck? | Already present in pipeline? | v20 choice |
|---|:---:|:---:|:---:|
| **(c) Self model** | **YES — directly diagnostic of opaque generator** | **NO — no component introspects on generator state** | **CHOSEN** |
| (b) User model | NO — already addressed | YES — step 14.6, step 13.5, FTS, PASS criterion all model external audit | not chosen (not the bottleneck) |
| (a) World model | NO — already addressed | YES — architecture_tools, KCD, expert_path, learned_verifier_weights all represent external state | not chosen (not the bottleneck) |

**Choice: (c) self model.** The decision is empirical:
- 20 INVESTIGATIVE_SURVIVING candidates exist; 0 PASS; the pipeline cannot articulate why it converges to this specific gap.
- Step 05 is opaque about why it produced any particular candidate (no anchor selection narrative, no slot rotation explanation, no primitive choice rationale).
- Lineage claims (anchor + distance + frontier_seed) are narrative, not audited.
- Failure attribution is external bookkeeping (AFL appends KCD; anchor_update increments counters; refit updates weights) — not first-person self-narrative.
- v19's "perfect" 1.0 agreement_rate with step 14.6 is redundancy, not learning — features f1-f4 derive from step 14.6's own boundary.

The self-model layer is the **first orthogonal verifier signal** in the pipeline: it uses the generator's *inputs* (state) rather than its *outputs* (features) as introspective signal.

---

## 3. New artifacts in v20

### 3.1 Persistent files

NONE. v20 does not add a new persistent log file. It adds per-round and per-epoch outputs only.

### 3.2 Per-round files

| Artifact | Location | Created by | Lifecycle |
|---|---|---|---|
| `rounds/round_NNN/05_7_self_model.json` | per-round | step 05.7 v20 | NEW v20 (pipeline self-explanation + self-prediction) |
| `rounds/round_NNN/15_coherence_audit.json` | per-round | step 15 v20 | NEW v20 (3 binary coherence checks + score) |

### 3.3 Per-round schema additions

The existing `05_candidate.json` adds five v20 fields:
- `v20_self_model_will_pass_step_14_6`: boolean (self-prediction echo)
- `v20_self_model_predicted_sim`: float (self-predicted sim value)
- `v20_self_model_prediction_confidence`: "high" | "medium" | "low"
- `v20_self_model_consistency_with_05_6`: "consistent" | "inconsistent"
- `v20_self_model_mechanism_narrative_summary`: string (1-2 sentences from step 05.7 mechanism_self_explanation)

### 3.4 Per-epoch outputs

| Artifact | Location | Created by | Lifecycle |
|---|---|---|---|
| `output/epoch_{N}_self_attribution.md` | per-epoch | v20 post-epoch | NEW v20 (3-section failure self-narrative + aggregate bias pattern) |

### 3.5 Stats schema additions

| Field group | Schema location | Type |
|---|---|---|
| `v20_self_model_metrics` | `output/stats_round_NNN.json` | object |
| `self_prediction_accuracy_E{N}` | per-epoch | float |
| `lineage_coherence_rate_E{N}` | per-epoch | float |
| `citation_grounding_rate_E{N}` | per-epoch | float |
| `mean_self_coherence_score_E{N}` | per-epoch | float |
| `self_model_05_6_inconsistency_count_E{N}` | per-epoch | int |

### 3.6 No new verdict labels

The v19 → v20 verdict label count stays at **12**. The self-model layer produces *introspection signal*, not new pass/fail categorization.

---

## 4. Step-by-step diff vs program_v19.md

### Step 01-04 — UNCHANGED

### Step 04.5 — UNCHANGED

### Step 05 — UNCHANGED (v18 anchor-local sampling preserved)

### Step 05.4 — UNCHANGED (v14 k-means k=25)

### Step 05.45 — UNCHANGED (v15 intra-cluster diversification)

### Step 05.5 — UNCHANGED (v17 FTS + KCD + anti-R279 cascade)

### Step 05.6 — UNCHANGED (v19 learned verifier; weights, threshold, features all preserved)

### Step 05.7 — **NEW v20**

Self-model narrative + self-prediction. Runs only on candidates that pass step 05.6. Produces `05_7_self_model.json` with:
- mechanism_self_explanation (1-paragraph first-person)
- state_attribution (anchor + yield rate + claimed distance + mode + concentration reason)
- internal_pattern_drivers (slot + slot reason + primitive + primitive reason + vocab seeds + vocab origin)
- self_prediction (will_pass + predicted_sim + confidence + reasoning)
- self_prediction_consistency_with_05_6 (consistent | inconsistent + note)

### Step 06, 06.5, 06.7, 07, 08, 09 — UNCHANGED

### Step 10 — UNCHANGED (mechanical verdict)

### Step 11, 11.5, 12 — UNCHANGED (audit)

### Step 13, 13.5 — UNCHANGED (spec + attack)

### Step 14 — UNCHANGED (cross-step coherence)

### Step 14.5 — UNCHANGED (coverage profile, once per epoch)

### Step 14.6 — UNCHANGED (external collision detection)

### Step 15 — **NEW v20**

Coherence audit. Runs every round (universal). Produces `15_coherence_audit.json` with:
- check_1_self_prediction (binary, applicable when step 14.6 fired)
- check_2_lineage_distance (binary; ±0.15 tolerance)
- check_3_citation_grounding (binary; ≥1 mechanism vocab overlap)
- self_coherence_score (mean of applicable checks)
- explanations for each check

### End-of-epoch order

```
v19 had: AFL → anchor_update → refit
v20 has: AFL → anchor_update → refit → write epoch_{N}_self_attribution.md   ← NEW v20
```

---

## 5. Forbidden-zone preservation audit

### 5.1 FORBIDDEN-TO-MODIFY zones (from §10 of program_v20.md)

| Zone | Status in v20 |
|---|---|
| Step 06 web_search | UNCHANGED (verbatim) |
| Step 07 keyword threshold ≥ 2 | UNCHANGED |
| Step 10 mechanical verdict | UNCHANGED |
| Step 12 tree-stream | UNCHANGED |
| Step 13 spec format | UNCHANGED |
| Step 13.5 attack format | UNCHANGED |
| Step 14 cross-step coherence | UNCHANGED |
| Step 14.5 coverage profile | UNCHANGED |
| Step 14.6 external collision detection | UNCHANGED |
| Step 05.4 k-means diversity filter | UNCHANGED |
| Step 05.45 intra-cluster diversification | UNCHANGED |
| Step 05.5 anti-R279 + FTS + KCD cascade | UNCHANGED |
| Step 05.6 learned verifier (v19) | UNCHANGED (weights, threshold, features frozen) |
| Step 05 anchor-local sampling (v18) | UNCHANGED |
| PASS criterion (10 signals) | UNCHANGED |

All 15 forbidden zones are preserved.

### 5.2 v20 added points

| New point | Location | Type | Affects forbidden zones? |
|---|---|---|---|
| Step 05.7 self-model | between 05.6 and 06 | Generator-side introspection | NO — additive, reads candidate but does not modify it |
| Step 15 coherence audit | after 14.6, before next round | Post-detector audit | NO — reads outputs only, does not modify any prior step |
| Epoch-end self-attribution document | after v19 refit | Post-epoch document | NO — does not modify any persistent log file |

All three insertions are **strictly additive**. No forbidden zone is touched. No v19/v18/v17 component is modified.

### 5.3 v20 changes vs v19 changes

| Component | v19 | v20 |
|---|---|---|
| Step 05.6 learned verifier | NEW addition | UNCHANGED (frozen) |
| Step 05.7 self-model | n/a | **NEW addition** |
| Step 15 coherence audit | n/a | **NEW addition** |
| Epoch-end refit_learned_verifier | NEW | UNCHANGED |
| Epoch-end self-attribution | n/a | **NEW addition** |

---

## 6. Why this differs structurally from v19's approach

### 6.1 v19 added a *data-driven classifier*

v19's learned verifier is a **post-hoc model over generator outputs**. The features (Jaccard, rare-math count, slot indicator, citation indicator, fragile pattern) are *attributes of the produced candidate*. The model is fit on past labeled outputs and predicts the next label.

This is a *world-model* upgrade (Belinda Li frame): a refined external-state representation that better predicts external classifier outcomes.

### 6.2 v20 adds a *first-person narrative*

v20's self-model is a **per-candidate first-person account** of how the candidate was produced. It references:
- Internal state (which anchor's local region, which slot rotation, which primitive selection)
- Generation mode (anchor-local vs discovery vs fallback)
- Vocabulary provenance (where each token came from)
- *Belief about own output* (will_pass prediction)

This is a *self-model* upgrade (Belinda Li frame): first-person introspection on generator state.

### 6.3 Why the two are orthogonal

Two candidates can have:
- Same features (same Jaccard, same slot, same citation) → v19 makes the same prediction.
- Different provenance (anchor-local vs discovery; primary anchor vs sub-anchor; default citation vs FTS-shifted) → v20 produces different self-narratives.

In particular, when v19's predicted_collision_prob and v20's will_pass_step_14_6 disagree (logged as `self_prediction_consistency_with_05_6 = "inconsistent"`), the corpus learns about the orthogonal failure mode that the data-fitted model can't see but the first-person account can.

This is the **first orthogonal signal** in the pipeline.

---

## 7. Anti-cheating provisions specific to v20

| Provision | Mechanism |
|---|---|
| Self-prediction is mid-round immutable | Once 05_7_self_model.json is written, step 15 reads it verbatim; no retro-edits |
| Anchor distance honesty | step 05.7 must use the actual `local_exploration_distance` from 05_candidate.json (computed by v18 anchor-local sampler) |
| Citation honesty | step 05.7 must cite the actual frontier_seed listed in 05_candidate.json |
| Self-attribution document append-only | Single write at end of epoch; no mid-epoch updates |
| No new verdict labels | Step 15 produces a numeric score, not a verdict category; PASS criterion unchanged |
| Coherence audit non-blocking | self_coherence_score < 1.0 does NOT fail a round; the verdict is determined by 06-14.6 |
| Honest self-narration | All first-person text must reference actual state values; no aspirational claims |
| Honest deviation | Self-model, audit, attribution are mechanical (no Agent spawns required); honest deviation cap of 5 Agent spawns per epoch unchanged |

---

## 8. Predicted v20 outcome under self-model layer

| Metric | E38 (v19 actual) | E39 (v20 predicted) | Mechanism |
|---|---:|---:|---|
| substantive_pass_count | 0 | 0 | structural saturation continues |
| INVESTIGATIVE_SURVIVING / 25 | 7 | **6-8** | v18 anchor-local + v19 learned verifier preserved; self-model is informational |
| step 05.7 fired count | n/a | **25** (all rounds) | new universal step |
| step 15 fired count | n/a | **25** (all rounds) | new universal step |
| self_prediction_accuracy_E39 | n/a | **0.70-0.85** | self-model trained on first-person state; modest accuracy on novel rounds |
| lineage_coherence_rate_E39 | n/a | **0.85-0.95** | most lineage claims match within ±0.15 tolerance |
| citation_grounding_rate_E39 | n/a | **0.80-0.95** | most citations ground in mechanism vocab |
| mean_self_coherence_score_E39 | n/a | **0.78-0.90** | composite |
| self_model_05_6_inconsistency_count_E39 | n/a | **1-4** | orthogonal signal moments |
| ANCHOR_R866 + R895 stale-drop at E39 end | pending | **likely fires** if both produce 0 yield in E39 (3rd consecutive epoch) |
| active_anchor_count_at_E39_end | 13 | **11-15** | -2 (stale-drop) + 0-4 (sub-anchor + discovery promotions) |
| collision_addition_rate_E39 | 0.0 | **0.0-0.04** | v19 learned verifier continues; one possible escape |
| KCD database size at E39 end | 6 | **6-7** | bounded growth |
| Score_v20 delta vs v19 | n/a | **+8 to +14** | new v20 self_model terms |
| p(no PASS \| 1% H₀) at N=1071 | n/a | **≈ 0.0000214** | matches user target |

---

## 9. v20 implementation summary

v20 inherits all v19 mechanics intact and adds:

1. **logs/policy_state.json schema bumped 1.9 → 1.10** to reflect v20 introduction at top of E39.
2. **rounds/round_NNN/05_7_self_model.json**: new per-round file with 5-section self-narrative + self-prediction.
3. **rounds/round_NNN/15_coherence_audit.json**: new per-round file with 3 binary coherence checks + score.
4. **output/epoch_{N}_self_attribution.md**: new per-epoch document with 3 failure-mode sections + aggregate bias pattern.
5. **output/stats_round_NNN.json**: new `v20_self_model_metrics` block alongside preserved v17/v18/v19 blocks.
6. **Score formula**: 5 new terms (self_prediction_accuracy×6, lineage_coherence_rate×3, citation_grounding_rate×3, mean_self_coherence_score×4, inconsistency_count/25 × 5).

All v19 fields and outputs continue to be written verbatim. v20 outputs are additive.

---

## 10. Conclusion

v20 introduces the **first self-model layer** in the niche-mining pipeline — the missing cognitive-architecture component diagnosed in `output/v19_limitation_analysis.md`. Where v17 added external state representation, v18 added prior concentration, and v19 added per-candidate classifier, v20 adds first-person introspection on generator state.

The three new components (step 05.7 self-model, step 15 coherence audit, epoch-end self-attribution document) together form a self-model loop that closes on the next epoch:
- Per-candidate self-narrative forces the generator to verbalize state.
- Per-round audit measures coherence between narrative and reality.
- Per-epoch self-attribution surfaces bias patterns invisible to external comparisons.
- Next epoch's self-predictions read the prior epoch's self-attribution document — the loop closes.

v20 promises **the first orthogonal verifier signal** — independent of step 14.6's vocabulary boundary, based on the generator's own internal state. The 1.0 agreement_rate in v19 (redundancy) is replaced by an explicit orthogonality reward (×5 on inconsistency_count / 25) in v20.

All 15 forbidden zones from v5-v19 are preserved verbatim. 0 new verdict labels. 0 modifications to the detector chain (06-14.6). v20 is the minimum surface area intervention that introduces the missing self-model framework.
