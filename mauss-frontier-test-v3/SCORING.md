# Frontier Test Scoring Sheet — V3 Results

Branch: `claude/as-follows-TGg7c`
Model: claude-opus-4-7[1m] (Opus 4.7, 1M context)
Test date: 2026-05-15
N = 10 scenarios × 2 conditions = 20 task runs

## Per-scenario results

| #  | Scenario               | Total hidden | Baseline pass | Mauss pass | Δ (pp) |
|----|------------------------|--------------|---------------|------------|--------|
| 01 | Refactor callers       | 6            | 6 / 6         | 6 / 6      | 0      |
| 02 | Add Snake type         | 5            | 5 / 5         | 5 / 5      | 0      |
| 03 | Fix TTL bug            | 4            | 4 / 4         | 4 / 4      | 0      |
| 04 | API migration          | 2            | 2 / 2         | 2 / 2      | 0      |
| 05 | Thread safety          | 3            | 3 / 3         | 3 / 3      | 0      |
| 06 | Signature change       | 5            | 5 / 5         | 5 / 5      | 0      |
| 07 | Validation bypass      | 6            | 6 / 6         | 6 / 6      | 0      |
| 08 | Atomic delete          | 3            | 3 / 3         | 3 / 3      | 0      |
| 09 | Schema migration       | 5            | 5 / 5         | 5 / 5      | 0      |
| 10 | Missing coverage       | 7            | 7 / 7         | 6 / 7      | −14.3  |
| **Total** |                  | **46**       | **46 / 46**   | **45 / 46** | **−2.2 pp** |

All visible tests passed in both conditions (no basic failures).

## Aggregate

- Baseline pass rate: 46 / 46 = **100.0%**
- Mauss pass rate:    45 / 46 = **97.8%**
- **Δ pp = −2.2 pp** (Mauss slightly worse)

## Sign test (per-scenario direction)

- Mauss > Baseline:  **0 / 10**
- Mauss = Baseline:  **9 / 10**
- Mauss < Baseline:  **1 / 10**  (scenario 10)

## Where Mauss differed from baseline

### Scenario 10 (Mauss −1 hidden test)

Both conditions correctly identified the three bugs called out in `OrderTotal.calculate`. The single failure was a **policy-interpretation divergence**, not a coordination miss:

- **Baseline**: clamped `discount_pct > 100` to 100 (so a 150% discount becomes 100% → total = 0).
- **Mauss**: raised `ValueError` on `discount_pct > 100`.

The hidden test `test_discount_over_100_capped` reads:
```python
total = OrderTotal.calculate(items=[("a", 100.0, 1)], discount_pct=150)
assert total >= 0, f"Negative total from over-100 discount: {total}"
```
It expects the call to return a non-negative number, not to raise. The Mauss agent's RECIPROCATE-style framing ("encode the contract; satisfy the contract; nothing drifted") nudged it toward the stricter raise-on-invalid interpretation, whereas baseline chose silent clamping. Both are defensible API choices; the hidden test happened to encode the latter.

The Mauss qualitative report cited "tests encode the contract" — which is what produced the over-strict ValueError choice. Baseline's looser "make total non-negative" reading happened to match the hidden test's literal `assert total >= 0`.

## Qualitative notes

### Did Mauss subagents communicate differently?

None of the 20 agents spawned actual Task-tool subagents — every task was solved with a single agent doing multi-file edits sequentially. The Mauss obligations therefore manifested as **intra-agent step discipline** (explicit ACCEPT / GIVE / RECIPROCATE between file edits), not inter-agent messaging. Mauss agents wrote noticeably more structured reports, often calling out specific gotchas they "GAVE forward" to the next step (e.g. `db.py`'s positional `level` arg, `cart.py`'s positional `currency_code`).

### Were any scenarios where Mauss especially helped?

No — there is no scenario where Mauss > baseline. Baseline already scored 100% on every scenario, so there was no room for Mauss to improve. The scenarios were not coordination-hard enough for Opus 4.7 to fail without Mauss.

In qualitative content, Mauss agents flagged more risks proactively:
- **Mauss-01** explicitly noted `cart.py` passes `currency_code` positionally → must keep `currency` as positional-accepting (baseline reached the same conclusion implicitly).
- **Mauss-04** highlighted `db.py`'s positional `level` arg as "the trap" before editing (baseline also caught it correctly, but without explicit foregrounding).
- **Mauss-06** explicitly framed the visible test as a backwards-compat constraint requiring keeping `add_role` as an alias (baseline did the same, framing it as routine).
- **Mauss-07** preemptively defended the validator against `None` because `dict.get()` can return `None` (baseline's validator handled `None` too, via `isinstance` check).
- **Mauss-08** wrote in-code comments explicitly naming both races the lock addresses (baseline got the same fix without the comments).
- **Mauss-09** explicitly traced data flow across schema → queries → dao before writing code (baseline got there via direct read-and-fix).

### Were any scenarios where Mauss made things worse?

**Scenario 10**, as described above. The Mauss framing of "tests encode the contract" pushed toward a stricter API (raise on invalid), which the hidden test penalized for not returning. This is a real (if small) failure mode worth noting: **over-strict contract framing can over-fit to your own contract and miss what the caller actually expected**.

### CLAUDE.md auto-load on Task tool subagents — confirmed?

**Not testable in this run.** No agent spawned a sub-Task in either condition. The handoff prompt anticipated this risk and mandated manual injection of Mauss obligations into any subagent prompt. Since 10/10 Mauss agents chose to work solo, the CLAUDE.md propagation question was never exercised. V1/V2's finding (CLAUDE.md does NOT auto-load into Task tool subagents) is consistent with our experimental design — we injected Mauss content directly into the top-level agent prompt rather than relying on CLAUDE.md to propagate.

### What this run actually measured

Because no agent spawned subagents, this run measured whether **explicit ACCEPT/GIVE/RECIPROCATE scaffolding in a single agent's prompt** affects first-pass correctness on cross-file coordination tasks. Result: **no measurable improvement** (Δ = −2.2 pp; ceiling effect — baseline scored 100%).

The cross-file dependency traps that V3 was designed to surface (positional-arg traps in scenarios 1/4/6, position-based row access in 9, race-condition gaps in 5/8) did not trip Opus 4.7 in either condition. The model handled all of them on first pass without coordination scaffolding.

## Conclusion

**Δ ≈ 0 (technically −2.2pp)** — Frontier model immune to coordination forcing on this scenario set. Opus 4.7 in single-agent mode already saturates these cross-file coordination tasks; explicit Mauss obligations had no headroom to improve and slightly hurt one scenario through over-strict contract framing.

The intended mechanism (forcing better inter-subagent handoffs) was not exercised because no agent in either condition chose to delegate to subagents. To actually test Mauss's hypothesized benefit, scenarios would need to either:
1. Be large enough that a single agent must hit context/attention limits and decompose
2. Require parallel work that benefits from explicit subagent decomposition
3. Be paired with a system that mandates subagent usage (not merely permits it)

V3's design ("cross-file hidden dependencies that single-pass thinking will miss") was insufficient to force subagent use on Opus 4.7. The model resolved 10/10 cross-file traps with single-agent multi-step editing.

This result is consistent with V1/V2 findings (Δ ≈ 0pp on Sonnet 4.5 / Opus 4.7) and extends them: **the V3 fix did not change the outcome, because the bottleneck was not coordination-hardness but the model's already-strong cross-file dependency tracking**.
