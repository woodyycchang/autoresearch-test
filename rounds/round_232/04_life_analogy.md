# R232 — life analogy

## Source domain: Victorian floriography / Turkish selam
- A nosegay (tussie-mussie) encodes a MESSAGE via a COMPOSITION of flowers, herbs, ribbons, and POSITION-of-presentation (right hand = yes, left hand = no). Each constituent has a dictionary entry.
- Meaning is COMPOSITIONAL but the surface text (the bouquet) is a benign-looking gift; the message decodes only with the shared dictionary.
- Selam additionally uses rhyme-aware substitution: flower-name rhymes with the actual message-word in Turkish.

## LLM analogy candidate
**Floriography-style adversarial prompt detection**: not at the level of single-token / single-phrase classification, but at the level of COMPOSITIONAL CODE. Train a "floriography classifier" head that takes the FULL prompt + tool-call sequence + ANY referenced file metadata + the user's task context AND scans for compositional signatures: presence of K specific dictionary terms in a structured arrangement (Turkish-selam-style "every Nth noun" pattern), benign-cover-text + steganographic embedding, position-conditioned meaning (which paragraph the key term occurs in determines its semantic role). The classifier outputs a "bouquet decode score": likelihood that the prompt is a compositional adversarial message rather than its surface text. Critical: scan must be COMPOSITIONAL — single-token detection is insufficient.

## What differs from prior art (claim)
Semantic Intent Fragmentation Attack (2604.08608) is the ATTACK side; the floriography classifier is the DEFENCE side based on compositional dictionary decoding. Compositional Steering (2601.05062) uses steering tokens for behavior control, not message-decoding for prompts. None apply the floriography-dictionary discipline as a detection layer for compositional adversarial prompts.
