# Life Analogy — Bulgarian gajda bagpipe bore-profile defect atlas

The **Bulgarian gajda** (Rhodope bagpipe):
- Chanter (gaidanitsa) has a conical bore with up to **seven subtle changes** along its length.
- Distinctive **flea-hole** (marmorka) — small extra hole covered by left index finger — raises any played note by a half step, producing characteristic ornamentation.
- Drone + chanter + blowpipe; goatskin bag.
- Regional variants: Thrace/Dobrudja (high), Shope (mid), Rhodope (deep kaba gaida).
- A defective bore (warped, cracked, or miscoupled chambers) produces detectable resonance signature deviation from canonical regional profile.

**BAGAJDA-BORE-PROFILE-ATLAS**: catalog each attention head's projection-matrix singular spectrum (Q, K, V leading-direction angle + spectrum-shape vector) against a learned atlas of K canonical "bore profile" centroids; mark head as defective if mahalanobis distance to nearest centroid exceeds threshold + parallel flea-hole channel records half-step deviation in singular angle. (1) Atlas of K canonical bore-profile centroids learned on healthy-head population (clean fine-tuned base). (2) Per-head bore profile = (σ_1, σ_2/σ_1, θ_QK, spectral-shape histogram). (3) Defect score = mahalanobis distance to nearest centroid + flea-hole channel scoring half-step (π/24 rad) deviation in θ_QK. (4) Residual cluster (head profiles not matching any centroid) flagged as defective. (5) Repair via projection-to-nearest-centroid finetune. (6) Differs from R476 IDRIJA-LACE-DEFECT (graph-minor canonical-motif atlas) by spectrum-profile-centroid representation + flea-hole half-step deviation channel.

## Adjacency
- Attention Head Survey 2409.03752 (head taxonomy)
- Attention Head Entropy ICLR 2025 (entropy defect score)
- Head Pruning / FedHead literature
- Mech-Interp circuit analysis

Expected FAIL — attention head taxonomy + entropy-based defect detection + pruning fully covered.
