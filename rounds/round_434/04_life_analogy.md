# Life Analogy — Mosuo zou hun walking marriage

The **Mosuo zou hun** (walking marriage):
- Matrilineal Yunnan/Sichuan culture; ~40K people.
- No-contract / no-obligation visit-relationship between two people from distinct Awo houses.
- Each partner retains primary residence in their matrilineal Awo.
- Multiple parallel walking-marriages permitted; visits are night-only.

**ZOU-HUN-BASIN**: a no-commitment dual-attractor inference scheme where the model maintains TWO baseline persona-attractors (Awo A and Awo B) and switches at runtime by NIGHT-VISIT-style soft cross-attention between them. Neither attractor is "primary" — both remain active and the model's response is a per-query convex combination depending on a small router scalar; no parameters are committed to either attractor permanently. Differs from MoE (commits expert per token) by NO-commitment soft mixing + dual-equal-attractor structure.

## Adjacency
- Attractor-Based Persona Continuity (Medium 2026/03)
- MasRouter Multi-Agent Routing
- vLLM Semantic Router Mixture-of-Models
- TinyTroupe Persona Simulation

Expected FAIL — model-routing + persona-attractor + no-commit soft-routing is well-covered.
