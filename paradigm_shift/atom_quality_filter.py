"""Atom quality filter for Paradigm-Shift Finder.

Rejects atoms that match negative features (talk meta-language, pure
analogy without mechanism, surface-noun open-problems, adjective-only
predictions, definitional blockers). Accepts atoms that have >=1 positive
feature (architectural primitive, specific algorithm name, empirical
claim with number, mechanism claim, time-specific prediction).

Decision rule:
    atom passes iff (positive_features >= 1) AND (negative_features == 0)

See design/atom_quality_diagnosis.md for the 5 failure modes and the
rationale for each rule.

The filter is precision-biased — it will reject borderline atoms that
might have contributed to an interesting candidate. The trade is fewer
candidates with higher signal per candidate.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---- Positive feature vocab ----

# F+1: Architectural / ML primitive vocabulary
PRIMITIVE_VOCAB = {
    "transformer", "attention", "self-attention", "convolution", "rnn",
    "lstm", "gru", "mamba", "ssm", "state-space", "ttt", "test-time-training",
    "diffusion", "vae", "gan", "encoder", "decoder", "embedding",
    "tokenizer", "softmax", "layer-norm", "batch-norm", "dropout",
    "residual", "skip-connection", "gradient-descent", "adam", "sgd",
    "rlhf", "ppo", "dpo", "rl", "reinforcement", "world-model",
    "self-model", "user-model", "self-attention", "cross-attention",
    "kv-cache", "long-context", "context-window", "probing",
    "interpretability", "mechanistic", "scaling-law", "compute-optimal",
    "chinchilla", "moe", "mixture-of-experts", "jepa", "energy-based",
    "self-supervised", "contrastive", "masked-language", "next-token",
    "chain-of-thought", "cot", "search", "mcts", "beam-search",
    "verifier", "reward-model", "outcome-reward", "process-reward",
    "in-context-learning", "few-shot", "zero-shot",
    "knowledge-graph", "retrieval", "rag",
    "neural-network", "deep-learning", "foundation-model",
}

# F+2: Specific algorithm / method name patterns
ALGORITHM_NAME_PATTERNS = [
    re.compile(r"\b[A-Z][a-zA-Z]+(?:-[A-Z][a-zA-Z]+)+\b"),  # Gated-Delta-Net
    re.compile(r"\b[A-Z]{2,}(?:-?\d+)?\b"),  # GPT, LSTM, GPT-4
    re.compile(r"\b[A-Z][a-z]+[A-Z][a-zA-Z]+\b"),  # CamelCase ChainOfThought
]

# Common false-positive names to exclude from algorithm-name detection
ALGORITHM_NAME_BLOCKLIST = {
    "I", "AI", "ML", "LLM", "LLMs", "AGI", "ASI", "HCI", "CV", "NLP",
    "OK", "TLDR", "DSL", "GUI", "CPU", "GPU", "RAM", "URL", "USA", "UK",
    "OS", "IP", "API", "JSON", "HTML", "CSS", "SQL", "PDF", "PhD", "MS",
}

# F+3: empirical claim with number + unit
NUMBER_UNIT_PATTERNS = [
    re.compile(r"\b\d+(?:\.\d+)?\s*(?:percent|%|x|×|fold|times|tokens|parameters|epochs|samples|layers|heads|dimensions|bits|flops|petabytes|terabytes|gigabytes)\b", re.IGNORECASE),
    re.compile(r"\b\d+(?:[.,]\d{3})*\s*(?:B|M|K|thousand|million|billion|trillion)\b"),
    re.compile(r"\b(?:10\^|10\*\*)\d+\b"),
    re.compile(r"\b\d+(?:\.\d+)?\s*(?:bps|tps|qps|fps|hz|ghz|mhz)\b", re.IGNORECASE),
]

# F+4: mechanism claim — causal verb between named subject and named object
MECHANISM_PATTERNS = [
    re.compile(r"\b(?:enables?|allows?|forces?|causes?|drives?|produces?|generates?|implements?|achieves?)\s+\w+", re.IGNORECASE),
    re.compile(r"\b(?:by|via|through|using)\s+\w+\s+(?:we|the\s+model|the\s+system)\s+(?:can|do|achieve|build|train|infer)", re.IGNORECASE),
    re.compile(r"\b(?:because|since)\s+\w+\s+\w+", re.IGNORECASE),
    re.compile(r"\b(?:if|when)\s+\w+\s+\w+\s+(?:then|,)\s+\w+", re.IGNORECASE),
]

# F+5: time-specific prediction
TIME_SPECIFIC_PATTERNS = [
    re.compile(r"\bby\s+20\d{2}\b", re.IGNORECASE),
    re.compile(r"\b(?:in|within)\s+\d+\s+(?:years?|months?|decades?)\b", re.IGNORECASE),
    re.compile(r"\bnext\s+(?:year|decade|generation|wave|era)\b", re.IGNORECASE),
    re.compile(r"\bwithin\s+(?:a|the)\s+(?:year|decade)\b", re.IGNORECASE),
]


# ---- Negative feature regex ----

# F-1: Talk meta-language in first 100 chars
TALK_META_PATTERNS = [
    re.compile(r"^[^.!?]{0,100}\b(?:in this talk|i'?m going to talk|i'?ll talk|let me explain|in this section|in the first section|in the second section|in the third section|first let me|i'?ll cover|today i'?ll|i'?m\s+going to be motivating|let me show|i'?ll show|let'?s take a look|next\s+the|let me go on|let me pick|let me illustrate|i'?m going to walk through)\b", re.IGNORECASE),
]

# F-2: Pure analogy without transferable structure
# An analogy must contain at least one of: structural mapping language, two named domains, or a "X is Y of Z" pattern
ANALOGY_STRUCTURE_PATTERNS = [
    re.compile(r"\b(?:like\s+\w+\s+but\s+for\s+\w+|is\s+the\s+\w+\s+of\s+\w+|preserves|isomorphism|corresponds\s+to|maps\s+to|analogous\s+to|structurally|in\s+the\s+same\s+way\s+that)\b", re.IGNORECASE),
    re.compile(r"\b[A-Z][a-z]+(?:\s+[a-z]+){0,3}\s+(?:is\s+like|is\s+similar\s+to|works\s+like)\s+[A-Z][a-z]+", re.IGNORECASE),
]

# F-3: Specific-problem-name patterns (used for open_problem and blocker types)
SPECIFIC_PROBLEM_PATTERNS = [
    # Named technical capability that doesn't exist yet
    re.compile(r"\b(?:long\s+context|test[-\s]time\s+training|continual\s+learning|world\s+model|interpretability|alignment|hallucination|reasoning|planning|memory|retrieval|composition|generalization|sample\s+efficiency|out[-\s]of[-\s]distribution|distribution\s+shift|catastrophic\s+forgetting|spurious\s+correlation|robustness|adversarial|scaling)\b", re.IGNORECASE),
    re.compile(r"\b(?:bottleneck|barrier|obstacle)\s+(?:is|of|in)\s+\w+\s+\w+", re.IGNORECASE),
]

# F-4: prediction with only adjectives (no year/tech/number/causal verb)
# Detected as: prediction does NOT match any F+3, F+4, F+5 patterns
ADJECTIVE_FUTURE_RE = re.compile(
    r"\b(?:more|less|better|worse|safer|reliable|adaptive|transparent|collaborative|robust|scalable|efficient|fast|cheap|good|bad|great|wonderful|amazing)\b",
    re.IGNORECASE,
)

# F-5: Definitional blocker — common methodological-clarification phrasing
DEFINITIONAL_BLOCKER_PATTERNS = [
    re.compile(r"\bwe\s+(?:don'?t|do\s+not|can'?t|cannot)\s+(?:measure|evaluate|observe|see|track|access)\s+(?:the\s+)?intermediate", re.IGNORECASE),
    re.compile(r"\bwe\s+(?:can\s+only|just)\s+(?:measure|evaluate|observe)\s+(?:the\s+)?(?:final|outcome|output)", re.IGNORECASE),
    re.compile(r"\bin\s+many\s+cases.{0,40}\bwe\s+(?:can'?t|cannot)\s+(?:evaluate|measure|observe)", re.IGNORECASE),
]


# ---- Feature detectors ----

def has_primitive_vocab(text: str) -> bool:
    text_norm = re.sub(r"\s+", "-", text.lower())
    for v in PRIMITIVE_VOCAB:
        if v in text.lower() or v in text_norm:
            return True
    return False


def has_algorithm_name(text: str) -> bool:
    for pat in ALGORITHM_NAME_PATTERNS:
        for m in pat.finditer(text):
            name = m.group(0)
            if name in ALGORITHM_NAME_BLOCKLIST:
                continue
            # Reject 1-character matches and overly-short matches
            if len(name) <= 2:
                continue
            return True
    return False


def has_number_with_unit(text: str) -> bool:
    return any(pat.search(text) for pat in NUMBER_UNIT_PATTERNS)


def has_mechanism_claim(text: str) -> bool:
    return any(pat.search(text) for pat in MECHANISM_PATTERNS)


def has_time_specific(text: str) -> bool:
    return any(pat.search(text) for pat in TIME_SPECIFIC_PATTERNS)


def has_talk_meta(text: str) -> bool:
    head = text[:200]  # broaden a bit beyond 100
    return any(pat.search(head) for pat in TALK_META_PATTERNS)


def has_analogy_structure(text: str) -> bool:
    return any(pat.search(text) for pat in ANALOGY_STRUCTURE_PATTERNS)


def has_specific_problem(text: str) -> bool:
    return any(pat.search(text) for pat in SPECIFIC_PROBLEM_PATTERNS)


def has_definitional_blocker(text: str) -> bool:
    return any(pat.search(text) for pat in DEFINITIONAL_BLOCKER_PATTERNS)


# ---- Per-atom decision ----

@dataclass
class FilterResult:
    atom_id: str
    passed: bool
    positive_features: List[str]
    negative_features: List[str]
    reason: str


def evaluate_atom(atom: dict) -> FilterResult:
    """Run the filter on a single atom dict."""
    aid = atom["atom_id"]
    quote = atom.get("verbatim_quote", "")
    ptype = atom.get("paradigm_type", "")

    pos: List[str] = []
    neg: List[str] = []

    # Positive features
    if has_primitive_vocab(quote):
        pos.append("F+1_primitive_vocab")
    if has_algorithm_name(quote):
        pos.append("F+2_algorithm_name")
    if has_number_with_unit(quote):
        pos.append("F+3_number_unit")
    if has_mechanism_claim(quote):
        pos.append("F+4_mechanism_claim")
    if has_time_specific(quote):
        pos.append("F+5_time_specific")

    # Negative features
    if has_talk_meta(quote):
        neg.append("F-1_talk_meta")

    if ptype == "analogy":
        if not has_analogy_structure(quote):
            neg.append("F-2_pure_analogy_no_mechanism")

    if ptype in ("open_problem", "blocker"):
        if not has_specific_problem(quote):
            neg.append("F-3_surface_noun_no_specifics")

    if ptype == "prediction":
        # F-4: prediction with adjectives but no year/tech/number/causal verb
        has_adj = bool(ADJECTIVE_FUTURE_RE.search(quote))
        signal = (has_time_specific(quote) or has_number_with_unit(quote)
                  or has_mechanism_claim(quote)
                  or has_primitive_vocab(quote)
                  or has_algorithm_name(quote))
        if has_adj and not signal:
            neg.append("F-4_adjective_only_prediction")

    if ptype == "blocker" and has_definitional_blocker(quote):
        neg.append("F-5_definitional_blocker")

    passed = (len(pos) >= 1 and len(neg) == 0)
    if passed:
        reason = "pass: " + ",".join(pos)
    else:
        reason_parts = []
        if not pos:
            reason_parts.append("no_positive_features")
        if neg:
            reason_parts.append("negatives=" + ",".join(neg))
        reason = "reject: " + " | ".join(reason_parts)

    return FilterResult(
        atom_id=aid, passed=passed,
        positive_features=pos, negative_features=neg,
        reason=reason,
    )


# ---- Directory-level filter ----

def filter_atoms_dir(
    atoms_dir: Path,
    out_dir: Path,
    report_path: Optional[Path] = None,
) -> Tuple[int, int, List[FilterResult]]:
    """Run the filter on every ATOM_*.json in atoms_dir; copy passing atoms
    to out_dir; write a per-atom report.

    Returns (n_pass, n_reject, all_results).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    results: List[FilterResult] = []
    n_pass = 0
    n_reject = 0
    pass_by_type: Dict[str, int] = {}
    reject_by_neg: Dict[str, int] = {}

    for ap in sorted(atoms_dir.glob("ATOM_*.json")):
        with ap.open("r", encoding="utf-8") as f:
            atom = json.load(f)
        res = evaluate_atom(atom)
        results.append(res)
        if res.passed:
            n_pass += 1
            pass_by_type[atom["paradigm_type"]] = pass_by_type.get(atom["paradigm_type"], 0) + 1
            # Copy to out_dir
            shutil.copy(ap, out_dir / ap.name)
        else:
            n_reject += 1
            for n in res.negative_features:
                reject_by_neg[n] = reject_by_neg.get(n, 0) + 1
            if not res.positive_features:
                reject_by_neg["no_positive_features"] = reject_by_neg.get("no_positive_features", 0) + 1

    # Build a fresh _index.json with paradigm_type_distribution recomputed
    by_type: Dict[str, int] = {}
    by_transcript: Dict[str, int] = {}
    ids: List[str] = []
    for ap in sorted(out_dir.glob("ATOM_*.json")):
        with ap.open("r", encoding="utf-8") as f:
            d = json.load(f)
        ids.append(d["atom_id"])
        by_type[d["paradigm_type"]] = by_type.get(d["paradigm_type"], 0) + 1
        tid = d.get("transcript_id", "?")
        by_transcript[tid] = by_transcript.get(tid, 0) + 1

    index = {
        "n_atoms": len(ids),
        "atom_ids": ids,
        "paradigm_type_distribution": by_type,
        "transcript_distribution": by_transcript,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "filter_applied": True,
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with report_path.open("w", encoding="utf-8") as f:
            json.dump({
                "filtered_at": datetime.now(timezone.utc).isoformat(),
                "atoms_dir": str(atoms_dir),
                "n_input": n_pass + n_reject,
                "n_pass": n_pass,
                "n_reject": n_reject,
                "pass_by_paradigm_type": pass_by_type,
                "reject_by_negative_feature": reject_by_neg,
                "per_atom": [asdict(r) for r in results],
            }, f, indent=2)

    return n_pass, n_reject, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atoms_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--report_path", type=Path, default=None)
    args = ap.parse_args()
    n_pass, n_reject, results = filter_atoms_dir(args.atoms_dir, args.out_dir, args.report_path)
    print(f"filter results: pass={n_pass}  reject={n_reject}  total={n_pass+n_reject}")
    # Summary
    by_type: Dict[str, int] = {}
    for ap in sorted(args.out_dir.glob("ATOM_*.json")):
        with ap.open("r") as f:
            d = json.load(f)
        by_type[d["paradigm_type"]] = by_type.get(d["paradigm_type"], 0) + 1
    for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t:18s} {n}")


if __name__ == "__main__":
    main()
