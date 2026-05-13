# Life Analogy — Old Norse skaldic kenning

**Skaldic kennings** are nested metaphor-chains: a kenning is "two nouns referring to an unspoken third" — e.g., *"swan's road" = sea*; *"horse of the swan's road" = ship*. The chain is potentially recursive:
- Level 1: noun + noun → unspoken third
- Level 2: substitute "noun" with another L1 kenning
- Level 3: substitute again
- …

Each substitution preserves the *referent* (ship is still a ship) while increasing *encoded depth* via metaphor stacking. Skaldic verse uses kennings at L2-L4 commonly. Reader/listener decodes top-down: knows mythology + cultural references, peels back each layer.

The unique principle: **recursive substitution of unspoken-referent metaphors** with **constant referent preservation**. Each layer compresses 2 nouns into 1 conceptual referent; the chain is a **multiplicative compression cascade**.

## Analogical mapping → LLM context compression

- Kenning L1 ↔ 2-token → 1-anchor first-stage compression
- Kenning L2 ↔ 2-anchor → 1-meta-anchor second stage
- Kenning L3 ↔ 2-meta-anchor → 1-super-anchor third stage
- Cultural mythology knowledge ↔ pretrained LLM background knowledge (decode key)
- Referent preservation ↔ lossless reconstruction of original referents at output

The mechanism: a **multiplicative recursive anchor-token compression** that compresses by factor 2^N over N stages — at each stage, every pair of anchors is fused into a single higher-level anchor with referent preserved via cross-attention. Decoding uses pretrained model knowledge as the "mythology library". Differs from prior gist-token / EDU compression by being **explicitly recursive and multiplicative** (factor 2 per stage, log-depth), with **referent-preservation cross-attention** rather than reconstruction loss.
