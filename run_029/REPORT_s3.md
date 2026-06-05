# Run 29 — BFS First-Mover — Session 3 Report (the v2 no-industrial-analog test)

**Date:** 2026-06-04 · **Branch:** `claude/nifty-heisenberg-r98Jp` (PR #63)
**Mission:** Test the session-2 (v2) hypothesis — *physics/sensory crafts with NO industrial analog may have no prior technique-application even in a twin → genuine `GAP_OPEN`.* Sweep new ML subfields + no-analog crafts (R15: tag `has_industrial_analog`), pair, verify, audit.

---

## VERDICT (R12, R14) — does the v2 hypothesis hold?

> **v2 is REFUTED at the capability-gap level: 0 of 12 no-analog candidates reached `GAP_OPEN`. All 12 = `GAP_NARROW`.**
> **v2 is PARTIALLY VALIDATED at the correlation level: no-analog crafts collide *less* (76% sit at none/very-low AI, vs 33% for partial-analog).**

The hypothesis predicted that removing the industrial analog would open white space. It does *narrow the field* (the `has_industrial_analog` tag genuinely correlates with lower AI penetration) but it does **not** reach OPEN, because of two collision mechanisms — at least one present in every candidate:

1. **The craft already has research-stage AI.** Even esoteric no-analog crafts have been touched: kodo monkoh incense-listening → **"Smell with Genji"** (`2602.02785`, CHI 2026, a Transformer incense classifier — *main-agent independently confirmed real*); organ voicing → Ising's closed-form intonation-number law + DL voicing; flint knapping → CGAN virtual knapping; paper marbling → "Mathematical Marbling" + Navier–Stokes sims; cognac → aroma-blend interaction ML (`2312.16124`, 160k pairs).
2. **The technique-family has a sibling foothold.** Where the craft *is* genuinely zero-AI (hedgelaying, solera, nerikoh), the fresh technique-family is already demonstrated elsewhere (visuo-tactile world-models → robot dough-kneading `2208.00386`; Koopman → industrial reactors). Since a **usable** fresh technique is by definition already demonstrated on *some* domain, no (technique × craft) cell is empty on **both** axes.

**Deeper lesson (params v3): saturation is deeper than the industrial-analog axis.** The 2024–2026 craft-AI research frontier has reached even the long tail.

---

## Cumulative banks (R10)

| Bank | S1 | S2 | S3 | **Cumulative** |
|---|---|---|---|---|
| `tech_bank` | 36 | 62 | **+24 → 86** | **86** |
| `life_bank` | 58 | 95 | **+42 → 137** | **137** |
| candidates paired | 10 | 12 | 12 | **34** |
| **`GAP_OPEN` (cumulative)** | 0 | 0 | **0** | **0** |
| `GAP_NARROW` | 6 | 11 | 12 | **29** |

---

## The v2 discriminator — `has_industrial_analog` × AI-penetration (R15)

Cross-tab over the 42 session-3 concepts:

| `has_industrial_analog` | none | very-low | low | moderate | high | **% none/very-low** |
|---|---|---|---|---|---|---|
| **no** (25) | 11 | 8 | 3 | 3 | 0 | **76%** |
| **partial** (15) | 3 | 2 | 8 | 2 | 0 | 33% |
| **yes** (2) | 0 | 1 | 0 | 0 | 1 | 50% |

**→ No-analog crafts collide measurably less** (76% vs 33%). The discriminator is a real low-penetration signal — necessary-ish, but **not sufficient** for the absolute-zero that `GAP_OPEN` requires.

---

## NEW technique subfields: usable vs vaporware (R10)

24 new techniques, **only 4 usable** — the new craft-relevant subfields are very vaporware-heavy this window:

| NEW subfield | usable/total |
|---|---|
| Tactile / haptic / visuo-tactile FMs | **2/8** (OmniVTA, Sound2Hap) |
| Olfactory / chemical / e-nose ML | 1/3 (odor-strength) |
| Koopman / DMD / evolution-operator | 1/4 (kooplearn) |
| Differentiable-sim / Hamiltonian-NN | **0/5** |
| Diffusion for inverse problems / DA | 0/4-ish (paper-only surge) |
| Implicit neural fields for physics | 0–1 (thin in-window) |

The 4 usable ones (OmniVTA, Sound2Hap, odor-strength, kooplearn) drove the pairings.

---

## Per-candidate verdict (final, post-crosscheck) — all 12 NARROW

| # | Technique (arXiv) | No-analog craft | craft zero-AI? | **Verdict** | Adjacency that blocks OPEN |
|---|---|---|---|---|---|
| C1 | OmniVTA `2603.19201` | Hedgelaying pleacher-cut | **yes** | NARROW | VT-WM `2602.06001` + robotic branch-pruning `2008.11613` |
| C2 | kooplearn `2512.21409` | Solera saca-timing | **yes** | NARROW | Koopman on CSTR reactors; sherry e-nose ML |
| C3 | OmniVTA `2603.19201` | Nerikoh consistency-by-feel | **yes** | NARROW | robot dough-kneading `2208.00386`/`2107.06924` |
| C4 | odor-strength `2512.08683` | Kodo monkoh discernment | no | NARROW | **"Smell with Genji" `2602.02785`** + agarwood e-nose |
| C5 | OmniVTA `2603.19201` | Bonsai wiring | no | NARROW | robotic plant-shaping `1804.06682` + VT stiffness |
| C6 | odor-strength `2512.08683` | Cognac assembly | no | NARROW→CLOSED | aroma-blend ML `2312.16124`; Mackmyra |
| C7 | SymTorch `2602.21307` | Organ flue-pipe voicing | no | NARROW | Ising intonation-number law + DL voicing |
| C8 | OmniVTA `2603.19201` | Knapping termination control | no | NARROW | CGAN virtual knapping (Sci Reports 2021) |
| C9 | kooplearn `2512.21409` | Marbling comb-stroke | no | NARROW | "Mathematical Marbling" + NS sims |
| C10 | SymTorch `2602.21307` | Clay plasticity-by-feel | no | NARROW | symbolic-regression plasticity (R²=0.998) |
| C11 | SymTorch `2602.21307` | Free-reed tuning | no | NARROW→CLOSED | closed-form free-reed frequency formula |
| C12 | OmniVTA `2603.19201` | Knapping platform-angle | no | NARROW | CGAN + >80% platform-angle classifiers |

**Tally: `GAP_OPEN` 0 · `GAP_NARROW` 12 (2 borderline-CLOSED).**

---

## The honest application-level nuance (R12 timing-edge)

Three candidates have **genuinely ZERO prior AI on the craft itself** — independently confirmed:
- **OmniVTA × hedgelaying** (only general hedge-*trimming* robots exist; *"machines can actually harm the hedgerow"*),
- **kooplearn × solera saca-timing** (*"did not find any papers directly combining"* Koopman + solera),
- **OmniVTA × nerikoh** (no nerikoh-specific AI).

These are **application-level first-movers** (you would be first to apply *any* AI) — a real timing edge — but they are graded `GAP_NARROW`, not `GAP_OPEN`, because the fresh technique-family is already demonstrated on a sibling domain. *If* application-novelty is the accepted win type, these are the session-3 wins; if method-novel OPEN is required, none qualify.

---

## Audit (R5/R6/R7/R10) — verbatim, determinism, hallucination

- **Hallucination: CLEAN.** All 4 candidate technique IDs resolve (OmniVTA, kooplearn, SymTorch, odor-strength). The decisive v2-refuting adjacency — **"Smell with Genji" `2602.02785`** — was independently main-agent-confirmed (arXiv + ACM CHI 2026), not a verifier hallucination. Agents caught false leads (cognac "Aqua Ignis A.I." = *Artisanal* Intelligence, not ML; multiple out-of-window date-traps rejected on ID prefix).
- **Logic-break — the params-v2 fix WORKED (measurable).** Baking the strict gate ("any adjacency ⇒ NARROW") into the verifier prompts eliminated the optimism that session 2's crosscheck had to correct: **session 3 verifiers returned 0 OPEN** (vs session 2's 5 false-OPEN). The pairing proposer still over-guessed (7 prelim-OPEN), but containment moved one stage earlier.
- **Determinism:** 8 sourcing + 5 verification agents + 1 Opus pairing subprocess + main-agent crosscheck over live search; sets not bit-reproducible; the 12-NARROW outcome is highly stable (every candidate ≥1 cited adjacency).
- **Verbatim caveat:** WebFetch/`arxiv.org` were HTTP 403; `verbatim_quote`s are from WebSearch result blocks, not live-page-verified.

