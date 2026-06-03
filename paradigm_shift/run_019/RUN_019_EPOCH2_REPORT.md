# Run 19 — Epoch 2 (research-skill labels → param nudge → convergence test)

## Headline (reported honestly, R12)

| metric | epoch 1 | epoch 2 | delta |
|---|---|---|---|
| **avg_search_quality** (convergence target) | 0.7983 | **0.7981** | **−0.0002 (FLAT)** |
| **avg_paper_hits** (niche saturation) | 21.0 | 21.4 | +0.4 (flat — saturation holds) |
| **niche verdict** | NICHE_NOT_FOUND | NICHE_NOT_FOUND | unchanged |

**Teaching the pipeline to "search like a researcher" did NOT raise the search_quality
metric.** The label→param loop worked mechanically and correctly; the metric stayed
flat for a specific, instructive reason (below). This is a real negative result,
reported as-is — not massaged into a win.

## What worked: the label → param loop (mechanically sound)
43 queries were labeled by the **research-skill rubric** (Swales "occupy the niche":
does the query probe white space / seek a gap / transfer a mechanism across domains?),
**on_target=27, diverge=16**. `apply_labels` nudged all 5 params toward the rubric:

| param | 0.5 → | Δ | rubric signal |
|---|---|---|---|
| cross_paper_pairing | 0.5463 | +0.046 | white-space between disjoint clusters (rewarded most) |
| sparsity_seeking | 0.5408 | +0.041 | target specific/rare mechanisms |
| collision_avoidance_phrasing | 0.5293 | +0.029 | gap-seeking |
| mechanism_focus | 0.525 | +0.025 | name a concrete mechanism |
| specificity | 0.5022 | +0.002 | query-writing quality (correctly NOT rewarded) |

And epoch 2's researcher-style query set DID move the rewarded dimension means in the
right direction:

| dimension | epoch 1 | epoch 2 | Δ |
|---|---|---|---|
| cross_paper_pairing | 0.8953 | 0.9070 | **+0.0117** ↑ |
| sparsity_seeking | 0.7093 | 0.7209 | **+0.0116** ↑ |
| mechanism_focus | 0.9535 | 0.9628 | **+0.0093** ↑ |
| specificity | 0.9913 | 0.9855 | −0.0058 |
| **collision_avoidance** | 0.4419 | **0.4233** | **−0.0186** ↓ |

## Why search_quality stayed flat: a scorer ↔ rubric MISALIGNMENT (the real finding)

Two effects canceled:
1. **The nudge shifted weight toward `collision_avoidance`** (param 0.5→0.529), a
   dimension whose mean is low (~0.44) — reweighting toward a low-mean dimension pulls
   the weighted average DOWN.
2. **The `collision_avoidance` scorer has a lexical blind spot.** It credits *literal*
   prior-art phrases — its keyword list is `["prior work","already studied","survey",
   "published","existing","prior art","already"]`. This has two perverse consequences
   under the research-skill rubric:
   - It **over-rewards "survey" queries** — which the rubric labels **DIVERGE** (they
     re-broaden to mature parent fields). Dropping the 3 survey queries in epoch 2
     therefore *removed* easy collision_avoidance points.
   - It **under-rewards semantic gap-probes** — the researcher-style queries we added
     ("**has** Fisher-Rao **been applied to** MoE routing", "**is there any paper**
     applying…", "thermodynamic computing for expert routing **unexplored**") are
     exactly gap-seeking by the rubric, yet match none of the literal phrases, so they
     scored `collision_avoidance = 0.2`.

So the behavioral improvement (more cross-domain, more gap-seeking *in meaning*)
registered on `cross_paper_pairing`/`sparsity_seeking` but was **cancelled on
`collision_avoidance`**, where the scorer can't "see" semantic gap phrasing. Net: flat.

**The convergence loop is sound; the search_quality METRIC is partly misaligned with
the human rubric.** The params now point the right way, but the scorer must be upgraded
to credit *semantic* gap-seeking before the metric can reflect researcher-style search.

## Recommended fix (NOT applied retroactively — would manufacture a win)
Upgrade the `collision_avoidance` dimension scorer to detect gap-seeking **patterns**,
and stop rewarding broad surveys:
- ADD regexes: `has .* been applied to`, `is there any (paper|work)`, `unexplored`,
  `where .* (not|n't) .* (applied|transferred)`, `no (paper|work) (on|that)`, `gap`.
- REMOVE `"survey"` from the literal list (surveys are DIVERGE per the rubric).
Then re-run epoch 3: the same researcher-style queries would score
`collision_avoidance ≈ 1.0`, lifting that dimension above the survey-driven 0.44 and
allowing avg_search_quality to rise. (Offered for the next session; not done here so
the epoch-2 number stays an honest measurement.)

## Niche track (secondary, R12)
avg_paper_hits 21.0 → 21.4 and verdict NICHE_NOT_FOUND confirm **saturation is
corpus-determined, not query-style-determined** — researcher-style searching finds the
white space more faithfully (e.g. the engine explicitly called the
thermodynamic-computing × expert-routing intersection "an unexplored area"), but the
fused niches still re-broaden to mature parent literatures. Niche staying 0 is the
honest, expected outcome — not a failure.

## Scope / honesty notes
- Science (3-paper corpus, 10 atoms, 5 candidates) held FIXED across epochs to isolate
  the param effect. The 6 queries that changed (3 sourcer abstract-fetches → cross-domain
  gap-probes; 3 verify "survey" reformulations → gap-probes) were searched FRESH this
  turn; the other 37 queries reuse this-session epoch-1 observations.
- The negative result is the deliverable: it located a concrete metric bug that the
  whole transparency program exists to surface.

## Persistent state
`direction_params.json`: epoch 2 → 3; `epoch_history` = [epoch 1 (0.7983, 21.0), epoch 2
(0.7981, 21.4)]; params carry the nudge forward.
