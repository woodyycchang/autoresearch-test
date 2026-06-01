# Run 16 — Epoch 3 report (low-overlap domain hypothesis tested)

Epoch 3 applied epoch-2's labels, extended the scorer to detect low-ML-overlap
domains, and sourced a **geology/seismology** atom to test a specific hypothesis:
*does a lower-overlap domain → lower prior-art density → a candidate that finally
clears Gate 1 (composite ≥ 0.90)?*

## Headline

| metric | epoch 2 | epoch 3 | delta |
|---|---|---|---|
| **avg_search_quality** | 0.5967 | **0.6024** | **+0.0057 ▲** |
| niche verdict | NICHE_NOT_FOUND | NICHE_NOT_FOUND | — |
| low-overlap candidate clears Gate 1? | — | **NO** | hypothesis not confirmed |
| proof points | 7/7 | 7/7 | — |
| A3↔A4 mismatches | 0 | 0 | — |

3-epoch trajectory: **0.5119 → 0.5967 → 0.6024** (monotonic ↑, diminishing returns).

## The hypothesis result: NO, but for an illuminating reason

The two ML×seismology candidates are **genuinely novel** — AGENT 3 and AGENT 4
*both independently* found **zero bridging papers** (the ML and seismology results
form disjoint clusters; nothing transfers rupture/off-fault-damage physics into
TTT/MoE mechanisms). So they pass **Gate 3** (no collision, cross-verified).

But they do **NOT** clear **Gate 1**, scoring composite 0.45 — identical to the
ML×ML candidate:

| cand | type | gates [1,2,3,4] | paper_hits | novelty | composite |
|---|---|---|---|---|---|
| 001 Similarity-Preserving Routing for TTT-MoE | ML×ML | 0 1 1 1 | 33 | 0.0 | 0.45 |
| 002 Rupture Dynamics of TTT Hidden States | ML×geo | 0 1 1 1 | 24 | 0.0 | 0.45 |
| 003 Damage-Regularized Orthogonal Routing | ML×geo | 0 1 1 1 | 27 | 0.0 | 0.45 |

**Why:** Gate 1's composite measures novelty as `1 − paper_hits/20`, where
`paper_hits` = *all* paper-like results returned across the prior-art searches.
For a cross-domain niche, each single domain (ML; seismology) is individually
well-populated, so the searches still return 24–27 papers even though **none
bridges the domains**. Total prior-art volume stays high → novelty floors to 0 →
Gate 1 rejects.

**Diagnosis:** cross-domain novelty is the *bridging*-paper count (here 0, =
Gate 3's collision signal), not the *total* prior-art volume that Gate 1's
composite counts. The two cross-domain candidates clear **3 of 4 gates**, failing
only the one gate whose novelty proxy is miscalibrated for cross-domain work.

**Honest note:** I did **not** retune Gate 1 after seeing this — changing the
locked gate to manufacture a survivor would be exactly the results-driven gaming
this project guards against. The straight answer to the hypothesis is "no, the
low-overlap candidate does not clear Gate 1," with the diagnosis above. A
principled fix (for a *future* epoch, with your sign-off) is to base Gate-1
novelty on the bridging/collision count rather than total search volume — which
would let candidate 002/003 through, since their bridging count is 0.

## Search-quality dimensions (what moved)

| dimension mean | e2 | e3 | note |
|---|---|---|---|
| reformulation_specificity | 0.89 | **0.92** | ▲ |
| mechanism_focus | 0.74 | **0.50** | ▼ naming seismology terms diluted mechanism density |
| cross_domain_reach | 0.02 | **0.31** | ▲▲ directive #1 worked — both-domain naming + extended FIELD_LEX |
| atom_source_diversity | 1.00 | 1.00 | — |
| collision_avoidance_phrasing | 0.30 | 0.27 | ~ |

The small net delta (+0.0057) is an honest **tradeoff**: the large cross_domain_
reach gain (0.02→0.31) was mostly offset by the mechanism_focus drop (0.74→0.50),
since cross-domain queries spend tokens on domain vocabulary instead of mechanism
verbs. Both directives (name both domains; lift cross_domain_reach) succeeded
mechanically; they just traded against mechanism focus.

## Two metric caveats disclosed
1. **Mid-experiment metric change:** the scorer's FIELD_LEX was extended this
   epoch (geology/linguistics/materials/ecology + hyphen-split matching) per your
   directive #1. So epoch-3 cross_domain_reach is measured on a richer lexicon
   than epochs 1–2 — part of the cross_domain_reach jump is genuine both-domain
   naming, part is the metric now being *able* to see seismology terms. Disclosed,
   not hidden.
2. The +0.0057 delta is real but small; the interesting epoch-3 result is the
   Gate-1 hypothesis finding, not the metric tick.

## Proof points: 7/7 PASS
agents_all_committed · report_verbatim ([REPORT 1..5]) · four_gate_deterministic ·
cross_check_ran (AGENT 4 independently confirmed all 3, found no bridging papers) ·
no_hallucination · search_quality_tracked · params_persisted. 19 offline tests pass.

## Honest disclosures
- AGENT 1 again caught its own R5 slip (a pre-existing/draft atoms.json with
  unverified ids), and recommitted with real searched papers.
- The cross-domain candidates' novelty is real (0 bridging papers, cross-verified);
  Gate 1 simply doesn't measure it. That gap is the epoch's main finding.

## Parameter state (R9)
`direction_params.json`: epoch 3 → 4; `epoch_history` = [e1 0.5119, e2 0.5967,
e3 0.6024]. Params after epoch 3: specificity 0.5698, mechanism 0.594,
cross_domain 0.5059, collision 0.5147 (the epoch-3 nudge from epoch-2 labels).

## Next
Label epoch-3's queries for the epoch-4 nudge. And decide: should Gate-1 novelty
switch to a bridging-paper (collision-based) count so genuinely-novel cross-domain
niches can clear it? That single change would likely turn candidate 002/003 into
the loop's first survivors.
