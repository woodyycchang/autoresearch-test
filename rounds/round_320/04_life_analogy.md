# R320 — life analogy

## Source: Anasazi kiva ventilation
- Underground ceremonial chamber with central hearth.
- Vertical intake shaft + deflector stone between shaft and fire.
- Deflector redirects incoming cold air UPWARD, preventing it from extinguishing the fire.
- Result: stable fresh-air circulation around central focus.

## LLM analogy
**KIVA-DEFLECT**: context-window with central attention focus + entry-side fresh-token shaft + DEFLECTOR layer that redirects incoming-token activations upward to attention sink (not directly onto central focus). Prevents new noisy tokens from disrupting central reasoning state.

## Differs from prior art (claim)
StreamingLLM (2309.17453) uses attention sinks at SEQUENCE START. SinkTrack (2604.10027) anchors first token as information anchor. KIVA-DEFLECT routes NEW incoming tokens through deflector to existing sink — but the redirection-to-sink mechanism is essentially attention sink usage.
