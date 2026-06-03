# Run 26 — Anomaly-Driven Niche Hunting (the second path to discovery)

**Date:** 2026-06-03
**Verdict:** `ANOMALY_NICHE_NOT_FOUND` (0 of 9 anomalies clear all 4 gates)
**Scale:** 9 sourced anomalies · ~117 real WebSearches · 0 fabricated (R5) · 7-agent sequential pipeline

---

## 0. The reframe (why Run 26 is different)

Runs 16-25 mined niches by **combination** (fuse two concepts → propose a mechanism). That space is
**saturated** (Run 25: 0/98 clear gates). Run 26 takes physics's *other* discovery path — **anomaly
hunting**. Vera Rubin didn't combine concepts; she *measured* galaxy rotation, found it **contradicted**
the Newtonian prediction, and that unexplained discrepancy → dark matter. The hypothesis: a place where a
simple ML **measurement disagrees with established theory**, still **unresolved**, is novel *by
definition* (no one has explained it) and should escape combination-saturation.

## 1. Pipeline & gates

7 sequential agents: **(1)** source reported anomalies → **(2)** resolution-status → **(3, opus)** propose
explanatory mechanisms → **(4)** verify anomaly-real + mechanism-collision + independent crosscheck →
**(5)** audit. Gates: **G1** anomaly REAL · **G2** quarantine · **G3** UNRESOLVED (no *accepted*
explanation, R13-strict) · **G4** proposed explanation CONCRETE + TESTABLE + *novel*.

## 2. THE KEY DATA — 9 anomalies, gate by gate (R10)

| id | anomaly | G1 real | G3 status | G3 pass | G4 mechanism | clears all |
|----|---------|---------|-----------|---------|--------------|-----------|
| ANOM_01 | Grokking (delayed generalization) | ✓ | RESOLVED (weight-decay circuit competition) | ✗ | — | **no** |
| ANOM_02 | Deep double descent (more data hurts) | ✓ | RESOLVED (variance decomposition) | ✗ | — | **no** |
| ANOM_03 | Emergent abilities (sharp thresholds) | ✓ | **CONTESTED** (mirage vs real) | ✓ | de-superposition SNR → **already proposed** (2312.11560 / 2512.13568) | **no (G4)** |
| ANOM_04 | Sharp minima generalize | ✓ | RESOLVED (reparam-invariant flatness) | ✗ | — | **no** |
| ANOM_05 | Adam LR "surge" vs batch size | ✓ | RESOLVED (self-resolving paper) | ✗ | — | **no** |
| ANOM_06 | Reversal curse (A is B ↛ B is A) | ✓ | RESOLVED (unidirectional AR objective) | ✗ | role-gated keys → **already proposed** (2504.01928) | **no** |
| ANOM_07 | Inverse scaling (bigger = worse) | ✓ | RESOLVED (objective/data flaws + U-shape) | ✗ | — | **no** |
| ANOM_08 | LLMs know more than they show | ✓ | **CONTESTED** (truth vs knowledge-recall) | ✓ | frequency-prior override → **already proposed** (2502.16143 / 2504.12585) | **no (G4)** |
| ANOM_09 | RLHF degrades calibration | ✓ | RESOLVED (mode collapse / sharpening) | ✗ | — | **no** |

### Distribution
```
Anomalies sourced .................... 9   (all measurement != prediction, verbatim R5)
Gate 1 — empirically REAL ............ 9/9  (independently reconfirmed, replicated)
Gate 3 — UNRESOLVED (R13-strict) ..... 2/9  (ANOM_03, ANOM_08 — both CONTESTED, no consensus)
                                       7/9 RESOLVED (accepted explanation exists despite fame)
Gate 4 — novel testable mechanism .... 0/5  (all 5 proposed mechanisms ALREADY PROPOSED; forced-hits 6-9)
Survivors clearing all 4 gates ....... 0
Real WebSearches ..................... ~117 (34 source + 18 status + 9 propose + 45 verify/xcheck + 11 audit)
Fabricated results ................... 0
```

