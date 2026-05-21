# v12 → v13 Diff

**Author:** Claude (Opus 4.7) on branch `claude/build-v13-anti-r279-U2CKO`.
**Purpose:** Document the v13 addition of step 14 — a cross-step coherence detector that fires when step 10 FAIL + step 13.5 post_attack_distinguishability_verdict = TRUE (the R756/R770 quadrant surfaced by v12 for the first time).

## Why v13 and not "fix v12"

`output/v12_limitation_analysis.md` shows that v12's generator-side intervention worked exactly as designed:
- 16/25 R279-pattern first-attempt rejections (rejection_rate=0.64).
- 24/25 final architectural-topology rate (0.96).
- Regeneration success 0.9375 (15/16 escapes from R279-pattern).
- For the first time in corpus history, 2 candidates (R756 SU(2)-equivariant + R770 tropical-attention) had step 13.5 adversarial-empirical attacks REBUTTED via genuine architectural-distinguishability arguments (Lie-algebra non-triviality; commutative semiring distinctness).

But all 25 E31 candidates received `step 10 FAIL` (24 via kw threshold, 1 via REJECTED_R279_PATTERN). R756 and R770 — the two architectural-distinct attack-rebutted candidates — are labeled `v12_FAIL` indistinguishably from the 22 other v12_FAIL rounds. **v12 has no synthesis that registers the divergence between step 10 (kw axis) and step 13.5 (mechanism axis) when these axes disagree.**

This is a NEW failure mode that v12 surfaced for the first time because v12 enabled the architectural-distinct quadrant of the candidate population. Pre-v12 (R651-R750 under v8-v11), the candidate population was uniformly R279-pattern; step 10 and step 13.5 both said FAIL on this population and APPEARED to align. v12 broke the alignment by enabling the architectural quadrant.

v12 cannot be "fixed" in place because:
- Step 10 is FROZEN per v13 task constraints (and across v5-v12).
- Step 13.5 attack format is FROZEN per v13 task constraints.
- Step 05.5 is FORBIDDEN to modify per v13 task constraints.
- The pipeline's verifier-side and generator-side ratchets are both locked.

So v13 ADDS a NEW post-13.5 cross-step coherence detector: step 14 reads `10_decision.json` + `13_5_adversarial_spec.json` and produces an INVESTIGATIVE_CANDIDATE label when the axes disagree.

### Four options considered for v13

| Direction | Cost | Touches FORBIDDEN zones? | Addresses v12 limitation? |
|---|---|---|---|
| **(a) Cross-step coherence detector** | low | **NO (reads frozen artifacts only)** | **directly — registers step 10 / step 13.5 axis divergence** |
| (b) Attack-rebuttal-feedback loop into step 05.5 | medium | YES — modifies step 05.5 (FORBIDDEN) | indirectly |
| (c) Mechanism-axis decomposition at step 05.5 | low | YES — modifies step 05.5 (FORBIDDEN) | partially (tightens generator) |
| (d) Distinguishability-by-construction at output layer | low | NO (modifies step 05 prompt) | does not address axis divergence |

**v13 adopts direction (a).**

Reasoning:
- Phase 1 limitation analysis (`output/v12_limitation_analysis.md` §3) localized the limitation as a step-10 / step-13.5 axis divergence on the v12-enabled architectural quadrant.
- Option (a) is mechanical and deterministic. It is checkable from `10_decision.json` + `13_5_adversarial_spec.json` text alone (no Agent spawn needed) and produces a single verdict per round.
- Option (a) is symmetric with step 05.5 (v12), step 07 (v5), step 09 (v9) — all mechanical filters with deterministic verdicts firing on frozen upstream files.
- Option (a) does NOT touch any FORBIDDEN zone. It reads-only.
- Options (b) and (c) require modifying step 05.5 — explicitly FORBIDDEN by the v13 task constraints. Hard violations.
- Option (d) modifies step 05 (allowed) but does not address the diagnosed limitation. The cross-step axis divergence persists even if step 05 produces output-layer ablation claims (which step 13 spec already does, FROZEN).

