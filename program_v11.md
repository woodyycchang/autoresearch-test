# program_v11.md
## Niche-Mining Pipeline — v11: Adversarial Reward-Channel Extension (step 13.5)

This file extends the **v10 base pipeline** (= v9 base + step 13 toy-experiment-spec generator + `logs/policy_state.json` candidate-policy update) with ONE NEW structural upgrade that addresses v10's diagnosed limitation (see `output/v10_limitation_analysis.md`):

> v10 step 13 produces a `distinguishability_pre_check` verdict via LLM structural reasoning on a hypothetical experiment. Because the spec author and the pre-check author share the same LLM context, the verdict is author-biased — modally "uncertain", preserving optionality. v11 introduces step 13.5: an INDEPENDENT adversarial agent that reads the step 13 spec and actively searches for ways the experiment would fail to reveal real differences (e.g., A_candidate ≡ B_control under realistic data distributions; metric collapses across variants; statistical test is under-powered at chosen N). Step 13.5 emits a post-attack distinguishability verdict that overrides step 13's pre-check when the attack succeeds.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

The following zones are **FROZEN** verbatim from v5 / v7 / v8 / v9 / v10:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL — keyword ∪ semantic ∪ functional)
- **Step 12 tree-stream** (v8 helper + per-hint solver + conservative synthesis)
- **Step 11.5 adversarial external** (v7 contribution; gated)
- **Step 13 spec format** (v10 contribution; FROZEN at the JSON schema level — v11 reads it but does not modify it)
- **All v8 components** (step 05 token streams, step 11 Q-rubric)
- **All v9 components** (step 08 inverse-search, step 09 gap-position)
- **All v10 components** (step 13 spec generation, `logs/policy_state.json` policy update, PASS_WITH_EMPIRICAL_CAVEAT verdict label)

v11 is **strictly additive**. It ADDS step 13.5 between step 13 and the v11 final verdict synthesis. It does NOT modify any prior file or any prior step.

---

## 0. Why adversarial extension and not something else

### 0.1 The v10 limitation diagnosed in `output/v10_limitation_analysis.md`

`output/v10_limitation_analysis.md` shows that v10's step 13 is best classified as a **structural-reasoning evidence channel**, not a reward channel — every signal it produces is LLM inference on a hypothetical experiment, not an empirical observation. The specific failure modes are:

1. **Author bias.** Spec author and pre-check author share LLM context; "uncertain" is the modal verdict because it preserves optionality.
2. **Hypothetical-only.** No data is observed.
3. **Non-actionable middle class.** "uncertain" is the modal verdict in E29 (2/3 fired); the label provides no rank ordering.

### 0.2 The four candidate v11 upgrades

| Option | Cost | Extends reward channel? | Addresses author bias? |
|---|---|---|---|
| (a) Spec → executable Python file | medium | weakly (artifact concreteness) | no |
| **(b) Adversarial step 13.5** | low (≤3 spawns) | **directly** | **yes — adversary has no incentive to preserve uncertain** |
| (c) Cross-candidate distinguishability matrix | low | NO — adds NEW channel (corpus saturation) instead | no |
| (d) Policy state hardening | very low | NO — operates on policy not reward | no |

**v11 adopts direction (b).**

### 0.3 Symmetry with v7's step 11.5

v7 added step 11.5: an adversarial agent that reads the candidate (vocabulary-stripped) and searches for prior art. This converted step 06's evidence-channel signal into a more reliable verdict by introducing an independent skeptic. The pattern is proven; v11 replicates it for step 13's empirical claim:

- **Step 11.5:** adversarial against the *literature-novelty* claim. Spawned ≤25 times in E25, 0 in E26-E29.
- **Step 13.5 (NEW v11):** adversarial against the *empirical-distinguishability* claim. Spawned at most 3 per epoch (= top-3 step-13 FIRED rounds).

### 0.4 What v11 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§9 below) — UNCHANGED.
- v10 step 13's JSON schema — UNCHANGED. (Step 13.5 reads it but does not modify it.)
- `logs/policy_state.json` schema and update protocol — UNCHANGED.
- PASS criterion definition (still "no prior art + has mechanism value" → 8 signals from v10) — UNCHANGED, but now there is one more independent check (step 13.5 attack) that can flip the empirical-distinguishability signal.
- Cumulative N_verified counting protocol — UNCHANGED.

