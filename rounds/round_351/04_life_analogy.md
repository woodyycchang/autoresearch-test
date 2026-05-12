# Life Analogy — Saraiki dohra parallel-couplet redundancy

The Saraiki **dohra** is a two-line couplet form (Punjabi/Saraiki tradition) where the second line repeats or completes a thematic anchor from the first, often using parallel grammatical structure. Sufi-tradition dohras stack many semantically-redundant couplets in sequence so a listener who misses one couplet still receives the same anchor meaning from the next — a form of **lossy-channel error-correction by content repetition with structural parallelism**.

The two lines share grammatical scaffold; the listener decodes the anchor word once and uses parallel structure to fill in elided content. Multiple dohras stacked create N-way **semantically redundant attention to the same anchor concept** at different positions in the recitation.

## Analogical mapping → LLM decoding

- Dohra couplet line 1 ↔ primary decoded token sequence
- Dohra couplet line 2 ↔ parallel redundant decoded chunk grounded in the same anchor token
- Anchor word ↔ semantic-anchor token in the decoder's KV
- Stacked dohras ↔ N parallel decoder branches voting on the same anchor

The mechanism is parallel decoding where each branch is forced to re-route attention back to one shared semantic-anchor token, providing N-way confirmation of the anchor-grounded chunk.
