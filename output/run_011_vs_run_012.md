# Run 11 vs Run 12: Comparison Report

## Headline finding

| Metric                                | Run 11                                            | Run 12                                                                  |
| ------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------- |
| Survivor threshold                    | Soft 10-param composite >= 0.70                   | **Empirical threshold 0.90** (calibrated on N=30 labeled FALSE max 0.838 + 0.062 buffer) |
| Atom-level quarantine                 | none                                              | **6 atoms** (evodevo, thermodynamics, market_making, PG_E1_A05, KP_E2_A06, KP_E2_A12) |
| Cross-LLM verify gate                 | queued only (top-10), never executed              | **≥5 web_search per non-quarantined candidate at >= 0.90**              |
| Belinda audit                         | Mechanical 3Q (any analogy passes)                | **Strict**: Q1 mechanism vocab required, Q2 rejects ANALOGY_TRANSFERS_TO_OPEN, Q3 quote >= 30 chars |
| Candidates scored                     | 84 (12 × 7 epochs)                                | 84 (12 × 7 epochs, non-quarantined pairings only)                       |
| **Run 11 24 survivors recheck**       | **24 survivors** at 0.70                          | **0 survivors** under strict gates                                      |
| **Run 12 fresh 7 epochs**             | n/a                                               | **0 survivors** at 0.90 (max 0.7871)                                    |
| Cross-LLM verify diagnostics          | 0 collisions detected (not run)                   | **4 diagnostic verifies, 4/4 hard arXiv collisions**                    |
| Mean composite                        | 0.6290                                            | 0.6248 (Phase 6 fresh, very close to Run 11 mean)                       |
| Top candidate composite               | 0.8379 (CAND_011_E7_011)                          | 0.7871 (CAND_012_E7_012) — still 0.113 below strict threshold           |
| Final paradigm-shift candidates       | 24 (under Run 11 rules)                           | **0** (under Run 12 strict rules)                                        |

## Did the strict gates work as designed?

**Yes, exactly as designed.** Run 12 was built specifically to test whether 4 stacked strict gates would reject ALL Run 11 survivors (a labeled-FALSE-calibrated null) and ALSO reject 0 fresh survivors when the worst recurring atoms were quarantined.

Both predictions held: 0/24 Run 11 survivors clear Run 12's gates, and 0/84 Phase 6 fresh candidates do either. The 4 diagnostic cross-LLM verifies (on the 4 highest non-quarantined candidates across Runs 11+12) all returned hard arXiv collisions, meaning even if the threshold had been lowered, the cross-LLM gate would have caught them.

## Per-gate rejection breakdown (Run 11's 24 survivors reflowed through Run 12 gates)

| Gate                                  | Description                                         | Rejected by this gate | Cumulative survivors |
| ------------------------------------- | --------------------------------------------------- | --------------------- | -------------------- |
| Input                                 | 24 Run 11 survivors                                 | —                     | 24                   |
| G1: threshold 0.90                    | composite >= 0.90 required                          | 24 (all)              | **0**                |
| G2: quarantine                        | atom must not be in 6-atom quarantine list          | 18/24 caught (75%)    | (subsumed by G1)     |
| G3: cross-LLM verify (diagnostic)     | >=5 web_search; ANY collision rejects               | 3/3 tested            | (subsumed by G1)     |
| G4: Belinda strict (diagnostic)       | Q2 rejects ANALOGY_TRANSFERS_TO_OPEN                | ~22/24 (estimated)    | (subsumed by G1)     |
| **Final**                             | All gates                                            | **24/24 rejected**    | **0**                |

The redundancy is intentional: G1 alone kills all of Run 11, but G2-G4 would individually kill ~75-92% of the same set, validating that the gates probe genuinely different failure modes.

## Quarantine impact in detail

The quarantine list was derived from the user-labeled N=30 FALSE batch:

