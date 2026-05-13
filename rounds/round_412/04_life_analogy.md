# Life Analogy — Spider trichobothria (multiscale frequency-tuned hair array)

The **spider trichobothria**:
- Each leg carries an array of ~100 trichobothria hairs.
- Hair LENGTHS vary 100-1400 μm; each length has a **specific best mechanical resonance frequency** (40-600 Hz).
- The full array of varying-length hairs acts as a **BANK OF FREQUENCY-TUNED FILTERS** — each hair samples a different frequency band.
- Phasic response to deflection speed; the spider integrates the bank's outputs into a directional, frequency-decomposed air-current map.

The unique principle: **physical-length-determined per-receptor frequency tuning in a parallel bank** — same sensor type, different geometric parameter (length), produces a frequency decomposition without any active processing. Cheap, parallel, geometric.

## Analogical mapping → per-head frequency-band tuned attention cascade

- Trichobothria array ↔ a multi-head attention layer
- Hair length ↔ a fixed per-head "frequency width" parameter (a property of the head, not learned)
- Frequency band each hair tunes to ↔ a fixed frequency-domain attention window per head
- Bank of filters ↔ ensemble of per-head frequency-selective attention outputs

The mechanism: **TRICHOBOTHRIA per-head frequency-band tuning cascade** — assign each head h_k in an MHA layer a FIXED positional-frequency mask m_k(t-t'): m_k(Δ) = cos(2π f_k Δ) · exp(-Δ^2 / σ_k^2) where f_k = f_0 · 2^(k/H) (geometric series; H heads span H frequency octaves) and σ_k = c/f_k (bandwidth scales inversely with center frequency). Apply m_k as a multiplicative bias on the attention scores of head k before softmax: score_k(t, t') = QK^T_k + log m_k(t-t'). This forces head k to attend at frequency f_k. As tokens cascade through layers, low-frequency heads accumulate long-range context, high-frequency heads accumulate local context — the cascade integrates a multi-scale frequency-decomposed context. Differs from (a) ALiBi linear bias (linear-in-Δ not frequency), (b) RoPE positional encoding (rotary embed not bandpass mask), (c) cascaded multi-scale attention (typically learns scales, not fixed log-spaced), (d) PowerAttention DAG (sparse not frequency-tuned) by enforcing FIXED GEOMETRIC FREQUENCY SPACING per head.

## Note on adjacency

The information-cascade form fits. Adjacent: ALiBi positional bias, log-distance bucketing, RoPE, FNet Fourier mixing. Distinct: explicit per-head bandpass with geometric f_k spacing, fixed by construction rather than learned.
