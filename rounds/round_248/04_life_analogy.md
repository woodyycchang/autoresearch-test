# R248 — life analogy

## Source domain: bonsai cultivation
- Decade-long shaping of small tree to mimic FORM and PERCEIVED AGE of a large mature tree. Techniques: wiring (branch positioning), pruning (defoliation, root reduction), grafting, gnarl-encouragement.
- The bonsai is NOT a tree-pruned-small — it's a tree shaped to LOOK ANCIENT despite being small. Aesthetic of perceived age, weathering, asymmetric mature form.
- Critical: the SHAPING is a long-cycle iterative process. Each year's growth is selectively retained or pruned to project the desired age-form.

## LLM analogy candidate
**Bonsai-style stylized-aging distillation**: distill a large teacher LLM into a small student, but train student to PROJECT the rhetorical FORM and CONTEXTUAL HISTORY of a much larger / older model — not just performance match. Specifically: distillation loss includes (1) standard logit-matching, (2) STYLISTIC AGING term — student response is penalized if it lacks hedging/cross-reference/long-context markers that the teacher produces, (3) PRUNING SCHEDULE — fine-tune phases with explicit weight-redistribution iterations like annual wiring. Output: a SMALL model that not only reasons like the big one but PRESENTS as if it has the big one's training depth.

## What differs from prior art (claim)
KD literature (2602.01064, 2604.00626, 2504.14772) targets PERFORMANCE preservation under compression. The bonsai discipline adds STYLISTIC-AGING term (project rhetorical depth) + iterative wiring-style shaping schedule. Not retrieved in surveyed prior art as a single distillation discipline.
