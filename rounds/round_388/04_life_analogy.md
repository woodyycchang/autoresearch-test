# Life Analogy — Sumerian cuneiform clay tablet

**Cuneiform** writing uses a reed stylus to impress wedge-shapes into wet clay tablets, then dries/fires the tablet to lock in the inscription. Process:
- Stylus shape is **fixed** (wedge-tip) — limited primitive set.
- Wet clay surface accepts impression cheaply.
- After firing, the tablet is **permanent** (3000+ year survival).
- Each tablet records a fixed, immutable record (administrative, legal, literary).

The unique principle: **fixed-primitive impression on receptive substrate followed by fire-locking** — once fired, the tablet is unmodifiable. Pre-firing it is malleable.

## Analogical mapping → LLM training schedule

- Wet clay ↔ pre-fine-tune model state (malleable)
- Stylus wedge ↔ fixed-template prompt
- Impression ↔ fine-tuning gradient
- Fire-locking ↔ post-fine-tune freezing
- Tablet ↔ frozen LoRA adapter

The mechanism: a **clay-and-fire training protocol** — (i) malleable phase: fine-tune with fixed-template prompts only (small primitive vocabulary, like wedge shapes); (ii) impression phase: apply gradient updates from a SMALL FIXED template family of prompts only (no general data); (iii) firing phase: freeze the adapter and apply numerical stabilisation (quantize to INT8 + apply weight-mass projection); (iv) post-firing: adapter is read-only. Differs from standard fine-tuning (open template) by FIXED-PRIMITIVE PROMPT VOCABULARY restricted to a small wedge-set and explicit POST-TRAINING NUMERICAL FREEZE. The constraint produces predictable, narrow adapters with no over-fitting risk.
