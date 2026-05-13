# Life Analogy — Brazilian capoeira ginga rocking baseline

The **ginga** of capoeira:
- Continuous side-to-side rocking footwork — perpetual baseline.
- Capoeirista always returns to ginga between every attack, dodge, feint.
- Bantu/Kongo origin "to sway/dance/play" — *active* neutral state.
- Function: confuse opponent + always ready to attack/dodge in any direction.

**GINGA-BASELINE**: an active-neutral baseline-rocking safety alignment scheme. (1) Define neutral baseline policy π_0 — explicit "active neutral" distribution (refusal + clarification + tone-neutral acknowledgment). (2) Between every substantive response token, model is constrained to return to ginga proximity (small KL-divergence to π_0 at periodic checkpoints every K tokens). (3) Active-baseline: ginga is not a fixed point but a *rocking* distribution — slight oscillation between alternative neutral responses prevents over-determinism. (4) Attack response: when generating substantive content, model can excurse from ginga but must return within bounded τ tokens. (5) Multi-directional readiness: ginga maintains low KL distance to multiple potential safety attractors simultaneously.

## Adjacency
- NSPO Null-Space Constrained 2512.11391
- Safety Alignment More Than Few Tokens OpenReview
- Adaptive Safe Context Learning 2602.13562
- Cognitive Computation 2026 Human Agency

Expected FAIL — safety baseline + KL-constrained alignment is mainstream.
