# v6 → v7 Diff

**Author:** Claude (Opus 4.7) on branch `claude/epoch24-false-passes-v7-5DHwe`.
**Date:** 2026-05-14.
**Purpose:** Document the rollback of v6 step 06.8, the v7 addition of
step 11.5 (adversarial external verification), and the FORBIDDEN-zone
audit.

---

## Why v7 and not "fix v6"

### v6 rollback finding (Phase 0)

Epoch 24 (R576-R600) ran under v6 (`program_v6.md`). v6 added step
06.8, a per-paper-completeness LLM-judge layer that scored each
retrieved paper on whether it jointly covered all K candidate
sub-mechanisms. v6 reported 24/25 PASS with 96 pp Pattern E
mitigation.

Phase 0 spot-audit of R577 BEKTASHI-12-IMAM-DHIKR-CYCLE against
**HARPE — Hierarchical Adaptive Routing with Per-Expert prompts
(arXiv:2412.07171)** confirmed direct functional coverage of ALL
FIVE candidate sub-mechanisms under vocabulary substitution:

| R577 sub-mechanism | HARPE coverage |
|---|---|
| 12-imam canonical S_12 ordering | hierarchical expert ordering |
| Per-imam soft-prompt P_imam | per-expert prompt anchor vectors |
| 12-phase scheduler R_12 | adaptive routing scheduler over experts |
| Mursid-murid lineage M_lineage | teacher→student prompt-direction transfer |
| Zarif coherence L_zarif | prompt-direction drift regularizer across student fine-tunes |

v6 06.8 scored HARPE at **0.42**. True joint coverage is **5 of 5**
→ should score ≥ 0.85. The judge over-weighted vocabulary distance
(`12-imam` ≠ `per-expert`, `muršid/zarif` ≠ `teacher/regularizer`)
and under-weighted functional joint coverage.

**Generalization:** ANY candidate that re-clothes a known LLM
mechanism in fresh cultural vocabulary evades v6 06.8. All 25
R576-R600 PASSes are subject to this flaw and are marked
v6_false_positive=true in `logs/memory_db.json
epoch_24_summary.epoch_24_rollback_audit_2026_05_14`.

### Why not fix v6 06.8

Three options were considered:

- **Option A** (rejected): tighten v6 06.8 by reducing source-domain
  vocabulary weight. Requires the same LLM judge to internally
  ignore terminology — empirically unreliable on multi-feature
  composites where culture-specific terms (12-imam, zarif) anchor
  the embedding space.
- **Option B** (rejected): add a vocabulary-stripping preprocessor
  inside 06.8. The judge still sees the stripped candidate AND the
  full retrieved paper text together; the candidate's K-enumeration
  remains anchored to the original ordering and is still gameable
  by varying K.
- **Option C** (CHOSEN): externalize the adversarial pressure. Run
  a separate skeptical-reviewer agent with NO access to the
  candidate's source-domain framing, the primary's retrieved
  papers, or the cross-agent verifier's verdict. Force this agent
  to issue its own web_searches from multiple angles. v6 06.8 is
  REMOVED entirely; the v7 base reverts to v5.

Option C decouples the scoring layer (which the primary controls)
from the adversarial search layer (which an external agent controls).
The agent's search queries are anchored to the stripped functional
description only, so cultural vocabulary in the candidate cannot
propagate into search terms.

---

## What v7 ADDS (one new step)

```
v6: 01 → 02 → 03 → 04 → 04.5 → 05 → 06 → 06.5 → 06.7 →
    [06.8 per-paper-completeness] → 07 → 10 → 11 → 12

v7: 01 → 02 → 03 → 04 → 04.5 → 05 → 06 → 06.5 → 06.7 →
    07 → 10 → 11 → 12 → [11.5 adversarial external verification]
```

(Step 11.5 is named for naming-monotonicity with the file chain;
operationally it runs AFTER step 12.)

### Step 11.5 — Adversarial External Verification

**Trigger:** Only when step 10 PASS AND step 12 PASS.

**Action:**
1. Strip source-domain anchors from `candidate.llm_application` via
   regex on culture/folklore/form proper nouns and culture-specific
   anchor words. Preserve LLM artefact + K sub-mechanisms +
   novelty claim in LLM vocabulary.
2. Spawn fresh skeptical-reviewer agent (distinct agentId).
3. Give agent ONLY the stripped llm_application. NO access to:
   - source-domain framing
   - 06_search_raw.json
   - 06_7_functional_hits.json
   - 12_verification.json
4. Agent issues 3-5 web_searches from multiple angles
   (primary effect, synonym, secondary sub-mechanism,
   metaphor-free re-phrasing, closest known taxonomy).
5. Agent returns papers_found with functional_similarity scores.
6. `adversarial_hit = (max_functional_similarity >= 0.7)`.

**Output:** `11_5_adversarial.json` with raw skeptical output + meta.

**v7 verdict:**
```
v7_verdict = PASS               if step_10_PASS AND step_12_PASS AND NOT adversarial_hit
           = FAIL_ADVERSARIAL   if step_10_PASS AND step_12_PASS AND adversarial_hit
           = FAIL               otherwise
```

