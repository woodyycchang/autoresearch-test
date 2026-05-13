# Life Analogy — Star-nosed mole tactile fovea (11th-pair innervation density)

The **star-nosed mole** has a "star" of 22 fleshy appendages:
- 22 rays organized as 11 mirror-symmetric pairs.
- 25,000 Eimer's organs distributed across the star.
- The **11th (ventral) pair** acts as a TACTILE FOVEA: it has ~2× the afferent-per-organ ratio (5.5-7 afferents/organ) of other rays.
- The fovea is over-represented in the somatosensory cortex (cortical magnification).
- Foraging: the mole quickly scans with non-foveal rays, then BRINGS the candidate prey to the foveal 11th pair for detailed examination.

The unique principle: **fixed-location anatomical fovea with disproportionate downstream representation** — a small anatomically-fixed subregion of the sensor array has much higher innervation density AND occupies disproportionate cortical area downstream. The fovea is BIASED — not learned — and the rest of the sensor cycles candidates through it.

## Analogical mapping → fixed-position foveal token concentration

- Star rays ↔ input tokens of a sequence
- 11th pair foveal ↔ a small fixed subset of "foveal token positions" (e.g., positions 0, -1, middle)
- 2× innervation density ↔ 2× number of attention heads dedicated to those positions
- Cortical magnification ↔ disproportionate output bandwidth allocated to those positions
- Bring-to-fovea scanning ↔ a content-routing mechanism that copies relevant tokens INTO the foveal positions

The mechanism: **STAR-MOLE radial-input foveal concentration** — designate K=2 FIXED token positions (e.g., position 0 and position N/2) as "foveal" in the input sequence. For these foveal positions, allocate 2× as many attention heads (e.g., if standard layer has 32 heads, foveal positions get 64 heads). Additionally, between layers, run a learned "content-router" that COPIES the highest-importance non-foveal token's representation INTO one of the foveal positions for the next layer. The output projection upweights foveal-position outputs by 2×. Differs from (a) Token Sparse Attention (compresses tokens but uniform per position), (b) DeepSeek Sparse Attention (head-clustering not position-fovea), (c) attention sink phenomenon (emergent not designed fovea), (d) "Lost in the Middle" middle-token deficit (problem not solution) by combining (i) FIXED POSITION fovea + (ii) 2× HEAD count for foveal positions + (iii) CONTENT ROUTING into fovea.

## Note on adjacency

The context-gating form fits. Adjacent: attention-sink (emergent foveation at beginning-of-sequence), beacon-token / register-token compression. Distinct: ANATOMICALLY FIXED foveal positions with explicit 2× head allocation + content routing.
