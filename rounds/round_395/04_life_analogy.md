# Life Analogy — Mongolian deel multi-layer winter clothing

The **Mongolian deel** is a layered winter clothing system:
- **Layer 1 (innermost):** fine silk for moisture-wicking.
- **Layer 2:** medium wool for thermal trapping.
- **Layer 3:** thick wool / animal skin for insulation.
- **Layer 4 (outermost deel):** wind/water barrier + belt for closure.
- Each layer has a **specialized function**; together they keep the wearer alive in -40°C steppe winters.
- The deel + layers are **loose enough to allow air pockets** for extra insulation.

The unique principle: **functionally-differentiated 4-layer stack** — each layer does ONE specific job (wicking / trapping / insulating / blocking), and together they form a stable thermal envelope.

## Analogical mapping → LLM safety stability

- Layer 1 silk ↔ input pre-filter (moisture-wicking = malicious-input drying)
- Layer 2 wool ↔ in-context safety prompt
- Layer 3 thick wool ↔ aligned-model safety training (deeper)
- Layer 4 deel ↔ output post-filter (wind barrier)
- Belt ↔ deterministic policy enforcement
- Air pockets ↔ uncertainty buffer

The mechanism: a **4-stage functionally-differentiated safety stack** for LLM-based applications — Stage 1: input pre-filter (PII scrubbing, syntax check, "wicking"); Stage 2: in-context safety preamble (soft constraints, "wool trap"); Stage 3: alignment-trained model (RLHF safe-output bias, "thick insulation"); Stage 4: output post-filter (toxicity/PII/jailbreak detection, "wind barrier"). Each stage runs sequentially. Differs from prior defense-in-depth (which uses similar stages but functionally homogeneous filters) by requiring EACH STAGE TO HAVE A DISTINCT FUNCTIONAL ROLE (wick/trap/insulate/block) with explicit functional non-overlap.
