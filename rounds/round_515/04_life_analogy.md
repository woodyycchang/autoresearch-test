# Life Analogy — Hawaiian hula hālau kumu-alaka'i synchronized formation

The **hālau hula** (Hawaiian hula school):
- **Kumu** = master teacher; maintains style integrity passed down through lineage.
- **Alaka'i** = student leader, models style for others.
- **Students** = synchronized row formations with kumu/alaka'i at front.
- 4 basic steps (kāholo, lele, hela, 'uwehe); shoulders steady, knees bent invariant.
- Training: dance until "imprinted in sinews" (procedural memory).
- Style integrity maintained across generations via kumu-lineage.

**HULA-HALAU-KUMU-ALAKAI-FORMATION-PHASE-LOCK**: 3-tier phase-locked formation with kumu-style invariant + alaka'i intermediate-lead + student-row sync. (1) **Kumu LLM K** (high-capacity teacher): emits style-anchor embedding e_kumu defining current generation's style invariant. (2) **Alaka'i LLM A** (mid-tier student-leader): receives e_kumu + emits formation-leader step (lead-of-the-row); A's output is the per-step "front-row" exemplar. (3) **Student LLMs {S_1, ..., S_R}** (R-row formation): each S_i mimics A's step phase-locked at lag-i (slight phase offset proportional to row distance) — exact lag-locking. (4) **Kumu-style invariant loss**: L_kumu = sum_i ||emit_i - kumu_proj(emit_i)||^2 keeps all rows within kumu's style manifold (4 basic step variants); the 4 basic steps + shoulder-knee invariants encoded as fixed projection constraints. (5) **Sinew-imprint memory**: per-student, accumulated procedural-memory weights w_si update slowly (low LR for invariant moves, higher for new moves). (6) **Lineage style continuity**: kumu K periodically refreshes from previous-generation-kumu archive (style integrity transmission). (7) Differs from R094 PHYLLOTAXIS (golden-angle, no 3-tier) + R426 HAKA (synchronized stamp, no lineage) + R472 BAYANIHAN (community lift) + R477 LAUNEDDAS-TRIPLE-LOCK (1-drone+2-melody, no lineage) + R490 BOUZOUKI-TETRACHORD-COUPLE (4-course octave) + R502 CASTELL-PINYA-TRONC by 3-tier kumu-alaka'i-student + phase-lag-locked row formation + kumu-style-invariant loss + sinew-imprint slow-LR procedural memory + lineage style refresh.

## Adjacency
- GQA Grouped Query Attention (closest grouped)
- Hierarchical Attention Graph Learning RSC 2026
- MLA Multi-Head Latent Attention
- Multi-Stage Hierarchical Frameworks

Expected FAIL — GQA + MLA + hierarchical attention + grouped-formation literature fully covers.
