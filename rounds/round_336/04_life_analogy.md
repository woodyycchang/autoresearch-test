# R336 — life analogy

## Source: Antlion conical sand-trap
- Conical pit dug at angle of repose (≈30-35° for fine sand).
- Walls are PASSIVELY UNSTABLE: any disturbance causes a sand avalanche, sliding the disturber toward the center.
- Antlion at the bottom catches prey that slides in.
- Maintained by sand-throwing behavior to keep walls at critical angle.

## LLM analogy
**REPOSE-LANDSCAPE**: optimization-time loss landscape sculpted into a PASSIVE FUNNEL toward a specific desired-state minimum. The loss surface is augmented with a "repose-angle" regularizer that makes the gradient terrain PASSIVELY SLOPE TOWARD the desired minimum whenever the parameters are perturbed. Parameter null-space outside the desired basin is rendered passively unstable: any perturbation causes parameters to slide back toward the basin center via a sand-throwing-style ongoing low-amplitude probe.

## Differs from prior art (claim)
SafeGrad uses null-space projection to nullify harmful gradients (active intervention). GPAS scales activations to preserve gradients. Sharpness-aware minimization seeks flat minima. REPOSE-LANDSCAPE differs by PASSIVE landscape sculpting via ongoing low-amplitude probe that maintains a critical-angle slope toward the desired minimum — the parameters slide back on their own without an active gradient-surgery step.
