# R250 — life analogy

## Source domain: spider orb-web construction
- Multi-stage build process with EXPLICIT SCAFFOLDING that is later REPLACED:
  1. Bridge line (single thread across the gap)
  2. Y-frame (anchor polygon)
  3. Radial spokes (15-35 spokes at 10-25° intervals)
  4. AUXILIARY non-sticky spiral (from hub outward) — TEMPORARY scaffold
  5. Sticky capture spiral (from outside inward) — replaces the auxiliary, often REMOVING IT as it lays the sticky one
- Key principle: scaffold-then-replace. The auxiliary spiral is structurally important during construction but functionally irrelevant once the sticky spiral exists; the spider removes the scaffold to save silk.

## LLM analogy candidate
**Scaffold-then-replace progressive fine-tune**: train an LLM in stages where each stage installs a TEMPORARY auxiliary structure that is FORMALLY REMOVED in a later stage. Concrete: (1) bootstrap stage — adapter A_temp with explicit auxiliary head H_aux predicting intermediate quantities (entity tags / refusal flags / confidence) — used to drive learning signal. (2) main-task stage — primary adapter A_main trained while A_temp + H_aux are FROZEN-AND-CONSULTED via auxiliary loss. (3) replacement stage — A_main is fine-tuned to internalize what A_temp + H_aux were providing, then auxiliary structure is FORMALLY ABLATED at deploy-time. Output: a small primary model that has absorbed the temporary scaffold's learning signal without paying its deployment cost. Distinct from standard auxiliary-loss training: explicit two-step formal ABLATION with internalization-verification before removal.

## What differs from prior art (claim)
IMPROVE (2502.18530) iteratively refines but does not formalize a scaffold-then-ablate stage sequence. Two-stage prompting (2604.01029) covers the scaffold-then-refine pattern at inference but not at training-time with explicit auxiliary-structure ablation. EVOLVE (2502.05605) iterates self-refinement but does not ablate the auxiliary. The spider's discipline (auxiliary scaffold REMOVED after the primary structure absorbs its function) is distinguishing.
