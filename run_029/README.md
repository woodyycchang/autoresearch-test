# Run 29 — BFS First-Mover: fresh ML technique × all-of-life

**Strategy (the timing edge):** BFS broadly over BOTH (a) the NEWEST ML techniques
(published last 1–6 months, arXiv 2026) AND (b) all aspects of human life
(encyclopedia breadth). Find pairings where a JUST-PUBLISHED, USABLE technique could
be the FIRST application to a real-world domain nobody has applied it to yet.
First-mover on **application**, not method-novelty.

**Why this differs from Runs 16–25:** combination of MATURE concepts saturates.
The edge here is TIMING — a technique so new it hasn't diffused, applied to a domain
so under-served no one's looked. Double-fresh = real white space.

**Lesson carried from Run 22/23:** reframing as "application" can dodge
method-novelty saturation, but you MUST verify the gap is REAL because techniques
diffuse fast (Run 22 prion→memory and Run 23 Ostwald→memory both FAILED: the
application target was already occupied). Gates R7/R13 codify this.

## Date arithmetic (this session: 2026-06-04)
arXiv IDs are `YYMM.NNNNN`. Freshness window (last 1–6 months) = **2512–2606**
(Dec 2025 – Jun 2026). Training cutoff is Jan 2026, so 2602+ papers are sourced
purely from live web search (R5: record only what is actually seen).

## Gates (all required for a FIRST_MOVER_OPPORTUNITY)
1. Technique **FRESH** — published 2512–2606, verified by date.
2. Technique **USABLE** — code/checkpoint exists NOW (not pure theory).
3. Domain **LOW-penetration** — under-served, little/no AI work.
4. Application gap **REAL** — no one has applied the technique to the domain yet
   (verified via 5 reformulated searches, R5).
5. Feasible **NOW**.

## Files (persist + resume across sessions)
- `tech_bank.json`   — APPEND: all fresh-technique candidates seen (Axis A)
- `life_bank.json`   — APPEND: all life-domain concepts seen (Axis B)
- `traversed.json`   — resume state: subfields/domains already swept
- `usable_fresh_techniques.json` — Phase 2 output (fresh + usable filter)
- `first_mover_candidates.json`  — Phase 3 output (best pairings)
- `verify.json` / `crosscheck.json` — Phase 4 gap verification
- `reasoning_audit.json` — Phase 5 audit
- `direction_params.json` — learned fertile ML×life frontier regions (+ history)
- `REPORT.md` — session report (verbatim, determinism, hallucination, verdicts)
