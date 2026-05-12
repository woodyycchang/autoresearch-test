# Life Analogy — Senegalese gris-gris tied amulet

The Senegalese **gris-gris** is a West African (Mande) protective talisman:
- Small **cloth bag** containing Quranic scripture and ritual objects.
- **Tied with cord** to neck, arm, waist (physical attachment to body).
- Worn for protection from harm; the *binding* is itself part of the protection.
- **Layered**: scripture → bag → cord → body, each layer adds protection.
- Removal of the amulet removes the protection.

Distinctive feature: the **physical binding** (cord/string) is constitutive of the protective function — an untied gris-gris is not protective. The protection requires *active continuous physical attachment*.

## Analogical mapping → LLM identity preservation

- Cloth bag containing scripture ↔ encrypted/signed safety/identity LoRA module
- Tied with cord ↔ cryptographic binding of safety LoRA to base model
- Layered protection ↔ multi-axis verification (signature + hash + presence-check)
- Removal removes protection ↔ if safety module unbound, base model refuses to operate
- Continuous attachment ↔ runtime presence check at every forward pass

The mechanism: a **bound safety LoRA** that is *cryptographically tethered* to the base model so that (a) the LoRA cannot be removed without breaking model output (model refuses to operate without it); (b) the LoRA cannot be modified (signed); (c) every forward pass checks for the LoRA's presence via a small verification gate that emits NaN/refusal if absent. This makes safety inseparable from the model at runtime — different from optional adapter-merge where safety can be silently dropped.
