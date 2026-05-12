# R334 — life analogy

## Source: Stomatopod saddle elastic-loaded hammer
- Mantis shrimp delivers 23 m/s strike (water-piston punch).
- Muscle slowly loads saddle spring quasi-statically over many ms.
- Mineralized outer + chitin/protein inner bilayer stores elastic energy.
- Release: stored energy converts to kinetic at strike-time; muscle bypassed during strike.

## LLM analogy
**SADDLE-PRE-WARM**: training method where a small "preload" phase quasi-statically accumulates gradient information in a special SPRING parameter group (frozen high-LR adapter) before any update is applied to the main weights. After preload, the spring is released — its accumulated update is APPLIED at high amplitude in a single fast step to main weights — and reset. Repeated cyclically. Different from standard accumulation: spring weights are a SEPARATE parameter group with bi-layer structure (slow-load layer + fast-release layer), not just a gradient buffer.

## Differs from prior art (claim)
Gradient accumulation aggregates micro-batch gradients before a single optimizer step. WSD has separate warmup/stable/decay phases at LR-schedule level. Optimizer momentum stores past gradient direction. SADDLE-PRE-WARM differs by introducing a PARAMETER-GROUP STRUCTURE that physically (in parameter space) separates the slow-load reservoir from the fast-release applicator, with cyclic preload→release→reset cadence.
