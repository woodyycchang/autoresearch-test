# Run 19 — Epoch 4 (re-label with fixed scorer + param-shaped queries)

## Convergence trajectory (the headline)

| | epoch 1 | epoch 2 | epoch 3 | **epoch 4** |
|---|---|---|---|---|
| **avg_search_quality** | 0.7983 | 0.7981 | 0.8130 | **0.8355** |
| Δ vs prev | — | −0.0002 | +0.0149 | **+0.0225** |
| avg_paper_hits | 21.0 | 21.4 | 21.4 | 21.4 |
| niche verdict | NOT_FOUND | NOT_FOUND | NOT_FOUND | NOT_FOUND |

**search_quality is STILL CLIMBING** (Δe3→e4 = +0.0225, above the 0.005 plateau
threshold; not 2 consecutive sub-0.005 deltas → **NOT converged**). Total climb since
the baseline: **0.7983 → 0.8355 (+0.0372)**.

## PHASE 1 — re-nudge with the fixed scorer (param strengthened)
Re-ran `apply_labels` on the **same 43 labels** (unchanged), but recomputing each query's
`collision_avoidance` dim with the **epoch-3 fixed scorer**. Nudged from baseline 0.5:

| param | epoch-2 nudge | **epoch-4 nudge** | Δ |
|---|---|---|---|
| collision_avoidance_phrasing | 0.5293 | **0.5593** | **+0.0300 (STRENGTHENED)** |
| specificity | 0.5022 | 0.5022 | — |
| mechanism_focus | 0.525 | 0.525 | — |
| sparsity_seeking | 0.5408 | 0.5408 | — |
| cross_paper_pairing | 0.5463 | 0.5463 | — |

The strengthening is honest and traceable: removing `"survey"` credit (surveys = DIVERGE
per the rubric) **lowered the diverge group's collision_avoidance** (div_mean 0.35 → 0.20),
widening the on_target↔diverge gap (signal 0.146 → 0.296 → param 0.5593). `on_mean` stayed
0.4963 (the epoch-1 on_target queries were noun-phrase stacks, not gap-probe sentences).
Only `collision_avoidance` changed; the other four params' dims were untouched by the fix.

## PHASE 2 — AGENT 1 emits param-shaped queries (real WebSearch, R5)
Shaped by the strengthened params, AGENT 1 **dropped the diverge query types** (abstract
fetches, bare per-atom searches, surveys) and emitted **12 researcher-style queries** —
all gap-probes + cross-paper white-space bridges, e.g. *"has Fisher-Rao geometry been
applied to MoE routing entropy"*, *"is there any paper combining thermodynamic computing
hardware with expert routing"*, *"no prior work on kinetic proofreading applied to MoE
gating"*. Each was a real search; several confirmed genuine white space (the engine
explicitly found no thermodynamic-computing × expert-routing paper, no kinetic-proofreading
× MoE-gating paper), a few hit adjacency (Fisher-Rao × MoE = arXiv:2604.14500; thermodynamic
isomorphism of transformers = 2602.08216).

## PHASE 3 — mode: SCIENCE HELD FIXED (stated)
I held corpus/atoms/candidates/verify/paper-hits fixed (consistent with epochs 2–3) and
re-scored the new epoch-4 query set with the fixed scorer + strengthened params, to isolate
the param/query effect. avg_paper_hits stays **21.4**, verdict **NICHE_NOT_FOUND**.

## Per-dimension story (and an honest tension)
| dimension | epoch 3 | epoch 4 | Δ |
|---|---|---|---|
| **collision_avoidance** | 0.4977 | **1.0000** | **+0.5023** (all 12 are gap-probes) |
| specificity | 0.9855 | 0.8958 | −0.0897 |
| sparsity_seeking | 0.7209 | 0.5167 | −0.2042 |
| cross_paper_pairing | 0.9070 | 0.8333 | −0.0737 |
| mechanism_focus | 0.9628 | 0.9333 | −0.0295 |

**The +0.0225 net rise is driven entirely by `collision_avoidance` maxing at 1.0**
(weighted 0.5593), which overcame declines in the other four dimensions. Those declined
because gap-probe *sentences* ("has X been applied to Y", "is there any paper…") are less
keyword-dense than epoch-3's noun-phrase stacks — fewer exotic terms (↓sparsity), fewer
stacked domain keywords (↓cross_paper/specificity). **This is a real tension I'm reporting,
not hiding:** maximizing gap-probe phrasing traded off the other research dimensions, so the
metric is NOT maxed (0.8355, not its ~0.94 ceiling). A query that is *simultaneously* a
gap-probe AND a dense cross-domain bridge (e.g. *"has the Matrix-Bingham concentration
spectrum been applied to thermodynamic-sampling expert routing — unexplored"*) would score
higher on all five dims at once. That headroom is exactly why search_quality is still
climbing rather than plateaued.

## Convergence status
- Deltas: e1→e2 −0.0002, e2→e3 +0.0149, e3→e4 +0.0225.
- Stop criterion (|Δ| < 0.005 for **2 consecutive** epochs): **not met** — still climbing.
- The e1→e2 sub-0.005 delta was a buggy-scorer artifact (epoch-2 report), not real
  convergence; the real loop has risen every epoch since the scorer was fixed.
- **Continue:** next epoch should optimize the JOINT objective (gap-probe AND dense
  cross-domain), which should lift the traded-off dims back up while keeping
  collision_avoidance high — likely pushing toward the ~0.9 region before plateau.

## Honesty / no goalpost-moving
- Scorer **not re-tuned** (frozen from epoch 3 with the spec'd GAP_PATTERNS).
- Niche **gates unchanged**; **labels unchanged** (same 43); only the params were
  re-nudged (as the task asked) and the query set re-shaped.
- The rise mechanism is documented transparently above (collision_avoidance maxing,
  other dims trading off) — it is the RLHF-style alignment loop working
  (rubric → params → behaviour), not a manufactured number.
- avg_paper_hits + verdict unchanged: search behaviour improved; niche saturation
  (corpus-determined) correctly did not (R12).
- Determinism: `score_query` pure; re-score reproducible.

## Persistent state
`direction_params.json`: epoch 4 → 5; params carry collision_avoidance 0.5593;
`epoch_history` = [(1, 0.7983, 21.0), (2, 0.7981, 21.4), (3, 0.8130, 21.4), (4, 0.8355, 21.4)].
