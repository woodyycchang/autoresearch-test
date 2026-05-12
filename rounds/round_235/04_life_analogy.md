# R235 — life analogy

## Source domain: yam-pounding fufu two-person rhythm
- Two roles: POUNDER (raises and drops a heavy pestle in rhythmic strikes) and MODERATOR (sits low, hands enter mortar between strikes to turn/moisten the yam mass).
- Coordination is rhythmic and tight: moderator's hand MUST be out before pestle drops. The risk is hand crushed if rhythm slips. This forces SUB-BEAT phase alignment.
- The pounder commits to the rhythm; the moderator's hand-in/hand-out windows are determined by the pounder's strike phase, NOT by negotiation.
- Adding more pounders (3-6) requires harder rhythm: each adds an offset (counterpoint phase) to keep work continuous without strike collisions.

## LLM analogy candidate
**Phase-locked two-agent edit-correction loop**: two LLM agents alternate at fixed sub-token rhythm. Pounder agent emits short blocks of generation (5-10 tokens) at predictable cadence. Moderator agent runs between pounder strikes: while pounder waits for a fixed inter-strike interval Δt, moderator reads pounder's last block and inserts a single correction edit (delete-and-replace, position-anchored) committed at strike+Δt/2. Critical: moderator does NOT pause the pounder. The pounder commits to the rhythm; the moderator's edit window is fixed-width. Misaligned edits (moderator overruns Δt/2) are silently dropped — the pounder strikes regardless. This produces a continuous, predictably-paced output stream where corrections happen at fixed phase offsets, not via blocking dialogue. Extending to N pounders gives N counterpoint phases (each pounder offset by Δt/N).

## What differs from prior art (claim)
LLM-MAS literature (2605.02801 orchestration, 2508.04652 MARL, 2501.06322 survey) uses turn-taking or simultaneous decoding but rarely FIXED RHYTHM with strict phase-locked windows + silent edit drop on overrun. The yam-pounding discipline of "commit to rhythm; subordinate roles fit in fixed-width gaps; misalignment is silently dropped not negotiated" is distinctive.
