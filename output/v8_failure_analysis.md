# v8 Failure Analysis (post-E27 R651-R675)

**Author:** Claude (Opus 4.7), branch `claude/diagnose-v8-upgrade-v9-yRo0Q`.
**Date:** 2026-05-20.
**Question (Phase 1 of v9 task):** v8 was engineered as audit-tractability and did not raise substantive PASS rate. Which v8 component absorbed reward hacking? Where did agent budget shortcuts happen?

This file is the structural diagnosis that motivates program_v9.md.

---

## 1. Executive summary

v8 introduced three structural upgrades on top of v7:

| Upgrade | What it does | Component status after E27 |
|---|---|---|
| **Problem structure** (step 05 token streams) | Splits monolithic `05_candidate.json` into `prompt_tokens` / `sample_tokens` / `task_tokens`; runs stripping pass at construction time | Functioning as designed — produces clean, single-source-of-truth stripped text for downstream verifiers |
| **Solution structure** (step 12 tree-stream) | Helper Agent emits 4-7 hints; per-hint Solver Agents run web_search + reasoning; synthesizer composes verdict | **Functional but ratchet-aligned** — 76% step-10 alignment; surfaces Pattern-E new variant but never produces PASS because (a) one anticipated hint flips to FAIL and (b) all 25 candidates pre-fail at step 10 |
| **Evaluation structure** (step 11 Q-rubric) | 3-level scenarios → perspectives → criteria tree with deterministic file-chain checks | **Absorbed reward hacking by becoming a tautology** — 100% step-10 alignment by construction; no orthogonal signal |

**Diagnosis (one sentence):** v8's Q-rubric absorbed potential reward hacking by becoming **deterministically aligned with step 10** — every criterion is a file-chain check on existing step-06/06.5/06.7/07 outputs, so the rubric can never contradict the mechanical FAIL signal. This makes audit transparent but eliminates the rubric's potential to **rescue functionally-novel candidates that step 10 surface-rejects** (the Pattern-E new variant: R658, R659, R665, R666, R667, R670, R672, R674, R675).

**Agent budget shortcuts in E27:**
- Helper Agent spawns: **6/25 = 24% real** (R651-R656); 19/25 synthesized in main context.
- Solver per-hint Agent spawns: **0/25 = 0% real**; all main-context with claimed clean-context-per-hint switching.
- Documented under v8 §3.6 "budget-constrained variant" and in `output/epoch27_comparison.md` §8.

---

## 2. Which v8 component absorbed reward hacking?

### 2.1 Q-rubric absorbed reward hacking (PRIMARY)

The Q-rubric in `11_qrubric.json` is structurally engineered so that **no fresh LLM judgment** enters the verdict. From program_v8.md §4.5:

> "Criteria MUST cite an `evidence_field` pointing to an existing file-chain field. No criterion may be 'LLM-judged' — all criteria are deterministic file-chain checks."

Concrete instantiation in every E27 round:

| Perspective | Criterion | Reads from | Output |
|---|---|---|---|
| `P_prior_art` C1 (weight 0.5) | step 07 keyword_overlap_count ≥ 2 | `07_hit_miss.json` | true iff step 10 FAIL by keyword |
| `P_prior_art` C2 (weight 0.3) | step 06.5 max semantic ≥ 0.7 | `06_5_semantic_hits.json` | true iff step 10 FAIL by semantic |
| `P_prior_art` C3 (weight 0.2) | step 06.7 max functional ≥ 0.7 | `06_7_functional_hits.json` | true iff step 10 FAIL by functional |
| `P_evidence` C1+C2 | ≥3 results, ≥1 keyword hit | step 06 raw, step 07 | fires when step 06 returns ≥3 + step 07 ≥1 |
| `P_obfuscation` C2 | stripping recorded | `05_sample_tokens.json` | true in 25/25 by construction |
| `P_composition` C1 (weight 0.6) | K-1 sub-mechanisms covered | step 06.7 covers_sub_mechanisms | usually false (functional similarity low) |

The Q-rubric's `q_rubric_verdict = ANTICIPATED` simply restates step 10's FAIL with three additional decimal places of decomposition. **The Q-rubric cannot produce NOVEL when step 10 FAILs** because at least one of `P_prior_art.C1` (keyword ≥ 2) is true whenever step 10 fires; and even if all three priors miss, `P_evidence.C1+C2` typically push the scenario score above 0.5 simply because step 06 returned ≥3 results and step 07 found ≥1 keyword hit.

