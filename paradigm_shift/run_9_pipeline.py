"""Run 9 pipeline — deep tool use + recursive failure-driven self-improvement.

Eight layers on top of Run 6/7/8 infrastructure:

  Layer 1: snippet_decomposer  (reuse Run 6 purified snippets)
  Layer 2: atom_typer + Run 9 quality filter v2 (rejects past-tense
           "predictions", truncated mid-sentence atoms, "I think" misfires)
  Layer 3: analogy_engine with Run 9 cross-speaker diversity gate
           (speaker_diversity >= 2, where speaker = mapped from T-id;
            T007/T013 both = "karpathy" so the same-speaker pair fails)
  Layer 4: Belinda 3-question audit (verbatim line existence via view)
  Layer 5: first_principles_stress + arXiv citation gate
           (>= 3 web_search per sub-claim, captured in claim_evidence_log)
  Layer 6: market_verifier_v2 + speaker self-publish detector
           (>= 3 web_search per speaker; flags atoms whose verbatim quote
            is the speaker pitching their own published arxiv work)
  Layer 7: community_saturation_check  (>= 5 web_search per topic)
  Layer 8: recursive_failure_diagnostic (NEW)

The harness (Claude main agent) is responsible for issuing real
WebSearch calls; this module computes the gates and writes the
deterministic state.  Web search results are loaded from
phaseX_evidence_log.json files written by the harness.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

from analogy_engine import (  # noqa: E402
    VALID_TYPED_COMBINATORS,
    ParadigmCandidate,
    short_quote,
    make_prediction_grounded_in_principle,
    make_analogy_transfers_to_open,
    make_blocker_dissolved_by_principle,
    make_prediction_resolves_blocker,
)


# ---------- Speaker map (Run 9 NEW) ----------
TRANSCRIPT_TO_SPEAKER = {
    "T001": "belinda_li",      # MIT, self-models talk
    "T002": "yu_sun",          # Stanford/NVIDIA, TTT
    "T003": "nicholas_roberts",
    "T004": "valerie_chen",
    "T005": "amrith_setlur",
    "T007": "karpathy",        # Intro to LLMs
    "T008": "silicon_valley",  # "Silicon Valley doesn't understand the big picture"
    "T009": "sam_altman",      # Sam Altman startup lecture
    "T010": "hinton",          # Hinton "Will AI outsmart"
    "T011": "lecun",           # Yann LeCun JEPA
    "T012": "hinton",          # Hinton forward-forward — SAME SPEAKER AS T010
    "T013": "karpathy",        # Karpathy "software changing again" — SAME AS T007
    "T014": "naval_ravikant",  # Naval Ravikant
}


# ---------- Layer 2: Run 9 atom quality v2 ----------

PAST_TENSE_RECOLLECTION_MARKERS = [
    r"\bat the time\b",
    r"\bback then\b",
    r"\bI used to\b",
    r"\bwe used to\b",
    r"\bin the (past|old days)\b",
    r"\bwere seen as\b",
    r"\bI was\b\s+\w+ing",
]

TRUNCATED_MIDSENTENCE_TAILS = [
    r"\bbetween [a-zA-Z ]+ and\.$",
    r"\bbecause\.$",
    r"\bbut\.$",
    r"\bI think it was like\.$",
    r"\band\.$",
    r"\bis\.$",
    r"\bof\.$",
]

VAGUE_PREDICTION_PHRASES = [
    r"^I think that's a reasonable prediction",
    r"^I think it was like\b",
    r"^maybe$",
]


def is_past_tense_recollection(text: str) -> bool:
    for pat in PAST_TENSE_RECOLLECTION_MARKERS:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def is_truncated_midsentence(text: str) -> bool:
    s = text.strip().rstrip()
    # Look at the last sentence ending in "." — if it ends with a connector
    last = s.split(".")[-2] if "." in s else s
    for pat in TRUNCATED_MIDSENTENCE_TAILS:
        if re.search(pat, last + ".", re.IGNORECASE):
            return True
    return False


def is_vague_meta_comment(text: str) -> bool:
    for pat in VAGUE_PREDICTION_PHRASES:
        if re.search(pat, text.strip(), re.IGNORECASE):
            return True
    return False


def atom_quality_v2(atom: dict) -> Tuple[bool, str]:
    """Return (keep, rejection_reason). True = keep."""
    quote = atom.get("verbatim_quote", "")
    atype = atom.get("paradigm_type", "")
    if atype == "prediction":
        if is_past_tense_recollection(quote):
            return False, "RUN9_QV2_PAST_TENSE_RECOLLECTION_MISLABELED_AS_PREDICTION"
        if is_vague_meta_comment(quote):
            return False, "RUN9_QV2_VAGUE_META_COMMENT_NOT_SUBSTANTIVE_PREDICTION"
    if atype == "first_principle":
        if is_truncated_midsentence(quote):
            return False, "RUN9_QV2_TRUNCATED_MIDSENTENCE_FIRST_PRINCIPLE_NO_COMPLETED_CLAIM"
    if len(quote.split()) < 12:
        return False, "RUN9_QV2_TOO_SHORT_LESS_THAN_12_WORDS"
    return True, ""


# ---------- Layer 3: Run 9 cross-speaker diversity gate ----------

def speaker_of(transcript_id: str) -> str:
    return TRANSCRIPT_TO_SPEAKER.get(transcript_id, transcript_id)


def speaker_diversity(transcript_ids: List[str]) -> int:
    return len(set(speaker_of(t) for t in transcript_ids))


def cross_speaker_ok(cand: dict) -> Tuple[bool, str]:
    ts = cand.get("source_transcripts", [])
    if speaker_diversity(ts) < 2:
        speakers = [speaker_of(t) for t in ts]
        return False, f"RUN9_L3_SINGLE_SPEAKER_COLLISION_speakers={speakers}"
    return True, ""


# ---------- Layer 6: speaker self-publish detector ----------
# We don't have direct API access to arxiv; the harness provides
# speaker_self_publish_evidence_log.json with per-speaker evidence
# (arxiv IDs + key topics).  This module checks whether the atom's
# verbatim_quote literally matches the speaker's self-published topic.

SPEAKER_KNOWN_SELF_PUBLISH = {
    "yu_sun": {
        "arxiv": ["2407.04620", "2512.23675", "2505.23884"],
        "topic_keywords": [
            "test-time training", "ttt", "test time training",
            "gradient descent at test time",
            "do gradient descent on the model at test time",
            "change the model ways at test time",
            "model ways at test time",
            "hidden state machine learning model",
            "rnn expressive hidden state",
        ],
        "paper_titles": [
            "Learning to (Learn at Test Time): RNNs with Expressive Hidden States",
            "End-to-End Test-Time Training for Long Context",
        ],
    },
    "hinton": {
        "arxiv": ["2212.13345"],
        "topic_keywords": [
            "forward-forward", "forward forward", "ff algorithm",
            "ford algorithm",  # transcription error for forward-forward
            "negative phase", "positive phase", "sleep wake learning",
            "goodness function", "sum of squared activities",
            "language is a modelling medium",
            "language is a modeling medium",
            "words which are bricks from which you can build models",
            "language is a wonderful way to build a particular complicated model",
            "relational knowledge is just in how you turn the word into features",
            "all the relational knowledge",
            "real function of language is to give you words",
            "perceptual sensations",
            "cohesive internal logic",
            "good enough model of what one urine is",  # "one neuron is" mis-transcription
            "doesn't need to have a perfect model of the forward system",
        ],
        "paper_titles": [
            "The Forward-Forward Algorithm (arXiv:2212.13345)",
            "Hinton 'Language as Modeling Medium' (T010 talk position)",
        ],
    },
    "karpathy": {
        "arxiv": [],
        "topic_keywords": [
            "software 2.0", "software 2 point 0", "neural net classifier different",
            "assistant model next word prediction", "huggingface software 2.0",
        ],
        "paper_titles": [
            "Software 2.0 (Karpathy Medium 2017)",
            "Intro to Large Language Models (Karpathy)",
        ],
    },
    "belinda_li": {
        "arxiv": ["2511.08579"],
        "topic_keywords": [
            "world user self model", "self model for llm",
            "unifying framework for llm failures",
            "self-consistency and privileged access",
            "self-explainer beats another model as explainer",
            "generated description matches the ground truth description",
            "trained to explain themselves",
            "world user and self models remains a unifying framework",
            "world user and self model", "world, user, and self model",
            "structured world user and self models",
            "lens of structured world user",
            "language model failures in terms of these structured models",
            "language model failures in terms of structured models",
            "failures of modern ai systems can be understood",
            "broader challenges remain open problems",
            "user model section",
            "augmented with explicit user models",
            "language models augmented with explicit user models",
            "make updatability realized just in general",
            "updatability realized just in general",
            "extract world models from our ai systems",
            "extract scientific knowledge from systems trained on large scale",
            "if we can extract world models",
            "building a mini world model inside",
            "mini world model inside of its inside",
            "transformer which looks something like",
        ],
        "paper_titles": [
            "Self-Models for LLMs (Belinda Li T001)",
            "Training Language Models to Explain Their Own Computations (arXiv:2511.08579)",
        ],
    },
    "nicholas_roberts": {
        "arxiv": ["2503.10061", "2412.06540", "2604.01411"],
        "topic_keywords": [
            "compute optimal scaling of skills",
            "knowledge vs reasoning scaling",
            "sloth scaling law",
            "skills scaling laws",
            "skill-dependent scaling",
            "skills and scaling laws",
            "scaling law math or understanding",
            "scaling law or math or understanding of how this universe of these parameters",
            "scientific research agents",
            "data efficient foundation model pipelines",
            "applying these agents to unsolved math problems",
            "two very basic primitives",
            "skills in particular, this is just data",
            "next frontier beyond these is to take these agents",
            "diverse scientific tasks",
            "agents to unsolved math problems",
            "build up these flux agent models",
            "flux agent models", "flex agent models",
            "first component of how we're going to build",
            "data efficient foundation model",
            "we've been training our models suboptimally",
            "training our models suboptimally",
            "building up to this work",
            "scientific data for these other agents",
            "run out of human text data in general",
            "going to run out of human text data",
            "training free adaptation via using external knowledge",
            "knowledge graphs to understand the relationships",
            "make flex agent",
            "conceptual primitive is going to be useful for training",
            "developing physical descriptions of the universe",
        ],
        "paper_titles": [
            "Compute Optimal Scaling of Skills (arXiv:2503.10061)",
            "Sloth: Scaling Laws for LLM Skills (arXiv:2412.06540)",
            "Test-Time Scaling Makes Overtraining Compute-Optimal (arXiv:2604.01411)",
        ],
    },
    "amrith_setlur": {
        "arxiv": ["2410.08146", "2601.14209", "2603.08754"],
        "topic_keywords": [
            "rewarding progress process verifier",
            "process reward model prm",
            "advantages of a complementary llm",
            "advantage of a complementary llm mu",
            "right notion of reward for a trace",
            "sampler is one of exploration on hard problems",
            "online traces you generate for this particular problem",
            "terminal reward of zero",
            "intervention training credit assignment",
            "hindsight credit assignment",
            "qed nano", "qednano", "four-b-size",
            "small four-b-size pre-train model",
            "algorithm learning techniques",
            "advantages of a complementary",
            "complementary llm mu",
            "complementary llm",
            "if the model has a prior to produce a proof",
        ],
        "paper_titles": [
            "Rewarding Progress (arXiv:2410.08146)",
            "InT: Self-Proposed Interventions (arXiv:2601.14209)",
            "Hindsight Credit Assignment (arXiv:2603.08754)",
        ],
    },
    "lecun": {
        "arxiv": ["2306.02507"],
        "topic_keywords": [
            "jepa", "joint embedding predictive", "self-supervised",
            "average or aggregate of all the possible futures",
            "predict some average or aggregate",
            "predict in representation space",
            "world model is a predictor",
            "joint embedding predictive architecture",
            "now we're going to be able to handle with those role models",
            "generic ways of training them",
            "train a generative model to predict what's going to happen next",
            "generative model to predict what's going to happen next",
            "the same idea as llms, which is to train a generative model",
        ],
        "paper_titles": ["JEPA: Joint-Embedding Predictive Architecture (LeCun)"],
    },
}


def is_speaker_self_publish(atom: dict) -> Tuple[bool, str]:
    sp = speaker_of(atom.get("transcript_id", ""))
    spk = SPEAKER_KNOWN_SELF_PUBLISH.get(sp)
    if not spk:
        return False, ""
    quote_low = atom.get("verbatim_quote", "").lower()
    for kw in spk["topic_keywords"]:
        if kw.lower() in quote_low:
            return True, f"speaker={sp} matches keyword '{kw}' from own paper(s) {spk['arxiv'] or spk['paper_titles']}"
    return False, ""


# ---------- Layer 8: recursive_failure_diagnostic ----------

@dataclass
class FailureRecord:
    candidate_id: str
    layer_failed: str
    reason_code: str
    detail: str


def cluster_failures(records: List[FailureRecord]) -> Dict[str, List[str]]:
    """Group failure reasons into root cause categories."""
    by_root: Dict[str, List[str]] = {
        "SPEAKER_SELF_PUBLISH": [],
        "SINGLE_SPEAKER_COLLISION": [],
        "ATOM_TYPE_REGEX_MISFIRE": [],
        "TRUNCATED_OR_VAGUE_ATOM": [],
        "MECHANISM_INCOHERENT_PAIRING": [],
        "COMMUNITY_SATURATED": [],
        "OTHER": [],
    }
    for r in records:
        rc = r.reason_code
        if "SELF_PUBLISH" in rc:
            by_root["SPEAKER_SELF_PUBLISH"].append(r.candidate_id)
        elif "SINGLE_SPEAKER" in rc:
            by_root["SINGLE_SPEAKER_COLLISION"].append(r.candidate_id)
        elif "PAST_TENSE" in rc or "META_COMMENT" in rc:
            by_root["ATOM_TYPE_REGEX_MISFIRE"].append(r.candidate_id)
        elif "TRUNCATED" in rc or "TOO_SHORT" in rc:
            by_root["TRUNCATED_OR_VAGUE_ATOM"].append(r.candidate_id)
        elif "MECHANISM" in rc or "INCOHERENT" in rc:
            by_root["MECHANISM_INCOHERENT_PAIRING"].append(r.candidate_id)
        elif "SATURATED" in rc:
            by_root["COMMUNITY_SATURATED"].append(r.candidate_id)
        else:
            by_root["OTHER"].append(r.candidate_id)
    return by_root


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
