# v9 Failure Diagnosis v2 (post-E28 R676-R700)

**Author:** Claude (Opus 4.7), branch `claude/add-reward-signal-v10-K8of4`.
**Date:** 2026-05-20.
**Question (Phase 1 of v10 task):** v8 and v9 added evidence channels (Q-rubric, tree-stream, inverse-search landscape, gap-position score). Why did detector upgrades plateau without raising PASS rate?

This file extends `output/v8_failure_analysis.md` by re-reading it under a Yu-Sun-TTT + Gao-test-time-of-agent lens. It motivates `program_v10.md`.

---

## 1. Executive summary

| Version | New structural channel | PASS-rate effect | Reward signal type |
|---|---|---:|---|
| v7 (E25-E26, R601-R650) | Step 11.5 adversarial external | 0/50 | Gate (subtractive, gated on step-10 PASS) |
| v8 (E27, R651-R675) | Q-rubric + tree-stream + token streams | 0/25 | **Evidence reorganization** (no fresh judgment) |
| v9 (E28, R676-R700) | Inverse-search landscape + gap-position | 0/25 | **Hypothesized landscape** (no empirical check) |
| **v10 (target)** | **Empirical toy experiment spec + candidate policy update** | open | **Empirical reward (TTT-inspired) + policy-gradient bias (Gao-inspired)** |

**Core diagnosis (one sentence):** v8 and v9 added **evidence channels** but no **reward channel** — every signal in the pipeline reads from desk-research outputs (literature retrieval, hypothesized landscape clusters, deterministic file-chain checks); none has an **empirical handle** that distinguishes "this candidate plausibly works" from "this candidate is verbally novel." The PASS criterion "no prior art + has mechanism value" is **unverifiable at desk-research stage** because "mechanism value" requires running something.

**Why detector upgrades plateau:** v6 → v7 → v8 → v9 added more checks on the **same underlying input** (retrieved papers + LLM prior knowledge). Each new check absorbs reward-hacking pressure (v7 step 11.5 stripping; v8 Q-rubric determinism; v9 anti-leak inverse-search) but cannot raise the PASS rate because the **rate-limiting signal is not "are we checking enough?" — it is "what would actually validate this candidate?"** The answer to the second question is empirical, not literature-based.

---

## 2. Re-reading v8_failure_analysis.md under a reward-signal lens

`output/v8_failure_analysis.md` correctly diagnosed two structural failures of v8:

1. **Q-rubric is deterministically aligned with step 10** (file-chain checks; no fresh LLM judgment can enter the verdict).
2. **Tree-stream surfaces Pattern-E new variant but cannot rescue** (conservative synthesizer; one anticipated hint flips to FAIL).

v8_failure_analysis.md proposed direction (d) **inverse search** as the v9 upgrade. Direction (c) **empirical pre-check (toy experiment)** was scored "infeasible in mining context" and dropped (see `output/v8_failure_analysis.md` §4.2 table).

That dismissal was correct **for the v9 epoch scope** (running an actual training experiment per round costs >> 30 min on free hardware) but **deferred the structural problem v10 must now confront**: every desk-research-only verifier — no matter how sophisticated — operates on a subspace of the search space that lacks the empirical-difference signal. v9 inverse-search has joined v7 adversarial + v8 Q-rubric + v8 tree-stream as **another desk-research lens**.

### 2.1 The "evidence vs reward" distinction

In the RL terminology Yu Sun's TTT work uses: an **evidence channel** is a feature/observation, and a **reward channel** is a scalar that ranks candidates by an objective external standard.

