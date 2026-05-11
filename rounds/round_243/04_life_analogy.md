# R243 — life analogy

## Source domain: capoeira ginga rhythmic baseline
- Ginga is the constant rhythmic baseline footwork of capoeira: a continuous A-B-C-A-B-C sway maintained at all times. Every attack/defense LAUNCHES from a phase of the ginga and RETURNS to the ginga.
- Berimbau (bow instrument) dictates tempo; capoeiristas synchronise their ginga to its rhythm.
- Functional property: the ginga is BOTH idle (when nothing is happening) AND launch-platform (when an attack is mounted). The capoeirista's body is never STATIC — always in ginga even if nothing else.

## LLM analogy candidate
**Ginga-baseline idle reasoning**: when an LLM is at LOW LOAD (between user requests or with low-confidence input), instead of going silent, it runs a continuous BACKGROUND IDLE LOOP: low-temperature self-reflection generation over a rolling 5-step buffer of recent context. Each "ginga step" is one short auto-completion of "What ambiguity in user context could surface in the next request?" or "What background fact about user might be relevant later?". Outputs are stored in a rolling background-reasoning buffer. When a user request arrives, response generation LAUNCHES from a current background buffer state (rather than from scratch) — saving warm-up tokens and giving the LLM a pre-rumbled context. Idle ginga = continuous reasoning baseline; user-request response = launch-from-ginga.

## What differs from prior art (claim)
LLMs Have Rhythm (2502.20589) is FINGERPRINTING via inter-token time, not behavioral baseline. RHYTHM (2509.23115) is temporal tokenization for time-series prediction, not idle-baseline reasoning. The capoeira-ginga discipline of CONTINUOUS BACKGROUND REASONING with user-request-launches is not retrievable in surveyed prior art.