## 3. The key analysis — did anomaly-hunting escape combination saturation?

**No — and the reason is illuminating.** Anomaly hunting hit the *same* wall as combination mining, but
via a different mechanism:

- **Combination mining** saturates because the **concept-fusion space** is densely explored (Run 24/25:
  every obscure-mechanism→LLM analogy already has a functional twin).
- **Anomaly hunting** saturates because **famous anomalies attract a dense thicket of explanation
  attempts**. An anomaly becomes famous *precisely by* being studied — so by the time it is searchable, its
  **explanation space is already crowded**. 7/9 have an *accepted* explanation (fail G3); the 2 genuinely
  contested ones (emergent abilities, LLMs-know-more) have so many *competing* proposals that any new
  mechanism collides (fail G4).

**The Vera-Rubin signature requires three conjuncts** — *real* ∧ *unexplained* ∧ *no-mechanism-yet-proposed*.
Famous ML anomalies satisfy "real" but fail "unexplained" (7/9) or "no-mechanism-proposed" (the other 2).
A true anomaly niche would have to be a **freshly-reported, narrow, not-yet-famous discrepancy** — which is
structurally hard to surface by search, *because* search ranks the famous. This is the honest limit of
search-based anomaly hunting.

## 4. Honest assessment (R13/R14)

- **No lead was explained away.** The audit checked loudly in both directions: a niche would need a
  novel+testable mechanism on a Gate-3-*passing* anomaly. The 2 passers (ANOM_03, ANOM_08) have robustly
  pre-existing mechanisms; the 2 candidates with a sliver of residual novelty (ANOM_01 0.6, ANOM_06 0.55)
  attach to *RESOLVED* anomalies, so they fail Gate 3 regardless. No wrongly-killed niche.
- **The closest things to leads** are the 2 contested anomalies themselves — genuine open scientific
  standoffs worth following — but they are *open problems with crowded explanation spaces*, not niches:
  proposing a novel explanation collides, exactly as combination candidates do.
- **Testability:** both ANOM_03 and ANOM_08 proposed predictions ARE concrete + falsifiable (measurable
  order parameter + causal intervention) — moot for niche purposes since both mechanisms collide.

## 5. Rigor (R7) — determinism, hallucination, grounded-gap

- **Hallucination:** all 6 audited collision anchors confirmed REAL + functionally matching (2502.16143,
  2305.14552, 2312.11560, 2504.01928, 2309.02390, 2305.14689). The audit independently surfaced a
  *stronger* ANOM_08 collision (2504.12585). **Zero hallucinated citations.** Future-dated 2026 arXiv IDs
  were used only corroboratively; no gate decision rests on one.
- **Determinism:** G4 collisions are mechanically forced (≥2 content-word overlap, forced-hits 6-9). G3
  status independently reproduced by Phase-2 and Phase-4-crosscheck (full agreement).
- **Grounded-gap:** mechanism-collision used ML-native reformulations of each proposed mechanism, not the
  anomaly name — so "already proposed" is a functional match, not a keyword artifact.

## 6. Honest deviations
Phase-3 "claude -p --model opus" realized via the native Agent tool (independent Opus context, R3 intent);
sequential agents, each committed+pushed by main on completion (R1/R2 intent; push-race avoidance); WebFetch
403-firewalled, all evidence via real WebSearch.

## 7. One-line conclusion

> Reframing from combination to **anomaly hunting** (Vera-Rubin's path) sourced **9 real ML anomalies**, but
> **7/9 are already explained** and the **2 genuinely contested** ones (emergent abilities, LLMs-know-more)
> have **crowded explanation spaces** where every proposed mechanism collides — **0/9 clear all 4 gates**.
> Anomaly-hunting does **not** escape saturation: *famous anomalies attract explanations*, so the
> explanation space is as saturated as the combination space. A real anomaly niche would require a
> *freshly-reported, not-yet-famous* discrepancy — structurally hard to find by search. `ANOMALY_NICHE_NOT_FOUND`.
