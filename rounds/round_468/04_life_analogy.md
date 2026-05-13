# Life Analogy — Chinese pipa 4-string spectral pitch-bend lute

The **Chinese pipa**:
- 4-string lute; 12-31 frets; high frets enable continuous-pitch bend between frets.
- Per-string spectral allocation: 4 strings tuned to 4 distinct base frequencies.
- Continuous pitch-bend + slide + vibrato + harmonics per-string left-hand fingering.
- Right-hand plucking adds rapid tremolo + ornament across all 4 strings.

**PIPA-BEND**: a 4-string per-head spectral-allocation with continuous pitch-bend. (1) Partition transformer heads into 4 spectral bands per layer (analog of 4 pipa strings). (2) Per-band base frequency ω_i tuned across spectral range; per-head attention restricted to its band's spectral signature. (3) Continuous pitch-bend: a learned per-token offset δ_t enables continuous excursion from base frequency (analog of fret-free bend) — small additive bias to RoPE phase. (4) Right-hand tremolo: rapid per-band amplitude modulation across 4 bands during token generation (analog of rapid plucking ornament). (5) Cross-band harmonics: per-head overtone production combines bands via Hadamard-style product.

## Adjacency
- AMSFormer Adaptive Multi-Scale Spectral Filtering
- Spectral-Spatial Wave-Frequency Interactive Transformer
- Sparse Spectral Transformer Dynamic Frequency-Aware
- MFformer Multi-Frequency Aggregation

Expected FAIL — multi-band spectral transformer + pitch-aware attention well-covered.
