# R306 — life analogy

## Source: Australian bushfire backburning + hazard reduction
- Hazard reduction = controlled burns during low-risk conditions to deplete bushfire fuel before wildfire season.
- Backburning = lighting an independent fire AHEAD of an approaching wildfire to consume fuel before the wildfire front arrives, creating a firebreak.
- Both depend on deliberately consuming "fuel" (combustible biomass) in advance, in a controlled direction.

## LLM analogy
**ASH-LINE**: when a jailbreak classifier detects an approaching attack signature, the model is forced to emit a controlled "burn" — a short burst of high-entropy refusal-loaded tokens that DEPLETE the attention budget at the next k layers. By the time the jailbreak signal arrives, the attention "fuel" (downstream KV slots, value-space concentration) at the relevant heads has already been consumed, leaving no room for the jailbreak to propagate.

## Differs from prior art (claim)
SafeProbing (2601.10543) probes latent safety during decoding and bypasses high-susceptibility layers; ProAct (R298) triggers bundled defense; logit-based steering shifts logits. None deliberately PRE-CONSUME attention budget downstream to create a firebreak.
