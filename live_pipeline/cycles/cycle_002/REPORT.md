# Cycle 2 — Live-Fetch Niche Finder (R11 breadth fix + Stage 7)

**Terminal result:** 1 niche survived all 7 stages — `LoadTightening AutoTTS` —
classified **SEED_ONLY** by the new Stage-7 agent + EV gate. **0 fabrications.**
~48 parallel tool-using agents, ~600 real WebSearches.

## The corrected design (R11)

Cycle 1's fundamental error was fetching only academic-science concepts. Cycle 2
fixes it: **merge = newest-ML technique × a real life/culture concept** (the
encyclopedia merge). Stage 1 ran two axes — 8 agents across the full breadth of
human life/culture (food, craft, ritual, navigation, games, music, language) and
4 agents on newest-ML (last 1–6 mo).

## What each stage did

1. **Live fetch (12 + 3 agents):** 36 concepts (24 life/culture + 12 newest-ML),
   all with real URLs. ML axis 12/12 arXiv IDs independently verified REAL. Life
   axis: 18 verified, **6 SUSPECT (embellished mechanisms), 0 fabricated** — and 2
   embellishments were exactly the computationally-attractive *hook* (Songlines
   "recoverable from any one channel"; Plain-Bob "all n! permutations"), flagged so
   no merge built on a false premise.
2. **Merge (4 agents):** 8 buildable ML×life methods (Coppice-GA, EtakLR,
   Adaptive-Fenwick, Kigumi-VLA, Kotekan Dual-Draft, Entropy-Gated VeriCache,
   Global Advantage Fallow, LoadTightening AutoTTS).
3. **Integrity (8 + 3 tie-break):** 5/8 survive. New **analogy-collapse probe**
   unanimously dropped 3 (EtakLR→SALR, Kigumi-VLA→Titans, Entropy-VeriCache→AdaEDL).
   New **tie-break** recovered 3 disagreements (all GENUINE on 3rd cover). Caught a
   **false attribution** (Kotekan merge mis-described PARD as dual-head).
4. **Niche check (10 agents):** 1/5 survive (0.0 disagreement). All 4 drops were
   trivial variants — including **all 3 tie-break recoveries** — against *closer,
   more recent* prior art than Stage 3 found (L-MTP, PosS, REINFORCE++, adaptive-decay).
5. **Value + prior-art (4 agents):** G4-2 → unanimous **NO_COLLISION** (~44
   queries) + unanimous **MODEST_INCREMENTAL**.
6. **Reasoning audit (2 Opus):** both **NICHE_CONFIRMED_WITH_CAVEATS**. Flagged a
   real accuracy risk, judged the Kigumi life-axis **decorative**, scoped "provable"
   to code (not system), and caught an unverifiable Stage-5 citation (2603.20537).
7. **Viability (2 agents, AGENT-rendered per R9):** both **SEED_ONLY**. Exact combo
   not done, but HIGH accuracy risk + MODEST value → EV gate routes to SEED_ONLY.

## The surviving seed (honest framing)

**LoadTightening AutoTTS** — constrain AutoTTS-synthesized test-time-scaling
controllers so stop/prune thresholds are provably monotone in accumulated compute,
verified at synthesis time. Real, unclaimed combination, but **a SEED at best**:
the hard monotone constraint may be *actively harmful* (it forbids the controller
from tightening after a mid-trajectory confidence collapse — the very flexibility
behind AutoTTS's best accuracy/compute tradeoff), the value delta over AutoTTS's
existing beta convention is modest, and the life/culture axis (Kigumi) is decorative.

## Algorithm-improvement evaluation — cycle 2 vs cycle 1 (R7)

Both cycles produced exactly **one marginal `CONFIRMED_WITH_CAVEATS` survivor** — but
cycle 2 added the **EV gate + Stage 7** that cycle 1 lacked, so the same outcome is
now honestly classified **SEED_ONLY** instead of reported as "the niche found." That
is the headline improvement: **manufactured-survivor inflation is eliminated.**

New-mechanism scorecard (from the Opus audit):
- **Analogy-collapse probe — CLEAR WIN.** Became the dominant, clean integrity
  discriminator ("reduces to a named ML method").
- **EV gate — NECESSARY/load-bearing.** The only thing preventing a MODEST idea
  from being promoted as a discovery; correctly stamped the survivor SEED_ONLY.
- **R11 ML×life breadth — WORKED at fetch, LEAKED at merge.** 0 fabrications and 6
  embellishments caught, but merge agents over-concentrated on 5/24 distinct life
  concepts (Etak ×3, Kigumi ×2).
- **Tie-break — NET-WASH.** Recovered 3 merges that all died one stage later;
  3/3 pro-genuine bias. Kept as a diagnostic (it proved integrity ≠ niche), revised
  to require re-derivation.

**Binding constraint diagnosed:** ML-subarea *saturation* — every cycle-2 ML concept
sat in a crowded fast-moving area, so 4/5 Stage-3 survivors collapsed at Stage 4 to
very recent prior art. Cycle-3 fixes queued in `direction_params.json`: distinct-
life-concept-per-merge (breadth-leak fix) + ML-whitespace steering + crowdedness
penalty (the yield fix) + load-bearing-life-axis check + deeper Stage-3 prior-art +
checker-citation verification sweep.

Per-cycle metrics: `direction_params.json → metrics_history`. Raw per-stage agent
outputs: `stageN_*.json`. Resume/dedup state: `traversed.json`.
