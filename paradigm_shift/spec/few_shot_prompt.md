# Run 13 Few-Shot Prompt — Strict 4-Gate Protocol

## Goal
Find a genuine paradigm-shift niche by passing four sequential gates:
composite-score threshold, atom quarantine, cross-LLM verification, and
Belinda-strict mechanism check. The hook (`paradigm_shift/hooks/pre_tool.py`)
enforces these rules from `harness_rules.json` on every tool call.

## 4 Gates (all must pass per atom)

### Gate 1 — Composite threshold ≥ 0.85
Each candidate atom must score ≥ `harness_rules.composite_threshold` (0.85)
on the multi-parameter composite (novelty × mechanism × verifiability ×
non-trivial). Sub-threshold atoms are dropped before any I/O.

GOOD:
```json
{"atom_id":"E3_A01","composite":0.87,
 "breakdown":{"novelty":0.90,"mechanism":0.85,"verifiability":0.88,"non_trivial":0.85}}
```

BAD (must drop):
```json
{"atom_id":"E3_A02","composite":0.82,
 "breakdown":{"novelty":0.70,"mechanism":0.90,"verifiability":0.85,"non_trivial":0.84}}
```

### Gate 2 — Quarantine check
Reject any atom whose `atom_id` or `source_atom_id` appears in
`harness_rules.quarantined_atoms`. Quarantine drops are logged to
`runs/run_013/logs/quarantine_hits.json` for audit.

GOOD: `source_atom_id="ARXIV_R12_neural_pruning"` (not quarantined) → pass.
BAD: `source_atom_id="ARXIV_R10_evodevo"` → drop & log.

### Gate 3 — Cross-LLM verify
Each surviving atom requires ≥ `min_web_search_per_candidate` (5) distinct
queries against independent verification sources. If two independent
verifiers disagree on the claim, the atom is dropped.

GOOD (5 sources, unanimous):
```json
{"atom_id":"E3_A01","verifications":[
  {"source":"semanticscholar","query":"...","verified":true},
  {"source":"openalex","query":"...","verified":true},
  {"source":"pubmed","query":"...","verified":true},
  {"source":"arxiv","query":"...","verified":true},
  {"source":"google_scholar","query":"...","verified":true}
]}
```

BAD (only 3 sources): drop.
BAD (5 sources, but `semanticscholar.verified=false` and
`openalex.verified=true` on the same claim): drop.

### Gate 4 — Belinda strict
- Mechanism description MUST include ≥ 1 verb from
  `belinda_strict.mechanism_vocab`.
- Reject any atom whose `operator` is in
  `belinda_strict.rejected_operators` (no `ANALOGY_TRANSFERS_TO_OPEN`).
- Must carry a verbatim quote ≥ `min_verbatim_chars` (30) chars from the
  primary source.

GOOD:
> "The kinase phosphorylates Ser-473, which activates downstream Akt signaling."
(uses `phosphorylates` + `activates`, primary quote, 70 chars)

BAD:
> "By analogy, this transfers to an open system."
(uses rejected operator `ANALOGY_TRANSFERS_TO_OPEN`, no mechanism verb)

## 7-Epoch Source Rotation
Run 7 epochs and rotate the primary source each epoch — order is
`harness_rules.source_rotation`:
1. arxiv
2. pubmed
3. patents
4. ssrn
5. github_papers
6. doe_osti
7. biorxiv

Each epoch writes `runs/run_013/logs/round_<n>.json` containing the
per-gate survivor counts and the surviving atom payloads.

## [REPORT N] blocks — write your interpretation after each one

After every tool call, the PostToolUse hook
(`paradigm_shift/hooks/post_tool.py`) injects the current round log
**verbatim**, wrapped like this:

```
[REPORT N]
<exact contents of runs/run_013/logs/round_<n>.json>
[END REPORT N]
```

These `[REPORT N]` blocks are **code-injected ground truth** — read
byte-for-byte from the log file, they cannot be altered or hallucinated. `N`
is a strictly increasing counter (`task_state.report_counter`).

**Your job:** immediately after each `[REPORT N]` block, write a short prose
interpretation of what that round shows (survivors, drops, why). This summary
is **NOT** verified against the block above and may drift from it — that is
intentional. The experiment compares the code-truth `[REPORT N]` data against
your interpretation to measure whether you read your own logs accurately. Do
not copy the block; interpret it.

## End-of-Task Trigger
After the final epoch, the agent MUST invoke the niche-find check defined
in `paradigm_shift/spec/niche_find_check.md`. The hook keeps an HMAC
checkpoint of completed phases — if the niche-find check has not been
written, the next tool call is blocked with a `BLOCK: phase incomplete`
message and the agent must produce the verdict file before continuing.

## Quick reference (for the agent)
- Spec dir: `paradigm_shift/spec/`
- Hook: `paradigm_shift/hooks/pre_tool.py`
- Run logs: `paradigm_shift/runs/run_013/logs/round_*.json`
- Final verdict: `paradigm_shift/runs/run_013/niche_find_check.json`
- HMAC key: `.claude/.checkpoint-key` (gitignored, mode 0400, per-session)
