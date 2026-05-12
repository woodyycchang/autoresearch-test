# Life Analogy — Tibetan tsampa pre-roasted portable food

**Tsampa** is roasted barley flour, the staple food of Tibetan nomads, monks, and pilgrims. Key properties:
- **Pre-roasted at home** — the energy-intensive cooking is done ONCE, before travel.
- **No further cooking needed** — just mix with hot butter tea and eat.
- **Carried in leather pouch** — extremely portable.
- **Roasting breaks down starches** — rapid digestion = rapid energy on the trail.
- **Long shelf life** — stable for months.

The principle: shift the *expensive preprocessing* from the field (where energy and time are scarce) to the home (where they are abundant). Bring the *preprocessed* result, not the raw ingredients.

## Analogical mapping → LLM offline context preconditioning

- Pre-roasting at home ↔ offline KV-prefill computation on common contexts
- Carrying in leather pouch ↔ KV cache as a portable artifact
- Mix with butter tea ↔ runtime composition with user-specific prompt
- Rapid energy = rapid digestion ↔ TTFT reduction via pre-loaded KV

The mechanism: **pre-roasted KV prefills shipped as serialized portable artifacts**, where commonly-occurring system prompts, retrieval contexts, or task-specific scaffolds are KV-prefilled OFFLINE (analogous to roasting), serialized to a compact portable representation (analogous to leather pouch), and "rehydrated" with butter tea (a small per-query prefix) at inference time. Different from prefix-caching which stores already-served context — this is *anticipatory* offline computation of contexts the user has not yet asked.
