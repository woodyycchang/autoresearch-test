# Life Analogy — Korean Jeju Haenyeo sumbisori-coordinated diving pool

The **Haenyeo** (Jeju sea-women):
- Each diver holds breath ~1-3 min underwater (up to 20m depth) per dive.
- Surfaces with **sumbisori** sharp whistling sound — rapidly expels CO2, signals "I'm up".
- Collective community — multiple divers share the bay, coordinating dive cycles.
- Matrilineal knowledge transmission of locations + technique.

**HAENYEO-PHASE**: a multi-expert (or multi-agent) LLM inference pool with **coordinated dive-surface phase scheduling**. Each expert dives (runs intensive K-token computation) then surfaces, emitting a shared **sumbisori** synchronization signal token. Pool-wide phase-coherence rule: at any time only M/N experts are diving (computing), others recovering/holding context. Cross-expert phase coupling via shared timing-anchor stream produces collective coherent output.

## Adjacency
- LLM Inference Scheduling Survey 2025 TechRxiv
- Aegaeon SOSP 2025 GPU pooling synchronized serving
- Agent.xpu 2506.24045 heterogeneous SoC dispatch
- PerLLM 2405.14636 edge-cloud personalized inference scheduling

Expected FAIL — synchronized expert-pool inference scheduling is heavily covered in 2025-2026 systems literature.
