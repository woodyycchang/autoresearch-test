# Life Analogy — Welsh eisteddfod bardic chair cynghanedd cascade

The **eisteddfod bardic-chair** (Welsh, since 1176):
- Annual tournament: best awdl in strict cynghanedd 24-metre wins bardic chair.
- Winner (Prifardd) inherits chair lineage from prior winners.
- 24 strict metres codified 1523 Caerwys.
- Chair physically passes; lineage tracked.

**EISTEDDFOD-CHAIR-CASCADE**: tournament-cascade LLM generation with strict-meter constraint inheritance + chair-lineage best-of-N selection. (1) Generate N candidate outputs each under strict 24-metre constraint (cynghanedd-equivalent: structural+alliteration+rhyme). (2) LLM-judge selects winning candidate as 'bardic-chair winner'. (3) Subsequent generations inherit winner's constraint-satisfaction pattern (in-context examples or fine-tune signal). (4) Lineage tracking: maintain chain of prior winners' completions; new generations conditioned on chain. (5) Chair-physical lineage = fine-tune on winners' outputs. (6) Differs from plain best-of-N by chain-of-winners constraint-propagation.

## Adjacency
- Constrained Decoding Guiding LLMs (closest, 2403.06988)
- CRANE Reasoning + Constraint
- PoeTone Songci Constrained
- Awesome LLM Constrained Decoding

Expected FAIL — constrained decoding + best-of-N + in-context paradigms covered.
