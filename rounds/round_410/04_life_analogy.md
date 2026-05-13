# Life Analogy — Sumo basho (rotating regional tournament schedule)

The **Sumo honbasho** schedule:
- 6 tournaments per year, each in an **odd-numbered month** (Jan/Mar/May/Jul/Sep/Nov).
- 4 host cities with weighted rotation: **Tokyo** (3 tournaments: Jan/May/Sep), **Osaka** (Mar), **Nagoya** (Jul), **Fukuoka** (Nov).
- Each tournament is 15 days; all rikishi (wrestlers) travel to the host city.
- The home stadium (Tokyo Ryōgoku) is privileged: 3 of 6 tournaments; the regional rotations cover other regions seasonally.

The unique principle: **bi-monthly rotation through 4 host venues with a weighted "central + periphery" pattern** — central venue (Tokyo) is over-weighted (3/6); other venues each get 1/6 share. The schedule is FIXED and cyclic; wrestlers travel deterministically with the calendar.

## Analogical mapping → rotating-host multi-agent communication

- Tournament ↔ a multi-agent collaboration round
- Wrestlers ↔ the agent population
- Host city ↔ a chosen "central coordinator agent" for that round
- Tokyo over-weighting ↔ a privileged anchor agent appears in 1/2 of rounds
- 4-city rotation ↔ a small fixed set of K=4 candidate coordinators

The mechanism: **BASHO-ROTATION weighted-rotation multi-agent coordinator** — in an N-agent LLM system needing a single coordinator per round, designate a small fixed set of K=4 candidate-coordinator agents and assign them tournament-style weighted rotation: the "central" agent c_0 is chosen 50% of rounds; the 3 "peripheral" agents c_1, c_2, c_3 each chosen 1/6 of rounds. Schedule is FIXED and DETERMINISTIC (rotates by round number mod 6). All other N-K agents act as "rikishi" — they communicate only through the current coordinator. Differs from (a) RECONCILE round-table (no central rotation, every agent votes), (b) MAD multi-agent debate (no fixed coordinator schedule), (c) standard leader-election (probabilistic, not pre-scheduled), (d) A2A protocol (peer-to-peer, no fixed coordinator) by enforcing (i) FIXED PRE-SCHEDULED coordinator rotation + (ii) WEIGHTED (central over-represented) selection + (iii) SMALL K=4 candidate pool.

## Note on adjacency

The multi-agent-comm form fits. Adjacent: RECONCILE, MAD, A2A protocol, leader-election. Distinct: WEIGHTED FIXED PRE-SCHEDULED rotation (no negotiation). Closest twin: round-robin coordinator selection (uniform weighting, not weighted central).
