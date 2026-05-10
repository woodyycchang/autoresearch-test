# disagreement_log.md

Cross-agent verification (step 12) mismatches are logged here for human
review at the next 25-round checkpoint.

Format per entry:

```
## Round NNN
- Primary verdict: PASS|FAIL (hit_count = N)
- Verification verdict: PASS|FAIL (hit_count = M)
- Disagreement details:
  - URL: ...
    - Primary said: hit/miss
    - Verification said: hit/miss
    - Implication: (which agent likely biased)
- Action: human reviews this round before incorporating into final stats
```

---

(empty — agent populates this when step 12 produces disagreement)
