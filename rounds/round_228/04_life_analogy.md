# R228 — life analogy

## Source domain: bell-founding tuning
- A church bell has FIVE significant partials (hum, prime, tierce, quint, nominal). Cast bell is off-pitch; tuning is done by REMOVING small amounts of bronze from specific INSIDE heights (the bell wall thickness at axial position h controls a specific partial).
- The strickle-board profile is the bell's shape; harmonic tuning is performed by precision lathe-shaving at axial positions corresponding to nodal/antinodal heights of each partial.
- Bronze removal is MONOTONIC and IRREVERSIBLE; precise small cuts → harmonic alignment.

## LLM analogy candidate
**Harmonic-partial-targeted post-training pruning**: rather than pruning by global magnitude or per-layer importance, identify the LLM's "partial frequencies" as low-rank spectral modes of attention/feed-forward activations and prune ONLY the parameters whose effective contribution lies in OFF-TARGET partials. Specifically: compute per-layer activation Fourier-or-spectral decomposition; estimate per-partial gain; for each partial, identify the axial / depth / coordinate "shave point" where removal disproportionately suppresses that partial without affecting others; trim there. The bell-style discipline is that each shave is targeted at a specific partial, not at minimising aggregate norm.

## What differs from prior art (claim)
Recent statistical post-training pruning (2602.07375, 2503.09657) use magnitude / variance / per-layer importance. Spectral diagnostics (2605.05683) measure spectra but treat them as diagnostic only, not as the pruning target. None ties pruning policy to specific harmonic partials of the model with the bell-tuning discipline of "shave at axial position h to suppress partial p without disturbing partials q ≠ p."
