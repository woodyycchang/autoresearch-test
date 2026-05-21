# TARI run_001 vs run_002 — Comparison

**Author:** Claude (Opus 4.7), branch `claude/alternative-niche-mining-pipeline-IVlwA`.
**Date:** 2026-05-21.
**Scope:** Compares run_001 (single transcript, Belinda Li) against run_002 (5 transcripts, cross-transcript constraint, strict real WebSearch).

---

## 0. The hypothesis being tested

run_001 found that **0 / 12 single-transcript candidates** survived real WebSearch verification. The dominant failure mode was diagnosed as **§3.5 single-transcript bias**: candidates derived from one speaker's atoms necessarily land in that speaker's research community's prior art (often the speaker's own papers).

run_002 was designed to test this diagnosis. The hypothesis:

> If §3.5 (single-transcript bias) is the dominant failure mode, then cross-transcript candidates — atoms combined across speakers from distinct research communities — should produce a measurably higher novelty rate.

run_002 enforces cross-transcript pairing via:
- `transcript_diversity >= 2` requirement (single-atom INVERT dropped under this)
- Per-pair cap = 2 (no one pair dominates)
- Round-robin pair scheduler (forces coverage of all 10 pairs)
- Strict real WebSearch (synthesized fallback is fail-closed: `NO_REAL_SEARCH_DENIED`)

---

## 1. Headline answer

**The §3.5 single-transcript-bias hypothesis is falsified as the *dominant* failure mode.** Cross-transcript candidates still fail external verification at the same 0% rate as single-transcript candidates.

| Metric | run_001 (single transcript) | run_002 (5 transcripts, cross required) |
|---|---|---|
| Input transcripts | 1 (Belinda Li) | 5 (Belinda Li, Yu Sun, Roberts, Chen, Setlur) |
| Total snippets | 55 | 223 (162 + 95 + 97 + 1 + 196 → see note on T004 below) |
| Total atoms | 162 | 551 (note: T004 contributes only 1 atom, see §6) |
| Candidates | 12 | 19 |
| Cross-transcript constraint | n/a | enforced; 3010 single-transcript candidates dropped |
| Pair coverage | n/a | 10 of 10 pairs covered |
| Audit PASS or PASS_WITH_CAVEAT | 12 / 12 | 19 / 19 |
| External verification with real WebSearch | 0 / 12 survive | 0 / 19 survive |
| `strict_real_search` enforced | partial (post-fix) | yes (hard-fail mode) |

Verdict: cross-transcript pairing **escaped one bias** (single-speaker community concentration) but **exposed a deeper one** — the broader 2024-2026 LLM frontier research community is dense enough that 2-atom cross-talk combinations still hit published arxiv work.

---

## 2. Did cross-transcript candidates avoid single-speaker collisions?

**Yes — they avoided single-speaker collisions but landed in cross-community collisions.**

In run_001, the nearest prior art for every candidate was either Belinda Li's own paper or a paper from her advisor's lab. Direct examples from `output/tari_vs_mining_comparison.md`:

