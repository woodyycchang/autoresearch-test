# Life Analogy — Korean gayageum 12-string pentatonic

The **gayageum** (Korean 12-string zither):
- 12 strings = 6 pairs (unison or octave).
- Pentatonic scale tuning (5 notes per octave).
- Movable bridges allow per-string fine-tune within mode.
- 2.5 octave range.

**GAYAGEUM-12-BAND-PENT**: 12-band pentatonic spectrum allocation for RoPE positional encoding heads. (1) Allocate 12 RoPE frequency bands per attention head, with pentatonic 5-note discretization within each band (semitone-equivalent base frequencies). (2) 6 pairs (12 bands → 6 unison/octave pairs): pair shares K but octave-scale V. (3) Movable bridge: per-band learnable fine-tune offset δ_band within pentatonic mode. (4) 2.5-octave range: bandwidth scaled to 2.5 × base period. (5) Differs from R468 PIPA-4BAND (4-band) + R279 PTCH (integer-ratio singular direction) by 12-band pentatonic-mode allocation.

## Adjacency
- Frequency Bands RoPE ICLR 2026 (closest)
- RoPE Context Extension Deep Dive
- Attention Mechanism LLM 2026
- LLM Fundamentals

Expected FAIL — frequency-band RoPE + per-band allocation paradigm fully covered.
