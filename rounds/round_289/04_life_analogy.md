# R289 — life analogy

## Source: Korean ondol underfloor heating
- Firebox burns briefly + intensely → hot smoke routed through stone flue under floor.
- Floor stones (esp. mica) ABSORB and STORE the heat as thermal mass.
- After fire stops, stones SLOWLY RADIATE heat over 8-12 hours into the room.
- Net effect: brief expensive heat source amortized over long passive radiation.

## LLM analogy
**ONDOL-LLM (Thermal-Mass Amortized Inference)**: an inference-cache architecture where an expensive prefill ("burn") computes deep activations on a long shared-prefix prompt, and STORES them in a "thermal-mass" KV cache; subsequent short queries that share or partially share the prefix only re-read the cached activations (analogous to slow radiation from stored heat) — they spend NO new compute on the prefix. The prefix-warming is amortized across hours of subsequent queries; cache eviction is staggered like cooling-down stones.

## Differs from prior art (claim)
- TAPAS (2501.02600): thermal-aware scheduling at hardware level — not amortized prefix cache.
- Cooling Matters (2507.16781): hardware thermal benchmarking.
- BUT prefix-caching / shared-prefix KV reuse is a well-known LLM serving technique — vLLM, SGLang, prefix-tree-pool — directly equivalent functionally to the ondol metaphor. The "thermal mass" framing is metaphor for prefix-cache, not novel.
