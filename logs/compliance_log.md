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

## Round 043 — Step 05 composition rule violation
- Date/time: 2026-05-11 01:06
- Violation: v2 program §4 content_words composition rule requires ≥2 source-side terms; this round had only 1 (Byzantine).
- Trigger: candidate domain (BFT distributed systems) is single-mechanism, so naturally has only 1 source-side technical term
- Recovery: noted in 11_audit.json honestly; did NOT change content_words mid-round (motivated narrowing avoidance)
- Trehan & Chopra failure mode: implementation_drift (composition-rule application)

## Rounds 045/046/047/050 — Mechanical PASS via strict-substring artifact
- Date/time: 2026-05-11 01:17 to 01:43
- Violation: NONE — the file chain and mechanical rule were followed correctly
- Observation: strict-substring matching of content_words against title+snippet produces 0 hits when content_word phrases use a word order different from the published literature variant (e.g. 'plasticity loss' vs 'Loss of Plasticity'; 'LLM agent' vs 'LLM-guided' / 'LLM Multi-Agent'). The mechanical rule correctly returns total_hits=0 → PASS, but substantive prior art is dense.
- Recovery: cross-agent verification (step 12) successfully flags these as substantive FAIL despite mechanical agreement
- Trehan & Chopra failure mode: implementation_drift / scientific_taste — honest flagging in 11_audit and 12_verification
- This is data, not a bug: the artifact is itself an outcome of the strict-substring keyword rule and is faithful to the program's spec.


## Epoch 3 (R051-R075, program_v3.md) — appended after PR #3 conflict resolution

## Epoch 3 (R051-R075) — task-spec adaptation
- Date/time: 2026-05-11 08:20
- Violation: none, but flagged for transparency
- Description: Task spec said epoch 2 (R051-R075) had already run and to run epoch 3 as R051-R075. In actual repo state, only R001-R025 existed. Rather than fabricate R051-R075 data or halt, the agent ran 25 new rounds as R051-R075 (filling the gap) under program_v3.md and labeled the session "epoch 3" per the user's intent (memory-aware). The renumbering is documented in output/epoch3_comparison.md §0 and in this entry.
- Trigger: spec mismatch between expected file state and actual repo state
- Recovery: documented in epoch3_comparison.md §0; memory_db built from real R001-R025 data only; epoch 3 PASSes flagged with substantive-review caveats; final stats acknowledge the artifact.
- Trehan & Chopra failure mode: N/A — this is a spec adaptation, not an agent failure


## Epoch 4 (R076-R100, program_v4.md) — compliance summary

- Step 06.5 semantic check performed in 25/25 rounds
- Step 07 keyword rule applied unchanged in 25/25 rounds; v4 ORs semantic hit into the per-result hit flag
- Step 10 mechanical verdict applied in 25/25 rounds with total_hits = |keyword_hits ∪ semantic_hits|
- Step 12 cross-agent verification: 25/25 completed; 1 verifier disagreement on a specific result hit/miss flag (no verdict-level disagreement)
- 4 FORBIDDEN-TO-MODIFY zones (06, 07, 10, 12) preserved; only step 06.5 added between 06 and 07


## Epoch 5 (R101-R125, program_v5.md)

No compliance violations observed. All 25 rounds completed steps 01-12 with the new v5 file chain including:
- step 04.5 memory check (0 memory-skip events; all candidates from new domains)
- step 06.5 semantic-similarity check (mean max cosine 0.51; 5 rounds with semantic hits ≥0.7)
- step 06.7 LLM-judge functional-equivalence check (NEW v5; mean max judge 0.71; 20 rounds with functional hits ≥0.7)
- step 07 combined hit rule (keyword ∪ semantic ∪ functional)
- step 10 mechanical verdict (FROZEN)
- step 11 audit
- step 12 cross-agent verification (0 disagreements)

Forbidden zones unchanged: steps 06, 06.5, 07, 10, 12 all preserved verbatim from v4.

Phase 1 of this session (functional audit of R079/R085/R091/R092) was a methodological retroactive review, not a compliance violation. The audit's web searches are recorded in output/epoch4_functional_audit.md.
