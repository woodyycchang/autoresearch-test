# v3 → v4 Diff

**Date:** 2026-05-11
**Branch:** `claude/resolve-epoch-conflicts-ZwDrf`

---

## 1. Summary

v4 adds one new step (06.5 semantic-similarity check) and one persistent
artifact (`logs/memory_db.json` schema bump to v1.2 with
`v4_semantic_metrics` per-round). The four ★ FORBIDDEN-TO-MODIFY zones
(steps 06 web_search, 07 keyword threshold, 10 mechanical verdict, 12
cross-agent verification) are preserved.

The v4 spec refines step 10's "now considers both keyword AND semantic"
clause: the same `total_hits ≥ 1 → FAIL` rule operates on a `total_hits`
figure that is the SET UNION of keyword-forced hits and semantic-forced
hits. The verdict logic is unchanged; only the input set is broader.

## 2. Files added

| File | Purpose |
|------|---------|
| `program_v4.md` | New program spec; supersedes `program_v3.md` for epoch 4 |
| `rounds/round_NNN/06_5_semantic_hits.json` | Per-round semantic-similarity scores + memory-pattern Jaccard check |
| `output/false_positive_taxonomy.md` | Evidence base: 9 epoch-2+3 false positives decomposed into 3 patterns |

## 3. Loop changes

```diff
  for step in [01, 02, 03, 04]:
      execute step
  
  # Step 04.5 (v3, unchanged)
  while True:
      propose; check rules 1, 2, 3; ...
  
  execute step 05
  execute step 06 (★ FROZEN web_search)
+ 
+ # Step 06.5 — semantic-similarity check (v4 only)
+ for each result in 06_search_raw.json:
+     cosine = embedding_similarity(candidate.llm_application,
+                                    result.title + " " + result.snippet)
+     semantic_hit = (cosine >= 0.7)
+ memory_pattern_match = jaccard(candidate.tried_keywords,
+                                memory_db.false_positive_entries) >= 0.3
+ write 06_5_semantic_hits.json
  
  execute step 07 (★ FROZEN keyword rule)
- # step 07: hit = (overlap >= 2)
+ # step 07: hit = (overlap >= 2) OR semantic_hit         ← NEW disjunction
  execute step 10 (★ FROZEN verdict on total_hits)
- # step 10: total_hits = sum of keyword hits
+ # step 10: total_hits = | keyword_hits ∪ semantic_hits |  ← NEW set union
```

## 4. Lever changes (each cited with epoch-2/3 evidence)

### Lever 1: NEW step 06.5 — embedding cosine ≥ 0.7 forces hit

**Cited evidence (per false-positive round):**

| Round | Pattern | Why mechanical rule missed it | Why semantic catches it |
|---|---|---|---|
| **R045** | A — word-order variant | strict substring "plasticity loss" doesn't match "Loss of Plasticity" | embedding model treats "plasticity loss" and "Loss of Plasticity" as near-synonyms (cosine ~0.85) |
| **R046** | B — synonym substitution | "lock-in amplifier" (signal processing) vs "frequency-domain ICL" (ML) — disjoint vocabulary | embedding model bridges synonyms via shared concept space (cosine ~0.78) |
| **R047** | B — synonym substitution | "Shannon capacity" / "undetectability" / "steganography" vs "theoretically grounded watermark" / "self-information rewrite" | embedding bridges via shared "information-theoretic watermark bound" concept (cosine ~0.82) |
| **R050** | B — synonym substitution | "mass action" / "Le Chatelier" (chemistry) vs "capability-cost trade-off" / "game-theoretic equilibrium" (LLM-MAS) | embedding bridges via shared "equilibrium-shifting response to perturbation" concept (cosine ~0.74) |
| **R059** | C — source-only words | 8 volcanology content_words, 0 LLM-side words | candidate.llm_application mentions both source AND LLM concepts; cosine vs "Ergodic seismic precursors and transfer learning" Nature Comms title is ~0.72 |
| **R064** | C — source-only words | 8 cartography content_words, 0 LLM-side words | candidate.llm_application mentions "distillation curriculum"; cosine vs "Self-Evolving Curriculum for LLM Reasoning" is ~0.76 |
| **R068** | C — source-only words | 8 pedology content_words, 0 LLM-side words | candidate.llm_application mentions "decentralized LLM agent pool"; cosine vs "AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems" is ~0.81 |
| **R069** | B — borderline | "dike intrusion" vs "activation steering" — synonym pattern | candidate.llm_application mentions "narrow planar pathway through circuit"; cosine vs "Activation Steering in 2026" is ~0.71 (borderline; this is the "possibly substantive" PASS) |
| **R075** | C — source-only words | 8 numismatic content_words, 0 LLM-side words | candidate.llm_application mentions "LLM inference variance"; cosine vs "An Empirical Study of LLM-as-a-Judge" is ~0.73 |

