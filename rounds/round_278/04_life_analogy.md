# R278 — life analogy

## Source domain: Nepenthes pitcher plant peristome aquaplaning
- Insect lands on dry peristome: textured, walkable, no capture risk.
- Wet conditions (rain, condensation, hygroscopic nectar absorbs humidity) cause a thin water film to coat the radial ridges.
- The wet film + anisotropic radial ridges + smooth overlapping epidermal steps → friction collapses ONE WAY (toward pitcher interior); insect aquaplanes into the pitcher.
- Two-mechanism trap: water film disables soft-pad insects; ridges disable claw-grip insects.
- Mechanism is STATE-CONDITIONED: dry = safe walking surface; wet = irreversible trap. The trap is INVISIBLE when dry; cost to plant is only the nectar.

## LLM analogy candidate
**PCAP (Peristome Conditional Aquaplaning Gate)**: a state-conditioned input-filter for LLM agents. When the input context is "dry" (within normal usage distribution, no adversarial signals) the filter is INERT — passthrough, no latency, no overhead. When the input passes a "wetness predicate" (composed of multiple soft adversarial-indicator features above a calibrated threshold) the filter activates a one-way trap: it CHANNELS the request into a sandboxed sub-prompt that is anisotropic (the LLM can read but cannot influence its meta-state), and the request is processed inside a quarantine where any harmful completion is absorbed silently. The trap is LATENT under benign inputs.

## What differs from prior art (claim)
- HSF (2409.03788): single-stage hidden-state classifier; not conditionally activated, not anisotropic, not state-conditioned.
- Alert (2601.03600), Trace (2602.11495): detection without conditional-trap directional asymmetry.
- Standard input filters reject inputs; PCAP routes them into a quarantine where the LLM still answers but inside an anisotropic sandbox (the answer cannot influence the parent agent state).
- No prior work combines conditional-activation + anisotropic-direction + silent-absorption like aquaplaning peristome.
