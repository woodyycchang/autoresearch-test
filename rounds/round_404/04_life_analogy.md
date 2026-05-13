# Life Analogy — Bushmen San n!um trance dance external basin entry

The **San (Bushmen) n!um trance dance** (Ju/'hoan southern Africa):
- All-night dance with rhythmic singing/clapping activating "n!um" energy.
- Healer enters !kia trance state through gradually-building intensity.
- Trance entry is detected EXTERNALLY by community caregivers — the dancer cannot self-report; tremor, scream, fall to ground are the observable markers.
- Helpers (sweat-rubbers, flywhisks) sustain healer once observed as "in".

The mechanism: **basin entry detected externally, not internally** — the dancer doesn't know they have crossed; the watcher does. External observer signals entry to trance basin; community then transitions to "in-basin" care protocol.

## Analogical mapping → LLM externally-observed basin entry

- Healer ↔ target LLM sampling under self-consistency
- N!um energy build-up ↔ rising token-entropy / repetition rate during decode
- !kia trance state ↔ low-entropy basin (collapse to repetition/loop)
- External community observer ↔ separate judge agent watching output stream
- Tremor/scream marker ↔ observable behavioral markers (n-gram repetition, lexical drift, perplexity spike)

The mechanism: **NUM-TRANCE-BASIN** — an EXTERNAL judge agent observes the target LLM's output stream and signals entry into a "trance basin" (low-entropy self-loop / mode collapse) using observable markers — n-gram repetition rate, lexical diversity score, KL-drift from a reference distribution. The basin-entry signal is used as a TERMINATION signal for self-consistency sampling, distinct from internal-state probing because the judge has no access to model logits. Differs from KS-statistic stability on logits (R400), internal entropy probing, repetition penalty (decoder-level) by being EXTERNAL-only and using a SEPARATE agent.

## Note on adjacency

Closest LLM prior art:
- Agent-as-a-Judge 2508.02994 (external agent evaluation of action chains)
- LLM-as-a-Judge canonical
- Multi-Agent Debate Adaptive Stability (R400 reference; uses KS-statistic on judge votes, not on target output stream)
- Self-Consistency (decoder-level, internal sampling termination)

The "external-judge observes target output stream for basin entry" pattern is functionally close to Agent-as-a-Judge but for termination signaling rather than scoring. Expected FAIL with adjacent LLM-judge literature.
