# v11 Limitation Analysis (Phase 1 of v12 task)

**Author:** Claude (Opus 4.7), branch `claude/build-v12-adversarial-6U2QQ`.
**Date:** 2026-05-20.
**Sources read:** `output/v10_limitation_analysis.md`, `output/epoch30_comparison.md`, `output/stats_round_750.json`, `program_v11.md`, `rounds/round_279/05_candidate.json`, `rounds/round_279/13_5_adversarial_spec.json`, `rounds/round_708/05_candidate.json`, `rounds/round_735/05_candidate.json`, `rounds/round_735/13_experiment_spec.json`, `rounds/round_741/05_candidate.json`, `rounds/round_741/13_5_adversarial_spec.json`, `rounds/round_744/05_candidate.json`, `logs/policy_state.json`, `logs/memory_db.json` (E30 summary).

**Diagnostic question:** v11's step 13.5 confirms the empirical attack works — 4/4 succeeded on R279, 2/3 load-bearing on E30 fired specs. So why does the pipeline still produce 0 substantive PASS at N=846? Where is the actual constraint?

**Answer (one sentence):** The constraint is **the candidate generator (step 05), not the verifier chain.** v11's verifier chain can reliably KILL R279-pattern candidates but step 05 keeps GENERATING them — every step-13-FIRED candidate in the corpus (R279, R708, R715, R725, R735, R741, R744) is a variant of the same R279-pattern (a fixed scalar/diagonal/functional prior on an existing learnable parameter), and the pipeline has no mechanism to generate distinguishable-by-construction candidates.

---

## 1. Restating v11's demonstrated capability

`output/epoch30_comparison.md` summary:

| Verifier capability | v11 evidence |
|---|---|
| Adversarial-empirical attack on step 13 spec | Step 13.5 fired 3/3 on E30 top-3 (R735, R741, R744) |
| Attack success rate at load-bearing level | 2/3 = 0.667 on E30; 4/4 on R279 retrofit |
| Discriminates (not rubber-stamp) | R744 load-bearing attack rebutted via E_2 ≠ E_1 page-differential argument |
| Convergence with v7 step 11.5 on R279 | Yes — all three channels (v7 lit / v10 struct / v11 adv) agree R279 = PARAMETRIZATION-ONLY |
| One-way ratchet (no spurious flip from false → uncertain) | Yes — R279 false stayed false despite 4 succeeded attacks |

**v11 verifier capability is real.** The verifier chain can reliably detect and downgrade R279-pattern candidates.

---

## 2. The asymmetry v11 leaves intact

`output/v10_limitation_analysis.md` §5 stated the asymmetry plainly:

> **The pipeline can KILL bad candidates but cannot GENERATE good ones.**

v11 strengthened the KILL side (added adversarial-empirical channel). v11 did NOT touch the GENERATE side. Step 05 (candidate generation via token streams) is the v8 contribution and has been UNCHANGED since R651.

The result: every epoch since R651, step 05 produces candidates of similar quality. The verifier chain reliably rejects them. The PASS rate stays at 0.

---

## 3. Is step 05 the actual bottleneck? Empirical test via R279-pattern accounting

I went through every step-13-FIRED candidate in the corpus and decomposed its mechanism into either (a) R279-PATTERN = "fixed scalar/diagonal/functional prior on an EXISTING learnable parameter" or (b) STRUCTURAL-TOPOLOGY-CHANGE = "introduces a new architectural component, connection, or topology that does not reduce to a prior on an existing learnable parameter".

### 3.1 R279-pattern catalog

| Round | Candidate | Existing learnable param | Imposed prior/functional | R279-pattern? |
|---|---|---|---|:---:|
| R279 | PTCH (integer-ratio harmonic) | per-head SVD singular values | integer-ratio fixed target spectrum | **YES** |
| R708 | Dirichlet-series pruning | per-head attention-importance scalars | Dirichlet-series analytic-continuation evaluated at s=0/s=1 | **YES** |
| R715 | Ramsey-K_3 head allocation | head-pair adjacency graph | Ramsey K_3 guarantee for head-assignment edges | **YES** (constraint on existing head-adjacency) |
| R725 | Heegaard-genus diagnostic | embedding manifold (existing latent) | Heegaard genus (topological invariant) computed on it | **YES** (read-only diagnostic on existing latent) |
| R735 | Trace-class multi-moment prune | per-head attention matrix singular values | nuclear-norm + 2nd/3rd cumulant joint quantile rank | **YES** (multi-moment functional on existing SVD) |
| R741 | Saturation-gap evaluation | model output answer-type set (existing) | Set-cardinality functional with model-theoretic framing | **YES** (read-only functional on existing outputs) |
| R744 | Spectral-sequence E_2 depth controller | layer-depth loss filtration (existing) | E_2-page-convergence stopping criterion | **YES** (read-only convergence test on existing loss) |

