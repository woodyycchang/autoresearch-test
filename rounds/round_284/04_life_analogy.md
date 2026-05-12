# R284 — life analogy

## Source domain: Inuit skin-on-frame kayak
- Two-part construction:
  - FRAME (driftwood, lashed with rawhide that shrinks tight on drying) — STORED through winter, near-identical year-on-year.
  - SKIN (seal hide) — REPLACED each season; old skin sloughed; new skin wet-stretched and stitched onto frame.
- The hull's PROPERTIES (waterproof seal, flex, weight) come from the SKIN — the frame is a persistent invariant SKELETON.
- The skin can fail (puncture, rot) without breaking the frame — replacement = re-skin, not rebuild.

## LLM analogy candidate
**SOF-LLM (Skin-On-Frame LLM)**: a deployment architecture with TWO PERSISTENCE LAYERS:
- FRAME = a small, slow-to-change persistent identity tensor that encodes invariant agent personality / safety alignment / role-prompt — never swapped at inference time.
- SKIN = a heavier outer layer (LoRA-rank + few-shot exemplar buffer + KV cache header) that is COMPLETELY REPLACED per deployment context, per session, or per user.
- KEY INVARIANT: the SKIN can be replaced WITHOUT touching the FRAME, and the FRAME GUARANTEES properties (alignment, persona, refusal patterns) that the SKIN cannot override.
- The skin can be torn off and a new one stitched on per session; the frame is the stable core.

## What differs from prior art (claim)
- Activated LoRA / aLoRA (2512.17910): efficient adapter swap, but adapter and base are not segregated by persistence-of-property; aLoRA can override safety in principle.
- RECAST (2411.16870): combines shared blueprints + module calibration — adjacent but the blueprint is treated symmetrically with the module.
- Layer swapping (2506.02006): runtime quant-layer swap — operational, not architectural skin/frame split.
- SOF-LLM proposes an EXPLICIT ARCHITECTURAL split where the FRAME (identity tensor + safety + role) is enforced via PROJECTION constraints that the SKIN cannot reach. This is a stronger structural guarantee than LoRA-stacking.
