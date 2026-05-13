# Life Analogy — Inuit qajaq (Arctic skin-on-frame kayak)

The traditional **qajaq** is a sea-kayak built by Inuit hunters out of driftwood ribs and gunwales lashed with seal sinew, then covered with stretched seal skin. Distinctive features:

- **Per-frame elastic ribs**: ribs are steamed and bent into C-shape; each rib acts as a spring independently of the gunwale-frame.
- **Sinew lashings**: every joint is **lashed** (not nailed/glued), so each rib-to-gunwale joint can flex independently.
- **Per-frame impact dampening**: when waves hit, each frame absorbs and releases energy through its own elasticity instead of conducting shock rigidly along the hull.
- **Skin tensioning**: the seal skin is stretched and allowed to *shrink-fit* to the frame, producing per-frame surface tension. The skin is taut at rest but slips on the lashed frame under stress.

The unique principle: **per-frame independent elastic dampening** — each structural unit (rib) can flex without transmitting shock to its neighbour rib. The hull as a whole is therefore **passively dampened layer-by-layer**.

## Analogical mapping → LLM training stability

- Each rib ↔ each transformer layer
- Rib elasticity ↔ per-layer gradient absorption coefficient (a learnable scalar)
- Sinew lashing flexibility ↔ inter-layer gradient coupling strength
- Skin tensioning ↔ pre-LN / post-LN normalization tension
- Wave-shock ↔ gradient spike (loss spike during pretraining)
- Per-frame independent dampening ↔ per-layer independent gradient-shock dampening, **scheduled stronger at outer layers (gunwale) and weaker at inner layers (centre rib)**

The mechanism: a **per-layer trainable elastic-dampening coefficient** that scales gradient propagation between layers as a function of gradient-norm spike detection. Each layer can locally absorb a spike before propagating to its neighbour; the per-layer coefficient is learnable and **anti-correlates** with depth (outer layers absorb more, inner layers preserve signal).
