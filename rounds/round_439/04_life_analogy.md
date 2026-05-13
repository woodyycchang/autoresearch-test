# Life Analogy — Hadzabe click language phonology

The **Hadza/Hadzabe** language (Tanzania Lake Eyasi):
- Click consonants serve as rare phonemic markers + discourse / emphasis tokens.
- Within an utterance, click marker functions as feedback / back-channel signal.
- Hadzabe language isolate; clicks + ejective + prenasalized consonants.

**HADZA-CLICK-ATTEN**: a per-token feedback-attenuation scheme where rare special-marker tokens (e.g., 'CLICK_FEEDBACK', emit-stop, certainty-marker, refusal-token) are EXPLICITLY suppressed in token logits during the body of a response, with logit-bias = -∞ except at sanctioned positions; sanctioned positions defined by an attention-gated emission predictor. Differs from generic logit-bias suppression by combining (a) rare-token catalog + (b) per-position emission gate + (c) feedback-attenuation interpretation.

## Adjacency
- Backchannel/Filler Representation 2509.20237
- Aligning Backchannel Dialogue OpenReview
- SIGDIAL 2025 Discourse Markers
- Token Reduction Collection

Expected FAIL — rare-symbol logit suppression + back-channel/filler modeling is well-covered.
