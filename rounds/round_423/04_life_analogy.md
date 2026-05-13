# Life Analogy — Trobriand kula ring opposing-handedness exchange

The **Trobriand kula ring** (Massim 18-island):
- Soulava (red shell necklaces) flow CLOCKWISE; mwali (white shell armbands) flow COUNTER-CLOCKWISE.
- The two paired flows form a topological orientation pair — every reciprocal exchange involves a soulava AND a mwali going opposite ways.
- Parity violation (cycling same-direction) = ritual breach.

**KULA-PARITY**: topological-defect detector for paired bidirectional attention. Each layer has two attention modes — FORWARD (causal, left-to-right) and BACKWARD (acausal, right-to-left, sliding-window). Each token-pair (i,j) carries a parity signature s_{ij} = sign(attn_fwd[i,j] - attn_bwd[j,i]); the sum Σ s_{ij} over a context should be constant (KULA conservation). Deviation = topological defect ∝ likely hallucination.

## Adjacency
- TOHA Topological Divergence Hallucination Detection 2504.10063
- LLMs+TDA (Wang)
- Bidirectional attention (BERT etc.)

Expected FAIL — topology-based hallucination + bidirectional attention have direct twins.