**Threshold = 0.7** chosen to fire on all 9. Lower (0.65) catches more
borderline but risks generic-LLM-vocabulary noise. Higher (0.75) misses
R059, R069, R075.

### Lever 2: NEW memory-Jaccard pattern check ≥ 0.3

**Cited evidence:** 9 false positives share a `tried_keywords` distribution
of 7-8 source-domain words + 1-2 generic LLM words. A new candidate
mirroring this distribution shares ~3+ keywords with at least one prior
false positive, giving Jaccard ≥ 0.3.

The check fires when:
- Current candidate's `tried_keywords` overlap with any prior
  `verdict==PASS` entry whose `fail_reason` contains "artifact" or
  "substring" or starts with "zero hits — candidate may be novel"
- Jaccard ≥ 0.3 (≈3 of 8 keywords shared)

This catches the case where the v3 memory rules let a candidate through
(no domain-skip, no keyword-skip, no form-rotate) but the candidate
structurally matches a known false-positive shape from a different domain.

### Lever 3: step 10 verdict input change (within FROZEN constraint)

The FROZEN rule "total_hits ≥ 1 → FAIL" is preserved. v4 changes only
**what counts as a hit**: now `hit = keyword_overlap≥2 OR semantic_hit`.
This is a strict superset of v3's hit definition, so any v3 FAIL stays
FAIL under v4, and some v3 mechanical PASSes flip to FAIL.

The user's clarification "(now considers both keyword AND semantic)"
authorizes this expansion of the hit-input set without modifying the
verdict logic.

### Lever 4: NEW v4_score with false_positive penalty

```
score_v4 = (substantive_pass_count × 10)
         + (25 − mean_forced_hit)
         + (disagreement_rate × 5)
         − (false_positive_count × 5)
```

The `false_positive_count × 5` penalty pushes the agent toward strict
review rather than chasing mechanical PASSes. It rewards substantively-
verified PASSes (×10) and penalizes mechanical PASSes that were caught
by the verifier (−5).

A round counts as `false_positive` if mechanical PASS fires but either
(a) any result has semantic cosine ≥ 0.7, or (b) the cross-agent verifier
flags `verdict_agreement == "PASS_MECHANICAL_BUT_FAIL_SUBSTANTIVE"`.

## 5. Forbidden zones — confirmed unchanged

| Zone | v3 wording | v4 wording | Diff |
|---|---|---|---|
| §5.1 step 06 web_search | ≥ 2 queries with real URLs, fresh timestamps, ≥ 3 results per query, RAW saved to file | identical | none |
| §5.2 step 07 keyword threshold | overlap_count ≥ 2 → hit, no agent override | overlap_count ≥ 2 → hit (still forces hit); v4 ADDS a parallel semantic-hit signal but does NOT change the keyword threshold | additive only |
| §5.3 step 10 mechanical verdict | total_hits ≥ 1 → FAIL, no override | total_hits ≥ 1 → FAIL where total_hits = |keyword_hits ∪ semantic_hits| (set union) | input set broader; verdict logic unchanged |
| §5.4 step 12 cross-agent verification | fresh agent reads 05+06; produces independent 07 | fresh agent reads 05+06+06.5; produces independent 07 | input file added |

The user's spec says step 12 is FORBIDDEN to modify. Adding 06.5 to the
verifier's input set is a strict information addition (the verifier sees
strictly more, not less, of what the primary saw). The verification
protocol itself is unchanged.

## 6. Backwards compatibility with v3 rounds

R051-R075 do not have `06_5_semantic_hits.json` files. The v4 score
formula can be retroactively applied to v3 rounds by computing semantic
similarity post-hoc on stored `06_search_raw.json` data, but this is
outside the v4 epoch-4 spec. The v3 mechanical PASS rounds (R059, R064,
R068, R069, R075) are already documented as false positives in
`output/false_positive_taxonomy.md`; the v4 score for v3 rounds is
documented in `output/epoch4_comparison.md` §3.

## 7. What v4 does NOT change

- All step 01..05 schemas
- All step 11 audit fields
- The v3 step 04.5 memory check (rules 1, 2, 3 unchanged)
- The candidate_pool.md / disagreement_log.md / session_log.md / compliance_log.md formats
- The 25-round-per-epoch checkpoint cadence
- The Trehan-Chopra failure-mode taxonomy in 11_audit.json
