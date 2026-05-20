# v7 → v8 Diff

**Author:** Claude (Opus 4.7) on branch `claude/niche-mining-structural-upgrades-mlRIX`.
**Date:** 2026-05-20.
**Purpose:** Document the v8 addition of three structural upgrades inspired
by Gao's AI Scientist talk (Harvard, 2025) — problem structure (step 05
token streams), solution structure (step 12 tree-stream), evaluation
structure (step 11 Q-rubric) — and the FORBIDDEN-zone audit.

---

## Why v8 and not "fix v7"

### v7 was not broken

Epoch 25 (R601-R625) and Epoch 26 (R626-R650) both ran under v7
(`program_v7.md`). v7 added step 11.5 adversarial external verification
and preserved the four v5 FORBIDDEN zones. v7 produced 0 substantive
PASS over 50 strict-protocol rounds; the saturation result stands.

But v7 has a structural ceiling on **audit-tractability**. A v7 PASS
(if one were to occur) would carry a single-paragraph verifier rationale
and a single skeptical-reviewer report. An independent auditor reading
only the file chain cannot localize *which* facet of the candidate
the verifier weighted, or *which* angle the skeptical-reviewer's search
covered. The audit is opaque at the unit-of-verdict scale.

### Gao's structural framing (Harvard 2025)

Gao's AI Scientist talk decomposes every scientific judgment into three
structures:

| Structure | What it controls | v7 status |
|---|---|---|
| **Problem structure** | What facet of the candidate is under test (domain context vs sample vs evaluation harness) | Implicit — collapsed into a monolithic `05_candidate.json` |
| **Solution structure** | How the verifier searches (single-shot vs decomposed orthogonal angles) | Implicit — single verifier prompt in step 12 |
| **Evaluation structure** | How the verdict is computed (black-box scalar vs decomposed rubric) | Implicit — single LLM judge verdict |

v7 leaves all three implicit. v8 makes them explicit.

### Three options considered

- **Option A** (rejected): keep v7, accept the opacity. The 0-PASS
  saturation result is structural; audit-tractability is a luxury.
  Rejected because a future PASS — if one occurs — needs to survive
  independent forensic audit. An opaque v7 PASS is not auditable.
- **Option B** (rejected): tighten the v7 verifier prompt to enumerate
  the same structures. The verifier's per-round prompt cannot grow
  unboundedly; structures need to live in separate files for forensic
  granularity.
- **Option C** (CHOSEN): replace three steps (05, 11, 12) with explicit
  structured equivalents, preserving the v5+v7 FROZEN zones verbatim.

Option C makes each structure addressable by an auditor as a separate
file. The cost is three new file types per round (~3-5× step-05/11/12
content); the benefit is per-leaf traceability.

---

## What v8 ADDS (three structural replacements)

### Step 05 — Problem-structure replacement

v7:
```
05_candidate.json (monolithic)
```

v8:
```
05_prompt_tokens.json    ← domain context (where mechanism borrowed from)
05_sample_tokens.json    ← stripped candidate mechanism description
05_task_tokens.json      ← evaluation harness (scenario seeds, criteria seeds)
05_candidate.json        ← thin v8 index, derived from above three (backward compat for step 06 / 11.5)
```

The stripping pass that v7 step 11.5 ran on-the-fly now runs at step 05
construction time and is recorded in `05_sample_tokens.stripped_llm_application`.
This guarantees step 11, step 12, and step 11.5 all see the SAME
stripped text — no chance of drift between strip passes.

### Step 11 — Evaluation-structure replacement

v7:
```
11_audit.json — process audit (real_websearches counts, arxiv validity)
```

v8:
```
11_qrubric.json — three-level evaluation tree:
    scenarios (1-3 active per round) →
    perspectives (4 per scenario: P_prior_art, P_obfuscation, P_composition, P_evidence) →
    criteria (2-3 binary checks per perspective with explicit weights)

11_audit.json — thin backward-compat index (still written)
```

