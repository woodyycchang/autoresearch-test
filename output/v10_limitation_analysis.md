# v10 Limitation Analysis (Phase 1 of v11 task)

**Author:** Claude (Opus 4.7), branch `claude/build-v11-reward-channel-v1hrh`.
**Date:** 2026-05-20.
**Sources read:** `output/v9_failure_diagnosis_v2.md`, `output/epoch29_comparison.md`, `program_v10.md`, `rounds/round_279/13_experiment_spec.json`, `rounds/round_708/13_experiment_spec.json`, `rounds/round_715/13_experiment_spec.json`, `rounds/round_725/13_experiment_spec.json`, `logs/policy_state.json`, `output/stats_round_725.json`.

**Diagnostic question:** v10 step 13 generates an experiment SPEC but the spec is never executed. Does spec-without-execution produce a *real* reward signal, or is it another evidence channel masquerading as reward?

**Answer (one sentence):** It is **another evidence channel masquerading as reward** — but with a specific, non-trivial contribution: the `distinguishability_pre_check` field encodes a structural-reasoning signal that is orthogonal to literature-based signals (06, 11.5) and landscape-based signals (08, 09), so v10 is not value-less; the "reward" framing is over-strong, and the right v11 upgrade is to extract more signal from the same hypothetical-experiment channel rather than to claim execution we cannot perform.

---

## 1. Restating what v10's step 13 actually computes

A `13_experiment_spec.json` FIRED file contains:
- An `experiment.variants` block with A_candidate / B_control / C_baseline definitions.
- A `metric` + `statistical_test` block specifying what would be measured if the spec were run.
- A `distinguishability_pre_check` block with `test_variant_distinguishable_from_control ∈ {true, false, uncertain}` plus a 1-3 sentence `rationale`.
- A `budget_compliance` block stating estimated T4 runtime ≤ 30 min.

**Critical:** No code is run. No metric is computed on real data. The `distinguishability_pre_check` verdict is the output of *LLM reasoning about what would happen if the spec were executed*, taking as input:
1. The candidate's sub-mechanism decomposition (M_1...M_K from `05_sample_tokens.json`).
2. The step 11.5 adversarial finding (which prior-art papers cover which sub-mechanisms).
3. The LLM's prior over how "soft regularization toward a specific spectrum" / "topological invariant of a small simplicial complex" / "Dirichlet continuation of a finite series" would behave at the chosen dataset scale.

This is structural reasoning on top of (1)+(2)+(3). It is NOT an empirical observation outside the literature/prior space.

---

## 2. The evidence-vs-reward taxonomy revisited

`output/v9_failure_diagnosis_v2.md` §2.1 defined:
- **Evidence channel:** a feature/observation read from literature or LLM prior.
- **Reward channel:** a scalar that ranks candidates by an objective external standard (empirical observation outside the LLM/literature).

Under this taxonomy:

| Channel | Source | Type per v9 diagnosis | What v10 epoch actually used |
|---|---|---|---|
| Step 06 web_search | retrieved papers | Evidence | Evidence |
| Step 06.5/06.7 | retrieved papers + LLM judge | Evidence | Evidence |
| Step 07 / 10 | mechanical aggregation | Evidence | Evidence |
| Step 08 / 09 | LLM prior on landscape | Evidence | Evidence |
| Step 11 Q-rubric | file-chain deterministic | Evidence | Evidence |
| Step 11.5 adversarial | retrieved papers via 2nd LLM | Evidence | Evidence |
| Step 12 tree-stream | retrieved papers per hint | Evidence | Evidence |
| **Step 13 distinguishability_pre_check** | **LLM structural reasoning about a hypothetical experiment** | **claimed: partial reward** | **actually: evidence (structural-reasoning subtype)** |

Step 13's `distinguishability_pre_check` is computed by reading the candidate's structural decomposition and asking "would A_candidate produce a different metric distribution from B_control if we ran the spec?" That question is *answered* by LLM inference from the candidate's structural relationship to the control variant. No data is observed; no metric is computed on a real dataset. The output is therefore a *structural-reasoning evidence channel*, not a reward channel under v9_failure_diagnosis_v2.md's own definition.

**v10 used the word "reward" loosely.** What v10 actually added is a NEW subtype of evidence channel — *structural-distinguishability evidence*, distinct from literature-retrieval evidence and landscape-prior evidence — but it is still on the evidence side of the taxonomy.

---

## 3. Why this is not a complete failure of v10

v10's structural-distinguishability channel is genuinely orthogonal to the prior channels. Demonstrated:

