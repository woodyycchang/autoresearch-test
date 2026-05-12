# R346 — life analogy

## Source: Velvet ant high-cost aposematic defense
- 5 layered defenses: aposematic color, stridulation, alarm secretion, durable exoskeleton, painful sting.
- Sting is HIGH-COST (egg-laying organ usage); used as last resort.
- Pain is the deterrent; toxicity is low.
- Müllerian mimicry — multiple species share warning signal.

## LLM analogy
**MULTILAYER-DETERRENT-EVAL**: evaluation-diagnostic head built as a CASCADE of escalating-cost evaluators — cheap surface checks first (color/aposematic ≈ cheap regex/keyword), mid-cost intermediate evaluators (stridulation ≈ small classifier), heavy LLM-as-judge only at the deepest level (sting ≈ frontier-model judge with adversarial probing). High-cost levels rarely invoked. Total evaluation cost amortized by aposematic deterrent at cheap levels (most adversaries deflected by surface checks).

## Differs from prior art (claim)
LLM-as-Judge surveys (Evidently, Monte Carlo) discuss cost-reliability tradeoff. Multi-agent debate (2511.06396) uses critic-defender. MULTILAYER-DETERRENT-EVAL differs by EXPLICIT 5-LAYER cascade with deliberate cost asymmetry matching the velvet-ant defense topology (cheap-to-expensive, last-resort high-cost).