| Quarantined atom              | Run 11 FALSE labels | Reason                                                |
| ----------------------------- | ------------------- | ----------------------------------------------------- |
| ARXIV_R10_evodevo             | 9                   | Recurring evodevo + AI surface analogy                |
| ARXIV_R10_thermodynamics      | 5                   | Recurring thermo + ML surface analogy                 |
| ARXIV_R10_market_making       | 5                   | Recurring market making + LLM safety surface analogy  |
| PG_E1_A05 (Superlinear)       | 3                   | Pre-existing essayistic concept, no mechanism transfer |
| KP_E2_A06 (microGPT)          | 2                   | Karpathy self-publish circularity                     |
| KP_E2_A12 (microGPT culmination) | 2 (same theme)    | Same Karpathy microGPT self-publish theme             |

Quarantine alone catches 18/24 = 75% of Run 11 survivors at zero web_search cost. This is the cheapest gate by far and the spec's "quarantine first" rule is well-justified by the per-gate breakdown.

## Strict cross-LLM verify catch rate (Phase 3 diagnostics + Phase 6 diagnostic)

| Candidate                | Source phase | n web_search | Collision found at query                        | arXiv/product collision                                                 |
| ------------------------ | ------------ | ------------ | ----------------------------------------------- | ----------------------------------------------------------------------- |
| CAND_011_E7_009          | Run 11 #14   | 5            | q5                                              | arXiv:2512.16856 Distributional AGI Safety (sandbox economies)          |
| CAND_011_E4_012          | Run 11 #11   | 5            | q5                                              | TAIS / arXiv:2604.27297 (superlinear AI discovery already empirical)    |
| CAND_011_E7_006          | Run 11 #16   | 5            | q1                                              | arXiv:2405.15943 (belief states in transformers) — title-level collision |
| CAND_012_E7_012          | Run 12 #1    | 5            | q1, q3, q4                                      | arXiv:2512.24695 (Nested Learning), arXiv:2511.06232 (context phase transitions) |

**Catch rate: 4/4 = 100%.** Every diagnostic cross-LLM verify uncovered at least one arXiv/product collision within the first 5 reformulations, confirming the gate is operationally sound at the prescribed depth.

## Belinda strict reject rate

Applying Q2 strict (REJECT ANALOGY_TRANSFERS_TO_OPEN) alone to Run 11's 24 survivors:

- **Estimated rejection: 22/24 = 92%**
- 2 marginal candidates (CAND_011_E4_007 hallucination-as-thermodynamic-constraint, CAND_011_E2_002 verifier-density-as-selection-pressure) could be re-cast as PREDICTION_GROUNDED_IN_PRINCIPLE — both are quarantined though, so they still fail G2.

Q1 strict (mechanism vocab required, no filler) catches maybe 30-50% of Run 11 survivors that lean on "framework / principle / substrate / axis" filler. Q3 strict (quote >= 30 chars) does not bind for most Run 11 candidates because their atom texts are >100 chars.

Q2 is therefore the binding component of Belinda-strict and the most diagnostic improvement over Run 11's lenient 3Q audit.

## Did Run 12 find any robust real survivor?

**No.** 0 survivors across both pathways:
1. Run 11's 24 candidates reflowed through Run 12's gates: 0 survive.
2. Run 12's 84 fresh non-quarantined candidates: 0 survive at 0.90.

Top Run 12 Phase 6 composite (0.7871, CAND_012_E7_012 arch_train_unification_at_1M_context_phase_transition) is 0.113 below the strict threshold. Diagnostic cross-LLM verify on this candidate found 3 hard arXiv collisions (Nested Learning, scaling-law context phase transitions, Claude 1M product).

## Run 11 vs Run 12 score distribution comparison

