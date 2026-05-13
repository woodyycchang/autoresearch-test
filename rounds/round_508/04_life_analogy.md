# Life Analogy — Indonesian Pencak Silat tiered-grade kuda-kuda curriculum

The **pencak silat** (Indonesian martial art, UNESCO 2019):
- 8 basic techniques: kuda-kuda (stance), attitudes/movements, steps, kembangan, buah, jurus, sapuan (sweeps), guntingan (cuts/locks).
- Tiered belt ranks: white (basic) → yellow-1 → yellow-2 → red-3 → green/madya → blue/adult.
- **Kuda-kuda** = foundation: 6 stance types × light/medium/heavy + front/back/middle/side distribution.
- **Madya = teaching rights** unlocked at green-belt level.
- Grade-by-grade syllabus: each grade has prerequisite techniques + locked advanced techniques unlocked by promotion.

**PENCAK-SILAT-GRADE-UNLOCK-CURRICULUM**: tiered-grade LLM curriculum with grade-specific technique unlocking + kuda-kuda foundation invariant + madya-level teaching-rights for self-distillation. (1) 6 grades G_1 (white/basic), G_2 (yellow-1), ..., G_6 (blue/adult). (2) Per grade G_k: training set D_k contains prerequisite-only data; promotion criterion = capability-test C_k > τ_k unlocks next grade. (3) **Kuda-kuda foundation**: G_1-G_2 trains stance equivalent (basic syntax + entity recognition), held invariant across all later grades (no catastrophic forgetting via low-LR on stance heads). (4) **Per-grade technique-augmentation profile**: each grade G_k adds a profile-specific data augmentation (G_3 adds sweeps-style adversarial, G_4 adds cuts-style negation, G_5 adds combination, G_6 free-form). (5) **Madya teaching-rights at G_5**: model at G_5 can serve as teacher for distillation of G_1-G_4 students (self-distillation chain). (6) **Stance-distribution gating**: at each grade, attention-head allocation to light/medium/heavy-stance equivalent (small/medium/large-context heads) follows a grade-specific distribution. (7) Differs from R458 AIKIDO-KATA + R464 ARNIS-STICK + R483 JIEQI-24-STAGE + R496 GRIOT-HEREDITARY-DISTILL by 6-grade explicit promotion criterion + kuda-kuda foundation invariant + madya teaching-rights self-distillation + stance-distribution head gating.

## Adjacency
- Curriculum Learning Pretraining 2601.21698 (closest)
- Beyond Random Sampling 2506.11300
- EDCO Dynamic Curriculum
- Self-Evolving Curriculum 2505.14970
- Self-Distillation literature

Expected FAIL — curriculum learning + tier-progression + self-evolving + distillation literature fully covers.