---

## 1. File chain (v10 + one addition)

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

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN
    06_7_functional_hits.json        ★ FROZEN
    07_hit_miss.json                 ★ FROZEN

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json                 ★ FROZEN

    11_qrubric.json
    11_audit.json
    12_tree_stream.json              ★ FROZEN for v11
    12_verification.json
    11_5_adversarial.json            ★ FROZEN

    13_experiment_spec.json          ★ FROZEN for v11 (v10 contribution; v11 reads it but does not modify)
    13_5_adversarial_spec.json       ← NEW v11 (conditional: only when step 13 FIRED)
```

Side-channel (UNCHANGED from v10):
```
logs/policy_state.json
```

A v11 round MUST contain all v10 files. It MUST contain `13_5_adversarial_spec.json` ONLY IF `13_experiment_spec.trigger_status` starts with `FIRED`. Otherwise step 13.5 is SKIPPED with explicit skip status logged.

---

## 2. Step 13.5 — Adversarial spec attack (NEW v11)

### 2.1 What step 13.5 does

Step 13.5 is the first **adversarial-empirical** channel in the corpus. It runs after step 13 generates `13_experiment_spec.json` and before the v11 verdict synthesis. The adversarial agent (or main-context-direct equivalent) reads the spec and attempts to find ways the experiment would FAIL TO REVEAL real differences between A_candidate and B_control / C_baseline.

Attack categories the adversary considers:

1. **Variant equivalence under realistic data.** A_candidate and B_control may differ in `distinctive_parameter` on paper but produce identical or indistinguishable metric distributions at the chosen dataset scale (e.g., R279: integer-ratio target spectrum ≡ random target under SVD geometry pressure at MRPC scale).
2. **Metric collapse.** The chosen metric may not respond to the distinctive_parameter (e.g., R725: any topological invariant of a 1K-sample 3D embedding is dominated by sampling noise; the Heegaard-genus framing adds nothing the Betti-1 doesn't already report).
3. **Statistical test under-power.** The proposed N_seeds and sample size may yield p-values too noisy to distinguish the variants even when a real difference exists (e.g., 3 seeds × 408 dev examples for MRPC F1 has ~5% paired-t-test power for effect sizes < 0.5 std).
4. **Confounded baseline.** C_baseline may not be the strongest published baseline; A may beat C trivially while still collapsing into B (e.g., R708 vs Voita 2019 entropy: Voita 2019 is not state-of-the-art; outperforming it is uninformative).
5. **Implementation ambiguity.** The spec may underspecify a load-bearing detail (e.g., "Dirichlet continuation" without specifying truncation order or summation method can be implemented multiple ways with different empirical signatures).

Step 13.5 enumerates 1-5 specific attacks per spec, scores each as `succeeded | failed | indeterminate`, and emits a post-attack distinguishability verdict.

### 2.2 Step 13.5 trigger logic

```
trigger_step_13_5 = (13_experiment_spec.trigger_status.startswith("FIRED"))
```

If trigger fires: step 13.5 generates the adversarial attack file. Otherwise: step 13.5 emits a SKIP stub:

```json
{
  "round": "NNN",
  "epoch": 11,
  "trigger_status": "SKIPPED_step_13_NOT_FIRED",
  "reason": "step 13 did not FIRE (no FIRED_TOP_3_PROXIMITY or FIRED_RETROSPECTIVE status); no spec to attack."
}
```

### 2.3 Step 13.5 schema

```json
{
  "round": "NNN",
  "epoch": 11,
  "trigger_status": "FIRED",
  "trigger_reason": "<step 13 FIRED for this round>",
  "adversarial_agent_id": "<spawn agentId or main-context-direct-step-13-5-R<num>-attacker>",
  "real_adversarial_Agent_spawn": true | false,
  "step_13_spec_pre_check_input": {
    "test_variant_distinguishable_from_control": "<true | false | uncertain>",
    "rationale": "<echo of step 13's rationale>"
  },
  "attacks": [
    {
      "id": "A1",
      "category": "variant_equivalence | metric_collapse | test_under_power | confounded_baseline | implementation_ambiguity",
      "claim": "<one sentence: what the attacker asserts>",
      "evidence": "<one sentence: why the attacker believes this>",
      "verdict": "succeeded | failed | indeterminate",
      "load_bearing": true | false
    },
    ...
  ],
  "attacks_succeeded_count": <integer>,
  "attacks_failed_count": <integer>,
  "load_bearing_attack_succeeded": true | false,
  "post_attack_distinguishability_verdict": "true | false | uncertain | downgraded_from_true_to_uncertain | downgraded_from_uncertain_to_false",
  "rationale": "<2-3 sentences: synthesizing the attacks into a final verdict>",
  "spec_survives_attack": true | false,
  "would_flip_v10_verdict": true | false,
  "notes_for_executor": "<one sentence: what the executor should know if running this spec anyway>"
}
```

### 2.4 Post-attack verdict rules

```
post_attack_verdict =
    "true"                                            if step 13 pre_check was true AND no load_bearing attack succeeded
    "downgraded_from_true_to_uncertain"               if step 13 pre_check was true AND ≥1 load_bearing attack succeeded
    "uncertain"                                       if step 13 pre_check was uncertain AND no load_bearing attack succeeded
    "downgraded_from_uncertain_to_false"              if step 13 pre_check was uncertain AND ≥1 load_bearing attack succeeded
    "false"                                           if step 13 pre_check was false (already pessimistic; attacks confirm)
