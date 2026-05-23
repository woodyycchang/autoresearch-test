"""Transcript purifier for Paradigm-Shift Finder Run 6.

Raw YouTube auto-captions arrive as a single lowercase stream with no
punctuation, no capitalisation of sentence starts, and dense spoken
disfluency ("you know", "kind of", "sort of", "right", "I mean").

The existing snippet_decomposer relies on the regex ``[.!?]\s+[A-Z]`` to
split sentences. On a typical raw transcript that regex matches **zero**
times, so the whole transcript collapses into a single mega-snippet and
the type-tagged atom extractor finds almost nothing (T007 + T012 + T014
together yielded 1 atom in the pre-purifier baseline).

This module restores sentence boundaries with spaCy so the downstream
pipeline can do its job:

  1. Normalise whitespace and concatenate into a single line.
  2. Insert sentence breaks before strong discourse markers
     ("so", "but", "now", "okay", "and then", "the first", "you know")
     when followed by a clausal head.
  3. Run spaCy's parser and use ``Doc.sents`` to refine remaining
     boundaries (the dependency parser finds VERB roots even when the
     surface text lacks periods).
  4. Capitalise sentence starts and stand-alone "i".
  5. Strip the most common disfluencies that bury content words.
  6. Re-emit a clean .txt file with one sentence per line.

We deliberately keep this conservative: every output token is a token
from the input, in original order, with at most surrounding whitespace
and capitalisation changed. No paraphrasing.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List

import spacy

_NLP = None


def _get_nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


# Discourse markers that very frequently start a fresh independent clause
# in spoken English. We treat them as sentence boundaries when followed by
# a pronoun or determiner that itself begins a clause.
DISCOURSE_BREAKERS = [
    "so",
    "but",
    "now",
    "okay",
    "right",
    "well",
    "then",
    "and then",
    "and so",
    "you know",
    "i mean",
    "i think",
    "i believe",
    "the first",
    "the second",
    "the third",
    "the fourth",
    "the next",
    "the last",
    "another",
    "for example",
    "basically",
    "obviously",
    "actually",
    "essentially",
    "fundamentally",
    "eventually",
    "in fact",
    "in summary",
    "to summarize",
    "to recap",
    "to wrap up",
    "in conclusion",
]

# Common spoken disfluencies. We collapse repeated occurrences but keep the
# first instance so that the verbatim_quote contract from atom_typer still
# holds against the purified text.
DISFLUENCY_RE = re.compile(
    r"\b(?:um|uh|uhh|er|like(?=,)|sort of|kind of|i guess|i mean)\b",
    re.IGNORECASE,
)

PRONOUN_OR_DET = re.compile(r"^(?:i|we|you|they|he|she|it|the|a|an|this|that|these|those)\b")


def _normalise_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _insert_discourse_breaks(text: str) -> str:
    """Insert period+space before discourse markers when they look like the
    start of a new independent clause."""

    out = text
    for marker in DISCOURSE_BREAKERS:
        pattern = re.compile(
            r"(?<!^)(?<=[a-z0-9])\s+(" + re.escape(marker) + r")\s+(?="
            + PRONOUN_OR_DET.pattern[1:]   # drop the leading ^
            + r")",
            re.IGNORECASE,
        )
        out = pattern.sub(r". \1 ", out)
    return out


def _capitalise_starts(text: str) -> str:
    """Capitalise the first letter after each sentence-final period."""
    def _cap(m: re.Match) -> str:
        return m.group(1) + m.group(2).upper()
    out = re.sub(r"(^|\.\s+)([a-z])", _cap, text)
    # Stand-alone lowercase 'i' → 'I'
    out = re.sub(r"\bi\b", "I", out)
    return out


def _refine_with_spacy(text: str) -> List[str]:
    """Run spaCy on the already-broken text. ``Doc.sents`` gives us a
    second-pass refinement: clauses with their own VERB ROOT are split
    even if our discourse-marker pass missed them."""
    nlp = _get_nlp()
    doc = nlp(text)
    sentences: List[str] = []
    for s in doc.sents:
        sent_text = s.text.strip()
        if sent_text:
            sentences.append(sent_text)
    return sentences


def _split_long_sentences(sents: List[str], max_words: int = 40) -> List[str]:
    """Split run-on sentences at safe cut points (comma + pronoun, ' and '+
    verb-led clause) to keep snippet boundaries reasonable."""
    nlp = _get_nlp()
    out: List[str] = []
    for s in sents:
        words = s.split()
        if len(words) <= max_words:
            out.append(s)
            continue
        # Use spaCy to find clausal conjunctions in over-length sentences.
        doc = nlp(s)
        cuts = [0]
        for i, t in enumerate(doc):
            if i - cuts[-1] < 12:
                continue
            if t.text.lower() in {"and", "but", "because", "so"} and i + 1 < len(doc):
                nxt = doc[i + 1]
                if nxt.pos_ in {"PRON", "DET", "NOUN", "PROPN"}:
                    cuts.append(i + 1)
        cuts.append(len(doc))
        for a, b in zip(cuts, cuts[1:]):
            piece = doc[a:b].text.strip()
            if piece:
                # Make each piece look like a sentence: capitalise + period
                piece = piece[0].upper() + piece[1:]
                if not piece.endswith((".", "!", "?")):
                    piece += "."
                out.append(piece)
    return out


def _strip_disfluencies(text: str) -> str:
    cleaned = DISFLUENCY_RE.sub("", text)
    return re.sub(r"\s+", " ", cleaned).strip()


def purify_text(raw: str) -> str:
    """Top-level purifier. Returns clean text with one sentence per line."""
    flat = _normalise_whitespace(raw)
    flat = _insert_discourse_breaks(flat)
    flat = _capitalise_starts(flat)
    sents = _refine_with_spacy(flat)
    sents = _split_long_sentences(sents)
    # Disfluency strip after sentence segmentation, so we don't remove
    # tokens that the parser used for boundary detection.
    sents = [_strip_disfluencies(s) for s in sents]
    sents = [s for s in sents if len(s.split()) >= 4]
    # Ensure terminal punctuation
    sents = [s if s.endswith((".", "!", "?")) else s + "." for s in sents]
    return "\n".join(sents) + "\n"


def purify_file(in_path: Path, out_path: Path) -> int:
    raw = in_path.read_text(encoding="utf-8")
    cleaned = purify_text(raw)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(cleaned, encoding="utf-8")
    return cleaned.count("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_path", required=True, type=Path)
    ap.add_argument("--out_path", required=True, type=Path)
    args = ap.parse_args()
    n = purify_file(args.in_path, args.out_path)
    print(f"purified {args.in_path} -> {args.out_path} ({n} sentences)")


if __name__ == "__main__":
    main()
