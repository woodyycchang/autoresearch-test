# Life Analogy — Aikido kata progressive paired drill curriculum

The **Aikido kata** training system:
- Paired form drill (uke initiates attack, tori applies technique).
- 24 attacks ordered by progressive difficulty.
- Ikkyo → Rokkyo elbow-techniques in technical complexity order.
- Kyu/dan checkpoint gates: students cannot advance until mastery demonstrated.
- Each technique includes paired ukemi mastery (the receiver's role is itself trained).

**KATA-CHECKPOINT**: a paired-form curriculum LLM pretraining scheme. (1) Define a sequential lattice of training "kata-stages" S_1...S_M ordered by difficulty (token-level complexity, syntactic depth, reasoning steps). (2) Each stage has a checkpoint evaluation E_i that must be passed (E_i ≥ θ_i) before advancing. (3) Paired drill: each stage contains *paired* training examples (uke prompt, tori response) where the model is trained on both initiating-the-question and completing-the-response sides. (4) Mastery gate: if E_i < θ_i, repeat S_i with adaptive data resampling.

## Adjacency
- Curriculum Learning LLM Pretraining 2601.21698
- Beyond Random Sampling 2506.11300
- Curriculum-Guided Layer Scaling 2506.11389
- LR Decay Curriculum 2511.18903

Expected FAIL — curriculum learning + checkpoint gating is mainstream.
