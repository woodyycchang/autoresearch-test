# Life Analogy — Icelandic saga teller-chain provenance

The **Icelandic sagas**:
- Multi-generational oral narratives transmitted by semi-professional saga-men.
- Many sagas CLOSE with named-teller credit ("Þorvaldr told this saga", "I heard this from X who heard from Y").
- Authentication: chains of named tellers across generations let listeners assess credibility by chain length, teller authority, family ties.
- Cross-saga consistency emerges from overlap of teller chains, not from a central canon.

The mechanism: **provenance chain at retrieval level — each fact embedded with a chain of named-prior-tellers** which enables (a) chain-length-based confidence weighting, (b) teller-authority-based filtering, (c) cross-fact consistency checking via shared-teller intersection.

## Analogical mapping → LLM RAG provenance chains

- Saga ↔ retrieved RAG document
- Named teller chain ↔ teller-trace metadata (which retriever, generator, summariser handled it)
- Chain length ↔ retrieval-step-count audit value
- Teller authority ↔ source authority (academic, official, raw-web) per retrieval step
- Cross-saga teller intersection ↔ cross-document teller graph

The mechanism: **SAGA-CHAIN** — a retrieval-memory architecture that embeds a **teller-chain provenance trail** in each memory entry: every retrieved fact carries an audit chain of all prior agents (retriever, summariser, transformer) that handled it. Query filtering supports chain-length thresholds and teller-authority-graph weighting. Cross-fact consistency checked by computing teller-intersection graph between two retrieved facts. Differs from PROV-O Prompt Provenance (prompt-level, not per-fact retrieval-level), AEVS Anchor-Extraction-Verification-Supplement (source-text grounding, not chain), ProvSEEK forensic chain-of-thought (forensic-only) by combining (a) per-memory-entry teller-chain metadata, (b) chain-length/authority weighted retrieval, (c) cross-entry teller-intersection consistency check.

## Note on adjacency

Strong adjacency to Prompt Provenance, AEVS provenance grounding, ProvSEEK chain-of-thought audit. SAGA-CHAIN's specific per-fact teller-chain + intersection-graph is small extension. Expected FAIL.
