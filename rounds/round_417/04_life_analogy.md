# Life Analogy — Veps Karelian itkuvirsi decrescendo lament

The **Karelian itkuvirsi (lament)**:
- Ritualistic weeping by women at funerals/weddings.
- Verse cycles repeat similar lyrical material with progressive emotional decrescendo across cycles.
- Decrescendo signals lifecycle stage — initial intense → diminishing intensity → final whisper.

**VEPS-DECRESCENDO**: query-response amplitude decrescendo where successive paraphrases of same question produce progressively-lower-confidence output. Each paraphrase cycle k receives a calibrated confidence-decay factor α^k applied to logits. Final answer = lowest-confidence (most-doubted) response; intermediate cycles surface what the model is unsure about.

## Adjacency
- Uncertainty Propagation 2604.23505 (sequential history)
- Verbalised Confidence Elicitation 2306.13063
- Paraphrase consistency benchmarks (JMIR 2025)

Expected FAIL — repeated-paraphrase uncertainty growth is established.
