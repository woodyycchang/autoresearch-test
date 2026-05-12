# Life Analogy — Lithuanian sutartines polyphony

Lithuanian **sutartines** are an ancient polyphonic vocal tradition featuring:
- **Interlocking voices**: 2-3 singers perform overlapping but offset melodic phrases.
- **Strict canon entries**: voices enter at staggered intervals; voice B starts when voice A reaches a specific point.
- **Second-interval harmony**: voices are deliberately tuned to dissonant seconds (~180 cents), producing "maximum roughness" that the human ear cannot resolve into a single line.
- **Indivisible texture**: removing one voice destroys the texture; all voices must coexist.

This is a different musical paradigm from common-practice harmony — instead of consonance + voice independence, sutartines uses controlled dissonance + tight phase coupling.

## Analogical mapping → LLM KV-cache / attention

- Voice 1 / Voice 2 / Voice 3 ↔ 2-3 interleaved attention streams
- Canon-entry offset ↔ phase-staggered token entry into KV cache
- Second-interval ↔ deliberately near-but-not-equal embedding pair
- Tight phase coupling ↔ inter-stream attention reads cross-coordinated entries

The mechanism: rather than a single sequential KV cache, partition into K interleaved staggered sub-caches that each contain near-duplicate but phase-offset keys; the model attends across all K sub-caches with a "roughness" penalty on within-second-interval matches, creating attention that resolves to a richer composite representation.
