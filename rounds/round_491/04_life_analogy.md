# Life Analogy — Cherokee stomp dance counter-clockwise ring

The **Cherokee stomp dance**:
- Counter-clockwise circle around sacred fire.
- Shell-shaker women (turtle-shell + pebble rattles) carry rhythm.
- Alternating male-female spiral.
- Heart + left-hand toward fire (consistent orientation).
- Cannot start without shakers (rhythm anchor).

**STOMP-RING-NULL-CCW**: counter-clockwise ring-rotation null-space gradient subspace traversal with rhythm-anchored stepping. (1) Maintain K orthogonal gradient subspaces {S_1, S_2, ..., S_K} forming ring (S_K → S_1). (2) Per training step t, project gradient onto S_{t mod K} (counter-clockwise step). (3) Rhythm-anchor: 'shell-shaker' direction e_anchor = canonical alignment direction (fixed reference). (4) Heart-toward-fire: every step preserves cos-similarity(parameter, e_anchor) > τ. (5) Spiral motion: ring radius decreases monotonically (convergence toward fire-center) — annealed subspace radius. (6) Cannot start without shaker: alignment-direction must be defined before training begins.

## Adjacency
- Lotus Adaptive Subspace Switching (closest, 2602.01233)
- SubTrack++ Grassmannian Subspace Tracking (2502.01586)
- ReSpinQuant Subspace Residual Rotation
- TSR Trajectory-Search Rollouts

Expected FAIL — subspace traversal + gradient projection paradigm fully covered.
