# program_v10.md
## Niche-Mining Pipeline — v10: Empirical Reward Layer + Candidate Policy Update

This file extends the **v9 base pipeline** (= v8 base + inverse-search landscape generation, step 08 + step 09) with TWO NEW structural upgrades that address v9's diagnosed plateau (see `output/v9_failure_diagnosis_v2.md`):

> v8 and v9 added evidence channels (Q-rubric, tree-stream, inverse-search) but NO reward channel — every signal reads from literature/landscape priors. The PASS criterion "no prior art + has mechanism value" is **unverifiable at desk-research stage** because "mechanism value" requires running something. v10 introduces:
> 1. A **toy-experiment-spec generator** (step 13, NEW) as the first non-literature-based signal in the corpus — a partial empirical reward channel.
> 2. A **candidate policy update** (logs/policy_state.json, NEW) that biases candidate generation away from FAIL-correlated sub-patterns using prior epoch verdicts as coarse reward — a per-episode policy-gradient mechanism inspired by Gao's test-time-of-agent framework.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

The following zones are **FROZEN** verbatim from v5 / v7 / v8 / v9:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL — keyword ∪ semantic ∪ functional)
- **Step 12 tree-stream** (v8 helper + per-hint solver + conservative synthesis)
- **Step 11.5 adversarial external** (v7 contribution; gated)
- **All v8 components** (step 05 token streams, step 11 Q-rubric)
- **All v9 components** (step 08 inverse-search, step 09 gap-position)

v10 is **strictly additive**. It ADDS step 13 between step 12 and the v10 final verdict synthesis, and ADDS the `logs/policy_state.json` side-channel.

---

## 0. Why empirical reward + policy update

### 0.1 The plateau diagnosed in v9_failure_diagnosis_v2.md

v6 → v7 → v8 → v9 added more checks on the same underlying input (retrieved papers + LLM prior knowledge). PASS rate stayed at 0/N for every increment in N. The structural diagnosis: every signal in the v5-v9 pipeline is an **evidence channel** (reading from literature/landscape); none is a **reward channel** (scoring candidates by an external-to-literature standard).

The PASS criterion conjunct 1 ("no prior art") is verifiable at desk-research; conjunct 2 ("has mechanism value") is not. v5-v9 all attack conjunct 1. v10 attacks conjunct 2 by **generating** (not yet executing) a falsifiable empirical test for each near-PASS candidate.

### 0.2 Yu Sun TTT analogy: small test-time reward

Yu Sun's Test-Time Training shows that a small self-supervised reward computed at test time can guide adaptation without full training. Analogously, a small toy-experiment spec — even unexecuted — provides a **distinguishability check**: does the candidate variant materially differ from a random control + a baseline? Specs that collapse into the control are weaker; specs that articulate a measurable difference are stronger.

### 0.3 Gao test-time-of-agent analogy: per-episode policy update

Gao's test-time-of-agent uses prior-episode outcomes to bias future episode actions. Even with a coarse reward (FAIL = -1, PASS = 0 since corpus has 0 PASS), the policy can avoid re-entering FAIL-correlated regions. v10's `logs/policy_state.json` tracks sub-pattern FAIL counts and biases candidate generation accordingly.

### 0.4 What v10 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§8 below) — UNCHANGED.
- v9 step 08 and step 09 — preserved verbatim.
- PASS criterion definition (still "no prior art + has mechanism value") — UNCHANGED but with conjunct 2 partially testable via step 13.
- Cumulative N_verified counting protocol — UNCHANGED.

---

