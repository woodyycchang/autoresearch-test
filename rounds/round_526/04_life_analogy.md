# Life Analogy — Faroese føroysk-húgva knitted-shawl 3-panel topology with diamond+cable+decrease-ladder pattern grid

The **Faroese shawl** (Føroysk hálstrøa):
- Three structural panels: 2 triangular side panels + 1 trapezoidal back gusset.
- Bottom-up construction: hundreds of stitches cast on at hem; structural decreases at panel boundaries narrow upward toward neck.
- Diamond + lattice + cable motif grid: each motif cell is a topologically-typed pattern unit; boundary between motifs is a defect line.
- Decrease ladders create vertical defect seams running from hem to neck; these are the deliberate topological singularities required for fit.
- A skilled knitter mis-counting at the decrease ladder produces a pattern misalignment that propagates — a topologically-detectable winding-number drift along the panel boundary.

**FAROESE-3-PANEL-DEFECT-LADDER-WINDING**: per-attention-head topology classifier with 3-panel cellular decomposition + diamond/cable motif vocabulary + decrease-ladder winding-number signature + misalignment-defect propagation tracker. (1) **3-panel cellular decomposition**: attention pattern partitioned into 3 head-class panels P_side1, P_side2, P_gusset by per-head feature clustering; each panel has its own internal motif distribution. (2) **Diamond/cable motif vocabulary V_motif**: 5 canonical motif templates {diamond, lattice, cable-twist, lace-hole, plain} fitted to local 4×4 attention windows; per-head dominant-motif histogram. (3) **Decrease-ladder winding-number signature**: cumulative orientation winding of dominant attention direction along the panel-boundary trajectory; expected to monotonically wind by 2π per layer-depth band in a healthy model. (4) **Misalignment-defect propagation tracker**: defect detected when winding-number drift exceeds ±π/4 within a single layer; propagates along boundary like a knit-miscount cascading through subsequent rows. (5) **Repair finetune**: per-defect localized LoRA patch on the offending head-boundary subspace. (6) Differs from R501 BAGAJDA-BORE-PROFILE-ATLAS (centroid mahalanobis defect, no panel decomposition + no motif vocabulary + no winding-number signature) and R514 ROSEMALING-C-S-STROKE-CURVE-VOCAB-DEFECT (2-primitive C-S curve + winding-number topology, no 3-panel decomposition + no decrease-ladder + no misalignment-propagation) and R476 IDRIJA-LACE-DEFECT (lace bobbin defect, no panel decomposition + no motif vocabulary) by 3-panel cellular decomposition + decrease-ladder winding-number signature + 5-motif vocabulary + misalignment-defect propagation tracker.

## Adjacency
- TOHA Topological Divergence Attention Hallucination 2504.10063
- Hidden Holes Topological Language Models 2406.05798
- Vulnerability Detection TDA Attention Maps 2410.03470
- Attention Sinks Topological TDA Vietoris-Rips

Expected FAIL — TDA on attention literature + topological defect literature cover.
