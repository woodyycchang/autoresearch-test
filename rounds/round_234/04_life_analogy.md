# R234 — life analogy

## Source domain: Sacred Harp shape-note solfège
- A learning-aid notation where each scale degree has a DISTINCT GEOMETRIC SHAPE attached to the notehead: fa = triangle, sol = oval, la = rectangle, mi = diamond (four-shape system).
- Aikin's seven-shape extends to do=four-leaf, re=cup, mi=diamond, fa=triangle, sol=oval, la=rectangle, ti=ice-cream-cone.
- The shape is the SAME pitch encoding the staff already encodes; shape is REDUNDANT but PEDAGOGICALLY-SELF-EXPLANATORY: an untrained reader can sight-sing a melody from shape alone.
- Critically: shapes carry SCALE-DEGREE invariance, not absolute pitch. Same melody transposed reuses same shapes.

## LLM analogy candidate
**Shape-redundant subword tokenizer**: in addition to the standard BPE/SentencePiece token id, attach to EVERY token a "role-shape" code from a small fixed vocabulary K (≈ 4-7) of semantic/syntactic role categories: subject-noun, predicate-verb, modifier, qualifier, connective, quote-marker, code-block-marker. The role-shape is REDUNDANT with respect to the base token id (the same string in different roles gets different role-shapes) but provides a SCALE-DEGREE-INVARIANT signal: the same syntactic-role sequence reuses the same shapes regardless of vocabulary substitution. Downstream LLM heads can attend either to token-id or to shape-id; this gives an explicit interpretability hook for circuit analysis and a robust signal for inputs where vocabulary is paraphrased or adversarially perturbed but ROLE STRUCTURE is preserved.

## What differs from prior art (claim)
Symbolic Compression (2501.18657) compresses token id; Discrete Tokenizers survey (2502.12448) classifies single-id discretization. None propose a small (4-7) role-shape vocabulary REDUNDANTLY annotating every token to provide a scale-degree-style invariant. POS-tagging is the closest classical analog but is not used as a CO-LEARNED tokenizer signal in modern LLM training; shape-note framing argues for this as a pedagogical-explicit feature added INSIDE the embedding layer.
