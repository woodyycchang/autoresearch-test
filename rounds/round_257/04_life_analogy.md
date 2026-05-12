# R257 — life analogy

## Source domain: barchan sand dune migration
- Crescent-shaped dune; convex windward face, concave horns trailing downwind.
- **Mass-dependent migration rate**: dune migration rate ∝ 1 / dune height (because reconstitution time grows with the volume of sand to move).
- **Centerline is slowest, horns are fastest** — the dune does not migrate rigidly; the shape EMERGES from differential migration speeds along the crest.
- **Saltation threshold**: wind must exceed ~4-7 m/s to mobilize grains; below threshold the dune is static.
- Equilibrium shape (the crescent) is the steady-state of differential migration under uniform wind.

## LLM analogy candidate
**Differential-mobility curvature-shape stable training (DMCS)**: model parameter-update mobility as **mass-dependent** at the per-coordinate level. Each parameter coordinate has a learned effective "height" h_i (a slow EMA of |w_i| × |∇L w_i|); the per-coordinate effective LR is η_i = η_base / (1 + α·h_i), so heavily-utilized "centerline" coordinates migrate slowly while lightly-used "horn" coordinates migrate faster. Under a fixed gradient direction (analogue of uniform wind), the parameter "shape" reaches a steady-state crescent: heavy centerline coordinates stay nearly locked, peripheral coordinates redistribute. Crucially: add a **saltation-threshold gate** — coordinates with current gradient magnitude below τ are NOT updated at all (analogue of wind below saltation threshold). The steady state is a self-organized crescent of slow-moving important parameters + fast-moving peripheral parameters, with explicit threshold floor.

## What differs from prior art (claim)
SP large-LR (2505.22491) and muP literature are about WIDTH-scaled LR, not per-coordinate mass-dependent. Weight decay > muP (2510.19093) stabilizes via decay, not per-coordinate effective-height. Scaling with Collapse (2509.25087) is loss-curve cross-scale collapse. None retrieve a per-coordinate mass-and-threshold-gated mobility that produces a self-organized crescent in parameter space.