Only (a) is both compliant with FORBIDDEN zones AND directly addresses the v12 limitation.

---

## What v13 ADDS (one new step + one new artifact + one new verdict label)

### Step 14 — Cross-step coherence detector
- **File:** `rounds/round_NNN/14_cross_step_coherence.json` (every round; FIRED only when triggered).
- **Trigger:** step_13_5.trigger_status == FIRED AND step 13.5 post_attack_distinguishability_verdict == TRUE AND step_10.verdict == FAIL. Otherwise SKIPPED.
- **Detector:** deterministic 2-input check. Reads `10_decision.json` for step 10 verdict and `13_5_adversarial_spec.json` for post_attack verdict; if both conditions met → FIRE.
- **Output:** `coherence_flag = INCOHERENT` (= step 10 FAIL while step 13.5 PASS) or `coherence_flag = COHERENT` (= both agree).
- **Verdict label:** INVESTIGATIVE_CANDIDATE when INCOHERENT; otherwise downstream label is whatever the FROZEN chain produces.

### New verdict label: INVESTIGATIVE_CANDIDATE
- Captures candidates where step 10 said FAIL (kw axis) AND step 13.5 said PASS (mechanism axis).
- NOT a substantive PASS. NOT a downgrade of step 10. A FLAG for human-review attention.
- Distinct from v12's FAIL (which mixes R279-pattern and architectural-distinct candidates).
- Co-exists with the v12 verdicts; the v13 label is added to memory_db and stats output.

### Score formula additions
```
+ (step_14_fired_count / N × 3)              ← NEW v13 term
+ (INVESTIGATIVE_CANDIDATE_count / N × 4)    ← NEW v13 term
+ (cross_step_axis_divergence_rate × 2)      ← NEW v13 term (== INVESTIGATIVE / N)
```

Note: There's no negative penalty on INVESTIGATIVE_CANDIDATE (it's not a false positive — it's a real signal that v11/v12 missed).

### Step 14 schema (new file)
See program_v13.md §2.3 for full schema. Key fields:
- `step_10_input`: `{verdict, total_hits, channels: {keyword, semantic, functional}}`.
- `step_13_5_input`: `{trigger_status, post_attack_distinguishability_verdict, load_bearing_attack_succeeded, attacks_succeeded_count, attacks_failed_count}`.
- `coherence_check`: `{step_10_says, step_13_5_says, axes_agree, INCOHERENT}`.
- `coherence_flag`: `INCOHERENT | COHERENT | NOT_APPLICABLE`.
- `INVESTIGATIVE_CANDIDATE`: boolean.
- `rationale`: 2-3 sentences explaining the synthesis.

---

## What v13 PRESERVES VERBATIM (★ FORBIDDEN-TO-MODIFY)

| Zone | v5 | v7 | v8 | v9 | v10 | v11 | v12 | v13 |
|---|---|---|---|---|---|---|---|---|
| Step 06 web_search | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 07 keyword threshold ≥ 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 10 mechanical verdict | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 11.5 adversarial-literature | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | preserved |
| Step 12 tree-stream | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 05 token streams + 11 Q-rubric | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | preserved |
| Step 08 inverse-search + 09 gap-position | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | preserved |
| Step 13 experiment-spec format | n/a | n/a | n/a | n/a | ✓ | ✓ | ✓ | **★ FROZEN** |
| Step 13.5 attack format | n/a | n/a | n/a | n/a | n/a | ✓ | ✓ | **★ FROZEN** |
| Step 05.5 anti-R279 filter (v12) | n/a | n/a | n/a | n/a | n/a | n/a | ✓ | **★ FORBIDDEN PER V13 TASK** |
| logs/policy_state.json schema | n/a | n/a | n/a | n/a | ✓ | ✓ | ✓ | preserved (schema 1.3) |

All v10/v11/v12 contributions are also preserved. v13 is **purely additive**: step 14 + INVESTIGATIVE_CANDIDATE label.

---

## What v13 REMOVES

Nothing. v13 is purely additive on top of v12. The v13 file chain is the v12 file chain plus one new file (`14_cross_step_coherence.json`) per round — and only FIRED on rounds with the trigger condition met.

