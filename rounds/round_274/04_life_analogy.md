# R274 — life analogy

## Source domain: Amami pufferfish sand circle
- A 10 cm male pufferfish builds a ~2 m diameter geometric radial-maze sand structure over 7-9 days.
- The construction uses ONLY local fin-flapping actions; no global blueprint.
- Local rules: stir sand into radial ridges + decorate with shells/coral + maze inner region.
- The artifact is ONE-TIME-USE; abandoned after mating.
- Key principle: SIMPLE LOCAL RULES + LONG ITERATION produce LARGE-SCALE GEOMETRIC EMERGENT structure WITHOUT a centralized plan.

## LLM analogy candidate
**Pufferfish-style emergent local-rule large-artifact (PELRLA)**: a generation paradigm in which a small LLM (10-20× smaller than baseline) executes ONLY local-window rules (each token sees only ±k recent tokens) iteratively for many passes over an artifact buffer. The buffer grows into a large structured output without any global plan, because the local-rule set is calibrated so that emergent structure forms at the macroscale. The local-rule set includes: (a) symmetry-preservation (current token preserves a measured invariant from the window), (b) ridge-decoration (occasional inject of strong markers), (c) maze-perturbation (inject controlled chaos when entropy too low). After ~7-9 generation epochs, the artifact converges to a structured form. Distinct from autoregressive generation: PELRLA is multi-pass and local-rule only, no future-conditioning. Distinct from diffusion: PELRLA uses local-rule iteration not noise-removal.

## What differs from prior art (claim)
Survey LLMs Evolutionary Optimization (2509.08269), Emergent Abilities Survey (2503.05788), LLM Serving Math Optimization (2605.01280) cover related topics. None retrieve a multi-pass local-rule-only small-LLM emergent-structure generation framework.
