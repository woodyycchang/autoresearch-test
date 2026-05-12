# R340 — life analogy

## Source: Barn owl asymmetric ear (vertical ear offset)
- Left ear opening higher, right ear lower (asymmetric on vertical axis).
- ITD (interaural time difference) encodes azimuth.
- ILD (interaural level difference) encodes elevation — only possible because of asymmetry.
- Asymmetry CREATES a vertical localization dimension that two symmetric ears could not encode.

## LLM analogy
**ASYM-DUAL-PATH**: information-cascade architecture with TWO parallel input pathways that have BUILT-IN asymmetric encoding bias (path A weighted toward early-token features, path B toward late-token features). The difference between the two streams is computed and INJECTED back as an additional feature channel, encoding sequence-position level information that neither path can encode alone. Mechanism: deliberate asymmetry as information-creation, not just redundancy.

## Differs from prior art (claim)
Standard parallel attention heads symmetrize. Decorrelation via sparse connectivity is symmetric. Asymmetric NN inheritance (2602.09509) is about parent-child weight inheritance not parallel-path asymmetry. ASYM-DUAL-PATH differs by ENCODING information-content in the asymmetry-induced ILD-style channel between two parallel pathways.
