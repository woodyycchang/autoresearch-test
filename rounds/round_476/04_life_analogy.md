# Life Analogy — Slovenian Idrija bobbin lace pattern catalog

The **Idrija lace** tradition (Slovenia, since 1696; UNESCO ICH 2018):
- 40+ canonical motif patterns ("peonies", "hearts", "cradles", snowflake, etc.).
- Each motif specifies a topological signature of bobbin-crossings + twists.
- Lacemaker reads pricking template; deviation from canonical motif is visible defect.
- Repair: re-route individual bobbin paths through nearest canonical motif.
- Multi-pattern lace combines motifs via shared boundary crossings.

**IDRIJA-LACE-DEFECT**: a graph-minor topological-defect detector for attention pattern. (1) Treat per-head attention pattern as bobbin-crossings graph: nodes=tokens, edges=attention weights ≥ τ. (2) Maintain canonical motif catalog M = {peony, heart, cradle, ...} — 40 graph-minor templates extracted from healthy-model attention. (3) Per-row defect detection: graph-minor isomorphism check against M; flag rows where minor signature differs from all motifs by > δ. (4) Repair: per-row attention edge re-route to nearest canonical bobbin-graph minor via learned permutation π_repair. (5) Bobbin-path = attention edge; pricking template = canonical motif catalog.

## Adjacency
- TOHA topological divergence attention graphs 2504.10063 (closest — different metric, hallucination only)
- T3former 2510.13789 (different — temporal-graph)
- Topology-Informed Graph Transformer 2402.02005 (different — graph isomorphism not attention defect)
- Attention Head Intervention 2601.04398 (different — intervention not motif-catalog)

Expected FAIL — graph-minor + topological attention covered in TOHA + T3former clusters.
