# Run 29 — BFS First-Mover (fresh technique × all-of-life) — Session 1 Report

**Date:** 2026-06-04 · **Branch:** `claude/nifty-heisenberg-r98Jp`
**Strategy:** BFS both frontiers — newest ML techniques (arXiv 2512–2606) × all aspects of life — for *first-mover application* gaps (timing edge, not method novelty).

---

## VERDICT (R12, R14)

> **FIRST_MOVER_OPPORTUNITY: NOT_FOUND this session.**
> 0 of 10 candidates cleared all gates (none `GAP_OPEN`). **6 are qualified-`GAP_NARROW`** (a specific fresh-technique *capability* is unused, but the domain's broader problem is already AI-served). **4 are `GAP_CLOSED`** (already done — rejected).

The dominant, reproducible finding: **even FRESH (1–6 mo) + USABLE techniques paired with UNDER-SERVED domains tend to find the application target partially occupied** — usually by a 2023–2026 paper or a *shipping app*. This is the **Run 22/23 lesson reproduced at the timing/application layer**: novelty-by-recency does not by itself buy white space. The fertile region is the **capability-gap**, not the domain-gap.

---

## Cumulative bank sizes (R-report)

| Bank | This session | Total (cross-session) |
|---|---|---|
| `tech_bank` (Axis A techniques) | 36 | 36 |
| `life_bank` (Axis B concepts) | 58 | 58 |
| `usable_fresh_techniques` (Phase 2 pass) | 24 | 24 |
| rejected techniques (vaporware/out-of-window) | 12 | 12 |
| first-mover candidates paired | 10 | 10 |

*(Session 1 is the first of this series; totals = session. Banks are APPEND-only and resume via `traversed.json`.)*

**Breadth achieved:** 8 ML subfields × 8 life domains (meets the "8+ each" target).

---

## Gates reported explicitly (R10, R13)

| Gate | Rule | Result |
|---|---|---|
| **FRESH** | arXiv 2512–2606 (Dec 2025–Jun 2026), date-verified | 36/36 in window (agents pre-filtered; rejected stale-but-strong: Chronos-2 `2510`, Moirai-2.0 `2511`, GFM-RAG `2509`) |
| **USABLE** | code/checkpoint exists NOW (GitHub README fetched) | **24 usable**, **12 vaporware** (code-on-request) |
| **LOW-penetration** | domain under-served (none/very-low) | 42/58 concepts none/very-low |
| **GAP REAL** | no prior application (5 reformulated searches each) | **0 open**, 6 narrow, 4 closed |
| **FEASIBLE NOW** | buildable with released code | survivors yes; bottleneck is sensor→target calibration data |

---

## Fresh techniques: USABLE vs VAPORWARE (R10)

**24 USABLE (fresh + code verified)** — e.g. Mamba-3 `2603.15569`, Gated DeltaNet-2 `2605.22791`, Parallax `2605.29157`, MiniCPM-SALA `2602.11761`, Reverso `2602.17634`, Toto 2.0 `2605.20119`, VETime `2602.16681`, Flow2GAN `2512.23278`, SGNO `2602.18801`, Lance `2605.18678`, Bernini `2605.22344`, E3RelaxH2 `2603.23941`, GREPO `2602.13921`, Molmo2 `2601.10611`, InternVL-U `2603.09877`, VLA Foundry `2604.19728`, SIGMA-PPG `2601.21031`, PulseLM `2603.03331`, SAM-Audio `2512.18099`, Woosh `2604.01929`, Audio-Omni `2604.10708`, Sparse-BitNet `2603.05168`, Persistent-Q4-KV `2603.04428`, EEG-DLite `2512.12210`.

**12 VAPORWARE (fresh but NO usable code — rejected, R13)** — TimeRadar `2602.19068`, MeanVoiceFlow `2602.18104`, FLAC `2603.19176`, UNISON `2605.31530`, OGPP `2605.02222`, Cellular Sheaf NO `2606.00937`, LSD `2606.02455`, GIST `2603.16849`, SCNO `2604.11625`, Tensor-Channel-Equivariant-GNN `2605.16891`, GraphBFF `2602.04768`, Health-Conditioned-VLA `2605.16056`. **Pattern: the neural-operator / graph-foundation-model subfields are mostly "code-on-request"** — fresh on paper, not yet usable.

---

## Life domains least AI-touched (Axis B)

`ai_penetration` distribution over 58 concepts: **none 10, very-low 32, low 15, moderate 1.**
Lowest-touch concepts the sourcing agents surfaced (penetration = *none*): dry-cured ham *cala* smell test, dry stone walling, seed-saving roguing, Polynesian / Inuit / Tuareg wayfinding, stained-glass antique matching, lake-pigment making, marionette manipulation, gift-economy reciprocity.

**Caveat (learned):** a low Wikipedia-based penetration rating is *not* a reliable white-space signal — several "under-served" domains turned out to have **shipping consumer apps** (varroa counting, watch timegrapher) the life-sourcing missed. Next session adds an app-store search to the penetration read.

---

## The 10 first-mover candidates — gates & per-candidate verdict (R14)

| # | Fresh technique (date) | Under-served domain | Cap-match | **Gap verdict** | Killer prior art / note |
|---|---|---|---|---|---|
| 0 | Molmo2 (2026-01) | Varroa mite counting | strong | **CLOSED** ✗ | VarroDetector (YOLOv11, R²=0.98, MDPI 2025) + Apizoom/BeeScanning apps |
| 1 | SAM-Audio (2025-12) | Throat-singing overtone isolation | strong | **NARROW** | Spectrogram visualizers exist (Sygyt, Overtone Analyzer); *learned stem-separation* unused |
| 2 | Reverso (2026-02) | Cheese affinage forecasting | medium | **NARROW** | CV cheese-ripeness + ML volatile models exist; *tiny-zero-shot-TSFM per-wheel* unused |
| 3 | VETime (2026-02) | Watch timegrapher regulation | medium | **CLOSED** ✗ | `timegrapher.ai` ships mic→AI rate/beat/escapement diagnosis |
| 4 | InternVL-U (2026-03) | Painting conservation inpainting | medium | **CLOSED** ✗ | MIT/Kachkine reversible AI restoration (Nature, Jun 2025) |
| 5 | Toto 2.0 (2026-05) | Soy/miso moromi maturity | medium | **NARROW** | Own cited source gives objective metric; *multivariate-TS-FM forecasting* unused |
| 6 | Audio-Omni (2026-04) | Whistled-language (Silbo) transcription | medium | **CLOSED** ✗ | Jakubiak, *first* whistled-language ASR (Interspeech 2023, OpenSLR-137) |
| 7 | SGNO (2026-02) | Glassblowing reheat/viscosity | medium | **NARROW** ★ | Closest to open: only `2604.00135` (industrial DGF closed-loop control) + glass-viscosity ANN adjacent; *neural-operator forward-rollout for artisan glass* unused |
| 8 | Sparse-BitNet (2026-03) | Ethnoveterinary dosing advisor | medium | **NARROW** | Offline clinical LLM advisors exist (Farmer.Chat, Pocket RAG `2602.13229`); technique *incidental* |
| 9 | Mamba-3 (2026-03) | Polynesian wayfinding state-est. | medium | **NARROW** | Learned dead-reckoning (AI-IMU) + etak cognitive models exist; technique *incidental* |

★ = strongest qualified survivor.

**Win-condition answer (R12):** Did BFS first-mover pairing find a usable-fresh-technique × under-served-domain application *no one has done*? **No clean win.** The closest defensible qualified-first-mover is **SGNO (neural-operator PDE surrogate, `2602.18801`, Feb 2026) → real-time reheat/viscosity forecasting for artisan hot-glass working** — verified that no neural-operator/PDE-surrogate has been pointed at artisan glassblowing (only industrial laser-forming closed-loop control exists). It remains NARROW (not OPEN) because the *broad* "hold glass in the working band via thermal-camera + data-driven model" problem is occupied.

---

## Fertile frontier — what `direction_params.json` now favors (R12)

**Core steering update:** *match on CAPABILITY-GAP, not DOMAIN-GAP, and require the fresh technique to be the differentiator (not incidental).*

- **UP-weight (HIGH fertility):** Scientific-ML / **neural operators × physics-bearing crafts** (glassblowing, kiln, forge) — physics-forward-rollout rarely applied, no app market.
- **UP-weight (MED-HIGH):** **Foundation-model zero-shot transfer** (TS / audio) to low-data craft/fermentation — distinct from bespoke per-domain models.
- **MED:** learned **source-separation-into-stems** × performance-craft acoustics.
- **DOWN-weight (LOW):** **VLM counting/grounding/inpainting** (productized fast) and **generic LLM-backbones / on-device quantization as "the technique"** (incidental — don't define an application).
- **AVOID (saturated):** any niche with a hobbyist/consumer **app market** (varroa, horology, painting restoration, whistled-ASR).

---

## Determinism, hallucination & verbatim notes (R5, R6, R10)

- **Hallucination audit: CLEAN.** Main agent independently re-searched 6 surviving-technique arXiv IDs (Mamba-3 `2603.15569`, SAM-Audio `2512.18099`, Toto 2.0 `2605.20119`, SGNO `2602.18801`, prior-art `2604.00135`, Molmo2 `2601.10611`) — all resolve to real arXiv/HF/GitHub pages with matching titles. No fabrication detected.
- **Determinism / non-determinism:** sourcing + verification ran across 13 parallel agents; results depend on live web search ordering, so exact result *sets* are not bit-reproducible, but the *verdicts* were cross-checked (5 verify agents + independent main-agent crosscheck) and **no verdict was overturned**.
- **Verbatim / verifiability caveat (honest, R5/R6):** agent sandboxes had **WebFetch 403-blocked**; code-usability was directly verified via GitHub README fetches (`raw.githubusercontent.com` worked), but **`verbatim_quote` values are "as seen in WebSearch result blocks", not hand-verified against live pages.** Recorded only what was actually seen; uncertain/paraphrased sentences were dropped.
- **Logic-break:** Phase-3 (Opus pairing) exhibited **overexcitement** — 4 `why_no_one_done_it` claims ("no AI in the affinage cave", "first whistle→text pipeline", "no AI diagnostic tooling for timegraphers") were **falsified in Phase 4**. The adversarial verification + crosscheck contained them before any false WIN.

---

## Resume point (R11)

Session 1 fully executed Phases 1–5 + report. **Session 2 should:** BFS *new* ML-subfields + *new* life-domains (the 8+8 already swept are listed in `traversed.json → already_swept_do_not_repeat`); apply `direction_params.json` (up-weight neural-operators × physics-crafts, down-weight VLM-counting/LLM-backbones, add an app-store search to life-sourcing). Banks (`tech_bank`, `life_bank`) and `direction_params.history` are append-only and carry forward.

---

## Artifacts (all committed + pushed per batch, R1/R2)
`phase1/` (8 sourcing files) · `tech_bank.json` · `life_bank.json` · `usable_fresh_techniques.json` · `first_mover_candidates.json` · `phase4/` (5 verify files) · `verify.json` · `crosscheck.json` · `reasoning_audit.json` · `direction_params.json` · `traversed.json` · `REPORT.md`
