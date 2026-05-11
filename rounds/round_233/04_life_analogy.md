# R233 — life analogy

## Source domain: shape memory alloy nitinol
- Has TWO crystalline phases: austenite (high-T, simple cubic, "original shape") and martensite (low-T, monoclinic, "deformed shape").
- Phase transition is thermally hysteretic: martensite-start Ms ≠ austenite-finish Af; the hysteresis loop is ~20-50°C wide and is the alloy's MEMORY KERNEL.
- TWO-WAY TRAINING: by repeatedly heating + deforming in martensite + cooling cycles, the alloy "remembers" both a hot shape (austenite) and a cold shape (martensite), spontaneously snapping between them on temperature crossing.

## LLM analogy candidate
**Thermal-phase weight memory**: maintain TWO logical weight phases for an adapter — `W_A` (austenite = pre-fine-tune, "default" model weights) and `W_M` (martensite = task-specific fine-tuned). A scalar "temperature" parameter T (deployment-time, not training-time) controls which phase is ACTIVE by simulating a thermal-hysteresis snap rule:
- if T > T_af AND prev_phase=M: snap to phase A (recover defaults)
- if T < T_ms AND prev_phase=A: snap to phase M (apply fine-tune)
- inside hysteresis loop: remain in current phase

T is computed from runtime risk signal (prompt-risk classifier output). On low-risk routine inputs, the model runs in martensite (fine-tune active). On high-risk inputs, T rises above T_af and the model "anneals" back to austenite (pre-fine-tune defaults — preserving original safety alignment). The hysteresis prevents flicker (T near boundary doesn't repeatedly toggle phases). After cooling-cycle training (repeated alternation), the model exhibits two-way memory: clean fine-tune-task shape AND clean default-safety shape, snap-switched by T.

## What differs from prior art (claim)
Recovering Pre-Fine-Tuning Weights (2402.10208) shows it's POSSIBLE to recover defaults from a LoRA — but as an ATTACK. Watch-the-Weights (2508.00161) MONITORS fine-tune deformation but doesn't actively snap-back. None proposes the active deployment-time T-controlled phase-snap with hysteresis loop for safety/task duality.
