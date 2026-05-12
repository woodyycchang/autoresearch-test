# R314 — life analogy

## Source: Planktonic foraminifera carbonate sequestration
- Single-cell foraminifera build calcite (CaCO₃) shells (tests) from seawater carbonate ions.
- Upon death, shells sink to deep ocean floor, sequestering carbon for geological timescales.
- 25-50% of pelagic carbonate export flux is via forams; biological carbon pump.

## LLM analogy
**FORAM-ACC**: gradient sequestration training. Each mini-batch's gradient is treated as a "calcite shell" deposited into a sequestration buffer (parameter delta tensor) rather than immediately applied to weights. Every N steps a "shell death" event sinks the accumulated sequestration buffer into the parameter weights and freezes the affected layer, removing it from further gradient updates. Result: progressive layer freezing through bottom-up gradient sediment accumulation.

## Differs from prior art (claim)
Standard gradient accumulation merges into a single update. Layer freezing schedules are explicit per-layer. Progressive freezing methods exist. FORAM-ACC differs by tying freezing to GRADIENT-SEDIMENT volume — but the underlying mechanism is essentially staged gradient accumulation with progressive layer freezing, which is well-studied.
