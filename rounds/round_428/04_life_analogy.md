# Life Analogy — Maasai engang/boma concentric thorn-ring

The **Maasai engang (boma)**:
- Central cattle corral (highest-value asset; innermost).
- Surrounding ring of beehive-shaped enkaji huts (mid-priority; family dwellings).
- Outermost concentric thorn-fence (defensive boundary against lions/hyenas/raiders).
- Concentric three-tier priority-by-distance architecture.

**BOMA-RING-KV**: a concentric-ring KV-cache memory hierarchy with three explicit rings — (i) inner ring = highest-importance KV entries (computed via attention-score percentile), accessed first and never evicted; (ii) middle ring = medium-importance KVs, accessed only on miss; (iii) outer ring = low-importance defense-boundary tokens (e.g., system prompt, safety instructions, retrieval guard tokens) accessed last. Concentric access pattern enforces value-tier traversal from inner to outer. Differs from LMCache (hot/warm/cold by recency, not by attention-importance ring), IMPRESS (importance-aware single-tier prefix, not concentric ring), Tutti (SSD layout, not access ordering).

## Adjacency
- LMCache (hot/warm/cold KV tiers)
- IMPRESS multi-tier prefix KV USENIX FAST 2025
- Google Tiered KV Cache Kubernetes
- CTkvr 2-stage centroid-then-token retrieval
- KVCache-Centric Memory for LLM Agents

Expected FAIL — tiered/hierarchical KV memory by importance is saturated 2025-2026 design.
