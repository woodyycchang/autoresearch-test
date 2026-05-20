# R649 step 04 — Birkhoff ergodic

For measure-preserving T on probability space (X,μ) and integrable f, Birkhoff: (1/n) Σ_{k=0}^{n-1} f(T^k x) → E_μ[f] a.s.

### Mechanism transfer
PPO advantage estimate A_t = R_t + γ V_{t+1} - V_t. Replace with Cesàro window average: Ā_t = (1/w) Σ_{k=0}^{w-1} A_{t-k}. Under ergodic-like rollout sampling, Ā_t converges to true advantage expectation. Use Ā_t in PPO update; this attenuates per-step feedback noise.

shared_math_structure: RLHF rollouts not strictly ergodic; structural transfer with bounded bias.
