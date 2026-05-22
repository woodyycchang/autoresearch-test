# Market Verifier v2 — Spec

**Author:** Claude (Opus 4.7), branch `claude/paradigm-shift-finder-EAtbj`.
**Date:** 2026-05-22.
**Status:** Phase 2 of Run 3.

Drop-in replacement for `paradigm_shift/market_verifier.py` (v1). v1 is kept
for reproducibility of Run 1/Run 2 verdicts; v2 is invoked by a new
orchestrator stage `market_v2`.

---

## 1. The four upgrades, codified

### A. Semantic similarity (replaces 3-content-word overlap)

**v1:** A "strong match" required ≥3 content-word overlap between candidate
primary phrase and search result title+snippet.

**v2:** For each search result, compute a similarity score against the
candidate's semantic anchor (defined below). Use TF-IDF cosine similarity over
content words on (anchor) × (title + snippet). Threshold for COLLISION:
`similarity ≥ 0.5` (configurable per-axis).

**Semantic anchor** for a candidate is the concatenation of:
- the candidate's `claim` (with template scaffolding stripped — see below),
- the verbatim_quote of each cited atom,
- the candidate's `first_principles_validity_hypothesis`.

Template scaffolding to strip from claim text before TF-IDF (regex):
- `Apply the analogical structure in atom \S+ \(".*?"\) to the open problem framed in atom \S+ \(".*?"\)`
- `The prediction in atom \S+ \(".*?"\) is the resolution of the blocker in atom \S+ \(".*?"\)`
- `apply the mechanism described in atom`, etc.

Stripping leaves the **atom-quoted content** as the semantic signal.

### B. Speaker self-publish check (NEW)

For each candidate:
1. Read the manifest at `paradigm_shift/runs/<run>/manifest.json` and look up
   the `speaker` field for each transcript in `source_transcripts`.
2. For each `(speaker, primary_keyword)` pair, issue a web_search query:
   `"{speaker} {primary_keyword} 2024 OR 2025 OR 2026"`
   where `primary_keyword` is the top content word from the semantic anchor.
3. For each returned result:
   - If the result title+snippet semantically matches the candidate (TF-IDF
     cosine ≥ 0.5 against semantic anchor),
   - AND the speaker's name appears in title+snippet+url (author-presence check),
   - then verdict = `COLLISION_SPEAKER_SELF` with citation.

Cache the speaker_publications lookup to
`paradigm_shift/speaker_publications_cache.json` so re-runs are deterministic
and the user can inspect what was found per speaker.

### C. Recent paper weight (NEW)

For each web_search result, attempt to extract a publication year using:
- `arxiv.org/abs/(\d{4})\.(\d{5})` → first 2 digits of MM/YY → year code
  (`2406` = June 2024, `2512` = Dec 2025, etc.)
- A `20(2[4-9]|3\d)` regex on title+snippet.
- Fallback: `null` (unknown date).

Date weight applied to similarity score:
- Last 12 months (≥ 2025-05): weight × **2.0**
- Last 13-24 months (2024-05 .. 2025-04): weight × 1.5
- Older / unknown: weight × 1.0

A high-similarity result from Yu Sun's December 2025 paper therefore counts
twice in the COLLISION check.

### D. Cross-LLM sanity check (NEW)

For the top-3 candidates by `predicted_impact` that **survive** Layer 6 v2,
generate a paste-ready prompt for an independent LLM (Gemini / GPT) and
append to `paradigm_shift/cross_llm_verify_queue.json`:

```json
{
  "queue": [
    {
      "candidate_id": "CAND_run_003_007",
      "prompt": "You are reviewing a paradigm-shift candidate identified by another LLM. The candidate claim is: <CLAIM>. The cited source atoms are: <ATOMS>. The candidate's first-principles hypothesis is: <HYPOTHESIS>. Question: Has this idea (or anything semantically equivalent) already been published in a paper, productized as a startup, or talked about publicly by the speaker themselves or another author between 2023 and 2026? If yes, cite the source. If no, briefly state why this would be novel and what kind of POC would test the hypothesis.",
      "generated_at": "2026-05-22T..."
    },
    ...
  ]
}
```

