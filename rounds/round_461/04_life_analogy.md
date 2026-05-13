# Life Analogy — Andean Khipu knotted-cord positional encoding

The **khipu** (Inca knot-based record-keeping):
- Knotted cords carry decimal positional values via knot-type × orientation × position.
- Multi-modal: color, fiber, weave-direction, ply-direction all encode information.
- Selective access: khipu-kamayuk specialist untie/re-tie knots between deposit sections.
- Reading proceeds top-to-bottom per cord, cord-category gates content decode.

**KHIPU-GATE**: a position-bit-encoded context-gating attention scheme. (1) Each context-token gets a small 4-8 bit *category-cord* embedding (color/fiber analog) that gates downstream attention access. (2) Layer L attention reads token i only if i.category_bits ∈ L.allowed_categories — selective layer-wise gating. (3) Positional decimal-knot analog: token's position-in-category encoded in a small low-bit code that participates in attention scoring. (4) Selective re-tie analog: tokens can be promoted/demoted between gates during prefill (no extra parameters).

## Adjacency
- SqueezeAttention layer-wise KV budget
- KVQuant 2-bit/4-bit positional quantization
- RetrievalAttention selective KV retrieval
- TidalDecode position-anchored selective KV

Expected FAIL — gated KV retrieval + layer-wise budget is mainstream.
