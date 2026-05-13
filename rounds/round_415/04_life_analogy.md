# Life Analogy — Tibetan singing bowl partial-mode selective excitation

The **Tibetan singing bowl** (Himalayan ritual instrument):
- Bowl has multiple natural vibration MODES (fundamental + overtones), each with distinct frequency and spatial pattern.
- Player selectively excites different partials by varying (a) mallet position (rim vs centre vs lip), (b) mallet material hardness, (c) stroke direction (rub vs strike vs spin).
- Modes coexist: striking can excite multiple simultaneously, producing beating phenomena.
- Operational modal analysis (Wang AIP 2023) confirms radial + tangential modes concurrent + unstable mode rotating with puja angular velocity.

The mechanism: **selective excitation of distinct modal partials by varying input-driver location/direction/material** — different "strokes" produce different "voices" from the same instrument; samples maintained at fixed modal-frequency-ratio phase offset.

## Analogical mapping → LLM partial-mode decoder coverage

- Bowl modes ↔ distinct decoder output distributions (top-k logits subsets)
- Mallet position/stroke ↔ decoding strategy variant (top-k vs nucleus vs DSI)
- Modal frequency ratio ↔ phase offset between parallel samples
- Beating phenomenon ↔ output diversity from cross-sample coherence

The mechanism: **BOWL-PARTIAL** — phase-coherent multi-decoder strategy that runs K parallel decoders, each EXCITING a distinct logit-distribution mode by enforcing a phase offset in (temperature, top-p, repetition-penalty) parameter space. Phase offsets are placed at GOLDEN-ANGLE-DIVIDED points on the (T, p, r) cube to maximally cover decoder strategy space. At each step, K samples are emitted; final output chosen by judge over K modal samples. Differs from Diverse Beam Search (token-level dissimilarity reward not strategy-space phase offset), Arithmetic Sampling (single-strategy parallel only), Top-P/Min-P (single strategy) by combining (a) K-decoder strategy-space phase offset, (b) golden-angle-divided coverage, (c) judge-selection over modal samples.

## Note on adjacency

Strong adjacency:
- Diverse Beam Search (Vijayakumar 2016)
- Arithmetic Sampling (Vilnis 2023)
- DSI Mirostat Top-P literature
- R279 PTCH within-head harmonic (different LAYER but uses golden-angle reference)

Expected FAIL — multi-decoder phase-offset is recombinable from existing diverse-decoding literature.
