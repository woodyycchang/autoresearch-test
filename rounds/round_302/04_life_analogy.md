# R302 — life analogy

## Source: Brood-X 17-year periodical cicada prime emergence cycle
- Magicicada species emerge synchronously every 13 or 17 years (prime numbers).
- Prime-numbered cycles resist resonance with predator life cycles of period 2, 3, 4, 5, 6 — only every 13×3=39 or 17×3=51 years would a 3-year predator coincide with cicada emergence.
- Predator satiation + cycle-coprimality reduces between-emergence overlap with shorter-cycle threats.

## LLM analogy
**PRIME-CYCLE-REPLAY**: schedule continual-learning replay-buffer refreshes (and curriculum task rotations) at PRIME-numbered epoch periods (13, 17, 19, 23) deliberately COPRIME with other periodic training processes (lr cosine cycle, eval cadence, gradient-norm-clipping schedule). Eliminates resonance-driven gradient interference where two periodic schedules align and amplify forgetting.

## Differs from prior art (claim)
Standard replay schedules use uniform (every k epochs), surprise-driven (SURE 2024), or Ebbinghaus expanding-interval. None deliberately choose PRIME-numbered periods coprime with other concurrent periodic schedules to AVOID resonance-driven interference with other training cycles.