The user runs the prompt elsewhere, captures the answer, and either:
- Confirms novelty → keep the candidate.
- Reports collision → marks `CONFIRMED_COLLISION_BY_CROSS_LLM` in the labels file.

The cross-LLM check is **not** automated within v2; it's a human-in-the-loop
extension. v2 only generates the queue.

---

## 2. v2 verdict labels

```
SURVIVES_MARKET_CHECK_V2          - no collision found
FAIL_MARKET_EXISTS_V2_SEMANTIC    - semantic similarity >= 0.5 with any result
FAIL_MARKET_EXISTS_V2_SPEAKER     - speaker self-publish check hit
FAIL_MARKET_EXISTS_V2_BOTH        - both semantic AND speaker-self triggered
FAIL_NO_QUERIES                   - couldn't extract anchor (degenerate input)
PENDING_CROSS_LLM                 - candidate is in top-3 and queued for cross-LLM
                                    (still treated as surviving in the final tally
                                     until cross-LLM result comes back)
```

A candidate may carry both `SURVIVES_MARKET_CHECK_V2` and `PENDING_CROSS_LLM`
simultaneously — they are not mutually exclusive.

---

## 3. v2 implementation contract

`market_verifier_v2.verify_market_v2(candidate, search_fn, manifest, ...)`:
- Returns `MarketVerdictV2` dataclass with fields:
  - candidate_id, verdict, primary_keyword
  - semantic_anchor (the constructed anchor string)
  - speaker_collisions: list of `{speaker, paper_title, url, similarity, date_weight}`
  - semantic_collisions: list of `{title, url, similarity, date_weight}`
  - top_similarity (max across all checks, weighted)
  - cross_llm_queued (bool)

`market_verifier_v2.verify_all_v2(scored_dir, manifest_path, out_dir, search_fn, ...)`:
- Iterates over PASS_STRESS candidates.
- For each, builds queries (semantic + speaker-self), populates speaker cache,
  scores results, applies date weighting, emits MarketVerdictV2.
- Writes per-candidate JSON to out_dir, plus `_index.json` and `_rejected.json`.
- For top-3 survivors by predicted_impact, also writes
  `paradigm_shift/cross_llm_verify_queue.json` (appends, never overwrites).

`market_verifier_v2.retrospective_audit(run_dir, manifest_path, search_fn, out_path)`:
- Loads previous run's candidates from `<run_dir>/scored/`.
- Reuses already-cached search results in `<run_dir>/_search_cache.json` where
  possible; issues new queries via search_fn for what's missing.
- Writes a single JSON at out_path with per-candidate v1-vs-v2 verdict diff.

---

## 4. Computational cost

For 10 candidates × 4 speakers × 5 queries = up to 200 web_searches per run.
With cache, real cost ≈ 4 speakers × 5 queries = 20 fresh searches per run (we
reuse the existing `_search_cache.json` for any query we've already issued).

We will not exceed 50 fresh WebSearch calls in the entire Run-3 cycle.

---

## 5. What v2 does NOT change

- v1's `verify_market()` and `verify_all()` remain callable for legacy runs.
- v1's queries and verdicts in
  `paradigm_shift/runs/run_001/market/` and `paradigm_shift/runs/run_002/market/`
  are NOT rewritten — they're the historical record.
- v2 writes to a sibling directory `market_v2/` per run to keep the audit chain
  intact.

---

## 6. Honest limits (copied from `design/layer_6_failure_analysis.md` §4)

- Embedding model bias (we use TF-IDF, simpler but biased toward exact lexical
  forms; future v3 could switch to a sentence-transformer).
- Speaker-name extraction depends on manifest fidelity.
- Date parsing is heuristic and silently degrades to weight=1.0 on unknown.
- Cross-LLM is a manual loop, not a tight feedback loop.

These are the v2 contract's honest edges. They are documented up front; they
are not blockers for v2 deployment.
