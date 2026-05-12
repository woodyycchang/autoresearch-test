# Life Analogy — Yemeni mafraj qat-chew narrow-window session

The Yemeni qat-chew is a daily afternoon ritual bounded by:
- **Hard start** (post-noon prayer, ~1-2 pm)
- **Hard stop** (pre-sunset prayer, ~5-6 pm)
- **Single shared physical room** (the *mafraj*, top of tower-house)
- **Drug-mediated peak** ("Solomon's hour" near end) when participants enter focused private-thought state
- **Reset between sessions** — each session is independent; no carryover state from previous day's mafraj

Importantly, the session is *productive* despite being narrowly time-bounded: business deals are struck, political discussions happen, music is played. Cognitive output happens only in the bounded window — outside the window, nothing is processed.

## Analogical mapping → LLM context-window gating

- Mafraj room ↔ active context window for one session
- Prayer-bounded start/end ↔ hard gate-open / gate-close events
- Solomon's hour peak ↔ scheduled high-attention burst within the session
- Reset between sessions ↔ inter-session KV clear / context reinitialization
- Productive bounded session ↔ time-bounded focus burst yielding distilled output

The mechanism: **hard cyclic gate** that opens the attention/context-window only during a per-session window with a *scheduled-peak burst* in the middle of the session, and zeroes attention outside the window — different from continuous sliding-window attention because the gate is *event-driven* (prayer-bell-style external trigger), not token-position-driven.
