# session_log.md

Append-only log of session starts and stops. Helps track when the agent
restarted between sessions and what state it inherited.

Format per entry:

```
## Session NNN — 2026-MM-DD HH:MM
- Action: STARTED FRESH | RESUMED FROM ROUND X
- Rounds attempted this session: X to Y
- Rounds completed this session: Z
- Stopping reason: PASS found | 50 rounds done | rate limit | duplicates | violations | user halt
- Notes: (any anomalies)
```

---

(empty — agent appends on each session start)
