# R273 — life analogy

## Source domain: Tibetan thangka pigment preparation
- Raw minerals (lapis, malachite, cinnabar, orpiment) are hand-ground for days to fine consistent powder.
- Each pigment requires a binder (yak-hide glue) of strength MATCHED to the pigment's density and weight:
  - Light pigments (e.g., powdered earth): weak/standard binder.
  - Heavy pigments (e.g., gold powder): exceptionally strong binder so the dense particles don't sediment or flake.
- Gold leaf/powder requires a CLEAR strong binder so the gold's brilliance is not obscured.
- Key principle: BINDER STRENGTH scales with PIGMENT DENSITY/IMPORTANCE.

## LLM analogy candidate
**Pigment-density-matched precision allocation (PDMPA) quantization**: in mixed-precision quantization, allocate bit-precision to each weight matrix based on its INFORMATION DENSITY — a per-matrix scalar combining (a) gradient-magnitude statistics, (b) singular-value concentration, (c) downstream-impact estimate. High-density matrices (e.g., the embedding layer, attention output) get HIGH precision (binder-strength); low-density matrices get aggressive quantization. The KEY refinement: the precision ALLOCATION rule is EXPLICITLY PROPORTIONAL to a measured density scalar (not just hand-tuned per-layer), and is CLEAR — i.e., quantization-error spectrum is monitored and the precision-density curve refined automatically. Distinct from mixed-precision quantization that uses fixed bit-width per layer: PDMPA uses a continuous density-binder scaling rule.

## What differs from prior art (claim)
Mixed-Precision Quantization (2510.16805), Systematic LLM Quantization (2508.16712), Binary Weight+Activation PTQ (2504.05352) cover mixed/static precision allocation. None retrieve a CONTINUOUS density-proportional binder-strength precision allocation rule with auto-refinement from quantization-error spectrum monitoring.
