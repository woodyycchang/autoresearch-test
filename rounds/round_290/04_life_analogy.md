# R290 — life analogy

## Source: Quipu Inca knot-cord recording system
- Information is encoded along MULTIPLE INDEPENDENT AXES on a single cord:
  - Knot TYPE (single, long, figure-8) — symbolic class.
  - Knot POSITION on cord — decimal magnitude (ones/tens/hundreds).
  - Cord COLOR — categorical channel.
  - Cord SPIN direction (S vs Z ply) — sign/polarity bit.
  - Cord FIBER (cotton vs camelid) — meta-channel.
  - HIERARCHICAL ATTACHMENT: pendant cords attach to primary cord; subsidiary cords attach to pendants → tree of cords.
- The data structure is a TREE of multi-channel-encoded cords; reading requires a kamayuq (specialist).

## LLM analogy
**QUIPU-TOK (Multi-Axis Composite Token Encoding)**: token representation augmented with multiple ORTHOGONAL CATEGORICAL CHANNELS combined at embedding-lookup time:
- Channel 1: standard word-piece token.
- Channel 2: discrete "color" tag (semantic-category, e.g., domain tag, sentiment tag).
- Channel 3: discrete "spin" tag (polarity / negation / hedge).
- Channel 4: discrete "fiber" tag (modality / source).
- Channel 5: explicit hierarchy attachment (parent-cord pointer = parent-token positional reference).
- Embedding for the token = SUM of per-channel embeddings + hierarchical structure encoding.

## Differs from prior art (claim)
- Contextually Structured Token Dependency (2501.18205): structured dependency encoding, but generally one-dimensional.
- LLM Tabular Embeddings (2502.11596): numerical+categorical, but only for tabular tasks.
- Hybrid Tabular Tokenization (2508.01685): tabular structure injection.
- QUIPU-TOK: explicit 5-channel composite categorical embedding with hierarchy-attachment in general LLM text tokens — not yet a published encoding scheme combining all 5 axes.
