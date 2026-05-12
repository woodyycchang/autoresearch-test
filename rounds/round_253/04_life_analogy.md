# R253 — life analogy

## Source domain: origami Miura-ori
- A flat sheet tessellated with degree-4 vertices (each vertex sees 4 creases) using alternating mountain/valley folds; pattern satisfies Maekawa's theorem (|M − V| = 2) and Kawasaki's theorem (alternate angles sum to π).
- Properties:
  - **Single degree of freedom**: the whole sheet deploys/contracts via ONE parameter — no internal locking.
  - **Rigid panels**: faces between creases never bend.
  - **Flat-foldable**: can be compressed to a flat stack.
  - **Negative in-plane Poisson's ratio**: stretching in one direction stretches the perpendicular direction too.
  - **Scale-independent**: kinematics depend on geometry, not on material.

## LLM analogy candidate
**Miura-tessellated parameter manifold (MTPM)**: organize a model's parameter matrices into a discrete tessellation where each "panel" is a small rigid block (a low-rank subspace of fixed structure), and the inter-panel "creases" are learnable rotation-style mixing operators that satisfy a **Maekawa-equivalent constraint** (signed-mixing balance) and a **Kawasaki-equivalent constraint** (alternate-sum-to-π subspace alignment). Result: the entire parameter manifold collapses/expands along a **single scalar deployment parameter** θ that smoothly slides between a fully-expanded (training-mode) tensor and a fully-collapsed (deployment-mode) compressed tensor, with NO additional degrees of freedom. This gives lossless deploy-time compression by construction (rather than by reconstruction error). Distinct from PCA-truncation: PCA discards components; Miura folding preserves all panels by physically folding them. Distinct from LoRA: LoRA adds a low-rank delta; Miura-folding REORGANIZES the dense tensor onto a single-DOF manifold.

## What differs from prior art (claim)
FLAT-LLM (2505.23966) uses PCA truncation per head + greedy redistribution — discards components, not folds. DFloat11 (2504.11651) is dynamic-length float compression at byte level. ZipServ (2603.17435) is hardware-aware lossless byte compression. None impose a Maekawa+Kawasaki single-DOF kinematic constraint on the parameter manifold. The single-scalar-θ deployment of an entire tensor via tessellated rigid panels is not retrieved.
