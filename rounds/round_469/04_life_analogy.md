# Life Analogy — Sherpa rope-team load redistribution

The **Sherpa** Himalayan rope-team:
- 10-20 loads per expedition, distributed across porters.
- Equal-load policy avoids friction; redistributable on injury/fatigue.
- Rope-team safety lines connect climbers across glacier; load can be relayed.
- Ahead-of-team Sherpas fix lines + carry forward, redistributing as conditions change.

**SHERPA-REDIST**: an orthogonal-subspace LoRA team with dynamic load redistribution. (1) Pool of M LoRA-adapters L_1...L_M each in mutually orthogonal subspaces (analog of distinct loads per porter). (2) Per-task-batch dynamic redistribution: load (gradient updates) reassigned across L_i based on fatigue (capacity saturation) — overloaded L_i sheds direction onto under-loaded L_j via partial subspace transfer. (3) Safety-line: shared low-rank base S_0 acts as connecting rope through which redistributed updates flow without breaking orthogonality. (4) Ahead-fix: a small "scout" adapter L_scout fixes the subspace before the main team's pass. (5) Equal-load enforcement: balanced gradient norm across L_i per training step.

## Adjacency
- O-LoRA EMNLP 2023
- Shared LoRA Subspaces 2602.06043
- Compress then Serve LoRA 2407.00066
- Distributed LoRA 2511.22880

Expected FAIL — orthogonal-subspace LoRA + redistribution well-covered.
