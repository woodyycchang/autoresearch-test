# R681 motivation

Selberg trace formula equates a SPECTRAL sum (Laplacian eigenvalues on a
hyperbolic surface) to a GEOMETRIC sum (over closed geodesics). The
identity is a precise quantitative relationship between two
independently-computable quantities.

For LLM hallucination: existing methods (LapEigvals, EigenTrack) use only
the SPECTRAL side. Selberg's identity says the spectral side should
match a geometric side. If both sides are computed and they DIVERGE,
that's a hallucination signal.

Motivation: mechanism_transfer.
