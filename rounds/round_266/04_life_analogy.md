# R266 — life analogy

## Source domain: Etruscan buon-fresco
- Lime plaster (Ca(OH)2) freshly applied to a wall is WET and PLIABLE; pigment particles applied during this window are absorbed.
- Over hours-to-days, CO2 from the air reacts with Ca(OH)2 to form CaCO3 (crystalline calcium carbonate), trapping pigment in the matrix.
- After carbonation, the matrix is IMMUTABLE; further pigment cannot be absorbed (it sits on the surface and flakes off).
- The fresco has a HARD COMMIT WINDOW: write while wet; after carbonation, the structure is permanent.

## LLM analogy candidate
**Time-gated carbonation continual-learning commit window (TGCCLCW)**: a continual-learning protocol where new knowledge is written to a "wet" trainable buffer (a small set of mutable adapter parameters initialized at the start of each session). The buffer remains writable only for a fixed COMMIT WINDOW (e.g., 1000 training steps or until a triggered freezing event). At the end of the window, a CARBONATION pass crystallizes the buffer into immutable form: (a) any adapter parameters with high gradient consistency over the window are absorbed into the base model via a low-rank update (the CaCO3 crystallization); (b) any parameters with inconsistent gradients are rejected. After carbonation, the buffer resets to fresh and the cycle repeats. Distinct from continual fine-tuning: TGCCLCW has hard write-window boundaries and explicit absorption-or-reject. Distinct from MoE-CL: not task-routed; time-bounded chemical-style commit.

## What differs from prior art (claim)
MemoryBench (2510.17281), CL Generative AI Survey (2506.13045), MoE-CL (2509.18133) cover continual learning paradigms. None retrieve a hard time-gated commit window + gradient-consistency-based absorption-or-reject crystallization pass.
