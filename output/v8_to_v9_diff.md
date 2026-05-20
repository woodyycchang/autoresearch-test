# v8 → v9 Diff

**Author:** Claude (Opus 4.7) on branch `claude/diagnose-v8-upgrade-v9-yRo0Q`.
**Date:** 2026-05-20.
**Purpose:** Document the v9 addition of inverse-search landscape generation
(step 08) and gap-position scoring (step 09) that addresses v8's diagnosed
failure mode — v8's Q-rubric and tree-stream were both post-hoc explanatory
verifiers that could not raise PASS rate beyond v5/v7 baseline.

---

## Why v9 and not "fix v8"

### v8 was not broken

E27 R651-R675 under v8 produced 0 substantive PASS over 25 strict-protocol
rounds. The saturation result holds; v8's three structural upgrades
(problem-structure, solution-structure, evaluation-structure) made the
verdict reconstructible from the file chain (audit-tractability).

But v8 has a structural ceiling on **PASS yield**. From
`output/v8_failure_analysis.md`:

> v8's Q-rubric absorbed reward hacking by becoming a deterministic
> restatement of step 10 (100% alignment in E27). v8's tree-stream is
> conservatively gated and surfaces Pattern-E new variant (9/25 E27 rounds)
> but cannot override the step-10 ratchet. All v8 verifiers are post-hoc
> explanatory; none generate independent evidence about the niche landscape
> itself.

A v8 PASS (if one occurred) would require step 10 PASS, tree-stream PASS,
Q-rubric NOVEL, and skeptical-reviewer NOT adversarial-hit. But step 10
keyword surface filters out ~all candidates before downstream verifiers run.

### Three options considered for v9

- **Option A** (rejected): keep v8, accept the post-hoc ceiling. The
  saturation result is structural; PASS yield is bounded by mining
  distribution.
  Rejected because Pattern-E new variant rounds (E27 9/25) suggest there
  ARE functionally-novel candidates that step 10 surface-rejects; v8 has no
  channel to surface these as candidates worthy of human review.
- **Option B** (rejected): tighten the v8 tree-stream synthesis rule to be
  less conservative (allow PASS when 4/5 solvers find no overlap).
  Rejected because relaxing tree-stream re-opens the v6 06.8 reward-hacking
  failure mode — non-conservative LLM verdicts get gamed by vocabulary.
- **Option C** (CHOSEN): add a NEW prospective verifier that does NOT
  inherit step-06 / step-07 surface bias. The inverse-search Agent
  hypothesizes the prior-art landscape from the audit harness alone, then
  step 09 deterministically scores the candidate's gap-position.

Option C operates ORTHOGONAL to step 06's retrieval. It adds the
`gap_real` signal as a NEW evidence channel and the
`FAIL_GAP_REAL_LOGGED` verdict label to make Pattern-E new variant rounds
explicitly visible in the corpus.

### What the four directions in the task description offered, and why (d) won

The task description listed four candidate directions:
- (a) Multi-agent debate: 3 verifiers debate per candidate.
- (b) Sequential elimination: 5 sequential adversarial searches.
- (c) Empirical pre-check: candidate must pass CIFAR toy test.
- (d) Inverse search: hypothesize prior-art landscape, check candidate fills a real gap.

Scoring each direction against v8's diagnosed failure mode (post-hoc
explanatory inheriting step 06 surface bias):

| Direction | Generates prospective evidence? | Orthogonal to step 06 surface? | Budget-feasible (~5 spawns/round)? | Stays in forbidden zones? |
|---|---|---|---|---|
| (a) Multi-agent debate | No — debates existing evidence | No — debaters read step 06 papers | 3 Agents per round (feasible) | Yes |
| (b) Sequential elimination | Partially — generates 5 search variants | No — still searches literature | 5 Agents per round (at budget edge) | Yes |
| (c) Empirical pre-check | **Yes** — runs toy ML experiment | **Yes** — empirical, not literature | Infeasible (requires actual training) | Yes |
| **(d) Inverse search** | **Yes** — generates landscape hypothesis | **Yes** — generated, not retrieved | 1-2 Agents per round (very feasible) | **Yes** |

(d) is the unique direction that:
- Generates prospective evidence (not just reads existing file-chain fields).
- Operates orthogonally to step 06 (the Agent does NOT see retrieved papers).
- Fits the per-epoch Agent budget (≤ 25 inverse-search Agents per epoch).
- Stays inside the FORBIDDEN-to-modify zones.

