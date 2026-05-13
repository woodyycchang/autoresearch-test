# Life Analogy — Wolof xalam 5-string griot lute band allocation

The **Wolof xalam** (Senegalese griot lute):
- 5 strings; 3 standard tunings (ci suuf, ci kow, ardin) each fixing string→interval mapping.
- Griot's hand allocates each melodic phrase to a specific string, exploiting fixed frequency-band of that string.
- Praise-song narrative shifts trigger string-switch.

The mechanism: **fixed string→frequency-band mapping + phrase-aware band allocation**.

## Analogical mapping → LLM frequency-band specialised attention

- Xalam string ↔ specialised attention head pre-allocated to a frequency band
- Tuning system ↔ band-allocation scheme
- Phrase-aware string-switch ↔ token-aware band routing

**XALAM-FREQ**: spectral-allocation attention design where attention heads are pre-allocated to disjoint frequency bands of RoPE positional encoding; each head's Q/K projection forced via L2-norm constraint to occupy its assigned band only; routing layer assigns each query token to the band whose central frequency matches the token's "tessitura" (estimated from token embedding norm).

## Adjacency
- Frequency Bands in RoPE ICLR 2026 (direct twin)
- Spectral Scaling Laws EMNLP 2025
- Local Spectral Attention 2302.05693

Expected FAIL.
