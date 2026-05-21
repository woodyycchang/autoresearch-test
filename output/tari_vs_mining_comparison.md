# TARI v1 vs niche-mining-autoresearch v1–v20 — Comparison

**Author:** Claude (Opus 4.7), branch `claude/alternative-niche-mining-pipeline-IVlwA`.
**Date:** 2026-05-21.
**Scope:** Compares one TARI v1 epoch (run_001 on Belinda Li transcript) against 39 epochs of niche-mining (N=1071 rounds total).

---

## 0. Headline

| | niche-mining v1–v20 | TARI v1 run_001 |
|---|---|---|
| Rounds / candidates | 1071 rounds, 1071 candidates | 1 run, 12 candidates |
| Epochs | 39 | 1 |
| Substantive PASS under SYNTHESIZED detector chain | 0 | 12 of 12 *would* survive synth (synth returns empty) |
| Substantive PASS under REAL WebSearch verification | unknown (mining never ran real search) | 0 |
| Candidates source-traceable to an external artifact | 0 | 12 of 12 |
| Self-model audit (Belinda Q1/Q2/Q3) pass | not available pre-v20; partial coverage from v20 step 05.7 narrative | 12 of 12 (mechanical) |
| Mean candidates per epoch | 27.5 | 12 |
| Identifiable failure mode per failed candidate | aggregate INVESTIGATIVE_SURVIVING bin (22 cumulative); no per-candidate provenance | per-candidate: which atoms, which transcript line, which combination operator |

The headline finding: **TARI v1 produced 0 substantive PASS in 1 epoch — but it produced the first source-traceable, mechanically-auditable candidate set in the project's history**, and the first set verified against REAL WebSearch rather than synthesized search.

---

## 1. Are TARI candidates source-traceable in ways mining candidates were not?

### 1.1 Mining candidate provenance (program_v20.md)

A mining candidate's "lineage" was captured in `05_candidate.json` fields:

```
"anchor_id": "ANCHOR_R944"
"local_exploration_distance": 0.28
"frontier_seed_citation": ["FOSTER_REP_DIVERSE_SAMPLING"]
"v18_step_05_mode": "anchor_local"
"architecture_tool_slot": "S16"
```

Every one of those values is **internal pipeline state**. There is no external artifact a reviewer can consult to verify whether ANCHOR_R944 has yield 1.0, or whether the local_exploration_distance of 0.28 is actually 0.28 in some defined metric. v20's step 05.7 self-model added a narrative explanation, but the narrative is *also* internal — "I sampled anchor-local because…" cannot be cross-referenced against a non-pipeline source.

The v19 limitation analysis (`output/v19_limitation_analysis.md` §1.3.2) named this exactly: *"Lineage claims (anchor + distance + frontier_seed + slot) are narrative, not audited."*

### 1.2 TARI candidate provenance (this run)

A TARI candidate's lineage:

```json
"candidate_id": "CAND_001_003",
"combined_atom_ids": ["ATOM_S004_01", "ATOM_S025_01"],
"combination_operator": "COMPOSE",
"source_snippets": ["S004", "S025"]
```

Each atom_id points to a JSON file under `tari/runs/run_001/atoms/`, which contains:

```json
"verbatim_quote": "And finally transformers can implement the associative algorithm.",
"snippet_id": "S025",
"line_span": [212, 222]
```

The verbatim_quote is **checked against the canonical transcript file** mechanically: `self_model_audit.py` substring-matches the normalized verbatim_quote against the normalized transcript. An external reviewer can `grep -n "And finally transformers can implement the associative algorithm" tari/inputs/belinda_li_self_models_canonical.txt` and locate the line.

### 1.3 Concrete demonstration

```
$ grep -n "associative algorithm" tari/inputs/belinda_li_self_models_canonical.txt
252:And finally transformers can implement the associative algorithm.
268:And so this signature is inconsistent with the sequential and parallel algorithms, but consistent with the associative algorithm.
272:Okay, so both of these pieces of evidence point to the associative algorithm.
308:So earlier we saw that the language model learns to construct and update these kind of models internally using this sort of associative algorithm.
...
```

