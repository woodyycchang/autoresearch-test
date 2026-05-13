# Life Analogy — Marshall Islands rebbelib stick-chart pre-voyage memory

The **rebbelib** (Marshall Islands stick chart, micronesian wayfinding):
- Coconut-frond midrib framework; shells = island positions; threads = swell-direction patterns.
- 4 main ocean swells (rilib "backbone" + kaelib + bungdockerik + bundockeing).
- 3 chart types: **mattang** (abstract teaching), **meddo** (local), **rebbelib** (comprehensive chain).
- **Pre-voyage memorization**: chart studied + internalized; not consulted during voyage.
- Individual-only interpretation (each navigator's chart only readable by maker).

**REBBELIB-PRE-VOYAGE-CHART-COMPILE-MEMORY**: pre-voyage chart-compilation memory architecture with K-swell-direction tiers + island-anchor shells + abstract-mattang/local-meddo/comprehensive-rebbelib 3-tier curricular + personal-key interpretation. (1) **Pre-voyage compile phase**: at inference start, model "studies" a compiled chart embedding e_chart (precomputed structure for the task) for fixed K-tokens; afterwards e_chart is internalized via sparse-attention prior. (2) **K=4 ocean-swell tiers**: K-tier memory architecture with 4 swell tiers (backbone, secondary, tertiary, quaternary) — each tier holds a different abstraction level. (3) **Island-anchor shells**: discrete "shell" memory anchors at known reference points (analog of attention sinks at salient task entities). (4) **3-chart-type curricular hierarchy**: mattang abstract (training-time pattern learning) → meddo local (task-specific subgoal patterns) → rebbelib comprehensive (full-task chart) — model is trained on all 3 tiers. (5) **Personal-key interpretation**: each navigator's chart needs personal interpretation = model-specific embedding key e_id required to unlock chart (per-model finetune-specific compile). (6) **Sense-based-feel during voyage**: during inference, chart not re-consulted; instead model relies on internalized pattern + cross-attention to e_chart with low frequency (1-in-N forward passes). (7) Differs from R408 ICELANDIC + R428 WAVE-BOWL + R442 ADINKRA + R454 TIERED-KV + R470 CHILOTE + R479 OVOO + R492 STALLO + R504 GGANTIJA-APSIDAL-CORBEL by pre-voyage compile-phase + K-swell tier + island-anchor shell + 3-chart-type curricular + personal-key interpretation + low-frequency-consult inference.

## Adjacency
- MemOS Memory OS (closest tier)
- MemAgents ICLR 2026
- Awesome AI Memory
- Memory Age AI Agents Survey

Expected FAIL — multi-tier memory + curricular hierarchy + multimodal anchor literature fully covers.
