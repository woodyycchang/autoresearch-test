# v11 → v12 Diff

**Author:** Claude (Opus 4.7) on branch `claude/build-v12-adversarial-6U2QQ`.
**Purpose:** Document the v12 addition of step 05.5 — a generator-side mechanical filter that rejects R279-pattern candidates BEFORE step 06.

## Why v12 and not "fix v11"

`output/v11_limitation_analysis.md` shows that v11's verifier chain works (step 13.5 attack succeeds 11/14 across E30 + R279 retrofit). The bottleneck is on the GENERATOR side, not the verifier side:

- Every step-13-FIRED candidate in the corpus (R279, R708, R715, R725, R735, R741, R744) is an R279-pattern variant (fixed scalar/diagonal/functional prior on an existing learnable parameter).
- Step 05 has been UNCHANGED since v8 (R651), so it keeps producing the same candidate quality.
- v11's adversarial step 13.5 is a sharpened KILL channel; it does not change the GENERATE side.

v11 cannot be "fixed" in place because:
- Step 13.5 is FROZEN per v12 task constraints.
- The pipeline's verifier-side upgrades (v7-v11) have saturated on verifier discrimination but not generator diversity.
- The asymmetry "can KILL bad / can't GENERATE good" is unchanged by v11.

So v12 ADDS a NEW generator-side check: step 05.5 reads `05_candidate.json` and applies a mechanical structural classifier. R279-pattern candidates are rejected BEFORE step 06, forcing step 05 to regenerate with architectural-topology candidates.

### Four options considered for v12

| Direction | Cost | Generator-side? | Mechanical/deterministic? | Addresses R279-pattern saturation? |
|---|---|---|---|---|
| (a) Distinguishability-conditioned generation | medium | partial (output check) | partial (claim is LLM-asserted) | partial (post-hoc claim) |
| **(b) Anti-R279 candidate filter** | **low** | **yes (pre-search filter)** | **yes (3-question deterministic classifier)** | **directly (rejects R279-pattern outright)** |
| (c) Adversarial candidate generator | medium | yes (parallel agent) | no (LLM context) | indirect |
| (d) Empirical-result-conditioned generation | low | yes (prompt augment) | no (LLM context) | indirect (already attempted via policy_state in v10) |

**v12 adopts direction (b).**

Reasoning:
- Phase 1 limitation analysis (`output/v11_limitation_analysis.md` §3) catalogs 7/7 step-13-FIRED candidates as R279-pattern. The diagnosis is clear: step 05's 4-sub-mechanism decomposition path naturally lands on R279-pattern (existing learnable param → new functional → ranking → action).
- Option (b) is mechanical and deterministic. It is checkable from `05_candidate.json` text alone (no Agent spawn needed) and produces a single TRUE/FALSE classification per question.
- Option (b) is symmetric with step 07 (keyword threshold) and step 09 (gap-position) — all mechanical filters with deterministic verdicts firing before LLM-based verifier steps.
- Option (b) operates PRE-search. R279-pattern candidates do not consume step 06-13.5 budget; they are rejected at the cheapest checkpoint and trigger regeneration with explicit anti-R279 instruction.
- Options (a) / (c) / (d) all rely on LLM judgment somewhere in the loop. The Phase 1 diagnosis showed that LLM-judgment-based interventions (v10's policy_state, v11's adversarial agent) succeed at the LOCAL judgment but do not move the candidate population off R279-pattern. The structural classifier of (b) is the most direct intervention on the generator's recipe.

Only (b) directly intervenes on step 05's recipe at the structural level.

---

## What v12 ADDS (one new step + one new artifact + one new verdict label)

### Step 05.5 — Anti-R279 mechanical structural filter
- **File:** `rounds/round_NNN/05_5_pattern_filter.json` (every round; FIRED).
- **Trigger:** every round, no SKIP path. Runs AFTER step 05 produces `05_candidate.json` and BEFORE step 06 web_search.
- **Classifier:** 3-question deterministic structural classifier (Q1: new learnable module? Q2: new inter-layer connection? Q3: new layer topology?). All NO → R279_pattern = TRUE → REJECTED.
- **Regeneration protocol:** when REJECTED, regenerate step 05 with explicit anti-R279 instruction; re-run step 05.5; up to 2 regenerations; if all 3 attempts produce R279-pattern, log policy_override_step_05_5 and accept the 3rd attempt.
- **Output:** PASS / REJECTED_R279_PATTERN verdict + per-question evidence + regeneration log.

