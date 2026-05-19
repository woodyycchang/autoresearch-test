# R638 step 04 — source mechanism

## Source: Compressed sensing RIP

A ∈ R^{m×n} satisfies RIP_s(δ) iff (1-δ)‖x‖² ≤ ‖Ax‖² ≤ (1+δ)‖x‖² for all s-sparse x. RIP with δ_{2s} < √2-1 ensures Basis Pursuit `min ‖x‖_1 s.t. Ax=y` recovers the unique s-sparse solution.

### Mechanism transfer
MoE router projection W_router ∈ R^{E×d} acts as a "compressing matrix" from d-dim hidden state to E expert scores. Top-s selection of experts is exactly the s-sparse selection problem. Candidate: certify RIP_s(δ) for W_router via spectral lower bound on E^d sub-matrices; add RIP-aware regularizer ‖W_router^T W_router - I_E‖_F to push toward RIP-compliance.

Direct mechanism transfer: RIP is the exact algebraic identity governing sparse recovery.
