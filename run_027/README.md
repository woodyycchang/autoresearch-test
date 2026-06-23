# Run 27 — Physicist-Style Discovery (collaborating agents)

Tests a THIRD path for niche discovery, distinct from combination/unification
(Runs 24-25) and anomaly-hunting (Run 26), both of which saturated.

Operationalizes physics thinking-moves as distinct COLLABORATING agents:
1. AGENT-DIRAC      — formal derivation: from a real structural property of ML,
                      derive what the math implies should exist but is unlooked-for.
2. AGENT-EINSTEIN-AHA   — radical reframe: "X is actually Y in disguise".
3. AGENT-EINSTEIN-CRITIC — brutal adversarial kill (most ideas should die).
4. AGENT-BOHR-FILTER    — crazy-enough (paradigm) AND testable (falsifiable).
5. AGENT-REDUCTIONIST + AUDIT — deepest mechanism + the single test; then audit.

Agents are separate `claude -p --model opus` processes (genuine independence),
run in a non-git tempdir. The orchestrator runs the gating WebSearches itself
(formal-property realness, critic prior-art, grounded-gap) and records raw JSON.

Gates: G1 real-formal-property | G2 quarantine | G3 survives critic + grounded-gap
       | G4 Bohr (radical AND concrete falsifiable prediction).
R13: a reframe MUST make a DIFFERENT testable prediction than the standard view,
     else it is vacuous relabeling (reject).
