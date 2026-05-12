# R264 — life analogy

## Source domain: hagfish slime defense
- Hagfish glands hold tightly coiled protein thread skeins + mucin vesicles.
- When attacked, hagfish releases skeins+mucin into seawater.
- In <400ms the skeins UNWIND and mucin SWELLS, producing 10,000× volumetric expansion of slime, which clogs predator's gills.
- The slime is mostly water — the threads are a scaffold for trapping water that suffocates the gill-breathing attacker.
- Key principle: SMALL stored payload × MASSIVE expansion via environmental coupling = resource-asymmetric defense.

## LLM analogy candidate
**Slime-expansion adversarial-input throttling defense (SEAIT)**: when a context-aware prompt-injection or adversarial-input attack is detected (via cheap classifier), the LLM emits a precomputed COMPRESSED CONTEXT "skein" — a small token-payload that DECOMPRESSES into a massive context that fills the attacker's available context budget. The decompression happens via a recursive prompt that expands a small seed into a large quasi-random scaffold ("water-trapped"). Critical: the defender pays cheap (the small skein is precomputed) but the attacker pays expensive (must process the expanded scaffold to extract useful signal). Distinct from rate limiting: SEAIT doesn't refuse the request; it consumes the attacker's budget asymmetrically. Distinct from honeypots: honeypots are static decoys; SEAIT is an active expansion in response to detection.

## What differs from prior art (claim)
ARGUS (2605.03378) provenance verification. DataFilter (2510.19207) input filtering. Multi-Agent Defense Pipeline (2509.14285) specialized defenders. None retrieve a SKEIN-EXPANSION resource-asymmetric throttle that absorbs attacker compute via in-context recursive expansion.
