# Run 7 vs Run 8 — community saturation check + Belinda 3Q audit enforced

## 1. Pipeline diff

|        | Run 7 | Run 8 |
|--------|-------|-------|
| Layer 1: snippet_decomposer | ✓ | ✓ |
| Layer 2: atom_typer + quality filter v2 | ✓ | ✓ |
| Layer 3: analogy_engine + semantic_coherence_check | ✓ | ✓ |
| Layer 4: Belinda self_model_audit (mechanical) | informal | **explicit gate** |
| Layer 5: first_principles_stress + arXiv citation gate | ✓ | ✓ |
| Layer 6: market_verifier_v2 (speaker self-publish cache) | n/a in repo | **honestly reported as unavailable** |
| Layer 7: community_saturation_check | n/a | **NEW** |

Layer 6 disclosure: `market_verifier_v2` with the "Run 3 speaker self-publish cache"
is referenced in the Run 8 spec but does not exist in this repo (only
`market_verifier.py`, the Run 6 module). Rather than fabricate a synthesized
verdict, Run 8 reports `MARKET_UNCHECKED` for every candidate. This makes
Layer 6 a no-op pass-through in this run.

## 2. Atom-pair counts (layers 1-3 are deterministic, so Run 8 == Run 7)

| Metric | Run 7 | Run 8 |
|---|---|---|
| Atoms input | 734 | 734 |
| Atoms kept (quality filter v2) | 342 | 342 |
| Candidates brainstormed | 56 | 56 |
| Candidates passing semantic coherence | 9 | 9 |
| Candidates passing arXiv gate | 7 | 7 |
| Candidates passing Belinda mechanical 3Q | (not explicitly gated) | **7** |
| Candidates passing market_verifier | — | 7 (UNCHECKED) |
| Candidates passing community_saturation (new) | — | **6** |

Same 7 atom-pair fingerprints reach the arXiv gate in both runs (CAND IDs
differ only in run-ID prefix: `CAND_run_007_005` ≡ `CAND_run_008_005` etc.).

## 3. Phase 2 retrospective audit on Run 7's 7 survivors

Real WebSearch × 7 issued. Per-candidate Belinda 3Q audit and saturation:

| Run 7 survivor | Belinda 3Q | arXiv hits (24-month window) | Saturation |
|---|---|---|---|
| CAND_run_007_005 | PASS | 2 / 5 | UNSATURATED |
| CAND_run_007_011 | PASS | 2 / 2 | UNSATURATED |
| CAND_run_007_012 | PASS | 0 / 3 | UNSATURATED |
| CAND_run_007_026 | PASS | 2 / 4 | UNSATURATED |
| CAND_run_007_029 | PASS | 3 / 3 | UNSATURATED |
| CAND_run_007_048 | PASS | 4 / 4 | UNSATURATED |
| CAND_run_007_051 | PASS | 5 / 5 | **SATURATED** |

- Belinda mechanical 3Q audit: **7/7 PASS.** Every Q3 verbatim quote
  literally appears at the cited transcript line span (mechanical re-read
  confirmed).
- Saturation distribution: **1/7 SATURATED**, **6/7 UNSATURATED**.
- **Run 8's hypothesis (6+/7 SATURATED) is NOT confirmed at the
  mechanical threshold.**

## 4. Run 8 final survivor count

Six candidates survive all seven layers:

| Run 8 survivor | Atom A | Atom B | Operator | Saturation arXiv hits |
|---|---|---|---|---|
| CAND_run_008_005 | ATOM_T012_S003_PRE_01 | ATOM_T007_S009_FIR_01 | PREDICTION_GROUNDED_IN_PRINCIPLE | 2 |
| CAND_run_008_011 | ATOM_T002_S046_PRE_01 | ATOM_T007_S004_FIR_01 | PREDICTION_GROUNDED_IN_PRINCIPLE | 2 |
| CAND_run_008_012 | ATOM_T013_S002_PRE_01 | ATOM_T007_S009_FIR_01 | PREDICTION_GROUNDED_IN_PRINCIPLE | 0 |
| CAND_run_008_026 | ATOM_T007_S012_ANA_02 | ATOM_T001_S046_OPE_01 | ANALOGY_TRANSFERS_TO_OPEN | 2 |
| CAND_run_008_029 | ATOM_T002_S020_BLO_01 | ATOM_T007_S009_FIR_01 | BLOCKER_DISSOLVED_BY_PRINCIPLE | 3 |
| CAND_run_008_048 | ATOM_T013_S010_PRE_01 | ATOM_T002_S020_BLO_01 | PREDICTION_RESOLVES_BLOCKER | 4 |

CAND_run_008_051 (the scientific-agents candidate) was rejected by the
new community_saturation layer (5 in-window arXiv papers; threshold 5).

## 5. Per-survivor Belinda audit pass/fail rate

