# Round 687 — Future LLM/AI mechanism (E28 R687, v9)

Apply Frenet-Serret frame (tangent T, normal N, binormal B + curvature κ
+ torsion τ along a curve) to LLM context gating: treat the
hidden-state trajectory as a curve in embedding space, compute (T,N,B)
+ (κ,τ) per token, gate context attention by κ-magnitude (high curvature =
high-information point requiring more context).

Timestamp 2026-05-20T05:14:00Z. Form: context-gating.
