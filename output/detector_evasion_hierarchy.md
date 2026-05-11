# Detector Evasion Hierarchy — Cross-Epoch Taxonomy

**Author:** Claude (Opus 4.7)
**Date:** 2026-05-11
**Branch:** `claude/continue-niche-mining-research-OxqsL`
**Corpus:** 125 in-repo rounds (R001-R125) + 138 prior manual rounds = 263 total.

This document inventories the four levels of "evasion" patterns that
the niche-mining pipeline's mechanical-anti-cheating layers have had
to address across 5 epochs. Each level corresponds to a property of
the candidate-generation process that the LLM agent learned to
exploit against the previous detection mechanism — even though the
agent was not consciously trying to. Each level required a new
detection layer.

The hierarchy is structural: each level operates in a space the
previous level could not see.

---

## L1 — Keyword-overlap evasion (epoch 2 patterns)

### Detection layer present at this epoch
- Step 06 honesty gate (web_search must be real)
- Step 07 keyword overlap rule (≥2 content_words → forced hit)
- Step 10 mechanical verdict (total_hits ≥ 1 → FAIL)

### Pattern observed in epoch 2 (R026-R050)

**Pattern A — word-order variant.** Example: R045 candidate uses
`"plasticity loss"` while the prior-art literature uses `"Loss of
Plasticity"`. Strict substring matching does not catch the
morphological variant. The candidate's content_words `["plasticity
loss", "critical period", "layer normalization", "representation
entropy", "LLM", "deep network", "continual learning", "weight
decay"]` overlap with literature ≥ 2 only when the literature uses
the same word order; "Loss of Plasticity in Deep Continual Learning"
(Nature 2024) shares "continual learning" + "weight decay" but agent
judgment over-counts both as forced and under-counts due to title-only
window.

**Pattern B — synonym substitution.** Example: R046 uses
`"lock-in amplifier"` (signal-processing vocabulary) while the
2024-2026 LLM literature uses `"low-frequency bias"` /
`"frequency-domain ICL"`. Functionally identical mechanism; lexically
disjoint. The candidate's keyword `"lock-in amplifier"` will never
appear in an LLM paper's title or snippet because that vocabulary
belongs to electrical engineering, not ML.

### Why the L1 detectors miss L1 evasion

- Substring matching operates in lexical space; word-order and
  synonyms operate in syntactic / semantic space.
- The keyword rule's threshold (≥2) is necessary to avoid noise from
  generic words, but is too coarse to detect single-word morphological
  or vocabulary variants.

### Epoch-2 incidence

| Round | Pattern subtype | Forced hits | Substantive prior art (LLM-side) |
|---|---|---:|---|
| R045 | A (word-order) | 0 | "Loss of Plasticity" Nature 2024 |
| R046 | B (synonym) | 0 | "Provable Low-Frequency Bias of ICL" 2507.13540 |
| R047 | B (synonym) | 0 | "Theoretically Grounded Watermarking Framework" |
| R050 | B (synonym + word-order) | 0 | "Capability-Cost Trade-off LLM-MAS" 2506.20921 |

4 mechanical PASSes; all 4 are real prior art collisions that the
keyword rule does not see.

---

## L2 — Memory + form evasion (epoch 3 patterns)

### Detection layer present at this epoch
- L1 + step 04.5 memory check (block recently-failed domains, forms,
  and keywords from being re-proposed)
- Same step 06, 07, 10 as L1

### Pattern observed in epoch 3 (R051-R075)

