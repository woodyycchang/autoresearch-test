# Life Analogy — Igbo Uli body painting ephemeral by design

The **Igbo Uli** body-design tradition:
- Liquid juice from Uli pods drawn freehand on body/skin/walls.
- Patterns appear green initially; turn black via body-heat reaction; fade after ~1 week.
- Wall paint washes off in rainy season. Ephemeral nature is the defining feature.
- Women practitioners central to design knowledge transmission.

**ULI-EPHEMERAL**: time-decaying LoRA adapter with explicit half-life decay. Each adapter is given a decay constant τ (half-life). At training, the adapter weights ΔW are projected into the null space of base weights (orthogonality preserved); at inference, ΔW(t) = ΔW(0) · 2^{-t/τ}, where t is wall-clock or query-count since adapter creation. As t → 3τ, the adapter's effect has decayed to ~12% — gracefully "washed off." Combines null-space orthogonality (like Null-LoRA / OPLoRA / CLoRA) with time-decay scheduling specific to ephemeral knowledge.

## Adjacency
- Null-LoRA 2512.15233 (null-space init, no time decay)
- OPLoRA 2510.13003 (orthogonal projection, no time decay)
- LUNE 2512.07375 (unlearning via LoRA, but discrete erase not graceful decay)
- CLoRA ACL 2025 (subspace orthogonality regularization)

Expected FAIL — null-space LoRA + adapter-decay schedules are saturated 2025-2026 design region.
