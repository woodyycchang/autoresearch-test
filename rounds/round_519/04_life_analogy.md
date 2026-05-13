# Life Analogy — Pakistani Qawwali sama-listener trance evaluation

The **mahfil-e-sama** (Sufi qawwali listening gathering):
- Lead vocalist + harmonium + tabla + chorus — qawwali ensemble.
- Audience-listener experiences a continuum: kaif (mild enthusiasm) → kaifiyat (engagement) → hal (trance) → wajd (ecstasy) → fana (annihilation).
- Word-repetition with variation gradually induces trance.
- Adab (comportment rules) at sama gatherings.
- Trance markers: kanpna (trembling), eye-closure, head-movement, breath-pattern.

**QAWWALI-SAMA-TRANCE-CONTINUUM-EVAL**: 5-stage emotional-arousal evaluation with audience-trance signal + word-repetition-variation arousal-inducing reward + adab comportment constraint. (1) **5-stage hal continuum** = ordinal evaluation labels {kaif, kaifiyat, hal, wajd, fana} for output engagement-quality (instead of binary good/bad). (2) **Listener-trance proxy**: per-output, an LLM-as-listener evaluates and outputs a hal-continuum score s_h ∈ {0, ..., 4}; this proxies emotional-arousal-trace. (3) **Word-repetition-with-variation reward**: training reward boosts outputs that demonstrate **repetition + variation** structure (lexical bigram repeats with controlled morphological variation — induces audience hal). (4) **Adab comportment constraint**: outputs must conform to adab rules (no obscenity, no abrupt topic shift, no flat affect, etc.) — penalty constraint set. (5) **Kanpna trembling marker**: token-level "tremble-detector" measures attention-weight high-variance moments as proxy for output evoking trance. (6) **Lead-vocalist + chorus dual evaluator**: 2-channel evaluation (a high-capacity lead + a chorus consensus) — lead provides nuanced, chorus provides reliability. (7) Differs from R481 KHOOMEI-PARTIAL-JUDGE (harmonic-partial multi-criteria) + R494 NECHUNG-3-TIER-EVAL (trance-medium-council) + R506 KANUN-BESA-PRECEDENT-TRIBUNAL by 5-stage continuum + word-repetition-variation reward + adab comportment constraint + kanpna trembling marker + lead+chorus dual eval.

## Adjacency
- LLMs-as-Judges Survey 2412.05579
- Multi-Turn Dialogue Evaluator 2508.00454
- Eliciting Emotions LLMs CHI 2025
- GUIDELLM LLM-Guided NAACL 2025

Expected FAIL — LLM-judge ensemble + multi-turn evaluator + emotional-arousal literature fully covers.