Per perspective: `P_score = Σ C_i.weight × C_i.fired`. Per scenario:
`S_score = mean(P_score)`. Round-level: `q_rubric_score = mean(S_score)`.
`q_rubric_verdict = ANTICIPATED if score >= 0.5 else NOVEL` — **advisory
only**, does NOT override step 10.

All criteria are **deterministic file-chain checks**, NOT fresh LLM
judgments. The Q-rubric reproduces from the file chain alone.

### Step 12 — Solution-structure replacement

v7:
```
12_verification.json — single fresh-context verifier verdict
```

v8:
```
12_tree_stream.json — helper / solver / synthesizer trace:
    helper agent (sees retrieved-paper landscape, NOT candidate) emits 4-7 hints
    solver agent (clean context, NOT landscape) answers each hint via 1 web_search
    synthesizer composes verdict from per-hint trace

12_verification.json — thin backward-compat index (still written)
```

Conservative synthesis:
```
verdict_tree_stream = PASS  if ALL per_hint_verdict ∈ {not_anticipated, inconclusive}
                            AND max per_hint_similarity < 0.7
                    = FAIL  otherwise
```

A single `anticipated` hint flips the round to FAIL — no averaging.

---

## What v8 PRESERVES VERBATIM (★ FORBIDDEN-TO-MODIFY)

| Zone | v5 | v6 | v7 | v8 |
|---|---|---|---|---|
| Step 06 web_search | ★ FROZEN | ★ FROZEN | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 07 keyword threshold ≥ 2 | ★ FROZEN | ★ FROZEN | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 10 mechanical verdict | ★ FROZEN | DIVERTED via 06.8 | ★ FROZEN (RESTORED) | ★ FROZEN (UNCHANGED) |
| Step 11.5 adversarial external | n/a | n/a | ★ FROZEN (NEW v7) | ★ FROZEN (UNCHANGED, consumes pre-stripped sample_tokens) |

The user-explicit FORBIDDEN list for E27:
- step 06 web_search → preserved
- step 07 keyword threshold ≥ 2 → preserved
- step 10 mechanical verdict → preserved

Step 11.5 (v7) is also frozen in v8 but consumes
`05_sample_tokens.stripped_llm_application` directly (the pre-stripped
text from step 05) rather than stripping on-the-fly from
`05_candidate.llm_application`. The skeptical-reviewer behavior is
identical.

---

## What v8 REMOVES

- **v7 monolithic `05_candidate.json`** (as the canonical source).
  Replaced by three token-stream files; the thin v8 index file remains
  for backward compatibility.
- **v7 monolithic step 12 verifier**. Replaced by helper / solver /
  synthesizer trace.
- **v7 monolithic step 11 audit-as-process-check**. Replaced by Q-rubric
  evaluation tree.

