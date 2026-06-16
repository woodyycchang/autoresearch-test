# Run 33 — Inheritance & provenance notes

## Inherits Run 32 (PR #66)
Run 33 copies Run 32's engine and starts from **direction_params v5** (the
Run 32 output), then evolves to **v6**. The `run29–31` real-encyclopedia
artifacts are still **absent** from this repo (full-history search, as in
Run 32); the engine here is the reconstructed-then-evolved code, and the
prior-run scalar baselines (Run 30 = 1 false-pass, Run 31 = 0, the Run 32
results, the v1–v5 lineage) are **inherited from the prompt / PR #66** and
labelled as such — never recomputed by this run (R5).

## Concept provenance (R5, honest)
- **80 curated** concepts carried from Run 32 (`provenance: curated_run32`).
- **234 web-harvested** concepts (`provenance: websearch`). `WebFetch` is
  **403-blocked** by the network policy, so concepts were gathered with
  `WebSearch`: each concept records a **real result URL** that the harvest
  agent copied from actual WebSearch output (212 Wikipedia + ScienceDirect /
  Nature / GeeksforGeeks / libretexts / Yugabyte). This is **sourced** (real
  URLs) but **not verbatim page text** — stated plainly rather than
  fabricating quotes or URLs. Raw harvest: `harvest/harvested_concepts.json`.
- Validation after merge: **0 invalid tokens, 0 missing source URLs**, 1 dup
  dropped. Spot-checked a random sample of URLs (all real, on-topic).
- ~5 harvest agents self-corrected invalid tokens or **caught fabricated URLs
  in stale scratch** before finishing — recorded in `results/coordination.json`.

## Determinism of the audit (R3 + reproducibility)
The reasoning-audit (5 real Opus subprocesses, scratch in non-git `/tmp`)
produced a **frozen** table (`reasoning_audit/frozen_audit_table.json`). The
pipeline reads the frozen table, so `niche_check` stays byte-deterministic; the
LLM is consulted at adjudication time only, not on every run.
