# R335 — life analogy

## Source: Tree-frog toe-pad wet-conditional capillary adhesion
- Hexagonal-cell pads with mucus-filled inter-cell channels.
- Wet adhesion via capillarity + viscosity-dependent forces.
- Pad-substrate distance 0-35 nm; nanopillars 326±84 nm diameter.
- Adhesion is CONDITIONAL on wet state — pad grips only when correctly wetted; on a dry rough substrate the same pad mostly slides.

## LLM analogy
**CAPILLARY-GATE**: context-conditional attention gating where attention head firing strength is multiplied by an external context-moistness signal (e.g., a continuous estimate of context-relevance from a side-detector). When context is "dry" (low relevance), attention is weak/free-running; when context is "wet" (high relevance), attention enters strong-capillary regime with high gradient flow. Mechanism: NOT input-dependent gating per token, but per-context-window state gating.

## Differs from prior art (claim)
Gated Attention (2505.06708) gates per-head per-token via sigmoid on Q/K. Gated Linear Attention applies gating to value-stream. Standard context-aware methods (relevance scoring) use a separate retrieval model. CAPILLARY-GATE differs by introducing a CONTEXT-WINDOW-LEVEL "moistness" scalar (not per-token) that conditionally toggles attention from free-running to strong-capillary regime.
