# R344 — life analogy

## Source: Saguaro accordion-pleated rib expansion
- Vertical pleats on trunk: 20-25% volume swell on water uptake.
- Pleats expand without stretching skin → no structural failure.
- Contract on water depletion → same geometry, smaller volume.
- Mechanism: pre-folded reserve geometry; binary swell-contract cycle.

## LLM analogy
**ACCORDION-PARAM**: pretraining method using pre-folded reserve parameter capacity that EXPANDS to accommodate new training data without requiring new architecture. Model has K "pleat" parameter groups that are zero-initialized and folded into the base model. As new training data arrives, pleats unfold (gradient updates apply to them); on data plateau, pleats contract (parameters shrink back to near-zero via L1 prune). Binary expand-contract data-driven capacity adjustment.

## Differs from prior art (claim)
Weight factorization + gradient compression (2505.22922) reduce static capacity. Model growth / progressive layer addition expands architecture. ACCORDION-PARAM differs by HAVING pre-folded zero-init reserve capacity that data-driven expand-contract — binary swell-contract rather than monotonic growth.
