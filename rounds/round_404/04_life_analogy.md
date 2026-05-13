# Life Analogy — Sundanese angklung (octave-pair shaken ensemble)

The **angklung** is a Sundanese bamboo instrument:
- Each unit consists of **TWO bamboo tubes** in an **octave pair** (high tube + low tube) mounted on one frame.
- Each unit sounds a SINGLE pitch when shaken.
- In ensemble, **one player ↔ one unit ↔ one pitch class** — melodies are produced by HOCKETING across players.
- The octave-pair structure means each pitch is voiced with BOTH octaves simultaneously (parallel-doubled).

The unique principle: **single-pitch unit composed of two octave-paired oscillators activated together** — when any single unit fires, two octave-related tones sound together as a single event. The pair always fires; the player can't fire just one tube. Plus the hocketed ensemble assembles a melody from many such octave-pair units, each "owning" one pitch class.

## Analogical mapping → MoE octave-paired expert routing

- Angklung unit ↔ a 2-expert paired sub-cluster in an MoE layer
- Octave pair ↔ the two experts in the pair are functionally aligned (sub-cluster shares activation)
- Single-pitch ownership ↔ each pair specializes in one input cluster (gated by k-means/router)
- Hocketed ensemble ↔ MoE routing distributes tokens across pairs

The mechanism: **ANGKLUNG-OCTAVE 2-shard paired expert routing** — in a sparse MoE layer with N experts, group experts into N/2 PAIRS (E_a^(i), E_b^(i)). The router routes a token to a PAIR not an individual expert; the pair fires both experts on the same token, but with REDUCED individual capacity (each expert in a pair has half the FFN hidden dim of an unpaired expert). The two experts in a pair share an octave-pair correspondence: their FFN weights are tied so W_b^(i) = O · W_a^(i) where O is a fixed sparse "octave operator" (e.g., a fixed permutation matrix that maps low-freq to high-freq encoding). This forces the pair to produce a structured 2-component output rather than a single one. Top-k routing operates at the PAIR level. Differs from (a) GShard top-k expert routing (no pair), (b) DeepSeek shared expert (only one shared, not paired), (c) MoHGE heterogeneous grouped experts (group not octave-paired) by using FIXED OCTAVE-PAIR weight tying + PAIR-LEVEL routing.

## Note on adjacency

The multi-agent-comm form fits: MoE is a multi-expert sparse system. Adjacent: MoHGE grouped experts. Distinct: explicit FIXED OCTAVE-COUPLED weight relation (W_b = O W_a) between pair members instead of independent learned weights. Closest twin: paired-expert tied-weight MoE (if any exists).
