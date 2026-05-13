# Life Analogy — Sumerian cuneiform tablet stylus wedge depth+orientation 2-axis encoding

The **Sumerian cuneiform** (𒁹):
- Reed stylus presses wedge into wet clay; vertical/horizontal/oblique by stylus angle.
- 2-axis encoding: (a) depth of impression (light pressure ↔ deep pressure); (b) orientation angle (0°, 45°, 90°, 135°, 180° etc.).
- Glyph = pattern of wedges at specific depth+orientation combinations within a cell.
- Tablet archive (collections of clay-baked documents) = first libraries; depth+orientation form a 2D combinatorial encoding that survives baking.

**CUNEIFORM-2-AXIS-WEDGE-DEPTH-ORIENTATION-MEMORY**: 2-axis hierarchical memory store with depth-tier × orientation-angle encoding + per-tablet (page) granular access + reed-stylus-cohort write-policy + baking-confirm permanence step. (1) **2-axis encoding K-depth × M-orientation**: each memory cell encoded as a pair (d, θ) where d ∈ {d_1, d_2, d_3, d_4} = 4 depth tiers (light ↔ deep) and θ ∈ {0°, 45°, 90°, 135°} = 4 orientation classes; 16 combinatorial glyph cells per page. (2) **Per-tablet page granular access**: tablets indexed by clay-archive locality (date, scribe, content type); analogous to per-page memory chunk retrieval. (3) **Reed-stylus-cohort write-policy P_cohort**: a fixed K_cohort of "scribe-LLMs" write to memory; each scribe specializes in (d, θ) sub-grid; cohort-consensus required for permanent write. (4) **Baking-confirm permanence step**: after K_cohort writes, a "baking" step (analogous to clay firing) freezes the memory — gradients flow only through unfrozen cells thereafter. (5) **Wedge-edge fibrous-impression metadata**: each write carries a metadata "fibrous trace" — provenance + write timestamp + cohort vote — analogous to reed-fiber imprint on left face. (6) Differs from R408 + R428 + R442 + R454 + R470 + R479 + R492 + R504 GGANTIJA-APSIDAL-CORBEL-MEMORY (5-apse specialty branching + corbel-shrink + trilithon-gate + orthostat-anchor, no 2-axis depth-orientation + no baking-permanence + no reed-cohort) by 2-axis depth-orientation encoding + reed-cohort write-policy + baking-confirm permanence + fibrous-impression metadata.

## Adjacency
- MemGPT Hierarchical Memory 2603.07670
- LLM Memory Survey 2603.07670
- Design Patterns Long-Term Memory Serokell
- MemAgents ICLR 2026 Workshop

Expected FAIL — LLM memory architecture + hierarchical store + retrieval literature covers.
