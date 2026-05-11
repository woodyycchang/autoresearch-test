# Epoch Comparison — v1 (rounds 1–25) vs v2 (rounds 26–50)

## 1. Raw scores

```
score = (pass_count × 10) + (25 − mean_forced_hit_per_round) + (disagreement_rate × 5)
```

| Metric | Epoch 1 (v1) | Epoch 2 (v2 mechanical) | Δ |
|--------|-------------:|------------------------:|--:|
| PASS count (mechanical) | 0 | 4 | +4 |
| PASS count (substantive) | 0 | 0 | 0 |
| mean_forced_hit_per_round | 4.6 | 3.4 | −1.2 |
| disagreement_rate (any flag) | 0.88 | 0.28 | −0.60 |
| disagreement_rate (mechanical only) | 0.88 | 0.12 | −0.76 |
| **score_v_mechanical** | **24.8** | **62.2** | **+37.4** |
| **score_v_substantive (honest)** | **24.8** | **22.2** | **−2.6** |

The headline score number improves by +37.4 under the mechanical reading of
PASS. But the four mechanical PASSes are **strict-substring artifacts**, not
real research wins (see §4). On the honest substantive reading, score
moves slightly DOWN by 2.6.

## 2. Detail comparison

### 2.1 Compliance

| Step | Epoch 1 | Epoch 2 |
|------|--------:|--------:|
| 01 future present | 25/25 | 25/25 |
| 02 ≥3 sub-problems | 25/25 | 25/25 |
| 03 real arxiv IDs | 25/25 | 25/25 |
| 04 specific not generic | 25/25 | 25/25 |
| 05 not duplicate | 25/25 | 25/25 |
| 05 content_words count in range | 25/25 | 25/25 |
| 05 v2 composition rule | n/a | 24/25 (R043 logged) |
| 06 real web search ≥2 queries | 25/25 | 25/25 |
| 06 v2 query rules | n/a | 25/25 |
| 07 keyword rule applied | 25/25 | 25/25 |
| 07 no forced-rule override | 25/25 | 25/25 |
| 10 mechanical verdict | 25/25 | 25/25 |
| 12 verification completed | 24/25 (R022 API err) | 25/25 |

