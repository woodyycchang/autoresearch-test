# Paradigm-Shift Finder — Run 4 vs Run 5

**Author:** Claude (Opus 4.7 / `claude-opus-4-7[1m]`), branch `claude/paradigm-shift-finder-run-5-xa7Eu`.
**Date:** 2026-05-22.
**Scope:** Compares Run 5 (13-transcript corpus, cross-leader brainstorm, relaxed atom quality filter) against the prior runs.

---

## 0. Run history reality check

The Run 5 task prompt cites a corpus of "5 academic + Weijia Shi + 7 tech
leader = 13 transcripts" and "14 user labels accumulated across runs 2-4."
The on-disk state of this repository at branch start is narrower:

- `paradigm_shift/runs/run_001/` is the only previously-persisted run
  (5 academic transcripts; mechanism validation; 0 surviving candidates).
- `paradigm_shift/impact_labels.json` contains 3 labels, all of value 1
  ("trivial"), all from `run_001` (commit `6c3d54df`).
- Commit `ece58074` ("add 7 tech leaders transcript fetched locally")
  added T007..T014: Karpathy (×2 — `intro_llms`, `software_changing`),
  Sutton (`bitter_lesson` interview clip), Altman (`how_to_start_a_startup`),
  Hinton (×2 — `outsmart`, `forward_forward`), LeCun (`jepa`), Naval
  (`how_to_get_rich`).
- **No Weijia Shi transcript was committed.** The Run 5 prompt cited her
  by name, but the file does not exist in `tari/inputs/`. The
  speaker_self_publish_cache contains a forward-looking entry for her
  papers (In-Context Pretraining, REPLUG, FlexOlmo, Visual Sketchpad),
  but no Weijia Shi atoms enter the brainstorm because her transcript
  isn't in the corpus.

So the actual Run 5 corpus is **5 academic + 8 tech-leader-talk
transcripts covering 7 distinct tech leaders** (Karpathy ×2, Hinton ×2,
plus Sutton, Altman, LeCun, Naval). 13 transcripts total.

This comparison treats `run_001` as the on-disk baseline and treats the
"14 trivial labels across Runs 2-4" claim from the prompt as reported
prior context rather than verified prior data. Where the prompt asked
for "Run 4 vs Run 5", the substantive Run 4 artifact is the user's
labeling decisions (uncommitted), and we compare its **reported
outcome** (14 trivial labels suggests cross-transcript was insufficient)
against Run 5's structural changes.

---

## 1. Headline answer

**Run 5's structural changes ran end-to-end on the 13-transcript corpus.
The relaxed atom quality filter expanded usable atom yield, and the
cross-LEADER constraint did force candidates to span distinct speakers
rather than just distinct transcripts. The stress + market stages still
return 0 because no real WebSearch hook is wired in the sandbox.**

| Metric | run_001 (5 academic) | run_005 (5 academic + 8 tech-leader, cross-leader) |
|---|---|---|
| Transcripts in corpus | 5 | 13 (T001–T005, T007–T014) |
| Distinct speakers | 5 (all academic) | 11 (5 academic + 6 tech leaders) |
| Snippets total | not separately tracked | 165 across 13 transcripts |
| Paradigm atoms (pre-filter) | 264 | 579 |
| Paradigm atoms (post-filter) | n/a (no filter in Run 1) | 148 |
| TARI atoms (cross-reference) | 551 | 744 |
| Candidates | 10 | 27 |
| Candidate diversity (`transcript_diversity=2`) | 10/10 | 27/27 |
| Candidate `speaker_diversity=2` | n/a | 27/27 |
| Candidate speaker_class pair | n/a | 26 academic+tech_leader, 1 tech_leader+tech_leader |
| Audit PASS or PASS_WITH_CAVEAT | 10 / 10 | 27 / 27 |
| Self-publish hits across all atoms | n/a (no cache) | 3 / 148 (2.0%) |
| Stress survivors (PASS_STRESS) | 0 / 10 | 0 / 27 |
| Market survivors | 0 | 0 |
| Stress rejection reason | 100% FAIL_RAG_UNGROUNDED | 100% FAIL_RAG_UNGROUNDED |

**Verdict:** Run 5 satisfies CL-1, CL-2, QF-1, SP-1 from its manifest.
CL-3 is satisfied weakly (1 tech_leader+tech_leader pair, not many).
S-1 is **not met**, as expected without a real WebSearch hook —
identical to Run 1's documented limitation.

---

