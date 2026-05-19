# R646 step 01

**Timestamp:** 2026-05-19T20:24:05Z

## Scan focus
Bellman optimality residual as mechanism source for adversarial co-evolution. Bellman: Q*(s,a) = r(s,a) + γ E[max_{a'} Q*(s',a')]. The Bellman residual measures sub-optimality of the current Q. The candidate transfers to adversarial multi-agent training where each agent maintains its own Q-function and adversarial-coevolution requires bounded mutual Bellman residual.

## Motivation
mechanism_transfer: Bellman equation IS the fixed-point of optimal value functions; residual is a precise algebraic quantity. The candidate uses it as a coupling-bound in adversarial training.