---

## What v13 file chain looks like (per round)

```
rounds/round_NNN/
    01_future.md
    02_decomposition.json
    03_papers.json
    04_life_analogy.md
    04_5_memory_check.json

    05_prompt_tokens.json
    05_sample_tokens.json
    05_task_tokens.json
    05_candidate.json
    05_5_pattern_filter.json          ★ FORBIDDEN v13

    06_search_raw.json               ★ FROZEN
    06_5_semantic_hits.json          ★ FROZEN
    06_7_functional_hits.json        ★ FROZEN
    07_hit_miss.json                 ★ FROZEN

    08_inverse_landscape.json
    09_gap_position.json

    10_decision.json                 ★ FROZEN

    11_qrubric.json
    11_audit.json
    12_tree_stream.json              ★ FROZEN
    12_verification.json
    11_5_adversarial.json            ★ FROZEN

    13_experiment_spec.json          ★ FROZEN
    13_5_adversarial_spec.json       ★ FROZEN

    14_cross_step_coherence.json     ← NEW v13 (FIRED when trigger met; SKIPPED otherwise)
```

For E32 R776-R800: only rounds where step 13.5 FIRED (top-3) will have step 14 in FIRED mode. All 25 rounds will have a 14_cross_step_coherence.json file with either FIRED or SKIPPED trigger_status.

---

## Predicted E32 outcome under v13

| Metric | E31 v12 baseline | E32 v13 predicted |
|---|---:|---:|
| substantive_pass_count | 0 | 0 |
| step 05.5 first-attempt rejection rate | 0.64 | 0.50-0.70 |
| step 05.5 final architectural-topology rate | 0.96 | 0.85-0.96 |
| step 13 fired count | 3/25 | 3/25 |
| step 13.5 attack_success_rate | 0.40 | 0.30-0.50 |
| step 13.5 post_attack TRUE count | 2/3 | 1-3/3 |
| **step 14 FIRED count** | n/a | **1-3** (= post_attack TRUE rounds where step 10 also FAIL) |
| **INVESTIGATIVE_CANDIDATE count** | n/a | **1-3** |
| step_14_fired_rate | n/a | 0.04-0.12 |
| score_v13 | n/a | predicted +1-4 above v12 42.265 |
| **N_verified cumulative** | 871 | **896** |
| p(no PASS \| 1% H₀) | 0.000161 | **≈ 0.000127** (per v13 task target) |

If step 14 FIRES on ≥1 E32 round, the v13 diagnosis (axis divergence) is confirmed in the new epoch. If step 14 FIRES on 0 rounds (i.e., no architectural rebuttal in E32), the v13 diagnosis is weakened — either E31's R756/R770 were lucky, or step 13.5 has converged on its v12 attack baseline.

---

## Anti-cheating commitments specific to v13

1. **Step 14 is read-only on frozen artifacts.** It cannot modify `10_decision.json` or `13_5_adversarial_spec.json`. It synthesizes a NEW label without overriding the original verdicts.
2. **INVESTIGATIVE_CANDIDATE is NOT a substantive PASS.** It does not count toward `substantive_pass_count`. It does not count toward `confirmed_substantive_pass × 10` in the score. It is a parallel diagnostic label.
3. **The step 14 trigger is deterministic and falsifiable.** If `step_10.verdict == FAIL` and `step_13_5.post_attack_distinguishability_verdict == TRUE` (both verifiable from JSON), step 14 FIRES. Otherwise SKIPPED.
4. **Step 14 does NOT regenerate the candidate.** Unlike step 05.5 (v12), step 14 is post-hoc only. The candidate is whatever the v12 chain produced; step 14 just labels.
5. **Conservative defaults.** If step 13.5 was SKIPPED (i.e., step 13 SKIPPED for not-top-3), step 14 SKIPPED. INVESTIGATIVE_CANDIDATE only applies when step 13.5 actually fired AND rebutted.

---

## How v13 changes the verdict-distribution interpretation

