# R308 — life analogy

## Source: Hagfish (Eptatretus, Myxine) defensive slime
- Slime glands store compact "thread skeins" (~150 μm) of pre-coiled keratin-like protein.
- On attack, glands release skeins into seawater; mechanical agitation triggers rapid uncoiling — each skein unravels to ~15 cm thread (1000x length); 40 mg dry material expands to ~1 kg slime (25,000x volume).
- Result: predator's gills clogged; hagfish escapes.

## LLM analogy
**HAGFISH-SKEIN**: store a compact rank-r refusal "skein" (low-rank seed encoding pre-fabricated defensive activations) for each layer. On jailbreak classifier trigger, the skein is mechanically "agitated" — multiplied by a learned expansion operator E ∈ ℝ^(d×r) — and projected onto the active-context-window activations across the next K layers. Result: a defensive low-rank seed expands to a high-rank activation manifold that occupies attention capacity ("clogs" the adversarial signal's path).

## Differs from prior art (claim)
LoRA inverts: high-rank weight matrix factored to low-rank for parameter efficiency, but the expansion is OFFLINE during training. Defense literature uses fixed-shape defense outputs. None propose stored COMPACT SEED that EXPANDS by a tunable factor ON DEMAND during inference to occupy activation capacity defensively.
