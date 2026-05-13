# Life Analogy — Tuareg inadane lost-wax silver casting

**Inadane lost-wax casting** (Tuareg silversmith):
1. Sculpt detailed BEESWAX model of desired final piece.
2. Build CLAY MOLD around wax model (layered, dried, durable).
3. Heat mold → wax MELTS OUT, leaving cavity matching exact shape.
4. Pour MOLTEN SILVER into cavity; cool.
5. Break clay mold to reveal silver piece — IDENTICAL to wax model.

The unique principle: **two-mold-medium one-shot replication** — the wax (cheap, deformable) is the design substrate; the clay (refractory) is the mold; the silver (functional) takes the wax's shape via one-pass casting. The wax is SACRIFICED; the silver is the output. The mold (clay) is also broken — destroyed in extraction.

## Analogical mapping → one-pass parameter extraction via two-stage mold

- Wax model (design substrate, sculptable) ↔ a small lightweight DRAFT MODEL trained on target task
- Clay mold (refractory, holds shape during transfer) ↔ a TASK-SPECIFIC DISTILLATION DATASET capturing the wax's behavior
- Silver (functional, valuable) ↔ a frozen pretrained large LLM
- Pouring silver ↔ a single FINE-TUNING PASS over the LLM matching the distillation dataset
- Breaking the mold ↔ discarding the dataset and draft model after extraction

The mechanism: **INADANE-CAST single-shot mechanism-import via wax-clay-silver pipeline** — (1) sculpt a small draft model D_wax for target task T (e.g., 100M params trained from scratch); (2) generate a focused distillation dataset M_clay from D_wax outputs (e.g., 10K Q-A pairs covering T); (3) fine-tune frozen LLM L_silver for ONE PASS on M_clay using a strict no-overfit regularizer; (4) discard D_wax and M_clay. The novelty is the SACRIFICIAL TWO-MEDIUM pipeline + STRICT ONE-PASS extraction. Differs from (a) standard KD (teacher-student with iterative training), (b) self-distillation (model serves as own teacher), (c) MiniPLM (multi-pass training), (d) Muon-Optimized Distillation (specific optimizer not pipeline) by combining (i) SACRIFICIAL draft model + (ii) DISCARDED distillation dataset + (iii) STRICT ONE-PASS fine-tune extraction.

## Note on adjacency

The mechanism-import form fits. Adjacent: knowledge distillation, dataset distillation, one-shot pruning (SparseGPT). Distinct: TWO SACRIFICIAL media (draft model + dataset) BOTH discarded; single-pass extraction discipline.
