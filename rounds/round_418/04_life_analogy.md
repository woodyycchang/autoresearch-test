# Life Analogy — Bhutanese/Tibetan prayer flag (5-color cardinal stack)

**Prayer flag color stack**:
- 5 colors in STRICT ORDER: Blue, White, Red, Green, Yellow.
- Each color represents an element: sky, air, fire, water, earth.
- Each color represents a cardinal direction: N, S, E, W, Center.
- Each color represents a wisdom: compassion, sight, harmony, kindness, perfect-wisdom.
- The ORDER is meaningful — separation or rearrangement is improper.
- Each flag is a small unit; sequence of flags assembles a multi-dimensional ritual signal.

The unique principle: **fixed-ordered 5-symbol categorical scheme with multi-axis multi-meaning per symbol** — each symbol carries 3 INDEPENDENT axes of meaning (element + direction + wisdom). The PATTERN of all 5 in fixed order ENCODES the full ritual semantic; reading just one or rearranging loses information.

## Analogical mapping → 5-axis evaluation-diagnostic for LLM

- 5 colors in order ↔ 5 fixed-order evaluation axes for an LLM
- Color = element + direction + wisdom ↔ each axis = factual_accuracy + reasoning_consistency + safety
- Order significance ↔ axes are scored in a fixed dependency order (downstream axes depend on upstream pass)
- Multi-axis per symbol ↔ each axis is a 3-component sub-score
- Full sequence ↔ a compact 5-axis × 3-component multi-dimensional diagnostic vector

The mechanism: **PRAYER-FLAG 5-axis ordered evaluation-diagnostic** — for any candidate LLM, evaluate on 5 FIXED ORDERED axes (BLUE: factuality on closed-world facts; WHITE: factuality on open-world current info; RED: reasoning consistency; GREEN: safety/harmlessness; YELLOW: instruction-following / format). For each axis, report a 3-component sub-score (correctness, calibration, robustness). Total diagnostic = 5×3 = 15-d vector with PRESCRIBED ORDER for visualization. Downstream axes are scored ONLY if upstream axes pass minimum thresholds (e.g., RED reasoning is meaningful only if BLUE+WHITE factuality ≥ τ). Differs from (a) HELM (unordered, many axes), (b) MMLU (single axis), (c) Cognitive Diagnostic Models (multiple skill attributes, no order), (d) multi-dim eval GEC (5 metrics for one task, not multi-task ordered) by combining (i) FIXED-ORDERED 5 axes + (ii) MULTI-COMPONENT per axis + (iii) DEPENDENCY-CONDITIONAL downstream evaluation.

## Note on adjacency

The evaluation-diagnostic form fits. Adjacent: Cognitive Diagnostic Models (CDM, similar multi-attribute but unordered), HELM (many axes), HEIM. Distinct: FIXED-ORDER prescribed + dependency-conditional + symbolic mapping.
