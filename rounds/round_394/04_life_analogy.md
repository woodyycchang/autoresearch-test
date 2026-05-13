# Life Analogy — Inca tampu way-station network

The **Inca tampu network** consisted of:
- **Tampu** (rest stations) at one-day-walking intervals along the road system.
- **Chasqui-wasi** (runner houses) every ~2.5 km for relay messengers.
- Tampu acted as **standardized modular** structures providing rest/supplies/storage.
- Network covered the 1200-mile Cuzco-to-Quito route with 5-day relay delivery.

The unique principle: **standardized modular way-stations at regular intervals along a fixed path, each providing a fixed capability set (rest, supplies, storage)** — interchangeable and composable.

## Analogical mapping → LLM modular insertions

- Inca road ↔ transformer layer stack (fixed path)
- Tampu way-station ↔ pluggable adapter module
- Chasqui-wasi ↔ smaller, more frequent adapter (per-attention)
- Standardised structure ↔ uniform adapter interface
- One-day-walk interval ↔ every K-layers insertion

The mechanism: a **two-level adapter spacing scheme** — major adapters (tampu) inserted every K layers (e.g., every 4 layers) providing full PEFT capability; minor adapters (chasqui-wasi) inserted at finer granularity (every-layer) providing lightweight rank-1 sub-adapters. The two levels operate at different parameter budgets + different scales. Differs from prior single-level adapter insertion (LoRA at every layer with same rank) by EXPLICIT TWO-LEVEL SPACING with DIFFERENT FUNCTIONS per level. Adjacent to Mixture-of-Adapters but distinct in fixed-spacing-two-level scheme.
