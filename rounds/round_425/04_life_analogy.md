# Life Analogy — Aztec atlatl (lever-extended spear-thrower)

**Atlatl**:
- Low-mass rod (~50-60cm) functioning as ARM EXTENSION.
- Spear placed against bearing-surface; thrower's arm + atlatl together swing.
- 2-6x mechanical advantage: applies force over LONGER LEVER ARM = higher launch velocity.
- The rod itself adds no energy; it just lengthens the lever — extracts more energy from the same swing.

The unique principle: **passive lever extension multiplies useful force without adding source energy** — by making the moving arm longer, the same shoulder rotation creates higher tip velocity (v = ω · r). The cost is a tiny rod; the benefit is 2-6x range.

## Analogical mapping → CoT chain-extension as gradient lever

- Throwing arm length r ↔ chain-of-thought length L_cot (number of intermediate reasoning tokens)
- Shoulder angular velocity ω ↔ per-step parameter gradient magnitude
- Spear tip velocity v ↔ effective final-answer gradient signal during RL training
- Atlatl rod ↔ a learned EXTENSION POLICY that appends extra reasoning tokens before the answer

The mechanism: **ATLATL-LEVER gradient leverage via learned CoT extension policy** — during RL fine-tune (RLVR), allow the model to OPTIONALLY append k extra reasoning tokens before its answer. These k tokens are NOT trained directly; instead, the final-answer correctness signal is BACK-PROPAGATED through the entire chain as if the longer chain were one continuous compute. The gradient signal at early tokens is multiplied by the (1 + k/L_base) ratio, providing a lever effect: small swing (gradient at first reasoning step) produces large tip velocity (gradient at final answer through long chain). Differs from (a) standard CoT (handcrafted prompt format), (b) DeepSeek-R1 RLVR (no explicit lever-length policy), (c) o1-style reasoning (implicit length scaling), (d) Long-CoT 2502.03373 (analyzes long CoT but doesn't propose lever-extension policy) by combining (i) LEARNED EXTENSION POLICY + (ii) PROPORTIONAL GRADIENT LEVERAGE through chain + (iii) MECHANICAL-ADVANTAGE RATIO as training-time hyperparameter.

## Note on adjacency

The information-cascade form fits. Adjacent: long CoT, RLVR, test-time-compute. Distinct: explicit LEARNED EXTENSION POLICY treated as a LEVER, with gradient leverage ratio as hyperparameter.
