# R276 — life analogy

## Source domain: Moai rocking transport (Easter Island walking statues)
- 10-ton stone statue with broad D-shaped base + forward lean.
- Three rope teams (left, right, behind) pull rhythmically: left team pulls → statue rocks LEFT and base PIVOTS on left edge, advancing slightly forward; right team pulls → statue rocks RIGHT pivot, advancing again; rear team prevents toppling.
- Forward motion emerges purely from LATERAL OSCILLATION around a slightly off-center COM — not by lifting or pushing forward directly.
- Energy cost: only the lateral rocking work — the forward step is FREE (gravity does the work each pivot release).

## LLM analogy candidate
**Moai-pivot oscillation optimizer (MPOO)**: an optimizer that makes forward progress on the loss landscape NOT by descending the gradient at every step, but by ALTERNATING transverse perturbations orthogonal to the gradient. The geometry: a parameter cluster (analogous to a stone block) has a forward-leaning configuration (one principal-direction has natural drift due to gradient bias). The optimizer:
- Step t: apply a transverse rocking displacement Δθ_⊥ along positive direction in the null-space-of-loss tangent plane (left pull).
- Step t+1: apply Δθ_⊥ along negative direction (right pull).
- Each pivot RELEASES the natural forward-lean drift Δθ_∥ (= forward step) without spending compute on it.
- Net: forward parameter motion costs only the transverse work; the descent step is gravity-free (lateral oscillation does ALL the work, descent is the EMERGENT geometric result).

## What differs from prior art (claim)
- HGM (2506.22479): modulates lr by cosine alignment — adjusts SCALE, not direction in lateral plane.
- Sign-based Lion / Muon: take sign of full gradient; aligned with the descent direction, not transverse.
- Nesterov momentum: lookahead in the descent direction.
- None of the surveyed optimizers explicitly perform pure-lateral-oscillation steps in directions ORTHOGONAL to the loss gradient and rely on the forward-leaning natural drift for descent — descent comes from the geometry of the parameter manifold, not from the step direction.