## 1. File chain (v9 + two additions)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json

    05_prompt_tokens.json            ← v8 (unchanged)
    05_sample_tokens.json            ← v8 (unchanged)
    05_task_tokens.json              ← v8 (unchanged)
    05_candidate.json                ← v8 (thin index, unchanged)

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN (v4)
    06_7_functional_hits.json        ★ FROZEN (v5)
    07_hit_miss.json                 ★ FROZEN (keyword ∪ semantic ∪ functional)

    08_inverse_landscape.json        ← v9 (unchanged)
    09_gap_position.json             ← v9 (unchanged)

    10_decision.json                 ★ FROZEN (total_hits ≥ 1 → FAIL)

    11_qrubric.json                  ← v8 (unchanged)
    11_audit.json                    ← v8 (thin index, unchanged)
    12_tree_stream.json              ← v8 (unchanged, ★ FROZEN for v10)
    12_verification.json             ← v8 (thin index, unchanged)
    11_5_adversarial.json            ★ FROZEN (v7)

    13_experiment_spec.json          ← NEW v10 (conditional: step 10 PASS OR tree-stream PASS-with-caveat)
```

Side-channel:
```
logs/policy_state.json               ← NEW v10 (updated at epoch start; consulted in step 04.5 and step 05)
```

A v10 round MUST contain all v9 files. It MUST contain `13_experiment_spec.json` ONLY IF `10_decision.verdict == PASS` OR `12_tree_stream.tree_stream_verdict == PASS`. Otherwise step 13 is SKIPPED with explicit skip status logged in `13_experiment_spec.json` (a stub file with `trigger_status` field).

---

## 2. Step 13 — Toy experiment spec generation (NEW v10)

### 2.1 What step 13 does

Step 13 is the first **partial empirical reward channel** in the corpus. It generates a runnable toy-experiment spec for any candidate that reaches step 10 PASS or step 12 PASS-with-caveat. The spec is a JSON artifact describing:
- Dataset (1K-10K examples from a public source).
- Base model (small enough for free Colab T4 in <30 min).
- Variant A: candidate mechanism.
- Variant B: random control (a structural-twin variant with the candidate's distinctive parameter set to a random/uniform value).
- Variant C: baseline (the prior-art mechanism most similar to the candidate per step 11.5 or step 06.7).
- Metric (a single scalar with explicit measurement protocol).
- Statistical test (paired t-test or equivalent, with N seeds).

The spec is **generated, not executed** in v10. Execution is human-in-loop (Phase 3 of v10 only retrofits R279; future epochs may automate execution).

### 2.2 Step 13 trigger logic

```
trigger_step_13 = (10_decision.verdict == "PASS"
                   OR 12_tree_stream.tree_stream_verdict == "PASS")
                  AND step 13 not already generated for this round
