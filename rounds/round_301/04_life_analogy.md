# R301 — life analogy

## Source: Glasswing butterfly (Greta oto) wing nano-pillars
- Wing surface covered in randomly-sized, randomly-spaced nano-pillars (~100 nm diameter, aspect ratio up to 10).
- Each pillar is a sub-wavelength structure; collectively, they create a gradient effective refractive index from air to chitin.
- Omnidirectional anti-reflection: the wing scatters incident light into the bulk rather than reflecting it off the surface.

## LLM analogy
**GLASS-ATTN**: Pre-attention input projection through a learnable "random-amplitude-profile" tapered embedding layer. Each input token is projected through a stack of K sub-layers with monotonically decreasing scale magnitudes (analogous to nano-pillar tapering from base to tip). This produces a gradient embedding-norm transition from raw-input-space to attention-space, suppressing sharp boundary "reflections" (gradient discontinuities, spurious activation echoes at the input boundary) that interfere with attention focus.

## Differs from prior art (claim)
Standard input embedding is a single dense projection. Gated attention (2505.06708) gates information flow but does not impose a gradient-amplitude profile across sub-projections. Pre-norm/post-norm tuning shifts normalization placement but does not impose a nano-pillar-like tapered amplitude scaffold across multiple stacked projections.
