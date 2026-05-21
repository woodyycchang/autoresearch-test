"""Atom extractor for TARI v1.

For each snippet, extract atoms of 5 types:
  - PRIMITIVE       (named mechanism the speaker invokes)
  - MECHANISM_CLAIM (causal/structural claim)
  - NEGATIVE_RESULT (thing that failed or was ruled out)
  - METRIC          (a measurement reported)
  - OPEN_QUESTION   (a thing the speaker said is unsolved)

This step is heuristic/regex-based (no LLM call). It is intentionally conservative:
better to miss an atom than to fabricate one. Atoms that the heuristic produces are
*candidates* — the brainstorm engine will gloss them more carefully if it uses them.

CRITICAL DESIGN DECISION: every atom carries a verbatim_quote field copied literally
from the snippet's verbatim_text. The audit step later checks that this quote
appears verbatim in the transcript. This is the primary anti-fabrication mechanism.

Honest deviation: this is regex-based, not LLM-based, so the atoms are precision-
biased (high precision, recall is whatever the regexes catch). The trade-off is
deliberate: hallucinated atoms break the audit chain.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

# ---- Heuristic patterns ----

# PRIMITIVE: curated list of named technical concepts.
# We deliberately do NOT use a generic CamelCase regex because it matches sentence-initial
# capitalization (e.g. "Welcome to" was a false positive in pilot extraction).
PRIMITIVE_PATTERNS = [
    re.compile(r"\b(activation\s+patching|interchange\s+intervention|probing|test[-\s]*time\s+training|self[-\s]?model|world\s+model|user\s+model|associative\s+(?:scan|algorithm)|sequential\s+algorithm|parallel\s+algorithm|in[-\s]*context\s+search|Bayesian\s+model|particle\s+filter|posterior\s+inference|information\s+gain|reward[-\s]to[-\s]?go|chinchilla(?:\s+scaling)?|sliding\s+window|self[-\s]?attention|attention\s+diagram|transformer|gradient\s+descent|long\s+context|continual\s+learning|self[-\s]?supervised(?:\s+learning)?|input\s+ablations?|description\s+generation|active\s+task\s+elicitation|generative\s+active\s+task\s+elicitation|chatbot\s+arena|copilot\s+arena|performance\s+profiles?|policy\s+iteration|surrogate\s+(?:reward|sampler)|terminal\s+reward|advantage|meta[-\s]?RL|meta[-\s]?reinforcement\s+learning|meta\s+learning|test[-\s]?time\s+adapt(?:ation)?|inference[-\s]time\s+scaling|pass[-\s]?at[-\s]?k|skill\s+graph|skillet|weak\s+supervision|prediction[-\s]powered\s+inference|scaling\s+law|t[-\s]?squared\s+scaling|self[-\s]?explanation|self[-\s]?consistency|privileged\s+access|faithful\s+explanation|sycophancy|external\s+collision|POMDP|partially\s+observed\s+markov\s+decision\s+process|state\s+tracking|hidden\s+representation|auxiliary\s+data|offline\s+data|on[-\s]?policy|off[-\s]?policy|entropic\s+utility|reasoning\s+model|counterfactual|coherence|updatability|KV\s+cache|key\s+value\s+cache|Brown[-\s]measure|R[-\s]transform|S[-\s]transform|free[-\s]probability|Hochschild|cochain|Bayesian\s+linear\s+model|featurization|hallucinations?|self[-\s]?prediction|coherence\s+audit|frontier\s+model|nearest\s+neighbor|knowledge\s+graph|fine[-\s]tun(?:ing|e)|pre[-\s]train(?:ing|ed)|kernel\s+engineering|exploration|exploitation|verifier|verification|self[-\s]?simulation|self[-\s]?evolving|GATE|OPEN|RNN|state\s+space\s+model)\b", re.IGNORECASE),
]

# MECHANISM_CLAIM: contains a causal verb between a subject and a mechanism
MECHANISM_CLAIM_PATTERNS = [
    re.compile(r"\b(?:we|they|the (?:model|LLM|language model|system|pipeline|agent|algorithm|method))\s+(?:can|learn(?:s|ed)?|build(?:s|ed|ing)?|use(?:s|d)?|produce(?:s|d)?|generate(?:s|d)?|track(?:s|ed)?|update(?:s|d)?|infer(?:s|red)?|predict(?:s|ed)?|implement(?:s|ed)?|adapt(?:s|ed)?|improve(?:s|d)?|scale(?:s|d)?)\s+[^.!?]{15,200}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:this|that)\s+(?:means|shows|implies|suggests|indicates|allows|enables)\s+[^.!?]{15,200}[.!?]", re.IGNORECASE),
]

# NEGATIVE_RESULT: explicit failures, "doesn't work", "fails", "did not"
NEGATIVE_RESULT_PATTERNS = [
    re.compile(r"\b(?:does(?:n't| not)|cannot|can't|fail(?:s|ed)?|failed to|won't|will not|not enough|insufficient|but (?:this|that) (?:doesn't|does not)|but the (?:problem|issue|catch)|but it is also (?:quite\s+)?brittle|but really|but in practice)\s+[^.!?]{10,180}[.!?]", re.IGNORECASE),
    re.compile(r"\b(?:limitations?|bottlenecks?|deficits?|gaps?|missing|absent)\s+[^.!?]{10,180}[.!?]", re.IGNORECASE),
]

# METRIC: numerical quantities with units / percentages
METRIC_PATTERNS = [
    re.compile(r"\b\d+(?:\.\d+)?\s*(?:percent|%|x|×|times|tokens?|parameters?|epochs?|rounds?|samples?|layers?)\b", re.IGNORECASE),
    re.compile(r"\b\d+(?:[.,]\d{3})*(?:\.\d+)?\s*(?:B|M|K|thousand|million|billion|trillion)\s*(?:parameters?|tokens?|samples?)?\b", re.IGNORECASE),
]

# OPEN_QUESTION: explicit unsolved / open / future
OPEN_QUESTION_PATTERNS = [
    re.compile(r"\b(?:open\s+(?:problem|question|conjecture)|unsolved|remain(?:s|ing)?\s+(?:open|unclear|unsolved)|future\s+work|further\s+work|next\s+question|how\s+(?:do|can|should)\s+we|why\s+does|what\s+(?:is|are)\s+the\s+(?:right|optimal|best))\s+[^.!?]{5,160}[.!?]", re.IGNORECASE),
]


@dataclass
class Atom:
    atom_id: str
    atom_type: str
    snippet_id: str
    transcript_id: str
    line_span: tuple  # (start_line, end_line) of the SNIPPET, not the verbatim quote
    verbatim_quote: str
    gloss: str
    extraction_pattern: str


def find_quotes(snippet_text: str, patterns: List[re.Pattern]) -> List[str]:
    """Return list of UNIQUE verbatim matches from snippet_text using given patterns."""
    found = []
    seen = set()
    for pat in patterns:
        for m in pat.finditer(snippet_text):
            # Capture the full sentence containing the match, bounded by sentence ends.
            start = m.start()
            end = m.end()
            # Walk back to start of sentence
            for i in range(start - 1, -1, -1):
                if snippet_text[i] in ".!?\n":
                    start = i + 1
                    break
            else:
                start = 0
            # Walk forward to end of sentence
            for i in range(end, len(snippet_text)):
                if snippet_text[i] in ".!?":
                    end = i + 1
                    break
            else:
                end = len(snippet_text)
            quote = snippet_text[start:end].strip()
            if 20 <= len(quote) <= 350 and quote not in seen:
                seen.add(quote)
                found.append(quote)
    return found


def gloss_atom(atom_type: str, quote: str) -> str:
    """Produce a brief 1-sentence gloss of the atom (extractive, no LLM call)."""
    # For v1, the gloss is a truncated, type-prefixed version of the verbatim quote.
    # This is deliberate — a "gloss" that paraphrases would risk fabrication.
    s = quote.replace("\n", " ").strip()
    if len(s) > 180:
        s = s[:177] + "..."
    return f"[{atom_type}] {s}"


def extract_atoms_for_snippet(snippet_path: Path, snippet_index: int) -> List[Atom]:
    with snippet_path.open("r", encoding="utf-8") as f:
        snippet = json.load(f)

    text = snippet["verbatim_text"]
    sid = snippet["snippet_id"]
    tid = snippet.get("transcript_id", "T001")
    line_span = (snippet["start_line"], snippet["end_line"])

    atoms: List[Atom] = []
    counter = 0

    for atom_type, patterns in [
        ("PRIMITIVE", PRIMITIVE_PATTERNS),
        ("MECHANISM_CLAIM", MECHANISM_CLAIM_PATTERNS),
        ("NEGATIVE_RESULT", NEGATIVE_RESULT_PATTERNS),
        ("METRIC", METRIC_PATTERNS),
        ("OPEN_QUESTION", OPEN_QUESTION_PATTERNS),
    ]:
        quotes = find_quotes(text, patterns)
        for q in quotes[:4]:
            counter += 1
            # atom_id format: ATOM_{transcript_id}_{snippet_id}_{NN}
            # Examples: ATOM_T001_S004_01 (v2), ATOM_S004_01 (v1 - no transcript prefix)
            if tid and tid != "T001_LEGACY":
                atom_id = f"ATOM_{tid}_{sid}_{counter:02d}"
            else:
                atom_id = f"ATOM_{sid}_{counter:02d}"
            atoms.append(Atom(
                atom_id=atom_id,
                atom_type=atom_type,
                snippet_id=sid,
                transcript_id=tid,
                line_span=line_span,
                verbatim_quote=q,
                gloss=gloss_atom(atom_type, q),
                extraction_pattern=f"{atom_type}_regex",
            ))

    return atoms


def extract_all(snippets_dir: Path, out_dir: Path, append: bool = False) -> List[Atom]:
    """Extract atoms from all snippets in snippets_dir, write to out_dir.

    If append=True, do not overwrite the index — instead merge with any existing
    atoms in out_dir. This supports multi-transcript runs that consolidate atoms
    from multiple transcripts into a single shared atoms_dir.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    snippet_files = sorted(snippets_dir.glob("snippet_S*.json"))
    all_atoms: List[Atom] = []
    for i, sp in enumerate(snippet_files):
        atoms = extract_atoms_for_snippet(sp, i)
        all_atoms.extend(atoms)

    for atom in all_atoms:
        with (out_dir / f"{atom.atom_id}.json").open("w", encoding="utf-8") as f:
            json.dump(asdict(atom), f, indent=2, ensure_ascii=False)

    # Index: rebuild from all atom files in out_dir (covers append case)
    all_files = sorted(out_dir.glob("ATOM_*.json"))
    by_type = {}
    by_transcript = {}
    all_ids = []
    for af in all_files:
        with af.open("r", encoding="utf-8") as f:
            d = json.load(f)
        all_ids.append(d["atom_id"])
        by_type[d["atom_type"]] = by_type.get(d["atom_type"], 0) + 1
        tid = d.get("transcript_id", "T001")
        by_transcript[tid] = by_transcript.get(tid, 0) + 1

    index = {
        "n_atoms": len(all_files),
        "atom_ids": all_ids,
        "type_distribution": by_type,
        "transcript_distribution": by_transcript,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }
    with (out_dir / "_index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    return all_atoms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snippets_dir", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    args = ap.parse_args()
    atoms = extract_all(args.snippets_dir, args.out_dir)
    print(f"extracted {len(atoms)} atoms")
    types = {}
    for a in atoms:
        types[a.atom_type] = types.get(a.atom_type, 0) + 1
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t:18s} {c}")


if __name__ == "__main__":
    main()
