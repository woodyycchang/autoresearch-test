# Paradigm-Shift Finder v1 — 6-Layer Pipeline with RAG + Trainable Impact Filter

**Author:** Claude (Opus 4.7 / `claude-opus-4-7[1m]`), branch `claude/paradigm-shift-finder-EAtbj`.
**Date:** 2026-05-21.
**Status:** Design doc — Phase 1 of new project branch alongside `tari` and `niche-mining-autoresearch`.

---

## 0. Why a new pipeline, again

### 0.1 Acknowledgement of TARI v1/v2 result

TARI v1 (run_001, single-transcript, Belinda Li) and TARI v2 (run_002,
cross-transcript on 5 frontier-research talks) together produced
**zero substantive candidates** that survive the existing detector chain.
Across 19 audit-surviving candidates from run_002, all 19 returned
`FAIL_STEP_06_KEYWORD_THRESHOLD` — the cited atoms' content words landed
on existing arXiv preprints with ≥2-token overlap on the first
three returned hits.

The root cause is structural, and was honestly predicted by TARI v1
design §0.4: the target was a **paper-level ML architectural niche** in
a corpus (academic colloquium talks 2024-2026) where the candidates'
mechanical content words are saturated against the same 2024-2026
arXiv community Claude has indexed. Atom × atom cross-combination
on `probing × associative scan × test-time RL` cannot escape that.

The hypothesis carried into v2 — that cross-transcript pairwise
combination would reach a non-saturated niche — was wrong because the
five chosen transcripts are all drawn from the saturated community.
TARI did exactly what its design contract said it would do; the design
contract targeted the wrong distribution.

### 0.2 What `paradigm_shift_finder` changes

The new target is no longer "find a paper-level architectural niche."
The new target is **paradigm-shift candidates at startup-direction
granularity** — claims about *what the field should be doing in 3-10
years* that (a) cross fields, (b) survive a first-principles stress
test, (c) have no existing product/startup, (d) are tractable for a
solo founder POC. The Karpathy/Altman-shape claim, not the
"propositional probes" claim.

The input distribution flips correspondingly. Instead of academic
colloquium transcripts (researcher reporting *what they did*), the
target input is **longitudinal tech-leader vision content** —
multi-year corpora of long-form interviews, essays, blog posts, and
talks from people whose explicit job is to predict where the field
goes. The atom inventory shifts from `PRIMITIVE`/`MECHANISM_CLAIM`/
`NEGATIVE_RESULT`/`METRIC`/`OPEN_QUESTION` to **`prediction`**,
**`blocker`**, **`first_principle`**, **`analogy`**,
**`open_problem`**, **`trend`**. Each carries a date so we can spot
predictions whose predicate has not yet materialized in market.

### 0.3 Honest framing up front

Six predicted failure modes that this design does NOT claim to solve:

1. **Cross-field analogy may produce surface metaphor.** R279 risk
   from program_v20 persists. The first-principles RAG check reduces
   but does not eliminate.
2. **First-principles RAG reduces hallucination ~50-70%, not 100%.**
   Per-sub-claim retrieval narrows the space but Claude still glues the
   sub-claims into a story. Self-consistency-3 + atomic decomposition
   reduce further; we cannot prove they zero out.
3. **Impact-score classifier needs 10+ runs (50+ candidates, 10-20
   labels) to become meaningful.** Run 1 ships with hand-set heuristic
   weights only.
4. **Tech-leader vision content overlaps Claude's training corpus.**
   Anything Sam Altman, Demis Hassabis, Karpathy, Sutskever, etc. said
   publicly before Jan 2026 is plausibly indexed. Run 1 on academic
   transcripts is mechanism validation only.
5. **Market verifier returns false negatives.** A search-shaped query
   missing the right product term will say "no existing startup" when
   one exists. We mitigate with 3-5 query reformulations per
   candidate but cannot promise coverage.
6. **First-principles stress test is itself Claude.** The 4-question
   challenge is asked of the model. We grade rejections by stability
   across 3 framings — not by oracle ground truth.

### 0.4 What this pipeline does NOT replace

`paradigm_shift_finder` is additive to TARI; it does not delete TARI's
artifacts. The two pipelines coexist because their failure modes are
different. If a candidate survives both pipelines on disjoint axes,
that is meaningful signal. If `paradigm_shift_finder` reaches 0 after
its Phase 4 run on academic transcripts, that result is itself the
mechanism validation: we will have shown that academic colloquium
content can never be paradigm-shift input under any pipeline, which
is a useful constraint for the next iteration.

---

## 1. Architecture (6 layers)

