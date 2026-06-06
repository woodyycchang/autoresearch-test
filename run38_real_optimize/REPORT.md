# [REPORT] Run 38 — temporal + bottleneck + scaled-GT, on the REAL banks

Continues PR #71. Attacks ONLY the 2 structural failures (1: 99% flag-rate /
no precision; 3: value ranks real niches as junk) with the three angles Run 37
did not try, on the real 791-banks, scored against real history. Ground truth =
**43 WebSearch-verified historical ML niches** (real arXiv IDs/years).
Reproduce: `python3 analysis.py`. Raw: `analysis_results.json`, `niches_gt.json`.

## Contamination handling (R13)
Niche family name-words are dropped from the corpus before any signal is
computed (decontaminated corpus: 637 concepts). The banks literally contain the
niches (Run 37 finding), so this is mandatory.

## ANGLE 3 — scale the ground truth: DONE (8 → 43 real niches)
5 Opus agents harvested 43 real niches with **verified arXiv IDs/years** across
efficiency, PEFT, alignment, training, architecture/reasoning (2013–2024). This
is the prerequisite for honest held-out testing; it is also the only angle that
fully succeeded.

## ANGLE 1 — temporal / momentum: NOT MEASURABLE (reported, not faked)
A pre-emergence field-momentum signal needs historical paper-count time series.
Neither source is available here:
- **In-bank arXiv dates are wrong for this purpose** — they are the *recent
  citing paper* the harvester found, not emergence dates: ADMM (1976) is tagged
  `2012.07401`=2020; interior-point (1984) is tagged `2410.15731`=2024; 93/215
  tech entries are dated 2026. Unusable as emergence dates.
- **WebSearch cannot return year-by-year counts** — verbatim from the tool:
  *"the search results don't contain specific numerical data for the exact years
  you requested."* WebFetch/arXiv-API are 403-blocked.

So ANGLE 1's quantitative version cannot be measured with available tools. Not
attempted-and-failed — **infeasible to measure**; reported as such rather than
fabricating counts (R5).

## ANGLE 2 — bottleneck signal: HIGH RECALL, ~ZERO PRECISION
The agents flagged, per niche, whether the target problem was a **known
pre-dating bottleneck** (with a citable pre-dating paper).
- **Recall: 36/43 (84%)** of real niches addressed a known bottleneck. So
  "targets a known limitation" describes most winners — but also most *losers*.
- **Precision test (the decisive one).** The efficiency cluster has **8 methods
  that all hit the SAME attention-quadratic bottleneck** (all `bottleneck_before
  = true`). Of these, 2 broadly won (Mamba, Longformer) and 6 faded (Sparse
  Transformer, Reformer, Linformer, Performer, Nyströmformer, FNet). The best
  signal ranks them:

  | method | outcome | gxc-percentile |
  |---|---|---|
  | Performer | **faded** | **0.999** |
  | Mamba | winner | 0.951 |
  | Sparse Transformer | faded | 0.605 |
  | Longformer | **winner** | **0.155** |
  | Reformer | faded | 0.068 |
  | FNet | faded | 0.038 |
  | Linformer | faded | 0.005 |
  | Nyströmformer | faded | 0.002 |

  The **top-ranked method is a faded one (Performer, 0.999)**; one winner
  (Longformer) ranks **6th of 8**. `winner-mean(0.00148) > faded-mean(0.00113)`
  is **True but is a one-point artifact driven by Mamba** — exactly the Run-37
  fake-mean-inversion. By the per-item distribution it **does not separate
  winners from losers**, and is rejected as a success (R14). Bottleneck-framing
  flags the hot *area*, not the winning *niche* → it does not fix Failure 1.

## Failure 3 re-tested at 5× scale: CONFIRMED structural
Static signals (generality × centrality) on all 43 niches vs 20,000 random
merges: niche **median gxc-percentile = 0.221** (the median real niche scores
*below* 78% of random merges); **27/43 (63%) score below the random median**;
niche median `0.00102` < random mean `0.00133`. Five times more ground truth,
same result — **real niches do not rank above random** on any static signal.

## The survivorship barrier (why this can't be validated, let alone solved)
To *predict* (not recall) you must separate eventual-winners from
eventual-losers **at proposal time**. The loser class — plausible combos that
were tried and didn't pan out — is largely **unobservable** (failures aren't
published). The one place losers ARE observable (the 6 faded efficiency
competitors) is exactly where every signal failed to separate them from the
winners. So the predictive information is not just missing from the signals
tested — the **validation data needed to learn it is structurally unavailable**.

## VERDICT — failures 1 and 3 are PROVABLY STRUCTURAL (for available data)
| | Run 36/37 | **Run 38** |
|---|---|---|
| GT size | 8 | **43** (verified) |
| static signal vs random | fails | **fails at 5× scale** (median niche = 22nd pct) |
| temporal/momentum | untried | **infeasible to measure** (no historical counts; in-bank dates wrong) |
| bottleneck precision | untried | **~0** (84% recall, can't pick winner from 8 competitors) |
| winner-vs-loser (real outcomes) | untried | **no signal separates** (top is a faded method) |

This is no longer "not yet cracked." Across static structure (Run 37) **and**
the two new dynamic angles, **no measurable pre-emergence signal ranks real
niches above random, separates real winners from real losers, or gives the
niche-checker precision** — and the data required to learn such a signal
(observable losers) does not exist. What decided FlashAttention over Linformer,
or Mamba over Performer, was execution/empirics/ecosystem, not anything present
in pre-emergence concept structure or bottleneck-framing.

**Production-ready niche *prediction* is not reachable by this method on this
data.** The honest recommendation stands: the pipeline's real, defensible
capability is **recognition** — "has this combination already been done?"
(real run31: 18/18 variants correctly identified vs real arXiv, 0 hallucinated
citations) — not prediction of niches before they emerge.
