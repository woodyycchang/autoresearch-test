# R327 — life analogy

## Source: Bat (CF) Doppler-shift compensation
- Constant-frequency bat keeps emitted-call frequency well below its acoustic fovea (e.g., 83kHz emit / 84kHz fovea reference).
- Approach to prey produces Doppler upshift in returning echo (e.g., +1kHz).
- Bat lowers its emitted-call frequency by exactly the predicted shift so the returning echo always lands in the high-resolution fovea band.
- Audio-vocal feedback loop: continuously monitors echo frequency error and corrects vocal output to cancel out self-motion contamination.

## LLM analogy
**FOVEA-DECODE**: streaming-decode tokenizer with motion-velocity-aware compensation. Whenever the decoder's "context velocity" (cosine drift between sequential hidden states, normalized per-token) changes, the positional-encoding base or RoPE θ is dynamically re-targeted so the relative-position similarity always lands on the same "fovea" of attention sharpness regardless of decode rate. Feedback signal = recent hidden-state drift rate; correction signal = positional-encoding base adjustment.

## Differs from prior art (claim)
RoPE/ALiBi positional encoding is fixed at training time. Streaming positional encoding adjusts for context length but not for instantaneous decode-rate drift. Continuous speech tokenizer handles raw audio not LLM internal velocity. FOVEA-DECODE introduces a closed-loop drift-rate→encoding-base correction so attention stays optimal regardless of decode-rate variation.