---

## Fertile frontier (params v3) + Session-4 resume point (R11)

**The craft axis is likely exhausted for method-OPEN: 3 sessions, 0 `GAP_OPEN`, 29 `GAP_NARROW`.** Session 4 needs a **PIVOT** — pick one:

- **(A) Accept the timing-edge win and BUILD.** Stop searching; spec/prototype one zero-craft-AI NARROW — `SGNO × lime-clamp calcination` (thinnest adjacency, s2), or `OmniVTA × hedgelaying`, or `kooplearn × solera`.
- **(B) Abandon the craft axis.** BFS an all-of-life region never swept: digital-native practices, economic/market microstructure, scientific-instrument operation, legal/bureaucratic process, sports biomechanics — where fresh techniques may have no foothold.
- **(C) Flip to technique-first.** Start from a usable fresh technique with no known application and BFS outward.

Do **not** re-sweep the 22 ML subfields + 26 life domains already done (`traversed.json → already_swept_do_not_repeat`). Keep the strict-gate verifier fix and the app-store/funded-industry checks.

---

## Artifacts (committed + pushed per batch, R1/R2)
`phase1_s3/` (tech_1–3, life_1–5) · `merge_s3.py` · `tech_bank.json` (86) · `life_bank.json` (137) · `usable_fresh_techniques_s3.json` · `first_mover_candidates_s3.json` · `phase4_s3/` (verify_1–5) · `crosscheck_s3.json` · `reasoning_audit_s3.json` · `direction_params.json` (v3) · `traversed.json` (session 3) · `REPORT_s3.md`
