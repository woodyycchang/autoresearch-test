# INPUT_TRANSCRIPT_001 provenance

**File:** `tari/inputs/belinda_li_self_models_canonical.txt` (canonical, line-numbered form)
**Raw source:** `tari/inputs/belinda_li_self_models.txt` (single-line upload form)
**Speaker:** Belinda Li, MIT EECS PhD student, advisor: Jacob Andreas
**Venue:** Colloquium talk (Cornell CS Colloquium series, May 2026 based on talk content references)
**Duration / length:** 636 sentences (~10000 words)
**Topic:** "Building AI systems that model users, the world, and themselves" — internal mental models in language agents.

## Why this transcript was chosen for INPUT_TRANSCRIPT_001

Three reasons, documented in `design/tari_design_v1.md` §5:

1. **Self-evident match.** The talk is explicitly about self-models in language agents — the same framework TARI's audit step uses (Belinda's Q1/Q2/Q3). Bootstrapping a self-model-audit pipeline on a self-model talk is a closed loop: if TARI's audit cannot handle this transcript, it cannot handle any transcript.

2. **Frontier content (2025-2026).** The talk references Anthropic Opus 4.6 audit work and OpenAI self-model papers, placing content firmly in 2025-2026 frontier AI research. Niche-mining-autoresearch saturated in this regime (1071 rounds, 0 PASS) — if TARI extracts source-traceable candidates from this same regime, the comparison is direct.

3. **Rich atom structure.** Talk has explicit world-model / user-model / self-model sections, each with named techniques: probing, activation patching, GATE (generative active task elicitation), OPEN (Bayesian preference inference), self-explanation training. That structure should let atom_extractor.py find 30+ atoms across 3-5 thematic clusters, providing substrate for non-trivial brainstorm combinations.

## Pre-processing

The raw upload was a single-line file (no newlines). `tari/preprocess_transcript.py` splits on sentence-end markers (`.!?` followed by whitespace + capital letter) to produce the canonical line-numbered form. The canonical form has 636 lines, one sentence per line. **Line numbers in the canonical file are the canonical provenance addresses used throughout TARI.**

## What is NOT in this transcript

The transcript starts with the host's introduction and ends with the closing Q&A. It contains:
- Speaker name attribution at lines 2-4
- Talk content (mostly continuous monologue) from line 6 through line ~610
- Audience questions throughout, interleaved (NOT separately marked)
- Closing thanks at the end

Audience-question interleaving means snippet boundaries will sometimes fall in the middle of a Q&A exchange. snippet_decomposer.py uses topic-shift phrase detection to handle this conservatively; some atom_extractor outputs will contain audience-question fragments. This is acceptable — the verbatim quote check still anchors them to the transcript.

## Honest framing

The transcript is a single-speaker frontier talk. TARI v1 epoch 1 is therefore biased toward this speaker's framing of internal mental models. The pipeline is *designed* per-transcript; cross-transcript brainstorming is explicitly out of scope for v1.

If TARI v1 epoch 1 produces candidates that survive audit + external verification, those candidates are best characterized as **derived from Belinda Li's self-model framework**, not as discoveries Claude made independent of the talk. That framing is honest: TARI's value over mining is precisely that the candidate's provenance is external and traceable.
