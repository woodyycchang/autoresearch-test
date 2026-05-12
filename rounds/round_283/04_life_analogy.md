# R283 — life analogy

## Source domain: Andean chuño freeze-thaw-trample preservation
- Potatoes are not just dried — they're cycled:
  - NIGHT: extreme cold freezes inner cell water → ice crystals rupture cell walls.
  - DAY: warm sun thaws → ruptured cells release water + farmers TRAMPLE to physically squeeze it out.
  - REPEAT for 5 nights.
- The CYCLE is essential: a single freeze or single trample fails; the alternation between phase changes + mechanical pressure is what extracts moisture.
- Result: a dry, dense, decade-stable food product from a perishable one.

## LLM analogy concept
**FTTC (Freeze-Trample-Thaw Compression)**: a 3-phase LLM weight-compression schedule:
- Phase FREEZE: snapshot current weights, identify magnitude-outlier "ice crystals" (high-magnitude values that disproportionately drive activations).
- Phase TRAMPLE: apply a mechanical pressure step (gradient-based knowledge-distillation pass that pushes high-magnitude values toward the bulk, redistributing energy across neighbors).
- Phase THAW: relax quantization grid (let weights re-stabilize to new local optima at slightly relaxed bit-width).
- Repeat the 3-phase cycle N=5 iterations.

Distinct from one-shot PTQ + standard QAT: those don't alternate redistribution-press with grid-relax over multiple cycles.

## What differs from prior art (claim)
- AQLM (2401.06118): additive quantization — no cyclic press-relax phase structure.
- GPTVQ: interleaves column-quant with Hessian-update — adjacent (interleaving), but the press-relax of values into bulk is not its mechanism.
- PV-Tuning: alternates continuous and discrete optimization — adjacent but the mechanism is parameter-type alternation, not value-redistribution / phase-cycle.
- ARB-LLM (alternating refined binarizations) — closest in spirit; need to investigate.
- FTTC's distinguishing feature: explicit 3-phase freeze-press-relax cycle structured after a known preservation process (chuño) — and uses mechanical-pressure interpretation of distillation, not pure value-encoding alternation.
