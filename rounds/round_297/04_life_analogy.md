# R297 — life analogy

## Source: Octopus 3-layer skin display
- Chromatophore (pigment expansion/contraction) + iridophore (tunable mirror) + leucophore (broadband scatter) — three independently-controlled layers compose arbitrary output color at each "pixel" of skin.
- Each layer adds DIFFERENT optical channel; output = superposition of three.

## LLM analogy
**OCTOPUS-DECODE**: 3-layer compositional decoder where final token logit is the additive combination of three independently-controlled decoder heads:
- Pigment head: per-token logit (standard LM head).
- Iridophore head: tunable confidence-mirror that AMPLIFIES or ATTENUATES specific token logits based on safety/style policy.
- Leucophore head: broadband entropy-scatter that suppresses long-tail spikes.
Final = pigment + iridophore + leucophore added in logit space; each head trainable independently.

## Differs from prior art (claim)
- Zipper (2405.18669): multi-tower decoder for modality fusion.
- Tri-layer contrastive decoding (2510.14304): contrastive (subtract) layers.
- Layer contrastive (2509.25177): layer-comparison for hallucination.
- OCTOPUS-DECODE proposes ADDITIVE superposition of three role-specialized heads in logit space — close to multi-tower but with explicit role-functional separation.