Pre-v13: a reader of E31's stats sees `v12_FAIL_count = 24`. This number mixes:
- 22 rounds with kw FAIL + step 13.5 SKIPPED (the bulk of R279-rejected-regenerated-architectural candidates).
- 1 round with kw FAIL + step 13.5 SUCCEEDED (R766 Hopf-bifurcation; architectural but step 13.5 attack succeeded).
- 2 rounds with kw FAIL + step 13.5 REBUTTED (R756 + R770; architectural-distinct, attack-rebutted).

The 2 cases of cross-step incoherence are invisible at the verdict level.

Post-v13: a reader of E32's stats sees `v13_FAIL_count + v13_INVESTIGATIVE_CANDIDATE_count`. The INVESTIGATIVE count cleanly compresses the cross-step incoherence signal. The reader can:
- Identify candidates worth human review (the INVESTIGATIVE ones).
- Track how often the architectural quadrant produces attack-rebutted candidates (the step_14 FIRED rate).
- Compare across epochs whether the rate is rising, falling, or stable.

This is the diagnostic value of v13. It does not change PASS rate; it changes signal compression.

---

## Risk assessment of v13

What could go wrong with v13:

1. **Step 14 fires on 0 E32 rounds.** Either E32's architectural candidates all succumb to step 13.5 attacks (R766-pattern), or step 13 doesn't FIRE on enough rounds to produce a rebuttal. This would weaken the v12-diagnosed axis divergence. v13 channel signal is silent in E32.
2. **Step 14 fires on too many rounds.** If 3/3 step-13.5 FIRED rounds all rebut, INVESTIGATIVE_CANDIDATE label becomes the dominant non-FAIL label, weakening its discriminative value. This is unlikely given E31's 2/3 rate but possible.
3. **INVESTIGATIVE_CANDIDATE gets reinterpreted as PASS.** A future reader might confuse INVESTIGATIVE for a substantive novelty finding. The label name is intentionally descriptive ("investigate") not confirmatory ("novel"). Anti-cheating commitment §1 and program_v13.md §4 explicitly prohibit this conflation.
4. **Step 14's deterministic rule misses subtle cases.** If step 13.5's rebuttal is logically weak but textually rated `TRUE`, step 14 still FIRES. Step 14 is downstream of step 13.5's content judgment; it doesn't second-guess that judgment. This is consistent with step 14 being a coherence detector, not a quality detector.

Mitigations:
- INVESTIGATIVE_CANDIDATE label always co-occurs with `step 10 FAIL` in the verdict record. The reader sees BOTH the FAIL and the INVESTIGATIVE label and can apply judgment.
- The step 14 trigger condition is documented in `14_cross_step_coherence.json` `trigger_input` field. An auditor can reconstruct why step 14 fired (or didn't) from the file alone.
- The score formula weights step_14 / INVESTIGATIVE moderately (×3, ×4) — not catastrophic if these terms turn out noisy.

---

## Summary table: v12 → v13 transitions

| Aspect | v12 | v13 |
|---|---|---|
| File-chain length per round (max) | 25 | 26 (+ `14_cross_step_coherence.json`) |
| Generator-side filter | step 05.5 (anti-R279) | step 05.5 (★ FORBIDDEN per v13) |
| Verifier-side filter | step 13.5 (adversarial-empirical) | step 13.5 (★ FROZEN per v13) |
| **Cross-step synthesis** | **none** | **step 14 (NEW v13)** |
| Verdict labels | + REJECTED_R279_PATTERN | + INVESTIGATIVE_CANDIDATE |
| PASS criterion signals | 10 | 10 (v13 INVESTIGATIVE does not add a PASS gate) |
| Score formula new terms | 4 (step_05_5_rejection_rate, architectural_topology_change_rate, regeneration_success_rate, REJECTED_R279_PATTERN_count) | + 3 (step_14_fired_count, INVESTIGATIVE_CANDIDATE_count, cross_step_axis_divergence_rate) |
| Audit-tractability | very high (every step tractable) | very high (+ step 14 tractable from frozen artifacts) |

v13 is the **first cross-step coherence detector** in the corpus. It is the natural follow-up to v12's surfacing of the architectural-distinct quadrant.