## 2. Per-transcript atom yield (academic vs Weijia Shi vs tech leader)

Per the quality filter's `_quality_records.json` (input counts) and
`_quality_filter.json` (kept counts):

| Transcript | Speaker | Class | Atoms extracted | Atoms kept (Run 5 filter) | Keep rate |
|---|---|---|---|---|---|
| T001 | Belinda Li | academic | 89 | 29 | 33% |
| T002 | Yu Sun | academic | 44 | 10 | 23% |
| T003 | Nicholas Roberts | academic | 67 | 35 | 52% |
| T004 | Valerie Chen | academic | 6 | 5 | 83% |
| T005 | Amrith Setlur | academic | 58 | 20 | 34% |
| T007 | Karpathy | tech_leader | 0 | 0 | n/a |
| T008 | Sutton | tech_leader | 2 | 2 | 100% |
| T009 | Altman | tech_leader | 76 | 3 | 4% |
| T010 | Hinton | tech_leader | 38 | 4 | 11% |
| T011 | LeCun | tech_leader | 56 | 15 | 27% |
| T012 | Hinton | tech_leader | 1 | 0 | 0% |
| T013 | Karpathy | tech_leader | 142 | 25 | 18% |
| T014 | Naval | tech_leader | 0 | 0 | n/a |
| **Academic subtotal** | — | — | **264** | **99** | **38%** |
| **Tech-leader subtotal** | — | — | **315** | **49** | **16%** |
| **Weijia Shi subtotal** | — | — | **n/a — transcript not in corpus** | n/a | n/a |
| **Total** | — | — | **579** | **148** | **26%** |

Three observations:

1. **T007 (Karpathy intro_llms) and T014 (Naval) produced 0 atoms even
   pre-filter.** The atom_typer regex patterns all anchor on sentence
   boundaries (`[^.!?]{N,M}[.!?]`). T007 is one continuous 63K-character
   ASR transcript with no terminal punctuation; the patterns never match.
   Same for T014 (392 lines of unpunctuated bullet text). This is a
   **decomposer/extractor failure**, not a filter failure — the
   quality_filter would have kept them had they been extracted.
2. **T012 (Hinton Forward-Forward) extracted only 1 atom**, also due to
   sparse punctuation. The Forward-Forward paper-equivalent content is
   present in the transcript but isn't reaching the brainstorm.
3. **Academic transcripts have a higher keep rate (38%) than tech-leader
   talks (16%)** because the academic talks use technical vocabulary that
   matches the positive-vocab regex more densely. Tech-leader talks are
   more colloquial; the prediction/analogy regexes fire on conversational
   tics but those don't carry positive-vocab anchors.

Recommendation for Run 6: feed unpunctuated transcripts through a
sentence-restoration preprocessor (the spaCy/regex hybrid TARI has)
before atom extraction. Expected lift: T007 from 0 → ~100 atoms,
T014 from 0 → ~20 atoms, T012 from 1 → ~50 atoms.

---

## 3. Tech-leader self-publish hit rate

`paradigm_shift/runs/run_005/_self_publish_audit.json` reports:

| Speaker | Self-publish hits | Total atoms | Hit rate | Matched cache entries |
|---|---|---|---|---|
| karpathy | **2** | 25 | 8.0% | `karpathy_software_3_0` ×2 |
| sutton | **1** | 2 | 50.0% | `sutton_bitter_lesson` ×1 |
| altman | 0 | 3 | 0% | — |
| hinton | 0 | 4 | 0% | — |
| lecun | 0 | 15 | 0% | — |
| amrith_setlur | 0 | 20 | 0% | — |
| belinda_li | 0 | 29 | 0% | — |
| nicholas_roberts | 0 | 35 | 0% | — |
| valerie_chen | 0 | 5 | 0% | — |
| yu_sun | 0 | 10 | 0% | — |
| **All speakers** | **3** | **148** | **2.0%** | — |

The Karpathy hits are the two atoms whose verbatim quotes share ≥3
content-words with Karpathy's own Software 3.0 talk snippet — i.e.,
Karpathy reciting his own thesis. The Sutton hit is from his Bitter
Lesson interview clip restating the original 2019 Bitter Lesson essay.

**These are signal, not noise.** They are exactly the cases the
self-publish cache was built to flag: a candidate built from a Karpathy
Software-3.0-paraphrasing atom would be a candidate that just
re-tells Karpathy's own published claim. The cache lets market_verifier
v2 downgrade such candidates from SURVIVES_MARKET_CHECK to
DOWNGRADED_SELF_PUBLISH. Run 5 had 0 stress survivors so the downgrade
path didn't fire in the market stage, but the signal is captured at the
atom level for downstream use.

