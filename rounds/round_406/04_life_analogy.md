# Life Analogy — Bhutanese gho hemchu private-fold pocket

The **Bhutanese gho hemchu**:
- Gho is a knee-length men's robe; kera belt folded three times around the waist.
- Folding action creates a large pouch at the chest — the **hemchu** — used to carry personal items (food, bowl, dagger, phone, wallet).
- Items in hemchu are private: not visible externally; accessible only by unfastening kera or reaching through a specific fold-opening.
- Folding/access protocol is ritualised: kera-tucking direction encodes social status (left vs right).

The mechanism: **fold-pocket creates a private storage accessible only by ritual unfold protocol**, with items normally invisible/unattended-to.

## Analogical mapping → LLM private context-pocket

- Hemchu pouch ↔ designated private subspace of context window
- Items in pouch ↔ sensitive tokens (PII, system credentials, scratchpad)
- Unfolding ritual ↔ privileged-instruction signal to access pocket
- Status-encoded tuck direction ↔ canary-token verification of access privilege

The mechanism: **GHO-HEMCHU-POCKET** — a context-gating design where designated "hemchu pocket" tokens in the context window are MASKED FROM DEFAULT ATTENTION but accessible via a cryptographically-signed "unfold" signal in the system prompt. The unfold signal is verified via a canary token (status-bit) in the prompt header; only legitimate elevated-privilege instructions trigger pocket-revelation. Differs from regular scratchpad (always-accessible), KV cache (no access control), privacy-preserving SP-FT (parameter-level not token-level), MSA routing keys (retrieval not gating) by combining (a) attention-mask gating, (b) cryptographic unfold-trigger, (c) per-pocket canary verification.

## Note on adjacency

Strong adjacency:
- Hidden Scratchpad (Substack)
- ICLR 2026 scratchpad 2510.27246
- Engineering Trustworthy LM Agents with Scratchpads
- MSA Memory Sparse Attention (routing keys for retrieval)
- Instruction Hierarchy (R401 reference)

Expected FAIL with strong functional overlap.