```

If trigger fires, step 13 generates the spec. If trigger does not fire (the typical case in this corpus: step 10 FAIL and tree-stream FAIL), step 13 writes a SKIP stub:

```json
{
  "round": "NNN",
  "epoch": 10,
  "trigger_status": "SKIPPED_step_10_FAIL_AND_tree_stream_FAIL",
  "reason": "step 10 verdict=FAIL AND tree-stream verdict=FAIL; step 13 not triggered."
}
```

### 2.3 Step 13 spec schema

```json
{
  "round": "NNN",
  "epoch": 10,
  "trigger_status": "FIRED",
  "trigger_reason": "<step_10_PASS or tree_stream_PASS_with_caveat>",
  "spec_generator_agent_id": "<spawn agentId or main-context-direct-step-13-R<num>>",
  "candidate_stripped": "<echo of 05_sample_tokens.stripped_llm_application>",
  "experiment": {
    "dataset": {
      "name": "<e.g., 'WikiText-103 1K subset'>",
      "size": "<1K-10K examples>",
      "preprocessing": "<one sentence>",
      "source_url_or_id": "<public source identifier>"
    },
    "base_model": {
      "name": "<e.g., 'GPT-2 small (124M)' or '1-layer transformer + LoRA'>",
      "parameter_count": "<approximate>",
      "framework": "PyTorch + HuggingFace transformers (or equivalent)",
      "training_budget_minutes_on_T4": "<e.g., 25>"
    },
    "variants": {
      "A_candidate": {
        "name": "<short label>",
        "description": "<2 sentences: what the candidate variant does in the experiment>",
        "distinctive_parameter": "<the single parameter that makes A_candidate different from B_control>",
        "expected_behavior": "<one sentence: what would happen if mechanism has value>"
      },
      "B_control": {
        "name": "<short label>",
        "description": "<2 sentences: structural twin with distinctive_parameter set to random/uniform>",
        "distinctive_parameter_value": "<random/uniform/disabled>",
        "expected_behavior": "<one sentence: null-hypothesis baseline behavior>"
      },
      "C_baseline": {
        "name": "<short label>",
        "description": "<2 sentences: the prior-art mechanism most similar to the candidate per step 11.5 / step 06.7>",
        "reference_paper": "<arXiv ID or venue>",
        "expected_behavior": "<one sentence: published-baseline behavior>"
      }
    },
    "metric": {
      "name": "<e.g., 'validation loss after 1000 steps' or 'task accuracy on N=500 held-out'>",
      "measurement_protocol": "<one sentence: how the metric is computed>",
      "seeds": "<integer; e.g., 3 or 5>"
    },
    "statistical_test": {
      "name": "<e.g., 'paired t-test A vs B' + 'paired t-test A vs C'>",
      "significance_threshold": "<e.g., p < 0.05>",
      "expected_outcome_if_candidate_has_value": "<one sentence: A significantly better than B AND not significantly worse than C>",
      "expected_outcome_if_candidate_collapses_to_control": "<one sentence: A indistinguishable from B (paired t-test p > 0.5)>"
    }
  },
  "distinguishability_pre_check": {
    "test_variant_distinguishable_from_control": "<true | false | uncertain>",
    "rationale": "<one sentence: would A_candidate produce a different metric distribution from B_control at this scale?>",
    "implication": "<one sentence: if false, this candidate is parametrization-only and should be flagged as low-priority>"
  },
  "budget_compliance": {
    "total_runtime_minutes_on_T4": "<numeric estimate>",
    "under_30_min_budget": true | false,
    "memory_compliance_GB": "<numeric estimate>",
    "under_16GB_T4_memory": true | false
  },
  "human_in_loop_runnable": true,
  "notes_for_executor": "<one sentence: any caveat the executor should know>"
}
```

### 2.4 Constraints on step 13

- **Spec generation only** in v10. No actual execution. The `13_experiment_spec.json` file is the artifact.
- **<30 min on free Colab T4**: budget_compliance.total_runtime_minutes_on_T4 MUST be ≤ 30. If the candidate cannot be tested within this budget, the spec is invalid and step 13 emits `trigger_status: "INFEASIBLE_BUDGET"`.
- **Three variants mandatory**: A_candidate, B_control, C_baseline. If C_baseline cannot be identified from step 11.5 or step 06.7, step 13 emits `C_baseline.name: "no_prior_art_baseline (variant compared only to control)"`.
- **Distinguishability pre-check**: a binary flag indicating whether the spec-generator believes A_candidate would produce a different metric distribution from B_control at this scale. If `false`, the candidate is parametrization-only (R279-pattern) and is flagged as low-priority pre-experiment.
- **Statistical test mandatory**: the spec MUST name a specific test and a significance threshold. A spec without these is invalid.
- **Spec is auditable, not executable**: human-in-loop runs the spec; v10 does not execute.

### 2.5 For top-3 candidates per epoch (by mechanical-PASS proximity)

In each v10 epoch, the **top-3 candidates by mechanical-PASS proximity** receive a **full step 13 spec** (all fields populated, distinguishability_pre_check expanded into 3-5 sentences).

Mechanical-PASS proximity is ranked by:
1. step 10 verdict (PASS > FAIL).
2. total_hits (lower is closer).
3. mean per-hint similarity from tree-stream (lower is closer).
4. q_rubric_score (lower is closer).

The non-top-3 candidates either receive a SKIP stub (if step 10 FAIL and tree-stream FAIL) or an abbreviated spec (if step 10 PASS or tree-stream PASS-with-caveat but not in top 3).

---

## 3. Step 13 retrofit for R279

R279 PTCH is the canonical Pattern-C borderline candidate (Phase-0 UNCERTAIN; v7 adversarial downgrade to FAIL_ADVERSARIAL). The Phase 3 of v10 task requires retrofitting step 13 to R279:

- **Spec target:** R279 candidate as A_candidate; integer-ratio singular-value alignment removed (random target spectrum) as B_control; SORSA/SODA as C_baseline (from `11_5_adversarial.papers_found` top entry at functional_similarity 0.80).
- **Validate against actual:** The v7 adversarial finding was that SORSA/SODA at 0.80 covers M_1+M_2+M_4+M_5; only M_3 (integer-ratio target spectrum) differs. The retrofit spec's distinguishability_pre_check should flag this as parametrization-only (test variant A_candidate vs B_control would likely be indistinguishable at small scale because the integer-ratio constraint is a soft regularization that may or may not change top-K spectrum more than a random target would).
- **Expected R279 retrofit outcome:** `distinguishability_pre_check.test_variant_distinguishable_from_control: false` with rationale citing the SORSA/SODA finding.

If step 13 had been part of v5 (E12 / R279's original epoch), R279 would have been flagged pre-experiment as low-priority due to the distinguishability failure. The retrofit confirms step 13 has retroactive diagnostic value.

R279's retrofit is the **single in-context test case** for step 13's diagnostic claim.

---

## 4. Step 04.5 + step 05 — Candidate Policy Update (NEW v10)

### 4.1 What the policy update does

At each epoch start (before round 1 of the epoch), v10 reads:
- The PRIOR epoch's 25 candidate.json files (the `domain`, `candidate_form`, `motivation_strength` fields).
- The PRIOR epoch's 25 verdicts (the `v9_verdict` or `v8_verdict` or `v7_verdict` field from `12_tree_stream.json` or `11_5_adversarial.json` per epoch).

It computes a coarse reward:
- `reward = -1` for FAIL (any FAIL variant: FAIL, FAIL_ADVERSARIAL, FAIL_GAP_REAL_LOGGED).
- `reward = 0` for PASS (no PASS in corpus yet; reserved).
- `reward = -0.5` for PASS-with-caveat (rare).

It aggregates by sub-pattern:
- `motivation_strength × candidate_form` (e.g., `mechanism_transfer × spectral-allocation`).
- `motivation_strength × domain_class` (e.g., `mechanism_transfer × applied-math`; `shared_math_structure × category-theory`).

The aggregate FAIL count per sub-pattern is recorded in `logs/policy_state.json`.

### 4.2 Schema for `logs/policy_state.json`

```json
{
  "schema_version": "1.0",
  "v10_introduced_at_epoch": 29,
  "current_epoch": 29,
  "prior_epoch_used_for_update": 28,
  "policy_aggregates": {
    "motivation_strength_times_candidate_form": [
      {
        "key": "mechanism_transfer × spectral-allocation",
        "fail_count_in_prior_epoch": 2,
        "cumulative_fail_count": 12,
        "cumulative_seen_count": 12,
        "reward_estimate": -1.0,
        "status": "over-mined"
      },
      ...
    ],
    "motivation_strength_times_domain_class": [
      {
        "key": "mechanism_transfer × applied-math",
        "fail_count_in_prior_epoch": 5,
        "cumulative_fail_count": 53,
        "cumulative_seen_count": 53,
        "reward_estimate": -1.0,
        "status": "saturated"
      },
      ...
    ]
  },
  "policy_recommendations_for_next_epoch": {
    "down_weight": ["mechanism_transfer × spectral-allocation", "mechanism_transfer × memory-architecture"],
    "up_weight_explore": ["shared_math_structure × combinatorics", "mechanism_transfer × topology-discrete"],
    "rationale": "<one sentence justifying the recommendation>"
  },
  "candidate_distribution_drift_metrics": {
    "prior_epoch_top_3_subpatterns": [...],
    "next_epoch_planned_subpatterns": [...],
    "drift_score": 0.0
  }
}
```

### 4.3 How the policy biases candidate generation

In step 04.5 (memory-aware check) and step 05 (token streams), the candidate generator consults `logs/policy_state.json` and:

1. **Avoids "over-mined" sub-patterns**: if the proposed candidate's `motivation_strength × candidate_form` is in `policy_recommendations_for_next_epoch.down_weight`, the generator pivots to a different `candidate_form` for this round.
2. **Prefers "explore" sub-patterns**: if a proposed candidate matches an `up_weight_explore` sub-pattern, no pivot needed.
3. **Tracks drift**: at end of epoch, the generator computes `candidate_distribution_drift.drift_score` as a Jaccard distance between prior epoch's top-3 sub-patterns and next epoch's top-3.

The policy is **advisory**; it can be overridden when the candidate is judged to be a legitimate new entry into an over-mined area (e.g., if the candidate is a structurally distinct variant). Overrides are logged in the candidate's `02_decomposition.json` as `policy_override: true`.

### 4.4 Anti-cheating on policy update

- Policy update does NOT modify step 10 or any FROZEN signal.
- Policy update is consulted by the candidate generator BEFORE step 06; it cannot retroactively modify a verdict.
- Drift score is computed at end-of-epoch and stored in `output/stats_round_NNN.json` for audit.
- Reward = 0 is reserved for PASS; reward = -1 for FAIL. The policy CANNOT assign reward = +1 to anything (this would game the verifier). Reward is bounded above by 0 in this corpus.

### 4.5 Connection to step 13 (closing the loop)

Once step 13 generates experiment specs, the policy can additionally track:
- Sub-patterns whose specs have `distinguishability_pre_check.test_variant_distinguishable_from_control: false` (R279-pattern parametrization-only).
- Sub-patterns whose specs have `distinguishability_pre_check: true` (potentially-runnable test cases).

For E29 (the first v10 epoch), this finer signal is not yet available (no prior v10 specs). Starting E30, the policy can incorporate the spec-validity sub-signal.

---

## 5. Step 10 mechanical verdict (★ FROZEN, UNCHANGED FROM v5)

```
10_decision.verdict = "PASS" if total_hits == 0
                    = "FAIL" if total_hits >= 1
