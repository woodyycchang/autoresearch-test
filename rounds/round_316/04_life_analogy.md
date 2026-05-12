# R316 — life analogy

## Source: Permafrost cryogenic preservation
- Permafrost stores ~1300 Gt organic carbon, much for tens of thousands of years.
- Three vertical layers: (1) seasonal active layer (thaw-refreeze yearly), (2) cryoturbation zone (slow mixing), (3) deep permafrost (frozen, mineral-associated, millennial stability).
- Microbial decomposition is suppressed by cold + ice-rich sediments.

## LLM analogy
**PERMAFROST-PARAM**: 3-tier parameter memory architecture. Tier 1 (active): full-precision recently-used weights; Tier 2 (cryoturbation): INT8-quantized, rare-use cold cache; Tier 3 (deep permafrost): FP4 + disk-offload, frozen for millennia-equivalent training cycles unless explicit thaw event triggers. Transitions: parameters that have been unused for K steps demote to tier 2; unused 10K demote to tier 3. Iron-mineral analog: each tier-3 weight is stored with a small high-precision "stabilizer" anchor to prevent degradation.

## Differs from prior art (claim)
GPTQ/AWQ quantization compresses ALL weights to low precision uniformly. Mixed-precision quantization applies per-layer policy. Parameter offloading (e.g., DeepSpeed Zero) moves to CPU/disk uniformly. PERMAFROST-PARAM is access-frequency-gated 3-tier with iron-stabilizer anchor — but tiered memory architectures (hot/warm/cold) are mainstream in storage systems and increasingly applied to LLMs.
