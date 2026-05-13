# Life Analogy — Indonesian batik (wax-resist selective dyeing)

**Batik** is wax-resist dyeing:
- Hot beeswax applied to fabric via **canting** (pen) or **tjap** (stamp) — areas to PROTECT from dye.
- Fabric soaked in dye; waxed areas resist dye absorption.
- After dye sets, BOILED to remove wax; unwaxed areas now colored.
- Multi-color via SEQUENTIAL wax+dye cycles (apply more wax to protect dyed areas, dye next color, repeat).
- The wax is a SELECTIVE NEGATIVE MASK — it does not add new information; it PREVENTS dye from reaching protected pixels.

The unique principle: **negative-mask selective protection via removable physical layer** — instead of dyeing the part you want a color, you PROTECT the parts you DON'T want this color and dye the rest. The mask is removable, so it can be reapplied in subsequent rounds for multi-color output. The information lives in WHAT IS PROTECTED, not in what is applied.

## Analogical mapping → null-space fine-tuning via negative-mask protection

- Fabric ↔ pretrained LLM weights
- Wax-protected areas ↔ "frozen subspace" of weights protected from fine-tune update
- Dye ↔ fine-tune update Δθ
- Multi-color rounds ↔ sequential fine-tunes on different tasks with different wax masks
- Wax pattern designer (canting/tjap) ↔ a small learnable masking subnetwork that decides which weight directions are protected

The mechanism: **BATIK-WAX-RESIST null-space negative-mask fine-tune** — for each fine-tune task T, train a small MASKING SUBNETWORK m_T(W) that produces a per-weight 0/1 protection mask. Update only UNPROTECTED weights: W_T = W + m_T(W) ⊙ 0 + (1 - m_T(W)) ⊙ Δθ_T. For multi-task fine-tune, sequentially apply tasks T1, T2, ... each with its own learned mask; tasks with overlapping mask regions never interfere because the protected region of T1 is preserved during T2's update if m_T2 also marks it as protected. The mask is OUTPUT of a learnable function — not a fixed rule. Differs from (a) standard LoRA (low-rank not mask-based selection), (b) Sparse fine-tuning (selects parameters, no learnable mask network), (c) PESO subspace (subspace not mask), (d) DoRA (direction-rank not mask), (e) LIFT (Principal Weights selection, not learnable subnetwork mask) by combining (i) LEARNABLE per-weight mask network + (ii) NEGATIVE-protect interpretation + (iii) SEQUENTIAL multi-task layering.

## Note on adjacency

The null-space-traversal form fits. Adjacent: sparse fine-tuning, LIFT, LoRA-mask, AlphaSteer null-space (this batch R408 R414). Distinct: LEARNABLE MASK NETWORK per task + sequential layering as primary mechanism.
