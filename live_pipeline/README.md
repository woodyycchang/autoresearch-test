# Live-Fetch Niche Finder

A fresh architecture iteration of the niche-mining pipeline. Supersedes the
pre-stored-bank approach (`paradigm_shift/`, TARI). The fundamental correction:
**concepts are fetched live from the real encyclopedia at runtime — never from a
frozen snapshot or a pre-stored bank.**

## Non-negotiable architecture

1. **No pre-stored banks.** Every concept is obtained by a live `WebSearch` of
   real sources (Wikipedia / arXiv) at runtime. Frozen concept banks were the
   fundamental error of prior runs.
2. **Maximum agent parallelism at every stage.** Each stage fans out into many
   parallel tool-using agents. Redundancy + cross-check is the hallucination
   defense.
3. **Every agent uses tools.** No agent reasons from pretrained memory alone —
   that is precisely the failure mode being guarded against.
4. **Separate checker agents at every step** independently re-verify the prior
   agents (anti-fabrication + anti-pretrained-fallback). Search is a
   *last-resort integrity check, not a novelty gate* (R6).
5. **Persistence + auto-merge.** `direction_params.json` (tunable params +
   per-cycle measurements) and `traversed.json` (live-fetch dedup ledger) are
   committed each cycle; every stage auto-merges to `main`.

## Stages (each = many parallel tool-using agents + separate checkers)

| # | Stage | Parallel generators | Separate checkers |
|---|-------|---------------------|-------------------|
| 1 | Live encyclopedia fetch | N agents, one per knowledge branch, each `WebSearch`es real Wikipedia/arXiv and records concepts with **real source URLs** | URL-resolver agents `WebFetch` each claimed URL to confirm it is real (anti-fabrication) |
| 2 | Merge | N agents form maximally-distant concept triples (cross-branch) | — (pure generation) |
| 3 | Integrity check | — | N redundant checkers `WebSearch` each merge: genuine combination vs. already-existing/regurgitated; cross-validate |
| 4 | Niche check | N agents classify variant-vs-genuine | separate checkers re-verify survivors |
| 5 | Value + registry | N agents `WebSearch` prior art ("done already?") + value | checkers re-verify |
| 6 | Reasoning audit | 1 isolated Opus agent: final adjudication over survivors | — |

`niche = survives ALL stages.`

## What we actually evaluate (R9)

The output niche is a ground-truth *signal*, not the deliverable. We measure
whether the **algorithm as a whole** is improving: parameters + process +
agent-coordination + decision quality + fabrication resistance. Honest lineage
context: the predecessor pipeline logged **0 substantive PASS across N=1071
verified rounds**. We do not manufacture discoveries; we measure the process and
drive its parameters toward production-readiness.

## Files

- `direction_params.json` — persistent tunable params + per-cycle metrics + update log.
- `traversed.json` — concepts fetched + merges attempted, for next-cycle resume/dedup.
- `cycles/cycle_NNN/stageN_*.json` — real per-stage outputs (real URLs, tool-use counts).
- `cycles/cycle_NNN/REPORT.md` — what each stage did this cycle.

## Honesty guardrails (R5)

Agents return **only real tool results**. An agent that cannot retrieve a source
reports `NO_RESULT` rather than inventing one. Checkers independently re-fetch a
sample of every claimed URL; any unresolvable/fabricated source is logged and the
concept is dropped. No claim of a genuine paradigm shift is made on the strength
of generation alone.
