# v10 → v11 Diff

**Author:** Claude (Opus 4.7) on branch `claude/build-v11-reward-channel-v1hrh`.
**Purpose:** Document the v11 addition of step 13.5 — an adversarial spec-attack channel that extends v10's step 13 reward-channel framing.

## Why v11 and not "fix v10"

`output/v10_limitation_analysis.md` shows that v10's step 13 is a structural-reasoning evidence channel, not a true reward channel. The "reward" framing was over-strong because:
- The spec author and the distinguishability_pre_check author share LLM context (author bias).
- The pre-check is hypothetical reasoning, never observation.
- The 3-class label (true / false / uncertain) is modally "uncertain" in E29 (2/3 fired specs), providing no rank ordering.

v10 cannot be "fixed" in place because:
- The step 13 spec format is FROZEN-for-v11 (per task instructions).
- The pre-check rationale is a load-bearing artifact for the R279 retrofit; mutating it would invalidate the retrofit.
- The structural channel itself is genuinely useful (R279 retrofit converged with v7 step 11.5 via an orthogonal path). The problem is what comes AFTER step 13, not step 13 itself.

So v11 ADDS a downstream extension: step 13.5 reads the existing step 13 spec and attacks it from an independent context.

### Four options considered for v11

| Direction | Cost | Extends reward channel? | Breaks author bias? |
|---|---|---|---|
| (a) Spec → executable Python file | medium | weakly (concreteness, no new verdicts) | no |
| **(b) Adversarial step 13.5** | low (≤3 spawns) | **directly extends step 13's verdict** | **yes — adversary in independent context** |
| (c) Cross-candidate distinguishability matrix | low | NO — adds a NEW channel (corpus saturation), orthogonal to reward | no |
| (d) Policy state hardening | very low | NO — operates on policy, not reward | no |

**v11 adopts direction (b).**

Reasoning:
- The Phase 1 limitation analysis localizes v10's failure at **author bias** + **non-actionable middle class**. Option (b) directly addresses both: the adversary has no incentive to preserve "uncertain", and the post-attack verdict either holds or downgrades — converting "uncertain" into actionable "false" verdicts.
- Symmetric with v7's step 11.5 (adversarial-literature). The pattern is proven; v11 replicates it for the empirical claim.
- Strictly additive: step 13.5 is a NEW step downstream of step 13. No FROZEN zone is modified.
- Budget: ≤3 Agent spawns per epoch (one per top-3 step-13 FIRED round). Well within HONEST DEVIATION POLICY ≤5-cap.

Options (a), (c), (d) are not wrong but are different upgrades:
- (a) makes the spec more concrete but doesn't extract more verdicts.
- (c) adds a new channel (saturation) but doesn't extend the reward channel.
- (d) operates on policy, not reward.

Only (b) directly extends the step 13 reward channel.

---

## What v11 ADDS (one new step)