```
INPUT_CORPUS (multiple transcripts/essays/posts from tech leaders,
              longitudinal — same author across multiple dates)
        |
        v
[Layer 1: source_curation]
        |  Manual + scripted: 5-30 high-quality long-form pieces.
        |  Each tagged with (author, date, format, topic, vision_horizon).
        |  Output: manifest.json
        v
[Layer 2: paradigm_shift/atom_typer.py]
        |  Extend TARI's atom extractor with 6 new type tags:
        |    - prediction       (claim about future state of field/world)
        |    - blocker          (named obstacle preventing prediction)
        |    - first_principle  (foundational constraint the speaker invokes)
        |    - analogy          (cross-field comparison the speaker makes)
        |    - open_problem     (unsolved thing the speaker flags)
        |    - trend            (multi-year trajectory the speaker tracks)
        |  Each atom inherits TARI's verbatim_quote/snippet_id/line_span
        |  contract for traceability.
        v
ATOMS/ATOM_*.json  (typed, dated, source-anchored)
        |
        v
[Layer 3: paradigm_shift/analogy_engine.py]
        |  Cross-atom combine, restricted to pairings that respect type:
        |    - prediction + first_principle  → testable hypothesis
        |    - analogy + open_problem         → cross-field transfer
        |    - blocker + first_principle      → wedge candidate
        |    - prediction + blocker           → resolution candidate
        |  Each combination must include a 1-line first-principles validity
        |  hypothesis (which physical/economic/computational law makes
        |  this combination coherent).
        v
RAW_CANDIDATES/CAND_*.json
        |
        v
[Layer 4: paradigm_shift/impact_filter.py]
        |  4-axis scoring per candidate:
        |    - time_horizon          (years out: 0..15+, prefer 3-10)
        |    - impact_scale          (revenue/users/societal log10, 0..10)
        |    - poc_tractability      (solo-founder buildable, 0..1)
        |    - information_asymmetry (Claude-knows-but-market-doesn't,
        |                             measured as # known players named
        |                             by Claude vs # found by market_verifier)
        |  Initial weights from manual heuristic (set in this doc, §4).
        |  After each run, log predicted_impact + user_label_needed.
        |  Logistic regression refit on accumulated labels (after 10+ runs).
        v
SCORED_CANDIDATES/CAND_*.json  (with predicted_impact ∈ [0,1])
        |
        v
[Layer 5: paradigm_shift/first_principles_stress.py]
        |  4-question challenge per candidate:
        |    Q1: What law/constraint forces this prediction true?
        |    Q2: What law/constraint would have to bend for the prediction to fail?
        |    Q3: Atomic decomposition: list 3-5 verifiable sub-claims.
        |    Q4: For each sub-claim, ground it in ≥1 retrieved web/arXiv source.
        |  Hallucination prevention:
        |    - RAG: web_search per sub-claim (1+ retrieved doc required)
        |    - Self-consistency: ask Q1+Q2 three times with different framings;
        |                        reject if claims are not stable across all 3
        |    - Per-sub-claim grounding check: each sub-claim must cite a
        |      retrieved source from the corresponding web_search
        |  Reject candidate if ANY sub-claim is ungrounded or unstable.
        v
STRESS_SURVIVING/CAND_*.json
        |
        v
[Layer 6: paradigm_shift/market_verifier.py]
        |  For each survivor, search the live web for:
        |    - "existing startup doing X"
        |    - "existing product doing X"
        |    - "YC company X"
        |    - "Series A X"
        |    - "open source project X"
        |  3-5 query reformulations.
        |  If 0 strong matches across all reformulations: SURVIVES_MARKET_CHECK.
        |  Otherwise: FAIL_MARKET_EXISTS with citations.
        v
FINAL/CAND_*.json  (paradigm-shift candidates with full chain)
        |
        v
[paradigm_shift/impact_label_logger.py]
        |  Prompt user to label top-3 candidates 1-5 on impact.
        |  Append to paradigm_shift/impact_labels.json for future training.
```

The orchestrator (`paradigm_shift/orchestrator.py`) drives all six
layers, checkpoints state between layers (each layer's output is a
directory of JSON files plus an `_index.json`), and writes a final
`summary.md`. Resume-from-checkpoint is supported so a long Layer 5
RAG step does not have to re-run when Layer 6 is debugged.

---

## 2. Atom type taxonomy (Layer 2)

Six type tags, each backed by a regex pattern set in `atom_typer.py`:

