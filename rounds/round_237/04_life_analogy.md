# R237 — life analogy

## Source domain: espalier fruit tree training
- A young apple/pear tree is COMMITTED to a planar 2D geometry by training along horizontal cordons (a wire-and-post trellis). Every year, all out-of-plane shoots are pruned to maintain the flat form. The investment compounds: after 5-10 years the tree's BRANCH SCHEMA is locked into the 2D form even with reduced maintenance.
- Benefits: maximum sun exposure per unit ground, all fruit at arm height, predictable canopy density. The form is GROWN, not built — each year's growth is pruned to fit the target geometry.
- Critical: the trellis is the PRIOR; the tree's growth obeys phototropic + gravitropic biology AND the imposed prior simultaneously.

## LLM analogy candidate
**Espalier-trained adapter geometry**: instead of training an LLM adapter as an unconstrained-rank LoRA, define a TRELLIS — a fixed sparse pattern S over a high-dim parameter coordinate set (specific layer × specific head-subspace × specific channel-set bands), authored offline. The adapter is gradient-trained ONLY in coordinates inside S; out-of-trellis gradients are zeroed (espalier pruning). Repeated fine-tunes accumulate adapter capacity ONLY along S; after K cumulative fine-tunes, the adapter's USEFUL CAPACITY is locked into the trellis geometry. Benefits: (1) interpretability — every adapter coordinate is at a known location; (2) compose adapters by orthogonal-trellis selection; (3) catastrophic-forgetting suppressed since out-of-trellis weights cannot drift; (4) predictable parameter budget. The trellis is the PRIOR; gradient flow respects it.

## What differs from prior art (claim)
Structured pruning (LLM-Pruner, SlimLLM, BIP) prunes AFTER training. Alignment-Constrained Dynamic Pruning (2511.07482) constrains the pruning pattern. The espalier framing is a TRAINING-time hard zeroing of out-of-trellis gradients, with the trellis as a HUMAN-AUTHORED OFFLINE PRIOR (not learned), with multi-fine-tune accumulation along the same trellis. None of the surveyed work prescribes this exact discipline.
