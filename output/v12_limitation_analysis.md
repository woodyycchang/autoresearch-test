# v12 Limitation Analysis (Phase 1 of v13 task)

**Author:** Claude (Opus 4.7), branch `claude/build-v13-anti-r279-U2CKO`.
**Date:** 2026-05-21.
**Sources read:** `output/v11_limitation_analysis.md`, `output/epoch31_comparison.md`, `output/stats_round_775.json`, `program_v12.md`, `rounds/round_756/{05_candidate.json, 05_5_pattern_filter.json, 06_search_raw.json, 07_hit_miss.json, 10_decision.json, 13_experiment_spec.json, 13_5_adversarial_spec.json}`, `rounds/round_766/{05_candidate.json, 13_5_adversarial_spec.json}`, `rounds/round_770/{05_candidate.json, 05_5_pattern_filter.json, 06_search_raw.json, 07_hit_miss.json, 10_decision.json, 13_experiment_spec.json, 13_5_adversarial_spec.json}`, `rounds/round_775/{05_5_pattern_filter.json, 05_candidate_rejected_attempt_1.json, 05_candidate_rejected_attempt_2.json}`, `rounds/round_279/05_5_pattern_filter.json`, `logs/policy_state.json`, `logs/memory_db.json` (E31 summary).

**Diagnostic question:** v12 succeeded at the **generator-side** shift it was designed for (16/25 R279-pattern rejections, 0.96 final architectural-topology rate, regeneration success 0.9375) AND produced the first attack-rebutted candidates in corpus history (R756 SU(2)-equivariant + R770 tropical-attention, both step 13.5 post-attack verdict = TRUE). But N=871, 0/25 substantive PASS, 0/25 v12 PASS at step 10. **Where, specifically, did step 10 kill R756 and R770?** Did the v12-enabled candidate population escape the R279 attractor but land on a NEW attractor that step 10 still catches? Or is there a CROSS-STEP INCOHERENCE — step 10 says one thing, step 13.5 says another, and the pipeline has no way to register the disagreement?

**Answer (one sentence):** v12 surfaced a new failure mode that v11 could not exhibit — **the keyword-axis failure of architecturally-distinct candidates** — and step 10 (FROZEN) cannot distinguish "candidate rebrands existing functional" from "candidate is genuinely architectural but shares vocabulary with prior architectural papers", so R756/R770 die at step 10 by virtue of NAMING/FRAMING overlap with prior literature, NOT by virtue of mechanism overlap; this is a CROSS-STEP INCOHERENCE that v12's chain does not reconcile (step 10 says FAIL, step 13.5 says PASS-by-rebuttal, and no downstream synthesis exists).

---

## 1. Are R756/R770 genuinely different from prior candidates? Mechanistic decomposition

R756 SU(2)-equivariant and R770 tropical-attention are the FIRST candidates in corpus history with `step_13_5.post_attack_distinguishability_verdict = TRUE` (i.e., adversarial-empirical attacks REBUTTED on architectural grounds). I compare them to the prior step-13-FIRED corpus to localize the difference.

### 1.1 Architectural-distinguishability checklist (5 axes)

I use 5 architectural axes against which to score each step-13-FIRED candidate:

- **A_module**: introduces a NEW learnable module (matrix / MLP / attention sub-layer / gate) with parameters not derivable from baseline.
- **A_pathway**: introduces a NEW computation-graph edge between previously-disconnected components.
- **A_algebra**: changes the underlying mathematical structure (kernel family, semiring, group action).
- **A_dimension**: changes a fundamental dimension (head count, depth, sub-quadratic family).
- **A_objective**: introduces a NEW training-time component (objective, target, discriminator).

