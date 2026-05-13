# Life Analogy — Yanomami shabono circular communal architecture

The **Yanomami shabono** (Amazon Venezuela/Brazil):
- Circular communal dwelling, 80-90m central plaza diameter, 10m perimeter covered ring.
- Each family builds its perimeter unit (hammocks + hearth) — they're concatenated to form the ring.
- Central plaza is shared for rituals, feasts, games.
- 50-400 person capacity.

The mechanism: **angular sector partitioning around shared central plaza** — each family-sector owns its angular slice of the perimeter with own hearth (local processing); the central plaza is the shared open communication space.

## Analogical mapping → LLM angular-sector MoE attention

- Family perimeter sector ↔ specialized attention head/expert
- Hearth ↔ specialised local KV-cache for that sector
- Central plaza ↔ shared communication channel between heads
- Angular partition ↔ context-window angular slice

The mechanism: **SHABONO-RING** — an angular-sector MoE attention design where the context window is partitioned into K angular sectors, each with its own specialised expert (attention head + per-expert FFN). Sectors process locally and write to a shared central "plaza" residual stream that is reread by all sectors at the next layer. Differs from Ring Attention (communication topology, not sector-specialised), MoE (token-routing not sector-routing), UMoE (FFN-attention sharing not central-plaza) by combining (a) angular sector partitioning of CONTEXT not tokens, (b) per-sector specialised expert FFN, (c) shared-central-plaza residual stream between sectors.

## Note on adjacency

Strong adjacency:
- Ring Attention 2310.01889 (Liu) — ring communication but not sector-specialisation
- MoE (Mixtral 8x7B) — expert routing but not angular-sector context
- UMoE 2Z0OFReqkT — shared experts between FFN and attention

Expected FAIL — angular-sector partition + central-plaza is recombinable from existing components.
