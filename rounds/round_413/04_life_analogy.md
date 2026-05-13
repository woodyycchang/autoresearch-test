# Life Analogy — Sherpa Khumbu Icefall rope-ladder cascade

The **Sherpa Khumbu Icefall route** (Everest base-camp ascent):
- "Icefall Doctors" install fixed ropes + aluminum ladder bridges before climbing season.
- For wide crevasses, multiple ladders are LASHED TOGETHER in cascade — chain of 2-3 ladders each spanning a part of the gap.
- Each rope segment is anchored with ice-screws at both ends; carabiner clip-in REQUIRED at every anchor.
- A climber must CLIP-IN to a new anchor before UNCLIPPING from previous — no unanchored moments.

The mechanism: **cascading multi-segment crossing with mandatory anchor-handoff at each segment boundary** — each segment is independently verified before traversal; transition between segments has clipped-overlap to prevent failure.

## Analogical mapping → LLM cascading multi-hop reasoning

- Crevasse ↔ knowledge gap requiring retrieval/reasoning
- Fixed-rope segment ↔ reasoning step
- Ice-screw anchor ↔ checkpoint with explicit verification
- Carabiner clip-in/out overlap ↔ output-of-step-N becomes input-of-step-N+1 with explicit re-verification
- Lashed-ladders cascade ↔ multi-step decomposition with overlap handoff

The mechanism: **SHERPA-RAPPEL** — a cascading multi-hop reasoning protocol with explicit anchor checkpoints at each step boundary AND mandatory verification overlap. Each reasoning step k produces (a) output_k, (b) anchor_check_k (a self-consistency probe verifying the step's claim against the input), (c) next-step-input formed by COMBINING output_k AND anchor_check_k. Step k+1 cannot proceed unless anchor_check_k passes (CLIP-IN to new anchor before UNCLIPPING from previous). Final answer = output_K where K is dynamically chosen by step controller. Differs from generic CoT (no per-step anchor check), Chain-of-X paradigms (no mandatory overlap), CoT-RAG (RAG-only checkpoint) by combining (a) per-step explicit anchor_check, (b) MANDATORY OVERLAP — step k+1's input includes step k's anchor_check, (c) dynamic step-count K.", "novelty_claim": "Chain-of-X survey, CoT-RAG, Sketch-of-Thought, CoT-faithfulness measurement all cover per-step verification. SHERPA-RAPPEL recombines explicit anchor + mandatory overlap. Recombination of existing components.

## Note on adjacency

Strong adjacency:
- Chain-of-X paradigms survey (COLING 2025)
- CoT-RAG integration (EMNLP 2025)
- Sketch-of-Thought adaptive (EMNLP 2025)
- Self-Consistency CoT (Wang et al)

Expected FAIL — checkpoint+verification chain reasoning is well-explored.