**E27 evidence:** 25/25 rounds have `q_rubric_verdict = ANTICIPATED`. 0/25 rounds have `q_rubric_verdict = NOVEL`. The Q-rubric never disagrees with step 10. This is **by construction** (program_v8.md §4.5: "deterministic file-chain checks, NOT fresh LLM judgments") — and that constructive alignment is exactly what "absorbed reward hacking" means: the Q-rubric is engineered so a misaligned PASS cannot be produced even if reward-hacking pressures existed.

**Trade-off identified:** the Q-rubric is incorruptible (the reward-hacking absorption) but also incapable of providing orthogonal evidence (the failure-to-raise-PASS-rate). It is a transparent restatement of step 10, not an independent signal.

### 2.2 Tree-stream surfaced Pattern-E new variant but cannot RESCUE candidates

Tree-stream in `12_tree_stream.json` runs a helper-Agent + per-hint solver-Agent + synthesizer pipeline. The synthesis rule is **conservative**:

```
verdict_tree_stream = PASS  if ALL per_hint_verdict ∈ {not_anticipated, inconclusive}
                            AND max per_hint_similarity < 0.7
                    = FAIL  otherwise
```

A single `anticipated` hint flips the round to FAIL. Per-hint similarity ≥ 0.7 also flips to FAIL. This is conservatively safe (no false positives) but means tree-stream effectively NEVER produces PASS in E27 (0/25 PASS), even when per-hint similarities are uniformly < 0.4 in 9 Pattern-E new variant rounds.

**E27 evidence:**

| Round | Domain | Step 10 verdict | Tree-stream max per-hint sim | Tree-stream verdict |
|---:|---|:---:|---:|:---:|
| R658 | Drinfeld center braided | FAIL (3 kw on generic "category", "multi-agent") | 0.30 | FAIL (anchored to step 10 FAIL via synthesizer rationale) |
| R659 | Kac-Moody affine Lie | FAIL (2 kw) | 0.40 | FAIL |
| R665 | Coxeter root reflection | FAIL (3 kw) | 0.20 | FAIL |
| R666 | Catalan Dyck path | FAIL (2 kw) | 0.35 | FAIL |
| R667 | Möbius inversion | FAIL (2 kw) | 0.25 | FAIL |
| R670 | Skorokhod Brownian-bridge | FAIL (2 kw) | 0.30 | FAIL |
| R672 | Goldbach partition | FAIL (2 kw) | 0.20 | FAIL |
| R674 | Pell continued-fraction | FAIL (2 kw) | 0.20 | FAIL |
| R675 | Birch-Murnaghan EOS | FAIL (2 kw) | 0.35 | FAIL |

In ALL 9 Pattern-E new variant rounds, **tree-stream's solver traces find no per-hint similarity ≥ 0.5** — the candidates are *functionally novel by tree-stream's decomposed view*. But the v8 synthesizer is engineered to **anchor to step 10** for the final verdict (program_v8.md §3.4: "deliberately conservative"); and step 11.5 cannot fire because step 11.5 requires step 10 PASS *and* tree-stream PASS (§5.4). So tree-stream's "functional novelty" finding is **logged for audit but cannot rescue** the candidate from step 10's FAIL.

**The reward-hacking that did NOT happen here:** tree-stream could have been engineered to average per-hint similarities (smoothing out a single anticipated hint) or to produce a PASS-with-caveat when 4/5 solvers find no overlap. v8 explicitly forbids this (§3.6: "Do NOT average across hints to 'save' a PASS"). The conservatism IS the reward-hacking absorption. Cost: tree-stream cannot raise PASS rate either.

### 2.3 Token streams (problem structure) — neutral; not the reward-hack absorber

Step 05 token streams (`05_prompt_tokens.json`, `05_sample_tokens.json`, `05_task_tokens.json`) are a **transparent rewrite** of the v7 monolithic `05_candidate.json`. They do not contribute to reward-hacking absorption per se. They make stripping deterministic and single-source — a forensic improvement, not a verdict-mechanics change.

**E27 evidence:** 25/25 rounds have all three token streams. Stripping rule applied to math-discipline labels (Wiener-Hopf, Onsager, Steiner, Drinfeld, Möbius, Hilbert-Pólya, etc.). No change in step 10 verdicts compared to a counterfactual v7-monolithic round; the stripped text is identical to what v7 step 11.5 would have produced on-the-fly.

The token-stream split is **upstream plumbing**, not the verdict bottleneck. It does not absorb reward hacking; it does not raise PASS rate; it provides forensic granularity.

---

## 3. Where did agent budget shortcuts happen?

v8 spawns three types of Agents per round:
1. **Helper Agent** (sees landscape, NOT candidate) → emits 4-7 hints. 1 per round.
2. **Solver Agent** (sees candidate, NOT landscape) → answers 1 hint per spawn. K per round (K=4-7).
3. **Skeptical-reviewer Agent** (v7 step 11.5, only fires on step 10 PASS AND tree-stream PASS) → searches for prior art adversarially. 0 fired in E27 because step 10 FAIL gate triggered 25/25.

