# R639 step 04 — source mechanism

## Source: RKHS / Mercer's theorem

For positive-definite kernel k: X×X → R, Mercer gives k(x,y) = Σ_i λ_i φ_i(x) φ_i(y). The RKHS H_k is the closure of {f(x) = Σ_i α_i k(x,x_i)} with norm ‖f‖²_H = Σ α_i α_j k(x_i,x_j).

Attention(Q,K,V) = softmax(QK^T)V can be read as a kernel regression with kernel k(q,k) = exp(<q,k>/√d).

### Mechanism transfer
The candidate: compute top-r Mercer modes (λ_i, φ_i) of the empirical kernel matrix over a sample of tokens. Use modal energy ratio E_r = (Σ_{i≤r} λ_i)/(Σ_i λ_i) per-token as a bandwidth-gating signal. When E_r < τ, the token's context is "high-frequency" → widen attention bandwidth (lower softmax temperature); else narrow.

Direct mechanism transfer: Mercer's theorem and RKHS are the canonical mathematical framework for attention.
