# Paradigm-Shift Finder — Run 5 vs Run 6

> Comparison memo. Run 6 introduces three anti-hallucination interventions —
> transcript purifier, live web_search at Layer 5, and arXiv citation
> requirement per sub-claim — and re-runs on the full 13-transcript corpus.

## Honest framing of the "Run 5" baseline

The repository has no on-disk `run_005`. Only `run_001` (10 candidates) was
committed before this branch. "Run 5" in this memo refers to a
**Run-5-equivalent baseline** I generated for direct comparison: same
pipeline as Run 1, but widened to 27 candidates by raising
`max_per_operator` to 14 and allowing intra-transcript pairing. The
baseline is stored under
`paradigm_shift/runs/run_006/run_5_equivalent_baseline/candidates_27/`
so the comparison is reproducible.

## Headline numbers

| Stage | Run 5 (equiv. baseline) | Run 6 |
|-------|-------------------------|-------|
| Transcripts | 5 academic | 13 (5 academic + 8 tech-leader) |
| Tech-leader transcripts purified | 0 | 8 (T007–T014, spaCy) |
| Paradigm atoms total | 264 | 734 (+178%) |
| Atoms in T007 + T012 + T014 | 1 (raw) | 135 (purified) |
| Candidates generated | 27 | 40 |
| Live web_search calls | 0 (cache-only) | 32 (real WebSearch emissions across phases 2, 4, 5) |
| Sub-claims gated by arXiv | n/a | 236 across Run-5-eq + Run-6 |
| Run 5 survivors after gate | 21 / 27 | n/a (gate retro-applied) |
| Run 6 survivors after gate | n/a | 14 / 40 |

## What changed

### 1. `paradigm_shift/transcript_purifier.py` (new, spaCy)

YouTube auto-captions arrive as one lowercase stream with no sentence
punctuation. The existing `snippet_decomposer` relies on
`[.!?]\s+[A-Z]`, so a raw transcript collapses into a single mega-snippet
and the regex atom extractor finds almost nothing.

The purifier inserts sentence boundaries before strong discourse markers
("so", "but", "now", "okay", "and then", "you know", "I think", …) and
then refines with spaCy's dependency parser. It capitalises sentence
starts, stand-alone *i*, and strips the densest disfluencies.

Result on T007 / T012 / T014:

```
BEFORE PURIFICATION: 1 atom (T012 only)
AFTER PURIFICATION : 135 atoms across T007 (88), T012 (40), T014 (7)
Δ = +134
```

### 2. Live web_search at Layer 5 (replaces cached)

Run 1 / Run-5-equivalent shipped a `_search_cache.json` indirection so
the stress test could only see results an external loop had pre-fetched.
In practice it ran with an empty cache and rejected every candidate with
`FAIL_RAG_UNGROUNDED`.

Run 6 emits real `WebSearch` tool calls per unique sub-claim query — 32
of them across this branch (3 in Phase 2 + 19 in Phase 4 + 10 in
Phase 5). The cache is still used for de-duplication across candidates
that hit the same query, but every result it now holds was fetched
live in this session.

### 3. `paradigm_shift/arxiv_gate.py` (new)

A sub-claim is only **GROUNDED** if at least one of its supporting
search results is an arxiv.org URL with a parseable identifier
(`arxiv.org/abs/XXXX.XXXXX`, `…/pdf/…`, `…/html/…`, with optional
version). Blog posts, vendor pages, Substack, and Wikipedia citations
are rejected — they pass the original keyword-overlap heuristic but
provide no peer-review-style anchoring.

Per-sub-claim log line format:

```
{sub-claim} → arXiv:XXXX.XXXXX
{sub-claim} → NO_ARXIV_REJECT
```

The gate also requires keyword overlap ≥1 with the matched paper's
title or snippet, so an arXiv URL that's topically unrelated does not
spuriously accept the claim.

## Re-run of "Run 5"'s 27 candidates under the new rigor

