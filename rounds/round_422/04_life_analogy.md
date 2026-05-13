# Life Analogy — Norse bind-rune (ligature of 2-3 runes into single glyph)

**Bind rune** (Migration-era Germanic):
- Two or three adjacent runes are FUSED into a SINGLE GLYPH.
- Common construction: shared vertical stroke (stave) between runes.
- Same-stave variant: multiple runes along one long stem-line.
- Practical: space-saving + carving-error tolerance + stylistic.
- The bind-rune is a NEW glyph but DECOMPOSES into the original runes when read.

The unique principle: **fusion of 2-3 atomic symbols into one compound glyph WITH preserved decomposability** — the compound glyph occupies one slot but its meaning is the conjunction of its constituent runes. Reading requires knowing the alphabet AND the ligature convention.

## Analogical mapping → fixed-2-token conjunction merge in tokenizer

- Two adjacent runes ↔ a 2-token pair (t1, t2) with HIGH BIGRAM FREQUENCY
- Bind-rune fusion ↔ a TOKENIZER-LEVEL deterministic merge into a single token T_bind = t1⊕t2 with reserved id
- Preserved decomposability ↔ at decoding, T_bind splits back to (t1, t2)
- Same-stave variant ↔ a span of K>2 consecutive tokens merged

The mechanism: **BIND-RUNE 2-token ligature conjunction merge** — augment the BPE/Tiktoken tokenizer with a fixed PRE-ENCODE merge table of HIGH-MUTUAL-INFORMATION token pairs (computed once on calibration corpus, top-N=4096 such bigrams). At ENCODE time, every occurrence of (t1, t2) where (t1,t2) ∈ MergeTable is replaced by T_bind(t1,t2). At DECODE time, T_bind splits back to (t1, t2) before being passed to downstream tokenizer logic. Reduces sequence length by ~10-20% for frequent bigrams without retraining the LLM (T_bind shares the embedding of t1 + t2 averaged or summed). Differs from (a) standard BPE (learns single-token merges of all char pairs), (b) SuperBPE (cross-word superwords during training), (c) LiteToken (removes residues), (d) BoundlessBPE (cross-boundary merges during training), (e) multi-token prediction (decoder-side prediction) by combining (i) FIXED-PAIR HIGH-MI merge table + (ii) POST-HOC tokenizer augmentation NO LLM RETRAIN + (iii) DECODE-TIME split.

## Note on adjacency

The conjunction form fits. Adjacent: BPE, SuperBPE, BoundlessBPE, LiteToken, token merging. Distinct: POST-HOC FIXED-PAIR table with NO LLM RETRAIN — most BPE variants require retraining.
