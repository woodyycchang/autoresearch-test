# Life Analogy — Mongolian khoomei undertone-harmonic judge

The **khoomei** (Mongolian/Tuvan throat singing):
- Singer hums fundamental + selectively amplifies harmonic overtones (6th-13th partial).
- Kargyraa technique produces undertone exactly ½ fundamental.
- Sygyt-style merges formants to filter single overtone against stable fundamental array.
- Master judges deviation from clean overtone signal audibly: "pitch slip" = defective; "clean overtone" = approved.

**KHOOMEI-PARTIAL-JUDGE**: harmonic-partial-anchor LLM-judge with fundamental-reference + per-partial rubric. (1) For each generation, extract candidate output's "fundamental" (gist embedding e_F) + K harmonic "partials" {e_F + h_k · δ} as multi-aspect projections. (2) LLM-judge scores each partial against rubric anchored to fundamental: deviation_k = ||predicted_partial − ideal_partial(e_F, k)||. (3) Aggregate verdict: passes only if ALL K partial-scores deviate < τ_clean AND fundamental matches reference. (4) Defect localization: per-partial score identifies which aspect (factuality / coherence / structure / completeness) slipped. (5) Multi-criterion rubric tied to fundamental anchor, not free-floating dimensions.

## Adjacency
- Prometheus rubric-refinement 2026 (closest)
- REVISEVAL LLM-Judge calibration
- Multi-Agent LLM Judge Cao et al 2025
- LLM-as-Judge templates Arize / Monte Carlo

Expected FAIL — multi-criteria rubric-anchored LLM-Judge fully covered.
