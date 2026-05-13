# Life Analogy — Andean khipu primary-pendant-subsidiary cord cascade with decimal-hierarchy knot encoding

The **Andean khipu** (Quechua for knot):
- Primary (top) cord + K pendant cords + L subsidiary cords (secondary, tertiary, quaternary).
- 3 knot types: E-knot (figure-8) = 1; long-knot wrapped 2-9 times = 2-9; single-knot = 10ⁿ depending on position.
- Decimal hierarchy: 1s row farthest from primary cord, 10s above, 100s, 1000s.
- Subsidiaries = corrections, exceptions, subsets — cascade refinement of primary.
- Multi-dimensional encoding: cord ply + length + end-treatment + color + spacing all carry meaning.

**KHIPU-PRIMARY-PENDANT-SUBSIDIARY-CASCADE-DECIMAL**: 4-tier hierarchical token-routing cascade with primary-pendant-subsidiary refinement + 3-knot-type token-class encoding + decimal-position scaling. (1) **4-tier hierarchy**: primary backbone P_top → pendant LLM_pendant (K-class router) → secondary LLM_sec (subset routing) → tertiary LLM_tert (correction/exception); each tier escalates only if confidence below tier-specific threshold τ_R. (2) **3-knot-type token-class encoding**: each request classified into K_types {atomic, multi-step, exceptional} (figure-8 / long / single analogues) determining the cascade depth. (3) **Decimal-position scaling factor**: token position from primary scales the model size by 10^k (1s = smallest, 10s = small-medium, 100s = medium, 1000s = largest). (4) **Subsidiary correction loop**: when downstream tier produces output, primary-tier verifies; on disagreement primary spawns a tertiary "correction subsidiary" that explicitly handles the exception. (5) **Cord-attribute multi-dim metadata**: each request carries ply (modality), length (max budget), end (output format), color (priority) attributes used by router. (6) Differs from R413 + R422 + R429 + R438 + R455 + R480 + R493 + R505 KASHAN-QANAT-CASCADE-INFOFLOW (cistern context-buffer + wind-tower thermal-attention damping + vent-shaft per-stage diagnostic + sarooj impermeable boundary, no 4-tier primary-pendant-subsidiary + no 3-knot-type encoding + no decimal-position scaling) by 4-tier khipu hierarchy + 3-knot-type classification + decimal-position model-scale + subsidiary correction loop + cord-attribute metadata.

## Adjacency
- Dynamic Model Routing Cascading LLM Survey 2603.04445
- Unified Routing Cascading LLMs OpenReview
- Cascaded LM Cost-Effective Human-AI 2506.11887
- LLM Cascade Multi-Objective 2410.08014

Expected FAIL — LLM cascade-routing + hierarchical-escalation + multi-objective trade-off literature covers.
