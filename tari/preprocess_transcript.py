"""Preprocess raw transcripts into line-numbered canonical form.

Splits a single-line transcript into one sentence per line. The resulting file
is the canonical input to TARI: line numbers are stable and reference-able.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def preprocess(in_path: Path, out_path: Path) -> int:
    text = in_path.read_text(encoding="utf-8")
    # Strip system-reminder noise that may appear at end-of-file from upload artifacts.
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.DOTALL)
    sentences = SENTENCE_END.split(text)
    lines = [s.strip() for s in sentences if s.strip()]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_path", required=True, type=Path)
    ap.add_argument("--out_path", required=True, type=Path)
    args = ap.parse_args()
    n = preprocess(args.in_path, args.out_path)
    print(f"preprocessed {args.in_path} -> {args.out_path} ({n} sentences/lines)")


if __name__ == "__main__":
    main()
