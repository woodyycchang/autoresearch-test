# Life Analogy — Andalusian flamenco compás 12-beat allocation

The **compás** (Andalusian flamenco):
- 12-beat cycle = ¾ + 6/8 amalgamated.
- Accents on 3, 6, 8, 10, 12 → non-uniform allocation.
- Hemiola: binary articulated as ternary, tension via rhythmic ambiguity.
- Headless beat: beat 1 silent.
- Different palos (soleá, bulería, alegrías) share the 12-beat structure but vary entrance: bulería starts on beat 12; soleá starts on beat 1.

**COMPAS-NONUNIFORM-ALLOCATION**: 12-cycle non-uniform per-beat compute/attention allocation for transformer decoding. (1) Group tokens into 12-position cycles. (2) Allocate decode budget non-uniformly: B(position) higher at positions {3, 6, 8, 10, 12} (accent), lower at {1, 2, 4, 5, 7, 9, 11}. (3) Hemiola: optionally re-articulate binary 2+2+2 vs ternary 3+3+3+3 dynamically per cycle based on content. (4) Headless skip: position-1 attention computation skipped (gated mask). (5) Multi-palo: cycle entrance varies per task type (analytic = soleá start, generative = bulería start).

## Adjacency
- D-LLM Token Adaptive Compute Allocation (NeurIPS 2024)
- Non-Uniform KV Quantization
- Efficient LLM Inference Survey 2025
- Dynamic Cache Budget Allocation

Expected FAIL — non-uniform compute allocation paradigm well-covered.
