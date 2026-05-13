# Life Analogy — Tahitian va'a outrigger ama counterbalance

The **Tahitian va'a** (outrigger canoe) features:
- Single main hull + asymmetric **ama** (outrigger float) on the left side only.
- Two **iato** (struts) connect ama to hull at fixed lever arm.
- The main hull's outer side is **flat** (windward); inner side is **rounded** (between hull and ama).
- Stability comes NOT from hull symmetry but from the **distance** (lever arm) between hull and ama.
- A single, fixed counterbalancing mass — not a symmetric twin like a catamaran (vaka 'taurua).

The unique principle: **one-sided fixed counterbalance** — a single auxiliary mass at a known lever arm provides anti-roll stability, exchanging full bilateral symmetry for hydrodynamic efficiency in the main hull. The asymmetry is not random; it has a known forward direction (windward side is fixed).

## Analogical mapping → multi-head attention asymmetric anchor

- Main hull ↔ active learned attention head
- Single ama ↔ ONE fixed-direction anchor head
- Iato struts at fixed lever arm ↔ regularization coupling at fixed magnitude
- Flat windward side ↔ fixed-direction adversarial pressure resistance
- One-sided not bilateral ↔ asymmetric, not orthogonal

The mechanism: **AMA-COUNTERBALANCE** — in a transformer with H attention heads, designate ONE head per layer as a "fixed counterbalance head" with frozen weights initialized to a single known direction (e.g., positional shift identity). At training time, the remaining H-1 heads are free to learn but receive a regularization signal that penalizes their projection onto the counterbalance head direction WHEN AND ONLY WHEN the residual stream variance exceeds a learned threshold (representing "roll instability"). Differs from anchor attention (multiple anchors), TensorLLM Tucker shared-subspace (all heads coupled), and Grouped Query Attention (head-cluster sharing) by using a SINGLE fixed-direction anchor and an asymmetric lever-arm regularizer triggered only on variance excess.

## Note on adjacency

Anchor-attention literature (e.g., LongAnchor, anchor-token attention) uses anchors over TOKENS, not over heads. TensorLLM tensorizes via Tucker but couples ALL heads symmetrically. The closest twin is Stable-Attention regularization that bounds head variance, but that is symmetric over heads. The asymmetric single-anchor-head + variance-triggered iato regularization is a specific recombination.
