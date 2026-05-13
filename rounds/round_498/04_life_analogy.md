# Life Analogy — Inca Moray terraced microclimate

The **Moray terraces** (Inca, Peru):
- 12 concentric circular levels descending 150m.
- 12-15°C gradient top-to-bottom (microclimate per elevation).
- 250+ crop varieties tested at different elevations.
- Each level = distinct microclimate basin for robustness validation.

**MORAY-12-LEVEL-BASIN**: 12-level micro-basin temperature/lr-schedule across training stages for robust generalization. (1) Partition training schedule into 12 "elevation levels" each with distinct temperature τ_level + LR_level (gradient steepness analog). (2) Each level: validate on micro-basin perturbation subset (synthetic distribution shifts). (3) Crop variety test: at each level, model evaluated on 250+ task variants (long-tail OOD). (4) Robust model = one passing all 12 levels' micro-basin tests. (5) Stairstep schedule: descend by 1 level when current micro-basin test passes; ascend if perturbation tests fail. (6) Differs from R460 LEVADE-LIPSCHITZ + R485 JABAL-DRUZE-CHOKEPOINT by 12-level explicit temperature/LR schedule + per-level OOD validation.

## Adjacency
- Curriculum Learning LLM Pretraining (closest, 2601.21698)
- Self-Evolving Curriculum Boltzmann τ
- Curriculum Temperature for KD AAAI
- Mid-Training of LLMs

Expected FAIL — curriculum + temperature schedule paradigm fully covered.
