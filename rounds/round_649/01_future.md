# R649 step 01

**Timestamp:** 2026-05-19T20:37:40Z

## Scan focus
Birkhoff ergodic theorem as mechanism source for time-averaged feedback attenuation in long-rollout RL training. Birkhoff: for ergodic measure-preserving T and integrable f, lim (1/n) Σ f(T^k x) = E[f] a.s. The candidate transfers this to time-averaged advantage signal in PPO, replacing point-estimate advantage with ergodic average to attenuate per-step feedback noise.

## Motivation
shared_math_structure: Birkhoff requires ergodicity, which RLHF dynamics only approximately satisfy. The candidate uses Cesàro average of advantage signals as a noise-attenuated update direction.
