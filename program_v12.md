# program_v12.md
## Niche-Mining Pipeline — v12: Generator-Side Intervention (step 05.5 Anti-R279 Filter)

This file extends the **v11 base pipeline** (= v10 base + step 13.5 adversarial-empirical attack) with ONE NEW structural upgrade that addresses v11's diagnosed limitation (see `output/v11_limitation_analysis.md`):

> v11's verifier chain (step 11.5 + step 13 + step 13.5) can reliably KILL R279-pattern candidates (4/4 on R279 retrofit, 2/3 load-bearing on E30 fired specs) — but every step-13-FIRED candidate in corpus history (R279, R708, R715, R725, R735, R741, R744) is an R279-pattern variant (fixed scalar/diagonal/functional prior on an existing learnable parameter). Step 05 keeps generating R279-pattern candidates as the path of least resistance through the 4-sub-mechanism decomposition. v12 introduces step 05.5: a mechanical structural classifier that fires BEFORE step 06 and rejects R279-pattern candidates outright, forcing the generator to retry with architectural-topology candidates.

### Hard constraints carried forward (★ FORBIDDEN-TO-MODIFY zones)

The following zones are **FROZEN** verbatim from v5 / v7 / v8 / v9 / v10 / v11:

- **Step 06 web_search** (honesty gate)
- **Step 07 keyword threshold ≥ 2** (mechanical hit)
- **Step 10 mechanical verdict** (`total_hits ≥ 1` → FAIL — keyword ∪ semantic ∪ functional)
- **Step 12 tree-stream** (v8 helper + per-hint solver + conservative synthesis)
- **Step 13 spec format** (v10 contribution; v12 reads it but does not modify it)
- **Step 13.5 attack format** (v11 contribution; v12 reads it but does not modify it)
- **All v8 components** (step 05 token streams, step 11 Q-rubric)
- **All v9 components** (step 08 inverse-search, step 09 gap-position)
- **All v10 components** (step 13 spec generation, `logs/policy_state.json` policy update, PASS_WITH_EMPIRICAL_CAVEAT verdict label)
- **All v11 components** (step 13.5 attack, FAIL_EMPIRICAL_ATTACK verdict label)

v12 is **strictly additive**. It ADDS step 05.5 between step 05 and step 06. It does NOT modify any prior file or any prior step.

---

## 0. Why generator-side intervention and not something else

### 0.1 The v11 limitation diagnosed in `output/v11_limitation_analysis.md`

v11 added an adversarial-empirical attack on step 13's spec. The attack works — succeeded 11 times across 14 attacks in E30 + R279 retrofit. But the targets (R279/R708/R715/R725/R735/R741/R744) are all the same R279-pattern (fixed scalar/diagonal/functional prior on existing learnable parameter). The verifier chain catches R279-pattern reliably; the generator keeps producing R279-pattern.

The asymmetry stated in `output/v10_limitation_analysis.md` and reaffirmed:
> **The pipeline can KILL bad candidates but cannot GENERATE good ones.**

v11 strengthened the KILL side. v12 must address the GENERATE side.

### 0.2 The four candidate v12 upgrades

| Option | Where it intervenes | Cost | Addresses R279-pattern? |
|---|---|---|---|
| (a) Distinguishability-conditioned generation | step 05 output check | medium | partial (post-hoc claim) |
| **(b) Anti-R279 candidate filter** | step 05.5 mechanical filter | low | **directly — rejects R279-pattern pre-search** |
| (c) Adversarial candidate generator | step 05 parallel agent | medium | indirect (extra LLM context may also R279) |
| (d) Empirical-result-conditioned generation | step 05 prompt augment | low | indirect (already attempted via policy_state in v10; LLM misaligns) |

**v12 adopts direction (b).** See `output/v11_to_v12_diff.md` §0 for the cost/benefit analysis.

### 0.3 Symmetry with prior mechanical filters

v12's step 05.5 is symmetric with the prior corpus's deterministic mechanical filters:
- **Step 07** (keyword threshold ≥ 2): deterministic check on `06_search_raw.json`, decides forced-hit status.
- **Step 09** (gap_position): deterministic rule applied to `08_inverse_landscape.json`, decides gap_real status.
- **Step 05.5** (NEW v12): deterministic structural classifier applied to `05_candidate.json`, decides R279-pattern status.

All three fire BEFORE the LLM-based verifier chain. All three produce a single mechanical verdict from a fixed rule. v12 follows the same pattern at step 05's output.

### 0.4 What v12 does NOT change