All 6 Run 8 survivors PASS Belinda mechanical 3Q audit.

  - Q1: every cited atom_id exists in the atoms dir.
  - Q2: every combination_operator is one of the 4 paradigm-typed combinators
    (PREDICTION_GROUNDED_IN_PRINCIPLE, ANALOGY_TRANSFERS_TO_OPEN,
    BLOCKER_DISSOLVED_BY_PRINCIPLE, PREDICTION_RESOLVES_BLOCKER), each
    valid for the typed-pair it produced.
  - Q3: for every cited atom, the verbatim_quote is found (whitespace-
    normalized) inside the transcript text at the cited line span. The
    Q3 check re-reads each transcript file and asserts the quote is a
    substring of the span — no fabrication possible.

Pass rate: **6/6 = 100%**.

## 6. Honest assessment: is the pipeline still saturation-bound?

**Short answer: probably yes, but the mechanical layer 7 under-fires.**

The Run 8 layer 7 mechanically classified 6/7 Run 7 survivors as
UNSATURATED — the literal opposite of Run 7's narrative that all 7
collided with saturated 2024-2026 community topics (TTT, RLHF, on-device
LLM inference, ML4Science).

Two diagnostics for the gap:

**(a) Keyword extraction is literal, not conceptual.** The saturation
query is built from the speaker's own verbatim phrases (the atoms'
content nouns), not from the topic-concept the atoms instantiate. For
example, CAND_005's atoms talk about "generative model … discriminate
between real data and fake data … derivatives" — which Run 7's narrative
classified as "GAN / adversarial RLHF." The literal-keyword query
returned mostly deepfake-detection papers (5 distinct arXiv IDs across
2023-2025, only 2 in the 24-month window). The actual community the
candidate sits in — "GAN-style language-model alignment" — has dozens of
2024-2026 papers, but the query never asked for that concept.

**(b) Top-10 result sampling is a strict lower bound.** Web search
returns top-10 results ranked by relevance, not by recency. For a topic
with 200 recent papers, 7-8 of the top-10 are often foundational
pre-2024 papers that still dominate relevance. The 24-month window
strips them out and the remaining 2-3 falls below threshold 5. This
biases the verdict toward UNSATURATED on topics that are actually
heavily saturated.

**Implication.** The pipeline is plausibly still saturation-bound — the
6 Run 8 survivors all sit in obviously-frontier ML clusters (GAN-style
alignment, RL exploration plots, instruction-tuned assistant models,
self-improvement / cherry-picked sampling, test-time training on long
context, on-device batched LLM inference). What Run 8 *did* demonstrate
is that the community_saturation layer is **not vacuous**: CAND_051
(scientific agents) crossed the mechanical threshold and was rejected.
A topic that already saturates the *top-10 search results* in 24 months
is saturated by any reasonable definition.

**What would actually escape saturation.** Two changes are needed (out
of scope for Run 8):

  1. Concept-level query expansion. Map the atom's verbatim phrasing to
     2-3 canonical topic names (e.g., "discriminate real fake derivatives"
     → "generative adversarial network", "GAN", "adversarial training")
     before searching. This was deliberately not done in Run 8 because
     it requires either a static keyword table (won't generalize) or an
     LLM expansion step (would inflate the saturation count and game the
     gate). Both are worth trying, but they change the artifact's
     epistemic status.
  2. Corpus shift. The 13-transcript corpus is all frontier-ML speakers
     (Karpathy, Hinton, LeCun, Naval-the-startup-podcast, plus 5 academic
     ML talks). Cross-combinations of their atoms cannot escape the
     frontier-ML community by combinatorial construction. The
     near-saturation finding is consistent with the Run 7 hypothesis.
     Escaping saturation would require a corpus expansion to non-ML
     domains (neuroscience, economics, philosophy of mind), which makes
     the analogy_engine's "cross-leader semantic coherence" check
     materially harder.

**Verdict on Run 8 as an experiment.** The community_saturation layer
is implemented, mechanically functional, and not a no-op (it rejected
1/7 candidates). But its rejection rate is bounded below by the
literal-keyword-on-top-10 sampling bias. The "saturation-bound" claim
is neither confirmed nor refuted by Run 8's mechanical layer — both
runs produce 6-7 mechanism-coherent survivors that look like saturated
frontier-ML community work to an informed reader.

## 7. Artifacts

- `paradigm_shift/community_saturation_check.py` — new layer 7 module
- `paradigm_shift/belinda_audit_report.py` — Q1/Q2/Q3 detail builder
- `paradigm_shift/run_8_pipeline.py` — Run 8 driver (layers D-G)
- `paradigm_shift/runs/run_008/run_008_manifest.json` — final manifest
- `paradigm_shift/runs/run_008/phase2_retro/` — retrospective audit
- `paradigm_shift/runs/run_008/audit/CAND_run_008_*_belinda_audit.json` — per-survivor reports
- `paradigm_shift/runs/run_008/phase6_saturation_{queries,records,verdicts}.json`
- `paradigm_shift/runs/run_008/cross_llm_queue.md` — Phase 6 cross-LLM verify prompts
