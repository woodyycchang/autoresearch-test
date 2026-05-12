# R277 — life analogy

## Source domain: Bristlemouth eye-reference photophore counterillumination
- Bristlemouth fish in twilight zone (200-1000m) has ventral photophores.
- A predator looking up sees ANY silhouette against downwelling light.
- The fish's eye-facing photophore is pigmented anteriorly: it lets the eye sense downwelling light AND its own ventral output simultaneously.
- The brain CLOSES THE LOOP: adjusts ventral output until the eye sees both at the same intensity → ventral emission exactly cancels silhouette.
- If cloud passes overhead, ventral output drops in lockstep, maintaining cancellation.

## LLM analogy candidate
**Eye-reference counter-emission detector-feedback decoder (ECED)**: an LLM output module that maintains, at each generation step, a SECOND lightweight detector that observes BOTH the ambient distribution of human-written text (continuously sampled from a small recent web corpus) AND its OWN current output stream. The decoder modulates per-token sampling temperature, top-p, and rare-token-injection probabilities in real time to drive a divergence metric (KL between own running statistics and ambient stats) toward zero — actively dimming or brightening its statistical signature to match the local "downwelling" distribution. The KEY novelty: the closed-loop reference is the SAMPLED AMBIENT DISTRIBUTION, not a pre-trained detector or a fixed reference distribution.

## What differs from prior art (claim)
- Adaptive Text Watermark (2401.13927): watermarks high-entropy tokens; no closed-loop ambient-distribution-matching feedback.
- RLCracker (2509.20924): RL-trained adversarial removal attack on watermark; not a built-in self-cancellation decoder.
- Linguistics-aware watermark (2510.13829): syntactic-predictability watermark; not ambient-distribution match.
- ECED is purely cancellation toward a LIVE-SAMPLED ambient reference (analogous to bristlemouth's eye-facing photophore continuously sampling downwelling light), not a fixed adversarial-pre-train or a static watermark scheme.