### New verdict label: REJECTED_R279_PATTERN
Captures candidates where step 05's recipe lands on R279-pattern AND two regenerations also produce R279-pattern. These candidates are REJECTED at step 05.5 (do not reach step 06). The verdict is logged for diagnostic value (signal that the generator is stuck on R279-pattern).

### Score formula additions
```
+ (step_05_5_rejection_rate × 3)             ← NEW v12 term
+ (architectural_topology_change_rate × 4)   ← NEW v12 term
+ (regeneration_success_rate × 2)            ← NEW v12 term
− (REJECTED_R279_PATTERN_count × 1)          ← NEW v12 term
```

### Step 05.5 schema (new file)
See program_v12.md §2.3 for full schema. Key fields:
- `structural_questions`: Q1/Q2/Q3 booleans with per-question 1-sentence evidence pointers.
- `architectural_topology_change`: Q1 OR Q2 OR Q3.
- `R279_pattern`: NOT architectural_topology_change.
- `verdict`: PASS | REJECTED_R279_PATTERN.
- `regeneration_attempted`, `regenerated_candidate_summary`, `regenerated_candidate_passed_step_05_5`.
- `post_filter_candidate_used_downstream`.

---

## What v12 PRESERVES VERBATIM (★ FORBIDDEN-TO-MODIFY)

| Zone | v5 | v7 | v8 | v9 | v10 | v11 | v12 |
|---|---|---|---|---|---|---|---|
| Step 06 web_search | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 07 keyword threshold ≥ 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 10 mechanical verdict | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 11.5 adversarial-literature | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 12 tree-stream | n/a | n/a | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 05 token streams + 11 Q-rubric | n/a | n/a | ✓ | ✓ | ✓ | ✓ | **preserved** |
| Step 08 inverse-search + 09 gap-position | n/a | n/a | n/a | ✓ | ✓ | ✓ | **preserved** |
| Step 13 experiment-spec format | n/a | n/a | n/a | n/a | ✓ | ✓ | **★ FROZEN** |
| Step 13.5 attack format | n/a | n/a | n/a | n/a | n/a | ✓ | **★ FROZEN** |
| logs/policy_state.json schema | n/a | n/a | n/a | n/a | ✓ | ✓ | **preserved** |

All v10/v11 contributions are also preserved. v12 is **purely additive**: step 05.5 + REJECTED_R279_PATTERN label.

---

## What v12 REMOVES

Nothing. v12 is purely additive on top of v11. The v12 file chain is the v11 file chain plus one new file (`05_5_pattern_filter.json`) per round.

---

## What v12 file chain looks like (per round)

```
v11:                            v12:
rounds/round_NNN/               rounds/round_NNN/
    01..04                          01..04
    04_5_memory_check.json          04_5_memory_check.json
    05_*.json                       05_*.json
                                    05_5_pattern_filter.json   ← NEW v12
    06..07                          06..07
    08_inverse_landscape.json       08_inverse_landscape.json
    09_gap_position.json            09_gap_position.json
    10_decision.json                10_decision.json
    11_qrubric.json                 11_qrubric.json
    11_5_adversarial.json           11_5_adversarial.json
    12_tree_stream.json             12_tree_stream.json
    13_experiment_spec.json         13_experiment_spec.json
    13_5_adversarial_spec.json      13_5_adversarial_spec.json
```

`05_5_pattern_filter.json` is FIRED on every round (no SKIP path). The downstream files (06 onward) operate on the post-filter candidate (which is either the first-attempt step 05 output if it passed, or the regenerated candidate if first attempt was rejected, or the post-2nd-regeneration candidate with policy_override if both regenerations failed).

---

## New verdict label in v12

```
v9:  PASS | FAIL | FAIL_ADVERSARIAL | FAIL_GAP_REAL_LOGGED
v10: PASS | PASS_WITH_EMPIRICAL_CAVEAT | FAIL | FAIL_ADVERSARIAL | FAIL_GAP_REAL_LOGGED
v11: + FAIL_EMPIRICAL_ATTACK
v12: + REJECTED_R279_PATTERN   ← NEW v12
```