**7/7 step-13-FIRED candidates in corpus = R279-pattern.** No step-13-fired candidate has ever introduced architectural-topology change.

### 3.2 What R279-pattern looks like operationally

Operational definition:
- The candidate's `llm_application` (per `05_candidate.json`) describes a NEW way to *interpret* / *rank* / *prune* / *regularize* / *measure* a value that the BASELINE model already computes.
- The "novel" mechanism is the *imposed prior or functional*, not a structural change to the network.
- Removing the imposed prior reduces the candidate to the baseline architecture, unchanged.
- The candidate cannot be implemented without the baseline model's existing learnable parameters as substrate.

Examples passing this test (all in the corpus): R279/R708/R715/R725/R735/R741/R744.

Examples FAILING this test (none in corpus step-13-FIRED set, hypothetical): a candidate that adds a NEW layer with a new functional form, a candidate that introduces a NEW communication channel between heads via a new learnable matrix, a candidate that changes the attention sub-quadratic schedule to a fundamentally different sub-quadratic family (e.g., kernel-method via random Fourier features rather than softmax).

### 3.3 Why R279-pattern is the local minimum for step 05

Step 05's token-stream generator (v8) decomposes candidates into M_1...M_K sub-mechanisms. The path of least resistance for a 4-sub-mechanism candidate is:
- M_1: identify which existing learnable parameter to target (singular values, attention scores, head-importance scalars, etc.).
- M_2: compute a NEW functional on M_1 (a sum, a topological invariant, a moment, a complex-analytic continuation, etc.).
- M_3: derive a ranking / threshold / stopping criterion from M_2.
- M_4: act on the model (prune / regularize / cap-depth / score).

This recipe ALWAYS yields R279-pattern. Step 05 has no incentive to step outside it because:
1. Source-domain vocabulary (the v8 stripping target) is naturally a functional-form choice; structural changes don't come dressed in a single source-domain vocabulary.
2. Sub-mechanism decomposition rewards arithmetic over composition — a 4-step decomposition is harder to write for architectural topology changes (a NEW layer is a single sub-mechanism, hard to decompose into 4 named M_i without padding).
3. The downstream verifier chain (step 06 web_search, step 07 keyword threshold, step 12 tree-stream) is anchored to functional/keyword similarity — structural changes have higher prior risk of getting hit by step 10 because they often share architectural keywords with major published work.

So step 05 has converged on R279-pattern as a NASH equilibrium: it's the easiest candidate form to write, easiest to decompose into 4 sub-mechanisms, and lowest-risk in early-pipeline verification — but also the easiest for v7-step-11.5 / v10-step-13 / v11-step-13.5 to demolish at the empirical-distinguishability check.

---

## 4. The v11 attack confirms the pattern

v11 step 13.5 attack success on R279-pattern candidates is HIGH (0.667 load-bearing in E30 + 4/4 on R279 retrofit = combined 3/4 ≈ 0.75). The high attack success rate is not because the attacker is too aggressive — R744 survived attack via legitimate rebuttal (E_2 page ≠ E_1 page in transformers). The pattern is consistent: most R279-pattern candidates HAVE a load-bearing weakness because the imposed prior reduces to something the baseline already does.

This is the diagnostic value of step 13.5 — it documents that R279-pattern candidates have a load-bearing weakness 2/3 of the time. It does NOT cause step 05 to generate non-R279-pattern candidates.

R744's survival is the proof of the principle: R744 happens to claim something structurally distinguishable (E_2 cross-page differentials genuinely differ from E_1 single-page convergence in transformers with residual streams) — and the attack failed at load-bearing level. R744 is the ONE example of a step-13-fired candidate that approaches structural-topology-change rather than parametric-prior. (Even R744 is still mostly R279-pattern; the E_2 page argument is a thin shell of structural claim over what is fundamentally a stopping criterion on existing loss.)

If step 05 were generating more R744-style (legitimately structural) candidates, step 13.5's attack would have a LOWER success rate but the candidates would have higher PASS rate. v11 cannot test this hypothesis because step 05 hasn't changed.

---

## 5. Why this is not v10/v11's "fault"

v10 added the empirical-reward channel (step 13). v11 added the adversarial-empirical channel (step 13.5). Both are valid extensions of the verifier chain. Neither was asked to modify step 05.

The chain of upgrades has been verifier-side for 5 epochs:
- v7: adversarial-literature (step 11.5)
- v8: token streams / Q-rubric / tree-stream (step 05, 11, 12 — but step 05 is OUTPUT structuring, not generator change)
- v9: inverse-search / gap-position (step 08, 09)
- v10: empirical-reward spec (step 13) + policy_state (logs/)
- v11: adversarial-empirical attack (step 13.5)

