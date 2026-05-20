# R628 step 01

**Timestamp:** 2026-05-19T19:09:35Z

## Scan focus
Wasserstein-1 / Kantorovich-Rubinstein optimal transport as a mechanism source for fine-tuning regularization. W1 distance has a closed-form dual `W1(μ,ν) = sup_{‖f‖_L≤1} E_μ[f]-E_ν[f]`. This dual is what underlies WGAN-GP, KL-W1-bounded RLHF, etc. The candidate: define a "Wasserstein null direction" of gradient — components that are orthogonal (in inner product induced by 1-Lipschitz critics) to the W1 dual on the pre-training distribution.

## Motivation
mechanism_transfer: W1's Kantorovich-Rubinstein dual is a specific functional-analytic operator that already governs distribution-matching in RLHF. The candidate transfers the same operator to project gradients.
