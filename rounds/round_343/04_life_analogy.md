# R343 — life analogy

## Source: Pufferfish self-inflation defense
- Senses threat → rapidly draws water through mouth + closes gill covers.
- Stomach expands 50-100x via folds; total volume +3x in <15s.
- Spines erect during inflation = added defensive layer.
- High physiological cost (heart rate spikes, O2 consumption rises).

## LLM analogy
**PUFFER-CAPACITY**: context-triggered on-demand model capacity expansion under detected adversarial input. When a side-detector flags adversarial/jailbreak input, the inference engine RAPIDLY loads additional reasoning-mode LoRA + a self-reflection chain + safety-judge model — temporarily 3x compute. Idle state = baseline cost; threat state = inflated capacity. Cost-aware: limited inflation budget per session.

## Differs from prior art (claim)
Progressive Self-Reflection (EMNLP 2025) uses self-reflection always-on. Standard guardrails are always-on. Reasoning-mode routing is task-class triggered. PUFFER-CAPACITY differs by THREAT-DETECTOR-TRIGGERED rapid CAPACITY INFLATION (3x compute, multiple safety stages enabled) only on detected adversarial input, with explicit cost budget.