- All FORBIDDEN-TO-MODIFY zones (§9 below) — UNCHANGED.
- v8 step 05 token-stream FORMAT — UNCHANGED. (Step 05.5 reads the JSON output but does not modify the format or the generation prompt.)
- v10 step 13 / v11 step 13.5 — UNCHANGED.
- `logs/policy_state.json` schema — UNCHANGED.
- PASS criterion floor (still requires all 9 prior signals) — UNCHANGED; v12 adds ONE pre-condition (must not be R279-pattern at step 05.5).
- Cumulative N_verified counting protocol — UNCHANGED.

---

## 1. File chain (v11 + one addition)

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
    05_5_pattern_filter.json          ← NEW v12 (per-round; FIRED or PASS)

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN
    06_7_functional_hits.json        ★ FROZEN
    07_hit_miss.json                 ★ FROZEN

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json                 ★ FROZEN

    11_qrubric.json
    11_audit.json
    12_tree_stream.json              ★ FROZEN for v12
    12_verification.json
    11_5_adversarial.json            ★ FROZEN

    13_experiment_spec.json          ★ FROZEN for v12 (read but not modified)
    13_5_adversarial_spec.json       ★ FROZEN for v12 (read but not modified)
```

Side-channel (UNCHANGED from v11):
```
logs/policy_state.json
```

A v12 round MUST contain all v11 files PLUS `05_5_pattern_filter.json`. Step 05.5's verdict is recorded as either `PASS` (candidate is not R279-pattern; proceed to step 06) or `REJECTED_R279_PATTERN` (candidate is R279-pattern; regenerate with explicit anti-R279 instruction OR record as a documented rejection and proceed with NEW candidate). When REJECTED, the round records BOTH the rejected candidate AND the regenerated candidate, preserving audit trail.

---

## 2. Step 05.5 — Anti-R279 mechanical structural filter (NEW v12)

### 2.1 What step 05.5 does

Step 05.5 is the first **generator-side mechanical filter** in the corpus. It runs AFTER step 05 produces `05_candidate.json` and BEFORE step 06 web_search. The filter applies a 3-question deterministic structural classifier to the candidate's `llm_application` field:

```
R279_pattern_check(candidate):
    Q1. Does the candidate introduce a NEW learnable module (matrix, MLP, attention sub-layer)
        that is NOT a function of the baseline's existing parameters?
    Q2. Does the candidate add a NEW inter-layer/inter-head/inter-token connection
        that the baseline lacks?
    Q3. Does the candidate change the layer topology (depth, width, fan-in/out)
        in a way that is NOT a function of an existing parameter?

    architectural_topology_change = Q1 OR Q2 OR Q3
    R279_pattern = NOT architectural_topology_change
```

Operationalization (deterministic from `05_candidate.json` text alone):
- **Q1 = YES** if the candidate's `llm_application` contains explicit construction of a new learnable matrix / new bias / new gate / new module with parameters NOT present in the baseline (a learnable τ, β, W, M, etc., that is added on top of, not derived from, baseline parameters).
- **Q2 = YES** if the candidate's `llm_application` introduces a NEW edge in the computation graph that the baseline lacks (cross-layer skip connection from a non-existing place, a new attention pathway between previously-disconnected heads, a new pathway from token positions to non-existing places).
- **Q3 = YES** if the candidate's `llm_application` changes layer count / head count / hidden width / kernel-method family in a way that is NOT a function of an existing parameter (e.g., switches from softmax-kernel to random-Fourier-feature-kernel; goes from monolithic attention to gated mixture-of-experts; introduces a parallel pathway with its own learnable parameters).

If ALL THREE are NO → **R279_pattern = TRUE** → step 05.5 returns `REJECTED_R279_PATTERN`.
If ANY ONE is YES → architectural-topology-change → step 05.5 returns `PASS`.

### 2.2 Step 05.5 trigger logic

```
trigger_step_05_5 = always (every round runs step 05.5)
```

Every v12 round runs step 05.5. There is no SKIP path. The output is always `05_5_pattern_filter.json`.

### 2.3 Step 05.5 schema

```json
{
  "round": "NNN",
  "epoch": 12,
  "trigger_status": "FIRED",
  "candidate_classifier_input": {
    "llm_application": "<echo of 05_candidate.json llm_application>",
    "K_sub_mechanisms": <int>,
    "sub_mechanisms": [...],
    "candidate_form": "<from 05_candidate.json>"
  },
  "structural_questions": {
    "Q1_new_learnable_module": true | false,
    "Q1_evidence": "<one sentence pointing to where in llm_application this module is introduced (or absent)>",
    "Q2_new_inter_layer_connection": true | false,
    "Q2_evidence": "<one sentence>",
    "Q3_layer_topology_change": true | false,
    "Q3_evidence": "<one sentence>"
  },
  "architectural_topology_change": true | false,
  "R279_pattern": true | false,
  "verdict": "PASS | REJECTED_R279_PATTERN",
  "regeneration_attempted": true | false,
  "regenerated_candidate_summary": "<one sentence: if regenerated, the new architectural-topology candidate>",
  "regenerated_candidate_file": "<filename or null if no regeneration>",
  "regenerated_candidate_passed_step_05_5": true | false | null,
  "rationale": "<2-3 sentences: synthesize the 3-question outcome into a final R279_pattern verdict>",
  "post_filter_candidate_used_downstream": "<rejected candidate's ID or regenerated candidate's ID>",
  "honest_classification_note": "Step 05.5 is deterministic from 05_candidate.json text; no Agent spawn required. Classifier verdicts and per-question evidence are auditable line-by-line."
}
```

### 2.4 Regeneration protocol (when step 05.5 rejects)

When step 05.5 returns `REJECTED_R279_PATTERN`:

```
on REJECTED_R279_PATTERN:
    1. Log the rejected candidate (preserve 05_candidate.json as 05_candidate_rejected.json)
    2. Regenerate with explicit anti-R279 instruction prepended to step 05 prompt:
       "The previous candidate at this round was R279-pattern (fixed scalar/diagonal
        functional prior on existing learnable parameter). Generate a NEW candidate
        that introduces architectural-topology change: a NEW learnable module OR
        a NEW inter-layer connection OR a NEW layer topology. Reject any candidate
        whose 'llm_application' is a functional/measurement/ranking on existing
        baseline parameters."
    3. Re-run step 05 → step 05.5 with the regenerated candidate
    4. Accept the regenerated candidate IF it passes step 05.5 (architectural_topology_change = TRUE)
    5. If 2 consecutive regenerations fail step 05.5, accept the second regeneration
       AND log policy_override_step_05_5 = true (no infinite loop)
