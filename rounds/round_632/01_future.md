# R632 step 01

**Timestamp:** 2026-05-19T19:27:00Z

## Scan focus
Krylov subspace methods (Lanczos, Arnoldi, GMRES) as mechanism source for iterative reasoning steps. Krylov subspace K_n(A,b) = span(b, Ab, A²b, …, A^{n-1}b) gives the optimal n-dimensional approximation space for the solution of Ax=b for low n. The candidate transfers the Krylov-recursion as a phase-coherent reasoning step generator.

## Motivation
mechanism_transfer: Krylov subspace IS the canonical iterative-refinement framework with optimality guarantees (CG, GMRES). The candidate applies the same algorithm structure to LLM Chain-of-Thought reasoning — each step is a Krylov basis vector A^k r_0 of the residual, providing a controlled progression toward the answer.
