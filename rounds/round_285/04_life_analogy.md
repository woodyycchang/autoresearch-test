# R285 — life analogy

## Source domain: Mudskipper amphibious dual-mode respiration
- Mudskipper occupies both water (burrow) and land (mudflat).
- In water: GILL respiration via standard fish ventilation.
- On land / in air-filled burrow at high tide: CUTANEOUS respiration (skin uptake) + BUCCAL AIR POCKET (gill chamber holds an air bubble); brief water-flush periodically rewets gill surface.
- The mode-switch is TRIGGERED BY AERIAL HYPOXIA SENSING (aquatic hypoxia does NOT trigger switch).
- CRUCIAL: each mode shares ONE common organ (gill chamber) reconfigured by a VALVE; the same anatomy serves both modes via a binary switch.

## LLM analogy candidate
**MUDLLM (Mudskipper Substrate-Switching LLM)**: an LLM inference architecture where a SINGLE SHARED memory/compute region serves BOTH inference modes (e.g., on-device tiny-model + cloud big-model) via a VALVE-like gate that reconfigures the SAME KV cache + same attention layer routing rather than maintaining separate per-mode infrastructure. The mode switch is triggered by an EXPLICIT HYPOXIA SIGNAL (output uncertainty threshold + latency budget exceeded), NOT by a default routing policy or pre-set load balancer.
- One shared neural cache, two routing modes; cheap mode active by default, expensive mode triggered only by hypoxia signal.
- The valve is a sparse gate that re-uses the same parameters / cache in different reading patterns.

## What differs from prior art (claim)
- Edge-Cloud collaborative inference (2507.16731): routes between separate inference resources; the local/remote infrastructure is DIFFERENT.
- HybridGen (2604.18529): CPU+GPU hybrid attention; both run continuously.
- Adaptive Edge-Cloud (2512.12769): dynamic load balance, not a SINGLE-RESOURCE valve switch.
- MUDLLM's distinguishing feature: ONE physical resource (KV cache + attention layer) operates in two modes via a binary valve triggered by hypoxia-signal; not two separate resources orchestrated.
