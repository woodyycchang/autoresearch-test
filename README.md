# niche-mining-autoresearch

An autonomous research-niche-mining pipeline modeled on Karpathy's
[AutoResearch](https://github.com/karpathy/autoresearch).

## TL;DR

A `program.md` instruction file that a coding agent (Claude Code) reads to
autonomously search for a paradigm-shift research niche in LLM/AI by
cross-domain analogy mining + prior-art verification with three layers
of mechanical anti-cheating enforcement.

## Quick start

1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`
2. `cd` into this repo
3. Run `claude`
4. `/model opus`
5. Paste the prompt from `STARTUP_PROMPT.md` (section "To START a fresh run")
6. Agent autonomously runs the pipeline

## Repo layout

```
niche-mining-autoresearch/
├── README.md                  ← this file
├── STARTUP_PROMPT.md          ← prompts to paste in Claude Code
├── program.md                 ← agent's operating instructions (the heart)
├── saturation_evidence.md     ← prior human-run data (N=138 verified)
├── .gitignore
├── rounds/                    ← agent creates round_001/, round_002/, ...
├── logs/
│   ├── candidate_pool.md      ← seeded with exhausted candidates
│   ├── compliance_log.md      ← agent appends violations
│   ├── disagreement_log.md    ← cross-agent verification mismatches
│   └── session_log.md         ← session-level audit trail
└── output/
    └── (stats files + final_report.md written by agent)
```

## What problem this solves

Trehan & Chopra (arXiv 2601.03315, Jan 2026) documented 6 failure modes
in autonomous LLM research agents from a 4-attempt case study. Their
explicit future work: **quantify failure-mode incidence at scale.**

This repo lets you run n=50, n=100, or n=200 autonomous research
attempts with hard compliance enforcement, producing the quantitative
data Trehan & Chopra called for.

## Background data

A human running this pipeline manually in a chat interface for N=138
rounds got 0 PASS. The agent was caught skipping the prior-art
verification step in ~14 rounds in one batch and ~60 rounds in another.
Those caught failures are case studies of the same failure modes
Trehan & Chopra named. See `saturation_evidence.md` for full data.

## Three-layer anti-cheating design

1. **File chain** (Karpathy style) — Each step writes a file; next step
   reads it. Skipping a step makes downstream steps crash.
2. **Mechanical keyword overlap rule** — Step 05 freezes content_words
   before search. Step 07 mechanically forces `hit: true` if ≥2 content
   words appear in a result's title+snippet. Agent cannot override.
3. **Cross-agent verification** — Step 12 spawns a fresh agent to
   independently re-judge each round. Mismatches are flagged for human
   review.

What this CANNOT prevent: same-model RLHF training bias making all
agents systematically lean toward PASS. Human spot-checking of PASS
rounds is the final defense.

## Expected outcomes

- PASS probability per round: <1% (based on N=138 prior data)
- Useful thesis outputs even at 0 PASS:
  - Quantitative compliance rates per step
  - Trehan & Chopra failure-mode incidence rates
  - Saturation p-value with proper statistical bounds
  - Cross-agent disagreement rate (proxy for inter-rater reliability)

## License

MIT (matching Karpathy's AutoResearch).
