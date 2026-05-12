# R268 — life analogy

## Source domain: wheat threshing + winnowing
- **Threshing** loosens grain from stalk/husk via mechanical agitation (beating, animal-tread).
- **Winnowing** uses an external AIRFLOW: the threshed mixture is tossed into the wind. Lighter chaff is BLOWN ASIDE; denser grain falls VERTICALLY back. Passive physics; no per-grain inspection.
- Key: a SCALAR PROPERTY DIFFERENCE (density) + a UNIFORM EXTERNAL FORCE (wind) does separation cheaply at scale without examining each particle.

## LLM analogy candidate
**Threshing-winnowing data filter (TWDF)**: a two-stage corpus cleaning protocol:
- **Threshing**: a cheap noisy mechanical agitation pass that randomly perturbs each doc with small token shuffles + paraphrasing. Docs that LOSE meaning under this perturbation (measured via embedding shift) are "loosely-attached" content — like grain on stalk, easy to separate.
- **Winnowing**: a cheap uniform classifier (lightweight LLM scoring a single scalar density-signal — e.g., information density per token) is applied; below threshold docs are blown aside. No per-doc deep inspection.
The protocol is INTRINSICALLY CHEAP: agitation is regex-level; the density score is a single scalar. Distinct from LLM-judge filters that do deep per-doc inspection. Distinct from clustering: no pairwise comparison.

## What differs from prior art (claim)
Quality-Gated Corpus Refinement (2602.09875), REWIRE (2506.04689), Multilingual LLM Filter (2505.22232) use LLM-judge expensive per-doc inspection. TWDF is a PURELY SCALAR-DENSITY uniform-pass filter inspired by physical winnowing — no per-doc judge call. The agitation + density-scalar combination is the distinguishing piece.