(c) is conceptually strong but infeasible in the mining context (no actual
model training). (a) and (b) inherit step-06 bias because they operate on
retrieved literature.

**v9 adopts direction (d): inverse search.**

---

## What v9 ADDS (two new steps)

### Step 08 — Inverse-search landscape generation (NEW)

```
v8: (no step 08)
v9: 08_inverse_landscape.json
```

An inverse-search Agent reads ONLY `05_task_tokens.json` (the audit harness)
— NOT `05_sample_tokens.json` (the candidate) and NOT
`06_search_raw.json` (the retrieved papers). The Agent emits a JSON listing
3-6 prior-art clusters it EXPECTS to exist in the candidate's claimed niche,
drawing on its own training-data familiarity.

Each cluster has:
- cluster_name (short label)
- cluster_description (1 sentence in LLM vocabulary)
- expected_paper_signatures (1-3 example titles or arXiv IDs)
- claimed_coverage (which sub-mechanism this cluster covers)

An `anti_leak_check` block in `08_inverse_landscape.json` explicitly
affirms the Agent did NOT see candidate or retrieved-papers content. v9
rounds with `saw_sample_tokens = true` are MALFORMED.

### Step 09 — Gap-position scoring (NEW)

```
v8: (no step 09)
v9: 09_gap_position.json
```

A **deterministic comparison** (no LLM judgment) between the hypothesized
landscape and the candidate's stripped sample tokens:

```
for each cluster C_i in 08_inverse_landscape.json:
    keyword_overlap_C_i = |tokenize(C_i.cluster_description) ∩ tokenize(sample_tokens.stripped_llm_application)|
    sub_mechanism_match_C_i = (any sample sub_mechanism shares ≥ 2 tokens with C_i.claimed_coverage)
    inside_cluster_C_i = (keyword_overlap_C_i >= 3 or sub_mechanism_match_C_i)

gap_real = (sum(inside_cluster_C_i) == 0)
```

`gap_real = true` means the candidate sits in a niche the hypothesized
landscape leaves uncovered — a real gap. `gap_real = false` means the
hypothesized landscape anticipates the candidate.

The tokenization is fixed: lowercase, split on whitespace and punctuation,
remove stopwords ({the, a, an, is, are, of, for, with, and, or, on, in, to,
that}). The threshold ≥ 3 keyword overlap requires meaningful lexical
overlap, not just one shared word.

---

## What v9 PRESERVES VERBATIM (★ FORBIDDEN-TO-MODIFY)

| Zone | v5 | v6 | v7 | v8 | v9 |
|---|---|---|---|---|---|
| Step 06 web_search | ★ FROZEN | ★ FROZEN | ★ FROZEN | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 07 keyword threshold ≥ 2 | ★ FROZEN | ★ FROZEN | ★ FROZEN | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 10 mechanical verdict | ★ FROZEN | DIVERTED 06.8 | ★ FROZEN (RESTORED) | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 11.5 adversarial external | n/a | n/a | ★ FROZEN (NEW v7) | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 05 token streams | n/a | n/a | n/a | ★ NEW v8 | ★ FROZEN (UNCHANGED) |
| Step 11 Q-rubric | n/a | n/a | n/a | ★ NEW v8 | ★ FROZEN (UNCHANGED) |
| Step 12 tree-stream | n/a | n/a | n/a | ★ NEW v8 | ★ FROZEN (UNCHANGED) |

The user-explicit FORBIDDEN list for E28:
- step 06 web_search → preserved
- step 07 keyword threshold ≥ 2 → preserved
- step 10 mechanical verdict → preserved

All v8 contributions are also preserved verbatim. v9 is **purely additive**:
two new steps (08, 09) between step 07 and step 10.

---

## What v9 REMOVES

Nothing. v9 is purely additive on top of v8. The v9 file chain is the v8
file chain plus two new files (`08_inverse_landscape.json`,
`09_gap_position.json`).

---

## New verdict label in v9

```
v8: PASS | FAIL | FAIL_ADVERSARIAL
v9: PASS | FAIL | FAIL_ADVERSARIAL | FAIL_GAP_REAL_LOGGED       ← NEW v9
```

`FAIL_GAP_REAL_LOGGED` is assigned when:
- `10_decision.verdict == FAIL` (step 10 mechanical surface FAIL), AND
- `12_tree_stream.max_per_hint_similarity < 0.5` (tree-stream finds no
  functional overlap), AND
