# R271 — life analogy

## Source domain: Yagi-Uda antenna
- ONE actively-driven dipole (the "driven element") + multiple PASSIVE parasitic elements (directors in front, reflector behind).
- The parasitic elements are NOT electrically connected to the transmitter — they receive radiation from the driven element and re-radiate it.
- Each parasitic's LENGTH is tuned: directors slightly shorter (capacitive), reflector slightly longer (inductive). This creates phase shifts that combine constructively forward and destructively backward.
- Result: a directional radiation pattern with high forward gain from a single active source.

## LLM analogy candidate
**Yagi-style passive phase-coupled steering (YPPS)**: a frozen base LLM has ONE actively-trained "driven" output head. Add multiple PASSIVE FROZEN parasitic heads (similar architecture, NO gradient flow) tuned to specific behavior axes (refusal-direction, formality, length-bias). The parasitics RE-EMIT modulated logits at their own phase offsets (each tuned via its frozen length/phase parameter). The final output = driven head + sum-of-parasitic re-emissions, weighted by inter-head phase coupling. Directors add forward gain to desired behavior; reflectors cancel reverse / unwanted behavior. Distinct from activation-steering (additive vectors): YPPS arrays MULTIPLE passive heads with PHASE relationships, not single steering vectors.

## What differs from prior art (claim)
EasySteer (2509.25175), Activation Steering (2604.08169), KV Cache Steering (2507.08799) cover single-vector/single-direction steering. YPPS uses ARRAYED passive heads with phase-coupled directional summation — equivalent to multi-element antenna array vs single dipole.
