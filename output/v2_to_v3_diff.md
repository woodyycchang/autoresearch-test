# v2 → v3 Diff

**Note on naming.** This diff is between `program_v2.md` (Form rotation +
query/composition rules; ran R026-R050 in epoch 2) and `program_v3.md`
(memory-aware; ran R051-R075 in epoch 3 after PR #3 conflict resolution).
The original PR #3 was authored when only R001-R025 existed, so it
described the diff against `program.md`; the lever changes themselves
are unchanged — only the round-id range is updated.

---

## 1. Summary

v3 adds one new step (04.5 memory check) and one persistent artifact
(`logs/memory_db.json`). The four ★ FORBIDDEN-TO-MODIFY zones (steps 06
web_search, 07 keyword threshold, 10 mechanical verdict, 12 cross-agent
verification) are preserved byte-for-byte.

## 2. Files added

| File | Purpose |
|------|---------|
| `program_v3.md` | New program spec; supersedes `program.md` for epoch 3 |
| `logs/memory_db.json` | Persistent failure memory; appended after step 10 each round |
| `rounds/round_NNN/04_5_memory_check.json` | Per-round record of memory queries (REJECT and ACCEPT attempts) |

## 3. Loop changes

```diff
  for step in [01, 02, 03, 04]:
      execute step
      verify output file matches schema
+ 
+ # Step 04.5 — memory query loop (v3 only)
+ memory_skip_count = 0
+ while True:
+     propose (domain_norm, mechanism_keywords, form)
+     load logs/memory_db.json
+     if rule_1_domain_skip fires OR
+        rule_2_keyword_skip fires OR
+        rule_3_form_rotate fires:
+         memory_skip_count += 1
+         append REJECT attempt to 04_5_memory_check.json
+         continue
+     append ACCEPT attempt; break
+ if memory_skip_count > 25: halt round, log impasse
  
  execute step 05 using (newly: accepted) proposal
  execute step 06 (★ FROZEN)
  execute step 07 (★ FROZEN)
  execute step 10 (★ FROZEN)
+ 
+ # Memory update (v3 only)
+ append round entry to logs/memory_db.json
+ re-compute aggregates
  
  execute step 11
  execute step 12 (★ FROZEN)
```

## 4. The three new rules

### Rule 1 — Domain saturation skip
- **Trigger:** proposed `domain_normalized` has ≥ 3 prior FAIL in memory.
- **Action:** REJECT, regenerate with a different domain.
- **Epoch 1 evidence:**
  - `molecular-cell-biology`: 5 prior fails (R002 autophagy, R011 CRISPR-Cas, R019 riboswitch, R021 ribosomal frameshifting, R022 prion templating). Mean forced_hit 6.8.
  - `chemistry-materials`: 3 prior fails (R006 Roman concrete, R010 Liesegang, R023 Ostwald). Substantive LLM-side prior art in every case.
  - `non-western-medicine`: 3 prior fails (R007 TCM pulse, R009 Ayurveda tridosha, R024 TCM meridian).
  - `indigenous-ethnoscience`: 3 prior fails (R004 songlines, R016 Inuit ice, R020 fire-stick).
- **Epoch 3 blocked at start:** the 4 buckets above.

### Rule 2 — Mechanism keyword overlap skip
- **Trigger:** any proposed `mechanism_keyword` substring-matches a keyword that appears in ≥ 2 prior `tried_keywords` lists.
- **Action:** REJECT, regenerate with new keywords.
- **Epoch 1 evidence:**
  - "Traditional Chinese Medicine" appeared in R007 content_words AND R024 content_words. Both FAILED with the keyword itself anchoring a forced-hit cluster of TCM source-domain pages.
- **Epoch 3 blocked at start:** `["traditional chinese medicine"]` (the only keyword with frequency ≥ 2 at start; list grows as epoch 3 adds entries).

### Rule 3 — Form rotation
- **Trigger:** proposed `form` has ≥ 5 prior FAIL.
- **Action:** REJECT, regenerate selecting from the least-used set.
- **Epoch 1 evidence:**
  - `memory-architecture`: 10 fails (40% of all R001-R025): R002, R004, R006, R009, R011, R014, R015, R020, R022, R023. Mean hit_count 12.2 — agent's strongest training-prior pull.
  - `evaluation-diagnostic`: 5 fails (R001, R005, R007, R013, R025). Mean forced_hit_count 6.4 — the highest per-form forced-hit average.
- **Epoch 3 blocked at start:** `memory-architecture`, `evaluation-diagnostic`.
- **Least-used target set for epoch 3:** `context-gating` (3), `activation-control` (3), `training-method` (2), `mechanism-import` (1), `multi-agent-comm` (1), plus the not-yet-used `runtime-repair`.

## 5. ★ FORBIDDEN-TO-MODIFY zones — preserved verbatim

| Zone | Status |
|------|--------|
| Step 06 web_search (≥2 queries, real URLs, RAW saved) | UNCHANGED |
| Step 07 threshold (`overlap ≥ 2` → forced hit) | UNCHANGED |
| Step 10 verdict (`total_hits ≥ 1` → FAIL) | UNCHANGED |
| Step 12 cross-agent verification (fresh agent, same schema) | UNCHANGED |

v3 changes only **which candidates are proposed**, never **how a
proposed candidate is judged**.

## 6. Stats schema delta

```diff
 {
   "rounds_completed": ...,
   "pass_count": ...,
   "fail_count": ...,
   ...,
+  "v3_memory_metrics": {
+    "memory_skip_count_total": 0,
+    "memory_skip_count_by_rule": {
+      "rule_1_domain_skip": 0,
+      "rule_2_keyword_skip": 0,
+      "rule_3_form_rotate": 0
+    },
+    "blocked_domains_at_epoch_start": [...],
+    "blocked_domains_at_epoch_end": [...],
+    "blocked_keywords_at_epoch_end": [...],
+    "blocked_forms_at_epoch_end": [...]
+  }
 }
```

## 7. Why these three rules and not others

Considered-and-rejected alternatives:

- **Rule: forced_hit_count > 5 in same content_words → reject keyword set.**
  Rejected because rule 2 already covers this with explicit keyword
  matching, and rule 2 is more legible to the agent at proposal time.
- **Rule: similar candidate_summary cosine-similarity to past round → reject.**
  Rejected because this requires an embedding model the agent does not
  have native access to within program.md instructions, and substring +
  domain-bucket coverage gives 80% of the benefit.
- **Rule: time since last test in same domain.** Rejected because the
  whole point of memory is that ALL prior tests in a saturated domain
  argue against another test; freshness within a still-saturated bucket
  is not informative.

## 8. Backward compatibility

The v3 file-chain is a strict superset of v2's. A round produced under
v3 contains everything a v2 round contains plus `04_5_memory_check.json`.
Tooling that consumed v2 rounds works unchanged on v3 rounds.

## 9. Failure modes v3 cannot help with

- Same-model RLHF bias making candidates systematically gravitate toward
  PASS framing. (v3 still trusts the agent's framing; the keyword rule
  and cross-agent verification at step 12 are the defense.)
- Adversarial candidate-laundering: an agent could propose a candidate
  whose keywords avoid the memory blocks but is semantically equivalent
  to a blocked candidate. Cross-agent verification (step 12, FROZEN) is
  the defense; v3 does not introduce a new one.
- Truly novel candidates being rejected because they share a domain
  bucket with previously-saturated cousins. This is a false-positive
  cost of rule 1. Mitigation: at impasse (memory_skip_count > 25), the
  round halts and is surfaced — the impasse rate itself is a thesis
  metric ("how often does memory disagree with the agent's instinctive
  proposal").
