# R317 — life analogy

## Source: Mediterranean amphora wax/pitch seal
- Ceramic amphora interior coated with pine pitch or beeswax to reduce permeability.
- Mouth sealed with clay/resin stopper after filling.
- Long-term storage for wine, oil, grain; tapered base allows sediment settling and easy burial.
- Seal integrity could be verified: intact seal = original contents undisturbed.

## LLM analogy
**AMPHORA-KV**: each KV-cache entry is "sealed" with a cryptographic content-hash on creation; long-lived cache entries carry the seal hash. On retrieval, the seal is verified — mismatch = tamper/corruption detection. Sealed entries can be safely shared across requests/sessions/devices with integrity guarantee. Pitch-coating analog: each KV entry is also stored with a per-token rounding-error compensation buffer to reduce "permeability" (precision loss under quantization).

## Differs from prior art (claim)
LMCache content-addressed S3 connector (2025) already uses content-hashes for KV addressing. Tutti SSD-backed KV cache (2026/5) provides persistence. None combine cryptographic seal verification + precision-compensation buffer — but content-addressing is already published.
