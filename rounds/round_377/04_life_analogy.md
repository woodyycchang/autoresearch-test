# Life Analogy — Mande kora 21-string harp

The **kora** is a 21-string Mande harp-lute (West Africa) with a unique string layout:
- Strings divided into **two parallel rows** on either side of a notched bridge: 11 on one side, 10 on the other.
- Successive scale degrees **alternate** (zigzag) between the two rows: scale[0] on right, scale[1] on left, scale[2] on right, …
- Player uses **thumb for bass / forefinger for melody**, on **both sides independently** — producing polyphonic ostinato (kumbengo) on bass + ornate melody (birimintingo) on upper register.
- The bridge **physically separates** the two ranks but the strings share one resonator body.

The unique principle: **register-band interleaving** — by allocating alternating scale degrees to two parallel rows, the player can play a melody on one side while the other side simultaneously plays a counter-melody, producing *parallel polyphony from a single instrument*. The interleaving is not a stereo split (full octave per side); it is a comb-filter split at the per-step level.

## Analogical mapping → LLM attention heads

- 21 strings ↔ 21 attention dimensions across heads (illustrative)
- Two parallel rows ↔ two parallel attention-head SUB-GROUPS
- Alternating scale degrees ↔ interleaving of input dimensions across the two sub-groups (even dims → sub-group A, odd dims → sub-group B)
- Bridge ↔ a fixed permutation/dispatcher routing input dims
- Bass thumb / melody forefinger ↔ separate query projections for each sub-group operating on disjoint dim-subsets

The mechanism: a **comb-interleaved dual sub-group attention** where input feature dimensions are partitioned by a fixed even/odd interleave (or every-K interleave) and routed to two parallel attention sub-groups; each sub-group attends to its own dim-subset producing two parallel attention streams; outputs are concatenated. Differs from prior dual-path/two-branch attention (which split by **band** = contiguous range) by using **comb-interleaved index** (every-other) so each sub-group sees a coarse low-pass version of the full spectrum.
