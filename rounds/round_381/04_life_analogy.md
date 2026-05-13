# Life Analogy — Hopi katsina spirit-mask ritual

In Hopi tradition, when a dancer puts on a **katsina mask** + appropriate costume + body paint, his **personal identity is ritually suppressed**. The spirit-being depicted by the mask takes his place — the dancer becomes the katsina, not an actor playing one. Specific features:
- Ritual is **schedule-locked**: katsinim visit for half of each year only.
- Identity-suppression is **mask-bound**: removing the mask returns the dancer to his everyday self.
- Many distinct katsinim (500+) each with own mask + role.
- The mask is treated as a **conduit**: it doesn't *contain* the spirit, it *enables* the spirit's presence.

The unique principle: **identity null-space substitution via ritual mask** — the dancer's everyday persona-vector is *suppressed into null space* while the katsina's persona-vector is *projected onto the active subspace*. The mechanism is reversible (mask removal restores). Multiple identities are interchangeable via mask swap.

## Analogical mapping → LLM safety persona

- Personal identity ↔ default model persona (everyday "I am a helpful assistant")
- Katsina mask ↔ explicit persona-vector overlay
- Identity suppression ↔ projecting current persona-activation onto null-space of overlay subspace
- Mask removal restoration ↔ deactivating overlay returns default persona
- Ritual schedule ↔ runtime activation/deactivation window

The mechanism: a **persona-mask projection layer** at runtime where (a) a learned per-mask projection matrix M_k ∈ R^(d×d) is precomputed for each safety persona; (b) at inference, model hidden states h_ℓ at chosen layers are decomposed into (M_k h_ℓ) — the persona-aligned component — plus (I − M_k)(h_ℓ — the null-space residual; (c) the residual is **suppressed by factor β** (β ∈ [0,1]; β=0 = full mask, β=1 = no mask); (d) different masks (e.g., "child-safe", "expert-mode") swap M_k at runtime without retraining; (e) the operation is fully reversible.

This differs from system-prompt persona prompts (which just steer via tokens) by acting **directly on hidden-state subspaces** with **explicit reversibility** and **swappable mask matrices**.
