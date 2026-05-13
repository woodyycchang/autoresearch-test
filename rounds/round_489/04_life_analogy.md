# Life Analogy — Persian carpet medallion 4-fold rotational symmetry

The **Persian carpet medallion**:
- Centralised medallion with 4-fold (or 8-fold) rotational symmetry around carpet center.
- Symmetrical around longitudinal + transverse axes.
- Boteh teardrop motifs repeat in pattern with rotational equivariance.
- Defect detection: lacemakers/weavers check rotational consistency — broken symmetry signals defect.

**MEDALLION-ROT-DEFECT**: 4-fold-rotation equivariance check for attention pattern defect detection. (1) Per attention head, treat feature map F as 2D grid (rows × cols). (2) Apply 4-fold rotations R₀, R₉₀, R₁₈₀, R₂₇₀ around feature-map center; should be approximately equivalent under rotation in healthy heads. (3) Defect score d = max_θ ||F − R_θ · F||₂. (4) Defective heads: d > τ, flag for repair. (5) Repair: project F toward rotational-symmetric subspace via group-averaging F_repair = (R₀F + R₉₀F + R₁₈₀F + R₂₇₀F)/4. (6) Differs from R436 HUTSUL-PYSANKA (also 4-fold equivariance) by 4-fold-rotation defect detection + symmetry-group averaging repair.

## Adjacency
- PSC-YOLO Pinwheel-Shaped Conv (closest, 2025)
- Device Defect Intrinsic Rotational Symmetry
- DSAT Dynamic Sparse Attention
- FAX-Net Symmetric Attention

Expected FAIL — rotational symmetry defect detection paradigm fully covered.
