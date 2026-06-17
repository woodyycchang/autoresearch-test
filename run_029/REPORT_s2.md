# Run 29 — BFS First-Mover (fresh technique × all-of-life) — Session 2 Report

**Date:** 2026-06-04 · **Branch:** `claude/nifty-heisenberg-r98Jp` (PR #63)
**Strategy:** Resume from session-1 banks; BFS *new* ML subfields × *new* life domains for first-mover application gaps; grow the persistent banks; update steering params. Applied session-1's learned `direction_params` (up-weight neural-operators × physics-crafts; down-weight VLM-counting / LLM-backbones; add an app-store search to life sourcing).

---

## VERDICT (R12, R14)

> **FIRST_MOVER_OPPORTUNITY: NOT_FOUND this session.**
> **0 of 12 candidates are `GAP_OPEN`.** **11 are capability-gap `GAP_NARROW`** (a specific fresh-technique capability is unused, but the domain's broader problem — or its *industrial analog* — is already served). **1 is `GAP_NARROW`-bordering-`CLOSED`** (C7 slag/tap-hole).

**Session 2 reproduced AND sharpened the session-1 lesson.** The dominant new finding: *even in the highest-fertility region — neural operators × physics-bearing crafts — the result is capped at NARROW, because the craft's **industrial analog** already hosts the technique-family.* Bloomery↔blast-furnace thermal ML; anagama↔physics-informed-FNO tunnel-fire; lime-clamp↔rotary-kiln calcination models; artisan-quench↔PINN quench-field surrogates; glassblowing↔ViscNet/GlassNet. The artisan-scale + irregular-geometry + tacit-judgment slice is genuinely unmade — but that is a **capability-gap (NARROW)**, not virgin ground (OPEN).

---

## Cumulative bank sizes (R10)

| Bank | Session 1 | + Session 2 | **Cumulative total** |
|---|---|---|---|
| `tech_bank` (Axis A techniques) | 36 | **+26** (0 rejected; all in-window 2512–2606; no dup IDs) | **62** |
| `life_bank` (Axis B concepts) | 58 | **+37** | **95** |
| usable-fresh techniques (Phase-2 pass) | 24 | **+14 usable** (12 vaporware) | **38 usable** |
| first-mover candidates paired | 10 | **+12** | 22 |

Banks are APPEND-only; resume via `traversed.json`. Merge was reproducible (`merge_s2.py`, freshness + dedupe enforced mechanically).

---

## Per-domain AI-penetration distribution — which NEW domains are least AI-touched (R10)

Session-2 new concepts (37): **none 13 · very-low 9 · low 8 · moderate 5 · high 2.**

| NEW domain (session 2) | penetration skew | least-touched concepts (`none`) |
|---|---|---|
| Construction / masonry / earthen | **mostly `none`** | lime/brick-burn completion, lime-mortar slaking, cob mix-by-feel |
| Pottery / kiln firing / glaze | **`none`/`very-low`** | reduction-atmosphere by flame+smell, anagama stoking rhythm |
| Blacksmithing / heat-treatment | **`none`/`very-low`** | forge-weld timing, interrupted-quench judgment |
| Textiles / dyeing / tanning | **`none`/`very-low`** | indigo-vat readiness, veg-tanning endpoint, felting completion |
| Mining / smelting / metallurgy | `none`→`low` | ore-roasting/calcination endpoint |
| Water / irrigation / aquaculture | mixed | qanat maintenance, dowsing (`none`) |
| Waste / biogas / recycling | `low`→`moderate` | (none rated `none`) |
| Meteorology / foraging | **`high` (app-saturated)** | — weather lore + mushroom-ID are `high` |

**Least AI-touched (best white-space signal):** physics-bearing crafts of *construction (lime/cob)*, *kiln firing*, *blacksmithing*, and *textile chemistry (dyeing/tanning)*. **App-store search validated:** it correctly flagged folk weather-forecasting and wild-mushroom-ID as `high` (consumer apps ship), preventing a false white-space read.

---

## NEW technique subfields: USABLE vs VAPORWARE (R10)

26 new techniques, **14 usable / 12 vaporware (no released code).** Skew by subfield:

| NEW subfield | usable / total | skew |
|---|---|---|
| Active learning / test-time adaptation / few-shot | **3 / 3** | **USABLE-rich** (CANDI, ViTTT, VISION) |
| Causal discovery / causal representation | **3 / 4** | **USABLE-rich** (HOLOGRAPH, LCMs, CausalCompass) |
| Diffusion/flow for science | 2 / 4 | mixed (MolCrystalFlow, EnFlow usable) |
| LLM-agents / RL-reasoning | 2 / 3 | mixed (ProRL, DART) |
| Neurosymbolic / symbolic regression | 1 / 2 | mixed (SymTorch usable) |
| Tabular foundation models | 1 / 3 | **vaporware-heavy** (ShapPFN only) |
| RL / world models / planning | 1 / 3 | **vaporware-heavy** |
| Bayesian DL / UQ / SBI | 1 / 4 | **vaporware-heavy** (AFINs usable) |

**Pattern:** test-time-adaptation and causal-discovery ship code; world-models, tabular-FM and Bayesian/SBI/UQ are largely "paper-only / coming-soon" in this window.

---

## GATE results (R14) — GAP_OPEN? + named GAP_NARROW capability-gaps with honest adjacency

**GAP_OPEN found: NO (0).** Every "OPEN" the pairing proposer and the adversarial verifiers proposed was overturned to NARROW by the independent main-agent crosscheck (`crosscheck_s2.json`), because each had real prior adjacency.

**Capability-gap NARROW first-movers — named, with the exact unused slice + honest adjacent prior art (best-first):**

1. **★★ SGNO (neural operator, `2602.18801`) × traditional lime/brick CLAMP-burning calcination-front completion (C2).** *Unused slice:* stable long-horizon neural-operator rollout of the whole-charge calcination front over a multi-week clamp burn from flame cues. *Adjacency (honest):* particle-scale shrinking-core calcination models + modern rotary-kiln flame monitoring (Andritz LimeFire). *Traditional clamp burning has no predictive ML* — thinnest adjacency this session.
2. **★ SGNO × traditional BLOOMERY smelting interior-state rollout (C1).** *Unused slice:* autoregressive forecast of the unobservable interior thermal/reduction-state + bloom mass from sparse surface cues. *Adjacency:* modern blast/ladle-furnace thermal-state ML; the traditional bloomery is modeled only thermodynamically/archaeologically.
3. **EnFlow (energy-guided flow-matching, `2512.22597`) × lake-pigment dye-mordant ground-state → color (C11).** *Unused slice:* generate the precipitated dye-mordant complex's ground-state structure *from recipe params (pH/mordant ratio)* mapped to color/lightfastness. *Adjacency:* quantum-chem structure→color for madder/carmine (In-silico Madder; alizarin TD-DFT) + MOFFlow flow-matching for metal-organic complexes — flanking but the intersection is unbridged. *(cross-session: new tech × session-1 domain)*
4. **AFINs (amortized posterior, `2605.26419`) × chairside socket-fit pressure-FIELD with calibrated uncertainty (C12).** *Unused slice:* one-pass amortized, uncertainty-aware posterior of the residual-limb pressure field from sparse check-socket feedback. *Adjacency:* deterministic FEA Kriging surrogate (1.6 ms) + non-amortized Bayesian soft-tissue UQ. *(cross-session)*

Other NARROW (full table below): C3 quench, C4 glassblowing [carried s1], C5 anagama, C6 kiln heat-work, C8 overtone-stem [carried s1], C9 digester foaming, C10 indigo-vat. C7 slag/tap-hole is **near-CLOSED** (iFactory digital twins already "predict slag viscosity hours ahead of tap").

---

## Per-candidate verdict (final, post-crosscheck)

| # | Technique (arXiv) | Domain | Verifier label | **Final verdict** | Decisive adjacency |
|---|---|---|---|---|---|
| C1 | SGNO `2602.18801` | Bloomery smelting | NARROW | **NARROW** ★ | blast/ladle-furnace thermal ML |
| C2 | SGNO `2602.18801` | Lime/brick clamp calcination | NARROW | **NARROW** ★★ | shrinking-core / rotary-kiln models |
| C3 | SGNO `2602.18801` | Interrupted quench core-temp | OPEN | **NARROW** | PINN full-field quench surrogate + real-time VTS |
| C4 | SGNO `2602.18801` | Glassblowing viscosity window | OPEN | **NARROW** | ViscNet/GlassNet + digital glass control `2604.00135` |
| C5 | SGNO `2602.18801` | Anagama stoking response | OPEN | **NARROW** | physics-informed FNO for tunnel-fire fields |
| C6 | SGNO `2602.18801` | Kiln heat-work integral | NARROW | **NARROW** | PINN virtual thermal sensor + tunnel-kiln twins |
| C7 | SGNO `2602.18801` | Slag / tap-hole timing | NARROW | **NARROW→CLOSED** | digital twins predict slag viscosity hrs ahead of tap |
| C8 | SAM-Audio `2512.18099` | Overtone-stem pedagogy | OPEN | **NARROW** | visualizers (VoceVista) + isolated-overtone ML dataset |
| C9 | CANDI `2604.01845` | Digester foaming early-warning | OPEN | **NARROW** | fixed-model ML foaming prediction (MDPI 2024) |
| C10 | Toto 2.0 `2605.20119` | Indigo-vat readiness | NARROW | **NARROW** | Time-FLM bioreactor TSFM |
| C11 | EnFlow `2512.22597` | Lake-pigment structure→color | NARROW | **NARROW** ★ | quantum-chem structure→color + MOFFlow |
| C12 | AFINs `2605.26419` | Socket-fit pressure field | NARROW | **NARROW** ★ | deterministic FEA Kriging + non-amortized Bayes UQ |

**Tally: GAP_OPEN 0 · GAP_NARROW 11 · near-CLOSED 1.**

---

## Fertile frontier — what `direction_params.json` (now v2) favors (R12)

- **UP-weight (reinforced HIGH):** scientific-ML / **neural operators × physics-bearing crafts** — produced the most defensible NARROW capability-gaps again. *Do not expect OPEN here.*
- **NEW MED-HIGH:** **flow-matching-for-science × material/pigment crafts** (EnFlow×lake-pigment); **amortized-posterior-with-uncertainty × deterministic-tooling clinical crafts** (AFINs×socket).
- **NEW — usable but unpaired (chase next):** **causal discovery × process-data-rich crafts** (fermentation/kiln logs); **symbolic regression (SymTorch) × distilling a master's tacit law** (e.g. temper-color→hardness) into a symbolic equation.
- **DOWN-weight:** world-models/RL, tabular-FM, Bayesian/SBI/UQ (vaporware-heavy this window); VLM-counting & backbones (carried).
- **AVOID (added):** folk weather-forecasting and wild-mushroom-ID (consumer-app-saturated); **industrial** slag/tap-hole control (near-CLOSED).
- **OPEN hypothesis (key steering update):** to find a true `GAP_OPEN`, source **physics-bearing crafts whose INDUSTRIAL ANALOG DOES NOT EXIST** — the reliable presence of an industrial analog is exactly what capped every session-2 candidate at NARROW.

---

## Determinism, hallucination & verbatim notes (R5, R6, R7, R10)

- **Hallucination audit: CLEAN.** All 7 candidate-relevant arXiv IDs title-confirmed by re-search (SGNO, SAM-Audio, CANDI, Toto 2.0, EnFlow, AFINs, + prior-art `2604.00135`). The 3 **new-this-session** candidate techniques were **README-fetched (HTTP 200)** via `raw.githubusercontent` — CANDI (`kimanki/CANDI`), EnFlow (`Rich-XGK/EnFlow`), AFINs (`joohwanko/AFINs`@master) — plus bonus confirmations MolCrystalFlow, SymTorch. One agent proactively *excluded* PackFlow after finding its repo was unrelated (anti-hallucination behaviour).
- **Logic-break (contained):** the Phase-3 pairing proposer reproduced session-1's over-excitement (6 prelim-OPEN); the adversarial verifiers cut to 5 OPEN; the **independent main-agent crosscheck overturned all 5 to NARROW**. Systematic bias: proposer + verifiers equated "exact slice unmade" with OPEN, when any prior adjacency = NARROW. **0 false WIN escaped.** Fix recorded for session 3 (verifiers: any adjacency ⇒ NARROW).
- **Determinism:** 8 sourcing + 5 verification agents + 1 Opus pairing subprocess + main-agent crosscheck, all over live web search — result *sets* not bit-reproducible; robustness from 5 reformulations/candidate + independent crosscheck. No verdict survived as OPEN.
- **Verbatim caveat (honest):** `WebFetch` and direct `arxiv.org` returned **HTTP 403** (agent sandboxes *and* main agent). `verbatim_quote` values are "as seen in WebSearch result blocks", not hand-verified against live arXiv pages. Code-usability was hardened beyond snippets for candidate techniques via README fetches.

---

## Resume point (R11) — Session 3 START HERE

1. **Do NOT re-sweep** the 16 ML subfields + 16 life domains in `traversed.json → already_swept_do_not_repeat` (s1 + s2).
2. **Chase GAP_OPEN per the new hypothesis:** source **physics-bearing crafts with NO industrial analog** (so the technique-family has no prior foothold).
3. **Pair the usable-but-unpaired s2 subfields:** causal-discovery × process-log-rich crafts; SymTorch symbolic-regression × tacit-law distillation.
4. **Apply the verifier-optimism fix** (any adjacency ⇒ NARROW; OPEN only for zero adjacency on both axes).
5. **Keep** the app-store search in life sourcing.

---

## Artifacts (all committed + pushed per batch, R1/R2)
`phase1_s2/` (tech_1–4, life_1–4 sourcing) · `merge_s2.py` · `tech_bank.json` (62) · `life_bank.json` (95) · `usable_fresh_techniques_s2.json` · `first_mover_candidates_s2.json` · `phase4_s2/` (verify_1–5) · `crosscheck_s2.json` · `reasoning_audit_s2.json` · `direction_params.json` (v2) · `traversed.json` (session 2) · `REPORT_s2.md`
