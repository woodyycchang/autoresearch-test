# Layer 6 Failure Analysis — Run 2 False Positives

**Author:** Claude (Opus 4.7 / `claude-opus-4-7[1m]`), branch `claude/paradigm-shift-finder-EAtbj`.
**Date:** 2026-05-22.
**Status:** Phase 1 of Run 3 — diagnostic doc preceding Layer 6 v2 rebuild.

---

## 0. The 3 false positives

Run 2 produced 3 SURVIVES_MARKET_CHECK candidates: `CAND_run_002_007`,
`CAND_run_002_008`, `CAND_run_002_009`. All three are PREDICTION_RESOLVES_BLOCKER
candidates citing Yu Sun's long-context blocker atom
(`ATOM_T002_S020_BLO_01`) combined with one of three Roberts predictions.

The Yu Sun blocker atom verbatim:
> "And this problem, this long context, really arises because we're trying to
> find the workarounds, which in turn is because the old rules of machine
> learning dictate that we can't change the model ways at test time."

Each candidate's templated claim says, in effect: *the predicted future mechanism
resolves the long-context blocker.*

---

## 1. The collision Layer 6 v1 missed

**Yu Sun himself co-authored a December 2025 paper that directly addresses this
exact blocker:**

- **arXiv:2512.23675** — "End-to-End Test-Time Training for Long Context"
  (Yu Sun is one of 14 co-authors; published Dec 2025). The paper formulates
  long-context language modeling as continual learning rather than architecture
  design: the model continues learning at test time via next-token prediction
  on the given context. For 3B models, TTT-E2E scales with context length on
  par with full-attention Transformer, while Mamba 2 and Gated DeltaNet do not.

- **arXiv:2512.13898** — "Let's (not) just put things in Context: Test-Time
  Training for Long-Context LLMs" (Dec 15, 2025). Independent group; same
  thesis: targeted gradient updates on the given context (qTTT) overcome
  score dilution of static self-attention.

These two papers **directly publish what CAND_007/008/009 claim**: that a
test-time-training-shaped mechanism resolves the long-context blocker Yu Sun
described in his talk. Yu Sun's S020 atom literally hints at this — "the
simple idea is, what if we also do gradient descent on the model at test time?"
And that's what arxiv:2512.23675 builds out.

The candidates are not paradigm-shift candidates. They are **published**.

---

## 2. Why Layer 6 v1 failed to detect this

Layer 6 v1's algorithm (`paradigm_shift/market_verifier.py`):

1. Extract primary noun phrase = top-3 most frequent content words from
   candidate's `claim` + `first_principles_validity_hypothesis` +
   `why_potentially_useful`.
2. Build 5 query reformulations:
   - `"<primary> startup"`
   - `"<primary> YC company"`
   - `"open source <primary>"`
   - `"<primary> Series A OR Series B"`
   - `"<primary> founded 2024 OR 2025 OR 2026"`
3. For each result, "strong match" = ≥3 content-word overlap with primary
   phrase in title+snippet.
4. Verdict: 0 strong matches across all reformulations → SURVIVES_MARKET_CHECK.

For CAND_007/008/009, the extracted primary phrase was
**`blocker market prediction`** — produced because the templated candidate
fields have those three content words most frequently. The 5 queries became:

- `blocker market prediction startup`
- `blocker market prediction YC company`
- `blocker market prediction Series A OR Series B`
- `blocker market prediction founded 2024 OR 2025 OR 2026`
- `open source blocker market prediction`

These returned **Polymarket / Dome / Better Opinions / Kalshi** results (real
prediction-market YC startups), but the ≥3-content-word overlap check
required `{"blocker", "market", "prediction"}` to all appear in title+snippet.
Dome's title is "Dome: A unified API for prediction markets" — only "market"
and "prediction" overlap; "blocker" is absent. So Dome was *not* counted as a
strong match. SURVIVES verdict by accident of vocabulary.

### Four structural defects exposed

**D1. Primary phrase is template residue, not semantic anchor.**
"blocker market prediction" is a coincidence of template field repetition. It
is not the semantic content of the candidate. The candidate's actual semantic
content is *"test-time gradient updates resolve long context."* No primary
phrase extracted captures this.

