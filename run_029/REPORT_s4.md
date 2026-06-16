# Run 29 — Session 4 Report (Path B: pivot to modern non-craft domains; the R16 structural test)

**Date:** 2026-06-04 · **Branch:** `claude/nifty-heisenberg-r98Jp` (PR #63)
**Mission:** Abandon the (exhausted) craft axis; BFS **modern non-craft domains** (markets, clinical, instruments, legal, sports, logistics, education, infrastructure, dispatch, public-health). Test **R16**: is the "usable⟹has-sibling" NARROW ceiling **craft-specific or structural to BFS itself**?

---

## VERDICT (R12, R14, R16)

> **The pivot FAILED to escape the ceiling. 0 of 12 candidates `GAP_OPEN`; 8 `GAP_NARROW`, 4 `GAP_CLOSED`.**
> **R16 ANSWERED: the NARROW ceiling is STRUCTURAL to the BFS-first-mover method, NOT craft-specific.** Modern domains not only ceiling — they collide **harder** (4 CLOSED vs 0–1 in the craft sessions), because they carry research funding + commercial vendors and have **zero** none-penetration niches.

**The structural dilemma (the real finding of Run 29, now confirmed on a 2nd axis):**
- A **usable** fresh technique is *by definition* already demonstrated on ≥1 domain → it has a **sibling foothold** → any new application is capability-gap **NARROW**, never method-OPEN.
- A technique with **no sibling** (a genuine first-of-kind) is, in a 1–6 mo window, **vaporware** (no code) → fails R13 usability.
- `usable ⟹ has-sibling` and `no-sibling ⟹ vaporware` are mutually exclusive ⇒ `GAP_OPEN` (usable **and** no-sibling) is structurally near-empty.
- The life-axis cannot rescue it: **low-AI regions (crafts)** collide via the technique-sibling; **high-AI regions (modern institutions)** collide via the application-already-built (often a deployed vendor ⇒ CLOSED). **4 sessions, 46 candidates, 0 `GAP_OPEN`.**

---

## Cumulative banks (R10)

| Bank | S1 | S2 | S3 | S4 | **Cumulative** |
|---|---|---|---|---|---|
| `tech_bank` | 36 | 62 | 86 | **+19 → 105** | **105** |
| `life_bank` | 58 | 95 | 137 | **+55 → 192** | **192** |
| candidates | 10 | 12 | 12 | 12 | **46** |
| **`GAP_OPEN`** | 0 | 0 | 0 | **0** | **0** |
| `GAP_NARROW` | 6 | 11 | 12 | 8 | **37** |
| `GAP_CLOSED` | 4 | ~1 | ~2 | **4** | **~9** |

---

## Did NON-CRAFT modern domains yield `GAP_OPEN`? (the pivot test) — **No.**

The penetration distribution alone foreshadowed it — **modern domains have zero none-penetration niches:**

| Axis swept | none | very-low | low | mod | high |
|---|---|---|---|---|---|
| crafts w/ analog (s2) | 13 | 9 | 8 | 5 | 2 |
| crafts no-analog (s3) | 14 | 11 | 11 | 5 | 1 |
| **modern non-craft (s4)** | **0** | 9 | 23 | 21 | 4 |

Every modern niche already has *some* AI. The lone borderline-OPEN candidate the proposer found — **Internalized-Reasoning × sequencing-run QC judgment** — was killed on independent crosscheck by **seqQscorer** (Genome Biology 2021, open-source ML that predicts whether NGS data passes/fails QC, explicitly replacing manual expert QC). → NARROW.

---

## Is the NARROW ceiling craft-specific or universal? (R16) — **Universal / structural.**

Modern domains collided via two mechanisms, often both:
- **Application already built (⇒ CLOSED, 4 cases):** clinical handoff salience (RoBERTa saliency model PMC11615705 + DAX Copilot in Epic); SAR mission tasking (RL-with-Lost-Person-Model `2405.12800` + SAROPS); reconciliation-break root-cause (SmartStream TLM Affinity + Duco ML); EMD over-triage (Corti **live on Copenhagen 112**, EENA-backed).
- **Technique-family sibling (⇒ NARROW, 8 cases):** every usable technique (computer-use agents, graph-RAG, tabular-FM, Koopman, CANDI, Molmo2) is deployed elsewhere.

A new wrinkle modern domains add: several low-AI niches stay manual **deliberately** (safety/legal/relational), e.g. **IPO bookbuilding allocation** — VERIFY-5 found *no* ML for the allocation decision (application axis empty!) but it's NARROW because tabular-FMs-in-finance is a sibling **and** the decision is intentionally human/regulated. A poor build target despite the empty application.

---

## Per-candidate verdict (final, post-crosscheck)

| # | Technique (arXiv) | Modern niche | **Verdict** | Adjacency |
|---|---|---|---|---|
| C1 | Internalized-Reasoning `2604.02371` | Sequencing-run QC judgment | NARROW | seqQscorer NGS-QC ML + commercial MultiQC-AI |
| C2 | HOLOGRAPH `2512.24478` | Foodborne outbreak hypothesis | NARROW | public RF "Vehicle Prediction Tool" + LLM outbreak NLP |
| C3 | A-RAG `2602.03442` | Clinical handoff salience | **CLOSED** | RoBERTa saliency PMC11615705 + DAX Copilot |
| C4 | ShapPFN `2603.29946` | Youth talent projection | NARROW | NFL Next Gen draft models + relative-age correction |
| C5 | Dreamer-CDP `2603.07083` | SAR mission tasking | **CLOSED** | RL-Lost-Person-Model `2405.12800` + SAROPS |
| C6 | Molmo2 `2601.10611` | Warehouse damage adjudication | NARROW | Arvist AI / xis.ai deployed |
| C7 | CANDI `2604.01845` | Wastewater signal interpretation | NARROW | Covid-SURGE + NWSS + cross-sewershed transfer |
| C8 | LegalGraphRAG `2605.28120` | Corporate-action elective decisioning | NARROW | SmartStream/Xceptor/Broadridge AI + agentic graph-RAG |
| C9 | PMAx `2603.15351` | Reconciliation-break root-cause | **CLOSED** | SmartStream TLM Affinity + Duco + Gresham |
| C10 | kooplearn `2512.21409` | Accelerator beam tuning | NARROW | RL+BO tuning DESY/CERN/SLAC + Xopt/Badger |
| C11 | LCMs `2602.18662` | EMD acuity / over-triage | **CLOSED** | Corti live on 112 + Singapore RF cutting over-triage 15% |
| C12 | ShapPFN `2603.29946` | IPO allocation discretion | NARROW | application empty, but tabular-FM-finance sibling + deliberately-human |

**Tally: `GAP_OPEN` 0 · `GAP_NARROW` 8 · `GAP_CLOSED` 4.**

---

## Audit (R5/R6/R7/R10)

- **Hallucination: CLEAN.** 11 candidate IDs resolve (note: `2603.29946` sourced as "ShapPFN" resolves under title "Real-Time Explanations for Tabular Foundation Models" — ID real, name is the method nickname). Independent main-agent confirmation of the 3 load-bearing prior-art claims (seqQscorer, Corti-on-112, SmartStream recon ML) — all real. Agents caught false leads and honestly reported the empty C12 application axis rather than inventing prior art.
- **Logic-break:** strict-gate fix held a 2nd session — proposer produced only 1 borderline-OPEN (vs s3's 7), verifiers returned 0 OPEN. No overturning needed.
- **Data-hygiene:** LIFE-5 overwrote its own `life_5.json` mid-run; both distinct concept sets retained (deduped, provenance-tagged) — disclosed.
- **Verbatim/determinism:** WebFetch/arxiv 403 → quotes from WebSearch blocks; 8+5 agents + pairing subprocess + crosscheck over live search; the 0-OPEN/8-NARROW/4-CLOSED outcome is highly stable (4 candidates have deployed commercial products).

---

## Params v4 + Session-5 resume point (R11) — **the method is exhausted; pick a terminal path**

4 sessions across **3 distinct life-axis regions** (crafts-with-analog, crafts-no-analog, modern-institutions) → **0 `GAP_OPEN`, 37 NARROW, ~9 CLOSED.** Another BFS session (any axis) will reproduce the structural ceiling. **Do not run another search.** Session 5 should pick a terminal path:

- **(A) Write up the structural negative result as the deliverable** — quantified saturation, 46-candidate evidence, the `usable ⟺ sibling` dilemma. *This is exactly what the pipeline is designed to produce (README: useful outputs even at 0 PASS).*
- **(B) Build the single most defensible NARROW** — **SGNO neural-operator × traditional lime-clamp calcination-front** (thinnest adjacency of all 46 candidates), accepting capability-gap (not method-OPEN) as the win.
- **(C) Technique-first watch** — monitor the strongest **vaporware (no-sibling)** techniques and be first to apply when code drops; the only structurally-available route to method-OPEN, but it requires waiting.

Do **not** re-sweep the **28 ML subfields + 36 life domains** already swept (`traversed.json`).

---

## Artifacts (committed + pushed per batch, R1/R2)
`phase1_s4/` (tech_1–3, life_1–5) · `merge_s4.py` · `tech_bank.json` (105) · `life_bank.json` (192) · `usable_fresh_techniques_s4.json` · `first_mover_candidates_s4.json` · `phase4_s4/` (verify_1–5) · `crosscheck_s4.json` · `reasoning_audit_s4.json` · `direction_params.json` (v4) · `traversed.json` (session 4) · `REPORT_s4.md`
