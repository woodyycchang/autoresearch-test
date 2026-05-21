# program_v13.md
## Niche-Mining Pipeline — v13: Cross-Step Coherence Detector (step 14 Post-13.5 Synthesis)

This file extends the **v12 base pipeline** (= v11 base + step 05.5 anti-R279 mechanical structural filter) with ONE NEW structural upgrade that addresses v12's diagnosed limitation (see `output/v12_limitation_analysis.md`):

> v12 successfully shifted the candidate population to architectural-topology-change (24/25 in E31, 0.96 rate) and surfaced — for the first time in corpus history — two attack-rebutted candidates (R756 SU(2)-equivariant + R770 tropical-attention) where step 13.5's adversarial-empirical attacks were REBUTTED via genuine architectural-distinguishability arguments. But R756/R770 still received `step 10 FAIL` because step 06 web_search returns prior architectural papers with ≥2 keyword overlap on architectural vocabulary ("module", "transformation", "attention", "layer") — vocabulary that v12's regeneration prompt explicitly requires candidates to use. Step 10 measures FRAMING/NAMING similarity; step 13.5 measures MECHANISM distinguishability. These are different axes, and v12 surfaced their divergence for the first time. The v12 pipeline has no downstream synthesis registering this disagreement. v13 introduces step 14: a deterministic cross-step coherence detector that fires when step 10 FAIL + step 13.5 PASS-via-rebuttal, and labels the round INVESTIGATIVE_CANDIDATE (a new verdict label, NOT a substantive PASS).

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

The following zones are **FROZEN** verbatim from v5 / v7 / v8 / v9 / v10 / v11 / v12:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL — keyword ∪ semantic ∪ functional)
- **Step 12 tree-stream** (v8 helper + per-hint solver + conservative synthesis)
- **Step 13 spec format** (v10 contribution; v13 reads it but does not modify it)
- **Step 13.5 attack format** (v11 contribution; v13 reads it but does not modify it)
- **Step 05.5 anti-R279 mechanical filter** (v12 contribution; v13 reads it but does not modify it)
- **All v8 components** (step 05 token streams, step 11 Q-rubric)
- **All v9 components** (step 08 inverse-search, step 09 gap-position)
- **All v10 components** (step 13 spec generation, `logs/policy_state.json` policy update, PASS_WITH_EMPIRICAL_CAVEAT verdict label)
- **All v11 components** (step 13.5 attack, FAIL_EMPIRICAL_ATTACK verdict label)
- **All v12 components** (step 05.5 anti-R279 filter, REJECTED_R279_PATTERN verdict label)

v13 is **strictly additive**. It ADDS step 14 between step 13.5 and the final verdict synthesis. It does NOT modify any prior file, any prior step, or any prior verdict label.

---

## 0. Why cross-step coherence and not something else

### 0.1 The v12 limitation diagnosed in `output/v12_limitation_analysis.md`

v12 added step 05.5 (anti-R279 mechanical filter). The filter worked — 16/25 first-attempt R279-pattern rejections in E31, 0.96 final architectural-topology rate, regeneration success 0.9375. For the first time, the architectural-distinct candidate quadrant was populated (R756 SU(2)-equivariant + R770 tropical-attention with step 13.5 post_attack_distinguishability_verdict = TRUE).

But the architectural-distinct candidates STILL die at step 10 because v12's regeneration prompt forces candidates to use architectural vocabulary ("module", "attention", "layer", "pathway", "bridge") — vocabulary that necessarily overlaps with prior ML architecture papers, triggering step 07's keyword threshold and step 10's mechanical FAIL.

**Step 10 axis (kw overlap) and step 13.5 axis (mechanism distinguishability) are NOT the same axis.** v12 surfaced this for the first time because v12 was the first program to populate the architectural-distinct candidate quadrant. Pre-v12, the candidate population was uniformly R279-pattern; step 10 and step 13.5 BOTH said FAIL and APPEARED to align.

The v12 pipeline has no downstream synthesis registering the disagreement when step 10 says FAIL + step 13.5 says PASS-via-rebuttal. R756/R770 are labeled `v12_FAIL` indistinguishably from the 22 other v12_FAIL rounds.

### 0.2 The four candidate v13 upgrades

