# Life Analogy — Akan Adinkra symbol-proverb catalog

The **Akan/Asante Adinkra symbols** (Ghana):
- ~122 canonical visual symbols, each encoding a Twi proverb.
- Symbol = visual shorthand for a sentence-length wisdom.
- Symbol-proverb pairs form a SEMANTIC-LAYOUT SYSTEM ("pattern of patterns").
- Catalog functions as community memory: each symbol invokes a long moral tradition.

**ADINKRA-CATALOG**: a fixed-size canonical-symbol memory bank: K = 128 (Adinkra-cardinality) learned concept-vectors c_1..c_K each paired with a canonical-proverb retrieval token; during inference an attention probe q is routed to the catalog and retrieves the top-k symbols + their proverb-tokens for context augmentation. Differs from standard RAG (free-text passages) by FIXED CANONICAL CATALOG with paired retrieval-tokens.

## Adjacency
- Vector Stores LLM Memory canonical RAG
- A-MEM Agentic Memory 2502.12110
- LLMs Meet Vector Databases Survey 2402.01763
- Memory Patterns canonical-prompt retrieval

Expected FAIL — concept-vector memory bank + proverb-token retrieval is canonical RAG paradigm.
