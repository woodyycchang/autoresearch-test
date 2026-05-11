# R231 — life analogy

## Source domain: morin khuur sympathetic-overtone playing
- The morin khuur has TWO strings tuned to F and Bb. The F string carries the fundamental melody; the Bb string is bowed lightly or "answers" via SYMPATHETIC RESONANCE — the player induces specific overtones (Bb', F'', B'', F''' at successive natural harmonic node positions) on the Bb string by adjusting bow pressure / position while playing the fundamental on F.
- The TWO-CHANNEL output (fundamental F + selected overtone Bb) creates the characteristic biphonic morin-khuur timbre. Both channels share the same physical instrument, so any tension change couples them.
- Notably distinct from Tuvan throat singing (R213): morin-khuur is INSTRUMENTAL biphonic; Tuvan khoomei is VOCAL biphonic.

## LLM analogy candidate
**Sympathetic-overtone speculative decoding**: a model decodes a sequence on the fundamental channel (greedy or argmax token-by-token) while a TIED secondary "overtone channel" simultaneously samples from a frequency-shifted distribution P_overtone(t) = softmax((logits - logits_fundamental_shift) / τ_o) that produces speculative variants AT the harmonic positions of the fundamental sequence. The overtone channel is bowed at HARMONIC NODE positions (where the fundamental's prefix probability mass has a local maximum), not at arbitrary positions. Both channels run in parallel; the overtone tokens are verified against the fundamental's next-token distribution; if they pass an acceptance test, the fundamental sequence absorbs the overtone variant as an alternative-continuation seed for branching beam search. This is structurally distinct from standard speculative decoding (which proposes the NEXT token from a draft) — the overtone proposes ALTERNATIVE BRANCHES at harmonic-node prefix positions, exploiting the same fundamental's logit field.

## What differs from prior art (claim)
Parallel Prompt Decoding (2405.18628) and DiP-SD (2604.20919) use a single model to draft + verify next-token. Promise-based scaling (2502.11517) decouples decode into promise-chains. None proposes the morin-khuur structure of a TIED second channel sampling alternate-branch tokens at fundamental-prefix-harmonic positions, with sympathetic-coupling between channels (bow-pressure analog).
