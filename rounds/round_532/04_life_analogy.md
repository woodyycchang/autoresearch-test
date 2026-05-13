# Life Analogy — Chinese guqin 7-string silk + 13-hui harmonic-node positions + 3-mode (open/pressed/flageolet) spectral tuning

The **Chinese guqin** (古琴):
- 7 silk-strings pentatonic-tuned C2-D2-F2-G2-A2-C3-D3.
- 13 hui (徽) nodal-position marks placed at string divisions 1/2, 1/3, 1/4, ... 1/13 (harmonic nodes 2-13).
- 3 sound modes: (a) san-yin = open string fundamental; (b) an-yin = pressed-position note (any string-length fraction); (c) fan-yin = flageolet at hui node → harmonic partial.
- 91 commonly-used harmonics across 7 strings × 13 hui ≈ 91 grid.
- Half-hui positions (8.5 = between 8th and 9th) enable microtonal inflection beyond 12-TET.

**GUQIN-7-STRING-13-HUI-3-MODE-HARMONIC-NODE-ALLOCATION**: per-attention-head 3-mode spectral allocation with 7-string head-group × 13-hui frequency-node × 3-mode sound-class + half-hui microtonal interpolation. (1) **7-head-group × 13-frequency-node grid G_{7×13}**: K-attention heads partitioned into 7 string-groups (analogous to 7 silk-strings); each group gets 13 harmonic-node RoPE frequency positions (partial-2 to partial-13). (2) **3-sound-mode per query token**: each token's positional encoding assigned (a) san-mode = fundamental open RoPE, (b) an-mode = pressed continuous RoPE position, (c) fan-mode = flageolet harmonic-node — discrete RoPE at one of 13 hui frequencies. (3) **Half-hui microtonal interpolation**: between hui_k and hui_{k+1}, allow fractional ν = α·hui_k + (1-α)·hui_{k+1} for fine-grained pitch interpolation. (4) **Mode-selection token-class router**: each input token classified into 3 sound-classes by content type (san: factual lookup, an: reasoning, fan: harmonic-resonance / pattern-completion); routing chooses RoPE mode. (5) **91-position frequency lookup table** built from 7 strings × 13 hui-grid, accessed by (group, hui-index) per head. (6) Differs from R402 + R416 + R431 + R440 + R457 + R468 + R279 + R482 + R495 + R507 SYRIAC-OKTOECHOS-8-BAND (8-spectral-band attention-head partition + weekly mode rotation + mode-theme binding + Beth Gazo per-band template + epoch-boundary restart, no 13-hui nodal positions + no 3-mode san/an/fan + no half-hui microtonal + no 7-head-group × 13-hui grid) by 7-head-group × 13-frequency-node grid + 3-mode token classification + half-hui microtonal interpolation + 91-position grid lookup.

## Adjacency
- Hallucination Detection Spectral Features Attention 2502.17598
- Hardware-Aligned Sparse Attention ACL 2025
- Long-Context Generalization 2506.16640
- Frequency Bands RoPE ICLR 2026

Expected FAIL — spectral attention + frequency-band RoPE + per-head allocation literature covers.
