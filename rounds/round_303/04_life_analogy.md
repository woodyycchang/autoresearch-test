# R303 — life analogy

## Source: Velvet worm (Onychophora) slime-jet projectile
- Pair of oral papillae squirts liquid proteinaceous slime in two oscillating streams (30-60 Hz) at 3-5 m/s.
- Slime is sticky liquid in jet; rapidly forms solid disordered fiber web on impact via mechanical-agitation-triggered phase change.
- Acts at distance: prey/predator immobilized by adhesive entanglement, not by source-proximate puncture.

## LLM analogy
**SLIME-NET**: targeted projectile-style adversarial-token immobilization. On detection of an adversarial token at position p, project a learned "adhesive binding vector" to position p+k (the projected propagation target) so that when adversarial activation arrives at p+k, it triggers a precomputed liquid-to-solid phase change in the local attention pattern (transition from soft attention weights to a hardened, low-rank stop-state matrix) — entangling adversarial signal at downstream location rather than just blocking it at source.

## Differs from prior art (claim)
Stinging-nettle/AutoDefense fire at source on trigger. Token ablation prunes at source. Activation steering modifies direction at source. SLIME-NET projects defense to a DOWNSTREAM activation location with TWO-PHASE liquid-then-solid transition triggered by adversarial-feature arrival.
