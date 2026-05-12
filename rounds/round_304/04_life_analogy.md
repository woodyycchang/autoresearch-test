# R304 — life analogy

## Source: Diatom silica frustule hierarchical self-assembly
- Living diatoms convert silicic acid into silica nanospheres in the Silica Deposition Vesicle.
- Long-chain polyamines (LCPAs), silaffins, and silacidin peptides COOPERATE to organize nanospheres into hierarchically nested mesh patterns (20 nm → 100 nm → 1 μm features).
- Final frustule is a single integrated nano-micro structure formed by bottom-up molecular cooperation, not by template-down deposition.

## LLM analogy
**FRUSTULE-FT**: hierarchical self-assembling LoRA — start with small "nanosphere" rank-2 adapters at fine-grained sub-layers; small adapters COOPERATIVELY merge via cross-rank coordination peptide-analog (a learned cross-adapter binding objective) to form mid-scale rank-8 cluster adapters, which further self-assemble into layer-level rank-32 modules. Hierarchy emerges bottom-up via cooperative merging, not top-down rank assignment.

## Differs from prior art (claim)
HiLo (2502.03884) hierarchically configures rank/count top-down per layer. LoRA library + routing (2405.11157) uses retrieval to compose pre-built adapters. CompAs sums adapter parameters compositionally. None of these self-assemble small adapters into larger structures via cooperative binding objectives (cross-rank "peptide" objective). Bottom-up assembly is mechanistically distinct from top-down configuration or retrieval composition.
