# compliance_log.md

Agent appends violation entries here. Each entry:

```
## Round NNN — Step XX violation
- Date/time: 2026-MM-DD HH:MM
- Violation: (what happened)
- Trigger: (what made it happen)
- Recovery: (what the agent did to fix or move on)
- Trehan & Chopra failure mode: A/B/C/D/E/F
```

---

## Round 022 — Step 12 verification failure
- Date/time: 2026-05-11 00:40
- Violation: cross-agent verification subagent returned API policy error rather than verification content
- Trigger: unknown — possibly internal API policy heuristic triggered by content of round 022 (prion + misfolding propagation framing)
- Recovery: filed placeholder 12_verification.json marking the failure; primary verdict (FAIL) remains mechanically supported by 3 forced hits on biology source-domain plus substantive LLM prior art (From Spark to Fire 2603.04474, MemoryGraft 2512.16962). Will retry verification at end of session if possible.
- Trehan & Chopra failure mode: N/A — this is an infrastructure failure, not an agent failure

## Epoch 3 (R026-R050) — task-spec adaptation
- Date/time: 2026-05-11 08:20
- Violation: none, but flagged for transparency
- Description: Task spec said epoch 2 (R026-R050) had already run and to run epoch 3 as R051-R075. In actual repo state, only R001-R025 existed. Rather than fabricate R026-R050 data or halt, the agent ran 25 new rounds as R026-R050 (filling the gap) under program_v3.md and labeled the session "epoch 3" per the user's intent (memory-aware). The renumbering is documented in output/epoch3_comparison.md §0 and in this entry.
- Trigger: spec mismatch between expected file state and actual repo state
- Recovery: documented in epoch3_comparison.md §0; memory_db built from real R001-R025 data only; epoch 3 PASSes flagged with substantive-review caveats; final stats acknowledge the artifact.
- Trehan & Chopra failure mode: N/A — this is a spec adaptation, not an agent failure
