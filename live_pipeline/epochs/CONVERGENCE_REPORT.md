# Multi-Epoch Convergence Report (epochs 1–3)

**Stop reason:** metric plateau reached + parameter changes decelerating to near-zero
+ no VIABLE niche (3/3 epochs SEED-or-below) + session/context limit (R13, resumable).
The loop did NOT find a VIABLE niche and did NOT formally tick "param-L1 ≈ 0 for 2
consecutive epochs" (it is one epoch short) — but it reached **metric plateau**, the
substantive half of convergence.

## Per-epoch trajectory

| Epoch | Concepts | Funnel | Survivor | Tier | Terminal | Fab |
|---|---|---|---|---|---|---|
| 1 (cycle 1) | 18 (academic — pre-R11 error) | 18→3→1 | GridFermi-PE | MODEST | CONFIRMED_W_CAVEATS (no gate) | 0 |
| 2 (cycle 2) | 36 (R11 ML×life) | 8→5→1 | LoadTightening AutoTTS | MODEST | SEED_ONLY | 0 |
| 3 | 15 (whitespace+distinct+load-bearing) | 4→1 | Vickrey-Fréchet Merge | MODEST | SEED_ONLY | 0 |

## Metric plateau (the substantive convergence signal)

Across 3 epochs and large parameter changes, the **output distribution is invariant**:
exactly **1 marginal MODEST/SEED survivor per epoch, 0 fabrication**, dominant drop
reason stable (`reduces-to-existing-named-ML-method`), terminal verdict stable
(`SEED_ONLY`). The algorithm's *behavior* has converged.

## Parameter-change trajectory (decelerating)

- epoch 1→2: **LARGE** (~6 structural: EV gate, Stage 7, R11 breadth, analogy-collapse probe, tie-break)
- epoch 2→3: **LARGE** (~6: whitespace steering, distinct-concept, load-bearing-life check, deep-prior-art, tiebreak-rederivation, citation-sweep)
- epoch 3→4: **SMALL** (1 minor: ML-distinct-technique; tie-break demoted to diagnostic)

The big structural fixes are done; remaining changes are minor tuning → converging.

## Did the epoch-3 fixes work? (measured)

- **ML-whitespace steering → WORKED**: fetched genuinely less-saturated areas (unlearning, model-merging, conformal, causal-tabular, recommender-GNN, interpretable-forecasting).
- **distinct-life-concept-per-merge → FIXED the leak**: 4/4 distinct concepts (vs cycle-2's 5/24).
- **load-bearing-life check → WORKED**: cleanly flagged decorative axes (falconry, glassblowing) and produced a survivor that is load-bearing on both covers — directly fixing cycle-2's "Kigumi-decorative" critique.
- **tie-break → demoted to diagnostic** (cycle-2 net-wash confirmed): disagreements resolved conservatively, no output change, lower cost.

## The structural finding (the real production-ready conclusion)

ML-whitespace steering changed **which** prior art merges collide with, but **not the
mortality**: model-merging, unlearning, etc. are *themselves* crowded, so 3 of 4 merges
still reduced to existing methods. **"Whitespace" is relative and moving** — any active
ML subarea accumulates prior art faster than the pipeline can find a gap. Even the one
clean, load-bearing, no-precedent survivor (Vickrey-Fréchet) failed viability because the
transferred mechanism was *logically inverted* for its target.

**Implication:** the "newest-ML × life-concept" framing has a **near-zero VIABLE rate by
construction** — the newest-ML side is always already contested. The honest, converged
conclusion: the **process is sound, fabrication-free, and self-correcting**, but genuine
VIABLE niches via this framing are vanishingly rare (consistent with the predecessor's
0-PASS-in-1071 lineage). The main **untested lever** is a framing pivot: ML technique
applied to a *new problem a life concept reveals*, rather than improving an existing
recent ML method.

## Resumption (R13)

`direction_params.json` (epoch-4 params + convergence block) and `traversed.json`
(epochs 1–3 dedup) are committed to `main`. The next invocation resumes the loop at
epoch 4 with the updated params; one more low-Δ epoch would formally confirm the
"2 consecutive near-zero" criterion.
