# R282 — life analogy

## Source domain: Coral GFP-like fluorescent protein photoprotection
- Symbiotic zooxanthellae inside coral tissue do photosynthesis but are vulnerable to harmful blue/UV light.
- Coral synthesizes GFP-like proteins that ABSORB the harmful short wavelength AND RE-EMIT it as longer, photosynthesis-friendly wavelengths (or dissipate as heat for the non-fluorescent chromoproteins).
- Net effect: spectral SHIFT from a damaging band into a safe band, with energy partially conserved (re-used for photosynthesis) and partially dissipated as heat.
- Mechanism is OPTICAL: no recognition, just photon-physics frequency conversion.

## LLM analogy candidate
**FRECONV (Frequency Re-conversion Spectral Adapter)**: a fixed pre-attention layer that performs eigenspace projection on the input activation, IDENTIFIES the harmful-frequency components (those that historically correlate with adversarial inputs / jailbreak signatures) via a learned frequency-band classifier, and RE-EMITS the energy into a calibrated SAFE eigenspace band (the projection onto a known-safe direction of the attention input subspace). Architecture: input activation → spectral decomposition → frequency-classified routing (harmful → safe; benign → passthrough) → reconstruct. Loss objective: minimize total energy loss (preserve information) while maximizing safety-distribution rebalancing.

## What differs from prior art (claim)
- Hallucination Detection via Spectral Attention (2502.17598): uses spectral features to DETECT hallucination — no re-emission/spectral shift.
- Spectral Filters / Dark Signals (2402.09221): partitions singular vectors into bands for filtering — adjacent but filters DISCARD rather than re-emit at a safer band.
- Spectral Sphere Optimizer (2601.08393): training-time spectral constraint, not inference-time frequency shifting.
- FRECONV is distinguished by: spectral shift (not filter/drop) at inference time as a photoprotection mechanism, with energy partly conserved into a known-safe eigenband.
