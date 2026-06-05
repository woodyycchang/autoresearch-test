# Run 33 — Real-Encyclopedia Pipeline Optimization Cycle 2

Inherits Run 32 (PR #66). Attacks the two bottlenecks Run 32 measured:
**(1) scale** the bank (80 → 314 real concepts) and **(2) wire the
reasoning-audit** in as a confidence-gated borderline adjudicator (v6).

## Stages (all instrumented, all real)
| stage | file | metric |
|------|------|--------|
| 1 merge engine @ scale | `engine/encyclopedia_engine.py` | genuine-merge rate + cog-distance on 314-bank |
| 2 integrity | `…::integrity_check` | false-pass/reject |
| 3 niche checker (v5 vs v6) | `…::niche_check` (+`borderline_rule=audit_gated`) | false-pass/reject; **borderline adjudication accuracy** |
| 4 coordination | 13 harvest + 5 audit Opus agents | completion, self-correction, schema validity |
| 5 determinism | `instrumentation/{_niche_worker,_scale_worker}.py` | agreement across seeds, incl. at scale |

## Layout
- `engine/concept_banks.json` — 314 concepts / 27 domains (80 curated + 234 harvested).
- `harvest/` — controlled vocabulary + `harvested_concepts.json` (real source URLs).
- `ground_truth/labeled_constructs.json` — 21 fixtures incl. 5 borderline (BN/BV).
- `reasoning_audit/frozen_audit_table.json` — real Opus audit verdicts (frozen → deterministic).
- `engine/direction_params.json` — v5 base (+ v1–v5 lineage); `results/direction_params_v6.json` — derived v6.
- `results/` — `run33_metrics`, `determinism`, `borderline_adjudication`, `param_update_v5_to_v6`, `convergence`, `coordination`.
- `REPORT.md` — the `[REPORT]`.

## Reproduce
```
cd run33_real_encyclopedia
python3 engine/build_concept_bank.py        # 314-concept bank (deterministic)
python3 ground_truth/build_ground_truth.py
python3 instrumentation/run_cycle.py        # all metrics + derive v6 (seed sweep deterministic)
python3 instrumentation/convergence.py
```
(The reasoning-audit table is frozen/committed, so the pipeline reproduces
without re-invoking the LLM.)

## Headline result
Merge quality held at 3.9× scale (88.86%); determinism 1.0 including over 9,632
generated merges; **borderline-adjudication accuracy 0.40 → 1.00** via the
audit gate, determinism preserved. Verdict: **converged / approaching
production-ready**; next target = scale the 12-family known-approach registry.
