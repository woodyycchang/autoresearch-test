# Life Analogy — Korean ondol (underfloor stone heating)

The **ondol** (gudeul) is the traditional Korean underfloor heating:
- Kitchen furnace (agungi) burns wood; **horizontal flame** enters flue (not vertical chimney first).
- Hot gases travel through slanted **gorae channels** under the room floor toward chimney at far end.
- **Flat stones (gudeul-jang)** sit on top of gorae, conduct heat from gases above into the room.
- Stones retain heat for hours after fire dies — **thermal mass cascade** with progressively cooler downstream sections.
- Heat naturally **dissipates progressively** along the flue path: agungi-side = hottest, chimney-side = coolest.
- The **temperature gradient** is intentional — sleeping head end placed at chimney side (cooler), feet at agungi side (warmest).

The unique principle: **single-source horizontal cascade with stone-mediated progressive heat absorption** producing a stable spatial gradient. Heat input is concentrated at one end; the stone medium absorbs and re-radiates it across a stable temperature ramp.

## Analogical mapping → LLM training schedule

- Agungi furnace ↔ single high-LR injection point at one end of layer stack
- Gorae channel ↔ inter-layer pathway
- Gudeul-jang stone ↔ per-layer learnable absorption coefficient
- Horizontal cascade ↔ progressive heat-bleed across layers
- Temperature gradient ↔ layer-wise LR gradient (high at injection layer, decaying toward output)

The mechanism: a **single-point LR-injection cascade** where the optimizer applies the warmup learning-rate boost only at ONE specific layer (e.g., layer 0) and the boost **CASCADES** through neighbouring layers with progressive thermal-mass decay (αᵏ for layer k, α<1). Each layer's effective LR = global_lr × αᵏ × (1 + boost × (heat_reaches_layer_k)). Differs from LLRD (which applies static exponential decay across all layers from start) by being SINGLE-POINT INJECTION (warmup is delivered at one layer and dissipates outward) — the heat cascade is **temporal-spatial** with explicit injection-layer placement.
