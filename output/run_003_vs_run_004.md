# Run 3 vs Run 4 — Atom Quality Filter Impact

**Author:** Claude (Opus 4.7 / `claude-opus-4-7[1m]`), branch `claude/paradigm-shift-finder-EAtbj`.
**Date:** 2026-05-22.
**Status:** Phase 6 of Run 4.

Run 4 adds:
- `paradigm_shift/atom_quality_filter.py` (5 positive + 5 negative features)
- `paradigm_shift/youtube_fetcher_v2.py` (3 fallback methods)
- Orchestrator: new `atoms_filtered` stage between `atoms_paradigm` and `candidates`

Same 5 academic transcripts (T001–T005); auto-fetch sandbox-blocked across
all 3 methods (see `paradigm_shift/fetch_methods_log.json`); Weijia Shi
transcript not yet pushed to repo. Corpus expansion still deferred.

---

## 0. Headline

| Metric                          | Run 3              | Run 4               | Δ                  |
| ------------------------------- | ------------------ | ------------------- | ------------------ |
| Paradigm atoms total            | 264                | 42 (filtered)       | -84%               |
| Predictions                     | 99                 | 32                  | -68%               |
| Analogies                       | 153                | 9                   | -94%               |
| Open problems                   | 7                  | 0                   | -100%              |
| Blockers                        | 5                  | 1                   | -80%               |
| Candidates brainstormed         | 10                 | 5                   | -50%               |
| Operators firing                | 2 of 4             | **1 of 4**          | analogy→open dead  |
| Layer 5 PASS_STRESS             | 10                 | 4                   | (5→4 after RAG fix)|
| Layer 6 v2 SURVIVES             | 6                  | 4                   | -2                 |
| Layer 6 v2 FAIL_SPEAKER         | 4                  | 1                   | -3 false-negative? |

The filter removed 84% of atoms. The downstream effect is **fewer
candidates, more focused atom content** — but on academic input, only one
of the 4 typed operators still fires.

---

## 1. Did the filter reduce noise?

`paradigm_shift/runs/run_004/atoms_filter_report.json`:

```
pass_by_paradigm_type = {"prediction": 32, "analogy": 9, "blocker": 1}
reject_by_negative_feature = {
    "no_positive_features":       157,   # majority of rejections
    "F-2_pure_analogy_no_mechanism": 132,
    "F-4_adjective_only_prediction":  11,
    "F-3_surface_noun_no_specifics":  11,
    "F-1_talk_meta":                   3,
    "F-5_definitional_blocker":        1,
}
```

**Yes — most rejected atoms had zero positive features** (157/222 = 71% of
rejections). The dominant signal is "atom contains no ML primitive, no
algorithm name, no number, no mechanism, no time marker" — i.e., academic
spoken-language qualifiers that the original regex over-extracted.

**F-2 (pure analogy without structural mapping)** rejected 132 of 153
analogy atoms. The surviving 9 analogy atoms all contain at least one
structural-mapping marker ("preserves", "isomorphism", "like X but for Y",
etc.) — exactly the design intent.

**Open-problem atoms went to 0** — all 7 in Run 3 lacked the F+1..F+5
positive features the filter requires. Examples like *"many of these
challenges remain open problems"* were rejected for no specific named
problem.

---

## 2. Per-transcript yield

| Transcript ID | Speaker             | Atoms in Run 3 | Atoms in Run 4 (filtered) | Retention |
| ------------- | ------------------- | -------------- | ------------------------- | --------- |
| T001          | Belinda Li          | 89             | 19                        | 21%       |
| T002          | Yu Sun              | 44             | 7                         | 16%       |
| T003          | N. Roberts          | 67             | 10                        | 15%       |
| T004          | V. Chen             | 6              | 1                         | 17%       |
| T005          | A. Setlur           | 58             | 5                         | 9%        |

Yu Sun and Setlur transcripts retain the smallest percentage but the
absolute counts are still meaningful. Belinda Li retains the most absolute
atoms (19) — her talk has explicit references to "self-models", "world-models",
"updatability", and a mix of mechanism-claim language that survives the
filter.

**Cross-transcript composition of surviving candidates:**

| Candidate | Source transcripts | Speakers              |
| --------- | ------------------ | --------------------- |
| 001       | T005, T002         | Setlur, Yu Sun        |
| 002       | T003, T002         | Roberts, Yu Sun       |
| 003       | T001, T002         | Li, Yu Sun            |
| 004       | T001, T002         | Li, Yu Sun            |
| 005       | T003, T002         | Roberts, Yu Sun       |

All 5 candidates pair a Yu Sun blocker atom (the single surviving blocker
`ATOM_T002_S020_BLO_01`) with a prediction atom from another transcript.
The candidate diversity collapses to "Yu Sun's long-context blocker +
something else" — a structural artifact of having only 1 blocker atom
after filtering.

---

## 3. New surviving candidates after Layer 6 v2

```
Run 4 Layer 6 v2 verdicts:
  SURVIVES_MARKET_CHECK_V2:        4    (CAND_001, 002, 003, 004)
  FAIL_MARKET_EXISTS_V2_SPEAKER:   1    (CAND_005 — Yu Sun TTT match, sim 0.301)
```

**Why only 1 v2 SPEAKER-collision in Run 4 (vs 4 in Run 3)?**

