# R272 — life analogy

## Source domain: Aztec chinampa floating garden
- Long narrow rectangular plots (~6-10m × 100-200m) of mud anchored with willow + reed fences, surrounded by shallow lake canals.
- The canals carry **continuous moisture + nutrient supply** from decomposing organic waste in the lake.
- Farmers DREDGE muck from canals onto plots as fertilizer — a continuous nutrient cycle between water and soil.
- Each plot has its OWN soil but shares the COMMON CANAL WATER as nutrient supply.

## LLM analogy candidate
**Chinampa-style shared-canal in-context plot array (CSCIPA)**: a multi-agent or multi-task LLM system in which (1) each "plot" is a TASK-SPECIFIC in-context buffer (a private chunk of dedicated context tokens carrying the task's working state). (2) Plots are arranged in a GRID, each with its own task. (3) A SHARED "canal" of system-wide context (recently-completed reasoning summaries, knowledge from sibling plots) flows around all plots and is periodically DREDGED into each plot as nutrient — a slim fact/insight extracted from the canal is added to the plot's in-context buffer when relevant. (4) Each plot's outputs are dumped back to the canal, decomposed into key insights, and become nutrient for other plots. Distinct from shared workspace MAS: CSCIPA has periodic dredging + plot-specific soil + canal as decomposed nutrient pool.

## What differs from prior art (claim)
SCoL (2605.07076), InCA (2412.15563), Memini (2605.05097) cover continual context-based knowledge incorporation. None retrieve a plot-array + shared canal nutrient cycle + periodic dredging combo at multi-agent in-context level.
