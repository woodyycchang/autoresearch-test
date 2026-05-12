# R265 — life analogy

## Source domain: Mevlevi dervish whirling sema
- Semazen rotates on a FIXED PIVOT FOOT (left), driving with the right; the rotation axis through the body is INVARIANT across the entire long ceremony.
- The ceremony is divided into FOUR salams, each with its OWN tempo/musical quality, but the rotation axis remains locked through all four.
- The semazen maintains rotation for ~30-60 minutes despite changes in tempo and inner intent — the geometric invariant (locked axis) carries through the diverse phases.

## LLM analogy candidate
**Axis-locked phase-segmented long-horizon reasoning (ALPSLHR)**: an LLM long-horizon reasoning protocol that maintains a FIXED RESIDUAL-STREAM AXIS (the "axis-of-thought" — a specific projection of the residual stream tied to the problem identity) across the entire reasoning sequence, while allowing tempo/strategy variation across PHASES. Implementation: (1) at the start of reasoning, extract a problem-identity vector v from the question encoding. (2) During each reasoning step, project the residual stream onto v's 1-D axis and enforce that the projection's magnitude does not change sign (axis-lock invariant). (3) The reasoning is divided into PHASES (e.g., understand → plan → execute → verify) each with its own tempo (max thinking tokens, exploration vs verification mode). (4) The axis-lock is verified at phase transitions; if violated, the chain rolls back to the last lock-point. Distinct from CoT: CoT has no axis invariant. Distinct from scratchpad with reflection: scratchpads do not enforce a geometric invariant on the latent state.

## What differs from prior art (claim)
Halo Limited Reasoning Space (2602.19281), ScaleLogic (2605.06638), Model-First Reasoning (2512.14474) cover long-horizon reasoning. None retrieve residual-stream axis-lock invariant + phase-segmented tempo + rollback-on-violation triad.