| Round | Step 13 distinguishability | Prior channel verdict | Did step 13 add information? |
|---|---|---|---|
| R725 Heegaard genus | **false** (parametrization-only) | step 10 FAIL (kw=2); tree-stream FAIL; q-rubric ANTICIPATED | **Yes** — the prior channels said FAIL via keyword overlap; step 13 said FALSE via structural-collapse-to-Betti-1 reasoning. Different reason, same verdict. |
| R708 Dirichlet | **uncertain** | step 10 FAIL; tree-stream FAIL | **Partial** — step 13 surfaces the conditional "if importance is monotone-decay then continuation ≈ rescaled magnitude"; prior channels do not. |
| R715 Ramsey | **uncertain** | step 10 FAIL; tree-stream FAIL | **Partial** — step 13 surfaces "Ramsey K_3 guarantee on K_8 doesn't bind tightly for 1024-token sequences"; prior channels do not. |
| **R279 retrofit** | **false** | v7 step 11.5 FAIL_ADVERSARIAL (SORSA/SODA at 0.80 covers M_1+M_2+M_4+M_5) | **Yes — independently arrived at the v7 verdict via a different reasoning path.** |

The R279 retrofit is the strongest single piece of evidence that step 13 is doing real work: it converged with the v7 adversarial-literature finding *via a different reasoning path* (structural collapse of A into B, vs literature-retrieval of papers covering 4 of 5 sub-mechanisms). Convergence-from-orthogonal-paths is a meaningful signal even when no execution happens.

But: this still does not promote step 13 from "evidence" to "reward." It promotes it to "high-quality evidence channel that converges with adversarial-literature on R279."

---

## 4. Where v10's reward framing falls short

Three specific failures of the "step 13 = reward channel" claim:

### 4.1 The distinguishability verdict is author-biased