```

A **load-bearing attack** is one whose claim, if true, would make the experiment fail to distinguish A from B even when A_candidate has real mechanism value. Attacks that merely add caveats are not load-bearing.

### 2.5 Constraints on step 13.5

- **Attack count: 1-5 per spec.** Fewer than 1 is invalid; more than 5 is wasteful. v11 epochs target 3-4 attacks per spec.
- **Each attack must be specific.** Generic objections ("the dataset might be too small") are not load-bearing unless the attacker shows the specific size at which power fails.
- **Adversarial Agent spawn budget: ≤3 per epoch.** With ≤3 step-13-FIRED rounds per epoch, this is one Agent spawn per FIRED round (max). Excess uses main-context-direct labeling.
- **Spec format is NOT modified.** Step 13.5 produces a SEPARATE file (`13_5_adversarial_spec.json`); the original `13_experiment_spec.json` is left intact.
- **The pre-check verdict in step 13 is the starting point.** Step 13.5 can only downgrade (true → uncertain, uncertain → false). It cannot promote false → uncertain or uncertain → true. This is asymmetric on purpose — the adversary is a one-way ratchet toward pessimism, consistent with v7 step 11.5's pattern.

### 2.6 For E30 R726-R750 plus R279 retrofit-attack

In E30:
- The top-3 step-13 FIRED rounds receive step 13.5 attack.
- Per HONEST DEVIATION POLICY ≤5 synthesized Agent spawns per epoch, the adversarial spawn budget is ≤3 (one per top-3 round). Main-context-direct labeling is allowed for the remainder.
- **R279 step 13.5 retrofit attack:** apply step 13.5 retroactively to `rounds/round_279/13_experiment_spec.json`. Expected outcome: the existing distinguishability=false stands; attacks consolidate the verdict (no flip). Validates that step 13.5 does not produce spurious flips on already-pessimistic specs.

---

## 3. Step 13.5 attack design patterns (for the spec generator)

When generating step 13.5 attacks, the adversarial agent should target the spec's load-bearing claims. Patterns from prior corpus analysis:

### 3.1 Pattern A: Variant Equivalence
The `distinctive_parameter` is presented as discriminative but, under realistic data, A and B occupy equivalent regions of metric space.

Example for R708 (Dirichlet head pruning):
- Spec claim: D(s=0) is structurally different from L2-magnitude.
- Attack: For typical attention-head importance distributions (heavy-tailed, near-monotone decay), D(s=0) ≈ Σ a_n is the arithmetic mean of importance scores; the rank ordering induced is the same as magnitude rank ordering up to ties. The "structurally different" claim is technically true (D vs sum) but empirically equivalent on this dataset.
- Verdict: **succeeded**, load_bearing=true.

### 3.2 Pattern B: Metric Collapse
The chosen metric is sensitive to noise larger than the variant effect.

Example for R725 (Heegaard genus diagnostic):
- Spec claim: Spearman correlation between genus and accuracy per subject.
- Attack: With only 4 subjects × 3 seeds = 12 (genus, accuracy) pairs, Spearman ρ has standard error ~0.5. The "if genus negatively correlates with accuracy r < -0.5" criterion is sensitive to seed variation in t-SNE init alone. The metric does not concentrate.
- Verdict: **succeeded**, load_bearing=true.

### 3.3 Pattern C: Statistical Test Under-Power
N_seeds × dataset_size insufficient for the effect size the candidate is expected to produce.

Example for R715 (Ramsey head allocation):
- Spec claim: paired t-test A vs B at p < 0.05 with 3 seeds.
- Attack: Paired t-test with df=2 has ~5% power for Cohen's d < 1.0. Ramsey-init vs random-init effects on LRA-Pathfinder are typically <0.5 std after 20K training steps (random-init has high variance in early training that washes out long-term). Expected outcome: A ≈ B not because Ramsey lacks value, but because the test cannot resolve the difference.
- Verdict: **succeeded**, load_bearing=true.

### 3.4 Pattern D: Confounded Baseline
C_baseline is not the strongest published baseline; outperforming it is uninformative.

Example: spec compares to "Voita 2019" attention-entropy pruning. Attack: Voita 2019 is one specific entropy pruning method; the SOTA pruning method on this dataset is BERT-of-Theseus 2020 or Movement-Pruning 2020, neither tested.

### 3.5 Pattern E: Implementation Ambiguity
The spec is under-specified at a load-bearing detail.

Example: spec says "compute Dirichlet continuation D(s)". Attack: Dirichlet continuation via direct sum (s ≥ 1), Abel summation (s ≤ 1), Euler-Maclaurin (s near 0), or Riemann-Siegel (specialized) all give DIFFERENT numerical values. Without specifying method, the experiment is not reproducible.

---

## 4. v11 final verdict synthesis

After all steps 08-13.5:

```
v11_verdict =
    PASS                          if step_10 PASS
                                  AND tree_stream PASS
                                  AND q_rubric_verdict == NOVEL
                                  AND gap_real == true
                                  AND adversarial_hit == false
                                  AND step_13.pre_check.test_variant_distinguishable_from_control == true
                                  AND step_13_5.post_attack_distinguishability_verdict == true

    PASS_WITH_EMPIRICAL_CAVEAT    if step_10 PASS
                                  AND tree_stream PASS
                                  AND q_rubric_verdict == NOVEL
                                  AND gap_real == true
                                  AND adversarial_hit == false
                                  AND (step_13.pre_check.test_variant_distinguishable_from_control == false
                                       OR step_13_5.post_attack_distinguishability_verdict ∈
                                          {downgraded_from_true_to_uncertain, downgraded_from_uncertain_to_false, false})

    FAIL_EMPIRICAL_ATTACK         if step_10 PASS
                                  AND tree_stream PASS
                                  AND q_rubric_verdict == NOVEL
                                  AND gap_real == true
                                  AND adversarial_hit == false
                                  AND step_13_5.load_bearing_attack_succeeded == true
                                  AND step_13_5.post_attack_distinguishability_verdict == "downgraded_from_uncertain_to_false"
                                  AND step_13.pre_check was "uncertain"
                                  (a v10 PASS_WITH_EMPIRICAL_CAVEAT that v11 promotes to FAIL because the attack actually demolishes the empirical claim)

    FAIL_ADVERSARIAL              if step_10 PASS AND tree_stream PASS AND adversarial_hit == true
    FAIL_GAP_REAL_LOGGED          if step_10 FAIL
                                  AND tree_stream max per-hint sim < 0.5
                                  AND gap_real == true
    FAIL                          otherwise