v8 does NOT remove step 11.5 (v7's contribution). v8 does NOT
re-introduce step 06.8 (v6's deprecated layer).

---

## Scoring formula change

```
v7: score_v7 = (confirmed_substantive_pass × 10)
             + (25 − mean_forced_hit)
             + (disagreement_rate × 5)
             − (false_positive_count × 5)
             − (adversarial_hit_count × 10)

v8: score_v8 = (confirmed_substantive_pass × 10)
             + (25 − mean_forced_hit)
             + (tree_stream_step_10_alignment_rate × 5)        ← was disagreement_rate
             − (false_positive_count × 5)
             − (adversarial_hit_count × 10)
             + (qrubric_step_10_alignment_rate × 3)            ← NEW v8
             + (mean_hints_per_round / 7 × 2)                  ← NEW v8
```

The disagreement-rate term flips polarity: under v8, ALIGNMENT between
tree-stream and step 10 is rewarded (since tree-stream is the v5
verifier's decomposed replacement, alignment shows the decomposition
is faithful). Under v7, DISAGREEMENT was rewarded (because the v5
verifier used a different rubric on purpose). The polarity flip
reflects that v8 tree-stream is engineered for FIDELITY to step 10,
whereas v7's verifier was engineered for ORTHOGONALITY.

`confirmed_substantive_pass` under v8 requires ALL of:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- tree_stream verdict = PASS (all solver hints NOT anticipated, max sim < 0.7), AND
- q_rubric_verdict = NOVEL (q_rubric_score < 0.5), AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7.

Strictly more demanding than v7. Six independent signals must align.

---

## Calibration evidence (predicted)

### R577 BEKTASHI under v8 (retrospective)

- `05_prompt_tokens.json`: source_domain_family = "Sufi-Turkish-Bektashi";
  metaphor_or_mechanism = "metaphor_only".
- `05_sample_tokens.json`: stripped_llm_application = "phase-coherence
  mechanism with K-canonical sequence ordering + K per-element frozen
  soft-prompts + K-phase round-robin scheduler + master-student lineage
  weight-delta along K prompt directions + cross-finetune prompt-direction
  drift regularizer" (12-imam, dhikr, muršid, zarif all stripped at
  construction).
- Step 10: 8/8 keyword hits → FAIL.
- Step 11 Q-rubric: P_prior_art fires C1+C2+C3 = 1.0; P_obfuscation fires
  via metaphor_only flag; q_rubric_score = ~0.85, q_rubric_verdict =
  ANTICIPATED, aligned with step 10.
- Step 12 tree-stream: SKIPPED (step 10 FAIL would NOT skip step 12
  — they run in parallel — but the verdict synthesizer sees step 10 FAIL
  and reports FAIL anyway). Helper would issue hints, solver would find
  HARPE on hint H_A.
- Step 11.5: SKIPPED (step 10 FAIL gate, identical to v7).
- v8_verdict: FAIL — caught at step 10 like v7.

### R279 PTCH under v8 (retrospective)

- Step 10: PASS (was UNCERTAIN in v5 audit, then FAIL_ADVERSARIAL in v7
  E25 step 11.5).
- Step 11 Q-rubric: P_prior_art fires partial; q_rubric_score ~0.4-0.5
  borderline; q_rubric_verdict probably NOVEL but close to ANTICIPATED.
- Step 12 tree-stream: helper sees retrieved paper landscape (SVFT,
  SORSA, CLoRA cluster), emits hints including HINT_FAMILY_A
  prior-art-coverage. Solver, given stripped PTCH application, runs
  per-hint web_searches and surfaces the same papers v7 step 11.5
  found. tree_stream_verdict = FAIL on per_hint_similarity ≥ 0.7
  (SORSA at 0.80).
- v8_verdict: FAIL — caught at step 12 tree-stream BEFORE step 11.5
  fires (because step 12 PASS is no longer guaranteed by the v5
  Pattern-E divergence — tree-stream is engineered to ALIGN with the
  mechanical FAIL signal).

The v8 tree-stream is engineered to catch what v7's verifier missed
on R279: a candidate whose mechanical step 10 PASSes (0 keyword hits)
but whose decomposed orthogonal hints surface prior art the original
v5 verifier did not weight heavily.

---

## Migration plan

- R651-R675 runs under v8 in epoch 27.
- v7 rounds (R601-R650) NOT retroactively re-run under v8. They are
  retained as v7 forensic record.
- memory_db.json updated with v8 fields per round in epoch 27.
- stats_round_675.json adds v8 problem / solution / evaluation metrics.

---

## What v8 explicitly does NOT promise

- v8 does NOT promise more substantive PASS verdicts. The saturation
  is structural.
- v8 does NOT promise 0 false positives. Time-lag false positives
  remain possible.
- v8 does NOT re-litigate the 746-round 0-substantive-PASS corpus
  statistic. The mining-distribution claim — that p ≈ 0 on 1%-novelty
  H₀ at N=746 — stands. v8's contribution is audit-tractability, not
  yield.
- v8 does NOT re-introduce step 06.8 or any v6 layer.
- v8 does NOT modify the four FORBIDDEN zones (step 06 web_search,
  step 07 keyword threshold, step 10 mechanical verdict) or the v7
  step 11.5 adversarial external verification.
