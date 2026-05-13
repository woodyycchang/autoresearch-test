# Life Analogy — Sardinian launeddas triple-pipe phase coherence

The **launeddas** (Sardinia, since 8th BCE Nuragic):
- 3 pipes simultaneously played by single player.
- Tumbu (drone) provides continuous fundamental reference.
- Mancosa + mancosedda play melody in 3rds/6ths against drone.
- Circular breathing — player inhales nose while exhaling stored cheek-air — sustains continuous output.
- Drone-melody phase coherence is the musical essence: every melody note locks against drone fundamental.

**LAUNEDDAS-TRIPLE-LOCK**: three-channel synchronized attention head triplet against shared drone-reference embedding. (1) Designate one "drone-head" per layer that maintains continuous low-frequency reference embedding D_layer (extracted via long-EMA of layer activations). (2) Per layer, designate 2 "melody-heads" that synchronize against drone by adding phase-locked offset φ_drone-melody(token, drone-reference). (3) Drone-head's reference is continuous (sustained across context window via circular-breathing-style stored KV without re-computation). (4) Phase-coherence loss: penalize drone-melody embedding drift > τ. (5) Triplet (drone + 2 melody heads) coordinates as a single phase-locked unit per layer.

## Adjacency
- TransMLA Multi-Head Latent Attention 2502.07864 (closest — shared latent KV reference)
- DuoAttention retrieval+streaming heads 2410.10819 (dual-channel)
- DeepSeek MLA latent shared KV (ACL 2025)
- Cross-Attention Routing one head many models 2509.09782

Expected FAIL — shared-reference multi-head architectures heavily covered MLA / DuoAttention 2024-2026.