`REJECTED_R279_PATTERN` is a separate category from FAIL. It applies ONLY IF:
- step 05.5 verdict at first attempt was REJECTED_R279_PATTERN, AND
- regeneration was attempted (at least once), AND
- 2 consecutive regenerations also produced R279-pattern (or policy_override was logged after 2 failed regenerations and the 3rd attempt was accepted).

This is a narrow, well-defined slice. The label is RESERVED for cases where step 05 truly cannot escape R279-pattern even with explicit instruction. If the regeneration succeeds (1st or 2nd attempt produces architectural-topology candidate), the round proceeds through steps 06-13.5 normally with the regenerated candidate, and the final verdict is computed from those downstream signals (FAIL / PASS / etc.).

---

## Score formula

```
v11:
score_v11 = (confirmed_substantive_pass × 10)
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
          + (step_13_5_fired_count / N × 3)
          + (step_13_5_attack_success_rate × 3)
          − (FAIL_EMPIRICAL_ATTACK × 1)
          + (verdict_shift_v10_to_v11_count × 1)

v12 = v11 +
      (step_05_5_rejection_rate × 3)         ← NEW v12
    + (architectural_topology_change_rate × 4)  ← NEW v12
    + (regeneration_success_rate × 2)        ← NEW v12
    − (REJECTED_R279_PATTERN_count × 1)      ← NEW v12
```

Where:
- `step_05_5_rejection_rate × 3`: rewards rounds where the classifier correctly identifies R279-pattern at first attempt. Calibration: 0 if no rejections (step 05 escaped R279 unprompted — falsifies Phase 1 diagnosis); 3 if all rejected (every candidate was R279-pattern, generator is stuck).
- `architectural_topology_change_rate × 4`: rewards the post-filter candidate population. Highest weight because this is the v12 goal. Calibration: 0 if no candidate passes step 05.5 even after regeneration (generator cannot produce architectural-topology); 4 if all pass.
- `regeneration_success_rate × 2`: rewards the step 05 generator's ability to escape R279-pattern when instructed. Calibration: 0 if every regeneration also fails (generator is stuck even with explicit prompt); 2 if regeneration always succeeds on first retry.
- `REJECTED_R279_PATTERN_count × -1`: small penalty per terminal R279-pattern verdict. These are diagnostically informative (signal that the generator is stuck) but represent the failure mode v12 wants to detect, so a small penalty is warranted.

---

## Predicted v12 effect (Phase 4 to confirm)

If v12's step 05.5 is implemented in E31:

| Metric | E30 (v11) | E31 (v12) predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (saturation maintained at N=871) |
| **step 05.5 first-attempt REJECTED count** | n/a | **predicted 10-18/25** (R279-pattern dominance in corpus; classifier should reject ~50-70%) |
| **regeneration_success_rate** | n/a | **predicted 0.5-0.8** (LLM can escape R279-pattern when explicitly instructed, but not always on first retry) |
| **architectural_topology_change_rate (final candidate)** | n/a | **predicted 0.8-1.0** (most rounds end up with architectural candidate after regeneration) |
| mean kw forced-hit | 2.84 | **predicted 3.0-3.5** (architectural candidates share keywords with major architectural papers; UP from v11 baseline) |
| step 13 fired count | 3/25 | **predicted 0-3/25** (depends on whether architectural candidates pass mechanical-PASS proximity ranking; could be 0 if all are killed by step 10 keyword overlap) |
| step 13 distinguishability_pre_check distribution | 0/3 true / 3 uncertain / 0 false | **predicted shift if step 13 fires:** more "uncertain" or "true" (architectural candidates have more genuine distinguishability claims) |
| step 13.5 attack_success_rate | 0.667 load-bearing | **predicted DROP** (architectural candidates harder to demolish with variant_equivalence; R744-style rebuttals more common) |
| REJECTED_R279_PATTERN final verdict count | n/a | **predicted 0-3/25** (rare; only when 2 regenerations also fail) |
| verdict_shift_v11_to_v12_count | n/a | **predicted 10-18/25** (rounds where the candidate would have been different under v12 → different downstream signals → potentially different verdict) |
| score | 35.91 | **predicted +1 to +5 above 35.91** |
| R279 retrofit step-05.5 | n/a | REJECTED_R279_PATTERN (canonical R279-pattern; classifier should correctly identify) |

