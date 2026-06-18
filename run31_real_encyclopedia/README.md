# Run 31 — Real-Encyclopedia Merge-Brainstorm

**Core fix vs Run 30:** Run 30 bootstrapped 297 *invented* concepts. Run 31 forbids invention — **every concept in both banks traces to a REAL searched source** (Wikipedia / arXiv) with a verbatim quote (R5/R12).

## Pipeline
- **Phase 0 — Harvest (REAL, no bootstrap):** `tech_bank.json` + `life_bank.json`, assembled from
  - 13 parallel branch-agents harvesting real Wikipedia across 12+ knowledge branches (natural science, engineering, medicine, social science, history, geography, arts, food/agriculture, religion/philosophy, games, language, earth/astro), and
  - 3 parallel technique-agents harvesting real ML/CS/math techniques from arXiv/Wikipedia, plus
  - **merged-in REAL Run 29 banks** (accumulated craft/sensory-skill life concepts + ML techniques; each carries its own source+verbatim).
- **Phase 1 — Merge:** 6 Opus agents merge maximally distant REAL concepts into triples (`merges.json`). No search.
- **Phase 2 — Deepen:** Dirac (mechanistic) + Einstein (first-principles) passes (`deepened.json`).
- **Phase 3 — Integrity check:** separate checker; search used ONLY for anti-cheating (hallucination + regurgitation), never as a novelty gate (`integrity_check.json`).
- **Phase 4 — Rank:** cognitive-distance × generativity × mechanism-concreteness (`ranked.json`).
- **Phase 5 — Niche-value check + audit:** separate strict niche-checker (`final_check.json`, `reasoning_audit.json`). **R13:** a construct that is a method-variant of an ACTIVE research area is NOT_NICHE even if the exact combination is unpublished (the M032 lesson).

## Provenance
Every bank entry has a `source` URL + `summary_verbatim`. WebFetch to wikipedia.org is blocked in this environment, so verbatim text was captured from real Wikipedia/arXiv excerpts returned by WebSearch; canonical article URLs are recorded for every concept. See `REPORT.md` for the full provenance + niche verdicts.
