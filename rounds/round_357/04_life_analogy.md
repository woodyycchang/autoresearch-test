# Life Analogy — Mongolian khoomei throat singing

Khoomei (Mongolian throat singing) is a vocal technique where a single singer produces TWO simultaneous pitches:
- A low **fundamental** rumble (chest/diaphragm).
- A high **overtone** whistle (vocal-tract resonance, selecting specific partials — 6th, 7th, 8th, 9th, 10th, 12th, 13th harmonics).

The two pitches are produced *from the same airflow*, *at the same time*, but exist in *frequency-disjoint bands*. The high whistle melody is heard distinctly *because* it lives at high partial frequencies that don't interfere with the low fundamental.

Key features:
- **Single source, two outputs**: one breath produces two harmonically related pitches.
- **Frequency disjoint**: low band and high band cannot mask each other.
- **Selectable partial**: singer chooses which harmonic to amplify by vocal-tract shape.
- **Spectral allocation**: low band = continuous text/word substrate; high band = melodic line.

## Analogical mapping → LLM dual-band decoder

- Fundamental (low band) ↔ verbose / standard token decoder stream
- Overtone (high band) ↔ compressed / summary / annotation stream
- Frequency disjoint ↔ output tokens drawn from disjoint vocabulary subspaces (e.g., text + tags)
- Selectable partial ↔ runtime selection of which secondary stream is active
- Single airflow source ↔ shared base trunk producing both streams in one pass

The mechanism: a single shared trunk produces TWO simultaneous output streams in vocabulary-disjoint subspaces — e.g., low-band = standard text; high-band = structured metadata/citations/tags — neither suppressing the other, both decodable in one inference pass.
