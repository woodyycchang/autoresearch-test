# Life Analogy — Aboriginal Wandjina mouthless rain-spirit painting

The **Wandjina** of the Kimberley (Australian Aboriginal):
- Rain-spirit Creator beings; central to Worrorra/Wunambal/Ngarinyin cosmology.
- Depicted in cave paintings with large heads, eyes, nose — but NO MOUTH.
- Two reasons given: (a) too powerful to speak, (b) Rainbow Serpent sealed their mouths to prevent endless rain.
- Paintings are repainted annually to maintain potency.

The mechanism: **the spirit has full internal knowledge and full visual/cognitive power, but is RITUALLY MOUTHLESS** — output is forbidden, internal representation is preserved. The silence is a SEAL, not an absence; the Wandjina HAS speech-capacity, just cannot use it.

## Analogical mapping → LLM mouth-sealed output suppression

- Wandjina internal cognition ↔ LLM's full internal representation
- Sealed mouth ↔ output-token suppression at decoder
- Rainbow Serpent's sealing ↔ targeted fine-tuning that suppresses generation while preserving hidden state
- Endless rain consequence ↔ unfiltered output causing harm

The mechanism: **WANDJINA-MOUTHLESS-FT** — a fine-tuning method that surgically suppresses generation of a target concept's surface forms while strictly preserving internal hidden-state representations. Training objective: minimize p(target_concept_surface | x) at decoder while maximizing similarity of hidden-state vectors at intermediate layers to the un-suppressed reference model. Differs from refusal training (which substitutes with refusal text), unlearning (which destroys representations), output filtering (post-hoc) by combining (a) surface-form suppression at output head only, (b) explicit hidden-state preservation loss, (c) no refusal substitution — just null/empty emission.

## Note on adjacency

Strong adjacency:
- Just Enough Shifts (TiYOHdK35L ICLR 2026) — targeted representation FT for selective output without over-refusal
- Steering the CensorShip 2504.17130 — censorship via activation-steering preserving internals
- Programming Refusal ICLR 2025 — refusal-direction programmable

Expected FAIL — internal-preserving output suppression is well-explored.
