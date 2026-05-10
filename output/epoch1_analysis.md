# Epoch 1 Analysis (Rounds 1–25)

## 1. Headline numbers

- Rounds completed: 25
- PASS count: 0
- FAIL count: 25
- mean_forced_hits_per_round: **4.6** (median 3; max 17 R005 / R017)
- Disagreement rate (rounds with ≥1 primary-vs-verifier mismatch / total rounds):
  22 / 25 = **0.88**
  (Zero-disagreement rounds: R011, R019, R020. R022 verifier returned API
  policy error — counted as "disagreement-unknown" but tallied with the 22.)

### score_v1

```
score_v1 = (pass_count × 10) + (25 − mean_forced_hit_per_round) + (disagreement_rate × 5)
         = (0 × 10)         + (25 − 4.6)                        + (0.88 × 5)
         = 0                + 20.4                              + 4.4
         = 24.8
```

## 2. Compliance health

| Gate | Pass | Notes |
|------|-----:|-------|
| Step 06 real web_search ≥2 queries | 25/25 | file-chain held; zero skips |
| Step 07 keyword rule applied | 25/25 | 7 inline substring corrections |
| Step 07 no forced-rule override | 25/25 | impulses to override logged in 11_audit, not acted on |
| Step 10 mechanical verdict | 25/25 | |
| Step 12 cross-agent verification | 24/25 | R022 API-policy-error infrastructure failure |

The three-layer enforcement worked at a procedural level. No fake searches,
no rule overrides. The session's failures are research-substance failures,
not compliance failures.

## 3. Failure-mode incidence

| Failure mode | Count | Representative rounds |
|--------------|------:|-----------------------|
| bias_training_data | 0 | — |
| implementation_drift | 7 | R003, R007, R009, R010, R015, R017, R018, R021, R022, R025 (substring edge cases — singular/plural, hyphen/space, prefix) |
| memory_context | 0 | — |
| overexcitement | 4 | R001, R004, R005, R010 (clean-mechanism aesthetic pull) |
| domain_intelligence | 2 | R002, R003 (queries returned source-domain papers, not LLM-application) |
| scientific_taste | 0 | — |

## 4. Why every round FAILed — the structural pattern

Reading all 25 `11_audit.json` honest_notes plus the disagreement log, the
mechanism of failure is consistent:

1. **Cross-domain analogy + LLM-application framing is saturated at the
   umbrella level.** Every round, primary found at least one 2024–2026
   LLM paper occupying the umbrella mechanism the candidate proposed.

   Direct prior-art examples named in audits:
   - R003 estoppel → AgentArmor 2508.01249 (Program-Dependence-Graph runtime locking)
   - R004 songlines → MemPalace 2604.21284 ("first systematic spatial-memory")
   - R007 TCM pulse → Bloom's Taxonomy linear probing 2602.17229
   - R009 Ayurvedic dosha → AI Agent Behavioral Science 2506.06366
   - R010 Liesegang → Quantifying Emergence 2409.01568 + multiple surveys
   - R011 CRISPR PAM → Prompt Infection LLM Tagging 2410.07283
   - R012 stomatal → Tool Attention 2604.21816
   - R013 KAM → Safety Basin literature 2405.17374
   - R014 hyporheic → MemVerse 2512.03627
   - R017 waggle dance → PMC12467162 biological-comm-to-UAV swarm
   - R019 riboswitch → Agentic Context Engineering 2510.04618
   - R022 prion → "From Spark to Fire" 2603.04474, MemoryGraft 2512.16962
   - R023 Ostwald → TiMem/Memoria/A-Mem/LightweightAgentMemory cluster
   - R024 TCM meridian → Locate-Steer-Improve 2601.14004 + 6 more
   - R025 spin glass → 5+ stat-mech-NN foundation papers + LLM software aging

   Even program.md's `§8` explicitly-named "untested" sub-doctrines failed:
   - Ayurvedic dosha (R009), TCM meridian (R024), riboswitch (R019),
     indigenous fire (R020). All have substantive 2024–2026 prior art.

2. **Source-domain noise inflates mean_forced_hits.** A large fraction of
   the 4.6 mean is *biology / physics / wiki encyclopedic pages* that
   substring-match 2+ content_words because the content_words include
   the source-domain mechanism name (e.g., "autophagy", "Bauschinger",
   "Liesegang ring"). These are forced hits but are not LLM-side prior
   art. They drive the verdict mechanically but they are noise in the
   inter-rater-reliability measurement.

   In R002, 17 of 23 hits were source-domain biology pages. In R005,
   9 of 19 were materials-science pages. In R025, the source-domain
   plus LLM substantive prior art both saturated the result set.

3. **Disagreement pattern is structural.** In 19 of 22 successful
   verifications, the disagreement direction was the same:
   **primary judged hit / verifier judged miss** on agent-judged
   (overlap < 2) results. Primary used substantive-equivalence
   liberally; verifier used it strictly. Verdict-level FAIL agreement
   held in 22/22 successful verifications because forced hits alone
   were sufficient to FAIL each round.

   3 rounds with zero disagreement (R011, R019, R020) all had
   substantive prior art so direct that primary and verifier converged
   on the same hit set.

## 5. What the data says, plainly

- Saturation hypothesis is well-supported in the corpus. The
  cross-domain-analogy + 2024–2026 LLM literature interaction is saturated
  enough that no surveyed candidate cleared the bar.
- Compliance-enforcement design works. File chain + mechanical rule +
  cross-agent verification did what they were supposed to do.
- The "forced hit" metric measures BOTH (a) prior-art density and
  (b) source-domain naming choices. Lowering it without cheating means
  picking candidates where the content_words are more discriminating —
  not just narrowing words to escape hits.

## 6. Implications for epoch 2 (per phase-2 constraints)

ALLOWED levers (per the user instruction):
- candidate generation strategy
- web search query formulation
- content_words selection rules
- stopping condition tuning

FORBIDDEN levers (per the user instruction):
- step 06 web_search requirement
- step 07 keyword threshold
- step 10 mechanical verdict
- step 12 cross-agent verification

The clean change-space for v2:
- **Candidate generation**: shift away from single-mechanism cross-domain
  analogy. Specifically epoch 1 evidence — every single-mechanism analogy
  found a 2024–2026 umbrella paper — supports trying *conjunction* or
  *negation* or *quantitative-specific* candidate forms.
- **Query formulation**: epoch 1 queries returned source-domain pages
  (R002, R003 audits) inflating forced hits. v2 can require an
  LLM-application qualifier in every query string to shift result mass
  toward the LLM-side, surfacing substantive prior art faster and reducing
  source-domain noise.
- **content_words rules**: epoch 1 content_words mixed source-domain
  jargon and LLM jargon, so encyclopedic source-domain pages and
  LLM-side prior-art papers both forced-hit. v2 can require an
  intent-split: ≥2 LLM-side technical terms must be in the list, so a
  source-domain encyclopedic page (which contains zero LLM terms) cannot
  reach overlap ≥ 2 even though it names the mechanism. This is NOT
  threshold-tuning (still ≥2). It is content-words-composition tuning.
- **Stopping conditions**: epoch 1 hit 25 successfully but operated near
  context budget. v2 can stop earlier if a 5-round-window forced-hit
  pattern is unchanged AND verifier-disagreement pattern is unchanged
  (no new information being generated).

These are precisely the levers the prompt names as allowed. Each v2 change
cites the round evidence above.
