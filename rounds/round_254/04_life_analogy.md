# R254 — life analogy

## Source domain: anglerfish-Photobacterium symbiosis
- **Esca** = a fleshy lure on the female anglerfish's "fishing rod"; contains a **photophore** (specialized organ) housing **Photobacterium** symbionts.
- The bacteria GENERATE the light (luciferin + O2 → luciferase chemistry).
- The host does NOT generate light directly; instead, it CONTROLS emission by modulating **oxygen blood-flow** to the esca: more O2 → brighter; restricted O2 → dim/off.
- Bacteria are **acquired from seawater** during development (not vertically inherited); they have a **genome reduced** to dependency-on-host while in the esca.
- **Saturating feedback**: there is a maximum brightness set by the size of the photophore + bacterial density; the host can attenuate but cannot exceed.

## LLM analogy candidate
**Host-gated symbiotic signal-generator module (HGSSGM)**: pair a frozen pretrained host LLM with a SMALL auxiliary "symbiont" module trained externally on a generic signal-generation task (e.g., calibrated-confidence emission, uncertainty token emission, refusal-flag emission). At inference, the host's hidden state passes through a learnable **oxygen gate** = a scalar attenuation σ(h) ∈ [0,1] that modulates the symbiont's emission output before it is added to the host residual. The symbiont was trained on an external corpus and has a **reduced "genome"** = parameter count much smaller than the host's, dependent on the host's hidden state to disambiguate its outputs. The host can ATTENUATE (turn down σ) but cannot EXCEED the symbiont's saturating maximum. Result: the host gains a calibrated emission capability without retraining; the symbiont is generic and acquired from a public model zoo. Distinct from MoE: experts are co-trained; HGSSGM symbiont is externally pretrained, host-attenuated, with explicit saturating cap.

## What differs from prior art (claim)
SignalLLM (2509.17197) is LLM orchestrating external DSP tools, not an internal symbiotic module. SCRAMBLe (2504.04740) generates synthetic preference data. None retrieve a host-frozen + externally-pretrained + host-attenuated emission module with saturating cap (anglerfish-esca-style auxiliary). Auxiliary classifier heads exist but are co-trained; the externally-acquired + attenuation-only-control is the distinguishing piece.