forced_by_rule = (keyword_hit_count >= 1)
```

v10 does NOT modify step 10. Neither step 13's distinguishability_pre_check nor the policy update is a step-10 input.

---

## 6. v10 final verdict synthesis

After all steps 08-13:

```
v10_verdict = PASS                       if step_10 PASS
                                          AND tree_stream PASS
                                          AND q_rubric_verdict == NOVEL
                                          AND gap_real == true
                                          AND adversarial_hit == false
                                          AND step_13.distinguishability_pre_check.test_variant_distinguishable_from_control == true
            = PASS_WITH_EMPIRICAL_CAVEAT  if step_10 PASS
                                          AND tree_stream PASS
                                          AND q_rubric_verdict == NOVEL
                                          AND gap_real == true
                                          AND adversarial_hit == false
                                          AND step_13.distinguishability_pre_check.test_variant_distinguishable_from_control == false
                                          (verbal novelty without empirical distinguishability; R279 retroactive pattern)
            = FAIL_ADVERSARIAL            if step_10 PASS AND tree_stream PASS AND adversarial_hit == true
            = FAIL_GAP_REAL_LOGGED        if step_10 FAIL
                                          AND tree_stream max per-hint sim < 0.5
                                          AND gap_real == true
            = FAIL                        otherwise
