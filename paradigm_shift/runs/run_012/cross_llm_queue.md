# Run 12 Cross-LLM Queue

## Status: EMPTY

No candidates survived Run 12's 4 strict gates (threshold 0.90, quarantine, cross-LLM verify >= 5 web_search, Belinda strict).

Both pathways produced 0 survivors:
1. **Run 11 recheck**: 0/24 Run 11 survivors clear Run 12's gates.
2. **Phase 6 fresh**: 0/84 fresh non-quarantined candidates reach threshold 0.90 (top: 0.7871, CAND_012_E7_012).

## Why no queue entries?

The spec's POST-RUN rule is: "If any survivor, generate cross_llm_queue.md for external ChatGPT/Gemini verification." Since no survivors exist, no candidate is queued for external LLM novelty verification.

## Diagnostic verifies already executed (single-session, recorded for transparency)

These are NOT external-LLM verifies — they are web_search reformulations performed during Run 12 to diagnose whether the cross-LLM verify gate would have caught the top non-quarantined candidates if they had reached threshold 0.90:

| Candidate                | Source     | n web_search | Outcome                                                                  |
| ------------------------ | ---------- | ------------ | ------------------------------------------------------------------------ |
| CAND_011_E7_009          | Run 11     | 5            | HARD_COLLISION arXiv:2512.16856 Distributional AGI Safety                |
| CAND_011_E4_012          | Run 11     | 5            | HARD_COLLISION TAIS/arXiv:2604.27297 (superlinear AI discovery)          |
| CAND_011_E7_006          | Run 11     | 5            | HARD_COLLISION arXiv:2405.15943 (belief states in transformers)          |
| CAND_012_E7_012          | Run 12 P6  | 5            | HARD_COLLISION arXiv:2512.24695 (Nested Learning) + arXiv:2511.06232     |

All 4 candidates failed the diagnostic cross-LLM verify (4/4 = 100% collision rate). None advance to formal external-LLM queue.

## If a future run produces a survivor

For Run 13+ — if any candidate ever clears all 4 strict gates, this file will be regenerated with:

```
{candidate_id, joint_topic, atoms, supporting_arxiv, predicted_paper_title}
```

formatted for direct submission to:

- **Claude Sonnet 4.6** (separate session, no shared context with the generator)
- **GPT-5.5-Thinking**
- **Gemini frontier**

Each external LLM is asked Q1 (is the joint claim genuinely novel as of submission date?), Q2 (what existing papers most closely contradict the novelty claim?), Q3 (could this be a paper worth writing or is it surface analogy?). A candidate is accepted only with >= 2/3 LLM agreement on Q1 = "yes, novel" and Q3 = "worth a paper".

## Status as of 2026-05-24

| Field                        | Value                                                                  |
| ---------------------------- | ---------------------------------------------------------------------- |
| Run 12 final survivors       | 0                                                                      |
| Queue entries                | 0                                                                      |
| Diagnostic verifies executed | 4                                                                      |
| Diagnostic collision rate    | 4/4 = 100%                                                              |
| Next action                  | Run 13 design — relax gates OR change atom-mining corpus OR add positive labels |
