# Run 32 — Real-Encyclopedia Pipeline Optimization Cycle

**One optimization cycle of the niche-finding pipeline.** The product is the
*pipeline* (params + process + agent coordination + decision-making); the
niche found/not-found verdict is only the ground-truth signal that steers
param updates. See `INHERITANCE.md` for why this run reconstructs the engine
(the run29–31 artifacts were not present in the repo).

## Pipeline stages (all instrumented)
| stage | file | what it does | quality metric |
|------|------|--------------|----------------|
| 1 merge engine | `engine/encyclopedia_engine.py::generate_constructs` | pair concepts across domains into constructs | % genuine-merge, cognitive-distance distribution |
| 2 integrity checker | `…::integrity_check` | genuine merge vs trivial/incoherent/restatement | false-pass / false-reject vs ground truth |
| 3 niche checker (R13) | `…::niche_check` | niche vs method-variant vs saturated (the key component) | false-pass / false-reject; variant-trap catch rate |
| 4 reasoning audit / coordination | `instrumentation/coordination_probe.py` | real Opus sub-agents audit constructs | retry / malformed rate |
| 5 determinism | `instrumentation/run_cycle.py` | re-run niche checker across PYTHONHASHSEED | decision-agreement rate |

## Inputs
- `engine/concept_banks.json` — real-encyclopedia bank (built by `build_concept_bank.py`).
- `engine/direction_params.json` — `direction_params` **v4** (inherited) + reconstructed v1–v4 lineage.
- `ground_truth/labeled_constructs.json` — curated labelled test fixtures incl. inherited traps M032/M005/M056 and new probes M057/M059/M060/M0B1/M0B2.
- `ground_truth/known_approaches.json` — registry of existing method families (incl. realistic near-duplicate families A4b/A9b).

## Run it
```
python3 engine/build_concept_bank.py
python3 ground_truth/build_ground_truth.py
python3 instrumentation/run_cycle.py          # emits results/*.json + the v4->v5 param update
```

## Outputs (`results/`)
- `run32_metrics.json` — per-stage quality metrics (this cycle, v4 and v5)
- `determinism.json` — v4 vs v5 decision-agreement across hash seeds
- `param_update_v4_to_v5.json` — each change + the measurement that motivated it
- `convergence.json` — the 4 convergence metrics vs prior runs
- `../REPORT.md` — the `[REPORT]`
