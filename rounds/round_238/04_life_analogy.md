# R238 — life analogy

## Source domain: stained glass leaded panel construction
- Each colored glass piece is bounded by H-channel LEAD CAMES that hold the piece in place and separate it from neighboring pieces. The lead lines provide the visible drawing while structurally locking the assembly.
- A "CARTOON" (full-size design drawn on plaster) is the offline plan: every piece numbered, colored, oriented. The cames pattern is the cartoon's negative — where the lead runs is the drawing.
- Mechanical property: structural integrity depends on the came network forming a closed, fully-bounded mesh. Any unsealed cames gap → glass piece falls out.

## LLM analogy candidate
**Cames-bounded concept compartments in LLM activations**: take the residual stream and OFFLINE partition the dimension axis into N concept-compartments (cames-network) by a learned-orthogonal block-diagonal projection. Each compartment is bounded by a "lead came" — a low-rank projection layer that strictly separates the compartment's signal from its neighbors. Forward pass routes information through the compartments according to a CARTOON (offline-authored routing graph: which compartment activates for which prompt-class). Cross-compartment leakage is monitored by a "soldering loss" that minimises cross-compartment cosine. Properties: (1) interpretability — every neuron is in exactly one compartment with a known concept name; (2) intervention — knock out a compartment without affecting others; (3) audit — flag any cross-compartment leak as a "broken came." Distinguishing from MoE: compartments are over INTERNAL DIMENSIONS not experts; the cartoon is HUMAN-AUTHORED, not learned.

## What differs from prior art (claim)
Concept Layers (2502.13632) provide intervention handles at the conceptual layer level. Mechanistic interpretability literature (2510.02917 ICLR 2026) finds switch-like features but does not BOUND them with explicit cames. Sparse Auto-Encoder feature decomposition gives sparse concepts but does not enforce a closed-came-mesh integrity check. Concept compartments with adversarial soldering loss + human-authored cartoon are distinguishing.
