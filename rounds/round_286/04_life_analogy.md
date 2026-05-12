# R286 — life analogy

## Source: Madagascar baobab seasonal water-storage trunk
- Trunk physically SWELLS in wet season (stores ~120,000 L), SHRINKS in dry season (-2-3 cm circumference, -12% water).
- Stored water is RELEASED to flush new leaves at end of dry season, before rains return.
- KEY: storage organ is the SAME physical body that does structural support; storage is an emergent property of low-density parenchyma + fiber arrangement.

## LLM analogy
**BAOBAB (Buffered Activation-Storage with Off-peak Elastic Allocation)**: an LLM serving architecture where the SAME PARAMETER MEMORY POOL serves both (a) live attention/activation computation and (b) ELASTIC OVERFLOW STORAGE for sequences that exceed nominal context — the pool expands during off-peak (low concurrent traffic), absorbing context-overflow into normally-unused parameter slack, and contracts at peak. Storage is opportunistically reclaimed from low-priority weights via temporary low-rank approximation while traffic spikes; restored at off-peak.

## Differs from prior art (claim)
- eLLM (2506.15155): elastic memory but uses separate buffer pool, not parameter slack repurposing.
- dLLM-Serve (2512.17077): handles oscillating footprints but for diffusion LLMs, not via parameter-pool repurpose.
- MemAscend (2505.23254): SSD offload — different storage tier.
- BAOBAB's claim: USE THE PARAMETERS THEMSELVES as elastic storage during dry season, restoring them at off-peak — collapse-and-rehydrate of low-priority parameters via temporary low-rank.