```

The PASS criterion now requires **NINE** independent signals:
1. step 10 keyword (FROZEN)
2. step 10 semantic
3. step 10 functional
4. tree-stream helper + solver synthesis
5. Q-rubric
6. gap_real
7. step 11.5 adversarial-literature
8. step 13 distinguishability pre-check
9. **step 13.5 post-attack distinguishability verdict** (NEW v11)

**Strictly more demanding than v10** (which had 8 signals).

A new verdict label `FAIL_EMPIRICAL_ATTACK` captures candidates that v10 would have rated PASS_WITH_EMPIRICAL_CAVEAT but where v11's attack demolishes the empirical-distinguishability claim entirely. These are NOT PASS_WITH_EMPIRICAL_CAVEAT; they are full FAIL via the new channel.

---

## 5. Loop control (v11)

```
# Epoch start (UNCHANGED from v10)
read logs/policy_state.json (or initialize)
update policy aggregates from prior epoch
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute (UNCHANGED)
    execute step 04.5 (v10 policy-augmented)
    execute step 05 (UNCHANGED)
    execute step 06 (★ FROZEN)
    execute step 06.5 / 06.7 (★ FROZEN)
    execute step 07 (★ FROZEN)
    execute step 08 (v9 inverse-search) (UNCHANGED)
    execute step 09 (v9 gap-position) (UNCHANGED)
    execute step 10 (★ FROZEN)
    execute step 11 (v8 Q-rubric) (UNCHANGED)
    execute step 12 (v8 tree-stream) (★ FROZEN for v11)
    execute step 11.5 (v7 adversarial) (★ FROZEN)
    execute step 13 (v10 spec) (★ FROZEN for v11)

    # Step 13.5 (NEW v11): adversarial spec attack
    if 13_experiment_spec.trigger_status.startswith("FIRED"):
        spawn adversarial-spec-attacker Agent (or main-context-direct)
        write 13_5_adversarial_spec.json (1-5 attacks; post-attack verdict)
    else:
        write 13_5_adversarial_spec.json with trigger_status = "SKIPPED_step_13_NOT_FIRED"

    # v11 verdict synthesis
    compute v11_verdict per §4
    update memory_db.json round entry with v11 fields including step_13_5

    if round_num % 25 == 0:
        write output/stats_round_NNN.json

