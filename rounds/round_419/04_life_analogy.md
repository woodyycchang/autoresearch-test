# Life Analogy — Madagascar ravinala traveler's palm (planar fan + orthogonal water store)

The **ravinala** (Madagascar traveler's palm):
- Tall stem with leaves growing in a **single planar fan**, often oriented east-west.
- Each leaf base (petiole) cups water in a **reservoir** orthogonal to the fan plane.
- The plant survives drought via this water hoard — passive accumulation, no active pumping.
- The fan's planar shape + leaf-base cup means the fan plane (horizontal data exchange via leaves) and the cup (vertical hoard) are ORTHOGONAL functional axes.

The unique principle: **single-axis fan for primary function + orthogonal off-axis reservoir for stress reserve** — the plant's primary photosynthetic function happens in the fan plane; its drought-survival memory happens in the orthogonal cup. The two axes don't interfere; the reservoir is held in "off-band" capacity.

## Analogical mapping → orthogonal off-axis KV cache basin-stable reserve

- Fan plane (primary photosynthesis) ↔ main attention compute on standard KV cache
- Leaf-base water cup (orthogonal reserve) ↔ an orthogonal RESERVE-BASIN KV cache for low-attention tokens
- Drought triggers reservoir use ↔ KV-cache-pressure (memory full) triggers spillover to reserve
- Orthogonal axes don't interfere ↔ reserve KV stored in low-rank orthogonal subspace of main KV

The mechanism: **RAVINALA orthogonal basin-stable KV reserve** — augment standard KV cache with a SECONDARY ORTHOGONAL RESERVE-BASIN cache. Compute reserve_KV_t = Proj_U⊥(KV_t) where U is the top-k principal direction of the primary KV cache. When primary cache exceeds memory budget, EVICTED tokens have their reserve_KV preserved in the reserve basin (low-rank orthogonal storage). On retrieval requiring evicted token, REHYDRATE primary_KV ≈ Proj_U(prior_value) + reserve_KV. Differs from (a) standard KV eviction (drops evicted token entirely), (b) KV quantization (lossy compression of ALL tokens), (c) MTDS hierarchical storage (multi-tier copy not orthogonal decomposition), (d) PagedAttention (paging not decomposition), (e) Streaming-LLM attention sink (keep selected positions, not decomposition) by combining (i) ORTHOGONAL decomposition + (ii) RESERVE BASIN for evicted tokens + (iii) REHYDRATION via projection sum.

## Note on adjacency

The basin-stability form fits. Adjacent: MTDS hierarchical KV cache, low-rank KV decomposition (ESPACE, FLAT-LLM), Streaming-LLM attention sink. Distinct: ORTHOGONAL DECOMPOSITION reserve specifically for EVICTED tokens with REHYDRATION.