```

### 2.5 Post-filter downstream behavior

After step 05.5 PASS:
- Step 06 web_search runs normally on the post-filter candidate (FROZEN).
- All downstream steps (07/08/09/10/11/11.5/12/13/13.5) run normally.
- The candidate is now an architectural-topology candidate (by step 05.5 definition).

Predicted downstream shifts (testable):
- Mean kw forced-hit may go UP (architectural-topology candidates share keywords with major architectural papers).
- step 13.5 attack_success_rate may go DOWN on FIRED rounds (architectural candidates have different load-bearing weakness profile).

### 2.6 Constraints on step 05.5

- **Deterministic and auditable.** The 3-question classifier is applied to text. Each question's verdict has a 1-sentence evidence pointer to specific `llm_application` content. No Agent spawn needed; main-context-direct is the default.
- **Falsifiable.** Each question has a definite TRUE/FALSE answer based on the candidate text. If unclear, default to FALSE (more conservative — more rejections).
- **Pre-search rejection.** Step 05.5 fires BEFORE step 06. R279-pattern candidates do not consume step 06-13 budget; they are rejected and regenerated.
- **One-step regeneration cap.** ≤2 regenerations per round. If both regenerations also fail step 05.5, accept the second one and log `policy_override_step_05_5`.
- **Does not modify step 05 output schema.** Step 05 still produces `05_candidate.json` with the same fields. Step 05.5 reads it, does not modify it. Regenerated candidates overwrite `05_candidate.json` only when accepted (and `05_candidate_rejected.json` preserves the rejected version).

### 2.7 For E31 R751-R775 plus R279 step-05-5 retrofit

In E31:
- Every round runs step 05.5 (25 rounds).
- Expected step-05.5 rejection rate: 0.4-0.6 (10-15 rejections from 25 baseline-attempted candidates, based on the R279-pattern dominance documented in `output/v11_limitation_analysis.md` §3.1).
- Per HONEST DEVIATION POLICY ≤5 synthesized Agent spawns per epoch, step 05.5 is main-context-direct by default (deterministic classifier; no Agent spawn needed).
- **R279 step 05.5 retrofit:** apply step 05.5 retroactively to `rounds/round_279/05_candidate.json`. Expected outcome: R279_pattern = TRUE; verdict = REJECTED_R279_PATTERN (with regeneration logged retroactively). Validates that step 05.5 correctly classifies R279 (the canonical R279-pattern candidate).

---

## 3. Step 05.5 classifier examples (for the v12 implementer)

### 3.1 R279-PATTERN examples (REJECTED at step 05.5)

**R279 PTCH:**
- llm_application: "constrain each head's top-K singular directions to integer-ratio multiples"
- Q1 (new learnable module): NO — the SVD already exists in baseline LoRA; constraint is on existing values
- Q2 (new connection): NO — uses existing per-head computation
- Q3 (topology change): NO — same head count, same layer count, same kernel family
- Verdict: **REJECTED_R279_PATTERN**

**R708 Dirichlet:**
- llm_application: "Form a Dirichlet series in s using attention-head importance values"
- Q1: NO — uses existing head-importance values
- Q2: NO — single-head computation
- Q3: NO — pruning only
- Verdict: **REJECTED_R279_PATTERN**

**R735 trace-class:**
- llm_application: "Per-head attention matrix → nuclear norm + 2nd/3rd cumulant traces → joint quantile ranking → prune"
- Q1: NO — functionals on existing matrices
- Q2: NO — single-head computation
- Q3: NO — pruning only
- Verdict: **REJECTED_R279_PATTERN**

**R744 spectral-sequence E_2:**
- llm_application: "Filter loss by depth; compute E_2 page differentials; trigger depth cap on E_2 stabilization"
- Q1: NO — uses existing loss filtration
- Q2: NO — same layer-depth indexing
- Q3: NO — depth-cap is a stopping criterion, not a new topology
- Verdict: **REJECTED_R279_PATTERN** (note: even R744, which survived step 13.5 attack, is still R279-pattern at the structural level — it just happens to have a hard-to-attack functional)

### 3.2 ARCHITECTURAL-TOPOLOGY-CHANGE examples (would PASS step 05.5)

**Hypothetical candidate H1: Cross-head learnable communication gate**
- llm_application: "Introduce a NEW learnable square matrix G ∈ R^{H × H} between heads in each layer. Compute G·attention_outputs as a global head-mixing operation before residual."
- Q1: YES — G is a NEW learnable matrix not present in baseline
- Verdict: **PASS** (architectural-topology change)

**Hypothetical candidate H2: Random-Fourier-feature kernel attention**
- llm_application: "Replace softmax attention with random-Fourier-feature kernel attention. Project keys and queries with a learnable kernel-bandwidth parameter σ. Compute kernel similarity via 1024 random Fourier features."
- Q3: YES — kernel family changed from softmax to RFF
- Verdict: **PASS**

**Hypothetical candidate H3: Parallel low-rank pathway with learnable bridge**
- llm_application: "Add a parallel low-rank pathway W_p = U_p V_p^T (NEW learnable U_p, V_p) that runs alongside attention and is added via learnable mixing gate γ"
- Q1: YES — U_p, V_p, γ are new learnable parameters
- Verdict: **PASS**

### 3.3 Edge cases (default to R279-pattern when ambiguous)

Edge case 1: Candidate says "add a learnable scalar α that interpolates between existing methods"
- Q1: a learnable scalar α is technically a "new learnable module" — but interpolating between existing methods is a parameterization choice, not a topology change.
- v12 convention: a single learnable SCALAR that is a function of existing methods → Q1 = NO → R279_pattern = TRUE.
- A learnable MATRIX or MLP that introduces new degrees of freedom → Q1 = YES → architectural-topology-change.

Edge case 2: Candidate that prunes layers conditioned on a learned condition
- Q3 (topology change): does pruning depth based on a learned criterion count as topology change?
- v12 convention: pruning IS a topology change at inference, but the structural prior dimension comes from an existing parameter (the criterion's input). NO → R279_pattern = TRUE unless the candidate also adds a learnable component.

Edge case 3: Candidate introduces a new training objective that changes gradient flow
- Q1-Q3: a NEW objective is a new optimization signal but not necessarily a new architectural component.
- v12 convention: if the objective adds a learnable component (a learnable target/teacher/discriminator), Q1=YES. If the objective is a fixed functional of existing parameters, NO → R279_pattern = TRUE.

### 3.4 Calibration with corpus

Applying the §3.1 classifier to corpus history:
- R279, R708, R715, R725, R735, R741, R744: all REJECTED (R279-pattern). 7/7.
- Most other rounds in E29/E30 are also R279-pattern at the same structural level — they just don't fire step 13 because they don't pass mechanical-PASS-proximity ranking.

Predicted E31 rejection rate: 60-80% (15-20 of 25 baseline-step-05-attempted candidates are R279-pattern at the classifier level).

The classifier is conservative — when in doubt, defaults to R279-pattern (REJECTED), which is the desired behavior (force step 05 to retry on architectural-topology).

---

## 4. v12 final verdict synthesis

After all steps 05.5-13.5:

```
v12_verdict =
    PASS                          if step_05_5 PASS
                                  AND step_10 PASS
                                  AND tree_stream PASS
                                  AND q_rubric_verdict == NOVEL
                                  AND gap_real == true
                                  AND adversarial_hit == false
                                  AND step_13.pre_check.test_variant_distinguishable_from_control == true
                                  AND step_13_5.post_attack_distinguishability_verdict == true

    PASS_WITH_EMPIRICAL_CAVEAT    if step_05_5 PASS
                                  AND step_10 PASS
                                  AND tree_stream PASS
                                  AND q_rubric_verdict == NOVEL
                                  AND gap_real == true
                                  AND adversarial_hit == false
                                  AND (step_13.pre_check == false OR step_13_5.post_attack ∈ {downgraded_to_uncertain, downgraded_to_false, false})

    FAIL_EMPIRICAL_ATTACK         if step_05_5 PASS
                                  AND step_10 PASS
                                  AND tree_stream PASS
                                  AND q_rubric_verdict == NOVEL
                                  AND gap_real == true
                                  AND adversarial_hit == false
                                  AND step_13_5.load_bearing_attack_succeeded == true
                                  AND step_13_5.post_attack == "downgraded_from_uncertain_to_false"
                                  AND step_13.pre_check was "uncertain"

    REJECTED_R279_PATTERN         if step_05_5.verdict == "REJECTED_R279_PATTERN"
                                  AND regeneration_failed_twice == true
                                  (a v12 verdict only — does NOT exist in v10/v11)

    FAIL_ADVERSARIAL              if step_05_5 PASS AND step_10 PASS AND tree_stream PASS AND adversarial_hit == true
    FAIL_GAP_REAL_LOGGED          if step_05_5 PASS AND step_10 FAIL AND tree_stream max sim < 0.5 AND gap_real == true
    FAIL                          otherwise
