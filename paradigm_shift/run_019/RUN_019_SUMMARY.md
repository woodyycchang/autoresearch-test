# Run 19 — persistent param file + sentence decomposition (epoch 1 baseline)

Merges **Run 16** (persistent `direction_params.json` + label-driven param nudging
across epochs) with **Run 18** (sentence-level decomposition of verbatim abstracts +
per-atom saturation + sparsest cross-paper pairing), on the **Run 17** transparency
layer. Branch `claude/run-19`, stacked on `claude/run-18`. Run 16's 4 gates inherited
UNCHANGED.

**Convergence target = SEARCH QUALITY (label-driven, has ground truth), NOT
"find a niche" (degenerate reward).** Both metrics and the niche verdict are reported
SEPARATELY and honestly (R12).

## Epoch 1 baseline (the three numbers, reported separately)

| metric | epoch 1 | delta vs prev |
|---|---|---|
| **avg_search_quality** (convergence target) | **0.7983** | — (baseline) |
| **avg_paper_hits** (niche saturation) | **21.0** | — (baseline) |
| **niche verdict** | **NICHE_NOT_FOUND (0/5)** | — |

`avg_search_quality = sum_k(param_k · mean_dim_k)/sum_k(param_k)` over **43 real
queries**, params all 0.5 (neutral baseline). Dimension means: specificity **0.99**,
mechanism_focus **0.95**, cross_paper_pairing **0.90**, sparsity_seeking **0.71**,
collision_avoidance **0.44**. The low `collision_avoidance` (few queries used
prior-art-probe phrasing) is the clearest headroom for the label-driven loop to lift.

## The persistent convergence loop is now live (R10)
- `direction_params.json` written: **epoch 1 → 2**, `epoch_history` records epoch 1
  (avg_search_quality 0.7983, avg_paper_hits 21.0, params snapshot).
- `queries_to_label.json` emitted: **43 queries** each with their 5 dimension scores
  and a `label` slot. **Your turn:** mark each `on_target` or `diverge`, paste into
  `direction_params.json.labeled_examples`, then epoch 2's `apply_labels` will nudge
  the params toward the on_target profile (lr 0.2, clamped [0.05,0.95]) and we measure
  whether avg_search_quality rises.
- The nudge is the proven Run 16 machinery (label-driven, deterministic, no labels ⇒
  no change — which is why epoch 1 params stayed 0.5).

## Niche track (secondary, R12): saturation holds, CAND_003 is the closest call ever
3 verbatim abstracts → 10 sentence-level atoms (8 mechanism + 2 context) → 5 sparsest
cross-paper merges → verify + crosscheck → 4 gates.

| cand | fused niche | atoms (hits) | verify hits | composite | gates |
|---|---|---|---|---|---|
| 001 | Fisher-Rao annealing of continuous routing entropy | P1_S3(3)×P2_S2(3) | 26 | 0.45 | 0**1**11 |
| 002 | Thermodynamic concentration-controlled MoE routing | P1_S3(3)×P3_S1(3) | 20 | 0.45 | 0**1**11 |
| 003 | Fisher-Rao annealing for thermodynamic sampling hardware | P2_S2(3)×P3_S1(3) | 24 | 0.25 | 0**1**1**0** |
| 004 | Fisher-Rao concentration scheduling for Grassmannian MoE | P1_S2(4)×P2_S2(3) | 16 | **0.56** | 0**1**11 |
| 005 | Thermodynamic sampling of Grassmannian Bingham gates | P1_S2(4)×P3_S1(3) | 19 | 0.2775 | 0**1**1**0** |

All fail Gate 1 (novelty floored by prior-art volume); CAND_003 & 005 also fail Gate 4
(mechanism lacks a Belinda causal verb — honest, not massaged). **CAND_019_003 is the
lowest-margin candidate of Runs 17–19:** the Sivak–Crooks *thermodynamic length* result
already establishes that optimal annealing schedules are friction-tensor
(Fisher-information-metric) geodesics — so "Fisher-Rao-optimal annealing schedule for a
thermodynamic process" is essentially a *known principle*; only the narrow
sampling-*hardware* application is unclaimed. We record `collision_found=false` at the
strict fused-niche level but flag that its novelty is genuinely low **on principle**, a
reviewer could reasonably call it a collision. (AGENT 4 verify + independent crosscheck
both reached this, 0 mismatches.)

## Transparency scorecard
- **61/61** traces complete · **0 logic-breaks** · determinism OK · real-Opus
  anti-hallucination **0 mismatches** · proofs **11/11** · offline tests **9/9**
- 32 non-fatal flags (terse verifier-reformulation confidence + grounding heuristics on
  short decisions) — same honest character as Runs 17–18.

## Honest caveats (disclosed)
- **R12 anti-degeneracy:** we converge toward `avg_search_quality` (which has ground
  truth via your labels), NOT toward niche-finding (which would reward a degenerate "call
  everything novel" policy). Niche saturation (0 survivors) is the expected, honest
  outcome and is NOT treated as failure.
- **Corpus reuse:** epoch 1 reuses Run 18's 3-paper corpus (abstracts re-sourced fresh
  this run) so future epochs isolate the *param* effect; the convergence target is the
  quality of the *queries*, not the papers.
- **Single-search cap:** per-atom hits (1–5) are capped; the comparable volume figure is
  the per-candidate 5-reformulation count (avg 21.0).
- **AGENT 5 rule-based by design** (an LLM auditor would reintroduce a black box).

## Artifacts (branch `claude/run-19`)
- `direction_params.json` (PERSISTENT, now epoch 2 with epoch_history) ·
  `queries_to_label.json` (43 queries for your labels) ·
  `REASONING_TRANSPARENCY_REPORT.md` · `sparse_analysis.json`
- `logs/`: atoms(+reasoning), atom_search, candidates(+merge envelopes),
  verify(+reasoning), crosscheck, reasoning_audit, **search_quality**, report_log
  ([REPORT 1-6]), gate_results, determinism_check, hallucination_check, summary_llm
- `niche_find_check.json` · `proof_scorecard.json` (11/11)
- `run19_merge.py` · `run19_audit.py` · `run19_orchestrator.py` · `test_run19.py` (9 tests)

## Next epoch (when you've labeled)
1. Paste labeled queries into `direction_params.json.labeled_examples`.
2. `python3 paradigm_shift/run19_orchestrator.py apply_labels` (nudges params).
3. Re-run AGENT 1–5 + MAIN → compare epoch-2 `avg_search_quality` to 0.7983.
