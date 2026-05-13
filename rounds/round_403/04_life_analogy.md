# Life Analogy — Welsh cynghanedd (cross-harmony consonant mirroring)

**Cynghanedd Groes** ("cross-harmony"), the strictest of the four Welsh cynghanedd forms, requires:
- A line is split at the cæsura into two halves.
- The CONSONANTS of the first half must be MIRRORED, in order, in the consonants of the second half (excluding the final unstressed syllable in some sub-rules).
- Plus internal rhyme between the accented syllables of each half.
- E.g., "Clear cold day" / "claered cwâl dair" — c-l-r-c-l-d ↔ c-l-r-c-l-d ordered consonant correspondence.

The unique principle: **ordered consonant-class correspondence between two halves of a structured unit, enforced as a HARD constraint (not a soft preference)** with hierarchical sub-rules (Groes strict, Draws partial, Sain hybrid). The bard must construct meaning under this constraint — the constraint isn't free decoration, it shapes lexical choice.

## Analogical mapping → constrained-pretraining loss

- Line ↔ a structured token-pair construct (e.g., 2 consecutive sentences in pretraining)
- Cæsura ↔ middle-token split
- Consonant ↔ a learnable "consonant-class" embedding category over token vocabulary
- Mirroring across cæsura ↔ a constraint on the learned representation such that the half-sequence-of-consonant-class-IDs of the first half MATCHES the half-sequence-of-consonant-class-IDs of the second half
- Hard constraint ↔ a pretraining loss term that penalizes mismatch

The mechanism: **CYNGHANEDD-MIRROR consonant-class symmetry pretrain** — augment standard pretraining with an auxiliary loss L_cyn that requires, for token-pair-sequences (sentence A, sentence B) sampled with a structural symmetry signal (e.g., A is a paraphrase of B, or A ↔ B is a parallel construction), the learned MIDDLE-LAYER representation of (a_1, ..., a_n) and (b_1, ..., b_n) shares an ORDERED CLASS SEQUENCE under a learnable K-class clustering of token embeddings. Concretely: cluster every token embedding into K classes (K~32) by a learnable codebook; for paired sentences in the augmented corpus, enforce L_cyn = sum_i |cluster_id(a_i) - cluster_id(b_i)| as auxiliary loss term. Differs from (a) contrastive pair loss (works on full embeddings not class sequences), (b) span-masking BERT (no pair-symmetry), (c) Beyond-Multi-Token-Prediction future-summary (different artefact — future not symmetric) by using a CONJUNCTION of (i) discrete K-class codebook over tokens + (ii) ORDERED class sequence correspondence across paired sentences as auxiliary pretraining loss.

## Note on adjacency

The "conjunction" form fits: candidate combines an existing component (vector quantization codebook over token embeddings, as in VQ-VAE/MEGABYTE) with another existing component (paired-sentence pretraining, as in T5 paraphrase pretraining) under a NEW objective (ordered class-sequence match). Closest twin: contrastive pretraining with paired sentences. Distinct: discrete class sequence not embedding similarity; ordered position-by-position match.
