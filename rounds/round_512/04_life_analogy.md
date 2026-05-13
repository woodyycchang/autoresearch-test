# Life Analogy — Italian Stradivarius wood-resonance selective damping

The **Stradivarius** violin (Cremona, 17th-18th c):
- Top + back plate wood (spruce/maple) seasoned for years.
- Plate thickness graduated micron-precisely (tiny changes = large frequency shift).
- Wood treated with mineral salts (borax, zinc, copper, alum) — chemical preservation.
- Ground-coat calcium-rich + final-varnish oil/resin layered.
- **Selective damping**: varnish damps weak frequencies, preserves strong fundamentals + harmonics.
- Low internal damping in wood; resonances strongly peaked.

**STRADIVARIUS-SELECTIVE-FREQUENCY-DAMP**: feedback-attenuation via selective-frequency damping of gradient/loss oscillations: (1) Decompose gradient signal g_t over training steps into K frequency bands G_1, ..., G_K via STFT/wavelet. (2) Identify "strong fundamental + harmonic" bands G_fund (low-frequency dominant signal) and "weak high-frequency oscillation" bands G_weak (likely-spurious). (3) Apply varnish-style selective damping: per-band damping coefficient d_k where d_k is high for weak bands and low for strong/fundamental bands. (4) Modified gradient g_t' = sum_k (1 - d_k) · G_k. (5) **Plate-thickness graduation** = layer-wise gradient norm budget β_l per layer; tiny changes in β_l = large effect on training dynamics — calibrated per-layer. (6) **Wood-seasoning** = pre-training warmup phase where high-frequency gradient bands are gradually attenuated until "well-seasoned" steady state. (7) **Mineral-salt chemical treatment** = pre-training data filtering removes salt-like contaminants (high-leverage low-quality samples) that destabilize frequency response. (8) Differs from R487 BHANGRA-DHOL-DUAL-DAMP (dual-band high/low EMA damp) by selective-per-band damping coefficient + plate-thickness layer-wise grad-norm budget + wood-seasoning warmup + mineral-salt pretraining data filtering.

## Adjacency
- Spike No More COLM 2025 (closest training stabilization)
- SPAM Spike-Aware Adam (closest gradient damping)
- DAPO/GSPO stabilization
- Layer-wise gradient norm
- Frequency band gradient analysis

Expected FAIL — gradient spike damping + selective band attenuation + warmup + data filtering literature fully covers.
