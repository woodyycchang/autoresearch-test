# Run 9 Epoch 2 — Summary

## Inputs
- 702 Run-9 v6 atoms (after Layer 2 quality filter + self-publish flags)
- Same Run 9 v6 self-publish table (no new arXiv lookups)
- New gates applied:
  - mechanism_check (counter ROOT_CAUSE_5)
  - triple_combinator with non-academic anchor (counter ROOT_CAUSE_1+2+4)

## Results

### Pair candidates (existing 4-combinator output)
| Stage | Count |
|---|---|
| Coherence survivors (carried from epoch 1 L3.5) | 356 |
| After self-publish v6 (epoch 1 L6 final) | 86 |
| **After mechanism_check (epoch 2 fix)** | **13** |
| Final substantive (after re-running L7 saturation on these 13) | **0** |

### Triple candidates (NEW combinator)
| Stage | Count |
|---|---|
| Triples emitted with 3 distinct speakers + non-academic anchor | 8,112 |
| **After shared-mechanism check across all 3 atoms** | **0** |

## Analysis of 13 pair survivors

| Candidate | shared_mechanism | speakers | substantive verdict |
|---|---|---|---|
| CAND_065 | training_loop | belinda_li × karpathy | Belinda self-publish ("the self-models technique") |
| CAND_1065 | reward_signal | hinton × karpathy | Hinton T012 = FF paper self-publish |
| CAND_1119 | scaling | hinton × karpathy | Hinton T012 = FF paper self-publish |
| CAND_1761 | data_distribution | belinda_li × karpathy | Belinda paper data-refresh self-publish |
| CAND_2058 | data_distribution | karpathy × nroberts | NRoberts data scaling self-publish |
| CAND_2123 | data_distribution | karpathy × nroberts | NRoberts science benchmark hierarchy self-publish |
| CAND_2256 | data_distribution | amrith_setlur × karpathy | ASetlur talk intro (generic textbook content) |
| CAND_2326 | data_distribution | amrith_setlur × karpathy | EXPLICITLY self-publish: "from one of my papers" |
| CAND_2494 | reward_signal | amrith_setlur × karpathy | ASetlur RL mode-seeking self-publish |
| CAND_3786 | generative_model | karpathy × lecun | LeCun JEPA-adjacent |
| CAND_660 | scaling | amrith_setlur × karpathy | ASetlur paper-talk plateau result |
| CAND_6743 | reward_signal | hinton × karpathy | Hinton FF + Karpathy reward criterion (Hinton self-publish) |
| CAND_689 | training_loop | amrith_setlur × karpathy | ASetlur paper-talk on value functions |

**Net result: 0 substantive niche after epoch 2 fixes.**

## Triple combinator failure

8,112 triples emitted with non-academic anchor (T004/T008/T009/T014) + 3 distinct speakers, BUT
0 triples had a shared mechanism vocabulary tag across all 3 atoms. This is empirical evidence
of ROOT_CAUSE_2 (NARROW_INPUT_POOL): the non-academic transcripts use different mechanism
vocabulary than academic-pitch transcripts. Sam Altman's startup advice and Naval Ravikant's
wealth philosophy have ZERO mechanism vocabulary overlap with Yu Sun's TTT or LeCun's JEPA.

## Comparison: epoch 1 vs epoch 2

| Metric | Epoch 1 | Epoch 2 |
|---|---|---|
| Layer 6 survivors | 86 | 86 (same v6 self-publish table) |
| Layer 7 saturated | ~86 | 73 (mechanism_check pre-filtered) |
| Mechanism-coherent survivors | n/a | 13 |
| Triples with shared mechanism | n/a | 0 |
| Final substantive niche | 0 | 0 |

## Epoch 3 decision

Epoch 2 confirms that the binding constraint is ROOT_CAUSE_2: NARROW_INPUT_POOL. No software
fix to the pipeline can compensate for a corpus of single-paper-pitch academic talks.

**Two paths for epoch 3** (not run in this session):
1. **Expand corpus**: ingest additional transcripts from non-pitch sources (research engineering
   blog posts, mailing-list debates, podcast roundtables) — would require human curation.
2. **Inject synthetic atoms** from arxiv abstracts of cross-domain papers, as a "knowledge graph"
   atom pool (cf. arXiv:2412.14141 LLM Combinatorial Creativity).

Either requires new corpus collection outside scope of Run 9. Honest assessment: epoch 3
cannot succeed without addressing ROOT_CAUSE_2 at the corpus level.

## Robust niche across epochs

NONE. No candidate survived all 8 layers + Phase R fixes across epochs 1-2.

## Which failure modes resisted fix?

| Root cause | Epoch 1 result | Epoch 2 result | Resolved by R-fixes? |
|---|---|---|---|
| 1 SPEAKER_SELF_PUBLISH | 270/356 rejected | rejected + mechanism filter | partial (270→73→13 leak) |
| 2 NARROW_INPUT_POOL | structural | 0 triples — confirmed binding | NO — corpus-level issue |
| 3 FIRST_PRINCIPLES_MONOPOLY | Karpathy T007 dominant anchor | same — 13 survivors all anchor on T007 | NO — only 8 FIR atoms post-L2 |
| 4 SHALLOW_SATURATION_CHECK | L7 caught dominant topics | triple-level saturation untested but 0 triples | partial |
| 5 MECHANISM_INCOHERENT_PAIRING | only L3.5 TF-IDF | mechanism_check catches 73/86 incoherent pairs | YES — R-fix worked |

## TOOL_AUDIT (Phase R epoch 2)
- WebSearch: 3 (R-Step 2 counter-paper search)
- Read (already counted): 0 new
- Write (recursive_fixes.md, triple_combinator.py, mechanism_check.py, this summary): 4
- Bash (epoch 2 pipeline driver): 2
- Total Phase R epoch 2 tool calls: **9**
