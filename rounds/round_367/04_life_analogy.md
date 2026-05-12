# Life Analogy — Indonesian gamelan kotekan interlocking parts

**Kotekan** is the Balinese gamelan technique of **interlocking parts**: two players (polos = on-beat, sangsih = off-beat) produce notes alternately. Neither part is musically complete alone; together they form a single fast composite figuration (faster than any single player could execute).

Key properties:
- **Two complementary parts** that interleave temporally.
- **Each part is sparse** (every other note); together they are dense.
- **Speed advantage**: composite tempo > 2× either part's solo tempo.
- **Roles fixed by convention** (polos = on-beat anchor; sangsih = off-beat fill).
- **Two players, one melody** — listener perceives one fast line.

## Analogical mapping → LLM decoding allocation

- Two interleaving players ↔ two interleaved sub-channels of a decoder
- Polos on-beat ↔ "anchor token" sub-channel (every other token)
- Sangsih off-beat ↔ "fill token" sub-channel (alternate every other)
- Composite tempo > 2× ↔ effective decoding throughput > 2× single-channel
- Listener perceives one melody ↔ output stream perceived as single sequence

The mechanism: **two-channel interleaved sub-decoders** where channel A produces tokens at positions {0,2,4,...} and channel B produces tokens at positions {1,3,5,...} of the output sequence. Each channel is sparse (skips alternate positions) so each operates on a coarser per-channel target rate, but the interleaved composite output is at full token rate. Critical: A and B share an attention trunk but use disjoint OUTPUT POSITION assignments, requiring no synchronization beyond strict positional alternation.