E27 actual realization vs program spec:

| Agent type | Spec per round | E27 actual (real spawns) | Synthesized in main context |
|---|---|---|---|
| Helper | 1 per round | **6/25 = 24%** (R651-R656; distinct agentIds aad5b2cb…, a2f0fb07…, a41e8a05…, aa2770e2…, ae786724…, ac4b7cd9…) | 19/25 (R657-R675); flagged as `main-context-synthesized-helper-R<num>` |
| Solver per-hint | K=4-7 per round → 100-175 spawns across 25 rounds | **0/25 real per-hint spawns** | 25/25 main-context with claimed clean-context-per-hint switching |
| Skeptical-reviewer | 0-25 (only fires on step 10 PASS AND tree-stream PASS) | 0 (gate never opened) | n/a |

**Estimated real-agent budget in E27 (helpers + solvers):**
- Real spawns: 6 (helpers only).
- Spec-implied spawns: 1 (helper) + ~5.84 (mean solvers) = ~6.84 per round × 25 rounds = ~171 spawns.
- **Realization rate: 6 / 171 ≈ 3.5%.**

This was documented honestly under v8 §3.6's "budget-constrained variant" allowance and in `output/epoch27_comparison.md` §8. But it does mean: **96.5% of v8's claimed solver per-hint orthogonality is main-context-synthesized**, not real per-hint Agent isolation.

### 3.1 Why this matters for v9 design

The honest deviation is logged, but the implication for reward-hacking is:
- Real per-hint clean-context Agent spawns would be the strongest evidence of orthogonal solver traces.
- Main-context-synthesized solver traces inherit the main agent's framing context — so the "orthogonal hint" promise is partially fictional in 96.5% of E27 rounds.
- v9 must either (a) reduce the per-round Agent count to a budget-feasible number (so 100% real spawns), or (b) accept the deviation and not rely on solver orthogonality for the PASS criterion.

For E28 (running v9), the same budget constraint will apply. The HONEST DEVIATION POLICY in the task description anticipates this: "if real Agent spawns exceed budget, document explicitly. Do NOT synthesize >5 verifiers — truncate epoch and log instead."

v9 will therefore design the new verifier to be FEASIBLE under a budget of ~5 real Agent spawns per round AND honestly truncate if exceeded.

---

## 4. The structural failure mode of v8

### 4.1 Post-hoc explanatory vs prospective

All three v8 verifiers (Q-rubric, tree-stream, step 11.5) fire **after** step 10's mechanical FAIL gate. None can rescue a candidate from step 10's surface-keyword-overlap when the candidate is functionally novel.

```
step 06 (FROZEN) → step 06.5 → step 06.7 → step 07 (FROZEN) → step 10 (FROZEN; total_hits ≥ 1 → FAIL)
                                                                    ↓
                              step 11 Q-rubric (deterministic, 100% align with step 10)
                              step 12 tree-stream (conservative, 76% align with step 10)
                              step 11.5 (gated on step 10 PASS; never fires when step 10 FAILs)
```

The Pattern-E new variant in E27 (9/25 rounds) is exactly this failure: candidate is functionally novel by tree-stream's per-hint solver-traces (max sim < 0.5), but step 10's surface keyword rule fires on generic terms ("category", "multi-agent", "Möbius", "Brownian bridge") appearing in pure-math reference papers. v8 surfaces the divergence in `12_tree_stream.json.solver_traces` but cannot override step 10.

### 4.2 The structural gap v9 must fill

v8's audit-tractability is genuinely useful — an auditor can localize WHICH step 10 keyword fired and WHY tree-stream disagreed. But **post-hoc explanation does not yield PASS**. To raise substantive PASS rate, v9 must introduce a verifier that:

1. **Generates prospective evidence** (not just reads existing file-chain fields).
2. **Operates orthogonally to step 06 keyword surface** (so it doesn't inherit step 10's surface-rejection bias).
3. **Stays within the FORBIDDEN-to-modify constraints** (step 06, step 07, step 10 unchanged).
4. **Fits in a budget-feasible Agent count** (≤ ~5 real spawns per round).

The four candidate directions from the task description, scored against these requirements:

