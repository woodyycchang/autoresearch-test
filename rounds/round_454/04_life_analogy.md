# Life Analogy — Chiloé palafito stilt-house tiered tidal dwelling

The **Chiloé palafito** (Chilean Patagonia, Castro):
- Wooden piles of luma/cypress dug into intertidal mud as flexible foundation.
- Multi-tier structure: water-line pier → ground-floor dwelling → attic storage.
- Rises/falls with tides up to 10m via flexible pile geometry.
- Multi-front: street access + sea-dock terrace; interconnected via wooden bridges.
- Each tier supports different functions / persistence (boat moor / daily life / long-term storage).

**CHILOTE-PALAFITO**: a hierarchical memory architecture with three persistence tiers and adaptive flexible-pile foundation embeddings. (1) Tier-0 (Pier, fastest): recent attention KV-cache, HBM, evicted on every K tokens. (2) Tier-1 (Dwelling, working): mid-context cache, DRAM, evicted by importance-LRU. (3) Tier-2 (Attic, persistent): long-term parametric memory with periodic compression. (4) Flexible-pile foundation: shared base embeddings anchored across tiers but adapt to "tidal" data distribution changes. (5) Wooden bridges: explicit cross-tier read/write paths for sliding window attention.

## Adjacency
- Tutti 2605.03375 (3-tier HBM-DRAM-SSD)
- Strata 2508.18572 (hierarchical context caching)
- MTDS 2025 multi-tier dynamic storage
- LMCache tech report

Expected FAIL — multi-tier KV cache is dominant 2025-2026 paradigm.
