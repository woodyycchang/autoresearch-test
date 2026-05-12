# Life Analogy — Berber tifinagh consonantal abjad

**Traditional Tifinagh** is a consonantal abjad:
- Writes only consonants (vowels reader-supplied).
- Vowels appear word-finally only.
- Reader fills vowels from context + oral knowledge.
- Approx 30% character reduction vs. fully alphabetic.
- Disambiguation handled by reader's linguistic context.

The unique principle: **deliberately incomplete encoding that defers vowel reconstruction to a reader's prior**. The encoding is sparse + lossy at the surface level but reliably reconstructible given context.

## Analogical mapping → LLM tokenization

- Tifinagh consonants ↔ kept tokens
- Reader-supplied vowels ↔ context-filled missing tokens
- Word-final vowels ↔ explicit anchor tokens
- Reader's prior ↔ LLM's contextual completion ability

The mechanism: a **CONSONANT-SPARSE TOKENIZER** for low-resource languages — drop a fraction (e.g., 30%) of high-frequency tokens (analog of vowels) from the vocabulary; at inference time, the LLM's contextual completion fills the gaps. Differs from BPE / SentencePiece (full coverage) and BoundlessBPE (boundary relaxation) by intentionally OMITTING a class of frequent tokens and relying on contextual reconstruction. Token-count reduction → faster inference for tokenization-premium low-resource languages.
