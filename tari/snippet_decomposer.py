"""Snippet decomposer for TARI v1.

Reads an input transcript (UTF-8 plain text, one paragraph likely on one long line
or multiple lines), splits it into snippets at sentence-level granularity using
simple regex + manual boundary heuristics, and writes one JSON file per snippet.

The "boundary justification" field documents WHY each snippet starts/ends where it does,
so an external reviewer can audit decomposition choices.

Honest deviation: snippet boundaries are chosen heuristically. The transcript-line
numbering used as provenance is the canonical line numbering of the input file
(1-based), and is preserved verbatim through the rest of the pipeline.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List


# Sentence-splitter regex: split on .!? followed by whitespace and a capital letter.
# This is intentionally simple — over-segmentation is preferred to under-segmentation
# because the next step (atom_extractor) groups sentences within thematic boundaries.
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")

# Approximate target sentence count per snippet. Tuned for ~10000-word transcripts
# producing 20-40 snippets total.
TARGET_SENTENCES_PER_SNIPPET = 8
MIN_SENTENCES_PER_SNIPPET = 4
MAX_SENTENCES_PER_SNIPPET = 14


# Topic-shift markers that strongly suggest a new snippet boundary.
# These are markers a speaker uses to start a new section.
TOPIC_SHIFT_PHRASES = [
    "okay so",
    "so let me",
    "now let's",
    "now what",
    "so what",
    "the first part",
    "the second part",
    "the third part",
    "part one",
    "part two",
    "part three",
    "next up",
    "moving on",
    "in this section",
    "in this next section",
    "in the first section",
    "in the second section",
    "in the third section",
    "let's switch gears",
    "to recap",
    "to summarize",
    "in summary",
    "so to summarize",
    "to wrap up",
    "and finally",
    "and just to",
    "another question",
    "another thing",
]


@dataclass
class Snippet:
    snippet_id: str
    transcript_id: str
    start_line: int
    end_line: int
    verbatim_text: str
    boundary_justification: str
    sentence_count: int
    char_count: int


def load_transcript_lines(path: Path) -> List[str]:
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


def split_into_sentences_with_positions(text: str) -> List[tuple]:
    """Return list of (sentence_text, char_start_offset_in_text)."""
    out = []
    cursor = 0
    parts = SENTENCE_END.split(text)
    for part in parts:
        if not part.strip():
            cursor += len(part) + 1  # account for split whitespace
            continue
        idx = text.find(part, cursor)
        if idx < 0:
            idx = cursor
        out.append((part.strip(), idx))
        cursor = idx + len(part)
    return out


def char_offset_to_line(text: str, char_offset: int) -> int:
    """1-based line number containing the character at char_offset."""
    return text[:char_offset].count("\n") + 1


def is_topic_shift(sentence: str) -> bool:
    s = sentence.lower()[:60]
    return any(phrase in s for phrase in TOPIC_SHIFT_PHRASES)


def decompose(transcript_path: Path, out_dir: Path, transcript_id: str = "T001") -> List[Snippet]:
    raw_text = transcript_path.read_text(encoding="utf-8")
    sentences = split_into_sentences_with_positions(raw_text)

    snippets: List[Snippet] = []
    current_sentences: List[tuple] = []
    current_justification_tokens: List[str] = []

    def flush(reason: str):
        nonlocal current_sentences, current_justification_tokens
        if not current_sentences:
            return
        # Build snippet from current_sentences
        first_offset = current_sentences[0][1]
        last_sentence_text, last_offset = current_sentences[-1]
        last_offset_end = last_offset + len(last_sentence_text)
        start_line = char_offset_to_line(raw_text, first_offset)
        end_line = char_offset_to_line(raw_text, last_offset_end)
        verbatim = " ".join(s[0] for s in current_sentences)
        sid = f"S{len(snippets) + 1:03d}"
        snippets.append(Snippet(
            snippet_id=sid,
            transcript_id=transcript_id,
            start_line=start_line,
            end_line=end_line,
            verbatim_text=verbatim,
            boundary_justification=(
                f"reason={reason}; "
                f"sentence_count={len(current_sentences)}; "
                f"topic_shift_markers={','.join(current_justification_tokens) or 'none'}"
            ),
            sentence_count=len(current_sentences),
            char_count=len(verbatim),
        ))
        current_sentences = []
        current_justification_tokens = []

    for i, (sentence, offset) in enumerate(sentences):
        # Topic shift detection — but only valid as a snippet boundary if we have
        # accumulated at least MIN_SENTENCES.
        if (is_topic_shift(sentence)
                and len(current_sentences) >= MIN_SENTENCES_PER_SNIPPET):
            flush("topic_shift_marker_at_next_sentence")
            current_sentences.append((sentence, offset))
            current_justification_tokens.append(sentence[:30])
            continue

        current_sentences.append((sentence, offset))

        if len(current_sentences) >= MAX_SENTENCES_PER_SNIPPET:
            flush("max_sentences_reached")
        elif (len(current_sentences) >= TARGET_SENTENCES_PER_SNIPPET
              and i + 1 < len(sentences)
              and is_topic_shift(sentences[i + 1][0])):
            flush("target_reached_next_sentence_is_topic_shift")
        elif len(current_sentences) >= TARGET_SENTENCES_PER_SNIPPET + 2:
            # Soft cap — break if a paragraph end is detected (double newline).
            current_end = offset + len(sentence)
            tail = raw_text[current_end:current_end + 5]
            if "\n\n" in tail or "\n " in tail:
                flush("paragraph_break_after_target")

    flush("end_of_transcript")

    out_dir.mkdir(parents=True, exist_ok=True)
    for snip in snippets:
        out_path = out_dir / f"snippet_{snip.snippet_id}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(asdict(snip), f, indent=2, ensure_ascii=False)

    # Write index
    index_path = out_dir / "_index.json"
    with index_path.open("w", encoding="utf-8") as f:
        json.dump({
            "transcript_id": transcript_id,
            "transcript_path": str(transcript_path),
            "n_snippets": len(snippets),
            "total_sentences": len(sentences),
            "decomposed_at": datetime.now(timezone.utc).isoformat(),
            "snippet_ids": [s.snippet_id for s in snippets],
        }, f, indent=2)

    return snippets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--transcript_id", default="T001", type=str)
    args = ap.parse_args()
    snippets = decompose(args.transcript, args.out_dir, args.transcript_id)
    print(f"decomposed {args.transcript} into {len(snippets)} snippets at {args.out_dir}")
    for s in snippets[:5]:
        print(f"  {s.snippet_id}  lines {s.start_line}-{s.end_line}  "
              f"({s.sentence_count} sentences, {s.char_count} chars)")
    if len(snippets) > 5:
        print(f"  ... ({len(snippets) - 5} more)")


if __name__ == "__main__":
    main()
