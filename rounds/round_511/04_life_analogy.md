# Life Analogy — Estonian Seto leelo polyphonic lead-chorus call-response

The **Seto leelo** (Estonian Setomaa polyphonic, UNESCO ICH 2009):
- Lead singer (sõnu ütõlja) delivers each new verse line.
- Choir (kiitja) joins on final syllables + repeats whole line.
- Solo accompanying voice (torrõ).
- Women-led tradition; King's "Mother of Song" honor on Seto Kingdom Day.
- Lead improvises new verses; chorus uses fixed pattern.

**SETO-LEELO-LEAD-IMPROV-CHORUS-FIXED-GATE**: lead-improvise + chorus-fixed context-gating. (1) **Lead-LLM** L_lead produces emit-line (free improvisation, high-temperature creative tokens). (2) **Chorus-LLM bank** {C_1, ..., C_K} = K fixed-pattern responder modules (each C_k holds a "chorus pattern" — a learned response template). (3) **Final-syllable gate**: at each line-end, L_lead emits a gate-signal g ∈ {1, ..., K} (selected by content of last-token-embedding); chorus C_g is activated to complete the line. (4) **Repeat-whole**: chorus C_g, after completing the final-syllable join, repeats the whole-line input (verifies parsing, locks meaning, smooths). (5) **Mother-of-Song improvisation reward**: L_lead receives bonus when emit-line is novel (low n-gram-overlap with prior lines in conversation) AND a chorus-pattern can match it (cross-verifier match — improvisation needs to be matched, otherwise no completion). (6) **Torrõ solo accompaniment** = a low-bandwidth third channel = a single low-frequency anchor stream that ties together L_lead + C_g (anchor token like attention sink). (7) Differs from R397 + R412 BEDOUIN + R435 + R444 + R461 KHIPU + R474 NADIRCLAW + R486 KBACH-GESTURE-VOCAB + R499 TSHACHU-TEMP-GATED by lead-improvise + chorus-fixed-pattern + final-syllable gate-signal + improvisation-match cross-verify reward + torrõ low-frequency anchor channel.

## Adjacency
- Qwen3 Gated Attention NeurIPS 2025
- LLM-Guided Gating Mechanism
- Unified Routing Cascading ICLR 2025
- Mixture of Experts gating
- Multi-Agent debate

Expected FAIL — attention gating + routing + MoE + cascade selection literature fully covers.
