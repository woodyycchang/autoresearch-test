# Life Analogy — Inuksuk (stacked-stone Arctic landmark)

**Inuksuk** (Inuit cairn navigation marker):
- Stones stacked WITHOUT cement; structural balance does the work.
- 3 type variants: nalunaikkutaq (single upright "deconfuser"), tikkuuti (triangular/linear "pointer"), inunnguaq (human-figure).
- Encodes practical information: depth of snow, safety of crossing, location of food cache, direction to village/North Star.
- Some have a "viewing window" through which one can see the NEXT inuksuk along a route — chained navigation.

The unique principle: **physical-balance-maintained spatial marker that encodes route + condition info via geometric type** — the mere geometry of the stack carries semantic content. The 3-type taxonomy (single/pointer/figure) classifies the kind of information being conveyed. Chained inuksuk enable a route to be traversed by sight-line-to-next.

## Analogical mapping → LLM evaluation-diagnostic via geometric stack output

- Single upright stone (nalunaikkutaq, "I am here, you are here") ↔ a single-token diagnostic confirming the model is on-task
- Triangular pointer (tikkuuti) ↔ a 2-3 token DIRECTIONAL diagnostic indicating which way to next-step
- Human-figure (inunnguaq) ↔ a multi-token full-output diagnostic resembling target behavior
- Chained sight-line ↔ a sequence of diagnostic outputs each predicting the next eval-checkpoint

The mechanism: **INUKSUK 3-TYPE geometric output-diagnostic ladder** — define 3 graded eval primitives: (1) NALUNAIKKUTAQ: single-token Y/N "I'm on the task" — cheapest diagnostic, can be run on every step. (2) TIKKUUTI: 2-3 token "next-step direction" — moderate cost, run every ~10 steps to verify trajectory. (3) INUNNGUAQ: full output sample, expensive, run only at sample-completion or major checkpoints. The eval-diagnostic ladder uses GEOMETRIC COMPLEXITY (1→3→N tokens) as PROXY FOR DIAGNOSTIC DEPTH. Chain: at each level, the upper level's pass implies lower-level checks (lower level outputs can be derived from inunnguaq output). Differs from (a) per-token entropy (single-dim), (b) HELM multi-axis (no chain), (c) PRAYER-FLAG 5-axis (this batch — different axes not graded levels), (d) test-time compute scaling (compute amount not diagnostic type) by combining (i) 3-level GRADED diagnostic primitives + (ii) GEOMETRIC TOKEN-COUNT complexity + (iii) CHAIN-IMPLIES across levels.

## Note on adjacency

The evaluation-diagnostic form fits. Adjacent: PRAYER-FLAG (5-axis, this batch), HELM (multi-axis), test-time compute scaling. Distinct: 3-LEVEL graded geometric ladder with chain-implication.
