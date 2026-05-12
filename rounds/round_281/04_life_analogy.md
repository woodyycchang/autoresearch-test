# R281 — life analogy

## Source domain: Welwitschia mirabilis basal meristem leaf growth
- Plant has ONLY TWO leaves, never sheds them.
- Both leaves continuously grow at the BASE — distal tip is the OLDEST tissue; the meristem (cell division zone) is at the BASE/CROWN.
- Distal tip frays/dies/dust-bleaches but base keeps producing fresh tissue → leaf grows up to 6m over centuries.
- Trunk/crown stays the same; ALL increment is at meristem, ALL aging is at the tip.
- The plant therefore CARRIES its entire morphological history as a continuous record in the leaf tissue — proximal = young, distal = oldest layer, no shedding.

## LLM analogy candidate
**Welwitschia-Meristem Continual Learning (WMCL)**: an LLM/agent learning architecture where the base parameters NEVER UPDATE (the "crown") and ALL learning happens by appending NEW low-rank parameter strips at a single growth-edge (the "meristem") that is fixed in location. Old strips are NEVER REMOVED and NEVER UPDATED; they're left to "fray" naturally (older retrievals get less weight as the strip stack grows). At inference, every output is a weighted convolution over the entire stack of historical strips, with weights monotonically decreasing toward the distal (oldest) end. KEY: no replacement, no replay, no LoRA-merge — just continuous one-end-only append.

## What differs from prior art (claim)
- O-LoRA / OA-Adapter (2505.22358): per-task adapters in orthogonal subspaces — but new tasks get NEW subspaces, not appended STRIPS in the same direction.
- ELLA (2601.02232): subspace de-correlation with high/low-energy distinction.
- ELDER: per-edit new adapter + router network.
- WMCL is uniquely one-edge-only append (no replacement, no router, no orthogonal-subspace constraint) and uses distance-from-meristem as a decay weight at inference — like reading a Welwitschia leaf from base to tip.