```

The PASS criterion now requires **EIGHT** independent signals:
1. step 10 keyword (FROZEN)
2. step 10 semantic
3. step 10 functional
4. tree-stream helper + solver synthesis
5. Q-rubric
6. gap_real
7. step 11.5 adversarial
8. step 13 distinguishability_pre_check

**Strictly more demanding than v9** (which had 7 signals).

A new verdict label `PASS_WITH_EMPIRICAL_CAVEAT` captures candidates that passed all 7 v9 signals but failed the v10 step-13 distinguishability check. These are NOT confirmed_substantive_pass; they are an explicit "literature-novel but empirically suspicious" category.

---

## 7. Loop control (v10)

```
# Epoch start
read logs/policy_state.json (or initialize if first v10 epoch)
update policy aggregates from prior epoch
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]:
        execute step

    # Step 04.5 (v3, v10 policy-augmented)
    memory_skip_count = 0
    while True:
        propose (domain_norm, mechanism_keywords, form, motivation_strength)
        load logs/memory_db.json + logs/policy_state.json
        check rules 1, 2, 3 (v3 memory dedup)
        check rule 4 (NEW v10): if (motivation_strength × form) in policy down_weight, pivot
        if any rule fires: continue with new proposal
        else: append ACCEPT (logging policy_override if applicable); break

    # Step 05 (v8, unchanged)
    write 05_prompt_tokens.json
    write 05_sample_tokens.json   (apply stripping rule)
    write 05_task_tokens.json
    write 05_candidate.json       (thin v8 index)

    execute step 06 (★ FROZEN)
    execute step 06.5 (★ FROZEN)
    execute step 06.7 (★ FROZEN)
    execute step 07 (★ FROZEN)

    # Step 08 (v9, unchanged): inverse-search landscape
    spawn inverse-search Agent with ONLY 05_task_tokens.json
    write 08_inverse_landscape.json

    # Step 09 (v9, unchanged): gap-position scoring (deterministic)
    write 09_gap_position.json

    execute step 10 (★ FROZEN)

    # Step 11 (v8, unchanged): Q-rubric
    write 11_qrubric.json
    write 11_audit.json (thin index)

    # Step 12 (v8, unchanged, FROZEN for v10): tree-stream
    write 12_tree_stream.json
    write 12_verification.json (thin index)

    # Step 11.5 (v7, ★ FROZEN): adversarial — only when step 10 PASS AND step 12 PASS
    if 10_decision.verdict == PASS AND 12_tree_stream.tree_stream_verdict == PASS:
        spawn skeptical-reviewer Agent
        write 11_5_adversarial.json
    else:
        write 11_5_adversarial.json with trigger_status = "SKIPPED_..."

    # Step 13 (NEW v10): experiment spec generation
    if 10_decision.verdict == PASS OR 12_tree_stream.tree_stream_verdict == PASS:
        # FIRED case: full spec
        generate 13_experiment_spec.json (full spec; A/B/C variants; distinguishability_pre_check)
    else:
        # SKIPPED case: stub
        write 13_experiment_spec.json with trigger_status = "SKIPPED_step_10_FAIL_AND_tree_stream_FAIL"

    # v10 verdict synthesis
    compute v10_verdict per §6
    update memory_db.json round entry with v10 fields including step_13.fired

    if round_num % 25 == 0:
        write output/stats_round_NNN.json

