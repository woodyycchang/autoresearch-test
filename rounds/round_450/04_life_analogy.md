# Life Analogy — Boer voortrekker laager defensive wagon-circle

The **Boer laager** (Great Trek 1835-1846):
- Closed-circle wagon formation lashed together for defense in unknown interior.
- Withstood massive numerical disadvantage at Vegkop (40 vs Ndebele) and Blood River (500 vs 15000 Zulu).
- Closed ring + interior assets (cattle, families) + perimeter defenders.
- KEY PROPERTY: ring stays closed under high adversarial pressure — robust basin.

**LAAGER-BASIN**: a robust-basin training objective that explicitly maximizes the radius of attraction of a designated safety-attractor under adversarial perturbation. Loss = standard safety loss + λ·penalty on the gradient of safety output w.r.t. perturbation direction (penalty pushes loss surface to be FLAT around safety-attractor → wider basin). Differs from generic adversarial training by EXPLICIT BASIN-RADIUS OPTIMIZATION via gradient-flatness regularizer.

## Adjacency
- Agentic Loops Geometric Dynamics 2512.10350
- DEQ Adversarial Robustness Tsinghua
- ANTIBODY Flat-Loss Robust Alignment ICLR 2026
- Latent Adversarial States Probing 2503.09066

Expected FAIL — flat-basin robust-alignment optimization is well-covered.