The same LLM context that wrote the candidate (via step 05 token streams) wrote the step 13 spec and the distinguishability pre-check. The author has a soft incentive to write "uncertain" rather than "false" — uncertain preserves optionality. In v10 E29, 2/3 fired specs were uncertain; only 1 was false (R725 — and R725's Heegaard framing is so obviously collapsible that even an author-biased context could not defend it).

A genuine reward channel would not be biased by the spec author's incentive. Step 11.5's adversarial agent reads the candidate but actively searches for prior art with NO source-domain priming — this is what makes it an honest evidence channel. Step 13 lacks an analogous adversarial protection.

### 4.2 Hypothetical reasoning cannot rule out empirical surprise

Step 13's distinguishability_pre_check answers "would the spec be distinguishable IF RUN?" The answer is LLM inference. Real experiments occasionally surprise — a candidate the prior says is parametrization-only might surface non-trivial effects (e.g., the integer-ratio constraint of R279 might introduce numerical stability properties orthogonal to the published SORSA/SODA scaffold). The hypothetical reasoning channel has no way to detect such surprises because it never queries the world.

### 4.3 No mechanism to convert "uncertain" into actionable signal

v10's step 13 produced 2 "uncertain" verdicts (R708, R715) and 1 "false" (R725). The "uncertain" verdicts are the *most diagnostically interesting* (they are where the candidate might still have value) but step 13 has no follow-up — uncertain stays uncertain, gets logged, and the verdict does not flip. The signal is informational, not actionable.

A real reward channel produces a number that ranks candidates. v10's step 13 produces a 3-class label (true / false / uncertain) where the middle class is the modal output in E29 and provides no rank ordering.

---

## 5. What this implies for v11

The fundamental constraint is the same as in v10: we cannot execute experiments in the v11 pipeline (budget, latency, infrastructure). So v11 cannot promote step 13 from evidence to reward in the strict taxonomic sense.

What v11 *can* do — and what the user's prompt asks for — is **extend the reward channel** by extracting more signal from the same hypothetical-experiment substrate. Four directions were proposed:

### 5.1 Evaluating the four options

| Option | What it adds | Cost | Addresses v10 failure mode? |
|---|---|---|---|
| **(a) Spec-execution stub** (write `13_runnable.py`) | Concrete Python artifact; still unexecuted in v11 | Medium per top-3 round (writing real code) | Partially addresses §4.3 (more concrete signal); does NOT address §4.1 (author-bias) or §4.2 (hypothetical-only) |
| **(b) Adversarial step 13** (2nd agent attacks the spec) | Independent skeptical verdict on same spec | Low (1 Agent spawn per top-3 round) | Directly addresses §4.1 (author bias broken by adversary) and §4.3 (attack can flip uncertain → false). Symmetric with step 11.5's literature-adversarial. |
| **(c) Cross-candidate matrix** (compare to R279/R301/R302) | Saturation-vs-corpus signal | Low (structural comparison) | Adds NEW channel (corpus saturation) but doesn't extend the *reward* channel — it adds a different evidence channel. |
| **(d) Policy state hardening** (5+ epoch tracking) | Drift collapse detection | Very low | Operates on policy, not reward — fails the "extending the reward channel" frame from the task. |

### 5.2 Why option (b) is the right v11 choice

The Phase 1 diagnosis localizes v10's weakness in *the spec author's bias plus the hypothetical-only nature of the reasoning*. The strongest extension that v11 can perform under the no-execution constraint is to introduce an INDEPENDENT skeptical context that reads the spec and tries to find ways the experiment would fail to reveal real differences. This:

1. **Breaks the author-bias loop** (§4.1) — the attacker has no incentive to preserve "uncertain"; it actively searches for "false" cases.
2. **Extracts more signal from the hypothetical** (§4.3) — the attacker can convert uncertain → false by surfacing specific failure modes the spec author missed.
3. **Is symmetric with step 11.5** — step 11.5 is the adversarial-literature channel; step 13.5 becomes the adversarial-empirical channel. The pattern is proven.
4. **Costs ≤ 5 Agent spawns/epoch** — within the honest deviation policy budget.

Options (a) and (c) are NOT wrong, but they introduce a NEW kind of channel rather than extending the existing reward channel:
- (a) extends the artifact form (JSON → Python file) but does not extract more verdicts.
- (c) introduces a corpus-saturation channel — orthogonal to and disjoint from the reward channel.
- (d) operates on policy, not reward.

Only (b) directly extends the step 13 reward channel by extracting an additional independent verdict on the SAME spec.

### 5.3 Predicted v11 effect

If v11's step 13.5 adversarial-empirical attack is implemented:

- E29's 2 "uncertain" verdicts (R708, R715) under v10 would likely be flipped to "false" under attack (the attacker would find Dirichlet ≈ magnitude under monotone-decay; Ramsey K_3 on K_8 doesn't bind for 1024 tokens — these were already noted as conditional failure modes in the spec's rationale and the attacker would promote them to load-bearing).
- E29's 1 "false" verdict (R725) would stay false (already pessimistic).
- E30's top-3 step-13 specs will get adversarial attack; expected flip rate ≈ 50-67% (the spec authors are biased toward uncertain).

This would mean v11's step 13.5 produces a verdict distribution that is shifted relative to v10 — more "false" verdicts, fewer "uncertain" verdicts. That shift IS the new signal v10 missed.

---

## 6. What v11 is NOT

v11 is not:
- An execution pipeline (no Colab runs).
- A new evidence dimension orthogonal to reward (cross-candidate is interesting but is a different upgrade path).
- A policy redesign.

v11 IS:
- An adversarial extension of the existing reward channel, symmetric with v7's step 11.5 adversarial-literature.
- Strictly additive: step 13.5 inserted AFTER step 13, BEFORE v11 verdict synthesis.
- Subject to the same FORBIDDEN-TO-MODIFY constraints as v10: step 06, 07, 10, 12, 13 spec format are UNTOUCHED.

---

## 7. Honest acknowledgments

- The conclusion "step 13 is evidence, not reward" is uncomfortable for v10's framing, but it is the right reading under v9_failure_diagnosis_v2.md's own definitions. v10 added high-quality structural-distinguishability evidence; that is genuinely new and valuable, but mis-labeling it "reward" obscures what v10 actually did.
- v11's step 13.5 will not promote step 13 to reward either. It will extract an additional independent verdict from the same hypothetical substrate. The corpus remains evidence-bound until an execution layer is added.
- The R279 retrofit's distinguishability=false is the canonical demonstration that orthogonal-path convergence is meaningful. v11's adversarial step 13.5 will test whether E30 candidates show analogous convergence under attack.

---

## 8. Diagnostic conclusion (in one paragraph)

v10's step 13 is a structural-reasoning evidence channel, not a reward channel; the "reward" framing was over-strong. The channel is still genuinely orthogonal to literature/landscape evidence and produced one canonical convergence (R279 retrofit converging with v7 step 11.5 finding via a different reasoning path). v10's specific failure modes are author bias (the spec author and pre-check author share LLM context), hypothetical-only reasoning (no empirical query), and a 3-class label that is modally "uncertain" (no actionable rank ordering). v11 extends the reward channel by adding step 13.5 — an adversarial agent that reads the step 13 spec and attempts to find failure modes the spec author missed. This is symmetric with v7's step 11.5 adversarial-literature pattern and is the cleanest extension of the reward channel under the no-execution constraint. v11's predicted effect: v10's "uncertain" verdicts will be flipped to "false" under attack at a meaningful rate, shifting the verdict distribution and producing the signal v10 missed.
