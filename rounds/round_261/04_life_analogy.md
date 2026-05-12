# R261 — life analogy

## Source domain: Greek entasis
- Doric columns are NOT straight cylinders; they are deliberately CONVEX (bulging slightly outward in the middle) — the "entasis."
- The stylobate (base platform) is NOT flat; it arches up ~2.6 inches at center over a 70-foot run.
- Purpose (traditional view, Hero of Alexandria): correct an APPARENT concavity / sag that the human eye would perceive in a perfectly straight column / flat platform.
- Mechanism: deliberate **pre-applied counter-distortion** in the artifact that compensates for the evaluator's perceptual systematic bias, producing the appearance of straightness.

## LLM analogy candidate
**Pre-applied counter-illusion calibration of LLM output (PACIO)**: model the evaluator's known systematic perceptual biases (positional bias, agreeableness bias, length bias, formatting bias) as a forward distortion D(output). At generation time, the LLM applies an INVERSE counter-distortion D^{-1}(intended_output) BEFORE emission, so that after the evaluator's natural distortion the perceived output equals the intended output. Implementation: a small calibration head trained on (intended_meaning, evaluator-judged-distortion) pairs, producing a pre-emission transformation (e.g., reordering, length adjustment, formatting tweaks) calibrated to specifically each evaluator profile. Distinct from RLHF: RLHF aligns the generator's preferences, not evaluator-specific perceptual distortions; PACIO is per-evaluator counter-distortion. Distinct from prompt engineering: PACIO is automated and profile-conditional.

## What differs from prior art (claim)
Judging the Judges (2604.23178), RBD (2505.17100), PRECISE (2601.18777) work on JUDGE-SIDE bias detection and correction. PACIO is **generator-side pre-applied counter-distortion** — calibration applied to outputs BEFORE evaluator inspects them, not to the evaluator. The generator-side counter-distortion against a fixed evaluator-profile is not retrieved in surveyed prior art.
