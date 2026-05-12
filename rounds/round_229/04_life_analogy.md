# R229 — life analogy

## Source domain: abalone nacre brick-and-mortar
- ~95% by volume of aragonite tablets (hard, brittle, oriented platelets) interleaved with ~5% volume of chitin-protein mortar (soft, ductile, glue).
- Mineral NANOBRIDGES penetrate the mortar at controlled densities, providing extra crack-deflection paths.
- The composite is 3000× tougher than monolithic aragonite while being structurally lightweight: cracks propagate through the mortar (energy dissipation) rather than fracturing tablets.
- Key insight: alternating-stiffness lamination + bridge density is what produces fracture toughness; neither tablet nor mortar alone is robust.

## LLM analogy candidate
**Nacre-architecture LoRA stack**: instead of placing all adapter capacity into ONE adapter layer or ONE LoRA, decompose the adapter into ALTERNATING "hard" and "soft" layers:
- HARD layers: low-rank rotation-locked (orthogonal) adapters with HIGH magnitude, behave like aragonite tablets — confer task capability but brittle to compositions.
- SOFT layers: high-rank low-magnitude regularization-dominant adapters, behave like chitin-protein mortar — diffuse errors / failures across boundaries.
- MINERAL NANOBRIDGES: sparse skip-connections between non-adjacent hard layers, controlled density.
The full stack mimics nacre's brick-and-mortar topology. Predicted property: catastrophic capability loss under hostile fine-tune (e.g. malicious data poisoning analogous to crack propagation) is ARRESTED at soft layers + bridged densely back to a different hard layer's capability anchor.

## What differs from prior art (claim)
Modular bricks (Configurable Foundation Models 2409.02877) treat neurons as functional partitions but not as a hard/soft alternating laminate with controlled bridge density. LoRA library reuse (2405.11157) is composition-of-experts at deployment time, not a lamination architecture. No surveyed work specifies the alternating hard-rotation + soft-regularizer + sparse-bridge topology of nacre and uses it for fracture-toughness-style robustness to adversarial fine-tune.
