# R294 — life analogy

## Source: Antikythera mechanism multi-period gear-train
- ~30 bronze gears interleaved → predict Metonic 19-year, Saros 18-year (eclipses), and synodic month simultaneously from ONE input rotation.
- Each gear ratio encodes a celestial period; differential gear combines (sun rate, moon rate) to compute synodic month.
- KEY: composition of MULTIPLE INCOMMENSURABLE CYCLES (19yr, 18yr, 235 months) via differential gear-train into a SINGLE shared time index.

## LLM analogy
**ANTIKY-LLM**: an attention architecture with K multi-period heads, each head fixed to a different periodic rotation (e.g., position-mod-2, mod-3, mod-5, mod-7, ... distinct primes), combined via a differential-gearing fusion (token-position rotor inputs to head k = position × cos(2πt/Pk), sin(2πt/Pk)); attention output is the deterministic ANGLE of the differential-gear sum across multi-period rotors — i.e., a Chinese Remainder Theorem composite-modulo position encoding.

## Differs from prior art (claim)
- Standard rotary position encoding (RoPE): SINGLE-frequency-set per head, sinusoidal.
- Attention Illuminates (2510.13554): observational, not prescriptive multi-period structure.
- Dual-Phase reasoning (2601.05616): two-phase iteration, not multi-period attention.
- ANTIKY-LLM: combines K incommensurable-period rotors at distinct prime periods + differential-gear fusion as CRT-style composite position encoding — open whether subsumed by existing RoPE-multi-frequency variants.
