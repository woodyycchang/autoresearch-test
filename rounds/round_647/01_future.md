# R647 step 01

**Timestamp:** 2026-05-19T20:28:40Z

## Scan focus
Linear programming (LP) strong duality as mechanism source for constrained-generation context gating. LP: min c^T x s.t. Ax=b, x≥0; dual: max b^T y s.t. A^T y ≤ c. Strong duality holds under regularity. The candidate transfers LP dual variables as per-constraint context-gate weights in constrained LLM generation.

## Motivation
mechanism_transfer: LP duality is the exact relationship between primal constraint slack and dual variable. The candidate uses dual variables as gating weights at decode time — direct algebraic transfer.