**D2. Keyword overlap is too brittle to be a collision detector.**
A Dec 2025 paper titled "End-to-End Test-Time Training for Long Context" has
zero overlap with primary phrase `blocker market prediction`. Even if the
phrase were `long context training`, exact-keyword matching would miss titles
that paraphrase ("End-to-End TTT" vs "long context training").

**D3. No speaker self-publish check.**
The most-likely real-world collision is the speaker themselves publishing the
candidate's idea — because the candidate atoms come from the speaker's talk,
and the speaker is most likely to follow up on their own hints. Layer 6 v1
never issues a `"<speaker_name> <topic>"` query.

**D4. No date weighting.**
A 2018 paper restating an idea is weak evidence the idea is taken; a 2024-2025
follow-up by the *talk's own speaker* is strong evidence. Layer 6 v1 treats
all results uniformly.

---

## 3. The right detection chain (what v2 must do)

To catch the Yu Sun collision, Layer 6 v2 must run **at least one** of:

**Path A — semantic embedding.** Embed candidate's claim + atom verbatim
quotes; embed candidate web_search snippets; compute cosine similarity;
flag any similarity ≥ 0.5 as COLLISION. The "End-to-End Test-Time Training
for Long Context" abstract would have cosine ≥ 0.6 with the candidate's
TTT-resolves-long-context claim.

**Path B — speaker self-publish check.** Extract the source-transcript
speakers; web_search `"{speaker_name} {primary_keyword} 2024-2026"`; if any
recent paper title+abstract semantically matches the candidate, flag as
COLLISION_SPEAKER_SELF. For Yu Sun + "long context" the Dec 2025 follow-up
papers surface immediately.

**Path C — recent-paper-weighted similarity.** Treat results from the last
12 months at 2× weight in any similarity calculation, because the speaker's
own recent follow-up is the most likely real collision.

**Path D — cross-LLM sanity check.** For the top-3 survivors, generate a
copy-paste-ready prompt asking a different LLM (Gemini / GPT) "Has anyone
already published or built this?" and persist to
`cross_llm_verify_queue.json`. The user runs the prompt elsewhere and feeds
results back.

These are the four upgrades the user prescribed. Together they make Layer 6
**speaker-aware, semantically-grounded, and time-weighted** — three properties
v1 lacked.

---

## 4. Honest limits of v2 (what it still cannot catch)

- **Semantic similarity uses an embedding model.** Whatever embedding is used
  (sentence-transformer, OpenAI ada-002, etc.) has its own biases. A
  candidate that paraphrases a 2024 paper using vocabulary the embedding
  hasn't seen well will still slip through. Mitigation: combine with the
  speaker self-publish check.

- **Speaker self-publish check requires correct speaker-name extraction.**
  The manifest already has `speaker` per transcript; v2 reads from there.
  Manifest typos → wrong query → false negative.

- **Recent paper weight requires a publication-date parser.** WebSearch
  doesn't always surface dates. v2 will use a heuristic (look for `20\d{2}`
  in title/snippet/url; fall back to assuming "unknown date"). Dates wrong →
  weighting wrong.

- **Cross-LLM sanity check is a manual loop.** The user runs the prompt in
  a separate session. This is not a tight loop; results may be stale.

These are not bugs to fix in v2; they are the v2 contract's honest edges.

---

## 5. Action items (next phases)

- AI-1. (Phase 2) Implement `paradigm_shift/market_verifier_v2.py` with the
  4 upgrades. Spec doc at `design/market_verifier_v2_spec.md`.
- AI-2. (Phase 3) Re-audit Run 2's full candidate set with v2; confirm
  CAND_007/008/009 now flagged as COLLISION (specifically
  COLLISION_SPEAKER_SELF on Yu Sun's Dec 2025 papers).
- AI-3. (Phase 4) Run paradigm_shift Run 3 on the same 5 academic transcripts
  with Layer 6 v2; expect 0-2 SURVIVES_MARKET_CHECK_V2 candidates.
- AI-4. (Phase 5) Comparison doc at `output/run_002_vs_run_003.md`; report
  v2 retrospective catch rate and surviving Run-3 candidates.
- AI-5. (Post-run) Generate the `cross_llm_verify_queue.json` with paste-ready
  prompts for the top-3 Run-3 survivors. User runs externally.
