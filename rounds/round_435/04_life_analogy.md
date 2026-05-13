# Life Analogy — Akha hill tribe spirit gate

The **Akha spirit gate**:
- Every Akha village entrance has a wooden gate carved with male/female human figures + amulets.
- Function: filter at threshold — benign spirits invited in, malign spirits deterred.
- Both-sides carvings (appealing AND grotesque) for dual-purpose attract-benign / repel-malign.
- The gate is sacred: humans must not touch; the gate itself does the classification.

**AKHA-GATE-FILTER**: a non-touchable BINARY input-gate that classifies every incoming prompt as benign-token-friendly or malign-token-suspect via a dual-sided carving — one classifier head trained to recognize benign-context patterns and PROPAGATE, the other trained to recognize malign-context patterns and BLOCK. Both heads see the full input; both signals are mandatory; PROPAGATE & not-BLOCK → admit; otherwise drop or reroute to safety pipeline. The gate parameters are FROZEN (sacred) — never updated during model fine-tuning, mimicking the untouchable Akha gate.

## Adjacency
- PromptGuard Sci Reports 2025 (input gatekeeping + structured)
- Bypassing Prompt Injection Guardrails 2504.11168
- OWASP LLM01 Prompt Injection 2025
- Adversarial Tokenization ACL 2025

Expected FAIL — LLM input-gate binary classifier + dual-head benign-malign filtering is heavily covered.
