# Life Analogy — Aboriginal songline (Dreaming-track route memory)

**Songlines** are Aboriginal Australian oral routes:
- Lyrics encode geography precisely — landmarks, waterholes, terrain.
- Singing in correct sequence reproduces the route.
- Each step in the song corresponds to a SPATIAL waypoint.
- The lyrics form an ORDERED, SEQUENTIAL memory anchored to landscape positions.
- Songlines transmit genealogy, kinship, ecology in addition to navigation.

The unique principle: **ordered-sequential memory anchored to spatial waypoints, retrieved by traversing the sequence**. Differs from generic key-value memory by being INTRINSICALLY SEQUENCED.

## Analogical mapping → LLM agent memory

- Songline route ↔ ordered chain of memory anchors
- Each lyric step ↔ memory entry at position k
- Singing sequence ↔ retrieval-by-traversal
- Landmark waypoint ↔ memory anchor's spatial-semantic key

The mechanism: a **songline external memory** for LLM agents — memory entries are stored as an ORDERED SEQUENCE M[0], M[1], …, M[K-1] (not key-value). Each entry has a SPATIAL-SEMANTIC ANCHOR (e.g., physical location in agent's environment, document page index). Retrieval is by TRAVERSAL: agent specifies a starting anchor and a direction; system returns the next-K entries in sequence. Differs from H-MEM/GAM/A-MEM (random-access semantic retrieval) by being SEQUENTIALLY-ORDERED and TRAVERSAL-BASED rather than similarity-keyed.
