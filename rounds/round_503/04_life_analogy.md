# Life Analogy — Romanian Doina vocal melisma rubato breath-bounded improvisation

The **Doina** (Romanian lyric vocal/instrumental free-form):
- Free-rhythm, highly melismatic improvisation over a fixed descending pattern (usually).
- Parlando-rubato: meter is subordinated to breath and expressive delivery — phrases expand/contract with breath rather than fixed pulse.
- Abundance of melismas, grace notes, glissando, microtimbral nuance.
- Sighs descending to tonic; emotional content of "dor" (Romanian sorrow).
- Solo, often unmetered.

**DOINA-MELISMA-RUBATO-NULL**: null-space-traversal LoRA with continuous-melisma rubato gradient: (1) Updates are projected to the null-space N(W_pre) of the pre-trained weights (LoRA-Null orthogonal projection — preserve prior capability). (2) Within N(W_pre), update follows a continuous-time melisma trajectory: ∂Θ/∂t = α(t)·proj_N(∇L) where α(t) is rubato schedule — α grows during "long-held" batch positions (where loss gradient is informative) and shrinks during "ornament" positions (where gradient is noisy). (3) α(t) is bounded by "breath budget" B = ∫α(t)dt over an epoch — global constraint mimicking singer's lung capacity. (4) Descent target: sighs to a tonic basin (cosine-annealed final point at minimum-energy region of null-space). (5) Differs from R478 SUTARTINES-DIAPHONY-NULL (orthogonal LoRA + Stiefel manifold, discrete-step rotation) by continuous-time rubato magnitude schedule + breath-budget global constraint + descending-tonic basin target.

## Adjacency
- LoRA-Null Tang et al. 2025 (closest)
- OPLoRA 2510.13003 (orthogonal projection)
- AltLoRA 2505.12455 (alternating projections)
- Continual Gradient Low-Rank ACL 2025
- Flat-LoRA / Stiefel-LoRA
- Cosine LR schedule + descending LR

Expected FAIL — null-space LoRA + variable-rate continuous-time gradient + cosine descent fully covered.