---

## What v7 REMOVES

- **v6 step 06.8 per-paper-completeness scoring.** v7 rounds MUST
  NOT write `06_8_per_paper_completeness.json`. If present, the
  round is malformed and flagged for re-run.
- **v6 verdict-driver semantics.** v7 reverts step 10 to the FROZEN
  v5 rule: `total_hits ≥ 1 → FAIL`. v6's verdict-path divergence
  (where 07_hit_miss.json was forensic-only and 06_8 drove the
  verdict) is reverted.

---

## What v7 PRESERVES VERBATIM (★ FORBIDDEN-TO-MODIFY)

All four FROZEN zones from v5 are preserved EXACTLY:

| Zone | v5 | v6 | v7 |
|---|---|---|---|
| Step 06 web_search | ★ FROZEN | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 07 keyword threshold ≥ 2 | ★ FROZEN | ★ FROZEN | ★ FROZEN (UNCHANGED) |
| Step 10 mechanical verdict | ★ FROZEN | DIVERTED via 06.8 | ★ FROZEN (RESTORED to v5) |
| Step 12 cross-agent verification | ★ FROZEN | ★ FROZEN | ★ FROZEN (UNCHANGED) |

The user-explicit FORBIDDEN list:
- step 06 web_search → preserved
- step 07 keyword threshold ≥ 2 → preserved
- step 10 mechanical verdict → preserved (and restored from v6
  divergence)
- step 12 cross-agent verification → preserved

---

## Scoring formula change

```
v6: score_v6 = (substantive_pass × 10)
             + (25 − mean_per_paper_completeness_hit)
             + (verdict_alignment_rate × 5)
             − (false_positive × 5)

v7: score_v7 = (confirmed_substantive_pass × 10)
             + (25 − mean_forced_hit)
             + (disagreement_rate × 5)
             − (false_positive × 5)
             − (adversarial_hit_count × 10)        ← NEW v7 term
```

The new `− (adversarial_hit_count × 10)` term is the score-level
expression of v7's design principle: adversarial verification is the
highest-authority signal and a single adversarial hit cancels a
substantive PASS.

`confirmed_substantive_pass` under v7 requires ALL of:
- keyword overlap < 2 across all results, AND
- semantic cosine < 0.7 across all results, AND
- functional judge < 0.7 across all results, AND
- verifier confirms substantive PASS, AND
- skeptical-reviewer finds 0 papers at functional similarity ≥ 0.7.

---

## Calibration evidence

### R577 retrospective replay (would have caught v6 false positive)

Stripped llm_application: "LLM phase-coherence mechanism with
K-canonical sequence ordering + K per-element frozen soft-prompts +
K-phase round-robin scheduler + master-student lineage weight-delta
along K prompt directions + cross-finetune prompt-direction drift
regularizer."

Predicted skeptical-reviewer search queries:
1. "hierarchical per-expert prompt anchor LLM"
2. "phase-locked router K experts soft-prompt"
3. "teacher-student prompt-direction transfer drift regularizer"
4. "canonical K-ordered expert routing soft-prompt"
5. "prompt-direction drift regularization fine-tuning"

Query 1 surfaces HARPE (arXiv:2412.07171) directly. Functional
similarity 0.85+ → adversarial_hit = true → v7 verdict =
FAIL_ADVERSARIAL.

Predicted v7 behavior on R576-R600 retrospective replay: ~80-100%
flip from v6 PASS to v7 FAIL_ADVERSARIAL.

### R279 PTCH as positive-control

R279 is the strongest niche candidate in corpus (triple-audited
UNCERTAIN). Phase 2 of the v7 branch runs step 11.5 on R279. If
R279 survives (adversarial_hit = false), upgrade UNCERTAIN →
CONFIRMED. If R279 fails (adversarial_hit = true), downgrade with
documented prior art. See `output/r279_adversarial_audit.md`.

---

## Migration plan

- R576-R600 marked v6_false_positive=true (Phase 0, completed).
- R601-R625 runs under v7 in epoch 25 (Phase 3).
- v6 06.8 prompt files preserved in rounds/round_576/ ... rounds/round_600/
  as forensic record (NOT deleted), but ignored for v7 verdict purposes.
- memory_db.json updated with v7_adversarial_metrics field and v7_verdict
  field per round in epoch 25.

---

## What v7 explicitly does NOT promise

- v7 does NOT promise more substantive PASS verdicts. v7 promises
  only that any PASS which DOES occur has survived adversarial
  external verification.
- v7 does NOT promise 0 false positives. A candidate whose
  functional composition is genuinely not yet published will pass
  all three verifiers; the retrieved literature may simply have not
  caught up. v7 minimizes the vocabulary-obfuscation failure mode,
  not the time-lag failure mode.
- v7 does NOT re-litigate the 696-round 0-substantive-PASS
  saturation result. The structural claim — that the niche-mining
  generator has reached p ≈ 0 on 1%-novelty H₀ — stands.