Every upgrade has been on the verifier side except v8's step 05 — and even v8's step 05 was a structuring upgrade (decomposing candidates into token streams), NOT a generation-quality upgrade. The underlying generator has been the same LLM-context-direct candidate prompt since v3.

**v12 needs a generator-side intervention.** That is the missing degree of freedom.

---

## 6. The four candidate v12 options

| Option | Where it intervenes | Cost | Addresses R279-pattern? | Pre-search vs post-search |
|---|---|---|---|---|
| (a) Distinguishability-conditioned generation | step 05 (output-side check) | medium (extra step per candidate) | partially — candidate must specify distinguishability claim | pre-search (rejects before step 06) |
| **(b) Anti-R279 candidate filter** | step 05.5 (new mechanical filter) | low (deterministic structural classifier) | **directly — flags R279-pattern as forbidden** | **pre-search (rejects before step 06)** |
| (c) Adversarial candidate generator | step 05 (parallel generator) | medium (extra Agent spawn per candidate) | indirectly — failure-mode reasoning may surface R279-pattern | pre-search (rejects before step 06) |
| (d) Empirical-result-conditioned generation | step 05 (LLM prompt augmentation) | low (text-only prompt edit) | indirectly — relies on LLM internalizing prior attack results | pre-search (bias not filter) |

### 6.1 Evaluating (a)