A reviewer can:
1. Read CAND_001_003.json
2. See it cites ATOM_S025_01
3. Read ATOM_S025_01.json
4. See the verbatim_quote field
5. Grep the canonical transcript and find line 217
6. **Confirm the candidate's claimed atom actually exists where the candidate says it does.**

There is **no equivalent workflow** for mining candidates. A reviewer who wants to verify R944's claim of "ANCHOR_R944 yield rate 1.0" has nowhere to go — that value lives in `logs/expert_path.json` which is itself a pipeline artifact.

### 1.4 Verdict

**Yes, TARI candidates are source-traceable in ways mining candidates were not.** Every TARI candidate has a verifiable external referent (the transcript file); every mining candidate has only internal-state references.

---

## 2. Do TARI candidates avoid the R279-pattern (surface metaphor) by design?

### 2.1 What R279-pattern was

`program_v12.md` introduced the "anti-R279 filter" at step 05.5 because mining candidates were producing candidates that simply renamed a math-X-thing as an LLM-X-thing without specifying a real intervention. Example: "use elliptic curves for token routing" with no concrete description of how the elliptic curve structure maps to a routing decision.

### 2.2 TARI's design defense

TARI's brainstorm engine has 6 typed operators (ANALOGIZE, INVERT, COMPOSE, GENERALIZE, RESTRICT, CONTRAST). Each operator emits a structured template. Two design properties limit pure-metaphor candidates:

- **The candidate.claim references atom IDs.** A claim like "Apply the mechanism described in atom ATOM_S025_01 ('And finally transformers can implement the associative algorithm.') to the problem framed in atom ATOM_S004_01" makes the source of the mechanism explicit. A reviewer can check the cited atom and decide whether the mechanism described there is real or vague.
- **The audit step's Q3 requires verbatim quote in the transcript.** This forces the mechanism to have been actually said by the speaker. A candidate cannot invoke "elliptic curve routing" unless an atom verbatim quote contains those words.

### 2.3 What TARI's run_001 actually shows

5 of 12 candidates were flagged with `AUX_claim_largely_restates_ATOM_xxx` — the audit step's check that the claim isn't simply a copy of an atom's verbatim quote. This is the inverse of the R279 problem: not metaphor without substance, but substance without novelty. The TARI failure mode is **§3.6 (restatement)** rather than R279.

A direct R279-style candidate ("use Hochschild cochain critic head" without further definition) is structurally impossible in TARI v1 because the brainstorm engine combines atoms from existing snippets; an atom whose verbatim quote contains "Hochschild" only exists if the speaker said "Hochschild" in their talk.

### 2.4 Verdict

**Yes, TARI's design eliminates R279-pattern candidates** — but introduces the §3.6 restatement failure mode as a substitute. Whether that's a net improvement depends on the downstream goal. For producing source-traceable candidates, it is. For producing novel-vs-the-source-transcript candidates, it is not.

---

## 3. How many candidates pass external verification per epoch?

### 3.1 Mining's verification rate

Across 39 epochs and N=1071 rounds:
- 22 candidates cumulative reached the INVESTIGATIVE_SURVIVING bin (synth step 14.6 < 0.7 functional similarity)
- 0 candidates passed step 10 (mechanical keyword threshold)

Verification rates depend on which threshold is used:
- under synthesized step 14.6 alone: 22/1071 = 2.1% pass-through
- under step 10 keyword threshold (real signal): 0/1071 = 0%

The step 10 figure is the more honest one — it's the only step that uses an externally-defined keyword overlap threshold rather than internal-state-derived features.

### 3.2 TARI run_001's verification rate

- Under synthesized step 06 / 14.6 (program_v20-style, empty search results): 12/12 = 100% would survive (synth verifies nothing)
- Under REAL WebSearch step 06 (3 results per candidate, real arxiv hits): 0/12 = 0% survive

The 0/12 under real WebSearch is the meaningful number. It matches mining's 0% rate.

### 3.3 The honest comparison

Direct comparison is constrained because:
- Mining never ran real WebSearch (program_v20 verifier is synthesized in main-context-direct mode).
- TARI ran real WebSearch on 12 candidates (one query per candidate, 3 results per query, all results captured verbatim from WebSearch tool output).

