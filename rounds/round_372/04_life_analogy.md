# Life Analogy — Cherokee syllabary Sequoyah's invented orthography

**Sequoyah** invented the Cherokee syllabary in the 1820s as a one-man project:
- He observed European "talking leaves" (writing) and recognized literacy as power.
- First tried **logograms** (one symbol per word) — too many symbols (thousands).
- Pivoted to **syllabary** — one symbol per syllable; 85 symbols sufficient.
- 12-year solo development; achieved mass Cherokee literacy in months.

Key principles:
- **Mid-granularity unit**: between alphabet (too small) and word-list (too large).
- **Closed inventory**: 85 fixed symbols cover all Cherokee syllables.
- **Designed from scratch**: not derived from existing scripts.
- **Optimal-size sweet spot**: too few = ambiguity; too many = unmemorizable.

## Analogical mapping → LLM tokenization

- Logograms (one per word) ↔ word-level tokenization (e.g., naive word vocabulary)
- Syllables (Cherokee) ↔ subword tokens (BPE) at the *syllable* granularity
- 85-symbol closed inventory ↔ small fixed-size vocabulary
- Designed from scratch ↔ language-specific invented tokenizer

The mechanism: a **deliberately small fixed-size vocabulary** (e.g., 100-200 tokens) of **syllable-granularity invented tokens** trained from scratch on a low-resource language, where the tokenizer is co-designed with the model rather than borrowed from a large multilingual base. The Cherokee insight is that a *carefully designed mid-granularity inventory* dramatically outperforms either character-level or word-level on certain languages.
