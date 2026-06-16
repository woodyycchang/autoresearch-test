# PIPELINE_STATE — consolidated lineage (Task A)

This file is the single source of truth for the niche-finding pipeline after
consolidating open PRs **#63–#69** onto one branch. It records what each run is,
which version is authoritative, and — importantly — an **honest discontinuity**
between the *real* lineage and a later *reconstruction*.

## TL;DR for future runs
- **Inherit the REAL banks/engine:** `run31_real_encyclopedia/` — **791 real,
  sourced, verbatim-quoted concepts** (life 576 / tech 215) + the merge →
  integrity → strict-R13 niche-check artifacts. Do **not** rebuild banks from
  scratch.
- **Re-use the reconstruction's METHODS** (deterministic instrumentation,
  audit-gated borderline adjudication, value/plausibility scorer) from
  `run35_real_encyclopedia/` — but be aware these were measured on a **separate,
  reconstructed, partly-synthetic** engine, not on the real banks (see the
  discontinuity below).

## Inventory (open PRs #63–#69)

| PR | run dir(s) | what it is | real or reconstructed | authoritative? |
|---|---|---|---|---|
| #63 | `run_029/` | Run 29 BFS first-mover (4 sessions, 46 candidates). Honest negative: "NARROW ceiling is STRUCTURAL to BFS — 0 OPEN across 4 sessions." params v4. | **REAL** (artifact-based, real `life_bank`) | latest for run29 |
| #64 | `run30/`, `run31/` | Run 30 merge-brainstorm **engine origin**; Run 31 Track-2 POCs (`m032_*`, `m057_*`). Run 30 banks were **297 INVENTED concepts (no source)** — superseded. | **REAL** (engine origin) | run30 superseded by #65 banks |
| #65 | `run31_real_encyclopedia/` | **THE real engine.** 791 real sourced concepts; 66 merges (6 Opus agents); 18/18 integrity PASS; strict R13 niche-check → **0 IS_NICHE / 18 NOT_NICHE**; adversarial audit **11/11 SOUND, 0 overturns, 0 hallucinated citations** (every cited 2024–26 arXiv paper verified real). | **REAL** — authoritative banks/engine | **YES (real data)** |
| #66 | `run32_…/` (+33/34/35 on same branch) | Run 32 reconstruction: deterministic Python engine, 80 concepts, instrumented; v4→v5. | **RECONSTRUCTED** | superseded by #69 within its own line |
| #67 | `run33_…/` | scale to 314 web-harvested concepts; audit-gating; v5→v6. | **RECONSTRUCTED** | — |
| #68 | `run34_…/` | registry 12→119 real methods; v6→v7. | **RECONSTRUCTED** | — |
| #69 | `run35_…/` | generator-side value/plausibility scorer; v7→v8. | **RECONSTRUCTED** | latest of the reconstruction line |

## ⚠️ The discontinuity (honest)
Run 32's task said "inherit `run31_real_encyclopedia/`". In the Run 32–35
sessions **those branches (#63–#65) were never fetched into the container**, so
`git log --all` showed nothing and Run 32 **reconstructed a parallel engine from
the spec in its prompt** rather than loading the real one. Consequences:
- run32–35 use a **different, smaller, partly-synthetic** concept set (80 → 314
  curated/web-harvested), **not** the real 791 sourced banks.
- The traps `M032` (incremental-variant), `M005` (SAFE-variant), etc. in run32–35
  are **synthetic fixtures that re-use the real names** but are **not** the real
  run31 constructs (real M005 = a SAFE/reward-velocity variant vs a real arXiv
  paper; real M016 = MoSE variant; etc.).
- Therefore run32–35's "0 false-pass / convergence / production-ready" results
  are real measurements **on the reconstructed engine**, not on the real banks.
  They demonstrate the *method* (instrumentation, determinism, audit-gating,
  value scoring); they do **not** validate the real run31 banks.

The two lineages are **parallel, not linear.** This consolidation keeps both,
clearly labelled, so a future run can do the real merge: apply the run32–35
*methods* to the real `run31_real_encyclopedia` *banks*.

## What was merged / dropped
- **Merged onto this branch:** `run_029`, `run30`, `run31`, `run31_real_encyclopedia`
  (real, from #63/#64/#65) + `run32–35_real_encyclopedia` (reconstruction, from
  #66's branch, which carries all four). All are **distinct top-level dirs — no
  file conflicts**, so this is a clean union, not a content merge.
- **Dropped / out of scope:** the older lineages still open as PRs
  (#3 epoch-3, #34 niche-mining v15, #43/#50/#52 paradigm-shift, #54–#62 run15–27)
  are **different projects** (niche-mining epochs, paradigm-shift-finder) and were
  **not** folded in — they are not part of the run29→35 real-encyclopedia pipeline.
  Nothing from the run29→35 lineage was dropped.

## Recommended next step (not done here)
"True merge" run: load `run31_real_encyclopedia/{life_bank,tech_bank}.json`
(791 real concepts) as the bank, port the run35 deterministic
merge/integrity/niche/value stages onto it, and re-measure. That would make the
optimization line actually operate on the real sourced data.
