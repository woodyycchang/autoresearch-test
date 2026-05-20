# R632 step 04 — source mechanism

## Source: Krylov subspace iterative methods (Lanczos, Arnoldi, GMRES, CG)

For Ax=b, the n-th Krylov subspace K_n(A,b)=span{b,Ab,A²b,...,A^{n-1}b}. Solutions x_n ∈ K_n minimize residual ‖b-Ax_n‖. Convergence rate ~((κ-1)/(κ+1))^n where κ is condition number.

### Mechanism transfer
The candidate constructs Krylov-style scratchpad for LLM CoT: define an LLM "reasoning operator" A_θ (one-step refinement using model), seed b = initial-question embedding; generate r_k = (A_θ - λ I)^k b for k=0..n. Each r_k becomes one CoT step. The scratchpad is the Krylov basis. Phase-coherent because the basis is mutually conjugate (CG-like) keeping each step a controlled linear update orthogonal in metric A.

Direct mechanism transfer: Krylov methods are the gold standard for iterative residual reduction with monotone error bounds.
