# Run 34 — Inheritance & provenance notes

## Inherits Run 33 (PR #67)
Run 34 copies Run 33's engine, 314-concept bank, 21 fixtures, and **frozen
reasoning-audit table**, and starts from **direction_params v6**, evolving to
**v7**. The `run29–31` artifacts remain absent; the engine is the
reconstructed-then-evolved code; prior scalars (Run 30=1 fp, Run 31=0, Run 32/33
results, the v1–v6 lineage) are **inherited from the prompt / PRs #66–67** and
labelled — never recomputed (R5).

## What this cycle adds
Scales the **known-approach registry 12 → 119** real published method families
(107 web-harvested by 9 Opus agents + 12 inherited). `harvest/build_ground_truth`
appends the harvested families to the 12 inline anchors at import time.

## Provenance (R5, honest)
`WebFetch` is network-blocked, so method families were gathered with
`WebSearch`; each records a **real result URL** copied from actual WebSearch
output (`provenance: websearch`). Validation after merge: **0 invalid tokens,
0 missing URLs**. 2 agents self-corrected, including one that **caught a
fabricated URL** and replaced it with the real one it found. Raw:
`harvest/harvested_approaches.json`. R3: all harvest scratch in non-git `/tmp`.

## Audit table reuse
The borderline audit table is the **frozen** Run-33 table
(`reasoning_audit/frozen_audit_table.json`), reused (not re-invoked), and
verified to still adjudicate correctly under the 119-registry. The pipeline
stays byte-deterministic.
