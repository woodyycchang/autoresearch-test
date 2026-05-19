# R640 step 04 — source mechanism

## Source: Mean field game (MFG) theory (Lasry-Lions, Caines-Huang-Malhamé)

MFG: continuum of agents with state x ∈ R^d, distribution m(t,x). Each agent i optimizes:
J(i) = E[∫₀^T L(x_t^i, α_t^i, m_t) dt + Φ(x_T^i, m_T)]

Equilibrium = coupled HJB-FP system:
- HJB: -∂_t u + H(x, ∇u, m) = 0
- FP: ∂_t m + div(m ∇_p H) = 0
m = density of agents.

### Mechanism transfer
Multi-LLM-agent population: each LLM-agent π_i is a policy; m_t = empirical agent-policy distribution in some embedding space. The candidate computes a discretized MFG equilibrium policy π*(x; m) and fine-tunes each LLM-agent toward π* under m. This is the N→∞ continuum limit of best-response multi-LLM coordination.

mechanism_transfer: MFG is a rigorous PDE-based framework; the candidate transfers HJB-FP equilibrium to LLM-agent populations.