| Channel | Source | Type | What it tells us |
|---|---|---|---|
| Step 06 web_search | retrieved papers | Evidence | What's published with these keywords |
| Step 06.5 semantic | retrieved papers | Evidence | Cosine to retrieved abstracts |
| Step 06.7 functional | LLM judge on retrieved papers | Evidence | Functional similarity to retrieved |
| Step 07 keyword | step 06 results | Evidence | Surface keyword overlap |
| Step 08 inverse-search (v9) | LLM prior | Evidence | Hypothesized landscape |
| Step 09 gap-position (v9) | step 08 + sample_tokens | Evidence | Lexical gap presence |
| Step 10 mechanical | step 07 + 06.5 + 06.7 | Evidence | Aggregate FAIL signal |
| Step 11 Q-rubric (v8) | file-chain checks | Evidence | Deterministic reorganization of 06-07 |
| Step 11.5 adversarial (v7) | stripped candidate + fresh search | Evidence | Adversarial framing of step 06 |
| Step 12 tree-stream (v8) | helper + solver agents | Evidence | Per-hint decomposed search |

**All 10 channels are evidence channels reading from literature/landscape priors. NONE is a reward channel.**

A reward channel for this niche-mining task would be: a quantitative signal that distinguishes "this candidate, if implemented and run on a tiny dataset, would produce a measurable effect" from "this candidate is verbally novel but would not improve any metric beyond a random/baseline control." That signal **cannot be computed** by reading literature — only by running a (small, controlled) experiment.

### 2.2 Why this matters for PASS rate

The corpus has 0 substantive PASSes in 796 verified rounds (p(no PASS | 1% H₀) ≈ 0.000335). Two interpretations are consistent with this data:

**Interpretation A (saturation):** The mining distribution is saturated — every mechanism in this distribution has prior art. The 0-PASS result is the truth.

**Interpretation B (verification gap):** There exist novel-and-valuable candidates in the distribution, but the verifier cannot distinguish them from novel-but-useless candidates because the verifier lacks an empirical signal. The 0-PASS result is an artifact of conservative verification.

v9 added inverse-search to test Interpretation B: if there are real gaps, gap_real should fire. E28 found 0/25 gap_real=true. This **strengthens** Interpretation A — but only conditionally on the inverse-search Agent's prior being calibrated. If the Agent's prior is overconfident (it generates clusters covering every conceivable area), gap_real will always be false even when real gaps exist.

**The way to disambiguate A vs B is not another desk-research channel.** Adding a v10 inverse-search-v2 or a v10 super-rubric would have the same plateau. The way to disambiguate is to **introduce an empirical channel** — a toy experiment that produces a number distinguishing the candidate from a random control.

---

## 3. Where the plateau comes from: the "no prior art + has mechanism value" non-decomposition

The PASS criterion has two conjuncts:

1. **No prior art** (literature search + adversarial framing + landscape gap)
2. **Has mechanism value** (the proposed mechanism would actually improve some metric)

v5/v6/v7/v8/v9 have all attacked conjunct 1 — increasingly sophisticated tests for prior art. The corpus shows that with v5-v9 verifiers, conjunct 1 fires FAIL on essentially every candidate in this mining distribution.

**Conjunct 2 has never been tested.** Every PASS in v5-v9 history was a "no prior art" PASS — the candidate evaded the prior-art checks. There is no candidate in the corpus that passed because "the mechanism, when implemented in a toy experiment, produced a measurable effect distinguishing it from random."

This is structurally why detector upgrades cannot raise PASS rate:

- A candidate that PASSES conjunct 1 (escapes all prior-art checks) currently auto-PASSES the whole criterion under v9, because conjunct 2 is not separately tested.
- A candidate that FAILS conjunct 1 cannot be rescued by conjunct 2 (since conjunct 2 is unverified).
- A candidate that PASSES conjunct 1 but FAILS conjunct 2 cannot be filtered out — it would be a false positive (verbal novelty without mechanism value).

R279 PTCH is the canonical case: it passed Phase-0 primary on a 0.71 semantic edge over a strict threshold (UNCERTAIN), then was downgraded under v7 adversarial when stripping revealed M_1 + M_2 + M_4 + M_5 covered by SORSA/SODA at 0.80. **R279 was never tested on conjunct 2**: does the integer-ratio singular-value constraint actually improve fine-tuning performance vs uniform or learned spectra? That question was never asked because the pipeline lacks a conjunct-2 channel.

### 3.1 What "verifiable at desk-research stage" means

A claim is "verifiable at desk-research stage" if a verifier with access only to literature, LLM priors, and deterministic computation on those can produce a high-confidence verdict. Examples:

- "Has prior art X been published?" — verifiable at desk-research (search for X).
- "Does X have surface keyword overlap with retrieved papers?" — verifiable at desk-research (compute overlap).
- "Does X fit inside a hypothesized landscape cluster?" — verifiable at desk-research (the cluster IS the landscape).

A claim is "**not** verifiable at desk-research stage" if it requires empirical observation outside the pipeline:

- "Does X improve metric M when implemented?" — NOT verifiable (requires implementation + measurement).
- "Does X distinguish itself from a random control in a controlled experiment?" — NOT verifiable.
- "Does X have higher learning efficiency than baseline Y?" — NOT verifiable.

The PASS criterion as written ("no prior art + has mechanism value") combines a verifiable claim with an unverifiable claim. v5-v9 have all chased the verifiable half. **The plateau is the unverifiable half asserting itself.**

---

## 4. Yu-Sun-TTT insight: empirical reward at test time

Yu Sun's Test-Time Training work uses the observation: at test time, a tiny self-supervised reward signal computed on the test example can guide adaptation. The reward is small, local, and quick — not a full training run, just enough to distinguish good adaptation from bad.

**Applied to niche-mining:** for each candidate that passes desk-research checks, generate a **minimal toy experiment spec** that would test conjunct 2 (mechanism value) in <30 min on free hardware. The spec includes:
- A small dataset (e.g., 1K examples from a public benchmark).
- A small model (e.g., a 1-layer transformer + LoRA on top).
- The candidate variant + a random control variant + a baseline.
- A measurable metric (e.g., loss after N steps, distinguishability via paired t-test).

The spec is **generated, not executed** at v10 epoch time. Generation produces an auditable artifact (`13_experiment_spec.json`) that:
1. Forces the candidate to commit to a specific, testable claim about mechanism value.
2. Defines what a falsifying observation would look like.
3. Provides a runnable seed for human-in-loop empirical follow-up.

The spec itself is a **partial reward channel**: a candidate that cannot even articulate a 30-min toy experiment is structurally weaker than one that can. The full reward channel is the actual experiment outcome (human-executed, post-v10).

### 4.1 Why generation-only is sufficient for v10

v10's contribution is the **policy that demands spec generation** for candidates reaching step 10 PASS or step 12 PASS-with-caveat. Even without running the experiments, the spec-generation step:
- Surfaces candidates that have no testable claim (these are excluded from "near-PASS" status).
- Surfaces candidates whose only difference from baseline is parametrization (R279-style: the test variant collapses into the random control).
- Documents what an empirical verdict would look like, for any future human-in-loop run.

The R279 retrofit (Phase 3 of v10) specifically tests this: generate a step-13 spec for R279 PTCH **after** knowing the actual Stage 1.5 / v7 adversarial result. If the spec would have flagged R279 as low-priority pre-experiment (because the test variant is a parametrization of SVD spectrum shaping, hard to distinguish from learned-spectrum control), v10 retroactively confirms its diagnostic value.

---

## 5. Gao-test-time-of-agent insight: candidate policy update

Gao's test-time-of-agent work uses the observation: an agent's per-episode policy should be biased by the reward signal from prior episodes — even when the reward is a coarse FAIL signal, the policy can avoid re-entering FAIL-correlated regions.

**Applied to niche-mining:** at each epoch start, read the prior epoch's 25 candidates and verdicts. Compute a coarse reward (currently reward = -1 for FAIL, 0 for PASS — since 0 PASSes in corpus). Use this to update a **candidate policy** that biases future candidate generation **away** from FAIL-correlated patterns.

The most actionable pattern in the corpus is `motivation_strength`:

| Strength | E26 corpus rate | FAIL rate |
|---|---:|---:|
| mechanism_transfer | 19/25 = 76% | 19/19 = 100% |
| shared_math_structure | 6/25 = 24% | 6/6 = 100% |
| metaphor_only | 0/25 = 0% (banned post-R279) | n/a |