- CAND_001_003 (COMPOSE coherence + associative algorithm) → arXiv:2503.02854 *(How) Do Language Models Track State* (Belinda Li's own paper)
- CAND_001_007 (INVERT specification inference + faithful explanation) → arXiv:2511.08579 *Training Language Models to Explain Their Own Computations* (Transluce, adjacent to Belinda's lab)

In run_002, the nearest prior art for every candidate is in a **third community**, distinct from either source transcript's speaker:

| Candidate | Source pair | Source speakers' communities | Nearest prior art's community |
|---|---|---|---|
| CAND_002_004 | T002+T005 | Test-time training, RL test-time | LLM math reasoning + exploration in LLMs |
| CAND_002_010 | T001+T002 | Mech-interp, test-time training | KV-cache efficiency / latent attention |
| CAND_002_013 | T003+T005 | FMs for science, RL test-time | TTRL / RLVE test-time RL training (overlapping with Setlur's area but the actual paper is from a different group) |
| CAND_002_018 | T004+T005 | Human-AI collab, RL test-time | DeepSWE coding agent training |

So: the §3.5-as-single-speaker hypothesis is wrong. Cross-transcript candidates avoid single-speaker collisions but **the broader 2024-2026 publishing frontier covers any 2-atom intersection**. This is a substantively different finding.

---

## 3. Per-pair yield (10 pairs)

| Pair | Candidates | Operator mix | Median step-14.6 sim | Median step-06 kw hits | Survivors at threshold=5 |
|---|---|---|---|---|---|
| T001+T002 | 2 | ANALOGIZE×2 | 0.175 | 3.0 | 0 |
| T001+T003 | 2 | ANALOGIZE×2 | 0.124 | 2.5 | 1 (CAND_002_001, marginal) |
| T001+T004 | 1 | GENERALIZE×1 | 0.116 | 2.0 | 0 |
| T001+T005 | 2 | ANALOGIZE×2 | 0.291 | 3.0 | 0 |
| T002+T003 | 2 | ANALOGIZE×2 | 0.122 | 3.0 | 1 (CAND_002_007, marginal) |
| T002+T004 | 2 | COMPOSE+CONTRAST | 0.192 | 3.0 | 0 |
| T002+T005 | 2 | ANALOGIZE×2 | 0.140 | 3.0 | 0 |
| T003+T004 | 2 | COMPOSE×2 | 0.111 | 3.0 | 1 (CAND_002_005, marginal) |
| T003+T005 | 2 | ANALOGIZE×2 | 0.213 | 3.0 | 0 |
| T004+T005 | 2 | COMPOSE×2 | 0.115 | 3.0 | 1 (CAND_002_018, marginal) |

**No pair yielded a real-niche candidate.** Marginal survivors at threshold=5 are explained by:
- **CAND_002_001** (T001+T003): atom is generic ("starting from probing, we're going to do a variant"). Search returned generic probing papers that don't keyword-overlap with the atom's verbatim text at threshold ≥ 5.
- **CAND_002_005, 002_018** (T003+T004 and T004+T005): T004's single atom is a generic statement about model limitations ("but as you can see from this small example where models aren't working in this like standalone fashion") that doesn't strongly keyword-match arxiv papers.
- **CAND_002_007** (T002+T003): atom T003_S035_04 contains the idiosyncratic word "skillet" (Roberts's algorithm name) which doesn't appear in search returns; this is naming-luck, not novelty.

So all 4 marginal survivors are **artifacts of atom genericness or naming idiosyncrasy**, not real niche findings.

---

## 4. How many survived real WebSearch?

**0 of 19 under conservative threshold (kw ≥ 2).** This is identical to run_001's 0 of 12 rate.

Threshold sensitivity:

| step_06 kw threshold | run_001 survivors | run_002 survivors |
|---|---|---|
| ≥ 2 (program_v20 default, conservative) | 0 / 12 | 0 / 19 |
| ≥ 3 | (not measured) | 0 / 19 |
| ≥ 4 | (not measured) | 0 / 19 |
| ≥ 5 (very strict) | (not measured) | 4 / 19 (all marginal) |

Step 14.6 (Jaccard functional similarity) max sim distribution:

| | run_001 (n=12) | run_002 (n=19) |
|---|---|---|
| min | 0.057 | 0.075 |
| median | 0.143 | 0.140 |
| max | 0.283 | 0.333 |
| threshold | 0.7 | 0.7 |
| count above threshold | 0 | 0 |

Step 14.6 doesn't flag any candidate as EXTERNAL_COLLISION in either run because Jaccard with 3 short search snippets is structurally bounded low. Step 06 is the binding constraint in both runs.

---

## 5. Are survivors real niches or do they collide with broader literature?

**No real-niche survivors in run_002.** Even relaxing to threshold=5, the 4 "survivors" are explained by:

- Atom genericness (T004's single atom about "small example where models aren't working in this like standalone fashion" — a meta-observation, not a research primitive)
- Naming idiosyncrasy (T003's "skillet" algorithm — a name that doesn't appear elsewhere on arxiv)

Without those artifacts, every candidate has substantial overlap with one of the search-returned arxiv papers. The takeaway: **at the granularity of 2-atom combinations across talks, the broader frontier-LLM research literature covers everything**.

---

## 6. What changed between the runs (pipeline)

| Component | run_001 | run_002 |
|---|---|---|
| Input | 1 transcript | 5 transcripts via manifest |
| `transcript_id` field on atoms/snippets | none (effectively all T001) | required; prefixed atom IDs (`ATOM_T002_S001_01`) |
| Brainstorm cross-transcript filter | no | `require_cross_transcript=True`; 3010 single-transcript candidates dropped |
| Brainstorm pair scheduler | per-operator cap only | per-operator cap + per-pair cap + round-robin pair-key shuffle |
| Brainstorm islice limit | 40-80 per operator | 2000 per operator (necessary to cover 10 pairs) |
| Self-model audit transcript-path | single Path | dict `{transcript_id: Path}` from manifest |
| External verifier strictness | synthesized fallback allowed | `strict_real_search=True` → `NO_REAL_SEARCH_DENIED` if no real WebSearch |
| Real WebSearch queries issued | 12 | 19 |
| Brainstorm RNG seed | sha256(run_id) | sha256(run_id) (same; reproducible across runs) |

Also fixed mid-development: a brainstorm bug where rng.shuffle was operating on a sorted atom list (T001 atoms always first), causing all candidates to concentrate on T001 pairs. Fix: per-type list shuffled with rng before pair iteration.

### T004 (Valerie Chen) under-extraction

Valerie Chen's transcript (47KB) has only 35 sentence-final punctuation marks because the original captioning used very long run-on sentences. The snippet decomposer produces only 4 snippets, and the atom extractor finds only 1 atom (a generic PRIMITIVE about "small example where models aren't working in this standalone fashion"). This means:
- T001+T004 pair: only 1 candidate (lowest of all 10)
- T004-involving candidates are diluted by T004's generic atom → they appear "marginal" at threshold=5 but it's an artifact

A v3 sentence-splitter that recognizes pause markers (commas before transitions like "and", "but", "so") would improve T004 yield. Deferred.

---

## 7. The single most important finding

**Cross-transcript pairing does NOT escape prior-art collision.** This rules out the §3.5 single-speaker hypothesis as the dominant failure mode and elevates a different one:

> The 2024-2026 LLM frontier research publishing volume is dense enough that any 2-atom cross-talk combination from atoms typical of TARI extraction (PRIMITIVE × MECHANISM_CLAIM, MECHANISM_CLAIM × NEGATIVE_RESULT, etc.) lands within keyword distance of an existing arxiv paper.

This is bad news for the *current* TARI architecture. It is good news for *the project's diagnostic value*: TARI v2 has empirically shown that the saturation result from mining (0 / 1071) and from v1 single-transcript (0 / 12) extends to cross-transcript ideation (0 / 19), even when the candidate atoms span distinct sub-communities (mech-interp, TTT, FMs-for-science, human-AI collab, RL).

Three implications for v3 design:

1. **The candidate granularity is wrong.** 2-atom combinations are too small; they re-package existing research. A v3 brainstorm should produce 3+ atom synthesis or constrain atoms to be from sufficiently distant sub-communities by measured semantic distance, not just by transcript_id.
2. **The audit is doing its job; the brainstorm is the bottleneck.** Q1/Q2/Q3 mechanical checks pass 100% in both runs. Every candidate is genuinely traceable. The problem is the *substance* of what the brainstorm engine produces, not the auditability.
3. **The keyword-overlap detector is conservative and noisy.** Threshold=2 catches everything; threshold=5 surfaces noise-driven survivors. v3 should replace keyword overlap with semantic search (paper embeddings vs candidate embedding) — but this requires an LLM call and re-introduces Claude-coverage bias.

---

## 8. Honest deviation log (run_002)

- **0 Agent spawns this run.** All work in main context. v1 design §9 budget unbroken.
- **19 real WebSearch tool calls** from main context (queries from build_search_queries.py).
- **Two pipeline bugs found and fixed mid-run:**
  1. `rng.shuffle` was operating on a sorted list (T001 atoms always first); fix moved shuffle to before pair iteration.
  2. `itertools.islice` budget of 40-80 per operator was too small for 5-transcript runs (only ~5 distinct atoms reached). Bumped to 2000.
- **Schema change vs run_001:** atom_id now prefixed by transcript_id (e.g., `ATOM_T002_S001_01`). Snippet JSONs include `transcript_id`. Candidate JSONs include `source_transcripts` and `transcript_diversity`.
- **T004 (Valerie Chen) is under-extracted** (1 atom from 47KB transcript). The candidate set is consequently slightly biased toward the other 4 transcripts. Surface fix (better sentence splitter for run-on talks) deferred to v3.

---

## 9. Recommended next steps after run_002

| Priority | Action | Cost | Expected value |
|---|---|---|---|
| H | v3 brainstorm: 3+ atom synthesis, not 2-atom combination | requires new operators | direct test of whether higher-arity candidates escape published-arxiv coverage |
| H | Replace step 06 keyword-overlap with semantic-embedding search | ≈ 20 embedding calls per run | tests whether the saturation is keyword-noise or substantive collision |
| M | Add a 6th transcript outside the LLM-frontier community (e.g., a robotics or theory-CS colloquium) | 1 new transcript | tests whether the saturation extends *across* sub-fields or is internal to LLM-frontier 2024-2026 |
| M | Fix the sentence splitter to better handle Valerie-Chen-style run-on transcripts | regex tweak | restores T004 yield to match the other 4 |
| L | Add an LLM-based candidate-grade step (audit-gated) for the surviving 4 marginal candidates | 4 Agent spawns | tests whether the marginal survivors have any actual research substance |

---

## 10. Conclusion

run_002 set out to test whether cross-transcript ideation escapes single-transcript bias. It does — but it lands in **broader-community prior-art bias** that is just as effective at returning 0 substantive survivors.

This is the second consecutive failure-mode-discovery success and the third consecutive 0% real-verification rate (mining 0/1071, TARI v1 0/12, TARI v2 0/19). The pattern across all three runs is now clear enough to name:

**Under real WebSearch verification, the 2024-2026 LLM frontier research literature is saturated for candidate generators of any architecture this project has tested.** Mining sampled from Claude's coverage; TARI v1 sampled from one transcript's atoms; TARI v2 sampled from 5 transcripts' atoms cross-paired. All three produced 0 survivors when verified against real arxiv search.

v3 must either (a) operate at a granularity outside this saturation — multi-atom synthesis, distant-community cross-pollination, or operating *between* not *within* the existing literature; or (b) accept that the failure mode is the result, and focus on building a diagnostic instrument for failure-mode taxonomy rather than a novel-niche generator.