LeCun is notable: 15 atoms, 0 self-publish hits. The JEPA/A-Path-Towards
papers are in the cache, but LeCun's talk content is high enough
abstraction that the 3-word-content-overlap threshold isn't tripped.
Either (a) the cache snippets are too narrow and miss the talk's vocab,
or (b) LeCun's talk legitimately stays out of his own published frame —
this is the question to refine in Run 6 by widening the cache snippets.

---

## 4. Cross-leader candidate count

`paradigm_shift/runs/run_005/candidates/_index.json` reports the
brainstorm output under the new cross-leader regime:

```json
{
  "n_candidates": 27,
  "operator_distribution": {
    "PREDICTION_GROUNDED_IN_PRINCIPLE": 8,
    "ANALOGY_TRANSFERS_TO_OPEN": 8,
    "BLOCKER_DISSOLVED_BY_PRINCIPLE": 3,
    "PREDICTION_RESOLVES_BLOCKER": 8
  },
  "speaker_diversity_distribution": {"2": 27},
  "speaker_class_pair_distribution": {
    "academic+tech_leader": 26,
    "tech_leader+tech_leader": 1
  },
  "require_cross_leader": true,
  "cross_leader_bias": true,
  "n_pairs_dropped_for_same_speaker": 0,
  "n_pairs_dropped_for_same_transcript": 130
}
```

Notes on the distribution:

- **27 / 27 candidates** have `speaker_diversity = 2`. The
  require_cross_leader constraint is enforced.
- **0 same-speaker pairs were dropped.** This is a corpus-shape
  consequence of the §2 extraction failure, not a sign the
  cross-leader constraint is inert. Same-speaker cross-transcript pairs
  would require atoms from both T007 AND T013 (Karpathy×Karpathy) or
  both T010 AND T012 (Hinton×Hinton). T007 yielded 0 atoms and T012
  yielded 0 kept atoms (the ASR/unpunctuated-transcript issue from §2),
  so no same-speaker atom pair is *possible* in this corpus regardless
  of constraint. The cross-leader filter is correctly implemented (a
  unit test confirms the predicate dispatch) but did not get to fire
  in Run 5 because the corpus structure made it a no-op. Once R6-1
  (sentence restoration) lands and T007/T012 produce atoms, the
  cross-leader constraint will start dropping real pairs.
- **Only 1 tech_leader+tech_leader candidate (CAND_run_005_019).** This
  is `BLOCKER_DISSOLVED_BY_PRINCIPLE` pairing Sutton's "we can't start
  with LLMs" blocker (T008) with a Karpathy software-changing
  first-principle (T013). It is the run's strongest structural test:
  two tech leaders, different paradigms, an operator that requires both
  a blocker and a first_principle (the rarest atom types).
- **26 academic+tech_leader candidates.** The cross-class bias ensures
  most candidates pair a researcher's open problem / prediction with a
  tech leader's prediction / first-principle. Run 5's intended hypothesis.

The 130 dropped same-transcript pairs is dominated by intra-T013 and
intra-T003 combinations (the two highest-yielding transcripts).

---

## 5. Surviving candidate composition

After the 6-layer pipeline (atoms → quality_filter → self_publish_audit
→ candidates → audit → scored → stress → market):

- **Audit:** 27 PASS or PASS_WITH_CAVEAT. (25 PASS + 2 PASS_WITH_CAVEAT.)
- **Scored:** 27 scored with heuristic weights. Top 5:

| Rank | candidate_id | predicted_impact | th | is | pt | ia | speaker_class_pair_kind | atoms |
|---|---|---|---|---|---|---|---|---|
| 1 | CAND_run_005_004 | 0.510 | 0.0 | 8.0 | 0.50 | 0.50 | academic+tech_leader | Belinda Li × Karpathy |
| 2 | CAND_run_005_016 | 0.510 | 0.0 | 8.0 | 0.50 | 0.50 | academic+tech_leader | LeCun × Belinda Li |
| 3 | CAND_run_005_013 | 0.493 | 0.0 | 5.0 | 0.60 | 0.50 | academic+tech_leader | Karpathy × Roberts |
| 4 | CAND_run_005_027 | 0.493 | 0.0 | 5.0 | 0.60 | 0.50 | academic+tech_leader | Belinda Li × Karpathy |
| 5 | CAND_run_005_001 | 0.488 | 0.0 | 5.0 | 0.50 | 0.50 | academic+tech_leader | (per file) |

