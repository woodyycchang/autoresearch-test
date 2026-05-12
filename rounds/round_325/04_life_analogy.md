# R325 — life analogy

## Source: Mudskipper bimodal respiration
- In water: gill respiration (fish mode).
- On land: cutaneous skin + buccal lining respiration (amphibian mode); 76% O2 via skin.
- Switches modes by detecting environmental presence (water vs air).
- Special valve closes gill slit in air mode to retain moisture.

## LLM analogy
**MUDSKIP-MODE**: dual-mode inference engine. Mode A (water/batch): full prefill + attention, GPU-throughput-optimized. Mode B (land/streaming): KV-cache-light decode, low-latency-optimized. Engine detects request-mode signal (batch size, request urgency) and switches between modes; a "valve" mechanism handles transition state without losing context.

## Differs from prior art (claim)
KVPR I/O-aware KV cache. Latency-aware LLM customization (USENIX ATC 2025). Adaptive batching frameworks switch between batch/decode phases. MUDSKIP-MODE re-frames as bimodal — close to dual-phase serving with adaptive mode switching.