```

The PASS criterion now requires **TEN** independent signals:
1. step 05.5 architectural-topology-change (NEW v12)
2. step 10 keyword (FROZEN)
3. step 10 semantic
4. step 10 functional
5. tree-stream helper + solver synthesis
6. Q-rubric
7. gap_real
8. step 11.5 adversarial-literature
9. step 13 distinguishability pre-check
10. step 13.5 post-attack distinguishability verdict

**Strictly more demanding than v11** (which had 9 signals).

A new verdict label `REJECTED_R279_PATTERN` captures candidates where step 05's recipe lands on R279-pattern AND two regenerations also produce R279-pattern. These are NOT FAIL (they failed at step 05.5, never reached step 06); they are a separate category.

---

## 5. Loop control (v12)

```
# Epoch start (UNCHANGED from v11)
read logs/policy_state.json (or initialize)
update policy aggregates from prior epoch
write logs/policy_state.json with current_epoch += 1

while round_in_epoch < 25:
    round_num += 1
    mkdir rounds/round_{round_num:03d}/

    for step in [01, 02, 03, 04]: execute (UNCHANGED)
    execute step 04.5 (v10 policy-augmented)
    execute step 05 (UNCHANGED — v8 token streams)

    # Step 05.5 (NEW v12): mechanical anti-R279 filter
    execute step 05.5 → produces 05_5_pattern_filter.json
    if step 05.5 verdict == REJECTED_R279_PATTERN:
        log rejected candidate as 05_candidate_rejected_attempt_1.json
        regenerate step 05 with explicit anti-R279 instruction
        re-run step 05.5 on regenerated candidate
        if regenerated also fails step 05.5:
            log 05_candidate_rejected_attempt_2.json
            regenerate once more with stronger anti-R279 instruction
            re-run step 05.5
            if 3rd attempt also fails:
                log policy_override_step_05_5 = true
                accept the 3rd attempt (no infinite loop)

    execute step 06 (★ FROZEN) on post-filter candidate
    execute step 06.5 / 06.7 (★ FROZEN)
    execute step 07 (★ FROZEN)
    execute step 08 (v9 inverse-search) (UNCHANGED)
    execute step 09 (v9 gap-position) (UNCHANGED)
    execute step 10 (★ FROZEN)
    execute step 11 (v8 Q-rubric) (UNCHANGED)
    execute step 12 (v8 tree-stream) (★ FROZEN for v12)
    execute step 11.5 (v7 adversarial) (★ FROZEN)
    execute step 13 (v10 spec) (★ FROZEN for v12)
    execute step 13.5 (v11 attack) (★ FROZEN for v12)

    # v12 verdict synthesis
    compute v12_verdict per §4
    update memory_db.json round entry with v12 fields including step_05_5

    if round_num % 25 == 0:
        write output/stats_round_NNN.json

