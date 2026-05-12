# Life Analogy — Maori tā moko (chiselled facial tattoo)

**Tā moko** is the traditional Maori facial tattoo, chiselled by *uhi* (chisels) into the skin (not punctured), producing textured grooves. Features:
- Each moko is **unique per individual**, encoding genealogy (whakapapa), life events, marital status, achievements.
- Functioned as **personal signature** — Maori chiefs signed land deeds with their moko.
- **Permanent and tamper-evident**: removing or altering the moko visibly damages the face.
- **Multi-dimensional**: lines/spirals encode multiple attributes simultaneously.
- **Public visibility** — moko is on the face, readable by anyone.

The unique principle: **persistent multi-attribute identity marker** carved directly into the substrate such that any modification is **physically visible**.

## Analogical mapping → LLM model fingerprinting

- Moko ↔ embedded fingerprint pattern
- Carved grooves ↔ permanent parameter-level modification
- Multi-attribute encoding ↔ multi-dimensional fingerprint payload
- Face visibility ↔ readout via fingerprint query
- Tamper-evidence ↔ fingerprint corruption detection

The mechanism: a **chiselled multi-attribute fingerprint** — embed fingerprint via small per-attribute weight perturbations at uhi-chosen coordinates (Π_a for attribute a). Each attribute encodes one identity field (model_id, owner, version, training_date). On fingerprint verification, query with attribute-specific probe Q_a returns response with attribute-dependent bias measurable via statistical test. The fingerprint is TAMPER-EVIDENT: any large perturbation to weights at Π_a destroys the attribute readout. Differs from prior single-bit fingerprinting (Markov Chain Lock, EditMF) by encoding MULTIPLE ORTHOGONAL ATTRIBUTES at MULTIPLE INDEPENDENT COORDINATE SETS, allowing partial-attribute readout.
