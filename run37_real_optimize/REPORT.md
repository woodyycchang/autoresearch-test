# [REPORT] Run 37 — optimize against the external backtest, on the REAL banks

Continues PR #70. Ran on the **real run31 791-concept banks** (not the run32–35
reconstruction). Ground truth = **8 real, WebSearch-verified historical niches**
(real arXiv IDs/dates). Self-metrics are banned as success evidence (R12); only
real-history performance counts. Raw numbers: `real_history_results.json`
(reproduce: `python3 real_history_experiments.py`).

## 0. The banks contain the answers (contamination, R13)
**7 of the 8** niche families are **literal entries in the real 2026-harvested
tech_bank**: `FlashAttention`, `FlashAttention-2`, `Mamba`, `Mamba-3`, `LoRA`,
`QLoRA`, `DoRA`, `Mixture-of-Experts for LLMs`, `DeepSeekMoE`, `Switch
Transformer`, `S4`. You cannot test whether the pipeline *predicts* LoRA when
LoRA is an entry in its bank. Every experiment below therefore runs on a
**decontaminated corpus** (dropped 21 family keywords → **774 concepts, 90
branches**). Even decontaminated, no predictive signal appears.

## FAILURE 2 — frame coverage (5/8 → 8/8): GENUINELY IMPROVED, but shallow
Added three generator templates (`niche_types.py`) for the niche types the old
"mechanism-transfer" frame could not express:
- `emergent_phenomenon` (grokking), `scaling_law` (Chinchilla),
  `prompting_format` (chain-of-thought).

Frame coverage of the 8 niches rises **5/8 → 8/8**. **This is real.** **Honest
caveat (load-bearing):** representability ≠ predictability. A template lets the
generator *write* "QUANTITY scales as f(RESOURCE)"; it does **not** let it
generate *Chinchilla* before Chinchilla. Failure 2 is fixed in **letter**
(representation), not in **spirit** (prediction).

## FAILURE 3 — value ranking (target: invert 0.26 < 0.436): NOT FIXED — STRUCTURAL
Tested **three principled, niche-blind** value signals computed from the
791-corpus (NOT fit to the 8 niches): mechanism **generality** (cross-branch
token frequency), problem **centrality** (cross-concept frequency), and their
product. Per-niche percentile vs 20,000 random real-bank merges:

| niche | value(gen×cent) %ile | gen-only %ile | cent-only %ile |
|---|---|---|---|
| grokking | 0.017 | 0.618 | 0.003 |
| chain_of_thought | 0.961 | 0.989 | 0.535 |
| chinchilla | 0.898 | 0.956 | 0.459 |
| lora | 0.422 | 0.618 | 0.260 |
| flash_attention | 0.722 | 0.254 | 0.965 |
| mamba_ssm | 0.998 | 0.972 | 0.973 |
| **mixture_of_experts** | **0.051** | **0.051** | 0.223 |
| **rlhf** | 0.023 | 0.708 | **0.003** |

- **MoE ranks bottom-5% on every signal; RLHF ranks bottom-0.3% on centrality.**
  Two of the most consequential niches in ML history are scored among the
  **worst** by every principled signal tried.
- niche **median** value `0.00139` ≈ random **mean** `0.00137`. The signal is
  noise w.r.t. real importance.
- The niche **mean** `0.00155` technically exceeds random `0.00137` (1.13×) — but
  that "inversion" is driven entirely by 2 outliers (mamba 0.998, CoT 0.961) and
  the two high non-transfer scorers (CoT, Chinchilla) score high only because the
  keywords I chose for them ("reasoning", "scaling") are common corpus words.
  **Reporting the mean-inversion as success would be cherry-picking — rejected
  (R14).** Per-niche, the signal does not separate real niches from random.

## FAILURE 1 — flag-rate 99.15% / precision: NOT FIXED
Gating the niche flag on the value signal does not help: a value bar set low
enough to **retain the weakest real transfer-niche (0.00065)** still admits
**97.7% of random merges**. So gating moves the 99% flag-rate by ~1 point and
precision on real history stays ≈ 0. (To exclude 97.7% of junk you would have to
set the bar above MoE and RLHF — i.e. discard them.)

## Convergence vs Run 36 baseline (the buyer's metrics)
| metric | Run 36 | **Run 37** | verdict |
|---|---|---|---|
| frame coverage of 8 niches | 5/8 | **8/8** | improved (representability only) |
| niche-flag rate | 99.15% | **~98%** (value-gated, retaining real niches) | **not meaningfully improved** |
| real-niche value rank vs random | 0.26 < 0.436 (mean) | mean 0.00155 > 0.00137, **median ≈ random; MoE/RLHF bottom-percentile** | **not fixed (structural)** |
| precision on real history | ≈0 | **≈0** (97.7% junk still admitted) | not improved |
| contamination | flagged | **banks literally contain 7/8 niches** | worse than feared |

## VERDICT (honest, no spin)
Optimizing against the real failures on the real banks **did not produce
real-history predictive value.**
- **Failure 2 is fixable** — the generator now represents 8/8 niche types — but
  representability is not prediction.
- **Failures 1 and 3 are STRUCTURAL.** No principled niche-blind signal ranks
  real niches above random (MoE and RLHF land in the bottom percentiles);
  value-gating cannot restore precision without discarding real niches; and the
  banks contain the answers, so any apparent recall is recognition.

The buyer's question — *would this surface a real niche before it emerged?* —
remains **No.** Run 37's honest contribution is a sharper diagnosis of *why*:
the value of a niche (that it hit a bottleneck that turned out to matter) is not
recoverable from pre-emergence structure by any signal tested, and the
generator's expressiveness — now fixed — was never the binding constraint.
