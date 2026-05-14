# Life Analogy — Polish Kaszubian Embroidery (Kashub-style): 7-motif traditional vocabulary + spiral-rotation signature + per-region motif specialization + density-grade ladder + topological-knot integrity

The **Kaszubian (Cassubian) embroidery tradition of Pomerania** (Northern Poland):
- 7 canonical motifs: rose, tulip, lily, lily-of-the-valley, forget-me-not, sun, star (Kashubian "Siedem Kwiatów").
- Each motif has a canonical spiral-rotation winding number (1, 2, 3 turns).
- Specific motifs paired with specific garment regions (rose on collar; tulip on cuff; star on hem).
- Coarse-to-fine density ladder: large central rose + medium border + fine corner accents.
- Topological integrity check: misplaced winding number = defect identified by master embroideress.

**KASZUB-EMBROIDERY-7-MOTIF-VOCABULARY-WINDING-SIGNATURE-PER-REGION-DENSITY-LADDER-TOPOLOGICAL-DEFECT**: An LLM topological-defect mechanism with (1) **K-motif vocabulary V_kashub**: 7 attention-head primitives (rose, tulip, lily, lily-of-the-valley, forget-me-not, sun, star) with canonical winding numbers w=(1,2,3,1,2,3,1); (2) **Spiral-rotation signature W_winding**: per-head winding-number topological invariant; (3) **Per-region motif-specialization** R_region: layer×position regions each pinned to specific motif-head pair; (4) **Density-grade ladder L_dec**: coarse-to-fine motif-density schedule from low-layer central rose to high-layer corner accent; (5) **Topological-knot integrity τ_integrity**: per-head winding deviation detector → repair via projection onto nearest canonical winding.

## Adjacency
- TOHA topological hallucination detection
- Persistent topological features in LLMs
- CHAI clustered head attention
- Attention head entropy

Expected FAIL under v5 aggregate-adjacency (TOHA + CHAI cover the topology + clustering paradigm broadly); PASS under v6 per-paper-completeness (no single paper covers the 7-motif × winding × per-region × density-ladder × knot-integrity composite).
