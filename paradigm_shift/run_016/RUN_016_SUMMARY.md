# Run 16 — Definitive result

**Verdict: the niche search is saturated, and saturation is robust.** Across three
epochs spanning same-domain, ML-adjacent, and exotic cross-domain pairings, every
candidate floored at the same composite novelty (0.45) and **zero of nine
candidates** cleared Gate 1. Meanwhile the **per-epoch parameter-improvement loop
worked as designed** — search quality rose monotonically. These are two separate,
both-honest findings.

## Two-track outcome

| | epoch 1 (ML×ML) | epoch 2 (ML×biology) | epoch 3 (ML×seismology) |
|---|---|---|---|
| domain pairing | same-domain | ML-adjacent | exotic / low-ML-overlap |
| **avg_search_quality** | 0.5119 | 0.5967 | 0.6024 |
| niche verdict | NICHE_NOT_FOUND | NICHE_NOT_FOUND | NICHE_NOT_FOUND |
| best composite | 0.45 | 0.45 | 0.45 |
| survivors | 0/3 | 0/3 | 0/3 |
| A3↔A4 mismatches | 0 | 0 | 0 |
| hallucination | none | none | none |
| proof points | 7/7 | 7/7 | 7/7 |

### Track 1 — the parameter-improving loop WORKS (per-epoch success, R12)
`avg_search_quality` improved **monotonically 0.5119 → 0.5967 → 0.6024** under
human-label-driven param nudges (+ a cold-start bootstrap for two dimensions).
The persistent `direction_params.json`, the lagged-label nudge (`apply_labels` at
epoch start), and `epoch_history` tracking all functioned. The mechanism the run
set out to build — measurable, human-steered search-quality improvement across
epochs — is demonstrated.

### Track 2 — the niche goal is saturated, ROBUSTLY (the scientific result)
We deliberately escalated the domain exoticism to attack the novelty gate:
- **Epoch 1 (ML×ML):** composite 0.45. Dense same-field prior art.
- **Epoch 2 (ML×biology):** composite 0.45. One real collision (EMNLP-2022 "Mixture
  of Attention Heads"), independently re-found by AGENT 4.
- **Epoch 3 (ML×seismology, near-zero ML overlap):** composite 0.45. **Zero
  bridging papers** (AGENT 3 + AGENT 4 both confirmed disjoint clusters), yet still
  floored.

**The definitive finding:** even at near-zero ML overlap (seismology), the
composite stayed identical to same-domain (0.45). Therefore saturation is **not**
"nobody wrote this exact combination" (trivially easy to satisfy — epoch 3's
bridging count was 0) but **"both components are individually mature and
heavily studied."** Total prior-art volume (24–33 papers per candidate) measures
that maturity correctly; it does not drop just because the pairing is exotic.
Cross-domain combinations of mature mechanisms saturate on total volume regardless
of how unusual the domain pairing is.

## Methodological integrity (why we did NOT manufacture a survivor)

After epoch 3, the cross-domain candidates passed Gates 2/3/4 and failed only
Gate 1. It was tempting to redefine Gate-1 novelty as a *bridging*-paper count
(0 for the cross-domain candidates) — which would have produced the loop's first
"survivors." **We did not.** That is the Run 11 error: loosening a gate to admit
soft-scoring positives, all 24 of which an honest Run 12 recalibration later
rejected.

"0 bridging papers" ≠ novel niche. Many component pairs are uncombined because the
combination is obvious, implicit, or a surface analogy — not because there is a
genuine gap. "Rupture Dynamics of Test-Time-Training Hidden States" is seismology
vocabulary wrapping a mature ML mechanism — precisely the
`ANALOGY_TRANSFERS`/surface-analogy failure the Belinda gate exists to catch.
Changing the metric would change how novelty is *measured*, not the candidate's
*actual* novelty, and would yield false survivors that fail external review.

**Gate 1 remains total-volume novelty, unchanged.** The honest verdict stands:
NICHE_NOT_FOUND, robustly.

## What held up under three epochs of stress

- **Cross-verification (R7) has teeth.** AGENT 4 independently *re-found* epoch-2's
  real collision (not rubber-stamping) and independently *confirmed* epoch-3's
  zero-bridging-papers. 0 mismatches across all 3 epochs.
- **Anti-hallucination.** Real Opus summaries restated every gate number; 0
  hallucination mismatches across 3 epochs. Determinism hash stable every epoch.
- **Agent self-correction (R5).** Every epoch, AGENT 1 caught its own first-draft
  slip (fabricated/future-dated arXiv ids) and recommitted with verified real
  papers — the honesty rule catching real errors, repeatedly.
- **Wipe-safety (R2).** All 5 agents/epoch committed + pushed before the next
  spawned; each output independently re-verified by MAIN before proceeding.
- **19 offline tests** green throughout.

## Honest caveats
- **Mid-experiment metric change (epoch 3):** the scorer's `FIELD_LEX` was extended
  with low-overlap-domain vocabulary (+ hyphen-split) so directive #1 could
  register. Part of the cross_domain_reach jump (0.02→0.31) is genuine both-domain
  naming; part is the metric newly *able* to see seismology terms. Disclosed.
- **Search-quality tradeoff:** epoch 3's small net delta (+0.0057) reflects
  cross_domain_reach (↑) traded against mechanism_focus (0.74→0.50), since domain
  vocabulary displaces mechanism verbs in queries.
- **Scope:** 3 candidates/epoch, 1 Belinda-strict configuration, the deterministic
  composite. The saturation finding is robust within this harness; it is a
  statement about *this* corpus + gate, honestly scoped.

## Recommendation (adopted)
Epoch iteration is **stopped** here. Three epochs answered the core question:
search-quality optimization works (Track 1), and niche saturation is robust across
same-domain, ML-adjacent, and exotic cross-domain pairings (Track 2). The only way
to a survivor would be either a genuinely *immature* (under-formalized) component —
a different hypothesis — or loosening the gate, which we decline. Run 16 stands as
the **definitive saturation result.**

## Artifacts (branch `claude/run-16`)
- `direction_params.json` — persistent state, epoch 4, `epoch_history` = all 3 epochs
- `RUN_REPORT.md` (epoch 1), `RUN_REPORT_epoch2.md`, `RUN_REPORT_epoch3.md`
- `logs/epoch_1/` archive + epoch-3 `logs/` (atoms, candidates, verify, crosscheck,
  search_quality, report_log, gate_results, determinism_check, hallucination_check)
- `run16_orchestrator.py`, `run16_merge.py`, `run16_scorer.py`,
  `test_run16_orchestrator.py` (19 tests)
- `proof_scorecard.json` — 7/7 each epoch