- `09_gap_position.gap_real == true` (candidate sits in hypothesized gap).

This is the Pattern-E new variant pattern explicitly labeled. These rounds
are NOT PASS (the mechanical verdict is FROZEN) but they are documented
for human review and represent the v9 contribution to honest accounting.

---

## Scoring formula change

```
v8: score_v8 = (confirmed_substantive_pass × 10)
             + (25 − mean_forced_hit)
             + (tree_stream_step_10_alignment_rate × 5)
             − (false_positive_count × 5)
             − (adversarial_hit_count × 10)
             + (qrubric_step_10_alignment_rate × 3)
             + (mean_hints_per_round / 7 × 2)

v9: score_v9 = (confirmed_substantive_pass × 10)
             + (25 − mean_forced_hit)
             + (tree_stream_step_10_alignment_rate × 5)
             − (false_positive_count × 5)
             − (adversarial_hit_count × 10)
             + (qrubric_step_10_alignment_rate × 3)
             + (mean_hints_per_round / 7 × 2)
             + (gap_real_rate × 4)                         ← NEW v9 term
             + (FAIL_GAP_REAL_LOGGED_count / N × 2)        ← NEW v9 term
```

Where:
- `gap_real_rate = count(rounds with gap_real == true) / N_rounds_in_epoch`.
- `FAIL_GAP_REAL_LOGGED_count` = count of rounds with step 10 FAIL AND
  gap_real == true AND tree-stream max per-hint sim < 0.5.
- N_rounds_in_epoch = 25 in epoch 28.

**Why two new terms (not one):**
- `gap_real_rate × 4`: rewards inverse-search providing a non-trivial signal
  across the epoch. If `gap_real` is always false (every candidate sits in
  some hypothesized cluster), inverse-search is not adding information.
- `FAIL_GAP_REAL_LOGGED_count × 2`: rewards explicit naming of the
  Pattern-E new variant pattern that v8 surfaced but could not label.

`confirmed_substantive_pass` under v9 requires ALL of:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- tree_stream verdict = PASS (all solver hints NOT anticipated, max sim < 0.7), AND
- q_rubric_verdict = NOVEL (q_rubric_score < 0.5), AND
- `gap_real == true`, AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7.

**Seven independent signals must align.** Strictly more demanding than v8.

---

## Calibration evidence (predicted)

### R658 DRINFELD under v9 (retrospective)

E27 R658 was a Pattern-E new variant round under v8:
- Step 10: FAIL (3 keyword hits on generic "category", "multi-agent",
  "monoidal").
- Tree-stream: max per-hint sim 0.30 (functionally novel).
- Q-rubric: ANTICIPATED (aligned with step 10 by construction).