# Epoch end
compute candidate_distribution_drift between this epoch and prior epoch
update logs/policy_state.json with new aggregates + drift metric
```

---

## 8. v10 score formula

```
score_v10 = (confirmed_substantive_pass × 10)
          + (25 − mean_forced_hit)
          + (tree_stream_step_10_alignment_rate × 5)
          − (false_positive_count × 5)
          − (adversarial_hit_count × 10)
          + (qrubric_step_10_alignment_rate × 3)
          + (mean_hints_per_round / 7 × 2)
          + (gap_real_rate × 4)
          + (FAIL_GAP_REAL_LOGGED_count / N × 2)
          + (step_13_fired_count / N × 3)                ← NEW v10 term
          + (step_13_distinguishable_count / N × 4)      ← NEW v10 term
          − (PASS_WITH_EMPIRICAL_CAVEAT × 2)             ← NEW v10 term (penalizes verbal-novelty-only)
          + (policy_drift_score × 2)                     ← NEW v10 term
```

Where:
- `step_13_fired_count` = rounds where step 13 trigger fired (step 10 PASS OR tree-stream PASS).
- `step_13_distinguishable_count` = rounds where step 13 emits `distinguishability_pre_check.test_variant_distinguishable_from_control: true`.
- `PASS_WITH_EMPIRICAL_CAVEAT` count from v10 final verdict synthesis.
- `policy_drift_score` = Jaccard distance × 1 ∈ [0, 1] between prior and current epoch top-3 sub-patterns.

**Why these terms:**
- `step_13_fired_count × 3`: rewards rounds where the empirical reward layer was actually triggered (a partial signal that the candidate was a near-PASS).
- `step_13_distinguishable_count × 4`: rewards rounds where the candidate articulates a distinguishable experiment (the higher-value signal).
- `PASS_WITH_EMPIRICAL_CAVEAT × -2`: penalizes verbal-novelty-only candidates (R279 pattern). The signal is "we'd want a different verdict here than v9 would have given."
- `policy_drift_score × 2`: rewards meaningful exploration drift between epochs (no drift = the policy update did nothing; high drift = aggressive exploration).

The `confirmed_substantive_pass` definition under v10 requires ALL of:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- tree_stream verdict = PASS, AND
- q_rubric_verdict = NOVEL, AND
- gap_real == true, AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7, AND
- step_13.distinguishability_pre_check.test_variant_distinguishable_from_control == true.

**Eight signals must align.** A v10 PASS is the most demanding criterion in the corpus.

---

## 9. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7+v8+v9)

### 9.1 Step 06 web_search (honesty gate) — UNCHANGED
### 9.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
### 9.3 Step 10 mechanical verdict — UNCHANGED
### 9.4 Step 11.5 adversarial external — UNCHANGED
### 9.5 Step 12 tree-stream — UNCHANGED (★ FROZEN for v10)
### 9.6 v8 components (step 05 token streams, step 11 Q-rubric) — UNCHANGED
### 9.7 v9 components (step 08 inverse-search, step 09 gap-position) — UNCHANGED

v10 is purely ADDITIVE: step 13 + logs/policy_state.json. No prior signal is weakened.

---

## 10. Stats schema additions in v10

`output/stats_round_NNN.json` adds these v10-specific fields on top of v9:

```json
{
  ... (all v1-v9 fields) ...,
  "v10_empirical_reward_metrics": {
    "step_13_fired_count": 0,
    "step_13_skipped_count": 0,
    "step_13_distinguishable_count": 0,
    "step_13_parametrization_only_count": 0,
    "step_13_infeasible_budget_count": 0,
    "real_step_13_Agent_spawns": 0,
    "main_context_direct_step_13": 0,
    "mean_total_runtime_minutes_per_spec": 0.0
  },
  "v10_policy_metrics": {
    "policy_state_file_present": true,
    "policy_down_weight_count": 0,
    "policy_up_weight_explore_count": 0,
    "candidate_distribution_drift_score": 0.0,
    "rounds_with_policy_override": 0
  },
  "v10_verdict_distribution": {
    "v10_PASS_count": 0,
    "v10_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v10_FAIL_count": 0,
    "v10_FAIL_ADVERSARIAL_count": 0,
    "v10_FAIL_GAP_REAL_LOGGED_count": 0
  }
}
```

---

## 11. Anti-cheating commitments (v10 additions on top of v9)

If you catch yourself wanting to:

- **Generate a step 13 spec that is "obviously runnable" with no distinguishability concerns** to inflate the score — don't. The spec must be honest about parametrization-only candidates (set distinguishability_pre_check.test_variant_distinguishable_from_control = false when applicable).
- **Skip step 13 even when the trigger fires** to avoid having to articulate an experiment — don't. The trigger is mechanical; if step 10 PASS OR tree-stream PASS, step 13 MUST fire (full or abbreviated spec).
- **Generate a step 13 spec that needs >30 min on T4** to claim ambitiousness — don't. The budget is hard. If the candidate is too expensive to test in 30 min, the spec is INFEASIBLE_BUDGET and step 13 emits an honest stub.
- **Use the policy update to bias toward "easy PASS" candidates** — don't. The policy only down-weights heavily-FAILED sub-patterns and up-weights unmined sub-patterns. It cannot reward a candidate based on predicted PASS.
- **Modify step 10 or step 12 to make step 13 fire more often** — don't. Step 13 is downstream of step 10 / step 12. Forbidden zones are FROZEN.
- **Synthesize >5 step-13 Agent spawns per epoch** — don't. Per HONEST DEVIATION POLICY: ≤5 synthesized verifiers per epoch; step 13 spec generation usually runs in main context (no Agent spawn needed). Main-context-direct is OPENLY LABELED, NOT a synthesized Agent ID claim.
- **Inflate the policy_drift_score** by reorganizing sub-pattern names — don't. The drift score is computed on canonical sub-pattern keys (motivation_strength × candidate_form); cosmetic relabeling is detectable.

The v3/v4/v5/v6/v7/v8/v9 instructions stand: data on agent impulse-to-bypass is more valuable than a clean fake run.

---

## 12. Inherited history (v1 → ... → v10)

- **v1**: file-chain + mechanical keyword rule + cross-agent verification. R001-R025.
- **v2**: Form A/B/C/D rotation. R026-R050.
- **v3**: step 04.5 memory check. R051-R075.
- **v4**: step 06.5 semantic-similarity. R076-R100.
- **v5**: step 06.7 functional-equivalence judge. R101-R575 across E5-E23.
- **v6**: step 06.8 per-paper-completeness. R576-R600 E24 (DEPRECATED).
- **v7**: reverts to v5 base; adds step 11.5 adversarial external. R601-R650 E25-E26.
- **v8**: keeps v7 base + step 11.5; adds three structural upgrades (problem/solution/evaluation structure). R651-R675 E27.
- **v9**: keeps v8 base; adds inverse-search landscape generation (step 08 + step 09). R676-R700 E28.
- **v10** (this file): keeps v9 base; adds empirical-reward step 13 + candidate-policy logs/policy_state.json. **R701-R725 + R279 retrofit runs under v10 in E29.**

---

## 13. What v10 does NOT promise

v10 does NOT promise more substantive PASS verdicts. The 796-round saturation result (0 confirmed substantive PASS, p ≈ 0.000335 on 1%-novelty H₀ at N=796) stands. v10's step 13 is a NEW orthogonal channel — partial empirical reward — not a yield-boosting trick.

What v10 promises:
- The first **partial empirical reward channel** in the corpus (step 13 spec generation).
- The first **per-episode policy-gradient mechanism** (logs/policy_state.json).
- A new verdict label `PASS_WITH_EMPIRICAL_CAVEAT` for verbal-novelty-only candidates.
- Strictly tighter PASS criterion (8 signals must align) than v9 (7 signals).
- R279 retrofit validates step 13's diagnostic claim retroactively.

v10 cannot guarantee 0 false positives. The "verbal novelty without empirical mechanism value" failure mode is partially addressed by step 13 spec generation but is not fully tested until the specs are executed (human-in-loop, post-v10). v10 cannot guarantee 0 false negatives either; the mechanical FROZEN step 10 ratchet ensures conservative bias.

---

## 14. Honest deviation policy (for E29 execution)

Per the v10 task description:
- Real WebSearch in step 06 (mandatory; same as v5-v9).
- Real Agent spawn for step 08 (inverse-search) and step 12 (helper) WHERE FEASIBLE.
- Step 13 spec generation runs in MAIN CONTEXT by default (no Agent spawn required; openly labeled).
- Per epoch, ≤5 synthesized Agent spawns across all steps. Excess uses main-context-direct labeling (NOT a fake Agent ID claim).
- Wall-clock timestamps ≥ 3-min logical gap per round (E29 explicit relaxation from E28's 4-min gap, per task description; logical-not-wall-clock the same as E25/E27/E28).
- R279 retrofit is epoch 29 round 0: a single retrospective run of step 13 on R279, written into `rounds/round_279/13_experiment_spec.json`. R279's step 13 is in addition to the 25 new rounds R701-R725.
