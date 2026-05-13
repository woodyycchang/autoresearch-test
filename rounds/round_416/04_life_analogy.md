# Life Analogy — Xylem cohesion-tension (continuous water column under negative pressure)

The **cohesion-tension theory** of plant water transport:
- Transpiration at leaves creates **NEGATIVE PRESSURE** (tension) at the top.
- This tension is transmitted DOWN through an **unbroken continuous water column** in the xylem.
- Cohesion (hydrogen bonds between water molecules) keeps the column intact even under tension.
- Adhesion to xylem wall + capillary action support the column.
- Cavitation (gas bubble) breaks the column; small perforations PREVENT spread of cavitation.

The unique principle: **demand-side pull through a passive continuous medium** — the work is done at the top (transpiration); the column passively transmits the demand downward via cohesion. The medium itself does NO active work; it just maintains continuity under tension.

## Analogical mapping → top-down demand-driven residual stream propagation

- Leaves transpire ↔ output layer / final loss
- Negative pressure / tension ↔ a "tension signal" propagating BACKWARD from output to input through residual stream
- Continuous water column ↔ residual stream maintained across all layers
- Cohesion ↔ identity skip connection that preserves the tension signal verbatim
- Cavitation ↔ activation discontinuity (e.g., dead ReLU, layer norm flush)
- Small perforations preventing cavitation spread ↔ per-layer LayerNorm/RMSNorm gates that PREVENT discontinuities from propagating

The mechanism: **XYLEM-TENSION continuous-cohesion residual propagation** — augment standard residual stream with a SECONDARY "tension stream" T_l that is INITIALIZED at the output layer's loss-gradient negative direction and propagates BACKWARD through layers via T_{l-1} = α T_l + (1-α) f_l(h_l) with α=0.95 (strong cohesion). The tension stream provides a forward-pass-time "demand signal" from output to input that is concatenated with each layer's input. Differs from (a) standard residual (identity not weighted-cohesion), (b) RNN backward states (sequential not parallel), (c) U-Net skip connections (single-skip not cohesion-chain), (d) Peri-LN (normalization not cohesion stream) by combining (i) SECONDARY tension stream + (ii) WEIGHTED COHESION α-blending + (iii) OUTPUT-INITIALIZED top-down propagation in forward pass.

## Note on adjacency

The information-cascade form fits. Adjacent: backward residual, U-Net skip, output-aware encoder. Distinct: WEIGHTED-COHESION TENSION STREAM initialized at output and propagating backward through forward pass.