The new signal v11 missed is the **candidate population shift**: how often does step 05.5 reject R279-pattern, and how often does regeneration produce a genuinely-architectural candidate? In E30, step 05 produced R279-pattern candidates in 7/7 step-13-FIRED rounds; if v12's classifier is calibrated, it should reject ~50-70% of first attempts, and regeneration should escape R279-pattern in most cases.

---

## Honest acknowledgment of v11's contribution

v11's step 13.5 adversarial-empirical attack is genuinely orthogonal to literature/structural signals and produced canonical convergence on R279 (4/4 attacks succeeded + R735/R741 downgraded). v12 preserves step 13.5 verbatim and reads its output as input. v12 does NOT claim step 13.5 was wrong; v12 claims step 13.5 cannot move the candidate population off R279-pattern (only step 05.5 can).

v12 is the smallest possible extension that:
- Adds a generator-side mechanical filter.
- Forces step 05 to retry on architectural-topology when R279-pattern is detected.
- Adds zero new evidence dimensions on the verifier side (does not introduce execution, cross-candidate, or policy hardening).
- Costs 0 Agent spawns per epoch (classifier is deterministic from text).
- Symmetric with step 07 (keyword threshold) and step 09 (gap-position) — mechanical filters.

This is the cleanest generator-side intervention under the no-execution constraint.

---

## Honest acknowledgment of v12's limitations

v12 does NOT:
- Promote step 05 to a true architectural-topology generator (the regeneration relies on LLM context).
- Address PASS rate (architectural-topology candidates may have higher kw forced-hit and fail step 10).
- Address corpus saturation (cross-candidate matrix is a separate upgrade path).
- Address policy collapse over many epochs (policy hardening is a separate path).
- Introduce execution capability or any out-of-pipeline signal.

v12 DOES:
- Add a mechanical, deterministic, auditable structural classifier at step 05.5.
- Force step 05 to retry on architectural-topology when R279-pattern is detected.
- Pre-search rejection saving step 06-13.5 budget on R279-pattern candidates.
- Provide a one-way ratchet (R279-pattern verdict cannot be flipped post-hoc; only override via policy log).
- Add 4 new score terms tracking generator-side discrimination, post-filter quality, regeneration success, and terminal-R279 detection.

The corpus remains evidence-bound until an execution layer is added. v12 is the strongest generator-side intervention that can be made under the current constraints.

---

## What forbidden constraints v12 respects

Per task description:
- Step 06 web_search: **UNTOUCHED.**
- Step 07 keyword threshold: **UNTOUCHED.**
- Step 10 mechanical verdict: **UNTOUCHED.**
- Step 12 tree-stream: **UNTOUCHED.**
- Step 13 spec format: **UNTOUCHED.** Step 05.5 doesn't read it.
- Step 13.5 attack format: **UNTOUCHED.** Step 05.5 doesn't read it.

v12 introduces ONE new step (05.5) and ONE new file (05_5_pattern_filter.json) and ONE new verdict label (REJECTED_R279_PATTERN). Step 05's output format is unchanged; step 05.5 only READS `05_candidate.json` and emits a separate file.

---

## Validation against `output/v11_limitation_analysis.md` predictions

| Prediction in v11 analysis | v12 implementation |
|---|---|
| step 05.5 fires R279-pattern rejection at non-zero rate | Mandatory: every round runs step 05.5. Rejection logic is mechanical from 3-question classifier. |
| step 13.5 attack success rate DROPS on post-filter candidates | Direct test: E31's step 13.5 attack success rate will be compared to E30's 0.667 baseline. |
| Mean kw forced-hit goes UP | Direct test: E31's mean_forced_hit will be compared to E30's 2.84 baseline. |
| score_v12 predicted +0-3 above 35.91 | Score formula adds 4 new terms; net effect computed in epoch31_comparison.md. |
| R279 retrofit classifies as REJECTED_R279_PATTERN | Mandatory retrofit: rounds/round_279/05_5_pattern_filter.json with Q1=Q2=Q3=NO and verdict=REJECTED_R279_PATTERN. |

If the Phase 1 diagnosis is correct, these predictions hold. If not, the deviations themselves are diagnostically informative (e.g., step 05.5 rejecting 0/25 would falsify the R279-pattern dominance claim).
