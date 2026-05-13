# Life Analogy — Bambara Bogolan resist-dye negative-space mud cloth

The **Bògòlanfini (Bambara mud cloth)**:
- Mali Bambara tradition: women apply fermented mud onto pre-dyed cotton.
- RESIST/NEGATIVE-SPACE technique: pattern emerges where mud was applied (un-dyed areas survive); background dye darkens cloth.
- Fermented mud (~1 year aging) reacts chemically with n'gallama leaf dye → brown fixed.

**BOGOLAN-NEGATIVE**: a SUBTRACTIVE LoRA adapter where the adapter is trained to NEGATE specific learned directions in the base weights (resist-dye analog) rather than ADD new directions. ΔW_neg = -α·(v · v^T) acts as a subtractive projection along learned-undesired direction v; combined with null-space orthogonal training to preserve base capability. Differs from generic null-space LoRA by SIGN-NEGATIVE adapter that resists/subtracts unwanted directions.

## Adjacency
- LoRA-Null 2503.02659 (null-space init)
- LoRA Subtraction Drift-Resistant Space 2503.18985
- Safe LoRA 2405.16833 (project to safety subspace)
- OPLoRA 2510.13003 (orthogonal projection)

Expected FAIL — subtraction/negation-style adapters + null-space LoRA are well-covered.
