# Life Analogy — Maori nguru nose-flute dual-mode (nose / mouth) breath direction + sacred-breath protocol

The **Maori nguru** (Taonga Pūoro):
- Small vessel-flute (Helmholtz oscillator class); carved from wood/gourd/whale-tooth.
- Dual playing mode: (a) **nose-mode** through upturned spout — sobbing soft tone (sacred); (b) **mouth-mode** through larger end at angle — louder.
- Breath direction = mode switch; same instrument, two acoustic regimes.
- Sacred nasal breath connects to spirit voices (Hineraukatauri goddess); played at tangihanga (funerals).

**NGURU-DUAL-MODE-NOSE-MOUTH-SACRED-BREATH-NULL-PROJECTION**: dual-input-mode null-space projection with nose-mode soft + mouth-mode normal + breath-direction mode-switch gate + sacred-breath reflexive identity. (1) **Dual-mode null-space projection**: per task gradient ∇ projected onto one of 2 null-space modes — N_nose (low-amplitude/quiet update) for sensitive/identity-preserving tasks; N_mouth (normal-amplitude update) for general tasks. (2) **Breath-direction mode-switch gate G_breath**: task-type classifier determines mode for current gradient step (sensitive → nose, general → mouth). (3) **Sacred-breath reflexive identity preservation**: nose-mode incorporates additional reflexive constraint requiring the model's identity-vector e_id to remain unchanged (||e_id^new - e_id^old|| < τ_id). (4) **Same-instrument shared parameter pool**: both modes update the same parameters but through different projection operators — analogous to single nguru played 2 ways. (5) **Helmholtz-oscillator-style mode-coupling**: cross-mode regularizer encourages consistent overall behavior between nose-mode and mouth-mode outputs. (6) Differs from R414 + R427 + R441 + R453 + R469 + R478 + R491 + R503 DOINA-NULL-SPACE-LORA-MELISMA-RUBATO (continuous-time melisma + breath-budget + descending-tonic basin + parlando rubato) and R528 NEY-4-REGISTER-NULL-GATE-OVERBLOW (4-register hierarchical + null-gate + breath-velocity + partial-hole + interdental) by dual-mode (nose/mouth) + breath-direction mode-switch + sacred-breath reflexive identity preservation + same-instrument parameter pool + Helmholtz mode-coupling.

## Adjacency
- Lotus Randomized Low-Rank 2602.01233
- Continual Gradient ACL 2025
- SubTrack-Grad Subspace Tracking
- BSZO Bayesian Zeroth-Order 2601.01452

Expected FAIL — gradient null-space + adaptive subspace + per-task projection literature covers.