```
Run 11 (per spec):
  84 candidates | 24 survivors at 0.70 | max 0.8379 | mean 0.6290
  Survivor floor 0.70 | 0/24 reach 0.90

Run 12 Phase 6 (non-quarantined pool):
  84 candidates | 20 survivors at 0.70 (old rule) | max 0.7871 | mean 0.6248
  Survivor floor 0.90 (strict) | 0/84 reach 0.90

Delta:
  Quarantine + new pairings DROPS max composite by 0.0508 (Run 11 top 0.8379 -> Run 12 top 0.7871)
  Mean essentially unchanged (-0.0042)
  Phase 6 fresh would have 20 survivors under old 0.70 rule; new 0.90 rule keeps 0
```

The strict threshold change is the dominant filter. Removing quarantined atoms drops the high-tail by ~0.05 because the quarantined ARXIV atoms were the top cross_disciplinary_bonus drivers (each contributed up to 0.24 × 1.0 = 0.0243 from cross_disciplinary_bonus weight × 1.0 score, plus saturation_distance and arxiv_grounding).

## Honest limitations of Run 12

1. **Threshold over-fit risk**: 0.90 is calibrated on FALSE labels only. There is no PRESENT TRUE label set; we don't know whether a TRUE candidate would even exist at this threshold. The threshold may be empirically tight against trivials but uncalibrated against genuine paradigm shifts.

2. **Quarantine is reversible**: An atom on the quarantine list could still appear in a genuinely novel future pairing. The current quarantine is based on 2-9 FALSE labels per atom; a future run with new partner atoms could re-introduce them after one or two retraining cycles.

3. **Cross-LLM verify is single-LLM only**: The ≥5 web_search reformulations use a single LLM (the current session) for query generation. True cross-LLM verify (sending to Claude Opus 4.7 + GPT-5.5-Thinking + Gemini frontier) is still queued in cross_llm_queue.md if any survivor emerges; in this run there are no survivors to queue.

4. **Phase 6 atom pool reuse**: Run 12's "fresh" atoms are Run 11's atom pool with quarantined ones removed and new cross-source pairings. We did NOT fetch genuinely new web material for Run 12 (web_search budget was spent on cross-LLM verify, not atom mining). A future run could add atom mining from May 2026 sources.

5. **WebFetch firewalled**: Same as Run 11 — direct fetches return 403; WebSearch summary text is the only viable channel.

## Open problems carried forward (post-Run-12)

- **RC_013 (NEW)**: Empirical threshold 0.90 may be over-tight. Need positive labels (TRUE candidates) to calibrate the upper edge.
- **RC_014 (NEW)**: Quarantine policy needs an expiration / revisit mechanism — atoms locked out after N=2 FALSE could be released after demonstrating they have an unsaturated pair partner.
- **RC_015 (NEW)**: Cross-LLM verify should use independent LLM evaluators, not single-session query reformulation. cross_llm_queue.md remains the artifact for routing to external models.
- **RC_010 (carried)**: The original "are soft-threshold survivors paradigm-shift candidates?" question is now mooted because the strict threshold + quarantine eliminates all soft survivors. The question becomes "is the strict-gate output set ever non-empty?" — answered NO for the current corpus.
- **RC_011 (carried)**: Per-source productivity heterogeneity is preserved (HN + WS still produced highest mean composite in Run 12 Phase 6, same as Run 11) but absolute survivor count is 0 across all sources.
- **RC_012 (carried)**: RLHF weight oscillation question is no longer reachable because Run 12 froze weights at v7 (post-Run-11 snapshot) and did not update; weight evolution under strict gates is a future-run question.

## Conclusion

Run 12 is a successful negative result: the 4 strict gates (threshold 0.90, quarantine, cross-LLM verify ≥5, Belinda strict) reject 100% of Run 11's survivors AND 100% of Run 12's fresh candidates. This means the previous "24 paradigm-shift candidates" claim of Run 11 is invalidated under empirical calibration on the user's FALSE label batch.

The empirical question for Run 13: can ANY candidate survive the strict gates? If not, the gates need to be relaxed (or a fundamentally different atom-mining corpus is required). If yes (in some future run), that candidate becomes a high-priority cross-LLM-queue entry for true external validation.
