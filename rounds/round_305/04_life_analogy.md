# R305 — life analogy

## Source: Persian qanat (Kariz) underground water network
- Mother well taps aquifer (deep memory source).
- Gently-sloping (0.3-0.5%) underground tunnel passively transports water by gravity over kilometers.
- Vertical access shafts at intervals provide ventilation, sediment maintenance, and local extraction points.
- Output: distribution gallery delivers continuous gravity-fed flow without active pumping.

## LLM analogy
**QANAT-KV**: distributed KV cache with a single "mother-well" deep-context anchor (long-term high-importance state vector), a gently-sloping passive priority gradient (token importance smoothly decays with cache position via fixed gravity-analog decay schedule), and "access shafts" — periodic eviction-and-merge points along the tunnel where low-priority tokens are flushed and the surviving stream is compressed. KV flows continuously from anchor to output without per-request re-pumping.

## Differs from prior art (claim)
LMCache (2510.09665) maintains external KV cache for cross-request sharing. TRIM-KV (2512.03324) learns per-token retention with decay. LKV (2605.06676) learns head-wise budgets. None propose a SINGLE-ANCHOR mother-well + FIXED-SLOPE gravity-decay + periodic-access-shaft merging architecture; QANAT-KV is a passive flow design rather than learned-importance design.
