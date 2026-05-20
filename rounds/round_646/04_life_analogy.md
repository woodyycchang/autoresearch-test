# R646 step 04 — Bellman residual

Bellman optimality: Q*(s,a) = r(s,a) + γ E[max_{a'} Q*(s',a')]. Residual R(Q) = TD error magnitude.

### Mechanism transfer
Adversarial coevolution: red-team Q_R, aligned Q_A. Compute per-agent Bellman residual ‖T Q_a - Q_a‖. Constraint: gap |R(Q_R) - R(Q_A)| ≤ τ; if exceeded, shrink learning rate of the dominant agent. Coupling rule keeps both agents at similar sub-optimality.

mechanism_transfer: Bellman residual is closed-form per agent.
