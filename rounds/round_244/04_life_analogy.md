# R244 — life analogy

## Source domain: intertidal zonation
- Vertical strata of organisms on rocky shores by tolerance to AIR-EXPOSURE: spray zone (lichens) > upper intertidal (periwinkles) > mid intertidal (barnacles) > lower intertidal (mussels) > subtidal (kelp, urchins).
- Each zone has its own ENVIRONMENTAL STRESS profile (desiccation, thermal, wave energy). Species evolve specific tolerance (heat-shock proteins in upper-zone gastropods; air-bubble storage in upper barnacles).
- Critically: species community is a STRATIFIED PROBABILITY DISTRIBUTION over tolerance space; zones are not arbitrary — they emerge from the gradient of environmental stress vs species tolerance.

## LLM analogy candidate
**Stress-stratified LLM layer specialization**: train an LLM with EXPLICIT layer-level NOISE / PERTURBATION gradient — earliest layers are subjected to highest input perturbation (= upper intertidal: alternately dry/wet, high stress), deepest layers see clean signal (= subtidal: stable). Each layer thus specializes for its local stress profile. Predicted effect: early layers become EXPOSURE-TOLERANT (robust to input noise / paraphrase / typo / adversarial perturbation) while deep layers retain CLEAN REASONING. Stress-gradient is enforced by per-layer dropout / noise injection schedule monotonically decreasing with depth. This is intertidal zonation transferred to layer specialization.

## What differs from prior art (claim)
Layer-wise scaling (Crown-Frame-Reverse 2509.06518) and sparsity (2502.14770) modulate CAPACITY per layer. None propose a per-layer NOISE/PERTURBATION gradient monotonically decreasing with depth as a STRESS-stratification training discipline. The intertidal framing (stress-gradient → tolerance-specialization → emergent layer roles) is distinguishing.
