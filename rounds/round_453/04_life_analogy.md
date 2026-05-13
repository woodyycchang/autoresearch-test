# Life Analogy — Bedouin bayt al-sha'r goat-hair tent slack/tension adaptive permeability

The **Bedouin black tent** (bayt al-sha'r):
- Woven from goat hair (sometimes camel hair + sheep wool).
- Coarse weave LOOSE in dry desert heat → tiny pores open → convection cooling.
- Fibers SWELL on rain → pores close → watertight.
- Pole-rope-canvas tension calibrated per pitch; side curtains raised/lowered as needed.
- Adaptive permeability via material self-adjustment + active rigging.

**SLACK-TENSION-NULL**: an orthogonal-null-space adapter with adaptive slack regularization. (1) LoRA-style low-rank update constrained to the null-space of pretrained weights (preserve prior knowledge). (2) Slack parameter σ controls the *width* of the null-space tube: σ=0 strict orthogonality (closed pores), σ>0 allows controlled drift through small subspace overlap (open pores). (3) σ is learned per-layer or scheduled to match data distribution drift — high σ for in-distribution data (cooling), low σ for out-of-distribution / adversarial (watertight). (4) Tension-rope analog: per-direction Riemannian Stiefel projector restores null-space membership after each step.

## Adjacency
- LoRA-Null 2503.02659
- NULL-LORA 2512.15233
- CLoRA ACL 2025
- LoRA-Subtraction Drift-Resistant 2503.18985

Expected FAIL — null-space LoRA + adaptive regularization heavily covered.
