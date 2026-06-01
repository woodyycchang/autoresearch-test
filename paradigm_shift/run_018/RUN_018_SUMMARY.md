# Run 18 — sentence-level decomposition from verbatim abstracts

**Method:** instead of one mechanism per paper (Run 17), decompose the **verbatim
abstract WebSearch returns** for an arXiv paper into sentence-level sub-mechanism
atoms (R9; WebFetch 403s so this IS the sourcing path), measure **per-atom
saturation**, and pair the **sparsest cross-paper sub-mechanisms** to test the key
question (R12): *at sentence granularity, does pairing sparse atoms beat the Gate-1
novelty floor that capped Runs 16–17?* Built on the proven Run 17 transparent loop
(`claude/run-18`, stacked on `claude/run-17`).

## The answer to the key question (R12): a real, measurable shift — but saturation still holds

| | Run 17 (one mechanism/paper) | Run 18 (sparsest sentence-level pairs) |
|---|---|---|
| per-candidate verifier paper-hits | **30, 34, 38** (min 30) | **18, 19, 19, 20, 23** (min **18**) |
| candidates with nonzero novelty | 0 / 3 | **3 / 5** (composites up to **0.505**) |
| Gate-1 threshold (composite ≥ 0.90) | needs ≤ 3 hits | needs ≤ 3 hits |
| survivors / verdict | 0/3 · NICHE_NOT_FOUND | 0/5 · **NICHE_NOT_FOUND** |

**Pairing the sparsest sentence-level sub-mechanisms measurably reduced prior-art
volume (~40%: min 30→18) and lifted novelty off the floor for the first time across
runs.** But the reduction is nowhere near enough: clearing Gate 1 needs ≤3 paper-hits,
and the best candidate still surfaced 18. **Every fused niche re-broadens to its
mature parent literatures** (MoE routing/collapse, Fisher-Rao information geometry,
thermodynamic computing, directional statistics). So **saturation holds at sentence
granularity — but measurably less severely than at paper granularity.** Honest answer,
reported whichever way it fell (R12).

### Why per-atom counts alone don't settle it (disclosed)
A single WebSearch returns a capped result list (~≤9), so all 11 sub-mechanisms
register below the <10 "sparse" flag; the meaningful signal is the **spread** of
distinct non-source papers per sub-mechanism — `[1, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5]` —
and, decisively, the **per-candidate 5-reformulation count** (18–23), which is the
figure directly comparable to Run 17's 30–38. The sparsest mechanism atoms were
P1_S5 *Bingham-spectrum→collapse bound* (2) and the Matrix-Bingham / Fisher-Rao /
thermodynamic-sampling clauses (3).

## Transparency mechanism (inherited from Run 17, the standing deliverable)
Every decision carries a `reasoning_trace`; AGENT 5 audited **all 63 traces**:

| | value |
|---|---|
| traces audited / complete | **63 / 63** |
| **logic-breaks** | **0** |
| decision↔data consistency checks (all agree) | **26** (incl. 11 NEW per-atom *sparsity* checks: each "sparse" label matches its recorded hit-count) |
| non-fatal flags | 29 (terse verifier-reformulation confidence + grounding-heuristic on short decisions) |
| determinism · anti-hallucination (Opus vs truth) | OK · **0 mismatches** |
| proof scorecard · offline tests | **11/11** · **9/9** |

## The 5 candidates (sparsest cross-paper mechanism pairs)
All pass Gates 2/3/4 (quarantine, verify⊕crosscheck no-collision, Belinda mechanism
verb + verbatim quote); all fail only Gate 1.

| cand | fused niche | atoms (hits) | verify hits | composite |
|---|---|---|---|---|
| 001 | Fisher-Rao annealing of router concentration vs collapse | P1_S5(2)×P2_S2(3) | 20 | 0.45 |
| 002 | Thermodynamic Bingham routers w/ collapse bounds | P1_S5(2)×P3_S1(3) | 19 | 0.4775 |
| 003 | Fisher-Rao scheduling of Grassmannian Bingham gating | P1_S2(3)×P2_S2(3) | 18 | 0.505 |
| 004 | Thermodynamic Grassmannian routing via physical Bingham sampling | P1_S2(3)×P3_S1(3) | 19 | 0.4775 |
| 005 | Fisher-Rao scheduling of continuous routing entropy | P1_S3(3)×P2_S2(3) | 23 | 0.45 |

**CAND_018_005 is the lowest-margin result:** AGENT 4 (verify + independent
crosscheck) repeatedly surfaced arXiv:2604.14500 *"Geometric Metrics for MoE
Specialization: From Fisher Information to Early Failure Detection,"* which genuinely
puts the Fisher metric on routing distributions — but for specialization *metrics /
failure detection*, not an optimal entropy *schedule*. No exact collision, but a
reviewer could call it incremental. Recorded honestly rather than hidden.

## Methodological notes (disclosed)
- **Sourcing (R9, verified):** WebSearch `"arxiv <id> <title> abstract"` returns the
  complete verbatim abstract as clean text (the search subsystem renders it, sometimes
  converting first-person → third-person); WebFetch 403s on arXiv/HF/alphaXiv. Atom
  text is recorded verbatim from these abstract renderings; titles/URLs from the Links
  arrays.
- **Mechanism-only pairing:** 2 of 11 atoms were problem-statement/gap *context*
  sentences (`is_mechanism=false`) and excluded from pairing — we pair sub-*mechanisms*.
- **AGENT 5 is rule-based by design** (an LLM auditor would reintroduce a black box);
  heuristic limits are recorded in each audit trace and account for the 29 flags.
- **Scope:** 3 papers, 11 atoms, 5 candidates, 1 epoch, Run 16's gates UNCHANGED.

## Verdict
**NICHE_NOT_FOUND (0/5)** — and the honest scientific finding: **sentence-level
decomposition does reach sparser, lower-prior-art regions (volume 30+→18, novelty off
the floor), but not sparse enough to clear Gate 1; saturation holds, less severely.**
Every one of the 63 decision points is visible, complete, and logic-audited (0 breaks).

## Artifacts (branch `claude/run-18`)
- `REASONING_TRANSPARENCY_REPORT.md` (end-to-end trace) · `sparse_analysis.json` (R10/R12 key data)
- `logs/`: `atoms.json`+`atoms_reasoning.json` (A1) · `atom_search.json` (A2, per-atom hits) ·
  `candidates.json` (A3) · `verify.json`+`verify_reasoning.json`+`crosscheck.json` (A4) ·
  `reasoning_audit.json` (A5) · `report_log.md` ([REPORT 1-6]) · `gate_results.json` ·
  `determinism_check.json` · `hallucination_check.json` · `summary_llm.md`
- `niche_find_check.json` · `proof_scorecard.json` (11/11)
- `run18_merge.py` · `run18_audit.py` · `run18_orchestrator.py` · `test_run18.py` (9 tests)
