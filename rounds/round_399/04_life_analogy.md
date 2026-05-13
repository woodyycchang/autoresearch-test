# Life Analogy — Korean kimchi multi-stage fermentation

**Kimchi** ferments through distinct biological stages:
- **Stage 1 (salting/brining)**: cabbage soaked in 3-7% brine, killing harmful bacteria (selection).
- **Stage 2 (early fermentation, ~15°C)**: heterolactic Leuconostoc dominate; produce lactic + acetic acid + CO2.
- **Stage 3 (mid fermentation, ~10°C)**: Lactobacillus brevis + plantarum dominate; deeper acidification.
- **Stage 4 (cool storage, ~4°C)**: psychrotrophic LAB; flavor refinement.
- Different stages use different temperatures + different microbial communities + different metabolic targets.

The unique principle: **MULTI-STAGE BIOLOGICAL TRANSITION with explicit microbial-community SHIFTS at each stage and TEMPERATURE-controlled phase boundaries** — sequential bacterial communities each playing a distinct role.

## Analogical mapping → LLM training pipeline

- Brine selection ↔ initial pretrain data filter
- Stage 2 early ferment ↔ broad pretrain
- Stage 3 mid ferment ↔ domain-specific training
- Stage 4 cool storage ↔ alignment + safety training
- Different microbial communities ↔ different training-data distributions
- Temperature control ↔ learning-rate decay across stages

The mechanism: a **4-stage temperature-controlled LLM training pipeline** with EXPLICIT MICROBIAL-COMMUNITY-ANALOG distribution shifts at each stage. Stage 1 PRE-FILTER (data filter + deduplication, "brining"). Stage 2 BROAD-PRETRAIN (broad data mix, LR=high, "warm ferment"). Stage 3 DOMAIN-FINE-TUNE (specialized domain data, LR=med, "mid ferment"). Stage 4 ALIGNMENT-COOL (RLHF/SFT, LR=low, "cold storage"). Each stage uses a CHARACTERISTIC DATA DISTRIBUTION + LR + DURATION. Differs from generic multi-stage pretraining (which uses similar phases but without explicit microbial-community-style distribution shifts framed as biology) — but functionally similar to existing annealing-style mid-training.
