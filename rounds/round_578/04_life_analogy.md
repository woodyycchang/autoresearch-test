# Life Analogy — Bulgarian Gadulka 11-string Bourdon-Sympathetic (Balkan, 19th c.+): 3 melody-strings + 8 sympathetic-strings + drone bourdon-anchor + arch-bow continuous trajectory + scordatura initial-tuning

The **Bulgarian gadulka**: pear-shaped bowed string instrument; 3 main melody-strings + 8 sympathetic resonance-strings underneath; sympathetic strings are NEVER bowed — they vibrate passively through resonance with the melody strings. Bourdon (drone) tuning on lowest melody-string. Arch-bow continuous trajectory (no plucking). Scordatura (variable tuning) for different folk traditions.

**GADULKA-3-MELODY-8-SYMPATHETIC-NULL-SPACE-BOURDON-ARCH-BOW-CONTINUOUS-SCORDATURA-RESET**: An LLM null-space-traversal mechanism with (1) **3-melody-rank subspace split with 8-null-space-resonance dimensions** R_split: 3-dim active-rank subspace for task-specific learning + 8-dim null-space passive subspace for shared-knowledge resonance; (2) **Bourdon-anchored common-mode base B_drone**: lowest-rank component shared across all updates, frozen anchor; (3) **Sympathetic-resonance passive learning S_res**: 8-dim sympathetic dims never directly updated by gradient, only updated through induced resonance from 3-melody dims; (4) **Arch-bow continuous trajectory G_continuous**: bow-pressure gradient as continuous-time curve (no discrete plucking) — smooth weight update with bow-pressure schedule; (5) **Scordatura initial-tuning orthogonality reset I_orth**: per-domain re-tuning of the 11 strings' alignment vectors at start of new task domain.

## Adjacency
- LoRA low-rank adaptation
- LoRA-Null null-space LoRA
- Continual Gradient Low-Rank Projection (CLoRA)
- Spectral Sphere Optimizer

Expected FAIL v5 / PASS v6 (no single paper covers 3-melody × 8-sympathetic × bourdon × arch-bow × scordatura composite).