| Type              | Marker phrases (illustrative)                          | Carries date? |
| ----------------- | ------------------------------------------------------ | ------------- |
| `prediction`      | "in 5 years", "by 2030", "I think we'll see", "will be" | yes (extracted from quote if present, else inherits from source.date) |
| `blocker`         | "the bottleneck is", "what's stopping us", "we can't"   | yes |
| `first_principle` | "fundamentally", "the physics is", "the constraint is", "in principle" | yes |
| `analogy`         | "like X but for Y", "X is to Y what A is to B", "imagine" | yes |
| `open_problem`    | "open question", "we don't know", "unsolved"            | yes |
| `trend`           | "over the last N years", "the trajectory is", "scaling"  | yes |

`atom_typer.py` reuses TARI's `extract_atoms_for_snippet` interface
but writes atoms with an extra `paradigm_type` field. TARI atoms (`PRIMITIVE`,
`MECHANISM_CLAIM`, etc.) are still extracted from each snippet so we
retain the option of pairing a TARI-typed atom with a paradigm-typed
atom in Layer 3.

Failure mode acknowledged: **regex-based type tagging is precision-biased
and will under-extract.** Long-form essays often phrase predictions
without trigger words ("we will see"); they say things like "the
generation that learns this will not need keyboards." We accept lower
recall in exchange for traceability — a missed atom is better than a
fabricated type.

---

## 3. Analogy engine (Layer 3)

Cross-atom combinations restricted by type. The 4 typed combinators:

| Operator                            | Atom A         | Atom B            | Output framing                                            |
| ----------------------------------- | -------------- | ----------------- | --------------------------------------------------------- |
| `PREDICTION_GROUNDED_IN_PRINCIPLE`  | prediction     | first_principle   | "Prediction A holds IF first-principle B is binding."     |
| `ANALOGY_TRANSFERS_TO_OPEN`         | analogy        | open_problem      | "Apply analogy A's structure to unresolved problem B."    |
| `BLOCKER_DISSOLVED_BY_PRINCIPLE`    | blocker        | first_principle   | "Blocker A is dissolved if we recognize principle B."     |
| `PREDICTION_RESOLVES_BLOCKER`       | prediction     | blocker           | "Prediction A is the resolution of blocker B."            |

Each combination output includes a `first_principles_validity_hypothesis`
field: a 1-sentence statement of which physical/economic/computational
law makes the pairing coherent. Layer 5 will stress-test this field;
Layer 3 does not validate it (that would be circular — Claude scoring
its own claim before the RAG layer runs).

