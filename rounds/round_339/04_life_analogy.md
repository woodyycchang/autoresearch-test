# R339 — life analogy

## Source: Snowshoe hare seasonal coat-color swap
- Two phenotypes: summer brown, winter white. Same hare body, different coat.
- Triggered by photoperiod (day-length sensor) → melatonin signal → ASIP/agouti switches melanin pathway.
- 10-week transition; gradual swap from extremities toward core.
- Switch is bidirectional and seasonally entrained.

## LLM analogy
**SEASONAL-LORA**: pre-train TWO LoRA adapter sets per task domain — one for high-throughput deployment ("summer/brown"), one for high-accuracy reasoning ("winter/white"). External context sensor (request urgency, latency budget, expected query difficulty) acts as photoperiod and triggers a GRADUAL 10-step bias-blend swap between the two. Hare biology: it's not instant, and the same base model uses both adapter sets — analogous to summer/winter coat of the same animal.

## Differs from prior art (claim)
LoRA hot-swap (per-request adapter loading) is instant. MoE routes per token. Standard fine-tuning produces one model. SEASONAL-LORA differs by maintaining TWO simultaneous adapter sets per task on the same base model with EXTERNAL context-sensor-driven GRADUAL bias-blend over multiple steps — biologically-inspired phenotypic alternation.
