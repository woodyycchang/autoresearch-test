# Life Analogy — Tlingit totem pole composite reading

Tlingit/Haida clan crest totem poles are composite narrative artifacts. Key features:
- **Bottom-up importance**: bottom figure is most important (bears the weight); Western viewers wrongly read top-to-bottom.
- **Composite reading**: meaning emerges only when prior knowledge of clan stories is available; figures are signposts not text.
- **Crest ownership context**: the *same* figure means different things depending on which clan claims it.
- **Master storyteller reading**: a knowledgeable reader points to each figure sequentially while reciting the associated story.

The totem pole is not decodable in isolation — it requires a *paired knowledge base* (the clan story corpus) and *bottom-up segment-by-segment* recitation tied to clan-context-disambiguation.

## Analogical mapping → LLM output composition

- Totem pole figure stack ↔ K decoded narrative segment stack
- Bottom-up reading order ↔ reverse-order generate-then-revise decoding (deepest segment first)
- Clan-story knowledge base ↔ shared anchor RAG context
- Crest-ownership disambiguation ↔ context-dependent token disambiguation
- Master storyteller pointing ↔ per-segment grounding-citation pass

The mechanism: a *bottom-up segment-recitation decoder* — generate the deepest / lowest-segment first, anchor to a shared retrieved knowledge base, then build upward narrative composition citing segment-disambiguation at each step.
