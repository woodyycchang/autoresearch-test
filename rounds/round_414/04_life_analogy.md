# Life Analogy — Aikido tenkan (redirect attacker's momentum)

**Aikido tenkan**:
- The defender PIVOTS in place at the attack's contact moment.
- Rather than RESIST the attacker's momentum, the defender LEADS it along a CURVED PATH (typically 180° rotation around defender's vertical axis).
- Tenkan REDIRECTS, not blocks; the attacker continues forward but along a controlled curved trajectory.
- Combined with irimi (direct entry), it forms tai-sabaki body-evasion that uses attacker's force as the energy source.

The unique principle: **redirect-not-block by tangent rotation about a fixed pivot** — accept the incoming momentum vector and add a perpendicular rotation that converts linear-attack into a controlled circle. The defender's energy cost is small; the attacker's momentum does the work but in a new direction.

## Analogical mapping → adversarial-input redirection at inference time

- Attacker's incoming punch ↔ adversarial input perturbation δ
- Defender's pivot point ↔ a fixed orthogonal subspace U (defender's "axis")
- Tangent redirection ↔ project δ onto U⊥ then add a rotation that maps δ to a tangent direction in U
- Forward motion controlled ↔ the rotated δ' is harmless and the LLM completes generation

The mechanism: **AIKIDO-REDIRECT adversarial momentum redirection** — at inference time, for each input embedding x_t, compute its DEVIATION δ_t from a calibration manifold M (low-rank PCA reference). Rather than zero out δ_t (block) or accept it (resist), project δ_t onto a fixed orthogonal subspace U⊥M then add a rotation R(90°) about an axis within U⊥M, producing δ_t' = R(δ_t - Proj_M(δ_t)). Add δ_t' back to Proj_M(x_t). The result: adversarial component is rotated 90° into a tangent direction that does not affect the LLM's task-relevant axis. Differs from (a) SmoothLLM (input smoothing not redirection), (b) PGD defense via adversarial training (training-time not inference), (c) JailbreakRadar (detection not redirection), (d) Self-Refine (post-hoc not real-time) by combining (i) DEVIATION from calibration + (ii) ROTATION in U⊥M (not zeroing) + (iii) INFERENCE-TIME redirection.

## Note on adjacency

The reverse-direction form fits. Adjacent: PGD adversarial training (defense via training), SmoothLLM smoothing, FLOAT-GLASS null-space attenuation (this batch — α-attenuates instead of rotates). Distinct: 90° ROTATION (not attenuation, not zeroing) of adversarial component into tangent.