Note `time_horizon=0.0` everywhere: the atom_typer extracted no
horizon-bearing quote (no `in N years` or `by 20XX`), and target_date
fell back to the source_date (~2025), which is essentially "now" relative
to today. Predicted impacts collapse to ~0.49 ± 0.02 because the
heuristic weight collapses under that prior.

- **Stress:** 0 of 27 PASS_STRESS. All 27 → FAIL_RAG_UNGROUNDED.
  The synthesized search callback returns `[]` because the sandbox has
  no live web_search hook. This is identical to Run 1's documented
  behavior; the stress layer correctly behaves as fail-closed when the
  RAG cache is empty.
- **Market:** 0 candidates reached the market stage (all rejected at
  stress).

**Final survivors: 0.** This satisfies the MV-1..MV-5 mechanism
validation but not S-1 substantive. S-1 would require a live web_search
hook to populate `_search_cache.json`, which the sandbox cannot do.

---

## 6. What changed structurally between Run 1 and Run 5

### Atoms layer
- **Run 1:** Single-pass regex extraction, no quality filter.
- **Run 5:** Adds `paradigm_shift/atom_quality_filter.py`. Keeps atom
  iff (≥1 positive-vocab hit OR paradigm_type in {open_problem,
  first_principle}). Positive vocab: AGI, scaling laws, world model,
  JEPA, software 2.0/3.0, agent, distillation, distributed,
  multi-modal, embodied, simulator, plus ~50 other paradigm-shift-shaped
  terms. Result: 579 → 148 atoms (74% rejection rate on the larger
  corpus); the kept atoms are anchored to a topical paradigm-shift
  vocabulary.

### Candidates layer
- **Run 1:** require_cross_transcript=True. 10 candidates from 4 of 5
  transcripts; all academic.
- **Run 5:** require_cross_leader=True, cross_leader_bias=True. 27
  candidates; 27/27 have ≥2 distinct speaker_ids; 26/27 mix academic
  with tech_leader. The constraint is **strictly stronger** than
  cross_transcript (Karpathy T007 × Karpathy T013 would have been
  accepted under cross_transcript but is excluded under cross_leader).

### Layer 6 v2 (market)
- **Run 1:** No self-publish cache.
- **Run 5:** Adds `paradigm_shift/speaker_self_publish_cache.json` +
  `paradigm_shift/speaker_self_publish.py`. The cache contains the
  paradigm-shift-shaped flagship papers/essays for each tech leader
  (Karpathy Software 2.0/3.0/intro-LLMs; Sutton Bitter Lesson; Altman
  Moore's Law for Everything + Planning for AGI; Hinton Forward-Forward
  arXiv:2212.13345 + Capsule Networks + Distillation; LeCun A Path
  Towards Autonomous Machine Intelligence + I-JEPA arXiv:2301.08243
  + V-JEPA; Naval How to Get Rich; Weijia Shi In-Context Pretraining
  + REPLUG + FlexOlmo + Visual Sketchpad — forward-looking, not yet
  in-corpus). The market_verifier v2 post-pass enriches each market-
  stage candidate with a self_publish_check field and downgrades the
  verdict from SURVIVES_MARKET_CHECK to DOWNGRADED_SELF_PUBLISH if all
  atoms paraphrase the speaker's own work.

---

## 7. The "14 trivial labels" signal from the prompt

The prompt reports "14 user labels accumulated, all trivial" across the
intermediate runs 2-4. That signal — even taken at face value — has a
clear interpretation:

**Hypothesis H-trivial:** Under cross-transcript-only brainstorm on a
mixed academic+tech-leader corpus, the candidates that survive Layers
2-5 are mechanically valid but humanly uninteresting because they pair
atoms that come from the same speaker's expressed paradigm (e.g.,
Karpathy T007 × Karpathy T013 = a paraphrase, not a synthesis).

Run 5's cross-leader constraint is the **direct mechanical test of
H-trivial**. If the cross-leader candidates also come back trivial under
user labeling, H-trivial is falsified and the deeper failure mode is
elsewhere (e.g., the atom_typer is extracting conversational filler,
the analogy_engine's template is too generic, or the academic-leader
pairing is fundamentally a culture-clash rather than a paradigm-shift).

If even half of Run 5's cross-leader candidates label ≥2 (small-but-
non-trivial), H-trivial is supported and Run 6 should double down on
the cross-leader axis (sample more leaders, longer talks, broader
vocab).

