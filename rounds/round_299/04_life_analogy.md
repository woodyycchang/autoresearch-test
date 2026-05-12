# R299 — life analogy

## Source: Bowerbird bower costly signaling
- Male builds elaborate bower + collects rare ornaments (Solanum berries, blue objects) → demonstrates quality via costly investment.
- Handicap principle: signal is honest because cheap to fake = cheap to ignore; cost makes it reliable.

## LLM analogy
**BOWER-LLM**: explicit COSTLY-SIGNAL DECODING where the LLM emits formatted/cited/verified-step output (sources, calculations, table rows) ONLY when its underlying confidence is HIGH; output cost (token count) scales with reliability — cheap signal = low confidence, costly signal = high confidence. Inverse of current verbosity-compensation (LLMs verbose when UNCERTAIN); BOWER-LLM is verbose only when CONFIDENT.

## Differs from prior art (claim)
- Verbosity Compensation (2411.07858): documents LLMs being verbose when UNCERTAIN — opposite of BOWER-LLM's prescription.
- Length Inflation (2603.10535): tries to FIX excess length without trading off, not actively use length as signal.
- BOWER-LLM proposes intentionally INVERTING verbosity behavior: only invest tokens when confident. Open whether this is published as a deliberate strategy.