Under v9:
- Step 08 inverse-search: Agent reads R658 `05_task_tokens.json` (audit
  question: "multi-agent LLM communication mechanism anticipated by
  2024-2026 prior art?"). Without seeing the candidate's Drinfeld-center
  framing, Agent emits clusters like:
  - C1: "RL-coordinated multi-agent LLM" (with Sakana-AI 2024, MA-RLHF 2025)
  - C2: "Pressure-field message-passing" (with 2601.08129 cited)
  - C3: "Hierarchical multi-agent" (with 2501.06322 cited)
  - C4: "Tool-use multi-agent" (with ReAct family)
- Step 09 gap-position: candidate's `sample_tokens.stripped_llm_application`
  describes "center-of-category construction over message-space with
  braiding morphism for invariant extraction". Tokenizing against C1-C4
  descriptions: 0-2 keyword overlap per cluster (category, center, braiding
  do not appear in C1-C4); sub_mechanism_match all false. All clusters
  inside_cluster = false. `gap_real = true`.
- Step 10: FAIL (★ FROZEN; 3 keyword hits unchanged).
- Tree-stream max per-hint sim 0.30 < 0.5.
- **v9 verdict: FAIL_GAP_REAL_LOGGED.** First explicit Pattern-E new variant
  label in the corpus.

### R675 BIRCH-MURNAGHAN under v9 (retrospective)

E27 R675 was the most extreme Pattern-E new variant round under v8:
- Step 10: FAIL (2 keyword hits on "SAM", "Hessian tracking").
- Tree-stream: max per-hint sim 0.35.

Under v9:
- Step 08 inverse-search: Agent reads R675 `05_task_tokens.json` (audit
  question: "basin-stability/training-stability mechanism anticipated by
  2024-2026 prior art?"). Without seeing the candidate's EOS framing,
  Agent emits:
  - C1: "Sharpness-aware optimization SAM" (Foret et al. 2021)
  - C2: "Hessian eigenvalue tracking" (Yao et al. 2020)
  - C3: "Curvature-based regularization" (KFAC, Fisher info)
  - C4: "Loss-landscape geometry surveys"
- Step 09 gap-position: candidate's
  `sample_tokens.stripped_llm_application` describes "weight-space volume,
  bulk modulus K_0, 3rd-order EOS fit, basin-stability gauge". Tokenizing
  against C1-C4: "weight" appears in C1 description; "curvature" may appear
  in C2/C3. But "volume", "bulk modulus", "EOS", "fit", "gauge" do not.
  Overlap typically < 3 per cluster. Sub_mechanism_match all false (EOS
  fitting is not a published sub-mechanism in any of C1-C4). `gap_real =
  true`.
- v9 verdict: **FAIL_GAP_REAL_LOGGED.**

### A v9 PASS candidate would require

Step 10 PASS (0 keyword hits across all retrieved papers) AND
tree-stream PASS (all solver hints not_anticipated, max sim < 0.7) AND
Q-rubric NOVEL (score < 0.5) AND
`gap_real == true` AND
skeptical-reviewer NOT adversarial_hit.

Given the 771-round saturation already established by E27, the v9 PASS
criterion is unlikely to be met in E28. v9's value is in EXPLICITLY LABELING
Pattern-E new variant rounds as `FAIL_GAP_REAL_LOGGED`, providing the first
prospective-evidence channel in the corpus.

---

## Migration plan

- R676-R700 runs under v9 in epoch 28.
- v8 rounds (R651-R675) NOT retroactively re-run under v9. They are
  retained as v8 forensic record. The retrospective predictions for R658
  and R675 above are CALIBRATION PREDICTIONS, not new round data.
- memory_db.json updated with v9 fields per round in epoch 28.
- stats_round_700.json adds v9 inverse-search / gap-position metrics.

---

## Budget realism for E28

v9 step 08 spawns 1 inverse-search Agent per round. v8 carry-over: helper
Agent (step 12) + 4-7 solver Agents per hint. If real Agent spawns are
budget-constrained (as in E27 with 6/25 helpers + 0/25 solvers = 6 real
spawns total), the v9 inverse-search Agent realization rate will likewise
be low.

**HONEST DEVIATION POLICY (from task description):**
> "if real Agent spawns exceed budget, document explicitly. Do NOT
> synthesize >5 verifiers — truncate epoch and log instead."

v9 honors this: the cap is 5 real inverse-search Agent spawns per epoch
(approximately one per 5 rounds). Beyond that, the agent SHOULD truncate
the epoch and log the truncation in `output/epoch28_comparison.md` rather
than synthesize more verifiers in main context. This is a tighter constraint
than E27's "synthesize with documented honest deviation" pattern.

E28 honest realization expectation:
- Step 08 inverse-search Agents: ≤ 5 real spawns; the remaining 20+ rounds
  use `main-context-synthesized-inverse-search-R<num>` with explicit
  documentation of the deviation per the policy.
- Step 12 helper Agents: same pattern as E27 (≤ 6 real spawns).
- Step 12 solver Agents per hint: 0 real spawns expected (same as E27).
- Step 11.5 skeptical-reviewer: only fires on step 10 PASS — likely 0 in E28
  (saturation result).

---

## What v9 explicitly does NOT promise

- v9 does NOT promise more substantive PASS verdicts. The 771-round
  saturation is structural; v9 cannot manufacture novelty that does not
  exist in the niche-mining generator distribution.
- v9 does NOT promise 0 false positives. Time-lag false positives remain
  possible.
- v9 does NOT re-litigate the 771-round 0-substantive-PASS corpus statistic.
- v9 does NOT modify the four FORBIDDEN zones (step 06, step 07, step 10,
  step 11.5).
- v9 does NOT modify the v8 components (step 05 token streams, step 11
  Q-rubric, step 12 tree-stream).

What v9 promises is:
- A NEW prospective evidence channel (`gap_real`) that does NOT inherit
  step 06 surface bias.
- The first explicit label for Pattern-E new variant rounds
  (`FAIL_GAP_REAL_LOGGED`).
- A 7-signal PASS criterion that is strictly more demanding than v8's
  6-signal criterion.
- Honest accounting under a strict budget policy: no >5 synthesized
  verifiers, truncate and log instead.
