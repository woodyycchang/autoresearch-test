# R627 step 04 source-domain mechanism

## Source: Hamiltonian mechanics / symplectic integration

### Core math
A Hamiltonian system has phase variables (q,p) and dynamics:
- dq/dt = ∂H/∂p
- dp/dt = -∂H/∂q

Symplectic integrators (e.g., leapfrog, Yoshida, Stormer-Verlet) preserve the symplectic 2-form ω = dq ∧ dp, which implies long-term bounded energy drift even with finite step size.

### Why mechanism-level (not metaphor)
SGD with momentum literally IS a discrete-time integrator of a Hamiltonian system: H(θ,p) = L(θ) + ||p||²/(2β). Standard Polyak momentum is a forward-Euler integrator (NOT symplectic) with linear-rate energy growth. Symplectic SGD (Maddison et al. 2018; Hamiltonian Descent 2018) uses time-reversible updates that preserve volume.

The candidate proposes using a STORMER-VERLET LEAPFROG step with explicit ENERGY-CONSERVATION RESIDUAL r_t = |H_t - H_0| < ε as a fine-tuning constraint. When r_t exceeds threshold, an energy-rebalancing kick is applied to project back onto the constant-H manifold.

### Structural map
- (q, p) classical phase ↔ (θ, momentum) optimizer state
- H(q,p) classical Hamiltonian ↔ L(θ) + ‖p‖²/2β
- Symplectic 2-form preservation ↔ Optimizer phase-space-volume conservation
- Time-reversibility ↔ Optimizer trajectory reproducibility under reverse step

Direct mechanism transfer.
