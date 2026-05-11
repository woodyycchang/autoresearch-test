# R236 — life analogy

## Source domain: wayang kulit dalang single-performer multi-role
- ONE dalang (puppeteer/narrator) is the entire performance: voices dozens of characters distinctly (king/clown/hero/villain), provides percussive cues (kepyak/cempala), conducts the gamelan orchestra, narrates, sings, and improvises on a known story-frame (Mahabharata/Ramayana).
- Key principle: the dalang is one PERSON but expresses MULTIPLE INDEPENDENT VOICES. Each character has a distinct vocal register, gestural style, and dramatic rhythm. The story is the same (canonical), but the realization varies with the dalang's interpretation.
- Constraint: the WHOLE PERFORMANCE flows from a single body; voice switches happen WITHIN A BREATH. There is no agent-coordination overhead.

## LLM analogy candidate
**Single-model dalang-style multi-role engine with shared latent scaffold**: instead of spawning N separate role-playing LLM instances (multi-agent literature), use ONE base model with a learned "dalang scaffold" — a compressed latent code combining (scene-frame, character-list, current-active-character) — that is prepended to every decode step. Character-switching is performed by modifying ONLY the (current-active-character) slot of the scaffold; the (scene-frame, character-list) slot persists across the entire conversation. Switching is sub-token (within a decode step) and incurs no agent-spawn overhead. The scaffold can be authored offline (declarative story) or inferred online (improvised). This gives wayang-kulit-style single-instance multi-voice generation with persistent narrative coherence — no inter-agent message passing.

## What differs from prior art (claim)
OpenCharacter (2501.15427), PsyPlay (2502.03821), Talk-Less Call-Right (2509.00482) achieve multi-persona via PROMPT engineering or finetuning. They don't propose a structured (scene-frame, character-list, active-character) latent scaffold that is single-token switchable mid-decode. Multi-agent role-playing literature uses N separate model invocations. The dalang framing is one-instance, sub-token switchable, with a persistent scene-frame slot.
