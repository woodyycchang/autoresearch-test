# R639 step 01

**Timestamp:** 2026-05-19T19:55:55Z

## Scan focus
Reproducing kernel Hilbert space (RKHS) as mechanism source for context-gating. RKHS H with reproducing kernel k satisfies <f, k(·,x)>_H = f(x). Attention can be viewed as an RKHS inner-product retrieval. The candidate transfers the RKHS framework to context-gating via Mercer-based finite-rank approximations that control bandwidth.

## Motivation
mechanism_transfer: attention IS kernel regression at scale (Tsai et al. 2019 etc.). Mercer eigen-decomposition gives an explicit finite-rank basis. The candidate proposes adapter-style bandwidth controller via top-r Mercer modes.
