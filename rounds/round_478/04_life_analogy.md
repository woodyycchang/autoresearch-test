# Life Analogy — Lithuanian sutartinės secondal-dissonance polyphony

The **sutartinės** (Lithuania, UNESCO 2010):
- Multi-part vocal/instrumental polyphony with intentional secondal dissonances (~1.7 semitones).
- Voices' independence is preserved horizontally rather than harmonized vertically.
- "Schwebungs-Diaphonie" — beat-diaphony — voices in tight dissonant intervals beat against each other.
- Each voice traces an orthogonal trajectory in pitch space; cohesion via interlocking rhythm not chord-stacking.

**SUTARTINES-DIAPHONY-NULL**: orthogonal voice-channel null-space adapter routing for LoRA. (1) Decompose LoRA update ΔW into K voice-channels {V₁, ..., V_K}. (2) Each voice-channel V_i lives in its own subspace S_i with orthonormality constraint <V_i, V_j> = 0 for i≠j. (3) Per-voice dissonance preservation: deliberately maintain interval (subspace-distance) > τ_dissonance between adjacent voices (no collapse into single chord-space). (4) Rhythmic interlock: cross-voice beat-pattern coordination via shared rhythmic mask M_rhythm but pitch-independent activations. (5) Voices traverse orthogonal null-space directions; no vertical harmonization (rank reduction).

## Adjacency
- CLoRA Null-Space Direction Constraint (ACL 2025 — closest)
- O-LoRA Orthogonal Subspace Learning (EMNLP 2023)
- StelLA Stiefel Manifold (NeurIPS 2025)
- Continual Gradient Low-Rank Projection (ACL 2025)

Expected FAIL — orthogonal-subspace LoRA paradigm heavily covered.
