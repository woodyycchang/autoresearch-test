# Life Analogy — Japanese wabi-sabi tea-ceremony patina-aging

The **Sen no Rikyū wabi-sabi** tea ceremony:
- Aesthetic of transience + imperfection (sabi = beauty through age/decay).
- Raku tea-bowls intentionally embrace cracks, chips, glaze irregularity.
- Bamboo scoops + weathered wood + moss-on-stone — gradual fading is valued.
- Tea-ceremony utensils accumulate patina (a controlled decay signature).

**WABI-PATINA**: a graceful-decay feedback-attenuation training schedule. (1) Each training signal sample s_t is assigned an *aging timestamp* τ_t. (2) Loss weight w(s_t) = exp(-(now - τ_t)/T_patina) with patina half-life T_patina varying per task category (fast for stale-info, slow for principled-skill). (3) Patina-controlled SFT/RL replay: old examples lose loss-weight but never deleted — preserve full corpus, attenuate signal. (4) Cracked-bowl analog: explicit "controlled imperfection" — small fraction (5%) of intentionally weighted noisy/erroneous samples preserved at full loss-weight to maintain epistemic humility. (5) Patina schedule learned by validation-loss curvature.

## Adjacency
- Mitigating Forgetting SFT Preference OpenReview
- WSO Warmup-Stable-Only 2603.16127
- Unlearning That Lasts OpenReview
- Continual Learning RL Wolfe substack

Expected FAIL — graceful-decay loss schedules well-developed.
