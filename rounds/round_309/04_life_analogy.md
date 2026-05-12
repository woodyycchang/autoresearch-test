# R309 — life analogy

## Source: Macrotermes termite mound passive ventilation
- Mounds use central "chimney" + lateral pores: warm air rises by convection (driven by termite + fungal-garden metabolic heat); cooler air drawn in through base pores.
- Diurnal temperature oscillation provides the driving gradient; no active fanning.
- Stigmergic construction: mound geometry self-optimizes for thermal homeostasis without central planner.

## LLM analogy
**MOUND-CONVECT**: passive convection-style context-gating. Each token activation has an "activation-temperature" (magnitude norm); high-magnitude tokens are routed via the central "chimney" path to the next layer's residual stream while low-magnitude tokens cycle through a lateral "cool-air" path (skip-connection or low-rank reservoir). The split is driven by activation-temperature gradient, not by learned attention. Gives passive context-window thermal regulation: active tokens propagate upward, inactive ones stagnate in reservoir.

## Differs from prior art (claim)
Mixture-of-Depths (MoD) routes tokens based on learned router. Attention-sink routing uses fixed anchor tokens. Token pruning ranks by attention. None route by activation-magnitude convection gradient with central chimney + lateral cool-air dual-path architecture.
