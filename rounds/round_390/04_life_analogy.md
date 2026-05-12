# Life Analogy — Sami yoik (wordless vocal song)

**Yoik** is the traditional Sami (Sápmi indigenous) singing style:
- Often **wordless** — uses syllables/vocables, not words.
- Melody + rhythm carry the meaning, not text.
- A yoik does not describe a subject; it **conjures** the subject.
- One of oldest surviving singing traditions in Europe — predates conventional word-language structure.
- The performer chooses subject (loved one, animal, landscape) and yoiks them into presence.

The unique principle: **wordless pre-linguistic vocal channel** that operates BELOW the text/token level, carrying meaning through prosody + melody + rhythm directly.

## Analogical mapping → LLM context-gating

- Text words ↔ standard text tokens
- Wordless yoik syllables ↔ pre-token acoustic-feature channel
- Melody + rhythm carrying meaning ↔ prosody-only feature stream that gates text generation
- Conjuring subject ↔ generating output conditioned on prosodic features rather than tokens

The mechanism: a **prosody-only context channel** for LLM generation — alongside the standard text input, the model receives a SECOND non-text channel consisting of {pitch contour, duration, energy} prosodic features extracted from yoik-style demonstration speech. This channel is fed via cross-attention into intermediate layers and GATES the text-generation distribution: the model's generation prosody is conditioned by the yoik channel even when no words are present. Differs from ProsodyLM (which uses word-level prosody tokens ON TOP of text tokens) by being a separate WORDLESS channel that PRECEDES tokenization and serves as a context-gating signal independent of word boundaries.
