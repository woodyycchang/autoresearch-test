# R687 motivation

Frenet-Serret formulas describe how the orthonormal frame {T,N,B}
rotates along a smooth curve in R³, via the structure equations T' = κN,
N' = -κT + τB, B' = -τN. Together (κ,τ) completely characterize the
curve up to rigid motion.

For LLM hidden-state curves: compute frame at each token, use κ as a
"local complexity" gauge. High κ = abrupt change in trajectory = important
context-binding token.

Motivation: mechanism_transfer.
