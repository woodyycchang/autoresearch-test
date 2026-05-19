# R638 step 01

**Timestamp:** 2026-05-19T19:51:30Z

## Scan focus
Compressed sensing Restricted Isometry Property (RIP) as mechanism source for sparse-activation guarantees in MoE / sparse-attention. RIP states: a matrix A satisfies RIP_s(δ) if (1-δ)‖x‖² ≤ ‖Ax‖² ≤ (1+δ)‖x‖² for all s-sparse x. RIP enables exact L₁ recovery via Basis Pursuit.

## Motivation
mechanism_transfer: RIP is the canonical mathematical condition for compressed-sensing exact recovery. MoE routers (s active experts of E total) and sparse-attention (top-k active heads) are literal s-sparse selection. The candidate certifies RIP for the routing matrix as a sufficient condition for stable sparse routing.
