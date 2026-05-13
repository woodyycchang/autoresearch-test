# Life Analogy — Punjabi bhangra dhol dual-band attenuation

The **dhol** (Punjabi bhangra):
- Double-headed: bass-head (thick skin, dagga curved stick) + treble-head (thin skin, chanti straight stick).
- Layered rhythm: bass establishes phrase anchor, treble adds detail.
- Hand-damping mute for staccato attenuation between phrases.
- Chaal 4-beat syncopated pattern; bass-attenuation creates room for treble emphasis.

**BHANGRA-DHOL-DUAL-DAMP**: dual-band gradient attenuation for training stability with phrase-level damping. (1) Decompose each gradient g_t into low-frequency component (long-time-average baseline) g_L and high-frequency component (short-time deviation) g_H. (2) Independent attenuators α_L, α_H scale each band per phrase (per-block training step). (3) Hand-damping: at high-curvature phrase boundaries, apply temporary attenuation α_L → 0 (bass-mute) to allow precise high-frequency steering. (4) Chaal-pattern: syncopated 4-step cycle for bass-treble balance — every 4th step bass-attenuates 50%. (5) Phrase-level attenuation prevents bass-gradient dominance during transitions.

## Adjacency
- DAPO Clip-Higher + Dynamic Sampling (2025)
- GRPO group-relative advantage
- Damping-Factor-Control Frequency Compensation
- Gradient-Variance Reduction

Expected FAIL — dual-band gradient damping + clip-higher paradigm covered.
