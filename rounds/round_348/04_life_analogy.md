# R348 — life analogy

## Source: Mongoose ACh-receptor point-mutation venom resistance
- Mutations at receptor positions 187/189/194 reduce alpha-neurotoxin binding.
- N-glycosylation independently evolved in 13 species → convergent resistance.
- Substitution preserves receptor function but blocks toxin docking.
- Cheap, targeted, structural defense.

## LLM analogy
**RECEPTOR-MUTATE**: targeted point-modification of attention-Q/K projection weights at IDENTIFIED critical positions (analogous to receptor residues) to BLOCK known jailbreak/adversarial prompt attack signatures while preserving general attention function. Mutation is performed on a SMALL number of specific weight indices (not full LoRA), with point-wise modifications informed by adversarial-attack residue analysis.

## Differs from prior art (claim)
Antidote prunes identified harmful weights. ACH (Meta) uses LLM-generated targeted mutants for testing. Fine-tuning safety-optimization re-trains broadly. RECEPTOR-MUTATE differs by POINT-WISE TARGETED MUTATION of identified critical weight positions (mongoose-style 187/189/194), not pruning or broad re-training.
