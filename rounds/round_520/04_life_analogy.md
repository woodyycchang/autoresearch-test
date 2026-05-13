# Life Analogy — Aboriginal Yolngu yiḏaki (didgeridoo) drone + overtones + tongue articulation

The **yiḏaki** (Yolngu Aboriginal Arnhem Land didgeridoo):
- Continuous drone via circular breathing (push from cheeks while inhaling through nose).
- **Fundamental + overtone** interval: slightly more than octave (E fundamental → E/F/F# overtone).
- Tongue articulation: interdental + retroflexed sounds + dup (quick jump to short trumpet).
- Yolngu style: intricate syncopation + tongue/lip dynamics layered over drone.
- Oldest continuously practiced musical tradition (NE Arnhem Land).

**YIDAKI-DRONE-OVERTONE-DUP-SPECTRAL-ALLOC**: continuous-fundamental drone anchor + overtone allocation + dup-style rhythmic gating per attention head. (1) **Continuous drone anchor**: 1 dedicated low-frequency RoPE band B_0 (fundamental) shared across all heads — analog of yidaki drone, persistent embedded fundamental. (2) **Overtone per-head allocation**: each head h_k receives ~1 overtone band B_k at interval slightly > 1 octave from B_0 (per-head RoPE frequency in {2.1, 4.2, 6.3, ...}); per Mixed-Frequency RoPE but with explicit octave-plus-spacing. (3) **Tongue-articulation rhythmic dup gating**: per-token rhythmic gate g_t ∈ {drone, dup-overtone} switches between fundamental-only and overtone-active emission (analog of tongue articulation jumping to dup). (4) **Circular-breathing inference**: forward-pass shadow KV cache pre-loaded with drone-fundamental tokens before context begins (analog of cheek-air supply); continuous drone never breaks during inference. (5) **Syncopation token-position bias**: positional encoding has secondary rhythm offset (period 4 tokens) applied to dup-gating only. (6) Differs from R402 TUVAN-IGIL + R416 XALAM + R431 TAONGA + R440 PHANTOM + R457 IMZAD + R468 PIPA + R279 PTCH + R482 COMPAS + R495 GAYAGEUM + R507 OKTOECHOS-8-MODE by continuous-drone shared B_0 fundamental + per-head octave-plus overtone B_k + dup rhythmic gate + circular-breathing pre-loaded KV + syncopation period-4 token-position bias.

## Adjacency
- Frequency Bands in RoPE ICLR 2026 (closest — per-head)
- Mixed-Frequency RoPE EliteKV
- Frequency Band Attention Mechanism
- Efficient Attention Survey 2507.19595

Expected FAIL — frequency-band RoPE + per-head allocation + rhythmic gating literature fully covers.
