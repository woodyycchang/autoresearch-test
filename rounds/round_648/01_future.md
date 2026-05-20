# R648 step 01

**Timestamp:** 2026-05-19T20:33:15Z

## Scan focus
Doob's optional stopping theorem (martingale theory) as mechanism source for adaptive early-exit decoding evaluation. OST: for a martingale M_n and stopping time τ with E[τ]<∞ and bounded increments, E[M_τ] = E[M_0]. The candidate uses OST to build a confidence-bound on partial decoding quality during generation.

## Motivation
shared_math_structure: Doob's OST is a rigorous theorem; partial-decode quality scores form an approximate martingale only under specific assumptions, so structural rather than mechanism transfer.