Both epochs maintained the file-chain. Epoch 2 had no infrastructure-failure
in step 12 (vs epoch 1's R022 API policy error). v2-specific composition
rule was followed in 24/25 rounds; the one violation (R043) was honestly
logged rather than retro-narrowed.

### 2.2 Forced-hit distribution

| Statistic | Epoch 1 | Epoch 2 |
|-----------|--------:|--------:|
| Mean | 4.6 | 3.4 |
| Median | 3 | 3 |
| Max | 17 (R005/R017) | 10 (R027) |
| Rounds with 0 forced hits | 0 | 4 (R045-46-47-50) |

The reduction in mean forced hits is the v2-design-intent: the content_words
composition rule (≥2 LLM-side, ≥2 source-side, ≤2 generic) reduces
source-domain encyclopedic noise. In epoch 1, many forced hits came from
biology / physics / wiki encyclopedic pages (R002 17 of 23 hits were
biology pages; R005 9 of 19 were materials-science pages). In epoch 2, the
LLM-side-anchored queries and content_words mean forced hits are
overwhelmingly LLM-side substantive prior art (e.g., R026 all 6 forced
hits are LLM-MAS coordination papers, no biology / physics noise; R044 all
6 are CoT-LLM papers).

### 2.3 Form-level performance (epoch 2 only)

| Form | Rounds | Mean forced hits | Mech-PASS count |
|------|------:|-----------------:|----------------:|
| A (conjunction)              | 7 | 4.4 | 2 (R046, R050) |
| B (negation/impossibility)   | 6 | 3.5 | 1 (R047) |
| C (quantitative)             | 6 | 4.3 | 0 |
| D (reverse direction)        | 6 | 2.5 | 1 (R045) |

Form D produced the lowest forced-hit mean — the LLM-→-non-LLM
predictive direction is least covered in current literature. Form C
quantitative is moderately covered. Forms A and B are roughly equivalent.

### 2.4 Disagreement pattern (epoch 1 vs epoch 2)

Epoch 1 disagreements were almost entirely
**primary-lenient vs verifier-strict on agent-judged (overlap<2) results**.
Epoch 2 has two qualitatively different disagreement modes:

- **Mechanical disagreements (epoch-1-style)**: 3 rounds (R028, R034,
  R036), all primary=substantive-hit / verifier=strict-miss on overlap=1
  agent-judged items. Lower rate than epoch 1 because v2 content_words
  composition rule reduces the locus where agent-judged hits arise.

- **NEW: Substantive-FAIL-flag despite mechanical-PASS-agreement**: 4 rounds
  (R045, R046, R047, R050). Both primary and verifier agree mechanically on
  total_hits=0, but verifier independently identifies substantive prior art
  that the strict-substring rule missed due to word-order variation
  ('Loss of Plasticity' vs 'plasticity loss'; 'LLM-guided' vs 'LLM agent';
  etc.). This is a NEW kind of cross-agent finding the program design did not
  anticipate.

## 3. What v2 changes worked

### Change 1 (candidate generation strategy — Form A/B/C/D rotation)
**Worked as intended.** Form D consistently produced lower forced-hit counts
than single-mechanism analogy in epoch 1. Form D mean forced hits 2.5 vs
epoch 1 mean 4.6. The reverse-direction predictive frame has thinner direct
prior art in the literature corpus.

### Change 2 (web search query formulation — LLM-side qualifier required)
**Worked as intended.** Forced hits in epoch 2 are overwhelmingly LLM-side
substantive prior art papers, not source-domain encyclopedic noise. The
LLM-qualifier-required rule pulls result-set mass toward the LLM literature
side, surfacing direct prior art faster.

### Change 3 (content_words composition — ≥2 LLM-side, ≥2 source-side, ≤2 generic)
**Worked as intended on noise reduction.** Source-domain encyclopedic pages
(R002 R005 epoch-1 pattern) no longer forced-hit because they lack the
LLM-side terms. R034 cryptochrome physics pages got 1 match each, below
threshold — exactly the design intent.

**UNINTENDED CONSEQUENCE: strict-substring artifacts.** The composition
rule pushes content_words toward specific phrasings (e.g., 'LLM agent',
'plasticity loss', 'attention head') that may not strict-substring-match
common literature variants ('LLM-guided', 'Loss of Plasticity',
'attention head's). This produces FOUR mechanical PASS verdicts (R045-46-47-50)
that are not substantively new candidates — the cross-agent verifier
correctly identifies dense substantive prior art in each case. The artifact
is faithful to the program's mechanical rule but inflates the mechanical
PASS count.

### Change 4 (stopping condition tuning)
**Partially used.** The abbreviated-audit option was used informally for
later rounds. The soft early-stop at 20 rounds was NOT triggered because
the pattern was not stable (the strict-substring artifact rounds emerged
mid-batch). Hard-halt signals were not triggered.

## 4. The four "mechanical PASS" rounds — honest analysis

| Round | Form | Why mechanical PASS | Why substantive FAIL |
|------:|:----:|---------------------|----------------------|
| 045 | D | content_word 'plasticity loss' not substring of literature variant 'Loss of Plasticity' | Nature 2024 paper directly establishes the phenomenon |
| 046 | A | content_word 'in-context learning' partial; 'ICL' acronym not substring | 2507.13540 'Low-Frequency Bias of ICL' is direct prior art |
| 047 | B | content_word 'LLM watermark' substring of 'LLM Watermarking' but other phrases miss | 2410.02890 'Theoretically Grounded LLM Watermarking' is direct prior art |
| 050 | A | content_word 'LLM agent' not substring of 'LLM-guided' / 'LLM Multi-Agent' | 2506.20921 LLM-MAS capability-cost paper is direct prior art |

All four PASSes are honest mechanical applications of the program's strict-substring rule, but represent cases where the literature uses a *different word order or morphological variant* than the candidate's chosen
phrasing. The cross-agent verification (program §12) successfully flags
each one as substantively occupied, demonstrating that the §9 design
intent (verifier catches what the mechanical rule misses) operates exactly
as planned.

For a research-honest score, these PASSes should be counted as FAIL:
**substantive PASS count = 0, same as epoch 1.**

## 5. Score with substantive interpretation

```
score_v2_substantive = (0 × 10) + (25 − 3.4) + (0.28 × 5)
                     = 0 + 21.6 + 1.4
                     = 23.0
score_v1             = (0 × 10) + (25 − 4.6) + (0.88 × 5)
                     = 0 + 20.4 + 4.4
                     = 24.8
```

Under the substantive reading, score_v2 is **−1.8** lower than score_v1.
The (25 − mean_forced_hit) term improved by +1.2 (less noise) but the
disagreement_rate × 5 term dropped by 3.0 (less cross-agent disagreement
since the v2 content_words rules left less room for agent-judged hits).

The bottom-line conclusion: **v2 produced cleaner data per round (lower
noise floor, less inter-rater disagreement) but did not crack the
saturation problem — combined N=188 still has 0 substantive PASS.**

## 6. What the v2 experiment tells us

1. **Saturation is robust to candidate-form-rotation.** Forms A/B/C/D all
   FAIL substantively in every round. The 2024–2026 LLM literature has
   covered cross-domain analogy AT umbrella level so densely that even
   conjunctions, negations, quantitative predictions, and reverse-direction
   bridges find substantive prior art.

2. **Form D (reverse direction) has thinnest direct bridge.** Forced-hit
   means by form: D=2.5, B=3.5, C=4.3, A=4.4. If a future epoch focuses
   on candidate-generation, Form D variants are most likely to find
   non-trivial cleaner candidates — though all 6 Form-D rounds still FAIL
   substantively due to the LLM endpoint of the bridge being published.

3. **Strict-substring rule has artifact failure mode.** The mechanical
   rule's strict-substring matching can be defeated by word-order /
   morphological variation in published literature. Future v3 might
   consider regex / lemma-aware matching, or explicit lemma forms in
   content_words (e.g., listing both 'plasticity loss' and 'loss of
   plasticity'). But that change is OUT OF SCOPE for v2 — it touches
   step 07 keyword threshold which is FORBIDDEN to modify.

4. **Cross-agent verification at §12 catches the §3 strict-substring
   artifact.** This is the program's intended design — the verifier
   independently identifies substantive prior art even when both primary
   and verifier agree mechanically. The strict-substring artifact thus
   reveals a useful PROPERTY of the multi-layer design: layer 3
   (verification) backstops layer 2 (mechanical rule) when layer 2 has
   limited expressive power.

## 7. Score table (one-line summary)

| Reading | Epoch 1 | Epoch 2 | Δ |
|---------|--------:|--------:|--:|
| Mechanical (PASS=4) | 24.8 | 62.2 | **+37.4** |
| Substantive (PASS=0, honest) | 24.8 | 23.0 | **−1.8** |

The user instruction in the prompt is to "Compute score_v2" — I report
both. The mechanical reading is what the formula literally says when
applied to the mechanical-rule output. The substantive reading is the
HONEST research-value reading.

## 8. Combined corpus (138 prior + 25 epoch-1 + 25 epoch-2 = 188)

- Total rounds: 188
- Substantive PASS: 0
- Mechanical PASS (strict-substring artifact only): 4
- p(no PASS | 1% novelty rate) ≈ (0.99)^188 ≈ 0.150 (substantive)
- p(no PASS | 5% novelty rate) ≈ (0.95)^188 < 0.0001
- p(no PASS | 10% novelty rate) ≈ (0.90)^188 < 10^-8

The saturation conclusion strengthens: at the 5% novelty rate the bound
is < 10⁻⁴, decisive evidence of saturation against any moderate novelty
hypothesis. At 1% the bound remains weak (≈0.15) — consistent with
"paradigm-shift candidates exist but are <1% incidence per round."
