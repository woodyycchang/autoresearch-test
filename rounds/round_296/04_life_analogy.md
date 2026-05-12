# R296 — life analogy

## Source: Cataglyphis desert ant path integration
- Continuously integrates DIRECTION (polarized sun compass) + DISTANCE (step counter) + LANDMARKS (visual learning) into a HOMING VECTOR maintained throughout the foraging run.
- Heterogeneous cues with explicit DOMINANCE HIERARCHY: polarization > idiothetic > landmarks under certain conditions.

## LLM analogy
**CATA-AGENT**: a long-running agent maintaining an explicit RUNNING HOMING VECTOR (current state estimate) continuously updated from three orthogonal feedback channels with a fixed dominance hierarchy:
- DIRECTION channel: alignment of recent outputs with target spec (polarization-compass).
- DISTANCE channel: number of LLM calls + tokens consumed (step counter).
- LANDMARK channel: explicit checkpoint events / tool successes (landmark anchors).
The agent maintains a single "homeward vector" estimate that integrates all three channels with documented dominance hierarchy.

## Differs from prior art (claim)
- LLM-Guided Navigation (2503.11702): map-based LLM instructions, no continuously integrated homing vector.
- FLAME (2408.11051): VLN navigation, but task-specific.
- STMR (2410.08500): semantic-topo-metric representation — closer.
- CATA-AGENT's open-question: explicit hierarchy of polarization>idiothetic>landmark integration in an LLM agent task — partially covered by VLN literature.