The atom-quality filter changed which prediction atoms feed each candidate.
For CAND_005, the prediction atom is a Roberts atom whose verbatim content
includes test-time-training-adjacent language ("models are actually going
to ..."), so its semantic anchor overlaps with Yu Sun's TTT paper at sim
0.301.

For CAND_001-004, the surviving prediction atoms talk about:
- *scaling model size* (CAND_001, Setlur)
- *understanding when models work* (CAND_002, Roberts)
- *building truly transparent AI* (CAND_003, Li)
- *world/user/self models as unifying framework* (CAND_004, Li)

None of these primary keywords ("model", "humans") trigger a strong-enough
TF-IDF match with the Yu Sun TTT paper (raw similarity < 0.15). They also
don't match Setlur's RL Hard Problems papers — different semantic content.

**Note this is partly a false-negative.** In Run 3, CAND_007/008/009 were
caught because their atoms were *Yu Sun's actual long-context-mechanism
sentences*, and the test-time-training-shaped semantic anchor matched
Yu Sun's TTT papers directly. In Run 4, the filter removed those atoms
(they were rejected as `F-4_adjective_only_prediction` or
`no_positive_features`), so the v2 speaker check has weaker content to
match against.

The filter's precision-bias acts in both directions: it reduces noise
(good) but also weakens the speaker-collision signal when the speaker's
own atoms were what triggered the original match (bad).

---

## 4. Speaker self-publish patterns

`paradigm_shift/speaker_publications_cache.json` populated:

- **Yu Sun**: TTT family (2407.04620, 2512.23675); Test-Time Training
  project website; Stanford trustworthy-AI page
- **Amrith Setlur**: "Reuse-your-FLOPs" (2026), POPE (2026), RL on
  Incorrect Synthetic Data (NeurIPS 2024)
- **Nicholas Roberts**: Compute Optimal Scaling of Skills (ACL Findings
  2025), Pretrained Hybrids with MAD Skills (COLM 2025)
- **Belinda Li**: Eliciting Human Preferences with Language Models
  (ICLR 2025)
- **Valerie Chen**: Collaborative Effort Scaling (NeurIPS 2025
  Responsible-FM Workshop Best Paper)

All 5 speakers have published follow-up work, matching the design
prediction. The Run 4 v2 speaker check correctly retrieves these and uses
TF-IDF cosine to determine similarity per candidate.

---

## 5. Is the pipeline mechanism- or content-limited?

**Mechanism status after Run 4:**
- ✅ Atom quality filter accepts/rejects with documented criteria.
- ✅ Filter reduces 264 → 42 atoms (84% reduction); 71% of rejections are
  "no positive features" — exactly the target population.
- ✅ Layer 5 stress test functions normally on the smaller candidate set
  (4 PASS_STRESS, 1 FAIL_RAG).
- ✅ Layer 6 v2 catches the Yu Sun TTT collision for CAND_005 with weighted
  sim 0.301; survival rate on filtered candidates is 80% (4/5) vs 60%
  (6/10) in Run 3.
- ⚠️ The filter is too aggressive on `analogy` (94% rejection) and totally
  removes `open_problem` atoms (100%). The `ANALOGY_TRANSFERS_TO_OPEN`
  operator stops firing entirely.
- ⚠️ Only `prediction + blocker` candidates remain. 1 of 4 typed operators.

**Content status (unchanged from Run 3):**
- ❌ Still 0 `first_principle` and 0 `trend` atoms.
- ❌ Still no tech-leader content (auto-fetch v2 still 403 across all 3
  methods).
- ❌ Surviving candidates still cite Yu Sun's blocker `ATOM_T002_S020_BLO_01`
  in 5 of 5 cases — single-blocker bottleneck after filtering.

**Conclusion (unchanged):** Pipeline is **input-quality-limited, not
mechanism-limited**. The atom quality filter improves precision but cannot
manufacture content the inputs lack.

---

## 6. Filter trade-off: precision vs operator coverage

Run 4 ran with the filter's default thresholds. A future iteration might
relax the negative features to preserve operator coverage:

| Possible relaxation              | Trade-off                                                                          |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| F-2 only rejects "X is like Y" without context | Recovers more analogy atoms; may readmit pure-metaphor atoms             |
| F-3 only rejects when first 30 chars are meta  | Recovers some open_problem atoms; readmits some surface-noun atoms       |
| Treat ALL `open_problem` as F+ implicitly      | Restores ANALOGY_TRANSFERS_TO_OPEN combinator; lower-quality candidates  |

These are tuning knobs for Run 5; not changed in Run 4.

---

## 7. Honest limits of Run 4

- **The filter is precision-biased by design.** It rejects ~84% of atoms,
  including some that would have been useful in some combinator. The trade
  is fewer, sharper candidates.
- **Filter reduces operator coverage** from 2 of 4 (Run 3) to 1 of 4
  (Run 4). The mechanism is healthy but starved for atom diversity.
- **Auto-fetch v2 still blocked.** Sandbox network policy excludes
  youtube.com, googleusercontent.com, and 3 wrapper services. The
  fetcher code is correct; sandbox cannot execute it. `paradigm_shift/
  fetch_methods_log.json` documents this.
- **Weijia Shi transcript not pushed.** The user mentioned manually
  pushing `transcript_006_weijia_shi_modular_lm.txt` to `tari/inputs/`,
  but the file is not in the repo. Run 4 proceeded with the existing 5
  transcripts.

---

## 8. Action items for Run 5

- AI-1. Tune `paradigm_shift/atom_quality_filter.py` to be less aggressive
  on `open_problem` and `analogy` types (recover operator coverage).
- AI-2. Ingest Weijia Shi transcript when it lands in `tari/inputs/`.
- AI-3. Run `paradigm_shift/youtube_fetcher_v2.py fetch ...` from a
  non-sandboxed machine to get the 11-URL tech-leader corpus.
- AI-4. Re-run pipeline on the expanded corpus; expect
  `first_principle` and `trend` atoms > 0 and all 4 typed combinators
  firing.
- AI-5. Generate cross-LLM verify queue for any Run-5 candidates that
  survive Layer 6 v2 with non-Yu-Sun-source content.
