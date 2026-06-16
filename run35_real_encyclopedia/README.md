# Run 35 — Real-Encyclopedia Pipeline Optimization Cycle 4 (value scoring)

Inherits Run 34 (PR #68). Adds a generator-side **value/plausibility scorer** so
the pipeline outputs niches that are *useful*, not merely novel — and confirms
the production-ready decision pipeline does not regress.

## Headline
- decision pipeline **0 regressions** (niche 0/0, determinism 1.0, borderline 1.0)
- structural ontology: 24 properties, 219 precondition + 130 affordance tags (0 invalid)
- value-discrimination **0.50 chance → 0.75 structural-only → 0.833 +audit**; confidence gate **rejected** (0.792)
- at scale: novelty **99% → 41% high-precision structural-value** (novel ≠ useful, quantified)

## Reproduce
```
cd run35_real_encyclopedia
python3 value/build_value_ground_truth.py
python3 instrumentation/run_cycle.py      # decision regression + value-discrimination + at-scale value + v8
python3 instrumentation/convergence.py    # 6-cycle trajectory
```
Verdict: decision pipeline **production-ready**; value scorer **works** but value
is fuzzier than novelty; full (novel+useful) pipeline **approaching** production-
ready. Next target: mature the value half (audit coverage / ontology / GT).
