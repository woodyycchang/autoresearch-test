# R251 — life analogy

## Source domain: Persian qanat
- Multi-element underground water delivery system:
  1. **Mother well** (single 0.8-1.0 m diameter cylindrical shaft sunk into aquifer fan, up to 300 m deep)
  2. **Infiltration gallery** (horizontal tunnel cutting through saturated aquifer; water seeps in across length)
  3. **Cascade of ventilation shafts** at regular intervals (50-100 m apart) used for spoil removal + air circulation during construction + later for inspection/cleaning
  4. **Gentle downhill slope** (0.1–0.2%) carrying water by gravity to the **mazhar (emergence)** kilometers away
  5. Built by **muqannis** in stages; shafts dug downward at intervals, then horizontal tunnel connects each shaft
- Key principle: a long distributed pipeline that **infiltrates** along its full body (not just at a single source), with periodic shafts as access points enabling inspection, intermediate observation, and incremental construction.

## LLM analogy candidate
**Cascaded-shaft long-context retrieval gallery (CSLRG)**: model long-context retrieval as a horizontal "infiltration gallery" through which a hidden-state stream flows from a "mother well" (initial deep encoding of question) to a "mazhar" emergence (final answer). At regular token-distance intervals (every Δ=512 tokens), install a **shaft** = a small auxiliary classifier (4-layer MLP) that (a) extracts an intermediate observable state, (b) decides whether the local span "infiltrates" the answer-aquifer (i.e., contains retrieval-relevant evidence), and (c) optionally pushes selected token KV entries into a sparse global **gallery cache**. Crucially, the gallery cache is itself a thin slope-along-tokens cascade: each shaft only writes a single low-rank summary vector AND a pointer back to its span. Final decoding "drains" the gallery cache rather than full KV. Calibrated by an auxiliary loss enforcing that shaft-classifier acceptances correlate with downstream answer accuracy on held-out probes.

## What differs from prior art (claim)
IC-Cache (2501.12689) and Fusion RAG Cache (2601.12904) cache retrieval results at prompt/prefix boundary; they do not install **periodic** mid-stream shafts during long-context decoding. Continuous Semantic Caching (2604.20021) is fully continuous, not discrete-shaft. Cache-to-Cache (2510.03215) is inter-LLM, not intra-LLM. Token-pruning / dynamic sparse attention is related but pulls from existing KV rather than building a separate gallery with periodic shafts. The qanat-spaced periodic-shaft + gallery-cache + mother-well-deep-encoding triad with calibrated shaft-acceptance is not retrieved in surveyed prior art.
