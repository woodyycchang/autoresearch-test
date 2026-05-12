# Life Analogy — Marshallese stick chart memorized navigation

Marshallese stick charts (rebbelib, meddo, mattang) are physical 3D maps showing **ocean swell patterns** + island positions, made from coconut-frond midribs and shells. The key feature is **chart usage protocol**:
- **Studied + memorized BEFORE voyage** (pre-trip prep).
- **NOT consulted during voyage** (left on shore).
- **At sea, navigator uses internal memory + body sense** (lying prone to feel canoe pitch/roll from swells).

The chart is a **TRAINING ARTIFACT**, not a runtime reference. After training, the navigator carries the chart *in his head* and reads the ocean via his body. The chart is functionally equivalent to a memorized lookup table baked into procedural memory.

## Analogical mapping → LLM training/inference separation

- Stick chart ↔ static training corpus / knowledge base
- Memorize before voyage ↔ pre-training / fine-tuning before deployment
- Don't consult during voyage ↔ no RAG/lookup at inference time
- Body senses + internal memory ↔ frozen parameters + working context
- Sensory navigation ↔ in-context streaming inference
- 4 main swell patterns ↔ K canonical embedded prototype patterns

The mechanism: a **pre-deployment memorize-then-deploy** training regime that *explicitly* prohibits runtime retrieval from external knowledge, forcing the model to internalize a SMALL set of canonical PATTERN PROTOTYPES (4 swell patterns, etc.) during fine-tuning and rely on COMBINING these prototypes during inference via in-context streaming inputs. Different from standard fine-tuning by enforcing memorization of canonical prototypes + retrieval-free inference + a deliberate small prototype dictionary.
