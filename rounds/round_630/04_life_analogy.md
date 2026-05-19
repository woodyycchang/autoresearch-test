# R630 step 04 — source mechanism

## Source: Kalman filter (Bayesian state estimation)

State-space: x_{t+1} = F x_t + w_t (w ~ N(0,Q)); y_t = H x_t + v_t (v ~ N(0,R)).

Kalman recursion:
- Predict: x̂_{t|t-1} = F x̂_{t-1}; P_{t|t-1} = F P_{t-1} F^T + Q
- Update: K_t = P_{t|t-1} H^T (H P_{t|t-1} H^T + R)^{-1}; x̂_t = x̂_{t|t-1} + K_t (y_t - H x̂_{t|t-1}); P_t = (I - K_t H) P_{t|t-1}

### Mechanism transfer
Kalman gain K_t exposes the OPTIMAL combination of prior estimate and new evidence under Gaussian assumptions. Standard SSMs (Mamba, S4) implement structured linear recurrences but typically discard the covariance / gain. The candidate explicitly tracks per-token covariance P_t alongside state x̂_t and uses Kalman gain to weight new tokens.

Direct mechanism transfer — Kalman filter is exactly the closed-form Bayesian recursive estimator.
