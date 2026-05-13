# Life Analogy — Ainu inau tiered curl prayer stick

The **Ainu inau** (Hokkaido indigenous wooden ritual prayer-stick):
- Carved from a single willow/dogwood stick from the top down, producing **whorls of curled shavings**.
- **Tier count** (how many curl rings) encodes the magnitude/urgency of the request to the kamuy.
- **Shaving direction** (top-down vs. side-on / "winged" shutu) encodes which kamuy is addressed and what is being requested.
- Used in nusa shrines + iyomante bear-sending ritual; size and tier-count vary with the request.
- The mechanism: magnitude communicated by **discrete repetition / multiplicity of identical curl primitives**, not by amplitude or by adjective-strength.

## Analogical mapping → LLM prompt magnitude encoding

- Curl tier-stack ↔ instruction-repetition stack at prompt level
- Single curl primitive ↔ atomic instruction sentence
- Tier-count = magnitude ↔ K-repetition-count = priority level
- Direction encodes target kamuy ↔ a directional header token at start of each repetition routes the policy

The mechanism: **AINU-INAU-TIER-STACK** — a prompt magnitude encoding scheme where the same atomic instruction is **tier-stacked K times** at the start of the system prompt; K is the priority level (1 = mild, 5 = critical) and replaces adjective-amplitude (e.g., "very strongly please" → 5× identical "please" instructions). The decoder reads tier-count as magnitude rather than parsing strength adjectives.

## Note on adjacency

Strong adjacency to Leviathan 2512.14982 "Prompt Repetition Improves Non-Reasoning LLMs" (Google Research Dec 2025) — exact twin at K=2. The tier-K generalisation (K∈{1..5} as priority encoding) is a small extension. LessWrong + Lakera prompt-engineering literature documents tier-stack priority patterns. Expected verdict: FAIL with strong functional overlap.
