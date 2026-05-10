# STARTUP_PROMPT.md

## How to use this repo with Claude Code

### First time setup (one-time)

1. Make sure Claude Code is installed:
   ```
   npm install -g @anthropic-ai/claude-code
   ```

2. Open terminal in this repo's directory:
   ```
   cd niche-mining-autoresearch
   claude
   ```

3. In Claude Code, switch to Opus model for 1M context:
   ```
   /model opus
   ```

---

### To START a fresh run (round 1)

Paste this prompt into Claude Code:

```
You are inheriting an autonomous research project. Read these three files in
order:

1. README.md — overview of what this repo does
2. saturation_evidence.md — 138 verified rounds of prior human-run data
3. program.md — your operating instructions (READ THIS CAREFULLY)

Then begin executing the pipeline from round 1.

Critical rules:
- Follow the file chain exactly. Each step reads the previous step's file.
- Never skip step 06 (real web_search). The mechanical keyword rule in step
  07 requires step 06's raw response.
- Apply the mechanical keyword overlap rule honestly. Do not narrow
  content_words after seeing search results.
- Honest self-audit in step 11 is more valuable than a clean fake run.
- Do not stop mid-batch to ask permission. Continue until you hit a
  stopping condition defined in program.md.
- Stopping conditions: PASS found, 50 rounds completed, 3+ violations,
  web_search rate-limited, or 5 consecutive duplicates.

Begin round 1. Create rounds/round_001/ and execute steps 01 through 12.
```

---

### To RESUME a run (from where last session stopped)

Paste this prompt:

```
You are resuming an autonomous research project. Read:

1. program.md — operating instructions
2. logs/candidate_pool.md — already-tested candidates (DO NOT duplicate)
3. logs/compliance_log.md — past violations (don't repeat)
4. The most recent stats file in output/

Look at rounds/ folder. Find the highest-numbered round folder. Your next
round is N+1.

Continue executing the pipeline from round N+1. Same rules as before.
Continue until a stopping condition is hit.
```

---

### To CHECK progress mid-run

Paste this prompt:

```
Run aggregate stats. Read all 10_decision.json files in rounds/. Read all
11_audit.json and 12_verification.json files. Compute:

- Total rounds completed
- PASS count
- FAIL count
- Compliance rates (step 06, step 07, step 10)
- Trehan & Chopra failure mode incidence counts
- Verification disagreement count
- Saturation p-value (binomial test against 1%, 5%, 10% novelty rate)

Write the result to output/stats_round_NNN.json where NNN is the latest
round number.

Do NOT execute new rounds. Just compute stats on existing data.
```

---

### When you want to STOP

Paste:

```
Stop the run. Write a final report to output/final_report.md containing:

1. Total rounds attempted
2. PASS count + the round numbers
3. FAIL count
4. Compliance violation summary
5. Trehan & Chopra failure mode tally
6. Cross-agent verification disagreement summary
7. Statistical saturation conclusion
8. Honest assessment: did the file-chain + keyword rule + verification
   actually prevent the failure modes seen in prior chat-based runs?
9. Recommendations for thesis writing
```

---

### Notes

- Token cost is not a concern per user instruction. Use Opus 4.7 freely.
- Each round may take 5-15 minutes of agent time. Plan accordingly.
- Cross-agent verification (step 12) can be a fresh agent in a new
  Claude Code session, OR the same agent with explicit adversarial framing
  ("re-judge as a skeptical reviewer"). The latter is faster but less
  rigorous; choose based on your needs.
- If you find a PASS round, manually verify by:
  - Reading rounds/round_NNN/06_search_raw.json
  - Independently searching the candidate domain on Google Scholar
  - Asking advisor before claiming it's a real niche
