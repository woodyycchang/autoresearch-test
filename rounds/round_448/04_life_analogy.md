# Life Analogy — Mapuche ülkantun song-passage memory

The **Mapuche ülkantun** oral memory:
- Traditional chants encoding occupation memory + lineage + healing across generations.
- Multiple ül categories (love/healing/elegy/lullaby/epic) — each plays a distinct damping role in collective memory.
- Memory passage is intentional: oldest events damped via stylized form, newer events sharper.

**ULKANTUN-DAMP**: a category-conditioned context-decay feedback attenuator where N category-anchors {LOVE, HEAL, ELEGY, LULLABY, EPIC} are attached to each context segment; each anchor carries a category-specific decay rate δ_c (epic = slow decay, lullaby = fast decay); attention weights to segment s_t at position t-τ scaled by exp(-δ_{cat(s_t)}·τ). Differs from generic distance-decay attention by CATEGORY-CONDITIONED multi-rate damping.

## Adjacency
- Memory Curse 2605.08060
- ACT-R LLM Memory Architecture
- Proactive Interference Memory Limits
- Context Window RAM-not-Storage 2026

Expected FAIL — category-conditioned context decay + attention attenuation is well-covered.
