# Life Analogy — Bhutanese tshachu hot-spring sequential bathing

The **tshachu** (Bhutanese hot springs):
- 4 ponds at distinct temperatures (45/53/51/52°C).
- Each pond treats specific ailment (stomach/skin/jaundice/UTI).
- Astrologer-gated timing (day-of-month window).
- 1-hour limit per pond.

**TSHACHU-TEMP-GATED-ROUTING**: 4-temperature-tier ailment-specific routing with astrologer-gated context activation. (1) Define 4 temperature-tiers T = {45°C-equivalent, 53°C, 51°C, 52°C} corresponding to 4 sampling-temperature settings for inference. (2) Per query type, route to specific tier (stomach/factual=53°C, jaundice/reasoning=51°C, skin/code=52°C, general=45°C). (3) Astrologer-gating: temporal context window (16-30th day of month-equivalent = recent context window). (4) 1-hour limit per pond = max sampling-budget per tier before forced re-routing. (5) Differs from generic temperature sampling by 4-tier ailment-specific routing + astrologer temporal-gating + max-budget limit.

## Adjacency
- Router-R1 Multi-Round Routing (closest)
- Multi-Turn RL of LLM Agents
- Tree Search LLM Agent RL
- Tiered LLM Inference

Expected FAIL — multi-tier routing + temperature paradigm fully covered.
