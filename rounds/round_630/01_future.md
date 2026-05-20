# R630 step 01

**Timestamp:** 2026-05-19T19:18:05Z

## Scan focus
Kalman filter / Bayesian state estimation as mechanism source for long-context recurrent state updating. Kalman filter is the optimal linear Bayesian estimator for Gaussian state-space models with a specific recursive update rule combining prior + measurement. The candidate: replace the KV-cache with a low-rank Kalman-style state filter where each token update applies a Kalman-gain combination of prior context (compressed) + new evidence.

## Motivation
mechanism_transfer: Kalman filter IS the optimal Bayesian recursive estimator for linear-Gaussian systems. Recent State Space Models (Mamba, S4) implement linear recurrences that are structurally analogous to Kalman recursions but typically don't expose the gain/covariance explicitly. The candidate proposes EXPLICIT covariance-tracked state updates with Kalman gain.
