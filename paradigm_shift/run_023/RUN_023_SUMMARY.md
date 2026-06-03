# Run 23 — process × RECENT (2025-2026) technique: does newer find more? A nuanced NO

## VERDICT: OPPORTUNITY_FOUND (3) — but the headline is the 2 *honest rejects*

Run 22 showed flipping the target (apply a **mature** AI technique to an under-served process)
escapes saturation (3 opportunities). Run 23 asks: do **RECENT** (2025-2026) techniques — whose
NEW capabilities (zero-shot / few-shot / label-free / sparse-sensor) mature methods lacked — find
**more or better** opportunities? Holding the process corpus ~fixed, the answer is a **nuanced NO**:
recent/fancier is **not** automatically better. 2 of 5 recent-technique pairings were **outclassed or
preempted by a *simpler* existing method**. The 3 survivors win *only* because the recent technique
enables a capability **no** method (simple or fancy) provides.

| pair (process × recent technique) | pen | gates [1234] | outcome |
|---|---|---|---|
| **charcoal_kiln × FNO** (sparse-sensor field recon) | 1 | **1111** | **OPPORTUNITY** |
| **indigo_vat × TSFM** (zero-shot forecasting) | 1\* | **1111** | **OPPORTUNITY** |
| **cork_harvest × VLMAD** (zero-shot anomaly) | 0 | **1111** | **OPPORTUNITY** |
| retting × HSIFM (hyperspectral FM) | 0 | 1101 | reject — **preempted by a simpler method** |
| indigo_vat × VLMAD (VLM anomaly) | 1\* | 1101 | reject — **preempted by a simpler method** |

Gates: 1 = process AI-penetration low, 2 = quarantine, 3 = application-gap real, 4 = concrete + **feasible-NOW (usable, not vaporware, honestly limited)**.
\*indigo penetration corrected 0→1 in PHASE 4 (see honesty note).

## The 2 rejects are the most important result (recent ≠ better)
- **retting × HSIFM → REJECT.** A hyperspectral *foundation model* is **outclassed**: 2025-2026 work already
  detects the retting endpoint with **4 wavelengths (480/490/600/610 nm) + PCA/PLS-DA**, drone-mountable
  (Nature *Sci. Reports* 2025 "smart farming tool to monitor degree of dew retting"; *Ind. Crops* 2026
  "spectral colour changes… smart flax dew retting monitoring"). The fancy technique solves an
  **already-solved** application with **more** hardware. Gate 3 fails.
- **indigo_vat × VLMAD → REJECT.** A 2024 LabVIEW **RGB machine-vision** system already reads the indigo vat
  by colour to time dyeing (Chiang & Lin, *J. Chinese Chem. Soc.* 2024). "Use CV to read the vat" is
  **taken**; a VLM is a fancier tool for a solved task. (This also **corrected** PHASE-2's indigo
  penetration 0→1 — PHASE 4 caught on-target prior art PHASE 2 missed.) Gate 3 fails.

## The 3 opportunities (the recent technique enables a capability NO method provides)
1. **Charcoal earth-kiln internal temperature-FIELD reconstruction via FNO** (`neuraloperator`/RecFNO).
   You cannot pack a buried mound with hundreds of probes or image its interior; a Fourier Neural Operator
   reconstructs the **full** field from **5-10 thermocouples**, resolution-invariant. Proven on adjacent
   thermal systems (composite curing, rotary kilns), never on the traditional earth kiln. **Limit (named):
   needs training data — simulated kiln physics or an instrumented kiln. Not drop-in.**
2. **Indigo-vat crash FORECASTING via a zero-shot TSFM** (Chronos-2 / TimesFM / Mamba4Cast).
   Forecasts the vat's pH/redox/temperature stream to predict a crash **before** it happens, with **no
   labeled per-vat history** — distinct from the 2024 present-state colour *monitoring*. **Limit (named):
   hardware-gated (probes must survive a hot caustic vat) + rare-event (crash) forecasting is genuinely
   uncertain.** The most speculative survivor.
3. **Cork-strip anomaly flagging via zero-shot VLM anomaly detection** (FADE / AnomalyCLIP, CLIP-based).
   Flags an about-to-split / cambium-exposing strip with **no labeled defect set** — which is why a
   supervised CNN can't be trained here. **Limit (named): cork bark is OUT-OF-DISTRIBUTION for CLIP and
   there is no labeled set even to *validate* it — a pilot, not a drop-in.** Assistive, not automation.

## R13 — HARD feasibility held (none are vaporware, but none are validated wins)
All 4 recent techniques are **usable now** (public code / pretrained checkpoints: `neuraloperator` on PyPI,
Chronos-2/TimesFM on HuggingFace, FADE/AnomalyCLIP on GitHub) — **0 vaporware**. But deployment maturity is
**tiered and disclosed**, and Gate 4 required each proposal to **name its own real limit** (5/5 did;
Opus itself wrote "Not drop-in", "hardware-gated", "Pilot-feasible"). *Usable-now ≠ field-validated.*

## Run 23 answer
**Does newer find more?** No — newer finds *different*, and only wins where it unlocks a capability the
simpler method cannot. Where a cheap mature method already solves the application (retting colour sensor,
indigo RGB vision), the recent technique is **preempted/outclassed** and correctly rejected. The durable
lesson across Runs 22-23: the opportunity is never "use the newest technique" — it is "**match a process's
open problem to the capability that uniquely removes its blocker**," whether that capability is old or new.

## Method integrity
- **Determinism:** gate hash stable across 2 runs (OK).
- **Verbatim:** 5/5 primary quotes are verified ≥30-char substrings of the process text.
- **Hallucination proxy:** every named technique resolves to a SOURCE-B entry with cited usable exemplars;
  PHASE-4 ran **independent** prior-art searches, so "unexploited" rests on real negative results — and the
  same searches **caught 2 false-opportunity claims** (the rejects) and **1 penetration error** (indigo 0→1).
- **Controlled design:** 3 processes carried verbatim from Run 22 to isolate the mature→recent variable.

## Artifacts (branch `claude/run-23`)
- `logs/processes.json`+reasoning · `techniques.json` (SOURCE B) · `penetration.json` · `technique_maturity.json` (R13)
- `logs/proposals.json`+5 `propose_*` envelopes · `verify.json` · `crosscheck.json` (penetration correction)
- `logs/reasoning_audit.json` (hard feasibility) · `logs/gate_results.json` · `opportunity_find_check.json` · this summary
- `run23_propose.py` (Opus subprocess + truncation-repair parser) · `run23_main.py`