Pro: requires the candidate to write down a distinguishability claim BEFORE step 06 search. Forces the generator to think about distinguishability.
Con: the distinguishability claim is still LLM inference (same problem as step 13's pre_check). The claim can be vacuous ("A and B differ in M_2") without surfacing R279-pattern. Doesn't address the structural cause — R279-pattern is BUILT INTO the 4-sub-mechanism decomposition path.

### 6.2 Evaluating (b)

Pro: **Mechanical and deterministic.** A candidate is R279-pattern if its `llm_application` modifies/regularizes/ranks/measures an existing learnable parameter without introducing new architectural topology. This is checkable from `05_candidate.json` alone (no Agent spawn needed). Symmetric with step 07 keyword threshold (mechanical structural check). Pre-search rejection saves budget on R279-pattern candidates.
Con: requires defining the structural classifier precisely. May reject legitimate candidates that happen to look R279-pattern (false positive risk). Force generator to retry with architectural-topology candidate.

### 6.3 Evaluating (c)

Pro: spawning an adversarial-candidate-generator parallel to the main generator could surface R279-pattern early (the adversarial agent knows R279 is the saturated pattern). 
Con: medium cost (extra Agent spawn). The adversarial agent has no special insight into structural topology — it's another LLM context that may also produce R279-pattern candidates. Symmetric with step 13.5 but addresses a different stage.

### 6.4 Evaluating (d)

Pro: lowest cost. Just augments the step 05 prompt with E27-E30 attack results.
Con: this is what `logs/policy_state.json` was supposed to do (v10). The policy_state already documents R279-pattern as over-mined (across all domains, all forms). E30's drift_score=0.8 was driven by pivoting to NEW domains, NOT by departing from R279-pattern. The LLM apparently parses "over-mined sub-pattern" as a DOMAIN signal rather than a STRUCTURAL signal. Adding more attack data won't fix this misalignment.

### 6.5 Why option (b) is the right v12 choice

The Phase 1 diagnosis localizes the bottleneck at step 05's structural recipe (R279-pattern is the easiest 4-sub-mechanism path). v10's policy_state and v11's adversarial channel have not changed step 05's recipe. The cleanest intervention is a MECHANICAL FILTER at step 05.5 that fires BEFORE step 06 and rejects R279-pattern candidates outright, forcing the generator to try architectural-topology candidates.

This is symmetric with step 07's keyword threshold (mechanical structural check, deterministic from upstream file). It is also symmetric with v9's gap-position check (deterministic rule on the artifact). And it operates pre-search, saving steps 06-13 budget on R279-pattern candidates that would have been killed downstream anyway.

Option (b) is also the ONLY option that touches step 05's recipe. (a) adds a check on step 05 output; (c) parallels step 05; (d) augments step 05's prompt. None of them FORCE the generator away from R279-pattern. Only (b) does (by deterministic rejection that triggers regeneration with explicit anti-R279 instruction).

---

## 7. Predicted v12 effect under option (b)

| Metric | v11 E30 baseline | v12 E31 predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (saturation likely persists — anti-R279 filter doesn't guarantee PASS) |
| step 05.5 R279-pattern rejection count | n/a | predicted 5-15/25 (generator retry on rejected R279-pattern) |
| step 05.5 architectural-topology-change candidate count | n/a | predicted 10-20/25 (post-filter passes) |
| step 13 fired count | 3/25 | predicted 0-3/25 (architectural candidates may be killed earlier; or may pass step 10 less often due to wider keyword surface) |
| step 13.5 attack_success_rate | 0.667 load-bearing | predicted to DROP if candidates are genuinely architectural (R744-style) — say 0.2-0.4 |
| post_attack uncertain → false flip rate | 0.667 | predicted to DROP for same reason |
| **diagnostic shift** | n/a | the v12 channel signal is in step 05.5 rejection rate × downstream attack-success rate change |
| score_v12 | n/a | predicted +0-3 above 35.91 |

**Predictions specifically tied to (b):**
1. step 05.5 fires R279-pattern rejection at non-zero rate. (If 0, then either step 05 already escaped R279-pattern on its own — falsifies the diagnosis — or the filter rule is too narrow.)
2. step 13.5 attack success rate DROPS on post-filter candidates. (If it stays at 0.667, then either the filter is rejecting candidates that aren't actually R279-pattern, or the architectural-topology candidates have a DIFFERENT load-bearing weakness — informative either way.)
3. Mean kw forced-hit goes UP. (Architectural-topology candidates share keywords with major architectural papers; step 10 will more reliably FAIL them via keyword overlap.) This is the COST of forcing the generator off R279-pattern.

---

## 8. What v12 is NOT

v12 is NOT:
- A way to raise PASS rate (corpus saturation at N=846 is empirically robust; v12 only changes the candidate-quality dimension, not the PASS rate).
- An execution pipeline (still no Colab runs).
- A change to step 06/07/10/12/13/13.5 (all FORBIDDEN per task).
- A new evidence channel on the verifier side.

v12 IS:
- A generator-side intervention at step 05.5.
- A mechanical structural classifier that rejects R279-pattern candidates BEFORE step 06.
- Symmetric with step 07's keyword threshold (deterministic structural check).
- Pre-search rejection saving downstream budget on R279-pattern.

---

## 9. Honest acknowledgments

- The R279-pattern definition (§3.2) is a STRUCTURAL classifier that requires a judgment about what counts as "existing learnable parameter" vs "new architectural component". For v12, I'll make this classifier as deterministic as possible by referencing the candidate's `llm_application` field and a 3-question checklist (does it add a NEW learnable module? does it add a NEW connection? does it change the layer topology?). If all three are NO, the candidate is R279-pattern. This is the operationalization in §3.2 made concrete.
- The Phase 1 diagnosis (step 05 is the bottleneck) is testable. v12's anti-R279 filter is the cheapest test. If E31 shows ≥5 R279-pattern rejections and downstream behavior shifts, the diagnosis is confirmed. If the filter rejects 0 (step 05 escapes R279-pattern unprompted) or rejects all 25 (filter is too aggressive), the diagnosis is falsified or the filter is mis-calibrated.
- The R744-survives-attack result is the strongest single piece of evidence for the diagnosis: when a candidate happens to be structurally-distinguishable, step 13.5's attack fails. v12 should generate MORE R744-style candidates and FEWER R279-style.
- v12 does NOT promise PASS rate increase. Likely E31 will still be 0/25 PASS. v12's contribution is shifting the candidate population away from R279-pattern, measured at step 05.5.

---

## 10. Diagnostic conclusion (in one paragraph)

v11 demonstrated the adversarial-empirical attack works: 4/4 on R279 retrofit, 2/3 load-bearing on E30 fired specs, 1/3 spec survived attack via legitimate rebuttal (R744). But v11 left step 05 (candidate generation) UNCHANGED — and every step-13-fired candidate in the corpus (R279, R708, R715, R725, R735, R741, R744) is an R279-pattern variant (fixed scalar/diagonal/functional prior on an existing learnable parameter). The verifier chain can KILL R279-pattern candidates; it cannot make step 05 GENERATE non-R279-pattern candidates. **Step 05 is the actual bottleneck.** v12 should add a generator-side intervention. Of the four options, option (b) — Anti-R279 candidate filter at step 05.5 — is the right pick: mechanical, deterministic, pre-search, symmetric with step 07's keyword threshold, and the only option that FORCES step 05 to retry on architectural-topology candidates. v12 predicts: step 05.5 fires R279-pattern rejection at non-trivial rate; downstream step 13.5 attack success drops (architectural candidates have different load-bearing weakness); mean kw forced-hit rises (architectural keywords overlap published architectural papers more). PASS rate stays at 0 (saturation is robust). The v12 signal is in the candidate-population shift, not the verdict.
