# Life Analogy — Welsh penillion cerdd dant counter-melody

The **Welsh penillion / cerdd dant** (Welsh: 'string music'):
- Solo singer improvises a counter-melody against a FIXED harp melody.
- The harpist plays a pre-known tune (cerdd dant); the singer (penillion) overlays a poetic counter-melody.
- Performance is duel-like — the singer adjusts in real time to fit harp phrasing.
- The mechanism: counterpoint with one FIXED voice (harp) and one IMPROVISED voice (penillion); harmony emerges through non-redundant complementation, not unison.

## Analogical mapping → LLM 2-agent counter-improvisation

- Fixed harp melody ↔ Agent A: fixed-policy "harp" emitting primary answer
- Improvised vocal counter-melody ↔ Agent B: "penillion" agent observing A's stream and emitting phase-offset alternative
- Counterpoint constraint ↔ KL/MI regularizer enforcing non-redundancy
- Bardic duel ↔ adversarial coevolution loop with judge

The mechanism: **PENILLION-COUNTER** — a 2-agent design where Agent A produces a "harp melody" answer following its fixed policy, and Agent B produces a "penillion" counter-melody by ATTENDING to A's token stream and ENFORCING phase-offset complementation via a non-redundancy regularizer (e.g., KL divergence above ε between A's and B's logits). Final output = harmonic resolution of A + B by a third aggregator agent. Differs from Multi-Agent Debate (which seeks consensus), RECONCILE (weighted vote), Multi-Agent Counterpoint Generation (music-only).

## Note on adjacency

Closest LLM-side prior art: Multi-Agent Debate, RECONCILE confidence-weighted voting. The "fixed-vs-improvised" asymmetry is a small variation. AAMAS 2026 KL-constrained per-agent literature is the directly adjacent technique. Music-counterpoint LLM literature exists (Magenta, MusicLM) but at output-token level not at architecture level.
