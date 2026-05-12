# Life Analogy — Japanese kintsugi (golden joinery repair)

**Kintsugi** is the Japanese art of repairing broken ceramics with **urushi lacquer + gold dust** on the seam, deliberately HIGHLIGHTING the crack rather than hiding it. Features:
- Crack lines treated as part of the object's history.
- Repair is **in-place** — the original is preserved; only seams are sealed with lacquer + gold.
- **Visible**: the repair line is clearly marked, not camouflaged.
- **Permanent record** of damage: subsequent users can see where the object broke.
- Method preserves the original substrate intact — repair adds a thin layer at the boundary.

The unique principle: **visible permanent in-place repair with golden marker** — the boundary of the modification is explicitly visible and indexed, and the original substrate is unchanged.

## Analogical mapping → LLM model editing

- Original ceramic ↔ pretrained model weights
- Crack ↔ identified error region (factual / safety / capability fault)
- Lacquer ↔ small parameter delta applied at the fault region
- Gold dust ↔ explicit visible MARKER tracking which parameters were edited
- Subsequent visibility ↔ every future inference logs that this region was patched

The mechanism: a **golden-seam visible model edit** — when applying a knowledge / behavior edit at parameter coordinates Π ⊂ θ, the system (a) applies the standard delta Δθ_Π; (b) registers the edit in a **visible patch registry** with the diff, timestamp, edit-reason, signed hash; (c) inference logs include a flag whenever the edit's parameters are involved in the forward pass — producing a **gold-traceable** generation; (d) edits are **reversible** by registry rollback. Differs from prior ROME / MEMIT / KE / safety-policy prefix-patching by being **AUDIT-FIRST** — the patch's existence is a first-class invariant exposed to inference-time logging, not just at training-time.
