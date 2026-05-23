# Run 10 epoch 1 — Recursive failure root-cause analysis

## R-Step 1: Failure summary

Run 10 epoch 1 yielded **15 survivors** after L8 cross-source diversity gate
(vs Run 9's 0). However, **saturation checks via web_search** showed every
surviving combination already has an existing paper that bridges the two atoms:

| Combo cluster | Survivors | Saturation paper |
|---|---|---|
| belinda_li × world_models JEPA | 3 | H-JEPA / ACT-JEPA / Causal-JEPA extend JEPA to embodied agents (already published) |
| amrith_setlur × RLHF reward hacking | 8 | PURE (arXiv:2504.15275) min-form credit assignment for reward hacking |
| lecun × retrieval_augmented | 2 | TI-JEPA / VL-JEPA bridge JEPA + retrieval (already published) |
| sparse_autoencoder × world_models | 2 | SparseJEPA (arXiv:2504.16140) already exists |

**Substantive niche count: 0.**

## R-Step 2: NEW root cause (not in persistent_knowledge_base)

### FAILURE_ROOT_CAUSE_6: HOT_TOPIC_ARXIV_SATURATION

Description: arXiv 2024-2026 corpus itself concentrates on the same hot topics
(JEPA, MoE, RLHF, RAG, SAE). Injecting arXiv abstracts from these popular
research clusters fails to escape the saturation constraint because the
combinatorial space is ALREADY occupied by cross-papers (e.g., SparseJEPA bridges
sparse-autoencoder × JEPA before our pipeline even tries).

Binding severity: **HIGH** (15 of 15 epoch 1 survivors hit this).

Empirical evidence: all 4 distinct topic combos that survived L8 had ≥1
existing cross-paper retrieved by saturation search.

## R-Step 3: Counter-paper search (≥3 web_search per new root cause)

For RC_006:

1. **arXiv:2510.16720** "Beyond Pipelines: A Survey of the Paradigm Shift
   toward Model-Native Agentic AI" — explicitly identifies the shift away
   from pipeline-prompt-stitched agents toward unified end-to-end-trained
   agents. NOT yet a saturated cross-topic.
2. **arXiv:2512.04119** "Humanity in the Age of AI: Reassessing 2025's
   Existential-Risk Narratives" — contrarian challenge to recursive
   self-improvement assumption. Cold topic; few cross-papers.
3. **arXiv:2509.23586** "Improving the Efficiency of LLM Agent Systems
   through Trajectory Reduction" — efficiency-of-agent-systems is
   under-explored (cited as such).
4. **arXiv:2605.01280** "Position: LLM Serving Needs Mathematical
   Optimization and Algorithmic Foundations, Not Just Heuristics" —
   under-explored algorithmic-foundations critique.
5. **arXiv:2604.17312** "A Survey of RL for LLMs under Data Scarcity" — data
   scarcity is a less saturated angle than reward hacking.
6. **arXiv:2510.25441** "Grounded in Reality: Learning and Deploying
   Proactive LLM from Offline Logs" — offline log learning is less saturated
   than online RLHF.

Counter-method: COLD_TOPIC_INJECTION. Replace the hot-topic arXiv atoms with
under-explored / contrarian / position-paper atoms whose topic clusters have
fewer cross-papers.

## R-Step 4: Pipeline fix applied

`arxiv_atom_injector.py` extended with `COLD_TOPIC_ABSTRACTS` (6 new atoms
spanning model-native agentic AI, contrarian existential risk, efficiency of
agent systems, algorithmic foundations of serving, RL under data scarcity,
offline-log proactive LLM).

Saturation check threshold tightened: an L7 saturation hit on any single
existing cross-paper now disqualifies the candidate (Run 9 + Run 10 epoch 1
used a softer hit-counter that allowed 1-2 hits).

## R-Step 5: Plan for epoch 2

Re-run pipeline with cold-topic-augmented atom pool. Expected outcome:
fewer raw survivors but each survivor more likely to bridge two
under-explored clusters and survive saturation.
