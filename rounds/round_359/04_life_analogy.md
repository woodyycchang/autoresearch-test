# Life Analogy — Etruscan haruspex Liver of Piacenza 16-section divination

The Etruscan **Liver of Piacenza** is a bronze model of a sheep's liver inscribed with the names of 16 deities, each governing a specific anatomical zone. The trained haruspex priest performed divination by:
- Examining a freshly sacrificed sheep's liver.
- Locating each anatomical zone on the actual organ.
- Mapping abnormality/normality in each zone to the deity that ruled it.
- Producing a structured deterministic report: "Tinia (north zone) shows X → war is auspicious; Fufluns (south-east zone) shows Y → harvest will fail."

Key features:
- **Fixed deterministic 16-zone grid** (no interpretation freedom in the mapping itself).
- **Per-zone fixed semantic anchor** (each zone = one deity = one domain of life).
- **Trained reader** required to perform mechanical zone identification.
- **Composite output** = 16 independent per-zone judgments concatenated, not a free-form holistic verdict.

The Liver of Piacenza is essentially a **rubric template** with structural / deterministic semantics — the haruspex's output is a structured 16-tuple, not free-form text.

## Analogical mapping → LLM evaluation rubric

- 16 anatomical zones ↔ K-dimension fixed rubric grid
- Per-zone deity ↔ per-rubric-dimension named criterion
- Liver of Piacenza as a template ↔ shared template enforced across all evals
- Trained haruspex ↔ judge LLM following deterministic per-zone lookup
- Structured 16-tuple output ↔ K-tuple deterministic per-dimension judgment

The mechanism: a **strictly deterministic K-zone rubric template** (no free-form holistic score) where each zone maps via a fixed lookup table to a named criterion + scoring scale; the judge LLM is forced to emit a K-tuple judgment with no interpolation between dimensions. Closest existing approach is DAGMetric / Analytic Rubric — the haruspex novelty is "fixed-template-as-cosmic-grid" enforcement.