| Verdict | Count |
|---------|-------|
| All sub-claims arXiv-grounded | 21 / 27 |
| ≥1 NO_ARXIV_REJECT sub-claim | 6 / 27 |
| Sub-claims accepted | 73 |
| Sub-claims rejected | 6 |

The 6 rejections concentrate in candidates that cite content tied to
named individuals or social-media artifacts ("Sasha mentioned on
Twitter", "Jake's hot take"). These query terms are unlikely to surface
arXiv papers on the actual underlying topic — the gate correctly fires.

## Run 6 results on the full purified 13-transcript corpus

| Verdict | Count |
|---------|-------|
| Candidates generated | 40 |
| Sub-claims total | 157 |
| arXiv ACCEPT | 86 (54.8%) |
| NO_ARXIV_REJECT | 71 (45.2%) |
| Candidates surviving (all sub-claims grounded) | **14 / 40** |
| Candidates rejected | 26 / 40 |

Surviving candidates: `CAND_run_006_011` … `CAND_run_006_024` (see
`paradigm_shift/runs/run_006/phase5_survivors.json`).

## What this comparison tells us

1. **The purifier moves the bottleneck from "no input" to "templated
   sub-claims".** Going from 1 → 135 atoms on three previously-mute
   transcripts unblocks the rest of the pipeline. The new bottleneck
   visible in Phase 5 is the heuristic decomposer producing sub-claims
   like *"the prediction in atom ATOM_T002_S051_PRE_01 is the
   resolution of the blocker in atom ATOM_T005_S032_BLO_01"* — those
   sub-claims are template-shaped, not knowledge-shaped, and live
   web_search can't ground them.
2. **The arXiv gate has bite.** It rejects 45% of Run-6 sub-claims, but
   only 6 of 73 Run-5-equiv sub-claims. The asymmetry is informative:
   the 8 tech-leader transcripts produce more sub-claims whose verbatim
   surface form doesn't map onto research-paper vocabulary, which is
   what Run 6 was built to surface.
3. **Hallucination cost dropped, recall dropped.** Run 5-equiv would
   have shipped 27 candidates downstream. Run 6 ships 14 — and the 14
   we ship come with concrete arXiv pointers, not free-text claims
   about "the principle of X".

## Open issues (Run 7 candidates)

- The heuristic decomposer still embeds atom-id template strings into
  sub-claims. A v2 decomposer should strip these before query
  construction so the live search hits substance instead of template
  filler.
- spaCy boundary recall is sentence-level. We are still over-segmenting
  at "and" / "because" inside genuinely long compound clauses. A
  per-transcript boundary calibration loop would help.
- The arXiv pool used for Phase 5 grounding is the 32-query pool from
  this session. A standing arXiv index (Semantic Scholar / arXiv API)
  would let every Run 6 sub-claim be checked against the full corpus
  rather than the live-search top-k.

## File map

| Phase | Path |
|-------|------|
| 1 — purifier | `paradigm_shift/transcript_purifier.py` |
| 1 — purified outputs | `paradigm_shift/runs/run_006/post_purify_T007_T012_T014/` |
| 1 — pre-purify baseline | `paradigm_shift/runs/run_006/baseline_pre_purify/` |
| 2 — live search log | `paradigm_shift/runs/run_006/phase2_live_search_log.json` |
| 3 — arXiv gate | `paradigm_shift/arxiv_gate.py` |
| 4 — Run-5-equiv candidates | `paradigm_shift/runs/run_006/run_5_equivalent_baseline/candidates_27/` |
| 4 — gate report | `paradigm_shift/runs/run_006/phase4_gate_report.json` |
| 5 — Run 6 candidates | `paradigm_shift/runs/run_006/full_purified/candidates/` |
| 5 — gate report | `paradigm_shift/runs/run_006/phase5_gate_report.json` |
| 5 — survivors | `paradigm_shift/runs/run_006/phase5_survivors.json` |
