# R252 — life analogy

## Source domain: gecko setae van der Waals adhesion
- Hierarchical attachment: lamellae (mm) → setae (μm, ~1M per foot) → spatulae (nm, ~100 per seta).
- Adhesion is **angle-and-load-gated**: vdW force is in principle always present, but adhesion only manifests when (a) seta is preloaded perpendicular to surface, then (b) dragged tangentially to engage spatulae at correct angle. Reverse drag releases.
- The huge total contact area is achieved through DIVISION of contact into nanoscale spatulae; each spatula's vdW contribution is small but multiplied across population.
- Two-step ATTACHMENT: preload + drag = ON. Detachment is **directional**: a hyperextension reverses the angle → spatulae release.

## LLM analogy candidate
**Preload-and-drag gated adapter coupling (PDGAC)**: install a hierarchical adapter array (1024 nano-adapters per layer, each with low rank r=2, distributed across head-subspaces) that is **gated by a two-step "contact protocol"**: (1) PRELOAD = the input first triggers a perpendicular-direction selector that activates only the head-subspaces whose vector signatures align with the input's low-frequency content; (2) DRAG = a tangential-direction adapter pass injects the actual update only for activated nano-adapters AT the angle determined by preload. Reverse-angle inputs (detected via cosine sign flip) deactivate the adapter array, releasing the parameter "grip". The asymmetric two-step engagement gives high effective coupling per parameter while enabling clean release. Distinct from MoE: MoE selects experts but does NOT have a two-axis preload+drag gating; distinct from soft routing: routing is single-step. The directional release is also distinctive.

## What differs from prior art (claim)
HILO (2502.03884) varies adapter rank hierarchically but does not gate on two-step preload+drag. Generative Adapter (2411.05877) contextualizes in a single forward pass. Multi-Grained Patch Training (2501.15087) is multi-grained but not preload-and-drag. The asymmetric two-step contact protocol with reverse-angle release is not retrieved in surveyed prior art.
