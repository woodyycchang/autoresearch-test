# Run 37 — optimize against the external backtest (on the REAL banks)

Continues PR #70. Targets the 3 measured failures from the Run 36 external
backtest, on the **real run31 791-concept banks**, scored against **8 real
WebSearch-verified historical niches** (not self-made fixtures). Self-metrics
banned as success evidence (R12).

## Honest result
- **Contamination (R13):** 7/8 niche families are literal entries in the real
  2026-harvested bank -> the banks contain the answers. All tests use a
  decontaminated 774-concept corpus.
- **Failure 2 (frame 5/8->8/8):** FIXED in representability (`niche_types.py`
  adds emergent-phenomenon / scaling-law / prompting-format templates) — but
  representability != predictability.
- **Failure 3 (value ranking):** NOT FIXED, structural. 3 principled niche-blind
  signals tested; MoE ranks bottom-5%, RLHF bottom-0.3%; median niche ≈ random.
- **Failure 1 (flag-rate/precision):** NOT FIXED. A value-gate retaining the
  weakest real niche still admits 97.7% of random merges.

**Verdict: no real-history predictive value.** Failures 1 & 3 are structural.
The buyer's answer remains No. Full detail: `REPORT.md`. Reproduce:
`python3 real_history_experiments.py` and `python3 niche_types.py`.
