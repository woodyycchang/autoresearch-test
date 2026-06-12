# [REPORT] Task B — External validation: would this find a REAL niche before it emerged?

**Short answer: No.** Not in any actionable sense. The detail below is the
honest measurement, not a spin.

## Method
8 landmark ML niches, each **verified real via WebSearch** (real arXiv paper +
date — no agent-made fixtures):

| niche | paper | date |
|---|---|---|
| grokking | Power et al., arXiv:2201.02177 | Jan 2022 |
| chain-of-thought | Wei et al., arXiv:2201.11903 | Jan 2022 |
| Chinchilla scaling | Hoffmann et al., arXiv:2203.15556 | Mar 2022 |
| LoRA | Hu et al., arXiv:2106.09685 | Jun 2021 |
| FlashAttention | Dao et al., arXiv:2205.14135 | May 2022 |
| Mamba / SSM | Gu & Dao, arXiv:2312.00752 | Dec 2023 |
| Mixture-of-Experts | Shazeer et al., arXiv:1701.06538 | 2017 |
| RLHF / InstructGPT | Ouyang et al., arXiv:2203.02155 | Mar 2022 |

Each was run through the run35 niche-checker + value scorer (the most complete
*reconstruction* engine — see `../PIPELINE_STATE.md`; the real run31 engine is
artifact-based and not runnable on new inputs). Raw numbers:
`backtest_results.json`.

## Findings (real measurements)

### 1. The "niche" verdict is uninformative — base rate 99.15%
The niche-checker flags **9550 / 9632 = 99.15%** of all random generated merges
as `NICHE_FOUND`. A signal that fires on 99% of everything cannot tell a buyer
which 1-in-a-million combination is worth pursuing. **Precision of a niche flag
≈ the base rate of useful merges, which is ~0.**

### 2. The merge frame can't even represent 3/8 of these niches
Only **5/8** are expressible as a "borrow mechanism A → apply to problem B"
transfer (LoRA, FlashAttention, Mamba, MoE, RLHF). **grokking** (a training
*phenomenon*), **chain-of-thought** (a *prompting format*), and **Chinchilla**
(an *empirical scaling law*) are not mechanism transfers at all — the generator
could never produce them.

### 3. Contamination: the verdict just tracks registry membership (name recognition, not foresight)
The verdict flips entirely on whether the niche's family string is in the
registry:

| niche | family in registry? | full registry | family removed (pre-emergence proxy) |
|---|---|---|---|
| **RLHF** | yes | **REJECT** (variant) | **NICHE_FOUND** |
| MoE | yes | REJECT | REJECT* |
| LoRA, FlashAttention, Mamba | **no** | NICHE_FOUND | NICHE_FOUND |

`RLHF` flips `REJECT → NICHE_FOUND` the moment its family is removed — proof the
checker is doing **string/token recognition of known methods, not structural
prediction of gaps**. (*MoE stays `REJECT` because a near-duplicate entry remains
— same point: it's matching a registry string.)

And note: even a registry **harvested in 2026** (post-dating every niche) contains
only **2 of the 8** families (MoE, RLHF). It is missing LoRA, attention,
FlashAttention, Mamba, DPO. So the pipeline would "flag" 6/8 landmark niches as
novel — **driven by its own registry incompleteness, identical to how it flags
useless junk.** That is not prediction.

### 4. The value scorer — the only possible discriminator — mis-ranks the real successes
Value-fit of each niche vs the distribution over 9632 random merges
(random mean **0.436**):

| niche | value_fit | percentile vs random |
|---|---|---|
| FlashAttention | **0.00** | **0.9%** (below 99% of random junk) |
| LoRA | **0.00** | **0.9%** |
| grokking / CoT | 0.00 | 0.9% |
| MoE | 0.27 | 17% |
| Mamba | 0.50 | 73% |
| RLHF | 0.50 | 73% |
| Chinchilla | 0.80 | 98% (but unrepresentable / trivial encoding) |

The 5 frame-fitting niches average value-fit **0.26 < 0.436 random**. The value
scorer rates **FlashAttention and LoRA — two of the highest-impact niches of the
decade — as less valuable than 99% of random combinations.** It would have
thrown them away.

## Caveats (stated, not used to soften the verdict)
- The token encodings of each niche were written by me **post-hoc, with
  hindsight**. That favors the pipeline if anything (I picked plausible tokens).
- The value ontology is coarse. So **finding 4 (value mis-ranking) is the
  *softest*** — it depends on encoding/ontology.
- But **findings 1–3 are robust** — they don't depend on the value ontology or
  the exact tokens at all: the 99% base rate, the 3/8 unrepresentable niches, and
  the verdict-flips-on-registry-membership are structural facts of the method.

## Verdict
**The pipeline has no genuine pre-emergence predictive value.** What it *can* do
(and the real run31 demonstrated this well: 18/18 constructs correctly judged
variants of real 2024–26 arXiv papers, **0 hallucinated citations**) is
**recognize whether a proposed combination already matches known work** — a
literature-grounded "has this been done?" checker. But "not yet in the
literature" describes ~99% of all merges and most of modern ML, so it is not a
signal you can act on. It recognizes the present; it does not predict the future.

For the buyer's question — *would this surface a real niche before it emerged?* —
the honest answer is **no.**
