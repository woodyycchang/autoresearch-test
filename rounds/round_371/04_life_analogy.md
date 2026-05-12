# Life Analogy — Mongolian airag slow continuous fermentation

Mongolian **airag** (fermented mare's milk, kumis) is produced by a unique slow-feed continuous fermentation:
- **Started once at season begin** (mid-June).
- **3000-5000 stirs over 1-2 days** to initialize bacterial culture.
- **Daily continuous additions** of fresh milk + 3000-5000 stirs per day.
- **Never reset**: same starter ferments all season.
- **Khukhuur stationed at ger entrance** — everyone passing through gives it a stir (distributed maintenance).

Key features:
- **Single starter, continuous feed**: living culture is preserved over months.
- **Daily small additions**: not one-shot batch.
- **Distributed stirring** (all family members): not centrally maintained.
- **Slow accumulation** of fermented mass: never converges, always evolving.
- **Seasonal cycle reset only annually**: long-running stable state.

## Analogical mapping → LLM training schedule

- Starter culture ↔ pretrained checkpoint
- Daily fresh milk addition ↔ daily incremental fine-tuning data
- 3000-5000 stirs/day ↔ many small gradient steps per day
- Never reset ↔ no full retraining, only incremental updates
- Distributed stirring ↔ federated/distributed small updates
- Seasonal cycle ↔ annual major recheck/refresh

The mechanism: a **continuous-ferment fine-tuning** regime where (i) a single starter checkpoint is initialized; (ii) every day, a small data batch is added; (iii) many small gradient steps integrate it; (iv) no full restart for the whole annual cycle. Different from continual learning (which often does full retraining cycles) and from RLHF (which is episodic) — this is *always-on slow-fermentation* with daily small data + many micro-updates and an annual cycle.
