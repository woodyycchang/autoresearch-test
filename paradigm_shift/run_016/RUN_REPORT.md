# Run 16 — epoch-wise parameter-improving niche pipeline

A persistent `direction_params.json` encodes "how to search/phrase well." Each
epoch a human labels which search directions were on-target vs diverge, and the
MAIN orchestrator nudges the params toward the on-target profile. **Per-epoch
success = measurable search-quality improvement (R12)**; niche-finding is the
long-run goal. Builds on the proven Run 15 loop (5 sequential subagents + MAIN).

## Epoch 1 (baseline) — result

| metric | value |
|---|---|
| **avg_search_quality (baseline)** | **0.5119** |
| search_quality_delta vs prev | `null` (no prior epoch — baseline) |
| niche verdict | `NICHE_NOT_FOUND` (0 survivors of 3) |
| determinism | OK (gate hash stable) |
| AGENT 3↔4 cross-check mismatches | 0 / 3 |
| hallucination check | clean (0 mismatches) |
| proof points | **7 / 7 PASS** |

`avg_search_quality = sum(param_k · dimension_mean_k) / sum(param_k)`, all params
= 0.5 this epoch, so it reduces to the plain mean of the five dimension means.

### Dimension means (the improvable signal)

| dimension | epoch-1 mean | reading |
|---|---|---|
| reformulation_specificity | 0.7262 | strong — queries are specific |
| mechanism_focus | 0.8333 | strong — queries name mechanisms |
| cross_domain_reach | **0.0000** | weak — every query stayed single-domain (ML only) |
| atom_source_diversity | 1.0000 | 3 atoms span distinct subdomains |
| collision_avoidance_phrasing | **0.0000** | weak — no prior-art-probing wording ("existing", "prior work", "survey"…) |

The two 0.0 dimensions are the honest, actionable finding of epoch 1: this epoch's
21 real queries had **no cross-domain reach** and **no collision-avoidance
phrasing**. These are exactly what the human-label step can push on.

## What ran (5 sequential subagents, each committed+pushed before the next)

| agent | output | commit | verified by MAIN |
|---|---|---|---|
| 1 sourcer | `atoms.json` — 3 arXiv atoms + 6 queries_used | `1ec489a9` | schema, text≥80, queries present |
| 2 merger | `candidates.json` — 3 Opus merges | `0a0798cd` (relabel `29823250`) | quotes re-verified as real substrings |
| 3 verifier | `verify.json` — 5 reformulations/candidate | `59f87c4e` | 15 non-empty queries, all collision=false |
| 4 cross-checker | `crosscheck.json` — 2 fresh re-searches/candidate | `4dc5a883` | **3/3 confirmed, 0 mismatch** (R7) |
| 5 scorer | `search_quality.json` — 21 queries scored | `c30cbc17` | re-ran deterministically, reproduced exactly |
| MAIN | gates + determinism + hallucination + param update | (this commit) | — |

The 3 candidates (cross-pairs of MoSA sparse-attention routing, GradPower gradient
transform, MemR3 reflective memory retrieval) all passed Gates 2/3/4 but failed
**Gate 1** (composite 0.45 < 0.90): each candidate's prior-art search surfaced
~22–24 paper-host results, flooring the novelty term. Honest **saturation-by-
density** rejection, cross-verified (not a single-paper collision) — same
mechanism observed in Run 15.

## Parameter update (R9/R10)

- `direction_params.json` persisted: `epoch 1 → 2`; epoch 1 appended to
  `epoch_history` with `avg_search_quality = 0.5119`.
- **No param nudge this epoch** (`param_nudges_last_update: {}`) — correct: there
  are no human labels yet. Labels are collected *after* epoch 1 (below) and drive
  the epoch-2 nudge.

## Proof points (7/7 PASS)
agents_all_committed · report_verbatim (`[REPORT 1..5]` verbatim) ·
four_gate_deterministic · cross_check_ran (AGENT 4 independent re-verify) ·
no_hallucination (real Opus summary vs ground truth, 0 mismatches) ·
search_quality_tracked · params_persisted. 16 offline tests pass.

## Honest notes
- **WebFetch returned HTTP 403** for arXiv again, so atom text is from real
  WebSearch snippets, not fetched abstracts (recorded in `atoms.json`). Verbatim
  Gate-4 grounding still holds: merge quotes are real substrings of the recorded
  atom text.
- AGENT 2's candidates were initially mislabeled `CAND_015_*` (merge-helper
  copy artifact); caught and relabeled `CAND_016_*` before downstream agents ran.
- AGENT 3 recorded some off-topic search drift verbatim (e.g. a power-systems /
  neuroscience hit) and correctly judged it non-colliding — honest, not hidden.

## How to read "success" here (R12)
Epoch 1 produces a **baseline** (0.5119); a delta only exists from epoch 2. The
pipeline "succeeds" per-epoch if avg_search_quality *rises* after the human-guided
param nudge. The verdict `NICHE_NOT_FOUND` is the long-run goal's status, not the
per-epoch metric.

## Next: human label step
See the labeling request in the session output — the human labels this epoch's 21
queries `on_target`/`diverge`; those labels populate `labeled_examples`, and
epoch 2's MAIN run nudges the params accordingly.