# Epoch end (UNCHANGED from v10)
compute candidate_distribution_drift_score
update logs/policy_state.json with new aggregates
```

---

## 6. v11 score formula

```
score_v11 = (confirmed_substantive_pass × 10)
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
          + (step_13_5_fired_count / N × 3)                     ← NEW v11 term
          + (step_13_5_attack_success_rate × 3)                 ← NEW v11 term
          − (FAIL_EMPIRICAL_ATTACK × 1)                         ← NEW v11 term
          + (verdict_shift_v10_to_v11_count × 1)                ← NEW v11 term
```

Where:
- `step_13_5_fired_count` = rounds where step 13.5 fired (= step 13 FIRED rounds).
- `step_13_5_attack_success_rate` = (load_bearing_attack_succeeded_count) / (step_13_5_fired_count) ∈ [0, 1]. Rewards the channel for being discriminating.
- `FAIL_EMPIRICAL_ATTACK` count from v11 final verdict synthesis (subtracts 1 each — small penalty, since these are diagnostic information losses for the candidate but not protocol failures).
- `verdict_shift_v10_to_v11_count` = rounds where the v11 verdict would have differed from v10 (e.g., v10 PASS_WITH_EMPIRICAL_CAVEAT → v11 FAIL_EMPIRICAL_ATTACK). Rewards v11 for adding actionable shifts.

**Why these terms:**
- `step_13_5_fired_count × 3`: rewards rounds where the adversarial-empirical channel was actually triggered (= step 13 fired, attack possible).
- `step_13_5_attack_success_rate × 3`: rewards epochs where attacks reveal real flaws (a successful attack indicates the channel is doing diagnostic work, not just rubber-stamping). Calibration: if all attacks fail (rate = 0), the channel adds 0 to score; if all attacks succeed (rate = 1), it adds 3.
- `FAIL_EMPIRICAL_ATTACK × -1`: small subtraction; these are real signal losses (the candidate had survived 7 prior checks; the attack demolished the 8th), but the SIGNAL ITSELF is valuable. Net effect: each FAIL_EMPIRICAL_ATTACK subtracts 1 from score but the attack_success_rate term adds offsetting credit.
- `verdict_shift_v10_to_v11_count × 1`: rewards v11 for adding actionable signal beyond v10.

The `confirmed_substantive_pass` definition under v11 requires ALL of:
- keyword overlap < 2, AND
- semantic cosine < 0.7, AND
- functional judge < 0.7, AND
- tree_stream verdict = PASS, AND
- q_rubric_verdict = NOVEL, AND
- gap_real == true, AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7, AND
- step_13.distinguishability_pre_check.test_variant_distinguishable_from_control == true, AND
- step_13_5.post_attack_distinguishability_verdict == true (no successful load_bearing attack).

**Nine signals must align.** A v11 PASS is the strictest criterion in corpus history.

---

## 7. R279 step 13.5 retrofit (Phase 3 of v11 task)

R279 PTCH is the canonical Pattern-C borderline candidate. Step 13's distinguishability=false retrofit (v10) was the canonical demonstration of orthogonal-path convergence with v7 step 11.5. v11 applies step 13.5 retroactively to `rounds/round_279/13_experiment_spec.json`:

- **Attack 1 (Pattern A — Variant Equivalence):** A_candidate (integer-ratio target) ≡ B_control (random target) at MRPC scale because the SVD alignment-loss gradient is dominated by per-head SVD geometry, not by the choice of fixed target. **Verdict: succeeded, load_bearing=true.** (Confirms step 13's existing rationale.)
- **Attack 2 (Pattern D — Confounded Baseline):** C_baseline (SORSA/SODA WACV 2025) is a strong baseline but already at functional similarity 0.80 to A; outperforming C by < 1 F1 point on MRPC is uninformative. **Verdict: succeeded, load_bearing=false** (consolidating attack, doesn't change the verdict but adds context).
- **Attack 3 (Pattern C — Statistical Test Under-Power):** 3 seeds × 408 MRPC dev examples has ~30% power for F1 effect sizes < 0.5 points; the spec's "A significantly better than B" criterion may produce false negatives. **Verdict: indeterminate** (could go either way; not load-bearing).

**Post-attack verdict for R279 retrofit:** false (already pessimistic; attacks consolidate, do not change). Validates that step 13.5 does not produce spurious flips on already-pessimistic specs.

---

## 8. Anti-cheating commitments (v11 additions on top of v10)

If you catch yourself wanting to:

- **Spawn step 13.5 attacks that always succeed** to inflate the attack_success_rate term — don't. The attack must be specific and falsifiable. Generic "the dataset might be too small" attacks are NOT load-bearing.
- **Always emit "downgraded_from_uncertain_to_false"** to make step 13.5 look like it's doing work — don't. If the spec has no load-bearing weakness, the post_attack_verdict is unchanged from the pre_check.
- **Promote false → uncertain or uncertain → true** via step 13.5 — don't. Step 13.5 is a one-way ratchet toward pessimism, symmetric with step 11.5.
- **Modify step 13 spec to make it harder to attack** — don't. Step 13's spec format is FROZEN for v11.
- **Synthesize >5 step-13.5 Agent spawns per epoch** — don't. ≤5-cap policy stands.
- **Generate a "would_flip_v10_verdict: false" override** when the attack DID demolish the empirical claim — don't. The would_flip flag is computed mechanically from the pre/post verdicts.
- **Use step 13.5 to second-guess step 13's spec content rather than its empirical claim** — don't. Step 13.5 attacks the *distinguishability claim*, not the spec's polish or framing.

---

## 9. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7+v8+v9+v10)

### 9.1 Step 06 web_search — UNCHANGED
### 9.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
### 9.3 Step 10 mechanical verdict — UNCHANGED
### 9.4 Step 11.5 adversarial external — UNCHANGED
### 9.5 Step 12 tree-stream — UNCHANGED (★ FROZEN for v11)
### 9.6 v8 components — UNCHANGED
### 9.7 v9 components — UNCHANGED
### 9.8 v10 step 13 spec format — UNCHANGED (★ FROZEN for v11)
### 9.9 v10 policy state schema — UNCHANGED

v11 is purely ADDITIVE: step 13.5 + new `FAIL_EMPIRICAL_ATTACK` verdict label.

---

## 10. Stats schema additions in v11

`output/stats_round_NNN.json` adds these v11-specific fields on top of v10:

```json
{
  ... (all v1-v10 fields) ...,
  "v11_adversarial_spec_metrics": {
    "step_13_5_fired_count": 0,
    "step_13_5_skipped_count": 0,
    "step_13_5_total_attacks": 0,
    "step_13_5_attacks_succeeded": 0,
    "step_13_5_load_bearing_attacks_succeeded": 0,
    "step_13_5_attack_success_rate": 0.0,
    "step_13_5_load_bearing_success_rate": 0.0,
    "real_step_13_5_Agent_spawns": 0,
    "main_context_direct_step_13_5": 0,
    "post_attack_verdict_distribution": {
      "true": 0,
      "false": 0,
      "uncertain": 0,
      "downgraded_from_true_to_uncertain": 0,
      "downgraded_from_uncertain_to_false": 0
    }
  },
  "v11_verdict_distribution": {
    "v11_PASS_count": 0,
    "v11_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v11_FAIL_count": 0,
    "v11_FAIL_ADVERSARIAL_count": 0,
    "v11_FAIL_GAP_REAL_LOGGED_count": 0,
    "v11_FAIL_EMPIRICAL_ATTACK_count": 0
  },
  "v11_verdict_shift_metrics": {
    "verdict_shift_v10_to_v11_count": 0,
    "rounds_where_v11_disagrees_with_v10": [],
    "shift_categories": {
      "v10_uncertain_to_v11_false": 0,
      "v10_PASS_WITH_EMPIRICAL_CAVEAT_to_v11_FAIL_EMPIRICAL_ATTACK": 0
    }
  }
}
```

---

## 11. Anti-cheating commitments (v11 additions on top of v10)

The v3/v4/v5/v6/v7/v8/v9/v10 instructions stand. v11 adds:

- **Step 13.5 attack honesty.** Each attack must reference a specific spec field, dataset detail, or statistical-power consideration. "I just have a bad feeling" is not an attack.
- **Adversarial agent must NOT see the candidate's source-domain vocabulary.** This is the same protection step 11.5 enforces. The attacker reads the stripped candidate from `05_sample_tokens.json` plus the spec; does not see `02_decomposition.json` source-domain framing.
- **Pre-attack and post-attack verdicts must be reconciled.** If post_attack ≠ pre_check, the rationale must name which load-bearing attack drove the change.
- **One-way ratchet enforced.** post_attack ∈ {same as pre_check, strictly more pessimistic}. Validation: pre_check = true ⇒ post_attack ∈ {true, downgraded_from_true_to_uncertain}; pre_check = uncertain ⇒ post_attack ∈ {uncertain, downgraded_from_uncertain_to_false}; pre_check = false ⇒ post_attack = false.

---

## 12. Inherited history (v1 → ... → v11)

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
- **v11** (this file): v10 base + step 13.5 adversarial spec attack. **R726-R750 + R279 step-13.5 retrofit-attack run under v11 in E30.**

---

## 13. What v11 does NOT promise

v11 does NOT promise more substantive PASS verdicts. The 821-round saturation result (0 confirmed substantive PASS, p ≈ 0.000260 on 1%-novelty H₀ at N=821) stands. v11's step 13.5 is a NEW orthogonal extension of the v10 reward channel, not a yield-boosting trick.

What v11 promises:
- The first **adversarial-empirical** channel in the corpus (step 13.5 attack on step 13 spec).
- A new verdict label `FAIL_EMPIRICAL_ATTACK` for candidates whose distinguishability claim collapses under attack.
- Strictly tighter PASS criterion (9 signals must align) than v10 (8 signals).
- The first **author-bias breakage** mechanism for step 13 — the attacker is in an independent context.
- Symmetric channel design with step 11.5 (adversarial-literature) — both are adversarial agents acting on a candidate-derived artifact.
- R279 retrofit-attack validates that step 13.5 does not produce spurious flips on already-pessimistic specs.

v11 cannot promote step 13 to a true reward channel (no execution). v11 can extract more signal from the same hypothetical-experiment substrate by introducing an independent adversary.

---

## 14. Honest deviation policy (for E30 execution)

Per the v11 task description:
- Real WebSearch in step 06 (mandatory; same as v5-v10).
- Real Agent spawn for step 08 (inverse-search) and step 12 (helper) WHERE FEASIBLE.
- Step 13 spec generation runs in MAIN CONTEXT (v10 default).
- **Step 13.5 adversarial-spec attack** is the v11 NEW channel; spawn budget ≤3 per epoch (one per top-3 step-13 FIRED round). Excess uses main-context-direct labeling.
- Per epoch, ≤5 synthesized Agent spawns across all steps. Excess uses main-context-direct labeling (NOT a fake Agent ID claim).
- Wall-clock timestamps ≥ 3-min logical gap per round (continued from E29 relaxation).
- R279 retrofit step-13.5 attack is epoch 30 round 0: a single retrospective application of step 13.5 to R279's existing step 13 spec, written into `rounds/round_279/13_5_adversarial_spec.json`. R279's step 13.5 is in addition to the 25 new rounds R726-R750.