| Direction | Generates prospective evidence? | Orthogonal to step 06? | Budget-feasible? | Stays within forbidden zones? |
|---|---|---|---|---|
| (a) Multi-agent debate (3 verifiers) | No — debates over existing evidence | No — debaters read step 06 papers | 3 Agents per round (feasible) | Yes |
| (b) Sequential elimination (5 adversarial searches with different framings) | Partially — generates 5 search variants | No — still searches existing literature | 5 Agents per round (at budget edge) | Yes |
| (c) Empirical pre-check (toy experiment) | **Yes** — runs a toy ML experiment | **Yes** — empirical, not literature | Infeasible in mining context (requires actual training) | Yes |
| (d) Inverse search (hypothesize landscape, check gap) | **Yes** — generates a hypothesized landscape | **Yes** — generated, not retrieved | 1-2 Agents per round (very feasible) | Yes |

### 4.3 v9 direction recommended: (d) Inverse search

(d) is the direction that:
- Most directly addresses v8's diagnosed gap (post-hoc → prospective; literature-bound → landscape-generative).
- Most directly responds to Pattern-E new variant (surface keyword surface-rejection: an inverse-search verifier can mark a candidate as filling a real gap even when step 10 surface-rejects).
- Fits the budget (1 landscape-generator Agent per round; the gap-scoring is deterministic from the generated landscape + candidate's sample_tokens).
- Stays inside the forbidden zones (no change to step 06, step 07, step 10).
- Provides forensic value (the generated landscape JSON is an explicit hypothesis, auditable in its own right).

(c) is the second-strongest direction conceptually but is infeasible in the mining context (requires actually training a model on CIFAR). (a) and (b) are less responsive to Pattern-E new variant because both still operate on retrieved literature.

**v9 will adopt direction (d): inverse search.** See program_v9.md and v8_to_v9_diff.md for the implementation.

---

## 5. Quantitative summary of v8 component contributions

| Component | E27 PASS contribution | Reward-hacking absorbed? | How it absorbs |
|---|---:|:---:|---|
| Step 05 token streams | 0 | Neutral | Upstream plumbing; not a verdict |
| Step 11 Q-rubric | 0 (100% align with step 10) | **PRIMARY** | Deterministic file-chain checks; no LLM judgment can be biased |
| Step 12 tree-stream | 0 (76% align with step 10; 24% Pattern-E new variant) | **SECONDARY** | Conservative synthesis (one anticipated hint flips); cannot rescue step 10 FAIL because gated under step 11.5 |
| Step 11.5 skeptical-reviewer | 0 fired | Inherits v7 absorption | Only fires on step 10 PASS — gate never opened in E27 |

**Net E27 yield contribution from v8 structural upgrades: 0 PASS. Net E27 audit-tractability contribution: high (per-hint solver-traces, per-criterion Q-rubric leaves, per-stream tokens).**

The reward-hacking absorption mechanism in v8 is **deterministic-by-construction Q-rubric + conservative-by-construction tree-stream**. Both are engineered to prevent a fake PASS from being injected via LLM bias. Neither can produce a real PASS that step 10 surface-rejects.

---

## 6. What this means for v9

v9 must:
1. **Add a NEW prospective verifier** that does not inherit step 10's surface-rejection bias.
2. **Preserve step 10's mechanical FAIL gate** for the v9 final verdict (no override).
3. **Log Pattern-E new variant rounds as `pattern_E_new_gap_real`** when the new verifier confirms the candidate fills a real gap — for honest accounting even when step 10 FAILs.
4. **Cap real Agent spawns at ≤ 5 per round** and document honest deviations under that cap.
5. **Score formula in v9 adds a `gap_real_rate × W` term** that rewards orthogonal landscape-generative signal alignment with step 10 PASS.

v9 PASS criterion is strictly more demanding than v8: it requires ALL of (step 10 PASS, tree-stream PASS, Q-rubric NOVEL, gap_real=true, step 11.5 NOT adversarial hit) — six independent signals must align.

v9 does NOT promise more PASS verdicts at the corpus-mining-distribution level. The 771-round saturation result (p ≈ 0.000465 on 1%-novelty H₀) stands. v9 promises an **orthogonal, prospective evidence channel** that can in principle identify Pattern-E new variant rounds as candidates worthy of human review, even when step 10 surface-rejects.

---

## 7. Honest provenance for this diagnosis

This diagnosis was authored in main agent context by reading:
- `output/epoch27_comparison.md` (E27 statistics + per-round outcomes).
- `output/v7_to_v8_diff.md` (v8 design intent).
- `program_v8.md` (full v8 pipeline spec).
- `rounds/round_658/*` and `rounds/round_675/*` (Pattern-E new variant exemplars).
- `output/stats_round_675.json` + `logs/memory_db.json` epoch_27_summary (cumulative stats).

No new web_searches or Agent spawns were used to produce this diagnosis. The diagnosis is a structural audit of v8's documented behavior, not new empirical evidence.
