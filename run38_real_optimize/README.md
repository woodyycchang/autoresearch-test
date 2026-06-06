# Run 38 — temporal + bottleneck + scaled-GT optimization (REAL banks)

Continues PR #71. Attacks ONLY the 2 structural failures (Failure 1: 99%
flag-rate / no precision; Failure 3: value ranks real niches as junk) with the
angles Run 37 didn't try, on the real 791-banks, scored against 43
WebSearch-verified real historical niches.

## Result (honest)
- **ANGLE 3 (scale GT 8->43):** done — 43 real niches, verified arXiv IDs.
- **ANGLE 1 (temporal/momentum):** NOT MEASURABLE — in-bank arXiv dates are
  citing-paper dates not emergence (ADMM 1976 tagged 2020); WebSearch can't
  return year-by-year counts; arXiv API/WebFetch 403-blocked. Reported, not faked.
- **ANGLE 2 (bottleneck):** 84% RECALL but ~0 PRECISION — all 8 attention-
  efficiency competitors share the bottleneck; no signal picks the 2 winners
  (Mamba, Longformer) from the 6 faded (top-ranked is faded Performer). The
  winner>faded mean is a 1-point Mamba artifact -> rejected (R14).
- **Failure 3 at 5x scale:** confirmed — median real niche at the 22nd
  percentile of random; 63% below random median.

**Verdict: failures 1+3 are PROVABLY STRUCTURAL for available data.** No
measurable pre-emergence signal ranks niches above random, separates real
winners from real losers, or gives precision; and the losers needed to learn
such a signal are unobservable (survivorship). Niche *prediction* is not
reachable by this method on this data; the defensible capability is
*recognition* (has this been done?), not prediction.

Reproduce: `python3 analysis.py`. Full detail: `REPORT.md`.
