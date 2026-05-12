# R315 — life analogy

## Source: Inuit igloo catenary compression dome
- Snow blocks laid in spiral pattern, leaning ~15° inward per row.
- Final structure approximates catenary arch — natural curve of a hanging chain under gravity.
- Catenary distributes load into pure compression; no bending moments or tensile stress.
- Compacted snow handles 1-5 MPa compressive strength.

## LLM analogy
**IGLOO-NORM**: pre-compute a CATENARY weight-distribution profile across attention heads at each layer. Heads are pre-normalized such that compute load (FLOP intensity per token) follows a catenary curve from highest-load central head to lowest-load peripheral heads. Load balancing is ARCHITECTURAL (encoded in pre-normalization), not dynamic (no runtime router). At inference, head-load distribution stays balanced even under uneven token-difficulty pressure.

## Differs from prior art (claim)
LIBRA predicts and balances MoE expert load dynamically. Block (2508.03611) balances LLM serving load. Multi-query and grouped-query attention reduce KV. IGLOO-NORM is a STATIC pre-normalization for catenary head-load — but pre-normalization of weight distribution is mainstream (e.g., GQA, MQA, layer-norm tuning).
