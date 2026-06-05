# Run 35 — Inheritance & provenance notes

## Inherits Run 34 (PR #68)
Copies Run 34's engine, 314-concept bank, 119-family registry, 21 niche fixtures,
and frozen niche-audit table; starts from **direction_params v7**, evolves to
**v8** by ADDING a value stage (decision params held). run29–31 artifacts remain
absent; prior scalars inherited/labelled, not recomputed (R5).

## New artifacts (Run 35)
- `value/structural_properties.json` — 24 structural primitives + definitions.
- `value/precondition_map.json` (219 mech tokens) + `value/affordance_map.json`
  (130 problem tokens) — tagged by 6 Opus agents against the fixed vocabulary;
  **0 invalid tags, 0 missing tokens**. These are agent structural JUDGEMENTS
  (not web-sourced facts) — a controlled ontology, validated for vocabulary
  conformance and spot-checked for sense.
- `value/value_ground_truth.json` — 24 curated constructs (12 useful / 12
  useless) with structural reasons. Value labels are inherently fuzzier than
  niche labels (acknowledged in the report).
- `value/frozen_value_audit.json` — 17 borderline value verdicts from 5 real
  Opus agents (neutral inputs, no label leak), **frozen** for determinism. R3:
  all agent scratch in non-git `/tmp/run35_scratch`.

## Determinism
The value scorer reads the frozen ontology + frozen value-audit table, so it is
byte-deterministic; the LLM is consulted only at adjudication time.