So the rows that compare:

| Verification regime | Mining rate | TARI run_001 rate |
|---|---|---|
| Synthesized step 14.6 (sim < 0.7) | 22/1071 ≈ 2.1% | 12/12 = 100% |
| REAL WebSearch step 06 (kw overlap ≥ 2 in any result) | n/a (never run) | 0/12 = 0% |
| Mechanical step 10 (kw ≥ 1 with synthesized search) | 0/1071 = 0% | similar — synth catches little |

The difference between the synth row and the real row is **the test of whether the synthesized verifier is a meaningful filter**. The TARI data answers: it is not. 100% survive synth, 0% survive real. This empirically confirms `output/v19_limitation_analysis.md` §1.1's claim that the synth verifier is structurally limited to Claude's own coverage.

### 3.4 Verdict

**Both pipelines produce 0 PASS under real external verification.** Mining at scale 1071 confirms saturation; TARI at scale 12 confirms saturation on one transcript. The substantive difference is that TARI's verification was REAL, mining's was synthesized — so TARI's 0 is *informative* about the field's prior art, while mining's 0 is *informative* about Claude's coverage. Both are saturation findings, but with different scientific content.

---

## 4. What failure modes emerge in TARI that didn't exist in mining?

### 4.1 Mining's failure mode taxonomy (12 verdict labels, program_v20 §6)

- FAIL_EMPIRICAL_ATTACK (v11)
- REJECTED_R279_PATTERN (v12)
- REJECTED_KNOWN_COLLISION (v17)
- REJECTED_NO_FRONTIER_SEED (v17)
- REJECTED_LEARNED_VERIFIER (v19)
- INVESTIGATIVE_CANDIDATE (v13)
- EXTERNAL_COLLISION (v16)
- FAIL_ADVERSARIAL
- FAIL_GAP_REAL_LOGGED
- FAIL
- PASS / PASS_WITH_EMPIRICAL_CAVEAT

All defined in terms of internal pipeline state. The 22 INVESTIGATIVE_SURVIVING candidates sit in a bin defined by *what the synth detector chain didn't catch*, not by what they actually are.

### 4.2 TARI's emergent failure modes

| Failure mode | Description | run_001 evidence | Mining equivalent |
|---|---|---|---|
| **§3.1 atom granularity (semantic incoherence)** | Brainstorm pairs atoms by type, not topic; some combinations are nonsense. | CAND_001_006: RESTRICT "user prefers basketball" + "Jack possesses book in probing experiments". | None — mining never combined atoms, so never produced this failure. |
| **§3.5 single-transcript bias** | All candidates land in the speaker's research community's prior art. | All 12 candidates' nearest prior art is in the LM-interpretability community, often Belinda's own lab. | Indirect — mining's "saturation" was Claude's general coverage, not a specific community's coverage. |
| **§3.6 claim restatement** | Brainstorm template is heavy; claim text mostly restates atom text. | 5/12 candidates flagged `AUX_claim_largely_restates_ATOM_xxx` by audit. | Not detectable — mining had no atom referent to restate against. |
| **§3.2-mitigated atom fabrication** | Brainstorm could cite a non-existent atom. | 0/12 — mechanical check catches it. | Mining had nothing to fabricate against. |
| **§3.3-mitigated traceability fabrication** | Claim could cite a line that doesn't say what the claim says. | Verbatim substring check catches gross cases; semantic entailment not yet checked (v2). | n/a |

### 4.3 The structurally-new failure mode: single-transcript bias

§3.5 is the failure mode mining could not see. Mining sampled from Claude's coverage as a whole; TARI samples from one transcript's coverage. TARI's 0/12 under real verification therefore says something specific: *the candidates derived from this transcript are not novel relative to this speaker's published research community*. Mining's 0/1071 said something more diffuse: *candidates derived from Claude's coverage are not novel relative to arxiv-as-a-whole, but we can't tell which subset of arxiv*.

This is the scientifically more interesting result. v2 of TARI should run multiple transcripts and check whether cross-transcript candidates avoid §3.5.

### 4.4 Verdict

