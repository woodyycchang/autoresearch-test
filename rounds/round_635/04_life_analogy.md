# R635 step 04 — source mechanism

## Source: Catastrophe theory (Thom; cusp)

Cusp potential V(x; a, b) = x⁴/4 + ax²/2 + bx.
Bifurcation set: 27 b² + 4 a³ = 0 (in (a,b) plane).
Inside the cusp, V has 3 equilibria (2 stable + 1 unstable); outside, only 1.
Hysteresis: trajectories crossing the cusp from different directions land on different stable branches.

### Mechanism transfer
The candidate: take (a, b) as two LLM-training control variables (e.g., a = scale of preference signal, b = mixture weight of new task in fine-tuning). Probe model behavior at points along path γ_1 and reverse path γ_2 through (a,b)-space; large hysteresis = cusp-region instability. Use as a basin-stability monitor — refuse to deploy checkpoints inside the cusp.

shared_math_structure rather than mechanism_transfer because we're not claiming SGD literally satisfies cusp ODE — only that the qualitative structure (fold bifurcation in 2D control space) matches.