---

## 8. Honest limitations of Run 5 (un-resolved from Run 1)

1. **No real WebSearch hook in the sandbox.** Stress and market layers
   are unable to ground sub-claims or check existing startups. All 27
   candidates → FAIL_RAG_UNGROUNDED. Same as Run 1.
2. **T007 / T012 / T014 extracted near-zero atoms** due to ASR-style
   unpunctuated transcripts. The Karpathy Intro-to-LLMs talk
   (T007), Hinton's Forward-Forward talk (T012), and Naval's tweetstorm
   (T014) are all effectively absent from the brainstorm despite being
   in the corpus. Run 6 needs a sentence-restoration preprocessor.
3. **Weijia Shi transcript was expected but not committed.** Her papers
   are cached for self-publish detection but no atoms exist for her.
   She is effectively "available for Run 6" rather than represented in
   Run 5.
4. **Impact-scoring is still heuristic.** With only 3 labeled candidates
   from Run 1 (and the prompt-reported 14 from Runs 2-4 not committed
   to `impact_labels.json`), the logistic-regression refit threshold
   (10+ labels with positive variance) is not yet met. Predicted impact
   stays near 0.49 ± 0.02 for all candidates.
5. **Cross-field analogy may still produce surface metaphor (R279
   risk).** Stress test reduces this but cannot eliminate; the empty
   RAG cache means we can't tell which of the 27 are surface vs deep.
6. **The cross-leader-bias is unidirectional toward academic+tech_leader.**
   tech_leader+tech_leader pairs are deprioritized because the bitter-
   lesson / forward-forward / JEPA atom yield is low (T008: 2 atoms,
   T010: 4 atoms, T012: 0 atoms). Run 6 with a sentence-restored
   T012 + T007 + T014 could re-balance this — expected to surface
   multi-tech-leader pairs like Karpathy×Hinton or LeCun×Sutton.

---

## 9. Action items for Run 6

Based on what Run 5 surfaced and what it didn't:

- **R6-1.** Add a sentence-restoration preprocessor for unpunctuated
  transcripts. T007/T012/T014 should each contribute ≥10 atoms.
- **R6-2.** Fetch and commit the Weijia Shi transcript so her atoms
  enter the brainstorm; the cache is already populated.
- **R6-3.** Wire a real (or canned-batch) WebSearch hook for the
  stress/market layers. Without it, S-1 is structurally unreachable.
- **R6-4.** Once 10+ user labels exist on cross-leader candidates,
  refit `impact_filter_weights.json` and re-score. Expected effect:
  predicted_impact distribution widens and the top-3 are no longer
  tied at 0.51.
- **R6-5.** Widen the speaker_self_publish_cache snippets (current cache
  uses ~50-100 chars per paper; LeCun's 0/15 hit rate suggests the
  cache misses are conservative). Aim for ~200-char snippets that
  cover the abstract+intro of each cached paper.
- **R6-6.** Add cross-LLM verification queue for the top-K candidates
  the user labels as ≥3 — the queue items would be (a) the candidate
  JSON, (b) the source verbatim quotes, (c) the asserted novelty claim.
  An external LLM (Sonnet, Haiku, GPT) can stress-test independently.

---

## 10. Files added or modified by Run 5

- `paradigm_shift/atom_quality_filter.py` — new module (Phase 1).
- `paradigm_shift/speaker_self_publish_cache.json` — new asset (Phase 2).
- `paradigm_shift/speaker_self_publish.py` — new module (Phase 2).
- `paradigm_shift/analogy_engine.py` — augmented `ParadigmCandidate`
  with `source_speaker_ids` / `speaker_diversity` /
  `source_speaker_classes` / `speaker_class_pair_kind`; added
  `require_cross_leader` and `cross_leader_bias` flags to
  `brainstorm_paradigm_candidates`.
- `paradigm_shift/orchestrator.py` — added two new stages
  (`atom_quality_filter`, `self_publish_audit`); added market-stage
  v2 post-pass that enriches with `self_publish_check`; added
  `--require_cross_leader` and `--cross_leader_bias` CLI flags.
- `paradigm_shift/runs/run_005/manifest.json` — 13-transcript manifest
  with speaker_id / speaker_class fields per transcript.
- `paradigm_shift/runs/run_005/` — full run output tree.
- `output/run_004_vs_run_005.md` — this comparison document.

No existing files were deleted. All Run 1 artifacts remain untouched
in `paradigm_shift/runs/run_001/`.
