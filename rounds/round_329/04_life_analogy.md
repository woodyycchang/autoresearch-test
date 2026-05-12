# R329 — life analogy

## Source: Archerfish refraction-corrected water jet targeting
- Fish sees prey at apparent (refraction-displaced) angle, but must aim at true angle.
- Builds an internal model of refraction perturbation via motor adaptation over trials.
- Aftereffect when refraction perturbation is removed → shoots in opposite direction. Proof of internal model.
- Learned correction is online and parameter-efficient.

## LLM analogy
**ARCHER-VERIFY**: an evaluation-diagnostic head. During inference, an LLM's output distribution is "distorted" by sampling temperature, constraint-decoding masks, RLHF tax, and grammar-aligned-decoding bias. ARCHER-VERIFY learns an online per-prompt-class refraction-correction lookup (small online-updated table) that produces the EXPECTED un-distorted output distribution given the observed distorted output. Run as a diagnostic against the deployed model to detect systematic mis-targeting (drift from training distribution).

## Differs from prior art (claim)
Grammar-Aligned Decoding (ASAp) corrects per-prompt distortion at decode. Calibration / temperature-scaling adjust global probabilities. RLHF-tax studies measure but don't correct. ARCHER-VERIFY differs: online per-class motor-adaptation-style learned correction USED AS A DIAGNOSTIC (not as inference modification) — flags model drift via aftereffect-like residual signal.
