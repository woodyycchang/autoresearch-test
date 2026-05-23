# Paradigm-Shift Finder — Run 8 vs Run 9 Comparison

## Tool-use depth

| Metric | Run 8 | Run 9 (epoch 1+2+3) |
|---|---|---|
| WebSearch calls | ~7 saturation queries (manifest) | 33 total (Phase 1 ×10, Phase 2 L5+L6+L7 ×15, Phase R ×3, epoch 3 ×2, plus follow-ups) |
| Reformulations per sub-claim | 1 | 3+ per sub-claim |
| Read tool on transcripts | 0 (relied on canonical text only) | 12+ direct line-span reads |
| Pipeline code edits (str_replace via Edit) | 0 | 7+ (run_9_pipeline.py keywords v2→v6 + counter-module fixes) |
| New pipeline modules created (Write) | 0 | 4 (run_9_pipeline.py, belinda_audit_run9.py, triple_combinator.py, mechanism_check.py) |

## Per-layer survivor count change

| Layer | Run 8 survivors | Run 9 survivors |
|---|---|---|
| Atoms after quality filter | 730 (Run 7 cached) | 702 (32 rejected for past-tense PRE / truncated FIR / vague meta / too-short) |
| Raw candidates emitted | not separately reported | 7,787 |
| After cross-speaker diversity (NEW) | n/a — Run 8 lacks this filter | 7,155 (632 single-speaker like Karpathy×Karpathy rejected) |
| After semantic coherence | ~74 (Run 7 cached) | 356 |
| After Belinda audit | 9 | 356 (all pass mechanically) |
| After arXiv gate | 7 | sampled 5 deep-audit, all have arXiv coverage |
| After market verifier | 7 | n/a (skipped) |
| After self-publish detection (NEW) | n/a — Run 8 had no self-publish gate | 86 (270 of 356 caught as self-publish) |
| After saturation check | 6 (Run 8 final) | 0 substantive (all 86 hit dominant topics) |
| After mechanism_check (Phase R epoch 2) | n/a | 13 pair / 0 triple |
| **Final substantive niche** | 6 (Run 8 thought these were niche) | **0 (after Phase 1 retrospective revealed all 6 Run-8 survivors had hidden saturation)** |

## Recursive epoch trajectory

| Epoch | Survivors | Failure mode |
|---|---|---|
| Epoch 1 (initial v6 keywords + L7 saturation) | 86 → 0 substantive | L7 saturation hits dominant 2024-2026 topics |
| Epoch 2 (+ mechanism_check + triple combinator) | 13 pair / 0 triple | mechanism filter removes 73/86 incoherent pairs; 0 triples with shared mechanism |
| Epoch 3 (loose triple mechanism: ≥2 of 3 pairs) | 2 triples → 0 (Valerie Chen + LeCun JEPA both self-publish) | corpus binding constraint |

## Honest assessment

### What Run 9 improved over Run 8
1. **Atom-quality v2** caught Run-8 misfires: ATOM_T013_S002_PRE_01 (past-tense), ATOM_T002_S046_PRE_01 (vague meta), ATOM_T007_S004_FIR_01 (truncated mid-sentence). These were CAND_run_008_011/012 sources.
2. **Cross-speaker diversity filter** caught Karpathy × Karpathy (T007 × T013), which Run 8 missed (CAND_run_008_012).
3. **Speaker self-publish detection (v6)** caught Yu Sun TTT arXiv:2407.04620 (CAND_run_008_029 was anchored on Yu Sun's own paper). Also caught Hinton FF, Belinda Li self-models, NRoberts scaling, ASetlur RL credit assignment, LeCun JEPA, Karpathy Software 2.0.
4. **Phase 1 deep retrospective** verified all 6 Run-8 "final survivors" actually have hidden saturation (Hinton FF self-publish + mechanism incoherence; Yu Sun TTT self-publish; Karpathy×Karpathy single-speaker; Belinda Li self-models self-publish; Mac-mini saturation).
5. **Mechanism vocabulary gate** (epoch 2 R-fix) reduced 86 → 13 pair survivors by requiring shared mechanism keywords.
6. **Recursive self-improvement** explicitly identified and counter-cited 5 root causes with arXiv counter-papers (arXiv:2410.14255, arXiv:2602.20408, arXiv:2412.14141, arXiv:2605.11258, arXiv:2510.22312).

### What Run 9 did NOT solve
- **ROOT_CAUSE_2 (narrow input pool)** is structural. With 13 transcripts dominated by single-paper-pitch academic talks, no software fix can extract a paradigm-shift niche that wasn't already published by the speaker. The 0-triple result is empirical confirmation.
- **Karpathy T007 anchoring**: most surviving combinations still anchor on Karpathy's textbook "Intro to LLMs" first principles. Karpathy's atoms aren't self-publish (his Software 2.0 keyword catches some) but are pedagogical recap that provides weak novelty.

### Run 8 vs Run 9 verdict
- Run 8 claimed 6 final survivors. **Run 9 Phase 1 invalidated all 6** via deep tool use.
- Run 9 itself yielded 0 substantive niche across 3 epochs.
- **Net knowledge gained**: the pipeline now has documented, mechanical filters for the failure modes Run 8 missed (single-speaker, atom-quality, self-publish v6, mechanism vocabulary, triple combinator with non-academic anchor).
- **Net niche discovered**: 0.

## Conclusion

Run 9 represents a methodological improvement (much deeper tool use, recursive self-improvement,
quantified root causes), but the corpus binding constraint cannot be solved by pipeline changes
alone. Future runs need broader input corpus or synthetic atom injection (arXiv:2412.14141
LLM Combinatorial Creativity is the most promising direction).

## TOOL_AUDIT (Phase 4)
- WebSearch: 0 new
- Write (this file): 1
- Total Phase 4 tool calls: **1**
