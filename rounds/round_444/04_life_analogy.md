# Life Analogy — Toraja tongkonan ancestor house elevation lineage

The **Toraja tongkonan** (Sulawesi):
- Stilt-pile elevated 3-tier structure: ground = livestock + storage, middle = living, upper = sacred relics + heirlooms.
- Saddleback boat-shaped roof oriented N-S aligning with cosmological axis.
- Represents lineage of founding ancestor; relics/heirlooms reside at highest tier (ELEVATION = priority).

**TONGKONAN-TIER-GATE**: a 3-tier attention-gate where tokens are classified into elevation tiers — tier-3 (sacred/priority: system prompt + safety + retrieval-grounded), tier-2 (active context: recent N tokens), tier-1 (background: older context). Cross-tier attention follows ASYMMETRIC ELEVATION RULE: tier-3 → all (highest priority broadcast), tier-2 → tier-2 + tier-1, tier-1 → tier-1 only. Differs from standard sliding-window by ELEVATION-asymmetric attention pattern.

## Adjacency
- Qwen3-Next gated attention sigmoid
- Efficient Attention Mechanisms LLM Survey 2507.19595
- Big LLM Architecture Comparison gating patterns
- Modern LLM Attention 2026

Expected FAIL — tiered attention masking + priority-context gating is well-covered.