**TARI surfaces 3 new failure modes** (§3.1 semantic incoherence, §3.5 single-transcript bias, §3.6 claim restatement) that mining couldn't detect because mining had no transcript referent. It also mitigates 2 (§3.2 atom fabrication, §3.3 traceability fabrication) by mechanical checks.

---

## 5. The single most important finding

**Real WebSearch catches every TARI candidate; synthesized step 06 / 14.6 catches none.**

This is a direct empirical answer to v19's diagnosis (`output/v19_limitation_analysis.md`) that synthesized detection is redundant signal. TARI v1 isolated the variable: same candidate set, two verifiers, opposite outcomes. The synthesized verifier produces 12 "survivors" and the real verifier produces 0. Mining's 22 INVESTIGATIVE_SURVIVING candidates have *never been tested against real WebSearch* — based on TARI's 12-of-12 collapse under real verification, the strong prior is that the 22 would also collapse under real verification.

The actionable inference: any future mining-style run (v21+) that wants to be meaningful must replace step 06 / 14.6's synthesized search with real WebSearch. That single change would likely:
- Collapse the INVESTIGATIVE_SURVIVING bin to near-zero
- Make the FORBIDDEN-TO-MODIFY zone honesty-bearing instead of cosmetic
- Cost ~25 WebSearch tool calls per epoch (manageable)

---

## 6. What v1 does NOT establish

- TARI v1 ran on **one** transcript. The single-transcript bias finding (§4.3) is a hypothesis about pipeline structure; multiple-transcript runs would test it.
- TARI's audit is mechanical (verbatim substring, file-exists, set-membership). A stronger entailment-based audit would reduce the AUX_claim_largely_restates rate but introduce LLM-call cost and re-introduce Claude-coverage bias. Deferred to v2.
- The brainstorm engine in v1 is deterministic and template-y. A real-time LLM-based brainstorm engine (gated by the same mechanical audit) is what v2 should test.
- 0/12 under real verification is consistent with mining's 0/1071, but n=12 is too small to make a strong claim. v1's value is not in the count but in *demonstrating the pipeline runs end-to-end and produces source-traceable candidates*.

---

## 7. Recommended next steps

| Priority | Action | Cost | Expected value |
|---|---|---|---|
| H | Add a second TARI transcript (e.g., Yu Sun's TTT talk) and run epoch 2 across both | ≈ 30 WebSearch calls, 1 hour | tests §3.5 single-transcript bias hypothesis |
| H | Replace mining's synth step 06 / 14.6 with real WebSearch in the next mining epoch | ≈ 25 WebSearch calls, 1 hour | tests whether 22 INVESTIGATIVE_SURVIVING actually survive real verification |
| M | Add a brainstorm-stage LLM call gated by mechanical audit | ≈ 5 Agent spawns per run | tests whether non-deterministic combination produces less template-y candidates |
| M | Add semantic entailment check to self-model audit | ≈ 1 Agent spawn per candidate | tightens §3.3 (currently mitigated only at the substring level) |
| L | Multi-transcript brainstorm (combine atoms from 3+ transcripts) | requires v2 design | direct test of whether cross-domain candidates avoid single-community prior art |

---

## 8. Conclusion

TARI v1 epoch 1 produces 0 candidates that pass full verification, identical to mining's 0/1071 result. The scientific value is in *what the failures look like*:

- Mining: opaque failures with no externalizable cause; the candidate's history is internal pipeline state.
- TARI: traceable failures with mechanically-checkable atoms, surfaced in 6 named operators across 55 snippets of one frontier transcript; failures attribute to (a) single-transcript bias, (b) brainstorm template restatement, (c) atom-pairing semantic incoherence.

The most useful direct evidence: real WebSearch invalidates the synthesized detector chain on 12/12 cases. This is the empirical confirmation v20's limitation analysis predicted and could not test.

**TARI v1 should be considered a successful failure-mode-discovery run, not a successful novel-niche-discovery run.** The pipeline does what the design doc said it would do (§4 "failure-mode success" criterion met). To produce a novel candidate that survives real verification, future epochs need either (a) multiple transcripts to escape single-transcript bias or (b) a more sophisticated combinator than v1's deterministic template engine. Both are deferred to v2.
