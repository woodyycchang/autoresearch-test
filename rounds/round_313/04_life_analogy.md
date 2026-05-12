# R313 — life analogy

## Source: Prosciutto salt-curing osmotic dehydration
- Salt applied externally creates concentration gradient → water diffuses out of muscle cells via osmosis.
- During aging, endogenous enzymes (cathepsins, calpains) progressively break down proteins into peptides + amino acids.
- Result: dehydrated, concentrated protein matrix with enhanced flavor — water content reduced, dry-mass relative weight increased.

## LLM analogy
**OSMO-NULL-PRUNE**: apply an external "salt-equivalent" — a structured anchor in the null-space of task-gradient — that creates a "concentration gradient" pulling weight magnitude out of NULL-SPACE (irrelevant subspaces) while keeping task-relevant subspace weights intact. After many gradient steps under osmotic regularization, the model is dehydrated: only task-relevant parameter mass remains, plus minor "aged" weight evolution in residual subspaces.

## Differs from prior art (claim)
GaLore projects gradient onto low-rank subspace. LoRA-Null initializes in null-space. Continual learning null-space methods (2024/2025 OpenReview) project gradient onto null-space to preserve prior tasks. None apply an OSMOTIC GRADIENT to actively draw weight magnitude FROM null-space (pruning irrelevant) WHILE retaining task subspace — but the mechanism is essentially null-space-aware regularization which has prior art.
