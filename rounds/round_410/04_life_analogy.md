# Life Analogy — Madagascan famadihana cyclical reburial

The **Madagascan famadihana** ("turning of the bones"):
- Every 5-7 years, families exhume ancestors from family crypts.
- Bones are rewrapped in fresh silk (lamba mena) and family names are rewritten on the cloth.
- Community dances around the tomb in celebration before reburial.
- Belief: spirits only finally join the ancestral world AFTER complete decomposition + cycles of rewrapping.

The mechanism: **periodic refresh of stored ancestral state** — old remains are NOT discarded; they're cyclically RE-WRAPPED with fresh material and reburied, preserving the original while accumulating new wrappings. Each cycle adds a layer of "freshness" without losing identity.

## Analogical mapping → LLM cyclical checkpoint refresh

- Family crypt ↔ checkpoint registry
- Old bones ↔ stored model checkpoint
- Lamba mena fresh wrapping ↔ continued pre-training on fresh data
- Name rewriting ↔ metadata refresh (version tag, freshness timestamp)
- 5-7 year cycle ↔ periodic refresh epoch
- Communal dance ↔ ensemble inference using old + freshly-wrapped model versions

The mechanism: **FAMADIHANA-CYCLE** — a periodic checkpoint-refresh training method. Every K training epochs (e.g., every 5 epochs), the system: (1) loads the OLDEST stored checkpoint from registry, (2) wraps it in fresh data — applies continued pre-training on data drawn from CURRENT distribution for one mini-epoch, (3) writes the refreshed checkpoint back to registry with new freshness-tag while PRESERVING the original. At inference, ensemble inference uses the K-most-recent-wrapping versions, weighted by recency. Differs from SSR Self-Synthesized Rehearsal (synthetic data not recycled checkpoint), SSU Source-Shielded Updates (parameter freezing not cyclical refresh), continual pretraining (single direction not cyclical) by combining (a) PRESERVED-ORIGINAL checkpoint storage, (b) PERIODIC re-wrapping with fresh data, (c) ENSEMBLE inference over wrapped versions.

## Note on adjacency

Strong adjacency:
- Continual pretraining 2401.03129
- SSR self-synthesized rehearsal (different — synthetic not cyclical)
- SSU source-shielded updates (different — freezing not wrapping)
- LoRA snapshot history (similar — versioned adapters but not cyclical refresh)

Expected FAIL with strong adjacency to continual-learning literature.