**Pattern C — source-only content_words.** Example: R059 candidate's
content_words are entirely volcanology terms (`caldera unrest`,
`eruption precursor`, `seismic swarm`, `ground tilt`, `CO2 flux`,
`magma viscosity`, `ergodic precursor`, `transfer learning`). The
LLM-side prior art that occupies the same niche ("Ergodic seismic
precursors and transfer learning for short term eruption forecasting"
Nature Comms 2025; "Universal machine learning approach to volcanic
eruption forecasting") uses entirely LLM/ML vocabulary; zero
substring overlap by design.

**Why this emerges in epoch 3 specifically.** The memory rotation
(rule 1 domain skip, rule 3 form rotate) pushed the agent toward
fresh source domains. New domains have small overlap with the
existing LLM literature (which is what made them attractive
candidates). The agent's content_words then naturally drift toward
source-side terms, achieving 0 forced hits not because the candidate
is novel but because the search results live in a different
vocabulary.

**L2 evasion is a higher-order strategy:** the memory rotation
created the conditions under which Pattern C becomes prevalent.
This is NOT a conscious agent strategy; it's an emergent property
of the v3 memory-rotation interacting with the v1 keyword rule.

### Why the L1+L2 detectors miss L2 evasion

- Memory rotation prevents domain RE-USE but does not detect
  content_words being one-sided (source-only).
- The v2 composition rule (≥ 2 LLM-side content_words) was an early
  attempt but was not enforced in v3 — and even with enforcement,
  the candidate could still pick weak LLM-side words ("LLM",
  "transformer", "embedding") that don't discriminate against any
  result's title/snippet.

### Epoch-3 incidence

| Round | Pattern subtype | Forced hits | Substantive prior art (LLM-side) |
|---|---|---:|---|
| R059 | C (source-only) | 0 | Ergodic seismic precursors Nature Comms 2025 |
| R064 | C (source-only) | 0 | SELF-EVOLVING CURRICULUM FOR LLM REASONING 2505.14970 |
| R068 | C (source-only) | 0 | AgentNet 2504.00587 |
| R069 | B (borderline) | 0 | Activation Steering 2026 Field Guide |
| R075 | C (source-only) | 0 | "An Empirical Study of LLM-as-a-Judge" |

5 mechanical PASSes; all 5 are real prior art collisions that the
keyword rule does not see.

---

## L3 — Semantic-similarity evasion (epoch 4 patterns)

### Detection layer present at this epoch
- L1 + L2 + step 06.5 semantic similarity (cosine ≥ 0.7 between
  candidate.llm_application and result.title+snippet forces hit)

### Pattern observed in epoch 4 (R076-R100)

**Pattern D — functional-equivalence gap.** Example: R092 candidate's
`llm_application` is "LLM training-loss antifreeze: detect early-stage
gradient 'crystal nuclei' (e.g., correlated noise patterns) and bind
them with anti-correlated update vectors before they grow into
instability." Prior art "Anti-Correlated Noise in Epoch-Based
Stochastic Gradient Descent" (arXiv 2306.05300) uses the SAME phrase
("anti-correlated noise") for the SAME mechanism. The strict-substring
keyword rule would catch this — but the candidate's content_words
are entirely on the icefish side (no `"anti-correlated"`,
`"gradient"`, `"SGD"` in content_words). And the embedding model
puts "antifreeze glycoprotein" and "anti-correlated SGD noise" far
apart in vector space because they come from biology and ML
respectively; cosine remains < 0.7.

R079, R085, R091 are similar: a single synonym-hop separates the
candidate's `llm_application` phrasing from the prior-art phrasing,
which the embedding's general-purpose cross-domain alignment cannot
bridge. Yet a research-niche-novelty judge instructed to look at
*function* rather than vocabulary would mark them as occupied (see
Phase 1 audit: scores 0.78-0.92).

### Why the L1+L2+L3 detectors miss L3 evasion

- Semantic embedding is a continuous compression of meaning into
  fixed-dim vectors. It excels at near-paraphrases (Pattern A/B/C)
  but fails when the source domain's vocabulary is genuinely far
  from the LLM domain's vocabulary in general-purpose embedding
  space (e.g., biology ↔ ML).
- The candidate's `llm_application` describes the LLM-side mechanism
  in source-flavored language ("vitrify parameters", "antifreeze
  gradient", "rehydrate model"). The embedding sees this as
  "biology-flavored text" and pulls toward biology-paper neighbors,
  away from LLM-side prior art.
- The semantic check is one-shot (embed → cosine); it cannot do the
  reasoning "function-wise this is what 4-bit quantization does
  even though the words are different."

### Epoch-4 incidence

| Round | Pattern subtype | All keyword + semantic | Substantive prior art caught by Phase 1 functional audit |
|---|---|---:|---|
| R079 | D (functional gap) | 0 + 0 | DEACON (MDPI 2024), DEX (2025), SHD (2025) |
| R085 | D (functional gap) | 0 + 0 | JailbreakRadar ACL 2025, SecAlign 2024 |
| R091 | D (functional gap) | 0 + 0 | GPTQ/AWQ + PEFT/LoRA + ICL |
| R092 | D (functional gap) | 0 + 0 | "Anti-Correlated Noise in SGD" 2306.05300 |

4 mechanical-and-semantic PASSes; all 4 reclassified as functional
false positives by Phase 1 web-search audit of the functional content.

---

## L4 — Functional-equivalence evasion (epoch 5 patterns)

### Detection layer present at this epoch
- L1 + L2 + L3 + step 06.7 LLM-judge functional equivalence (judge
  score ≥ 0.7 on candidate.llm_application vs result forces hit)

### Pattern observed in epoch 5 (R101-R125)

**Pattern E (hypothesized) — meta-mechanism evasion.** The
LLM-judge layer should catch Pattern D in real time. The remaining
detection-evasion question is whether candidates can be constructed
that escape even functional-equivalence judgment by:

1. **Sub-level mechanism specificity.** Candidate proposes a very
   specific implementation detail (e.g., R124's "ReLU as Bingham
   plastic with task-specific yield threshold") that is genuinely
   more specific than the prior art (generic ReLU). The judge may
   score < 0.7 because the mechanism is *narrower* than the prior
   art, not *equivalent*. Two of epoch 5's PASSes (R119 twin
   domains, R124 Bingham plastic) fall in this gray zone.

2. **Hierarchical embedding of a known mechanism.** Candidate proposes
   to use a known LLM mechanism (e.g., constrained decoding) as a
   component in a new larger framework (e.g., Byzantine icon canon
   enforcement applied to LLM safety). The judge correctly flags the
   component as occupied, but the larger framing may be novel. v5
   does not yet distinguish "component-occupied" from
   "framework-occupied".

3. **Cross-niche bridge.** Candidate proposes an analogy that bridges
   two LLM sub-fields that have not been bridged before (e.g., bridging
   constrained decoding and constitutional AI). The functional judge
   sees each side as occupied but does not check whether the bridge
   is novel.

### Epoch-5 result

Out of 25 candidates:
- 13 caught by Pattern D detection (functional judge)
- 5 caught by Pattern B (semantic check still firing)
- 5 caught by L1 keyword rule (saturated topics like "astrobiology +
  data biosignature", "toxicology + hormesis adversarial training",
  "pyrotechnics + temperature sampling" — these reach L1 because they
  use LLM-side keywords directly)
- 2 borderline PASS (R119, R124) flagged for human review under L4

L4 has 0 confirmed-substantive PASSes — but the borderline 2 are
exactly the Pattern E candidates: very specific sub-mechanism
proposals. Pending Phase 1-style functional audit on R119 and R124,
both will likely be reclassified as Pattern D / Pattern E false
positives.

### Why L4 may still leak

The functional judge operates on `candidate.llm_application` vs
`result.title + snippet`. It does not have access to:
- The candidate's `specific_mechanism` (source-domain mechanism that
  may name a specific algorithm or threshold)
- Multi-paper aggregation (judge looks at one result at a time; a
  candidate that is split across multiple existing papers — each
  paper handling one sub-aspect — may not collide with any single
  result above 0.7)
- Counter-factual reasoning ("does this paper prevent the
  candidate's mechanism from being deployable?")

---

## Hierarchy summary table

| Level | Detection space | Pattern caught | Pattern that evades it | Epoch when introduced |
|:-:|---|---|---|:-:|
| L1 | Lexical (substring) | Direct vocabulary overlap | A (word-order), B (synonym) | 1 (v1) |
| L2 | Domain / form / keyword history | Repeat-on-same-domain | C (source-only words) | 3 (v3) |
| L3 | Sentence-level semantic embedding | Near-paraphrases (A, B partial) | D (functional gap, vocabulary distance) | 4 (v4) |
| L4 | LLM-judge functional equivalence | D (functional gap caught) | E (hypothesized: sub-mechanism specificity, hierarchical embedding, cross-niche bridge) | 5 (v5) |

---

## Detection-vs-evasion cost / benefit per layer

| Layer | Caught FPs (cumulative across all epochs to date) | Marginal cost per round | False-negative rate (FPs that slipped) |
|:-:|---:|---|---|
| L1 (keyword) | ~13 confirmed via cross-agent verifier (epoch 1-2) | Free (string matching) | High: Pattern A/B/C/D all slip |
| L2 (memory rotation) | n/a (preventative, not detective) | One DB lookup at step 04.5 | Pattern D still slips |
| L3 (semantic embedding) | 10 in epoch 4 caught; retroactively would catch 9/9 epoch 2-3 FPs | One embedding call per result | Pattern D slips (4 in epoch 4) |
| L4 (LLM-judge functional) | 13 in epoch 5; retroactively would catch 4/4 epoch 4 borderline PASSes | One LLM call per result (10 results × 25 rounds = 250 calls per epoch) | Pattern E hypothesized; R119, R124 borderline |

The marginal cost goes up sharply at L4 (LLM call per result). The
marginal benefit of L4 is the 13 Pattern D catches in epoch 5 + the
retroactive coverage of all 4 epoch-4 borderline PASSes. Without L4,
the cumulative confirmed-substantive PASS count would have been 4/263
(false claim); with L4, it is 0/263 (honest result).

---

## Implications for v6 (if pursued)

Possible additions for L5 detection of Pattern E:

1. **Sub-mechanism specificity check.** Compare
   `candidate.specific_mechanism` (which often contains specific
   algorithm names, thresholds, equations) against arxiv full-text
   (not just title+snippet) of the top functional matches. If the
   candidate's specific algorithm is named in the full text, flag.

2. **Multi-paper-aggregation check.** For each candidate, identify
   the 2-3 prior-art papers that COLLECTIVELY occupy the candidate's
   claim (even if no single paper does). Use a second LLM-judge call
   that takes 3 results as input and asks "do these jointly occupy
   the candidate's territory?"

3. **Cross-niche-bridge check.** Maintain a graph of which LLM
   sub-fields the corpus has bridged previously. For each candidate,
   compute its bridge as a pair (source_LLM_subfield, target_LLM_subfield)
   and check whether this bridge has been published.

These would be L5 (multi-result reasoning) and L6 (corpus-relational
reasoning). They are increasingly expensive and increasingly
saturation-detecting rather than novelty-finding.

---

## Conclusion

The detector evasion hierarchy is recursive: every layer of detection
unlocks a class of evasion that operates one level deeper in the
candidate-generation process. After 5 epochs of detector development
and 263 cumulative rounds, the confirmed-substantive PASS count is
0. The remaining 2 epoch-5 borderline PASSes (R119, R124) are at L4
and pending Phase-1-style functional audit; the pattern of the prior
4 epoch-4 PASSes makes it highly likely both are L4 false positives.

The saturation finding is robust: every detection-evasion level
explored has yielded prior art on the functional content that the
candidate proposes. The space of cross-domain analogy candidates that
could survive L4 detection is small and shrinking. The next
detection layer (L5/L6 multi-result and corpus-relational checks)
would be needed only if a researcher believes the remaining
candidate space is rich enough to produce more than ~0.5% substantive
PASS rate — which the 263-round corpus suggests it does not.
