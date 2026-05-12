# R269 — life analogy

## Source domain: Khmer Angkor baray hydraulic cycle
- 4 large reservoirs (West, East, Preah Khan, Indratataka) with total storage ~100 million m³.
- During the **monsoon (wet season)**: rainwater is COLLECTED into the barays via channels.
- During the **dry season**: water is RELEASED through a downstream canal network to surrounding rice paddies, enabling year-round cultivation.
- The system is PHASE-LOCKED to the annual climate cycle — ingest and output happen in distinct phases of the year, mediated by the reservoir buffer.

## LLM analogy candidate
**Baray-buffered phase-locked training cycle (BBPLTC)**: in continual training of a long-running deployed LLM, alternate between two synchronized phases:
- **Wet phase** (e.g., daytime / high-traffic window): the model COLLECTS gradients from real user interactions, but instead of updating weights immediately, gradients are written to a **baray reservoir** = a large slow-evicting gradient memory of size ~10⁹ entries.
- **Dry phase** (e.g., nighttime / off-peak): the reservoir is DISTRIBUTED into the model via batched fine-tuning. The model is NOT updated during the wet phase (decoupling from inference latency), and the reservoir provides smoothed gradient batches during the dry phase (smaller variance).
- The wet-dry phase split is PHASE-SYNCHRONIZED with deployment traffic patterns rather than arbitrary time slicing. Distinct from Mid-Training (2510.06826) which is offline-only. Distinct from Periodic Asynchrony (2511.18871) which is workflow async, not seasonal-cycle phase-lock.

## What differs from prior art (claim)
Mid-Training (2510.06826), Periodic Asynchrony (2511.18871), LR-Decay-Free pretraining (2603.16127) cover training-schedule research. None retrieve a baray-buffered wet-collect + dry-distribute phase-locked traffic-synced continual-training cycle.
