# Life Analogy — Pit viper infrared loreal organ (differential heat sensor)

The **pit viper loreal organ** is an infrared sensor between eye and nostril:
- A thin **membrane** suspended in a hollow chamber with **air on both sides**.
- The membrane is heated by incoming IR; nerve fibers fire at a **baseline rate** corresponding to LOCAL THERMAL RADIATION AVERAGE.
- A warm-object signal is detected as a **DEVIATION** from this local baseline, not as an absolute reading.
- The dual-air-contact provides a **cool-side reference** so the differential = (signal - ambient) is computed at the membrane level itself.

The unique principle: **physically dual-pathway baseline subtraction** — the sensor's geometry encodes baseline-subtraction (warm membrane vs cool-side ambient) so that the signal it reports is the DIFFERENCE between the IR target and the local thermal background. The baseline is not a stored expectation; it is a continuously updated PHYSICAL reference.

## Analogical mapping → LLM evaluation differential signal

- IR target ↔ a candidate model's score on a benchmark
- Ambient thermal background ↔ a "trivial baseline" model's score on the SAME benchmark (e.g., constant majority-class, random retrieval, or LLM-fixed-prompt-output)
- Air-bath dual contact ↔ paired evaluation on the same query: candidate AND baseline both judged
- Continuously updated baseline ↔ benchmark-level recalibrated trivial baseline per task

The mechanism: **PIT-VIPER differential signal evaluation diagnostic** — for any benchmark B, evaluate the candidate LLM L_c AND a fixed "thermal baseline" model L_b (e.g., constant-output / random-guess / fixed-prompt-fragment) on the SAME queries. Report ONLY the DIFFERENCE D = score(L_c, q) - score(L_b, q) per query, then average over benchmark. The diagnostic signal is the differential — a candidate that scores high but only marginally above the trivial baseline (small D) is flagged as "not genuinely informative on this benchmark." Differs from (a) baseline-relative accuracy (compares to GLOBAL average not per-query), (b) Brier score (probabilistic decomposition not paired-trivial subtraction), (c) elo rating (head-to-head model competition not against trivial baseline) by computing PER-QUERY paired differential against a FIXED-TRIVIAL baseline model.

## Note on adjacency

The evaluation-diagnostic form fits. Adjacent: Item Response Theory (IRT) for benchmarks; calibration error; trivial-baseline ablation. Distinct: paired-trivial PER-QUERY subtraction inside a benchmark — most baselines are reported as a separate dataset-level number, not as a per-query subtraction signal.