At the motivation_strength level, all three categories FAIL uniformly — no policy gradient signal there. But within mechanism_transfer, sub-patterns vary:
- Domain class: pure-math (Drinfeld, Möbius, Catalan-Dyck) → 100% FAIL via Pattern-E new variant (step-10 surface keyword + tree-stream functional miss).
- Domain class: applied-math (Lévy stable, Petersen, Atiyah-Singer) → 100% FAIL via gap_real=false (anticipated by landscape).
- Form: spectral-allocation (R676, R689) → 2× 100% FAIL.
- Form: memory-architecture (R677, R688) → 2× 100% FAIL.

These sub-patterns provide a finer policy signal. v10's policy update tracks **candidate_distribution_drift** epoch-over-epoch: does the candidate generator move away from FAIL-correlated sub-patterns? Tracking this drift is the auditable artifact (`logs/policy_state.json`).

### 5.1 What the policy update DOES NOT do

- It does NOT bias toward "easy PASS" candidates. The policy reward is purely the corpus verdict; the policy update bias is purely "explore unmined sub-patterns."
- It does NOT modify step 10's mechanical verdict (FROZEN).
- It does NOT raise PASS rate by gaming the verifier. v10's PASS criterion is unchanged from v9 (7-signal alignment) and adds an 8th signal (step 13 experiment spec validity).
- The policy update is **epistemic** — it tells the candidate generator "you've tried this sub-pattern N times, all FAIL, try elsewhere" — not **adversarial** to the verifier.

### 5.2 Connection to empirical reward layer

Once step 13 generates an experiment spec, the policy state can track:
- Which sub-patterns generated specs with **distinguishable** test variants (variant ≠ control).
- Which sub-patterns generated specs where the test variant is a parametrization of the control (R279 pattern: not distinguishable).

This gives a finer reward signal even without running the experiments. A candidate that can articulate a distinguishable spec is a higher-reward candidate than one whose only spec collapses into the control.

---

## 6. The two v10 upgrades in design space

### 6.1 Upgrade 1: Empirical reward layer (step 13, NEW)

- **Trigger:** candidate reaches step 10 PASS OR step 12 PASS-with-caveat (tree-stream PASS without step 10 PASS).
- **Output:** `13_experiment_spec.json` — a runnable toy experiment spec.
- **Constraints:** <30 min on free Colab T4; explicit candidate-vs-control-vs-baseline comparison; quantitative metric with statistical test.
- **For v10 epoch:** generation only, not execution. Execution is human-in-loop.
- **R279 retrofit:** generate spec for R279 PTCH; validate against actual v7 adversarial findings (SORSA/SODA at 0.80 covers M_1+M_2+M_4+M_5).

### 6.2 Upgrade 2: Candidate policy update (logs/policy_state.json, NEW)

- **Trigger:** at epoch start.
- **Input:** prior epoch's 25 candidate.json + verdicts.
- **Output:** `logs/policy_state.json` — updated policy with FAIL-correlated patterns + sub-pattern reward estimates.
- **Use:** bias candidate generation in step 04.5 (memory check) and step 05 (token streams) toward unmined sub-patterns.
- **Tracking:** `candidate_distribution_drift` epoch-over-epoch.

### 6.3 What is FORBIDDEN for v10

- Step 06 web_search (UNCHANGED).
- Step 07 keyword threshold ≥ 2 (UNCHANGED).
- Step 10 mechanical verdict (UNCHANGED).
- Step 12 tree-stream (UNCHANGED).
- v9 inverse-search (step 08) + gap-position (step 09) (preserved verbatim from v9).
- All v7/v8 components (preserved verbatim).

v10 is **additive** like v9 — it inserts step 13 after step 12 and adds a side-channel policy file. The FORBIDDEN zones are untouched.

---

## 7. Why this is the right v10 direction

`output/v8_failure_analysis.md` §4.2 evaluated four directions for v9:
- (a) Multi-agent debate (3 verifiers): No prospective evidence; literature-bound.
- (b) Sequential elimination (5 framings): No prospective evidence; literature-bound.
- (c) Empirical pre-check (toy experiment): Prospective + orthogonal — **dismissed as infeasible**.
- (d) Inverse search: Prospective + orthogonal — chosen for v9.

