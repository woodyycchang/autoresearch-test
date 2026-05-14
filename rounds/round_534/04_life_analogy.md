# Life Analogy — Icelandic Glíma Brókartök fixed belt-grip with technique-over-strength honor code

The **Icelandic Glíma** (glíma):
- National sport; Viking-era origin; Jónsbók 1325 documented.
- **Brókartök** trouser-belt-grip: fixed start position; one hand grips opponent's belt, other grips trouser at thigh height; both wrestlers symmetric grip.
- Technique-over-strength: cannot push down with force; opponent must be made to fall via well-implemented trip/throw, falling "gracefully" per honor code.
- Circular foot work; upright stance maintained; throws come from balance disruption not strength contest.

**GLIMA-BROKARTOK-FIXED-GRIP-TECHNIQUE-OVER-STRENGTH-COEVOL**: adversarial-coevolution training with fixed initial-condition grip + technique-only (no force) reward + symmetric attacker-defender grip + circular-footwork search step + graceful-fall outcome reward. (1) **Fixed initial-condition grip G_fix**: every adversarial round starts from a fixed (attacker, defender) shared input-context (analogous to Brókartök grip start); attacker cannot "punch out of context" — must operate within the fixed-grip frame. (2) **Technique-only reward R_technique**: reward shaped to penalize brute-force tokens (e.g., copy-paste reuse, simple length attacks); only rewards balance-disruption-style attacks (semantic shifts that flip alignment via small perturbations). (3) **Symmetric attacker-defender grip A_sym = D_sym**: both attacker and defender start from same model class and parameter budget — no asymmetric "stronger attacker"; reward gradient is over technique quality, not capability. (4) **Circular-footwork search step**: attacker explores adjacent token-space in a circular pattern (rotational adversarial perturbation) rather than gradient-direct climbing. (5) **Graceful-fall outcome reward G_fall**: defender's failure is "graceful" if it falls into a coherent (not garbled) failure mode that still respects honor (no harmful output) — reward shaping favors graceful collapse over chaotic failure. (6) Differs from R419 + R424 + R433 + R437 + R459 + R473 + R484 + R497 + R509 LAAMB-DUAL-CHANNEL-MARABOUT (dual-channel grapple+frappe attack-mode mixing + marabout pre-fight self-warmup adversarial ritual defense + opponent-specific identity conditioning hash checkpoint prep + per-mode weakness signal attacker mode-switching policy, no fixed-grip + no technique-only + no symmetric capability + no circular-footwork + no graceful-fall) and R522 LETHWEI-9-LIMB (9-attack-channel + bareknuckle + headbutt + KO-revive, no fixed-grip + no technique-only) by Brókartök fixed-grip + technique-only reward + symmetric capability + circular-footwork search + graceful-fall outcome reward.

## Adjacency
- JailAgent Constraint Tightening 2604.05549
- Active Attacks Adaptive 2509.21947
- Automatic LLM Red Teaming RL 2508.04451
- Adversarial Preference Learning ACL 2025

Expected FAIL — adversarial co-evolution + red-team RL + constraint-tightening + preference-learning literature covers.
