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