# Epoch end (UNCHANGED from v11)
compute candidate_distribution_drift_score
update logs/policy_state.json with new aggregates + step_05_5_rejection_aggregates
```

---

## 6. v12 score formula

```
score_v12 = (confirmed_substantive_pass × 10)
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
          + (step_05_5_rejection_rate × 3)                      ← NEW v12 term
          + (architectural_topology_change_rate × 4)            ← NEW v12 term
          + (regeneration_success_rate × 2)                     ← NEW v12 term
          − (REJECTED_R279_PATTERN_count × 1)                   ← NEW v12 term
```

Where:
- `step_05_5_rejection_rate` = (REJECTED_R279_PATTERN count at first attempt) / N. Rewards the channel for being discriminating (correctly identifying R279-pattern candidates). Range [0, 1].
- `architectural_topology_change_rate` = (rounds with final candidate passing step 05.5) / N. Rewards post-filter candidate quality. Higher means more architectural-topology candidates reach step 06.
- `regeneration_success_rate` = (rounds where regeneration produced architectural-topology candidate) / (rounds with at least 1 rejection). Rewards step 05's ability to escape R279-pattern when explicitly instructed. Calibration: 0 means generator can't escape R279-pattern even with instruction; 1 means generator escapes on first regeneration.
- `REJECTED_R279_PATTERN_count × -1`: small penalty per REJECTED_R279_PATTERN final verdict (= 3 consecutive R279-pattern attempts). These are diagnostically informative (signal that the generator is stuck) but represent failure to produce architectural candidates.

**Why these terms:**
- `step_05_5_rejection_rate × 3`: rewards filtering R279-pattern. Calibrated similar to step_13_5 attack success rate × 3.
- `architectural_topology_change_rate × 4`: rewards moving the candidate population. Highest weight because this is the v12 goal.
- `regeneration_success_rate × 2`: rewards the step 05 generator's ability to escape R279-pattern when instructed (validates the regeneration protocol works).
- `REJECTED_R279_PATTERN_count × -1`: small penalty for terminal R279-pattern verdicts; these are failures of the generator to escape, not failures of the verifier.

The `confirmed_substantive_pass` definition under v12 requires ALL of:
- step 05.5 PASS (architectural-topology change confirmed), AND
- keyword overlap < 2, AND
- semantic cosine < 0.7, AND
- functional judge < 0.7, AND
- tree_stream verdict = PASS, AND
- q_rubric_verdict = NOVEL, AND
- gap_real == true, AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7, AND
- step_13.distinguishability_pre_check == true, AND
- step_13_5.post_attack_distinguishability_verdict == true.

**Ten signals must align.** A v12 PASS is the strictest criterion in corpus history.

---

## 7. R279 step 05.5 retrofit (Phase 3 of v12 task)

R279 PTCH is the canonical R279-pattern candidate. v12 applies step 05.5 retroactively to `rounds/round_279/05_candidate.json`:

Per §3.1:
- Q1: NO (no new learnable module; uses existing SVD)
- Q2: NO (single-head computation; no new inter-head connection)
- Q3: NO (same head count, same kernel family)
- Verdict: **REJECTED_R279_PATTERN**

This is the trivially-correct classification — R279 is the CANONICAL R279-pattern candidate. Step 05.5 retrofit validates the classifier on the namesake.

Expected retrofit output: `rounds/round_279/05_5_pattern_filter.json` with R279_pattern=TRUE, verdict=REJECTED_R279_PATTERN, regeneration_attempted=false (retrofit doesn't regenerate; only classifies).

This is in addition to:
- R279 v7 step 11.5 (literature finding: SORSA/SODA at 0.80 covers M_1+M_2+M_4+M_5)
- R279 v10 step 13 (structural finding: distinguishability=false)
- R279 v11 step 13.5 (adversarial-empirical finding: 4/4 attacks succeeded)

So **R279 retrofit now has 4 independent rejection signals** (literature + structural + adversarial-empirical + structural-classifier).

---

## 8. Anti-cheating commitments (v12 additions on top of v11)

If you catch yourself wanting to:

- **Classify candidates as ARCHITECTURAL-TOPOLOGY-CHANGE when they're R279-pattern** to inflate step_05_5 PASS rate — don't. The 3-question classifier is conservative: when in doubt, default to R279-pattern (REJECTED). Q1-Q3 each have a 1-sentence evidence pointer; if you can't write the evidence, the answer is NO.
- **Spawn step 05.5 as an Agent call to launder the classification** — don't. Step 05.5 is mechanical from the candidate JSON text alone. Main-context-direct labeling is the default. An Agent spawn for step 05.5 is allowed but adds no signal — the classification rule is deterministic.
- **Regenerate the same R279-pattern candidate dressed in different vocabulary** — don't. The regeneration MUST introduce architectural-topology change (Q1/Q2/Q3 = YES). If the regenerated candidate fails step 05.5 too, log policy_override_step_05_5 and proceed.
- **Skip step 05.5 on already-known-R279-pattern candidates** — don't. Every round runs step 05.5. The classifier is cheap and deterministic.
- **Promote a REJECTED_R279_PATTERN candidate through the rest of the pipeline** — don't. REJECTED candidates do NOT proceed to step 06. If you accept the post-2nd-regeneration candidate via policy_override, the override is logged and the candidate still runs steps 06-13.5 but the final v12 verdict is `REJECTED_R279_PATTERN` (overriding any downstream PASS).
- **Define R279-pattern loosely to make filter less aggressive** — don't. The definition is in §2.1 / §3 and is structural, not topical.

---

## 9. ★ FORBIDDEN-TO-MODIFY zones (preserved verbatim from v5+v7+v8+v9+v10+v11)

### 9.1 Step 06 web_search — UNCHANGED
### 9.2 Step 07 keyword threshold ≥ 2 — UNCHANGED
### 9.3 Step 10 mechanical verdict — UNCHANGED
### 9.4 Step 11.5 adversarial external — UNCHANGED
### 9.5 Step 12 tree-stream — UNCHANGED (★ FROZEN for v12)
### 9.6 v8 components — UNCHANGED (step 05 generation schema preserved; step 05.5 reads 05_candidate.json without modifying it)
### 9.7 v9 components — UNCHANGED
### 9.8 v10 step 13 spec format — UNCHANGED (★ FROZEN for v12)
### 9.9 v11 step 13.5 attack format — UNCHANGED (★ FROZEN for v12)
### 9.10 v10 policy state schema — UNCHANGED

v12 is purely ADDITIVE: step 05.5 + new `REJECTED_R279_PATTERN` verdict label.

---

## 10. Stats schema additions in v12

`output/stats_round_NNN.json` adds these v12-specific fields on top of v11:

```json
{
  ... (all v1-v11 fields) ...,
  "v12_pattern_filter_metrics": {
    "step_05_5_total_attempts": 0,
    "step_05_5_first_attempt_REJECTED_count": 0,
    "step_05_5_first_attempt_PASS_count": 0,
    "step_05_5_regeneration_attempted_count": 0,
    "step_05_5_regeneration_succeeded_count": 0,
    "step_05_5_two_regenerations_failed_count": 0,
    "step_05_5_rejection_rate_first_attempt": 0.0,
    "step_05_5_final_PASS_count": 0,
    "step_05_5_REJECTED_R279_PATTERN_final_verdict_count": 0,
    "real_step_05_5_Agent_spawns": 0,
    "main_context_direct_step_05_5": 0,
    "Q1_yes_count_first_attempt": 0,
    "Q2_yes_count_first_attempt": 0,
    "Q3_yes_count_first_attempt": 0
  },
  "v12_post_filter_downstream_metrics": {
    "mean_kw_forced_hit_post_filter": 0.0,
    "mean_kw_forced_hit_pre_filter_baseline": 0.0,
    "step_13_fired_count_post_filter": 0,
    "step_13_5_attack_success_rate_post_filter": 0.0,
    "architectural_topology_candidate_distinguishability_distribution": {"true": 0, "false": 0, "uncertain": 0}
  },
  "v12_verdict_distribution": {
    "v12_PASS_count": 0,
    "v12_PASS_WITH_EMPIRICAL_CAVEAT_count": 0,
    "v12_FAIL_count": 0,
    "v12_FAIL_ADVERSARIAL_count": 0,
    "v12_FAIL_GAP_REAL_LOGGED_count": 0,
    "v12_FAIL_EMPIRICAL_ATTACK_count": 0,
    "v12_REJECTED_R279_PATTERN_count": 0
  },
  "v12_verdict_shift_metrics": {
    "verdict_shift_v11_to_v12_count": 0,
    "rounds_where_v12_disagrees_with_v11": [],
    "shift_categories": {
      "v11_FAIL_to_v12_REJECTED_R279_PATTERN": 0,
      "v11_FAIL_to_v12_FAIL_with_kw_higher": 0
    }
  }
}
```

---

## 11. Anti-cheating commitments (v12 additions on top of v11)

The v3/v4/v5/v6/v7/v8/v9/v10/v11 instructions stand. v12 adds:

- **Step 05.5 classifier honesty.** Each of Q1/Q2/Q3 must have a 1-sentence evidence pointer to specific text in `05_candidate.json` `llm_application` field. "I just have a feeling" is not evidence.
- **Regeneration must produce a structurally-different candidate.** "Same candidate, new vocabulary" is the failure mode the filter exists to prevent.
- **Step 05.5 verdict is the verifier's verdict, not the regenerator's.** Step 05.5 runs on each candidate independently, including regenerated ones.
- **Conservative defaults.** When unsure about Q1/Q2/Q3, default to NO (which leads to REJECTED). This is the safer error direction — preferring false rejections to false acceptances.
- **One-way ratchet on verdict.** Step 05.5 verdict for a given candidate cannot be flipped post-hoc. Even if downstream verification passes, REJECTED_R279_PATTERN at step 05.5 sticks (unless override is logged).
- **Step 05.5 is NOT to be skipped.** Every round runs it. The classifier file (`05_5_pattern_filter.json`) is mandatory in v12.

---

## 12. Inherited history (v1 → ... → v12)

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
- **v12** (this file): v11 base + step 05.5 anti-R279 mechanical structural filter (generator-side intervention). **R751-R775 + R279 step-05.5 retrofit-classifier run under v12 in E31.**

---

## 13. What v12 does NOT promise

v12 does NOT promise more substantive PASS verdicts. The 846-round saturation result (0 confirmed substantive PASS, p ≈ 0.000203 on 1%-novelty H₀ at N=846) stands. v12's step 05.5 is a NEW orthogonal extension on the GENERATOR SIDE; it does not guarantee PASS rate change. PASS rate depends on the actual novelty distribution of architectural-topology candidates, not on filtering R279-pattern.

What v12 promises:
- The first **generator-side mechanical filter** in the corpus (step 05.5 anti-R279 classifier).
- A new verdict label `REJECTED_R279_PATTERN` for candidates whose generator is stuck on R279-pattern.
- Strictly tighter PASS criterion (10 signals must align) than v11 (9 signals).
- The first **pre-search rejection** mechanism in the corpus — R279-pattern candidates do not consume step 06-13.5 budget.
- Symmetric design with step 07 (keyword threshold) and step 09 (gap-position) — all mechanical filters with deterministic verdicts.
- R279 retrofit-classification validates that step 05.5 correctly classifies the namesake R279-pattern candidate.

v12 cannot promote step 05 to a true architectural-topology generator on its own. v12 can FORCE step 05 to retry on architectural-topology when R279-pattern is detected.

---

## 14. Honest deviation policy (for E31 execution)

Per the v12 task description:
- Real WebSearch in step 06 (mandatory; same as v5-v11).
- Real Agent spawn for step 08 (inverse-search) and step 12 (helper) WHERE FEASIBLE.
- Step 13 spec generation runs in MAIN CONTEXT (v10 default).
- Step 13.5 adversarial-spec attack runs in MAIN CONTEXT or Agent spawn (v11 default; ≤3 spawns).
- **Step 05.5 mechanical filter** runs in MAIN CONTEXT (v12 default; no Agent spawn needed because the classifier is deterministic from text).
- Per epoch, ≤5 synthesized Agent spawns across all steps. Excess uses main-context-direct labeling (NOT a fake Agent ID claim).
- Wall-clock timestamps ≥ 3-min logical gap per round (continued from E29-E30).
- R279 step 05.5 retrofit is epoch 31 round 0: a single retrospective application of step 05.5 to R279's existing 05_candidate.json, written into `rounds/round_279/05_5_pattern_filter.json`. R279's step 05.5 is in addition to the 25 new rounds R751-R775.

---

## 15. Phase 4 reporting requirements (for output/epoch31_comparison.md)

After E31 completes, the comparison document must record:
1. step 05.5 rejection rate (first attempt).
2. regeneration outcome distribution (first regeneration PASS / second regeneration PASS / 2 fails → policy_override).
3. final architectural-topology-candidate-rate.
4. downstream metric shifts: mean kw forced-hit (predicted UP), step 13 distinguishability distribution (predicted shift toward TRUE / fewer R279-pattern false), step 13.5 attack success rate (predicted DOWN if classifier works).
5. R279 retrofit-classifier outcome (predicted REJECTED_R279_PATTERN with Q1/Q2/Q3 = NO/NO/NO).
6. score_v12 with the 4 new terms.
7. verdict_shift_v11_to_v12 (rounds where v12 verdict differs from what v11 would have given).
8. cumulative N_verified after E31 = 871.
9. p(no PASS | 1% H₀) at N=871 = (0.99)^871 ≈ 0.000161.

The v12 channel's contribution is best seen at the step 05.5 level, not the final-verdict level (analogous to v11's step 13.5).