Constraint inherited from TARI: every candidate cites ≥2 atoms from
distinct snippets, and each atom's `verbatim_quote` must appear
verbatim in the source. The self-model audit step (carried over from
TARI's `self_model_audit.py`) runs before Layer 4 and rejects
candidates whose atoms have drifted.

---

## 4. Impact filter & trainable classifier (Layer 4)

### 4.1 The 4 axes

Each candidate is scored on:

| Axis                      | Range  | Meaning                                                                 |
| ------------------------- | ------ | ----------------------------------------------------------------------- |
| `time_horizon`            | 0..15  | Years until prediction materializes (extracted from atom date markers + heuristic). Prefer 3-10. |
| `impact_scale`            | 0..10  | log10 of estimated affected entities (users / dollars / population).    |
| `poc_tractability`        | 0..1   | Solo-founder buildable in 3-6 months without specialty hardware.        |
| `information_asymmetry`   | 0..1   | (Claude-named players − market-verifier-found players) / Claude-named players. |

### 4.2 Initial heuristic weights (Run 1)

```
predicted_impact = sigmoid(
    + 0.30 * (1 - |time_horizon - 6| / 9)        # peak at 6 years
    + 0.30 * (impact_scale / 10)                  # bigger is better
    + 0.20 * poc_tractability                     # buildable matters
    + 0.20 * information_asymmetry                # asymmetry matters
)
```

These weights are deliberate priors, not data-derived. They go into
`paradigm_shift/impact_filter.py` as named constants so the user can
override.

### 4.3 Trainable refit (Runs 2+)

After each run, `impact_label_logger.py` prompts the user to label
1-2 candidates with a 1-5 impact score. Labels accumulate in
`paradigm_shift/impact_labels.json`:

```json
{
  "labels": [
    {
      "candidate_id": "CAND_001_007",
      "run_id": "run_001",
      "predicted_impact": 0.62,
      "user_label": 4,
      "labeled_at": "2026-05-21T..."
    }
  ]
}
```

Once ≥10 labels are accumulated, `impact_filter.py` fits a logistic
regression (4 features → user_label binarized at ≥3) and replaces the
heuristic weights with the fitted coefficients. The threshold of 10
labels is honest: regression on 4 features needs at least 10 samples
for any meaningful coefficient estimate, and even 10 is a weak prior.
The classifier is **not** expected to be useful before run 5 / 10+
labels.

### 4.4 What the impact filter does NOT do

- It does not gate Layer 5. Even low-impact candidates flow through
  the first-principles stress test, so we don't lose signal from a
  bad initial heuristic. The filter only ranks the final output.
- It does not predict business success. It predicts a user-aligned
  ranking of paradigm-shift candidates by the user's own impact
  perception.

---

## 5. First-principles stress test (Layer 5) — hallucination prevention

This is the layer most at risk of generating Claude-internal fiction
masquerading as external grounding. The countermeasures, in order
applied per candidate:

### 5.1 Atomic decomposition

Layer 5 prompts the model: *"Given the combined claim of CAND_X, list 3-5
verifiable sub-claims, each a single declarative sentence with a single
verifiable predicate."* This forces the candidate into atomic statements
that can be checked one at a time, rather than one rolling thesis.

### 5.2 Per-sub-claim RAG

For each sub-claim, the orchestrator issues a real `web_search` query
constructed from the sub-claim's content words. The first 3 returned
documents are retained as the sub-claim's grounding set. If **0
documents** are returned, the sub-claim fails immediately.

If documents are returned but none of them contain the sub-claim's
key predicate (mechanical check: ≥2 content words from sub-claim must
appear in document title+snippet), the sub-claim is marked
`UNGROUNDED_BUT_SEARCHED` and the candidate is rejected with that
flag.

If at least 1 document covers the sub-claim's predicate, the sub-claim
is marked `RAG_GROUNDED` with the supporting document URL. The
candidate accumulates as many `RAG_GROUNDED` flags as sub-claims it
has.

A candidate proceeds to §5.3 only if **all** its sub-claims are
`RAG_GROUNDED`.

### 5.3 Self-consistency check (3 framings)

For Q1 ("what law/constraint forces this prediction true?") and Q2
("what law would have to bend for it to fail?"), the orchestrator
asks the same question three times with different framings:

- Framing A: declarative ("State the principle that...")
- Framing B: counterfactual ("If the prediction failed, which assumption broke?")
- Framing C: comparative ("Compared to the alternative X, why is this prediction privileged?")

Each framing's answer is reduced to a list of named principles
(extracted via simple noun-phrase matching). If the **intersection
across all 3 framings is empty** (no principle named in all 3 answers),
the candidate is marked `UNSTABLE_FIRST_PRINCIPLES` and rejected.

This is a coarse check — it cannot detect a clever model that names
the same fabricated principle across all 3 framings. We accept this
limitation. Self-consistency-3 catches noise; it does not catch
systematic hallucination. The RAG step in §5.2 is the load-bearing
defense against fabrication.

### 5.4 Honest acknowledgment

Both §5.2 and §5.3 reduce, but cannot eliminate, hallucination:

- **§5.2 limits:** web_search snippets are 2-3 sentences; Claude can
  always cherry-pick a snippet that *seems* to support a sub-claim.
  The mechanical keyword-overlap check is precision-low (a doc about
  X might cover X's *opposite* and still match keywords).
- **§5.3 limits:** Claude has stable training-data priors; asking the
  same question 3 ways often returns 3 versions of the same answer
  regardless of whether the answer is correct.

Expected hallucination reduction vs. ungrounded brainstorm: 50-70%.
This is a guess, not a measurement. Run 1 will produce data; subsequent
runs will let us tune.

---

## 6. Market verifier (Layer 6)

For each Layer-5 survivor, the verifier issues 3-5 web_search queries
designed to find existing solutions:

1. `"<candidate primary product noun> startup"`
2. `"<candidate primary mechanism> YC company"`
3. `"open source <candidate primary product noun>"`
4. `"<candidate primary product noun> Series A OR Series B"`
5. `"<candidate primary product noun> founded 2024 OR 2025 OR 2026"`

A "strong match" requires ≥3 content-word overlap with the candidate's
primary noun phrase in title+snippet, AND the matched document's
publication date is within the last 24 months.

Verdicts:
- `SURVIVES_MARKET_CHECK`: 0 strong matches across all reformulations.
- `FAIL_MARKET_EXISTS`: ≥1 strong match. Records the matched
  startups/products with URLs.

Honest failure mode: search-engine result quality is the bottleneck.
A startup that exists but doesn't surface in the top results we issue
will be a false negative.

---

## 7. Orchestrator and checkpointing

`paradigm_shift/orchestrator.py` defines `Stage = Literal[
    "manifest", "atoms", "candidates", "scored", "stress", "market", "summary"
]` and runs each stage gated by checkpoint existence. A `--resume_from`
flag skips completed stages. Each stage writes to a stage-specific
directory under `paradigm_shift/runs/run_<NNN>/`:

```
paradigm_shift/runs/run_001/
├── manifest.json
├── atoms/
│   ├── ATOM_*.json
│   └── _index.json
├── candidates/
│   ├── CAND_*.json
│   └── _index.json
├── scored/
│   ├── CAND_*.json   (with predicted_impact field added)
│   └── _index.json
├── stress/
│   ├── CAND_*.json   (with rag_grounding + self_consistency results)
│   ├── _rejected.json
│   └── _index.json
├── market/
│   ├── CAND_*.json   (with market_verifier verdict)
│   ├── _rejected.json
│   └── _index.json
└── summary.md
```

Web searches in Layer 5 and Layer 6 are wired through the orchestrator's
`web_search_hook`, which the agent invokes externally and writes
results to a `_search_cache.json` so re-runs of the stress/market
stages are deterministic.

---

## 8. Success criteria

Run 1 is **mechanism validation only** on the 5 existing TARI
transcripts. These transcripts are academic colloquium content
(researcher reporting *what they did*), which is the **wrong
distribution** for paradigm_shift_finder. Run 1's success criterion is
therefore:

**MV-1.** The 6 layers run end-to-end without crashing on the 5
transcripts.

**MV-2.** Layer 2 produces ≥1 atom of each new type (`prediction`,
`blocker`, `first_principle`, `analogy`, `open_problem`, `trend`) from
the academic transcripts. If a type yields 0 atoms, that is itself a
finding about the input distribution.

**MV-3.** Layer 5 rejects ≥1 candidate by either `RAG_UNGROUNDED` or
`UNSTABLE_FIRST_PRINCIPLES`. If Layer 5 passes everything, the
RAG/self-consistency check is rubber-stamping.

**MV-4.** Layer 6 marks the run's final candidates (if any). Whether
`SURVIVES_MARKET_CHECK` is 0 or >0, the verdict is recorded with
citations.

**MV-5.** `impact_label_logger.py` produces a labeling prompt for
the user with the top-3 ranked candidates.

The **substantive** success criterion (applies starting Run 2, on tech-leader
vision content):

**S-1.** ≥1 candidate where (a) cross-field analogy passes the
first-principles RAG check, (b) `market_verifier` returns
`SURVIVES_MARKET_CHECK`, and (c) `poc_tractability` ≥ 0.6 (solo
founder buildable).

Honest expectation for Run 1: S-1 is **not** expected to be met on
academic transcripts. The mechanism is being validated; the input
will be replaced for Run 2.

---

## 9. Comparison plan vs. TARI

After Run 1, `design/paradigm_shift_vs_tari.md` answers:

1. **Does first-principles RAG reject candidates TARI accepted?**
   Cross-reference TARI run_002's audit-PASS candidates against
   paradigm_shift_finder's Layer 5 verdicts on equivalent atom pairs.

2. **Does atom-type tagging produce different candidates than TARI's
   untyped extraction?** Compare the candidate distribution by source
   atom type. If `paradigm_shift_finder` candidates all come from
   `MECHANISM_CLAIM`-shaped atoms (TARI's untyped majority), the new
   typing was descriptive, not generative.

3. **Per atom-type productivity:** which type produces the most
   surviving candidates? If `prediction` × `first_principle` produces
   0 surviving candidates on academic transcripts (likely), the
   distribution-shift hypothesis is supported.

---

## 10. Open design questions deferred to Run 2+

- **DQ-1.** How to source longitudinal tech-leader corpora at scale
  without copyright friction. Run 1 ships with academic transcripts;
  Run 2 needs a curated tech-leader pool.
- **DQ-2.** How to handle predictions that have already materialized
  ("Sam Altman in 2018 said X; X is now true"). These should be
  filtered out, not used as candidates.
- **DQ-3.** Whether to add a 7th layer (`team_match`) that checks the
  candidate against the user's own background. Deferred to v2.
- **DQ-4.** Replacing the heuristic noun-phrase matcher in §5.3 with a
  better extractor (current matcher is the same precision-biased regex
  family as TARI's PRIMITIVE patterns).

---

## 11. What this design does NOT promise

- It does not promise a substantive PASS on Run 1.
- It does not promise that the RAG grounding check catches all hallucination.
- It does not promise that the impact classifier becomes useful within
  N runs without sufficient labels.
- It does not promise that academic colloquium content can ever produce
  paradigm-shift candidates (we expect it cannot, and Run 1 will test that).

The promise is: **the 6 layers will produce data we can use to falsify
each of the above.** That is the rigor mechanism.
