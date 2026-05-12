# Life Analogy — Yiddish badkhn (wedding bard)

The **badkhn** was the Ashkenazic Jewish wedding bard/jester. Features:
- Improvised **rhyming verse on the spot** for specific persons (bride, groom, in-laws).
- Standing rhymes (*shtey gramen*) — composed live during the event.
- **Person-specific content** drawing on details just learned (bride's family, deed accomplished).
- Audience-evaluated quality: if rhymes don't fit, badkhn loses status.
- Master of ceremonies guiding the wedding through stages.

The unique principle: **person-specific live-improvised verse evaluated by audience for both creativity and accuracy** — quality depends on relevance + originality jointly, not just one.

## Analogical mapping → LLM evaluation diagnostic

- Badkhn ↔ generative LLM under test
- Bride/groom-specific content ↔ test prompt with target persona / facts
- Audience ↔ evaluator
- Quality of rhymes ↔ joint creativity-accuracy metric

The mechanism: a **dual-axis evaluation diagnostic** for LLM generative output — for each test prompt, the evaluator computes BOTH (a) creativity score (semantic novelty against base-corpus) AND (b) factual-accuracy score (against ground-truth target persona facts). Final eval score is the GEOMETRIC MEAN of (a, b). The two are jointly required: high creativity + low accuracy = hallucination; low creativity + high accuracy = copy. Differs from prior eval (single-axis BLEU or single-axis fact-check) by JOINT geometric-mean penalising either-axis collapse.