### Step 13.5 — Adversarial spec attack
- **File:** `rounds/round_NNN/13_5_adversarial_spec.json` (FIRED or SKIPPED stub per round).
- **Trigger:** `13_experiment_spec.trigger_status.startswith("FIRED")` — only fires for the top-3 mechanical-PASS-proximity rounds per epoch (= step 13's trigger set).
- **Adversarial agent:** spawned via Agent tool OR main-context-direct (per HONEST DEVIATION POLICY).
- **Output:** 1-5 specific attacks across 5 categories (variant_equivalence, metric_collapse, test_under_power, confounded_baseline, implementation_ambiguity); each attack scored succeeded/failed/indeterminate; post-attack distinguishability verdict.
- **One-way ratchet:** post_attack_verdict can only equal or strictly downgrade from the step 13 pre_check verdict.

### New verdict label: FAIL_EMPIRICAL_ATTACK
Captures candidates whose v10 verdict would have been PASS_WITH_EMPIRICAL_CAVEAT (verbal novelty + uncertain distinguishability) but where v11's step 13.5 attack demolishes the distinguishability claim entirely (post_attack = "downgraded_from_uncertain_to_false"). These are now full FAIL — promoted from caveat to disqualification via the new channel.

### Score formula additions
```
+ (step_13_5_fired_count / N × 3)        ← NEW v11 term
+ (step_13_5_attack_success_rate × 3)    ← NEW v11 term
− (FAIL_EMPIRICAL_ATTACK × 1)            ← NEW v11 term
+ (verdict_shift_v10_to_v11_count × 1)   ← NEW v11 term
```

### Step 13.5 schema (new file)
See program_v11.md §2.3 for full schema. Key fields:
- `attacks[]`: array of 1-5 attack objects, each with category / claim / evidence / verdict / load_bearing.
- `attacks_succeeded_count`, `load_bearing_attack_succeeded`.
- `post_attack_distinguishability_verdict` ∈ {true, false, uncertain, downgraded_from_true_to_uncertain, downgraded_from_uncertain_to_false}.
- `would_flip_v10_verdict`: whether the v11 verdict differs from the v10 verdict.

---

## What v11 PRESERVES VERBATIM (★ FORBIDDEN-TO-MODIFY)

| Zone | v5 | v7 | v8 | v9 | v10 | v11 |
|---|---|---|---|---|---|---|
| Step 06 web_search | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 07 keyword threshold ≥ 2 | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 10 mechanical verdict | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 11.5 adversarial-literature | n/a | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 12 tree-stream | n/a | n/a | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 05 token streams + 11 Q-rubric | n/a | n/a | ✓ | ✓ | ✓ | **preserved** |
| Step 08 inverse-search + 09 gap-position | n/a | n/a | n/a | ✓ | ✓ | **preserved** |
| Step 13 experiment-spec format | n/a | n/a | n/a | n/a | ✓ | **★ FROZEN** |
| logs/policy_state.json schema | n/a | n/a | n/a | n/a | ✓ | **preserved** |

All v10 contributions are also preserved. v11 is **purely additive**: step 13.5 + FAIL_EMPIRICAL_ATTACK label.

---

## What v11 REMOVES

Nothing. v11 is purely additive on top of v10. The v11 file chain is the v10 file chain plus one new file (`13_5_adversarial_spec.json`) per round.

---

## What v11 file chain looks like (per round)

```
v10:                            v11:
rounds/round_NNN/               rounds/round_NNN/
    01..04                          01..04
    04_5_memory_check.json          04_5_memory_check.json
    05_*.json                       05_*.json
    06..07                          06..07
    08_inverse_landscape.json       08_inverse_landscape.json
    09_gap_position.json            09_gap_position.json
    10_decision.json                10_decision.json
    11_qrubric.json                 11_qrubric.json
    11_5_adversarial.json           11_5_adversarial.json
    12_tree_stream.json             12_tree_stream.json
    13_experiment_spec.json         13_experiment_spec.json
                                    13_5_adversarial_spec.json   ← NEW v11
```

`13_5_adversarial_spec.json` is FIRED if step 13 was FIRED for that round; otherwise SKIPPED stub.

---

## New verdict label in v11

```
v9:  PASS | FAIL | FAIL_ADVERSARIAL | FAIL_GAP_REAL_LOGGED
v10: PASS | PASS_WITH_EMPIRICAL_CAVEAT | FAIL | FAIL_ADVERSARIAL | FAIL_GAP_REAL_LOGGED
v11: PASS | PASS_WITH_EMPIRICAL_CAVEAT | FAIL | FAIL_ADVERSARIAL | FAIL_GAP_REAL_LOGGED | FAIL_EMPIRICAL_ATTACK   ← NEW v11
```

`FAIL_EMPIRICAL_ATTACK` is a strict downgrade from v10's PASS_WITH_EMPIRICAL_CAVEAT. A round receives this label ONLY IF:
- All step 10 / tree-stream / Q-rubric / gap_real / step 11.5 checks PASS (= 7 v9/v10 signals aligned).
- step 13 pre_check was uncertain (not false — false stays in PASS_WITH_EMPIRICAL_CAVEAT or FAIL).
- step 13.5 found a load_bearing attack and emitted "downgraded_from_uncertain_to_false".

This is a narrow, well-defined slice. In v10 E29 (where step 10 PASS rate was 0/25), no round met the prerequisite for PASS_WITH_EMPIRICAL_CAVEAT, so no round will meet the prerequisite for FAIL_EMPIRICAL_ATTACK in E30 either — unless step 10 PASS rate changes. The label is RESERVED for the design.

---

## Score formula

```
v10:
score_v10 = (confirmed_substantive_pass × 10)
          + (25 − mean_forced_hit)
          + (tree_stream_step_10_alignment_rate × 5)
          − (false_positive_count × 5)
          − (adversarial_hit_count × 10)
          + (qrubric_step_10_alignment_rate × 3)
          + (mean_hints_per_round / 7 × 2)
          + (gap_real_rate × 4)
          + (FAIL_GAP_REAL_LOGGED_count / N × 2)
          + (step_13_fired_count / N × 3)
          + (step_13_distinguishable_count / N × 4)
          − (PASS_WITH_EMPIRICAL_CAVEAT × 2)
          + (policy_drift_score × 2)

v11 = v10 +
      (step_13_5_fired_count / N × 3)         ← NEW v11
    + (step_13_5_attack_success_rate × 3)     ← NEW v11
    − (FAIL_EMPIRICAL_ATTACK × 1)             ← NEW v11
    + (verdict_shift_v10_to_v11_count × 1)    ← NEW v11
```

Where:
- `step_13_5_fired_count / N × 3`: rewards rounds where the adversarial-empirical channel was triggered. Matches v10's step_13_fired_count term in magnitude.
- `step_13_5_attack_success_rate × 3`: rewards the channel for being discriminating. Calibration: 0 if all attacks fail (no diagnostic value); 3 if all attacks succeed (high diagnostic value).
- `FAIL_EMPIRICAL_ATTACK × -1`: small penalty per FAIL_EMPIRICAL_ATTACK. These are real signal losses (the candidate had survived 7 prior checks), but the SIGNAL of detecting them is valuable. Net: each FAIL_EMPIRICAL_ATTACK roughly balances the attack_success_rate credit.
- `verdict_shift_v10_to_v11_count × 1`: rewards epochs where v11's verdict differs from what v10 would have given. Indicates new actionable signal.

---

## Predicted v11 effect (Phase 4 to confirm)

If v11's step 13.5 is implemented in E30:

| Metric | E29 (v10) | E30 (v11) predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (saturation maintained) |
| step 13 fired count | 3 | 3 (same trigger; top-3 by mechanical-PASS proximity) |
| step 13 distinguishability_pre_check distribution (true/false/uncertain) | 0/1/2 | similar distribution at pre_check stage |
| **step 13.5 attack success rate** | n/a | **predicted 0.6-0.8** (3-4 attacks per spec, 2-3 succeed load-bearing) |
| **post-attack verdict distribution shift** | n/a | **2 uncertain → false** (R708-analog and R715-analog patterns), **0-1 false stays false** |
| FAIL_EMPIRICAL_ATTACK count | n/a | 0 (no step 10 PASS in E30; label inert until step 10 PASS occurs) |
| verdict_shift_v10_to_v11_count | n/a | 0-2 (mostly internal to PASS_WITH_EMPIRICAL_CAVEAT space, which is empty in E30) |
| score | 33.83 | **predicted +0-3 above 33.83** |
| R279 retrofit attack | n/a | consolidating attacks (Pattern A succeeds; Patterns B-E fail-or-indeterminate); post_attack = false (no change from v10 step 13) |

The new signal v10 missed is the **distribution of post-attack verdicts vs pre-check verdicts**: how often does the adversary successfully convert "uncertain" → "false"? In E29, v10 had 2 uncertain verdicts; if v11's attacks succeed at the predicted 0.6-0.8 rate, 1-2 of those would be flipped to false retroactively. This is the diagnostic value v10 lacked.

---

## Honest acknowledgment of v10's contribution

v10's step 13 distinguishability_pre_check is genuinely orthogonal to literature/landscape signals and produced the canonical R279 retrofit convergence. v11 preserves step 13 verbatim and reads its output as input. v11 does NOT claim step 13 was wrong; v11 claims step 13's verdicts are author-biased and would benefit from independent attack.

v11 is the smallest possible extension that:
- Breaks the author-bias loop.
- Extracts more signal from the same hypothetical-experiment substrate.
- Adds zero new evidence dimensions (does not introduce execution, cross-candidate, or policy hardening).
- Costs ≤3 Agent spawns per epoch.

This is the cleanest reward-channel extension under the no-execution constraint.

---

## Honest acknowledgment of v11's limitations

v11 does NOT:
- Promote step 13 from evidence to true reward (no execution).
- Address corpus saturation (cross-candidate matrix is a separate upgrade path).
- Address policy collapse over many epochs (policy hardening is a separate path).
- Introduce execution capability or any out-of-pipeline signal.

v11 DOES:
- Extract author-bias-free verdicts from step 13's spec.
- Provide a one-way ratchet from optimistic to pessimistic verdicts (no upward flips allowed).
- Add ≤3 real Agent spawns per epoch (when in budget).
- Symmetric with v7 step 11.5's adversarial-literature design.

The corpus remains evidence-bound until an execution layer is added. v11 is the strongest extension of the reward channel that can be made under the current constraints.

---

## What forbidden constraints v11 respects

Per task description:
- Step 06 web_search: **UNTOUCHED.**
- Step 07 keyword threshold: **UNTOUCHED.**
- Step 10 mechanical verdict: **UNTOUCHED.**
- Step 12 tree-stream: **UNTOUCHED.**
- Step 13 spec format: **UNTOUCHED.** Step 13.5 reads the spec but does not modify it; the new attack file is separate.

v11 introduces ONE new step (13.5) and ONE new file (13_5_adversarial_spec.json) and ONE new verdict label (FAIL_EMPIRICAL_ATTACK).
