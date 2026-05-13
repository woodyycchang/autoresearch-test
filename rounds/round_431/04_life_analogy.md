# Life Analogy — Maori taonga pūoro microtonal wind instruments

The **Maori taonga pūoro** wind tradition:
- Kōauau (ductless flute), nguru, putorino, putatara — breath-driven instruments.
- Designed to produce MICROTONES outside the 12-tone Western semitone grid.
- Pitch micro-control via finger-pressure + breath modulation, not discrete fret positions.
- Spirit-voice rendering depends on sub-semitone tonal subtlety.

**TAONGA-MICRO-BAND**: a speech-codec quantization scheme that allocates DENSE SUB-SEMITONE pitch tokens in the pitch range corresponding to emotional / spirit-voice subtleties (Maori-microtonal-locus), while keeping standard semitone quantization elsewhere. Hybrid quantization map: in [F_low, F_high] semitone-quantize, in [F_emotional_low, F_emotional_high] use 50-cent or 25-cent fine bins. Mimics taonga pūoro's micro-control where it matters expressively.

## Adjacency
- Spark-TTS 2503.01710 (attribute tokenizer fine-grained pitch)
- SAC Dual-Stream Codec 2510.16841
- VoxCPM RALM (reconstructing subtle vocal characteristics)
- CosyVoice 2 (FSQ replaces VQ for finer-grained control)

Expected FAIL — fine-grained pitch quantization for TTS is saturated 2025-2026 design region.
