# R322 — life analogy

## Source: Bird cryptochrome magnetoreception
- Blue light excites FAD in Cry4a → forms radical pair with tryptophan electron.
- Pair oscillates between singlet/triplet spin states.
- External magnetic field biases oscillation rates; downstream chemistry yields direction signal.
- Evolved as a SENSITIVE probe rather than an active mechanism.

## LLM analogy
**CRYPTO-PROBE**: paired-prompt orientation diagnostic. For each model checkpoint, run two related prompts (P, P+δ) where δ is a small directional perturbation. Measure angular drift in feature space between output activations for P and P+δ; the drift vector reveals model's "magnetic compass orientation" in semantic space — used to detect drift, alignment shifts, distribution shifts.

## Differs from prior art (claim)
Paired prompting + contrastive probing are mainstream evaluation methods. Activation steering uses similar paired-prompt design. CRYPTO-PROBE adds magnetoreception framing but mechanism is paired-prompt drift measurement.