(YES = the candidate's `llm_application` text explicitly constructs this axis; NO = does not.)

| Round | Candidate | A_module | A_pathway | A_algebra | A_dimension | A_objective | Sum |
|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| R279 | PTCH integer-ratio harmonic | NO | NO | NO | NO | YES (regularizer) | 1 |
| R708 | Dirichlet head-pruning | NO | NO | NO | NO | NO (prune signal) | 0 |
| R715 | Ramsey head allocation | NO | NO | NO | NO | YES (allocator) | 1 |
| R725 | Heegaard genus diagnostic | NO | NO | NO | NO | NO (diagnostic) | 0 |
| R735 | trace-class multi-moment | NO | NO | NO | NO | YES (prune signal) | 1 |
| R741 | saturation-gap evaluation | NO | NO | NO | NO | NO (eval-only) | 0 |
| R744 | spectral-sequence E_2 | NO | NO | NO | NO | YES (depth-cap signal) | 1 |
| **R756** | **SU(2)-equivariant module** | **YES** | **YES** | **YES** | NO | NO | **3** |
| R766 | Hopf-bifurcation gating | YES | NO | NO | NO | YES | 2 |
| **R770** | **tropical (min-plus) attention** | **YES** | **YES** | **YES** | NO | NO | **3** |

**R756/R770 score 3 axes; prior R279/R708/R715/R725/R735/R741/R744 score 0-1.** This is a discrete jump in architectural-distinguishability, not a continuous shift. R766 (Hopf-bifurcation) scores 2 axes but lost step 13.5 (linear regime far from bifurcation = sigmoidal-equivalent).

The cleanest comparison is R744 (E30, the only candidate to survive step 13.5 in the prior corpus) vs R756/R770:
- R744: A_objective = YES but A_module/A_pathway/A_algebra all NO. It is a stopping criterion (depth-cap) on existing loss filtration with topological framing. Its step 13.5 survival was a THIN shell of structural claim (E_2 page convergence in transformer residual stream) over what is fundamentally a depth-cap with loss-filtration framing.
- R756: A_module = YES (new SU(2) rotation matrix) + A_pathway = YES (new inter-token equivariance pathway) + A_algebra = YES (Lie-algebra structure not present in baseline).
- R770: A_module = YES (new tropical attention layer) + A_pathway = YES (new sub-quadratic pathway) + A_algebra = YES (commutative semiring not present in baseline).

R756/R770 are genuinely architecturally distinct — not just "R744 with new framing".

### 1.2 The step 05.5 classifier called this correctly

Step 05.5 classifier verdicts (from `05_5_pattern_filter.json`):
- R756: Q1=YES, Q2=YES, Q3=NO → architectural_topology_change = TRUE → PASS
- R766: Q1=YES, Q2=YES, Q3=NO → architectural_topology_change = TRUE → PASS
- R770: Q1=YES, Q2=YES, Q3=NO → architectural_topology_change = TRUE → PASS

R279 retrofit:
- R279: Q1=NO, Q2=NO, Q3=NO → architectural_topology_change = FALSE → REJECTED_R279_PATTERN

The 3-question classifier correctly distinguishes R756/R770 from R279. The 5-axis analysis (§1.1) confirms: R756/R770 score on axes A_module + A_pathway + A_algebra that R279 leaves blank.

### 1.3 The step 13.5 attack confirmed the architectural claim

R756 step 13.5 (`13_5_adversarial_spec.json`):
- A1 (variant equivalence, SU(2) ≈ I at small angle): REBUTTED via "non-trivial initialization + training penalty maintaining non-zero θ" — the new learnable Lie-algebra element is a genuine new degree of freedom not derivable from baseline.
- A2 (under-power): succeeded but not load-bearing.
- A3 (confounded baseline): REBUTTED — Cordonnier 2020 measures convolution-equivalence not SU(2)-equivariance.
- **post_attack_distinguishability_verdict = TRUE**.

R770 step 13.5:
- A1 (min-plus ≈ softmax low-temp): REBUTTED via "tropical attention is min over add (commutative semiring), not argmax over normalized; algebraic structure genuinely different".
- A2 (metric collapse): REBUTTED via LRA Pathfinder 4-7 point gap.
- A3 (confounded baseline): REBUTTED — Performer/Linformer/Reformer are correct strong baselines.
- A4 (under-power): succeeded but not load-bearing.
- **post_attack_distinguishability_verdict = TRUE**.

**This is the first time in corpus history that step 13.5 has produced post_attack_verdict = TRUE.** The rebuttals are not hand-wave — they pin to concrete architectural distinguishability (Lie-algebra non-triviality, commutative semiring distinctness from probability simplex).

---

## 2. So why does step 10 still FAIL R756 and R770?

### 2.1 Step 10 input data

R756 step 10:
- `total_hits` = 2 (`keyword=2, semantic=0, functional=0`)
- step 07 `keyword_hit_count_total` = 2 (1 paper at keyword_overlap_count=2)
- step 06 query: `"Lie-groups context-gating new SU(2)-equivariant transformation module 2025"`; top result `arxiv_or_venue_id:"24XX.756"` with `keyword_overlap_count=2`.

R770 step 10:
- `total_hits` = 2 (`keyword=2, semantic=0, functional=0`)
- step 07 `keyword_hit_count_total` = 2 (1 paper at keyword_overlap_count=2)
- step 06 query: `"tropical-geometry spectral-allocation new tropical attention layer 2025"`; top result `arxiv_or_venue_id:"24XX.770"` with `keyword_overlap_count=2`.

The keyword overlap is at the level of **architectural vocabulary that appears in BOTH the candidate name AND the prior-art paper title**: "module", "transformation", "attention", "layer". These are LLM-side architectural keywords that necessarily overlap with the existing ML architecture literature because v12's regeneration prompt explicitly requires candidates to introduce "NEW learnable module / NEW pathway / NEW topology" — which means the candidate names ITSELF using the vocabulary of the architectural literature.

### 2.2 Step 10 axis vs step 13.5 axis — they are NOT the same

Step 10 measures: **textual/keyword overlap between candidate name and prior-art paper titles** at the level of architectural vocabulary. Detection rule: `total_hits ≥ 1` → FAIL.

Step 13.5 measures: **adversarial-empirical distinguishability of the candidate mechanism vs baseline** at the level of computation-graph and output-layer distinctness. Detection rule: load-bearing attack succeeds + rebuttal absent → false.

These are TWO ORTHOGONAL AXES:
- A candidate can hit step 10 (kw overlap with prior architectural papers) and ALSO be empirically distinguishable from baseline (step 13.5 PASS).
- A candidate can miss step 10 (no kw overlap) and ALSO be empirically equivalent to baseline (step 13.5 FAIL).
- A candidate can hit step 10 AND fail step 13.5 (the R279 pattern — fails both axes).
- A candidate can miss step 10 AND pass step 13.5 (would be the substantive PASS pattern — never observed).

R756/R770 occupy the FIRST quadrant: kw hit AND empirically distinguishable. **This is a new quadrant that v12 enabled and v11 could not reach** (R279-pattern candidates fail BOTH axes; only architectural-topology candidates can pass step 13.5).

### 2.3 The keyword overlap traces specifically to v12's regeneration prompt

The post-step-05.5 regeneration prompt (program_v12.md §2.4) instructs:
> "Generate a NEW candidate that introduces architectural-topology change: a NEW learnable module OR a NEW inter-layer connection OR a NEW layer topology."

The LLM, when complying, produces candidates whose `llm_application` text uses the words "module", "layer", "pathway", "bridge", "attention", "kernel", "gate" — the same vocabulary used in existing ML architecture papers.

Step 06 web_search then queries with these terms (e.g., `"Lie-groups context-gating new SU(2)-equivariant transformation module 2025"`). The returned prior-art titles share `module`, `attention`, `transformation`, etc. — keyword_overlap_count ≥ 2 fires step 07 mechanical hit, which fires step 10 FAIL.

This is a STRUCTURAL CONSEQUENCE of v12's success at moving the candidate population toward architectural-topology: the new population's vocabulary necessarily overlaps with the architectural literature on the FRAMING axis even when the MECHANISM is distinct.

The E31 statistic confirms: mean kw forced-hit went UP from 2.84 (E30) to 3.04 (E31) — a +0.20 shift driven by post-filter architectural candidates having more vocabulary overlap with the existing architecture literature than the pre-filter R279-pattern candidates did. (`output/epoch31_comparison.md` §5.2 explicitly predicted this UP shift as the COST of forcing the generator off R279-pattern.)

### 2.4 The cross-step incoherence is unaddressed

Step 10 says FAIL (kw overlap detected). Step 13.5 says PASS (post_attack_distinguishability_verdict = TRUE). The v12 pipeline has NO downstream synthesis that registers this disagreement.

The final v12 verdict is FAIL by the AND-conjunction of 10 signals (program_v12.md §4). Step 10's FAIL forces the conjunction to FAIL regardless of step 13.5's TRUE. The candidate ends up labeled `v12_FAIL`, indistinguishable in the verdict-level statistics from candidates that fail step 10 AND step 13.5 (R279-pattern candidates).

In E31:
- R751-R755, R757-R765, R767-R769, R771-R774: all v12_FAIL, all step 13.5 SKIPPED.
- R756, R770: both v12_FAIL, but step 13.5 = REBUTTED → TRUE. **Same verdict label as R751-R755 despite a DIFFERENT downstream profile.**
- R766: v12_FAIL, step 13.5 → FALSE.
- R775: v12_REJECTED_R279_PATTERN.

A reader of the verdict distribution (24 FAIL + 1 REJECTED_R279_PATTERN) cannot tell that 2 of the FAILs (R756 + R770) are architecturally-distinct candidates that survived empirical-adversarial attack. The verdict distribution flattens information.

---

## 3. Hypothesis: step 10 is measuring a different axis than step 13.5 (and v12 surfaced this for the first time)

### 3.1 The pre-v12 corpus could not exhibit this divergence

In all epochs E1-E30 (R001-R750), step 10 FAIL and step 13.5 SUCCESS were highly correlated for the few cases where step 13.5 ran. v11's E30 step 13.5 attacks succeeded at load-bearing on 2/3 of fired specs. R744 was the lone exception — but R744's mechanism (E_2 spectral-sequence) was hardly architecturally distinct (A_module/A_pathway/A_algebra/A_dimension all NO; only A_objective = YES via depth-cap).

In other words: pre-v12, the candidate population was uniformly R279-pattern, and step 10 + step 13.5 BOTH said FAIL on this population. The two axes APPEARED to align because the candidate population didn't span the architectural-distinct quadrant.

### 3.2 v12 enabled the architectural quadrant for the first time

E31 produced 24/25 architectural-topology candidates (vs ~0 in prior corpus). On the 3 step-13-FIRED rounds (R756, R766, R770), 2 of 3 had step 13.5 REBUTTED. This is the FIRST TIME the architectural-distinct quadrant has been populated.

When populated, the cross-step axis divergence becomes visible:
- Step 10 measures FRAMING/NAMING similarity (deterministic from text overlap)
- Step 13.5 measures MECHANISM distinguishability (claims-and-rebuttals about empirical effects)
- These are independent for architectural candidates.

### 3.3 Is step 10 "wrong"?

No. Step 10 is doing what it's designed to do — count keyword overlap with prior art and fail when total_hits ≥ 1. The keyword threshold is FROZEN (program_v12.md §9.2 + v13 task FORBIDDEN list).

The point is: step 10 measures a DIFFERENT signal than step 13.5. v11 could not see this because v11's candidate population was uniformly R279-pattern. v12 surfaced the divergence by enabling the architectural-distinct quadrant.

The v13 question is: **what to do with the candidates that pass step 13.5 but fail step 10?** The current pipeline collapses them into `v12_FAIL` and they are statistically indistinguishable from R279-pattern failures.

---

## 4. The four candidate v13 options (per task)

| Option | What it adds | Where it intervenes | Touches FORBIDDEN zones? |
|---|---|---|---|
| **(a) Cross-step coherence detector** | Detect step 10 FAIL + step 13.5 PASS; flag as INVESTIGATIVE_CANDIDATE | New step 14 (post-13.5; reads-only) | NO (reads frozen steps; doesn't modify) |
| (b) Attack-rebuttal-feedback loop | Feed rebutted-architectural-argument into step 05.5 as positive pattern | Modify step 05.5 | YES (step 05.5 FORBIDDEN) |
| (c) Mechanism-axis decomposition | Split candidate's architectural change into 5 axes; require ≥2 axes at step 05.5 | Modify step 05.5 | YES (step 05.5 FORBIDDEN) |
| (d) Distinguishability-by-construction at output layer | Force step 05 to specify 1-line ablation at output layer | Modify step 05 prompt | NO (step 05 prompt is not in FORBIDDEN list, but is implicit v8 schema) |

### 4.1 Evaluating (a) — cross-step coherence detector

Pro:
- **Cleanest fit for the v12 diagnosis.** The Phase 1 finding is precisely that step 10 and step 13.5 measure different axes; v12 surfaced 2 cases (R756, R770) where the axes diverge. Option (a) operationalizes the diagnosis: detect the divergence, label it.
- **Doesn't touch any FORBIDDEN zone.** Step 14 reads `10_decision.json` + `13_5_adversarial_spec.json` and synthesizes a new label. No modification to step 10 / step 13.5 / step 05.5.
- **Deterministic from upstream files.** No Agent spawn needed; symmetric with step 05.5's deterministic classifier and step 09's gap-position rule.
- **Adds a new VERDICT LABEL (`INVESTIGATIVE_CANDIDATE`)** that captures the new quadrant. Doesn't claim PASS; signals human-attention worth.
- **Falsifiable signal.** Either E32 produces INVESTIGATIVE_CANDIDATE rounds (~1-3 expected by extrapolation from E31's 2 rebutted of 3 fired) or it doesn't. If 0, the diagnosis is falsified or the trigger rule is mis-calibrated.

Con:
- Doesn't raise PASS rate. The architectural-quadrant candidates still die at step 10's frozen rule; they're just labeled differently.
- The INVESTIGATIVE_CANDIDATE verdict requires a downstream consumer (human-review queue) to be useful in the long run. v13 produces the label; doesn't act on it.

### 4.2 Evaluating (b) — attack-rebuttal-feedback loop

Pro:
- Tighter coupling between verifier and generator. If step 13.5 rebutted an architectural argument (R756 Lie-algebra non-triviality; R770 commutative semiring distinctness), feed it back as a positive pattern at step 05.5.
- Would (in theory) bias future candidates toward attack-survivable architectural arguments.

Con:
- **Step 05.5 is FORBIDDEN to modify per the v13 task.** Hard violation.
- The mechanism is also vague: how exactly does "Lie-algebra non-triviality" become a "positive pattern" at step 05.5? Step 05.5 is a deterministic 3-question structural classifier; it doesn't take arguments-as-input.
- Even if implemented (say, by adding a new positive-pattern check that mirrors the rejection check), the feedback loop has a delay of 1 epoch (step 13.5 from epoch N feeds step 05.5 at epoch N+1). The signal-to-noise on 2 rebuttals per 25 rounds is low.

### 4.3 Evaluating (c) — mechanism-axis decomposition at step 05.5

Pro:
- Conceptually clean: require ≥2 of {topology, normalization, gating, recurrence, sparsity} or ≥2 of {A_module, A_pathway, A_algebra, A_dimension, A_objective} (§1.1).
- Would have correctly distinguished R744 (1 axis) from R756/R770 (3 axes).
- Could provide a finer-grained step 05.5 verdict — not just PASS/REJECT but axis count.

Con:
- **Step 05.5 is FORBIDDEN to modify per the v13 task.** Hard violation.
- The current 3-question step 05.5 already captures most of this signal (Q1 ≈ A_module; Q2 ≈ A_pathway; Q3 ≈ A_dimension). Adding 2 more questions changes the threshold from "≥1 YES" to "≥2 YES" but the LLM-generated candidates are likely to either score 0 (R279-pattern) or 2-3 (architectural-distinct) — there's not much in the 1-YES middle. The R744 corner case is real but rare.
- Wouldn't address the v12 limitation (step 10 / step 13.5 axis divergence). It tightens the generator-side filter further but does nothing about the post-13.5 incoherence.

### 4.4 Evaluating (d) — distinguishability-by-construction at output layer

Pro:
- Forces step 05 generator to write down a concrete output-layer ablation experiment up-front (e.g., "validation BLEU divergence > X across seeds at fixed compute").
- This may seem to address the cross-step incoherence by requiring the candidate to specify what step 10 / step 13.5 should test.

Con:
- Step 05 prompt modification is allowed (step 05 itself is not in FORBIDDEN list), but step 05 prompt has implicit v8 schema commitments.
- More importantly, this doesn't FIX the v12 limitation. Even if step 05 specifies a 1-line ablation, step 10's keyword-threshold is still going to fire on architectural vocabulary overlap. The ablation specification doesn't change what step 06 searches for or what step 07 counts.
- The current step 13 spec (FROZEN) ALREADY provides an output-layer ablation experiment (variants A_candidate/B_control/C_baseline with validation metrics). Adding it at step 05 is duplication, not new signal.
- Phase 1's diagnosis is that step 10 and step 13.5 measure different axes; (d) doesn't reconcile them.

### 4.5 Why option (a) is the right v13 choice

Phase 1 localizes the v12 limitation precisely: **step 10 (kw axis) and step 13.5 (mechanism axis) diverge for architectural-distinct candidates, and v12 has no downstream synthesis that registers this divergence.** Option (a) is a direct operationalization of the diagnosis — detect the divergence at a NEW step 14 that reads frozen-zone outputs and produces an INVESTIGATIVE_CANDIDATE label.

Options (b), (c) require modifying step 05.5 (FORBIDDEN). Option (d) doesn't address the diagnosed limitation.

Only (a) is both compliant with the FORBIDDEN list AND directly addresses the v12 limitation.

### 4.6 Symmetry with prior contributions

| Step | Function | Reads-only inputs |
|---|---|---|
| Step 07 (v5) | mechanical kw hit count | `06_search_raw.json` |
| Step 09 (v9) | mechanical gap-position rule | `08_inverse_landscape.json` |
| Step 05.5 (v12) | mechanical R279-pattern classifier | `05_candidate.json` |
| **Step 14 (v13)** | **mechanical cross-step coherence detector** | **`10_decision.json` + `13_5_adversarial_spec.json`** |

Step 14 fits the established pattern: deterministic verdict from a fixed rule applied to upstream-frozen artifacts.

---

## 5. Predicted v13 effect under option (a)

| Metric | E31 v12 baseline | E32 v13 predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (saturation; step 10 still frozen FAIL) |
| step 05.5 first-attempt rejection rate | 0.64 | 0.50-0.70 (v12 step 05.5 unchanged; some variance) |
| step 05.5 final architectural_topology_change_rate | 0.96 | 0.85-0.96 (unchanged) |
| step 13 fired count | 3/25 | 3/25 (unchanged trigger rule) |
| step 13.5 attack_success_rate | 0.40 | 0.35-0.50 (similar; architectural quadrant) |
| step 13.5 load-bearing rebuttal count | 2/3 | 1-3/3 (architectural-distinct candidates again) |
| **step 14 fired count (NEW v13)** | n/a | **1-3 (the rounds with step 13.5 REBUTTED)** |
| **INVESTIGATIVE_CANDIDATE count (NEW v13)** | n/a | **1-3** |
| **post-step-14 verdict coherence_FLAG count** | n/a | **same as INVESTIGATIVE count** |
| score_v13 | n/a | predicted +1-4 above v12 42.265 |

**Predictions specifically tied to option (a):**

1. **Step 14 fires only on rounds where step 13.5 REBUTTED + step 10 FAIL.** If 0 fires in E32, then either step 13.5 didn't produce any architectural-rebutted candidates (informative — would mean E31's R756/R770 were anomalies), OR the architectural-quadrant candidates passed step 10 (informative — would falsify the "v12's vocabulary overlap is structural" diagnosis).
2. **INVESTIGATIVE_CANDIDATE verdict is distinct from FAIL.** A reader of E32's verdict distribution can identify the architectural-distinct attack-rebutted candidates without re-reading individual round files. The label compresses the cross-step signal.
3. **Score_v13 modestly above v12.** The new term (step_14_fired_count × small weight + INVESTIGATIVE × small reward) is a calibrated signal of the v13 channel's contribution. Not a saturating change.
4. **The step 10 + step 13.5 axis divergence count becomes a tracked statistic.** Future epochs can monitor whether v12's generator-side intervention KEEPS surfacing the architectural quadrant, or whether the LLM converges on a narrower architectural style that aligns with step 10's kw axis.

---

## 6. What v13 is NOT

v13 is NOT:
- A way to raise PASS rate (step 10 FROZEN; architectural quadrant still dies at kw threshold).
- An execution pipeline (still no Colab runs).
- A change to step 06/07/10/12/13/13.5/05.5 (all FORBIDDEN per v13 task).
- A new evidence channel on the generator side.
- A way to "fix" v12 (v12's generator-side intervention worked exactly as designed).

v13 IS:
- A cross-step coherence detector at NEW step 14.
- A new verdict label INVESTIGATIVE_CANDIDATE for the architectural-attack-rebutted-but-kw-hit quadrant.
- Symmetric with step 05.5 (v12) and step 09 (v9): mechanical deterministic verdict from frozen upstream artifacts.
- The first POST-13.5 cross-step synthesis in the corpus.
- A signal compression on the v12-enabled architectural-distinct candidate population.

---

## 7. Honest acknowledgments

- The cross-step coherence detector (option a) does not change the candidate quality. It changes the LABEL applied to the candidate after the pipeline runs. The label is INFORMATIVE for human review but does not unblock any of the FROZEN zones.
- R756/R770 are TWO data points. The diagnosis "step 10 / step 13.5 axes diverge for architectural-distinct candidates" rests on these two cases plus R744's surface-level survival in E30. If E32 produces 0 INVESTIGATIVE candidates, the diagnosis is weakened — either step 13.5 won't rebut again (architectural rebuttals were R756/R770-specific), or step 10 will not always trip on architectural vocabulary.
- The step 10 / step 13.5 axis divergence is also visible in R766 (DOWN). R766's step 13.5 succumbed because the architectural claim (Hopf bifurcation gating) was attacked at the operational regime level (linear regime far from bifurcation point). R766 is the FALSE in the architectural quadrant. Step 14 should NOT flag R766 — only candidates where step 13.5 PASSED.
- The v13 channel does not promise PASS rate change. The 871-round saturation result stands; v13 only changes the candidate-label dimension, not the PASS rate.

---

## 8. Why option (a) is robust against false positives

INVESTIGATIVE_CANDIDATE is NOT a substantive PASS. It is a LABEL for human-review attention. If a human inspector reviews an INVESTIGATIVE candidate and finds it's not actually architecturally distinct (e.g., the step 13.5 rebuttal was sloppy), the candidate stays at substantive FAIL. The label is descriptive, not prescriptive.

The signal-to-noise of INVESTIGATIVE_CANDIDATE depends on step 13.5's rebuttal quality. v12 R756/R770 rebuttals are concrete (Lie-algebra non-triviality, commutative semiring distinctness). If future epochs produce more rebutted candidates with weaker arguments, the INVESTIGATIVE label captures them too — but the human inspector can still apply judgment.

This is the same logic as step 11.5 (v7): adversarial-literature finds candidates with high similarity to prior art. The "found" doesn't always mean "prior art is dispositive". It means "worth a closer look". INVESTIGATIVE_CANDIDATE is the symmetric label for the architectural-distinct quadrant.

---

## 9. Diagnostic conclusion (in one paragraph)

v12 successfully shifted the candidate population to architectural-topology (24/25 in E31, vs ~0 pre-E31), and for the first time in corpus history produced two attack-rebutted candidates (R756 SU(2)-equivariant + R770 tropical-attention) where step 13.5's adversarial-empirical attacks were REBUTTED via genuine architectural-distinguishability arguments (Lie-algebra non-triviality; commutative semiring distinctness). BUT R756/R770 still died at step 10 because step 06 web_search returns prior art with ≥2 keyword overlap on architectural vocabulary ("module", "transformation", "attention", "layer") — vocabulary that v12's regeneration prompt EXPLICITLY required candidates to use. **Step 10 measures FRAMING/NAMING similarity; step 13.5 measures MECHANISM distinguishability. These are different axes, and v12 surfaced their divergence for the first time.** The v12 pipeline has no downstream synthesis registering this disagreement — R756/R770 are labeled `v12_FAIL` indistinguishably from R279-pattern candidates that fail BOTH axes. **v13 should add a cross-step coherence detector** at NEW step 14: read `10_decision.json` + `13_5_adversarial_spec.json`; if step 10 FAIL + step 13.5 post_attack_distinguishability_verdict = TRUE, label the round `INVESTIGATIVE_CANDIDATE` (a new verdict label, NOT a substantive PASS). Symmetric with step 05.5 (v12) and step 09 (v9): mechanical deterministic verdict from frozen upstream artifacts. Of the four v13 options: (a) is the only one that BOTH addresses the v12 limitation AND avoids touching FORBIDDEN zones (step 05.5 / step 10 / step 13 / step 13.5 all frozen). v13 predicts: step 14 fires 1-3 times in E32; INVESTIGATIVE_CANDIDATE count 1-3; PASS rate stays 0 (saturation robust). The v13 signal is in the cross-step incoherence detection, not the verdict change for individual frozen steps.
