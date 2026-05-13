# Life Analogy — Tuvan ovoo cairn waypoint memory

The **ovoo** (Tuvan/Mongolic):
- Cairn-of-stones at mountain passes, crossroads, springs.
- Travelers add a stone, request a prayer, circle clockwise 3 times.
- Tiered landmark: high-altitude pass-tier (longest sight-radius), crossroads-tier (route-junction), spring-tier (water-resource).
- Each ovoo accumulates contributions from many passing travelers — a community-curated landmark database.

**OVOO-LANDMARK-TIER**: a spatial-landmark memory architecture for LLM agents. (1) Maintain 3 tiers of landmark memory: high-altitude (rare-but-broad summaries), crossroads (junction-routing landmarks linking sub-tasks), spring (resource-providing factual nodes). (2) Each landmark = (key=spatial-hash of query context, value=top-K curated retrieval pointers, accumulation_count=N_visits). (3) Write: on each query, deposit a stone (insert pointer into nearest landmark in current tier). (4) Read: clockwise 3-pass — query each tier 3 times accumulating retrieved evidence. (5) Tier-eviction: low-visit landmarks demoted; high-visit landmarks promoted to higher tier.

## Adjacency
- HMT Hierarchical Memory Transformer NAACL 2025 (closest)
- ByteRover Agent-Native Hierarchical Memory 2604.01599
- Agent Memory Survey 2603.07670
- MemPalace Spatial Metaphor 2604.21284
- MemGPT tiered memory

Expected FAIL — tiered hierarchical agent memory paradigm heavily covered.
