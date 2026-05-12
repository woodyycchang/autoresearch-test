# Life Analogy — Mau Piailug star compass + wave pilotage

Master navigator Mau Piailug guided Hokule'a Hawaii→Tahiti using only:
- **Star compass**: 32 named houses for star rising/setting points (fixed celestial reference).
- **Swell pattern reading**: persistent ocean swells maintain bearing when stars are obscured.
- **Multi-cue dead reckoning**: sun + stars + swells + wind + clouds + birds + fish.

Cross-fleet relay tradition: multiple canoes maintain mutual visibility and check each other's positions. If one canoe drifts off-bearing, the swell pattern + star compass + cross-fleet visibility correction restore it. Piailug famously broke a familial-lineage tradition by training a non-Carolinian (Nainoa Thompson), thus *relaying* navigation knowledge across cultures.

Key features:
- **Fixed celestial reference** (star compass houses) common to all navigators in the fleet.
- **Persistent environmental signal** (swells) decoupled from current visibility.
- **Cross-canoe consistency check** — drift one canoe → others correct.
- **Single trained navigator per canoe** is the consensus owner.

## Analogical mapping → LLM multi-agent navigation

- Star compass 32 houses ↔ fixed shared reference frame (consensus-shared embedding axis)
- Swell pattern ↔ persistent low-frequency context signal
- Cross-canoe visibility ↔ multi-agent peer-consensus check
- One trained navigator per canoe ↔ one consensus-owner agent per workflow node
- Relay knowledge transfer ↔ teacher→student-agent skill transfer across fleet

The mechanism: a fleet of K agents share a FIXED star-compass-style reference frame for spatial bearings; each agent maintains its own swell-pattern (persistent low-frequency context); cross-agent visibility yields drift-correction consensus pulls; one designated "navigator" agent per local cluster owns the consensus decision and relays it to peer clusters. **The novel part is the FIXED SHARED REFERENCE FRAME (star compass) as the anchor for consensus, not the consensus mechanism itself.**
