# Run 22 — encyclopedia-fact AI-improvement: flipping the target escapes saturation

## VERDICT: OPPORTUNITY_FOUND (3) — the first positive result of the Run 16–22 arc

Run 21 proved saturation is *target*-determined: turning a concept INTO an AI niche collides,
because AI is the mature target. **Run 22 flips the target** — take a real-world *process* + its
inefficiency and ask whether a *current* AI technique could concretely improve it. Target = the
under-served process, not an AI research niche. **This escapes the saturation.**

| process | AI-penetration (on-target) | gates [1234] | outcome |
|---|---|---|---|
| **retting** (flax fiber) | 0 | **1111** | **OPPORTUNITY** |
| **cork harvest** (stripping) | 0 | **1111** | **OPPORTUNITY** |
| **charcoal kiln** (pyrolysis) | 1 | **1111** | **OPPORTUNITY** |
| nixtamalization | 1 | 1100 | reject (gap already filled) |
| sericulture sorting | 3* | 1100 | reject (already AI'd) |
| saffron harvest | 6 | — (not in lowest-5 proposal set / high penetration) | reject |

Gates: 1 = AI-penetration low, 2 = quarantine, 3 = application-gap real (verified), 4 = concrete+feasible.

## The 3 opportunities (concrete, feasible-on-proven-technique, no found prior art)

1. **Retting endpoint detection via NIR/SWIR hyperspectral imaging + ML regression.** Retting
   endpoint is judged by feel; over/under-retting ruins fibre. HSI+ML for material quality is
   *proven* (flaxseed damage, food quality, 90–93% acc) but **never applied to retting degree** —
   a non-destructive endpoint sensor is a natural, feasible, unexploited extension.
2. **Cork-stripping assist via acoustic-emission / vibration sensing of the cork–cambium boundary.**
   Stripping "resists automation; success depends entirely on the harvester's skill"; over-cutting
   kills the tree. Full robotic stripping has *failed repeatedly* (likely infeasible) — so the
   proposal is the **narrow assistive** version: AE-on-wood is proven (oak hygro-mechanical AE,
   crack detection), unapplied to sensing cork separation to guide the human's cut. Feasible
   *because it aids, not replaces*.
3. **Traditional charcoal-kiln pyrolysis-stage classification via a CNN smoke-plume classifier.**
   Earth kilns are watched 24/7 by smoke colour (15–25% yield). CNN smoke classification (fire/
   satellite) and rotary-kiln burning-state recognition are *proven*, but **not applied to
   traditional earth-kiln stage control** — a feasible CV monitor to end 24/7 watching and lift yield.

## Why the 2 rejects are correct (the gate discriminates)
- **nixtamalization**: low penetration, but the *exact* proposal (NIR+ML moisture/endpoint) is
  already published (Theor. Appl. Genet. 2021, SVM ρ=0.852) → Gate 3 (gap real) fails.
- **sericulture**: cocoon sorting is heavily AI'd (YOLOv5 97%, real-time ML sorter, multi-sensor
  SVM) → Gate 3 fails (already done). *(\*Its Gate-1 count of 3 understates the true high
  penetration — see honesty note; Gate 3 is the decisive filter and correctly rejects it.)*
- **saffron**: a hot robotics/CV area already (Dyno Robotics + NeRF, Robotic Saffron startup, ANN
  96–100%) — the "obvious" labor target is taken.

## R10 — the key data: AI penetration discriminates sharply
Two "obvious" labor-intensive targets (saffron, sericulture) are ALREADY heavily AI'd; the genuine
white space is in *unglamorous* processes (retting endpoint, cork-stripping assist, traditional
kiln monitoring) where the technique is proven elsewhere but nobody has made the application.

## R13 — honesty / meta-auditor mindset (NOT overselling)
These are **worth-pursuing hypotheses, not validated wins**:
- *Feasible-on-proven-technique* means the AI method works on adjacent tasks; **field deployment
  has lab-vs-field unknowns** (e.g., retting may lack a clean hyperspectral signature; cork AE may
  be confounded by wood heterogeneity; charcoal smoke colour is wind/humidity-sensitive — flagged
  in the proposals' own `could_be_wrong_if`).
- *"Unexploited"* = absence of evidence in these searches, **not proof of absence** — non-indexed /
  non-English ag-engineering literature or unpublished industry practice could exist.
- The cork opportunity is deliberately the **narrow assistive** version because full automation
  failed; claiming "automate cork stripping" would have been the dishonest, infeasible version.
- AGENT 5 feasibility audit: 5/5 proposals concrete (no "AI could help" hand-waving), 0 logic-breaks.

## R12 answer — does flipping the target escape saturation? YES.
Run 21: concept→AI-niche = 5/5 exact collisions (target saturated). Run 22: AI-technique→improve-
process = 3/5 genuine, feasible, unexploited opportunities. **The saturation was never about the
source corpus or search skill — it was that the *target* (a novel AI method/niche) is mature. Re-
aiming at real-world *application* — where a proven technique meets an under-served process — finds
genuine white space.** This resolves the whole Run 16–22 arc: the productive question is not
"invent an AI niche" but "apply an existing AI technique to a process AI hasn't reached yet."

## Traversal
Encyclopedia remains bounded; this epoch processed 6 processes. Unlike Run 21 (stop — corpus
irrelevant), here continued traversal IS productive: more low-AI-penetration processes → more
candidate application opportunities. A future epoch could mine further crafts/processes.

## Artifacts (branch `claude/run-22`)
- `logs/processes.json`+reasoning · `ai_penetration.json` (R10 counts) · `proposals.json`+envelopes
- `verify.json`+`crosscheck.json` (3 real gaps, 2 collisions) · `reasoning_audit.json` (feasibility)
- `gate_results.json` · `opportunity_find_check.json` (OPPORTUNITY_FOUND, 3) · this summary
- `run22_propose.py` / `run22_main.py`