| Option | Where it intervenes | Cost | Touches FORBIDDEN zones? | Addresses v12 limitation? |
|---|---|---|---|---|
| **(a) Cross-step coherence detector** | step 14 (NEW; post-13.5; reads-only) | low | **NO** | **directly — registers axis divergence** |
| (b) Attack-rebuttal-feedback loop | step 05.5 modification | medium | YES (step 05.5 FORBIDDEN) | indirectly |
| (c) Mechanism-axis decomposition | step 05.5 modification | low | YES (step 05.5 FORBIDDEN) | partial (generator-side; doesn't reconcile downstream) |
| (d) Distinguishability-by-construction at output | step 05 prompt modification | low | NO (step 05 prompt is not in FORBIDDEN list) | does NOT address axis divergence |

**v13 adopts direction (a).** See `output/v12_to_v13_diff.md` §0 for the full cost/benefit analysis.

### 0.3 Symmetry with prior mechanical filters and cross-axis steps

v13's step 14 is symmetric with the prior corpus's deterministic mechanical filters:
- **Step 07** (v5; keyword threshold ≥ 2): deterministic check on `06_search_raw.json`, decides forced-hit status.
- **Step 09** (v9; gap_position): deterministic rule applied to `08_inverse_landscape.json`, decides gap_real status.
- **Step 05.5** (v12; anti-R279): deterministic structural classifier applied to `05_candidate.json`, decides R279_pattern status.
- **Step 14 (NEW v13; cross-step coherence):** deterministic 2-input check on `10_decision.json` + `13_5_adversarial_spec.json`, decides INCOHERENT vs COHERENT.

All four fire deterministically. v13's step 14 is the first cross-step synthesis (reads outputs from TWO prior steps, not one).

### 0.4 What v13 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§9 below) — UNCHANGED.
- v8 step 05 token-stream FORMAT — UNCHANGED.
- v10 step 13 / v11 step 13.5 — UNCHANGED.
- v12 step 05.5 anti-R279 filter — UNCHANGED.
- `logs/policy_state.json` schema — UNCHANGED.
- PASS criterion floor (still requires all 10 prior signals) — UNCHANGED; v13 adds NO new PASS gate.
- Cumulative N_verified counting protocol — UNCHANGED.
- Step 10 verdict for any round — UNCHANGED. Step 14 does not override step 10; it ADDS a new label.

---

## 1. File chain (v12 + one addition)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json

    05_prompt_tokens.json
    05_sample_tokens.json
    05_task_tokens.json
    05_candidate.json
    05_5_pattern_filter.json          ★ FROZEN (v12 contribution; FORBIDDEN per v13 task)

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN
    06_7_functional_hits.json        ★ FROZEN
    07_hit_miss.json                 ★ FROZEN

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json                 ★ FROZEN

    11_qrubric.json
    11_audit.json
    12_tree_stream.json              ★ FROZEN
    12_verification.json
    11_5_adversarial.json            ★ FROZEN

    13_experiment_spec.json          ★ FROZEN
    13_5_adversarial_spec.json       ★ FROZEN

    14_cross_step_coherence.json     ← NEW v13 (per-round; FIRED only when trigger met; SKIPPED otherwise)
```

Side-channel (UNCHANGED from v12):
```
logs/policy_state.json
```

A v13 round MUST contain all v12 files PLUS `14_cross_step_coherence.json`. Step 14's verdict is recorded as either `FIRED` (step 13.5 FIRED + post_attack = TRUE + step 10 = FAIL → INVESTIGATIVE_CANDIDATE label) or `SKIPPED` (trigger condition not met).

---

## 2. Step 14 — Cross-step coherence detector (NEW v13)

### 2.1 What step 14 does

Step 14 is the first **cross-step coherence detector** in the corpus. It runs AFTER step 13.5 produces `13_5_adversarial_spec.json` and BEFORE the final v13_verdict synthesis. The detector reads two upstream artifacts:

```
cross_step_coherence_check(step_10_verdict, step_13_5_verdict):
    if step_13_5.trigger_status != "FIRED":
        return SKIPPED (cannot evaluate axis divergence if step 13.5 didn't run)

    step_10_says_FAIL = (step_10.verdict == "FAIL" AND step_10.total_hits >= 1)
    step_13_5_says_PASS = (step_13_5.post_attack_distinguishability_verdict == "true"
                          AND step_13_5.load_bearing_attack_succeeded == false)

    if step_10_says_FAIL AND step_13_5_says_PASS:
        return INCOHERENT → INVESTIGATIVE_CANDIDATE
    else:
        return COHERENT → no new label
```

Operationalization (deterministic from upstream JSON):
- `step_10_says_FAIL` = `10_decision.json.verdict == "FAIL"` AND `10_decision.json.total_hits >= 1`.
- `step_13_5_says_PASS` = `13_5_adversarial_spec.json.post_attack_distinguishability_verdict == "true"` AND `13_5_adversarial_spec.json.load_bearing_attack_succeeded == false`.
- `INCOHERENT` = both conditions met (step 10 disagrees with step 13.5 on the architectural-quadrant candidate).
- `COHERENT` = step 10 and step 13.5 agree (both FAIL, both PASS, or step 13.5 didn't fire).

If `INCOHERENT` → step 14 verdict = `FIRED_INVESTIGATIVE_CANDIDATE`.
If `COHERENT` (or step 13.5 didn't fire) → step 14 verdict = `SKIPPED_COHERENT` or `SKIPPED_NOT_APPLICABLE`.

### 2.2 Step 14 trigger logic

```
trigger_step_14 = (step_13_5.trigger_status == "FIRED")
```

Step 14 evaluates only on rounds where step 13.5 actually fired. On rounds where step 13.5 was SKIPPED (i.e., step 13 was SKIPPED for not being in top-3 mechanical-PASS proximity), step 14 records `trigger_status = SKIPPED_NOT_APPLICABLE`.

**Every v13 round produces a `14_cross_step_coherence.json` file** — either FIRED or SKIPPED. The file is mandatory.

### 2.3 Step 14 schema

```json
{
  "round": "NNN",
  "epoch": 13,
  "trigger_status": "FIRED | SKIPPED_COHERENT | SKIPPED_NOT_APPLICABLE",
  "trigger_reason": "<one-line explanation: why step 14 fired or didn't>",
  "step_10_input": {
    "verdict": "FAIL | PASS",
    "total_hits": <int>,
    "channels": {"keyword": <int>, "semantic": <int>, "functional": <int>}
  },
  "step_13_5_input": {
    "trigger_status": "FIRED | SKIPPED",
    "post_attack_distinguishability_verdict": "true | false | uncertain | <null if SKIPPED>",
    "load_bearing_attack_succeeded": true | false | <null>,
    "attacks_succeeded_count": <int>,
    "attacks_failed_count": <int>,
    "spec_survives_attack": true | false | <null>
  },
  "coherence_check": {
    "step_10_says": "FAIL | PASS",
    "step_13_5_says": "PASS | FAIL | UNKNOWN",
    "axes_agree": true | false,
    "INCOHERENT": true | false
  },
  "coherence_flag": "INCOHERENT | COHERENT | NOT_APPLICABLE",
  "INVESTIGATIVE_CANDIDATE": true | false,
  "v13_label_assigned": "INVESTIGATIVE_CANDIDATE | NONE",
  "candidate_summary": "<one sentence echoing 05_candidate.json llm_application key terms>",
  "rationale": "<2-3 sentences: synthesize step 10 vs step 13.5 disagreement (if any) into a final coherence verdict>",
  "human_review_priority": "high | medium | low | n/a",
  "honest_detection_note": "Step 14 is deterministic from 10_decision.json and 13_5_adversarial_spec.json text; no Agent spawn required. Detector verdicts are auditable by reading the two source files."
}
```

### 2.4 Post-step-14 v13 verdict synthesis

```
v13_verdict =
    PASS                          if step_05_5 PASS AND step_10 PASS AND tree_stream PASS
                                  AND q_rubric_verdict == NOVEL
                                  AND gap_real == true
                                  AND adversarial_hit == false
                                  AND step_13.pre_check.test_variant_distinguishable_from_control == true
                                  AND step_13_5.post_attack_distinguishability_verdict == true
                                  (UNCHANGED — same 10 signals as v12)

    PASS_WITH_EMPIRICAL_CAVEAT    (UNCHANGED — same v10 criteria)

    FAIL_EMPIRICAL_ATTACK         (UNCHANGED — same v11 criteria)

    REJECTED_R279_PATTERN         (UNCHANGED — same v12 criteria)

    INVESTIGATIVE_CANDIDATE       if step_14.INVESTIGATIVE_CANDIDATE == true
                                  (NEW v13 verdict label; co-exists with FAIL label on the same round)
                                  
                                  This is NOT a substantive PASS.
                                  This is a HUMAN-REVIEW FLAG.
                                  The round still has step_10 == FAIL underlying.
                                  v13_FAIL is also assigned to the round (the underlying FAIL holds).

    FAIL_ADVERSARIAL              (UNCHANGED — step 11.5 hit)
    FAIL_GAP_REAL_LOGGED          (UNCHANGED — gap_real + tree_stream low-sim)
    FAIL                          otherwise
```

**Important:** v13 INVESTIGATIVE_CANDIDATE does NOT replace FAIL. It is a parallel diagnostic label. The round's v13 verdict can be both `FAIL` AND `INVESTIGATIVE_CANDIDATE` simultaneously — the underlying step 10 FAIL stands, but the candidate is also flagged for human review.

This is intentional. It is the same logic as v12's REJECTED_R279_PATTERN being distinct from FAIL — both are diagnostic compressions, not novel PASSes.

### 2.5 Post-filter downstream behavior

After step 14 INVESTIGATIVE_CANDIDATE = true:
- The round still counts as `v13_FAIL` in the failure statistics (step 10 FAIL stands).
- The round ALSO counts as `v13_INVESTIGATIVE_CANDIDATE` in the v13-specific statistics.
- Memory db records BOTH labels for the round.
- Stats output records counts of both.
- Score formula rewards both `step_14_fired_count` and `INVESTIGATIVE_CANDIDATE_count`.

Predicted downstream metrics (testable):
- step 14 FIRED rate: small positive fraction (1-3 of 25 in E32).
- INVESTIGATIVE_CANDIDATE count: same as step 14 FIRED count.
- v13_FAIL count: similar to v12's E31 count (24).

### 2.6 Constraints on step 14

- **Deterministic and auditable.** The 2-input check is applied to two JSON files. Each output field has a 1-sentence rationale pointing to the source file content. No Agent spawn needed; main-context-direct is the default.
- **Falsifiable.** Each input has a definite TRUE/FALSE answer based on the JSON. If `13_5_adversarial_spec.json` doesn't exist (step 13.5 SKIPPED), step 14 records `SKIPPED_NOT_APPLICABLE`.
- **Post-13.5 only.** Step 14 fires AFTER step 13.5 completes. It cannot pre-empt step 13.5 or step 10.
- **No regeneration.** Unlike step 05.5 (v12), step 14 does not request a candidate regeneration. The candidate is fixed; the label is the output.
- **Does not modify any upstream file.** Step 14 reads `10_decision.json` and `13_5_adversarial_spec.json` without modifying them. Step 10's verdict for the round is unchanged. Step 13.5's post_attack verdict is unchanged.

### 2.7 For E32 R776-R800

In E32:
- Every round runs step 05.5 (v12; FROZEN), step 10 (FROZEN), step 13 (FROZEN trigger), step 13.5 (FROZEN trigger), and step 14 (NEW v13).
- Expected step 14 FIRED count: 1-3 (= rounds where step 13.5 FIRED AND post_attack = TRUE AND step 10 = FAIL).
- Per HONEST DEVIATION POLICY ≤5 synthesized Agent spawns per epoch, step 14 is main-context-direct by default (deterministic detector; no Agent spawn needed).

---

## 3. Step 14 detector examples (for the v13 implementer)

### 3.1 INVESTIGATIVE_CANDIDATE examples (FIRED at step 14)

**R756 SU(2)-equivariant retrospective (if v13 had been operational at E31):**
- step_10 verdict: FAIL (total_hits=2, channels={keyword:2, semantic:0, functional:0})
- step_13_5 post_attack: TRUE (A1 SU(2) ≈ I REBUTTED; load_bearing_succeeded=false)
- coherence_check: step_10_says=FAIL, step_13_5_says=PASS, axes_agree=false, INCOHERENT=true
- Verdict: **FIRED_INVESTIGATIVE_CANDIDATE**

**R770 tropical-attention retrospective (if v13 had been operational at E31):**
- step_10 verdict: FAIL (total_hits=2, channels={keyword:2, semantic:0, functional:0})
- step_13_5 post_attack: TRUE (A1 min-plus ≈ softmax REBUTTED; load_bearing_succeeded=false)
- coherence_check: INCOHERENT=true
- Verdict: **FIRED_INVESTIGATIVE_CANDIDATE**

### 3.2 SKIPPED_COHERENT examples

**R766 Hopf-bifurcation gating (E31 retrospective):**
- step_10 verdict: FAIL
- step_13_5 post_attack: FALSE (downgraded_from_uncertain_to_false; load_bearing succeeded)
- coherence_check: step_10_says=FAIL, step_13_5_says=FAIL, axes_agree=TRUE
- Verdict: **SKIPPED_COHERENT** (both axes agree on FAIL)

### 3.3 SKIPPED_NOT_APPLICABLE examples

**R751 sheaf-cohomology mixer:**
- step_10 verdict: FAIL
- step_13_5 trigger_status: SKIPPED (R751 not in top-3 mechanical-PASS proximity)
- coherence_check: cannot evaluate
- Verdict: **SKIPPED_NOT_APPLICABLE** (step 13.5 didn't fire)

### 3.4 Hypothetical PASS-aligned example (would never have INVESTIGATIVE label)

**Hypothetical perfect PASS candidate:**
- step_10 verdict: PASS (total_hits=0)
- step_13_5 post_attack: TRUE
- coherence_check: step_10_says=PASS, step_13_5_says=PASS, axes_agree=TRUE
- Verdict: **SKIPPED_COHERENT** (both axes agree on PASS; this IS the substantive PASS, handled by v12 chain)

### 3.5 Calibration with E31 corpus

Applying step 14's check to E31 retrospectively:
- R756: INCOHERENT → INVESTIGATIVE_CANDIDATE (step 10 FAIL + step 13.5 TRUE)
- R766: COHERENT (both FAIL)
- R770: INCOHERENT → INVESTIGATIVE_CANDIDATE (step 10 FAIL + step 13.5 TRUE)
- R751-R755, R757-R765, R767-R769, R771-R775: SKIPPED_NOT_APPLICABLE (step 13.5 didn't fire)

E31 retrospective: 2/25 INVESTIGATIVE_CANDIDATE (R756 + R770).

Predicted E32 rate: 1-3/25 (extrapolating from E31's 2/3 step-13.5-fired rebuttals).

---

## 4. v13 final verdict synthesis

After all steps 05.5-13.5-14:

```
v13_verdict =
    PASS                          (UNCHANGED — same 10 signals as v12; never observed at N=896)

    PASS_WITH_EMPIRICAL_CAVEAT    (UNCHANGED — v10)

    FAIL_EMPIRICAL_ATTACK         (UNCHANGED — v11)

    REJECTED_R279_PATTERN         (UNCHANGED — v12)

    INVESTIGATIVE_CANDIDATE       ← NEW v13: step 14 FIRED
                                  Co-exists with FAIL on the same round.
                                  NOT a substantive PASS.

    FAIL_ADVERSARIAL              (UNCHANGED)
    FAIL_GAP_REAL_LOGGED          (UNCHANGED)
    FAIL                          otherwise
```

The PASS criterion remains TEN independent signals (same as v12; v13 adds NO new PASS gate). v13 ADDS the INVESTIGATIVE_CANDIDATE label as a parallel diagnostic, not a PASS path.

---

## 5. Loop control (v13)

```
# Epoch start (UNCHANGED from v12)
read logs/policy_state.json (or initialize)
update policy aggregates from prior epoch
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute (UNCHANGED)
    execute step 04.5 (v10 policy-augmented)
    execute step 05 (UNCHANGED — v8 token streams)

    # Step 05.5 (v12; ★ FORBIDDEN per v13)
    execute step 05.5 → produces 05_5_pattern_filter.json
    (regenerate per v12 protocol if rejected)

    execute step 06 (★ FROZEN) on post-filter candidate
    execute step 06.5 / 06.7 (★ FROZEN)
    execute step 07 (★ FROZEN)
    execute step 08 (v9 inverse-search) (UNCHANGED)
    execute step 09 (v9 gap-position) (UNCHANGED)
    execute step 10 (★ FROZEN)
    execute step 11 (v8 Q-rubric) (UNCHANGED)
    execute step 12 (v8 tree-stream) (★ FROZEN)
    execute step 11.5 (v7 adversarial) (★ FROZEN)
    execute step 13 (v10 spec) (★ FROZEN)
    execute step 13.5 (v11 attack) (★ FROZEN)

    # Step 14 (NEW v13): cross-step coherence detector
    if step_13_5.trigger_status == "FIRED":
        compute INCOHERENT = (step_10.verdict == FAIL AND step_13_5.post_attack_distinguishability_verdict == "true")
        if INCOHERENT:
            write 14_cross_step_coherence.json with FIRED + INVESTIGATIVE_CANDIDATE=true
        else:
            write 14_cross_step_coherence.json with SKIPPED_COHERENT
    else:
        write 14_cross_step_coherence.json with SKIPPED_NOT_APPLICABLE

    # v13 verdict synthesis
    compute v13_verdict per §4
    update memory_db.json round entry with v13 fields including step_14

    if round_num % 25 == 0:
        write output/stats_round_NNN.json

# Epoch end (UNCHANGED from v12)
compute candidate_distribution_drift_score
update logs/policy_state.json with new aggregates + step_14_aggregates
```

---

## 6. v13 score formula

```
score_v13 = (confirmed_substantive_pass × 10)
          + (25 − mean_forced_hit)
          + (tree_stream_step_10_alignment_rate × 5)
          − (false_positive_count × 5)
          − (adversarial_hit_count × 10)
          + (qrubric_step_10_alignment_rate × 3)
          + (mean_hints_per_round / 7 × 2)
          + (gap_real_rate × 4)
          + (FAIL_GAP_REAL_LOGGED_count / N × 2)
          + (step_13_fired_count / N × 3)                       (v10 term, unchanged)
          + (step_13_distinguishable_count / N × 4)             (v10 term, unchanged)
          − (PASS_WITH_EMPIRICAL_CAVEAT × 2)                    (v10 term, unchanged)
          + (policy_drift_score × 2)                            (v10 term, unchanged)
          + (step_13_5_fired_count / N × 3)                     (v11 term, unchanged)
          + (step_13_5_attack_success_rate × 3)                 (v11 term, unchanged)
          − (FAIL_EMPIRICAL_ATTACK × 1)                         (v11 term, unchanged)
          + (verdict_shift_v10_to_v11_count × 1)                (v11 term, unchanged)
          + (step_05_5_rejection_rate × 3)                      (v12 term, unchanged)
          + (architectural_topology_change_rate × 4)            (v12 term, unchanged)
          + (regeneration_success_rate × 2)                     (v12 term, unchanged)
          − (REJECTED_R279_PATTERN_count × 1)                   (v12 term, unchanged)
          + (step_14_fired_count / N × 3)                       ← NEW v13 term
          + (INVESTIGATIVE_CANDIDATE_count / N × 4)             ← NEW v13 term
          + (cross_step_axis_divergence_rate × 2)               ← NEW v13 term
```

Where:
- `step_14_fired_count` = number of rounds where step 14 FIRED (= INVESTIGATIVE_CANDIDATE rounds). Rewards the channel for surfacing the cross-step incoherence signal. Range [0, N].
- `INVESTIGATIVE_CANDIDATE_count` = same numerator as step_14_fired_count (identical by definition). Rewards human-review-worthy candidates. Higher means more candidates worth closer inspection.
- `cross_step_axis_divergence_rate` = INVESTIGATIVE_CANDIDATE_count / N. Rewards the rate at which the architectural-distinct quadrant is being populated. Independent of N.

**Why these terms:**
- `step_14_fired_count × 3`: rewards firing the detector. Calibrated similar to step_13_5_fired × 3.
- `INVESTIGATIVE_CANDIDATE_count × 4`: rewards the LABEL. Highest of the three v13 terms because this is the v13 contribution.
- `cross_step_axis_divergence_rate × 2`: rewards population-level divergence rate. Independent of N.

There is NO negative term on INVESTIGATIVE_CANDIDATE_count. INVESTIGATIVE_CANDIDATE is not a false positive — it is a real signal that v11/v12 missed.

The `confirmed_substantive_pass` definition under v13 requires (UNCHANGED from v12):
- step 05.5 PASS, step 10 PASS, tree_stream PASS, q_rubric=NOVEL, gap_real=true, no adversarial hit, step 13 pre_check=true, step 13.5 post_attack=true.
- Step 14 is NOT a substantive PASS criterion. INVESTIGATIVE_CANDIDATE does NOT inflate confirmed_substantive_pass.

**Ten signals must still align for substantive PASS.** v13's INVESTIGATIVE_CANDIDATE is a parallel diagnostic label, not a PASS criterion.

---

## 7. No R279 retrofit needed for v13

v13's step 14 reads step 10 + step 13.5 outputs. The R279 round (rounds/round_279/) has step 10 = FAIL (mechanical) and step 13.5 = succeeded attacks (4/4) → post_attack = FALSE. So R279 retrospectively: step 14 would be SKIPPED_COHERENT (both step 10 FAIL and step 13.5 FALSE; axes agree).

No retrofit file needed. R279 does NOT trigger INVESTIGATIVE_CANDIDATE (it is correctly classified as R279-pattern across all 4+ channels).

This is the correct behavior: v13's INVESTIGATIVE_CANDIDATE label is for the architectural-attack-rebutted quadrant, which R279 (parametrization-only) does not occupy.

---

## 8. Anti-cheating commitments (v13 additions on top of v12)

If you catch yourself wanting to:

- **Mark INVESTIGATIVE_CANDIDATE as a substantive PASS** — don't. INVESTIGATIVE_CANDIDATE is a parallel diagnostic label, not a PASS path. The substantive_pass_count remains gated on the v12 10-signal criterion.
- **Override step 10's FAIL verdict because step 13.5 said PASS** — don't. Step 10 is FROZEN. Step 14 ADDs a label; it does NOT modify step 10's `verdict` field. The round still records step 10 verdict = FAIL.
- **Spawn step 14 as an Agent call to launder the verdict** — don't. Step 14 is mechanical from two JSON files. Main-context-direct labeling is the default. An Agent spawn for step 14 is allowed but adds no signal — the detector rule is deterministic.
- **Conflate INVESTIGATIVE_CANDIDATE with "this candidate is novel"** — don't. INVESTIGATIVE_CANDIDATE means "step 10 and step 13.5 disagreed on the axis of evaluation for this candidate." It is a SIGNAL that the candidate is worth a closer look, NOT a CONFIRMATION of novelty.
- **Inflate step 14 FIRED count by triggering when step 13.5 was SKIPPED** — don't. Step 14 trigger requires step 13.5 FIRED. SKIPPED step 13.5 → SKIPPED_NOT_APPLICABLE at step 14, NOT FIRED.
- **Promote a SKIPPED_COHERENT round to INVESTIGATIVE_CANDIDATE because the candidate looks novel** — don't. The INVESTIGATIVE label requires the deterministic INCOHERENT condition. If step 10 said PASS AND step 13.5 said PASS, both axes agreed — not INCOHERENT.
- **Hand-wave step 13.5's post_attack verdict as TRUE without rebuttal** — don't. Step 14 reads step 13.5's verdict as-is. If step 13.5 already labeled post_attack = FALSE, step 14 cannot promote it to TRUE.
- **Trigger step 14 on candidates that didn't make top-3 step-13** — don't. Step 14 trigger requires step 13.5 FIRED, which requires step 13 FIRED, which requires top-3 mechanical-PASS proximity. There is no path around this.

---

## 9. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7+v8+v9+v10+v11+v12)

### 9.1 Step 06 web_search — UNCHANGED
### 9.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
### 9.3 Step 10 mechanical verdict — UNCHANGED
### 9.4 Step 11.5 adversarial external — UNCHANGED
### 9.5 Step 12 tree-stream — UNCHANGED (★ FROZEN)
### 9.6 v8 components — UNCHANGED
### 9.7 v9 components — UNCHANGED
### 9.8 v10 step 13 spec format — UNCHANGED (★ FROZEN)
### 9.9 v11 step 13.5 attack format — UNCHANGED (★ FROZEN)
### 9.10 v12 step 05.5 anti-R279 filter — UNCHANGED (★ FORBIDDEN per v13 task)
### 9.11 v10/v11 policy state schema — UNCHANGED

v13 is purely ADDITIVE: step 14 + new `INVESTIGATIVE_CANDIDATE` verdict label.

---

## 10. Stats schema additions in v13

`output/stats_round_NNN.json` adds these v13-specific fields on top of v12:

```json
{
  ... (all v1-v12 fields) ...,
  "v13_cross_step_coherence_metrics": {
    "step_14_total_evaluations": 0,
    "step_14_FIRED_count": 0,
    "step_14_SKIPPED_COHERENT_count": 0,
    "step_14_SKIPPED_NOT_APPLICABLE_count": 0,
    "step_14_fired_rate": 0.0,
    "cross_step_axis_divergence_rate": 0.0,
    "INVESTIGATIVE_CANDIDATE_count": 0,
    "INVESTIGATIVE_CANDIDATE_rounds": [],
    "real_step_14_Agent_spawns": 0,
    "main_context_direct_step_14_count": 0
  },
  "v13_verdict_distribution": {
    "v13_PASS_count": 0,
    "v13_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v13_FAIL_count": 0,
    "v13_FAIL_ADVERSARIAL_count": 0,
    "v13_FAIL_GAP_REAL_LOGGED_count": 0,
    "v13_FAIL_EMPIRICAL_ATTACK_count": 0,
    "v13_REJECTED_R279_PATTERN_count": 0,
    "v13_INVESTIGATIVE_CANDIDATE_count": 0
  },
  "v13_verdict_shift_metrics": {
    "verdict_shift_v12_to_v13_count": 0,
    "rounds_where_v13_adds_INVESTIGATIVE_to_v12_FAIL": [],
    "shift_categories": {
      "v12_FAIL_to_v13_FAIL_plus_INVESTIGATIVE": 0,
      "no_shift": 0
    }
  }
}
```

The `v12_FAIL_to_v13_FAIL_plus_INVESTIGATIVE` shift category captures rounds where v12 would have only labeled FAIL but v13 ALSO assigns INVESTIGATIVE_CANDIDATE. This is the v13 value-added information.

---

## 11. Anti-cheating commitments (v13 additions on top of v12)

The v3/v4/v5/v6/v7/v8/v9/v10/v11/v12 instructions stand. v13 adds:

- **Step 14 detector honesty.** The 2-input check is mechanical from JSON. "I felt like it was incoherent" is not evidence. The exact field values (`step_10.verdict`, `step_13_5.post_attack_distinguishability_verdict`, `step_13_5.load_bearing_attack_succeeded`) must be cited.
- **No regeneration at step 14.** Unlike step 05.5, step 14 does not request regeneration. The candidate's verdicts are fixed by the FROZEN chain.
- **Step 14 verdict is the detector's verdict, not the labeler's.** Each round gets exactly one step 14 status (FIRED / SKIPPED_COHERENT / SKIPPED_NOT_APPLICABLE) based on JSON content.
- **One-way ratchet on label.** INVESTIGATIVE_CANDIDATE, once assigned, cannot be retroactively removed by a downstream review. (It can be reviewed by a human and the conclusion of the review can be that the architectural distinguishability claim was weak — but the label was correctly assigned by step 14's deterministic rule.)
- **Step 14 is NOT to be skipped on rounds where step 13.5 fired.** Every round with step 13.5 FIRED must produce a step 14 evaluation (FIRED or SKIPPED_COHERENT). Only rounds without step 13.5 FIRED can produce SKIPPED_NOT_APPLICABLE.

---

## 12. Inherited history (v1 → ... → v13)

- **v1**: file-chain + mechanical keyword rule + cross-agent verification. R001-R025.
- **v2**: Form A/B/C/D rotation. R026-R050.
- **v3**: step 04.5 memory check. R051-R075.
- **v4**: step 06.5 semantic-similarity. R076-R100.
- **v5**: step 06.7 functional-equivalence judge. R101-R575.
- **v6**: step 06.8 per-paper-completeness. R576-R600 (DEPRECATED).
- **v7**: v5 base + step 11.5 adversarial-literature. R601-R650.
- **v8**: v7 base + token streams (step 05) + Q-rubric (step 11) + tree-stream (step 12). R651-R675.
- **v9**: v8 base + inverse-search (step 08) + gap-position (step 09). R676-R700.
- **v10**: v9 base + step 13 experiment-spec generator + `logs/policy_state.json` policy update. R701-R725 + R279 retrofit.
- **v11**: v10 base + step 13.5 adversarial spec attack. R726-R750 + R279 step-13.5 retrofit-attack.
- **v12**: v11 base + step 05.5 anti-R279 mechanical structural filter. R751-R775 + R279 step-05.5 retrofit-classifier.
- **v13** (this file): v12 base + step 14 cross-step coherence detector (post-13.5 axis-divergence synthesis). **R776-R800 under v13 in E32.**

---

## 13. What v13 does NOT promise

v13 does NOT promise more substantive PASS verdicts. The 871-round saturation result (0 confirmed substantive PASS, p ≈ 0.000161 on 1%-novelty H₀ at N=871) stands. v13's step 14 is a NEW orthogonal extension at the CROSS-STEP SYNTHESIS layer; it does not guarantee PASS rate change. PASS rate depends on the actual novelty distribution of architectural-topology candidates passing step 10's kw threshold — and step 10 is FROZEN.

What v13 promises:
- The first **cross-step coherence detector** in the corpus (step 14).
- A new verdict label `INVESTIGATIVE_CANDIDATE` for the architectural-attack-rebutted-but-kw-hit quadrant.
- PASS criterion UNCHANGED at 10 signals (v13 adds NO new PASS gate).
- Symmetric design with step 05.5 (v12), step 09 (v9), step 07 (v5) — all mechanical filters with deterministic verdicts.
- The first **post-13.5 synthesis** in the corpus — reads step 10 AND step 13.5 outputs.
- A signal compression on the v12-enabled architectural-distinct candidate population.

v13 cannot make step 10 say PASS on a kw-hit candidate. v13 can FLAG the candidate as INVESTIGATIVE so a human knows to look closer.

---

## 14. Honest deviation policy (for E32 execution)

Per the v13 task description:
- Real WebSearch in step 06 (mandatory; same as v5-v12).
- Real Agent spawn for step 08 (inverse-search) and step 12 (helper) WHERE FEASIBLE.
- Step 13 spec generation runs in MAIN CONTEXT (v10 default).
- Step 13.5 adversarial-spec attack runs in MAIN CONTEXT or Agent spawn (v11 default; ≤3 spawns).
- Step 05.5 mechanical filter runs in MAIN CONTEXT (v12 default).
- **Step 14 cross-step coherence detector** runs in MAIN CONTEXT (v13 default; no Agent spawn needed because the detector is deterministic from JSON).
- Per epoch, ≤5 synthesized Agent spawns across all steps. Excess uses main-context-direct labeling (NOT a fake Agent ID claim).
- Wall-clock timestamps ≥ 3-min logical gap per round (continued from E29-E31).

No R279 retrofit needed for v13 (per §7).

---

## 15. Phase 4 reporting requirements (for output/epoch32_comparison.md)

After E32 completes, the comparison document must record:
1. step 14 trigger evaluation per round (FIRED / SKIPPED_COHERENT / SKIPPED_NOT_APPLICABLE).
2. step 14 FIRED count + cross_step_axis_divergence_rate.
3. INVESTIGATIVE_CANDIDATE list of rounds + per-round candidate summary.
4. v12 → v13 verdict shift: rounds where v12 would have labeled FAIL but v13 ALSO assigns INVESTIGATIVE_CANDIDATE.
5. Downstream metric continuity from E31 (step 05.5 rates, step 13/13.5 rates).
6. score_v13 with the 3 new terms.
7. cumulative N_verified after E32 = 896.
8. p(no PASS | 1% H₀) at N=896 ≈ 0.000127 (per v13 task target).

The v13 channel's contribution is best seen at the step 14 level + INVESTIGATIVE_CANDIDATE count, not the final-PASS-verdict level.