The dismissal of (c) was correct for v9's scope (running an actual experiment per round is out of budget). But the dismissal accepted "evidence prospectivity is sufficient" — which is the v9 plateau hypothesis. v10 revisits (c) under a **spec-generation-only** scope:

- The spec is generated by the LLM in main context (no Agent spawn required for spec generation; one optional Agent spawn for double-check).
- The spec is a JSON artifact; generation cost is comparable to step 11 Q-rubric construction (<2 min).
- The spec is forward-compatible with future epochs that DO execute it (human-in-loop or automated).
- The spec adds a partial reward signal **today** (distinguishability check) and a full reward signal **tomorrow** (when executed).

This is the structurally correct upgrade because it introduces the **first non-literature-based signal** in the corpus. Combined with upgrade 2 (policy update), v10 becomes the first version that has both:
- A reward channel (step 13 spec validity + experiment outcome if run).
- A policy-gradient mechanism (logs/policy_state.json).

This matches the Yu-Sun-TTT structure (small test-time reward) and the Gao-test-time-of-agent structure (per-episode policy update).

---

## 8. Honest acknowledgment of v9's contribution

v9's inverse-search is NOT useless. It provides the first prospective evidence channel in the corpus and the first explicit signal for Pattern-E new variant rounds (FAIL_GAP_REAL_LOGGED). E28 produced 0 such labels — but that itself is informative: under the post-R279 motivation_strength bias, mining-distribution candidates are conceptually anticipated by LLM literature priors, so there is no surface for FAIL_GAP_REAL_LOGGED to fire on.

v10 preserves v9 verbatim. v10 ADDS step 13 (empirical reward layer) and `logs/policy_state.json` (candidate policy). It does NOT remove or weaken any v9 signal.

The diagnosis "v9 lacks a reward channel" is a structural observation about the SPACE of v5-v9 verifiers, not a critique of v9's design quality. v9 was the best v8+1-step extension under desk-research constraints. v10 extends into a new design subspace (empirical + policy) that was previously dismissed as infeasible.

---

## 9. Predictions for v10 / E29

| Metric | E28 (v9) | E29 (v10) prediction |
|---|---:|---:|
| substantive_pass_count | 0 | 0 (corpus saturation maintained) |
| step 10 FAIL count | 25 | 25 (FROZEN; no relaxation) |
| step 13 spec generation rate | n/a | 0-3/25 (only for step 10 PASS OR tree-stream PASS-with-caveat) |
| R279 retrofit spec_validity | n/a | distinguishable-test = false (SORSA/SODA covers scaffold; integer-ratio is parametrization choice) |
| candidate_distribution_drift | n/a | nontrivial (policy steers away from spectral-allocation + memory-architecture overload in E28) |

v10 will NOT raise PASS rate. The N=821 cumulative target (771 prior + 25 E28 + 25 E29) at p ≈ 0.000284 is consistent with corpus saturation.

What v10 WILL produce:
- The first reward-channel artifacts in the corpus (step 13 specs, even if few; minimum 1 for R279 retrofit).
- The first policy-state artifact (`logs/policy_state.json`).
- The first candidate_distribution_drift measurement.
- Validation that R279's failure was distinguishable at conjunct-2 level (not just conjunct-1 level), retroactively.

---

## 10. Honest provenance for this diagnosis

This diagnosis was authored in main agent context by reading:
- `output/v8_failure_analysis.md` (v8 structural diagnosis).
- `output/epoch28_comparison.md` (E28 v9 outcomes).
- `output/stats_round_700.json` (E28 quantitative summary).
- `program_v9.md` (v9 pipeline spec).
- `rounds/round_279/*` (R279 PTCH file chain + v7 adversarial retrofit).
- `rounds/round_676/*` (E28 representative round).
- `logs/memory_db.json` (epoch_27_summary + epoch_28_summary structures).

No new web_searches or Agent spawns were used to produce this diagnosis. The diagnosis is a structural audit of the v5-v9 design subspace, motivated by Yu Sun's TTT framework and Gao's test-time-of-agent framework.
