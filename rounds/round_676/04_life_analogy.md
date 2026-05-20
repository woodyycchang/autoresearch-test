# R676 Life-analogy / motivation

The Lévy α-stable family generalizes the Gaussian (α=2) to fat-tail
distributions where rare extreme events are not exponentially suppressed.
Brownian motion (α=2) has finite second moment; α-stable Lévy motion
(α<2) has infinite variance and exhibits "jump" behavior.

In LLM attention, the standard scaled dot-product implicitly assumes
Gaussian-like attention-score distributions (via softmax of inner
products). But the EMPIRICAL distribution of post-softmax weights at
many layers is heavy-tailed: a few tokens dominate, most are near-zero.

The mechanism transfer: explicitly fit the α-stable α (stability index)
to per-layer attention weights, then renormalize by γ (the α-stable
scale parameter). This decouples "background routing budget" (mass in the
near-zero attention weights) from "needle-routing budget" (mass in the
heavy tail).

Motivation strength: mechanism_transfer (α-stable family is the canonical
heavy-tail mechanism; not metaphor; well-defined renormalization rule).
