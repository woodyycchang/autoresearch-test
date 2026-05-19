# R648 step 04 — Doob OST

M_n adapted to F_n is martingale if E[M_{n+1}|F_n] = M_n. OST: for stopping time τ bounded, E[M_τ] = E[M_0]. e-processes generalize via E[M_{n+1}|F_n] ≤ M_n.

### Mechanism transfer
Construct e-process E_n over partial decode: at each step n, e-multiplier B_n = score(token_n)/baseline. E_n = Π B_k. By Ville's inequality, P(sup_n E_n ≥ 1/α) ≤ α. Stop generation when E_n crosses threshold (sufficient quality with α confidence).

shared_math_structure: martingale construction depends on token scoring meeting martingale-like property; approximate.
