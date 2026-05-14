# Life Analogy — Georgian polyphony 3-voice mzakhri+zhir+bani Georgian-Triad + dissonant 2-4-7-9 harmony

The **Georgian polyphony** (UNESCO Intangible Heritage):
- 3-voice mzakhri (high)+zhir (middle)+bani (low/drone bass).
- Georgian Triad: C-F-G = perfect 4th + 2nd on top (dissonant cluster).
- Sharp dissonant intervals: seconds, fourths, sevenths, ninths.
- Kakhetian table-songs: bani drone + 2 melismatic voices above.
- Guria: highly individual freely-improvised vocal lines.

**GEORGIAN-3-VOICE-TRIAD-DISSONANT-SPECTRAL-ALLOCATION**: per-attention-head 3-voice spectral allocation with mzakhri-zhir-bani 3-band partition + Georgian-Triad dissonant-interval frequency anchor + drone-bani-fixed + 2-melismatic-voices-free + 2-4-7-9 dissonant-cluster anchor frequencies. (1) **3-voice-band attention-head partition K_3-voice**: K attention heads partitioned into 3 voice-groups K_mzakhri (high-pitch processing — long-range tokens) + K_zhir (mid-pitch — medium-range) + K_bani (low-pitch drone — context anchor). (2) **Georgian-Triad dissonant anchor frequencies**: 3 fixed RoPE anchor positions at C-F-G interval (period ratio 1.5 : 2.0 + 2nd-on-top dissonance) — explicit dissonant base frequencies. (3) **Drone-bani fixed-frequency anchor**: bani-group heads use single fixed base-frequency θ_bani serving as context-anchor sink; never modulates with position. (4) **2 melismatic voices free**: mzakhri+zhir heads use adaptive position-modulating RoPE with allowed swing over dissonant interval. (5) **2-4-7-9 interval-cluster regularizer L_diss**: explicit reward for attention concentration at 2nd/4th/7th/9th periodic positions; penalty on consonant-3rd/5th/6th major-triad concentration. (6) Differs from R402 + R416 + R431 + R440 + R457 + R468 + R279 + R482 + R495 + R507 SYRIAC-OKTOECHOS-8-BAND + R532 GUQIN-7-STRING-13-HUI-3-MODE-HARMONIC-NODE-ALLOCATION (7×13 grid + 3-mode san/an/fan + half-hui microtonal) by 3-voice band partition (not 7-string × 13-hui) + Georgian-Triad C-F-G anchors + drone-bani fixed-frequency + 2-melismatic free + 2-4-7-9 dissonant regularizer.

## Adjacency
- Frequency Bands RoPE ICLR 2026
- Mixed-Frequency RoPE EliteKV
- Hallucination Spectral Features EMNLP 2025
- Harmonizer Multimodal Tokenization MDPI 2025

Expected FAIL — per-head frequency band + spectral allocation + RoPE variants literature covers.
