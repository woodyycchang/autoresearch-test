# Life Analogy — Karen backstrap weaving warp-weft orthogonal binding

The **Karen backstrap loom weaving** (Burma/Thailand):
- Backstrap loom — weaver's body tensions warp threads vertically.
- WARP threads are taut, vertical, established at setup; WEFT threads pass horizontally perpendicular.
- Pattern emerges from warp-weft binding crosses — supplementary weft yarns create complex patterns without disturbing warp.
- Mathematical structure: warp-faced tabby weave with supplementary weft = TWO orthogonal pattern channels.

The mechanism: **two orthogonal pattern channels (warp = base structure, weft = new pattern); new pattern is added in WEFT-direction without disturbing the WARP**.

## Analogical mapping → LLM null-space orthogonal adapter

- Warp threads ↔ pre-trained model weight directions
- Weft threads ↔ new-task adapter update directions
- Warp-weft cross-binding ↔ explicit orthogonality between adapter and pre-trained
- Supplementary weft pattern ↔ new task capability added without disturbing base
- Backstrap tension ↔ pre-training regularization

The mechanism: **KAREN-WEFT-NULL** — a null-space orthogonal adapter design where new-task low-rank update matrix B is constrained to span only the LEFT NULL SPACE of pre-trained weight W's top-K SVD components (warp directions). Additionally, the adapter activation update is constrained to be orthogonal to the activation directions used by warp tasks (warp-tasks reserved on input side, adapter activations on output). The "weft" passes orthogonal to "warp" at BOTH parameter and activation levels. Differs from LoRA-Null (null space of ACTIVATIONS only), Null-LoRA (null space of weight direction only), OPLoRA (one-sided projection), CLoRA (pre-defined subspace) by combining DUAL-LEVEL orthogonality (parameter null-space AND activation orthogonality).

## Note on adjacency

Strong adjacency:
- LoRA-Null 2503.02659 (null space activations)
- Null-LoRA 2512.15233 (null space weights)
- OPLoRA 2510.13003 (orthogonal projection both sides)
- OLieRA 2509.06100 (Lie-group orthogonal continual learning)
- CLoRA 2025 (subspace orthogonal regularization)

Expected FAIL with very strong overlap — null-space LoRA is mature.
