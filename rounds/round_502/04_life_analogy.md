# Life Analogy — Catalan castell human-tower phase-coordinated rise

The **castell** (Catalan human tower):
- 3 components: pinya (base ring distributing weight) + tronc (trunk levels, 9-people-per-ring max) + pom de dalt (top 3 levels of children).
- For tallest towers: folre (2nd base) + manilles (3rd base) added above pinya for additional weight distribution.
- Built in **2 phases**: (a) pinya forms first, then signal/music starts; (b) tronc + pom de dalt rise rapidly to minimize lower-level weight strain.
- UNESCO Intangible Heritage 2010. Motto: força, equilibri, valor i seny.

**CASTELL-PINYA-TRONC-PHASE-RISE**: phase-coordinated layered attention with explicit base/trunk/top role differentiation + 2-phase build schedule. (1) Layer 0 (pinya) = weight-distributing K-head ring; receives all inputs and re-broadcasts to upper layers; high-fanout to absorb output gradient. (2) Layer 1-N (tronc) = stacked Multi-Head Attention with 9-head-per-layer cap (canonical castell ring constraint). (3) Layer N+1 (pom de dalt) = 3-head-light "child" top with small projection dim. (4) Inference: 2-phase — first compute pinya broadcast (no upper computation until pinya settles, controlled by gating coherence-score); then upper-tronc + pom proceed in tight wall-clock synchrony (step-locked, no out-of-phase activation). (5) Drop-detection: if upper-tronc coherence < τ, pinya catches via fallback re-broadcast (collapse-safety). (6) Differs from R477 LAUNEDDAS-TRIPLE-LOCK (1-drone+2-melody triplet, no base-ring weight distribution + no collapse-safety).

## Adjacency
- Hierarchical Attention papers (closest)
- Multi-Head Attention variants (Raschka 2026)
- Hierarchical Memory / Layer-Stack inference (INLG 2025 survey)
- Coherence Head literature

Expected FAIL — hierarchical multi-head attention + phase scheduling + coherence-head literature fully covers.
