# R321 — life analogy

## Source: Wallace's flying frog patagium
- Webbed toes + lateral skin flaps form patagia.
- Frog spreads patagia mid-fall to create lift drag — controlled descent up to 15m.
- Adhesive toe discs soften landing.

## LLM analogy
**PATAGIUM-CONF**: at decoding time, when model encounters high-uncertainty token, deliberately spread "patagia" — emit a small bundle of low-confidence companion tokens (uncertainty interval markers) that act as drag-creating descent stabilizers. Final output includes the predicted token + confidence-interval companions; adhesive landing = downstream verifier matches the interval.

## Differs from prior art (claim)
ConfTuner verbal confidence. Interval-based uncertainty for LLM judges. Verbalized confidence elicitation. PATAGIUM-CONF wraps prediction with companion uncertainty markers — close to verbalized confidence + interval methods.
