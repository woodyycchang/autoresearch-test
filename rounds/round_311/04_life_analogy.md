# R311 — life analogy

## Source: Olive press multi-stage extraction
- Olives crushed once; resulting paste pressed/centrifuged multiple times.
- First press = lowest acidity oil with highest polyphenols (extra virgin).
- Subsequent presses (under heat) yield lower quality "virgin" then "olive" oil.
- Different physical/chemical fractions extracted from SAME source by sequential mechanical extraction with different conditions per pass.

## LLM analogy
**PRESS-TUNE**: multi-stage progressive fine-tuning. Pass 1: gentle low-loss SFT on highest-quality data only → extracts most-preferred-response capability. Pass 2: higher-temperature DPO with diverse data → extracts diverse-response capability. Pass 3: low-rank deep adapter on raw web → extracts open-ended-generation capability. Each pass targets a different capability "fraction" with stage-specific optimizer/temperature/data.

## Differs from prior art (claim)
GLPFT (global-to-local progressive FT) sequences general → specific. CPT/SFT/RLHF/merging pipeline is mainstream. PRESS-TUNE explicitly maps olive-press fractionation onto multi-stage capability extraction — but the multi-stage progression itself is mainstream pipeline (CPT → SFT → DPO/RLHF → merge).
