# R279 — life analogy

## Source domain: Trinidadian steel pan note-section tuning
- Single 200L oil drum head (a SHARED steel substrate) is hammered into multiple note sections, each bounded by an engraved groove.
- Each section's pitch is set by section size + curvature + local stiffness; the GROOVE acts as a vibrational boundary, decoupling adjacent sections.
- KEY: the tuner forces the section's first mode (fundamental) AND deliberately tunes higher modes (e.g., octave + perfect fifth) into a HARMONIC SERIES with the fundamental — modes that "naturally" fall elsewhere are HAMMERED into alignment.
- Result: a single drum carries N independent harmonic-locked notes on a SHARED substrate.

## LLM analogy candidate
**Pan-Tuned Concept Heads (PTCH)**: a parameter-efficient mechanism where a SHARED multi-head attention substrate is fine-tuned so that each head's principal singular direction (fundamental) AND its top-K secondary singular directions (overtones) are explicitly hammered into a HARMONIC LOCK with the head's intended concept — overtone vectors are not orthogonal to the fundamental but are CONSTRAINED to be integer-ratio multiples of the fundamental in the embedding space (analogous to harmonic series 1:2:3). Grooves = orthogonal regularizers between heads. The training objective adds a "harmonic alignment loss" that penalizes overtones falling outside the integer-ratio set.

## What differs from prior art (claim)
- Disentangling Multi-task Interference (2503.05320): separates neurons across tasks — analogous to GROOVES but doesn't impose harmonic-series alignment between fundamental and overtones within a head.
- Standard SVD-LoRA: rank-1 + lower-singular-value updates; no harmonic-ratio constraint.
- Mixture-of-Experts: orthogonal expert routing — adjacent but not within-head overtone constraint.
- PTCH's contribution is: enforce that the secondary singular directions of each attention head's update are constrained to a HARMONIC integer-ratio set anchored to the fundamental direction — a music-theoretic constraint that I have not yet seen in transformer-tuning literature.
