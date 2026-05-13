# Life Analogy — Mbuti Twa Pygmy hocket interlocking polyphony

The **Mbuti/Twa** Pygmy hocket polyphony:
- Hocket = rapid alternation of single notes between singers (each singer contributes ONE note at a time).
- Combined output sounds like continuous melody but composed of single-tone contributions from multiple singers.
- Yodel chest/head register alternation amplifies the interleaving texture.

**MBUTI-HOCKET-DECODE**: a multi-decoder parallel-sampling architecture where K small draft decoders each emit exactly ONE token per step in PHASE-OFFSET interlocking pattern (decoder i emits token at position k·K + i). The resulting interleaved sequence is verified by a single target model. Differs from generic speculative decoding (one draft + verifier) by K phase-offset INTERLOCKING SINGLE-NOTE drafters + cohesive verification.

## Adjacency
- Parallel Token Prediction ICLR 2026 2512.21323
- Multi-Token Prediction 2507.11851
- Judge Decoding Speculative
- P-EAGLE Parallel Speculative Decoding

Expected FAIL — parallel speculative decoding + multi-token prediction is heavily covered.
