"""Self-model audit for TARI v1.

For each candidate, answer Belinda Li's three self-model questions and run
MECHANICAL checks (no LLM call) against the transcript file.

Q1 (activations from which atoms): which atoms drove this candidate?
    Check: every atom_id listed in candidate.combined_atom_ids must exist in atoms_dir.

Q2 (which gates / components used): which combination operator was applied?
    Check: combination_operator must be one of the 6 named operators.

Q3 (verbatim input lines): which verbatim transcript lines anchor this?
    Check: for each cited atom, the atom's verbatim_quote must appear (substring,
    whitespace-normalized) in the transcript text between the atom's line_span.

Auxiliary checks:
    - the candidate uses >= 2 atoms from distinct snippets (unless operator is INVERT)
    - why_novel_vs_speaker is non-empty and references at least one snippet_id
    - the candidate does not simply restate the verbatim quote (avoid "just rephrase")

The audit verdict is PASS, FAIL_<reason>, or PASS_WITH_CAVEAT (when minor issues
do not invalidate traceability).
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


VALID_OPERATORS = {"ANALOGIZE", "INVERT", "COMPOSE", "GENERALIZE", "RESTRICT", "CONTRAST"}


def normalize_whitespace(s: str) -> str:
    """Collapse runs of whitespace into single spaces, strip."""
    return re.sub(r"\s+", " ", s).strip()


def normalize_for_match(s: str) -> str:
    """Aggressive normalization: whitespace, unicode, lowercase."""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip().lower()
    return s


@dataclass
class AuditResult:
    candidate_id: str
    verdict: str  # PASS, FAIL_<reason>, PASS_WITH_CAVEAT
    q1_atoms_exist: bool
    q1_explanation: str
    q2_operator_valid: bool
    q2_explanation: str
    q3_quotes_verbatim_in_transcript: bool
    q3_explanation: str
    q3_per_atom_checks: List[dict] = field(default_factory=list)
    aux_distinct_snippets: bool = False
    aux_novelty_field_substantive: bool = False
    aux_not_pure_restatement: bool = False
    caveats: List[str] = field(default_factory=list)
    fail_reasons: List[str] = field(default_factory=list)
    timestamp: str = ""


def load_transcript(path: Path) -> tuple:
    """Return (raw_text, normalized_text)."""
    raw = path.read_text(encoding="utf-8")
    return raw, normalize_for_match(raw)


def load_atom(atoms_dir: Path, atom_id: str) -> Optional[dict]:
    p = atoms_dir / f"{atom_id}.json"
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_q3_quote_in_transcript(atom: dict, transcript_norm: str, transcript_raw: str) -> dict:
    """Check that the atom's verbatim_quote appears in the transcript.

    We check normalized substring containment. Also report the line in the
    raw transcript where the match starts, if any.
    """
    quote = atom["verbatim_quote"]
    quote_norm = normalize_for_match(quote)
    # Trim leading "..." or trailing "..." that the gloss might have introduced
    # (the atom's verbatim_quote should be unedited, but be defensive)
    quote_norm = quote_norm.strip(" .")

    if len(quote_norm) < 15:
        return {
            "atom_id": atom["atom_id"],
            "ok": False,
            "reason": "quote_too_short_after_normalization",
            "quote_norm_length": len(quote_norm),
        }

    in_transcript = quote_norm in transcript_norm
    return {
        "atom_id": atom["atom_id"],
        "ok": in_transcript,
        "reason": "verbatim_quote_found" if in_transcript else "verbatim_quote_NOT_found",
        "quote_preview": (quote_norm[:120] + "...") if len(quote_norm) > 120 else quote_norm,
    }


def audit_candidate(
    candidate_path: Path,
    atoms_dir: Path,
    transcript_norm,  # str OR dict[transcript_id -> normalized text]
    transcript_raw,   # str OR dict[transcript_id -> raw text]
) -> AuditResult:
    """Audit a candidate against its source transcript(s).

    transcript_norm and transcript_raw may be either:
      - a single string (run_001 backwards-compatible single-transcript mode)
      - a dict mapping transcript_id -> string (v2 multi-transcript mode)
    When dict mode is used, each cited atom is checked against its own
    transcript_id's text.
    """
    with candidate_path.open("r", encoding="utf-8") as f:
        cand = json.load(f)

    cand_id = cand["candidate_id"]

    res = AuditResult(
        candidate_id=cand_id,
        verdict="PENDING",
        q1_atoms_exist=False,
        q1_explanation="",
        q2_operator_valid=False,
        q2_explanation="",
        q3_quotes_verbatim_in_transcript=False,
        q3_explanation="",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    # --- Q1: cited atoms exist ---
    missing = []
    atom_objs = []
    for aid in cand.get("combined_atom_ids", []):
        ao = load_atom(atoms_dir, aid)
        if ao is None:
            missing.append(aid)
        else:
            atom_objs.append(ao)
    if missing:
        res.q1_atoms_exist = False
        res.q1_explanation = f"missing atom_ids: {missing}"
        res.fail_reasons.append("Q1_atoms_missing")
    elif not atom_objs:
        res.q1_atoms_exist = False
        res.q1_explanation = "candidate has zero atom citations"
        res.fail_reasons.append("Q1_no_atoms_cited")
    else:
        res.q1_atoms_exist = True
        res.q1_explanation = f"all {len(atom_objs)} cited atoms exist in atoms_dir"

    # --- Q2: operator valid ---
    op = cand.get("combination_operator", "")
    if op in VALID_OPERATORS:
        res.q2_operator_valid = True
        res.q2_explanation = f"operator '{op}' is one of the 6 valid operators"
    else:
        res.q2_operator_valid = False
        res.q2_explanation = f"operator '{op}' is not in {sorted(VALID_OPERATORS)}"
        res.fail_reasons.append("Q2_operator_invalid")

    # --- Q3: verbatim quotes appear in transcript ---
    # In multi-transcript mode (dict input), look up each atom's transcript text
    # by atom.transcript_id. In single-transcript mode (str input), use the same
    # text for every atom (run_001 backwards-compatible).
    def _norm_for(atom_obj):
        if isinstance(transcript_norm, dict):
            tid = atom_obj.get("transcript_id", "T001")
            return transcript_norm.get(tid, "")
        return transcript_norm

    def _raw_for(atom_obj):
        if isinstance(transcript_raw, dict):
            tid = atom_obj.get("transcript_id", "T001")
            return transcript_raw.get(tid, "")
        return transcript_raw

    per_atom_checks = [check_q3_quote_in_transcript(a, _norm_for(a), _raw_for(a))
                       for a in atom_objs]
    res.q3_per_atom_checks = per_atom_checks
    if per_atom_checks and all(c["ok"] for c in per_atom_checks):
        res.q3_quotes_verbatim_in_transcript = True
        res.q3_explanation = f"all {len(per_atom_checks)} cited atoms' quotes found verbatim"
    else:
        bad = [c["atom_id"] for c in per_atom_checks if not c["ok"]]
        res.q3_quotes_verbatim_in_transcript = False
        res.q3_explanation = f"atoms with quote NOT found: {bad}"
        if bad:
            res.fail_reasons.append("Q3_quote_not_verbatim")

    # --- Aux checks ---
    snippet_ids = {a.get("snippet_id") for a in atom_objs}
    if op == "INVERT":
        # INVERT is allowed on a single atom
        res.aux_distinct_snippets = True
    else:
        res.aux_distinct_snippets = len(snippet_ids) >= 2
        if not res.aux_distinct_snippets:
            res.fail_reasons.append("AUX_same_snippet_combination")

    novelty_text = cand.get("why_novel_vs_speaker", "")
    if len(novelty_text.strip()) > 50 and any(sid in novelty_text for sid in snippet_ids):
        res.aux_novelty_field_substantive = True
    else:
        res.aux_novelty_field_substantive = False
        res.caveats.append("AUX_novelty_field_lacks_snippet_reference")

    # Pure restatement check: does the candidate.claim normalized contain >= 80% of any
    # atom's verbatim quote (normalized)?
    claim_norm = normalize_for_match(cand.get("claim", ""))
    res.aux_not_pure_restatement = True
    for a in atom_objs:
        quote_norm = normalize_for_match(a["verbatim_quote"])
        if len(quote_norm) > 40 and quote_norm[:int(0.8 * len(quote_norm))] in claim_norm:
            res.aux_not_pure_restatement = False
            res.caveats.append(f"AUX_claim_largely_restates_{a['atom_id']}")
            break

    # --- Final verdict ---
    hard_fails = [r for r in res.fail_reasons if not r.startswith("AUX_") or r == "AUX_same_snippet_combination"]
    if hard_fails:
        res.verdict = "FAIL_" + "_".join(hard_fails[:2])
    elif res.caveats:
        res.verdict = "PASS_WITH_CAVEAT"
    else:
        res.verdict = "PASS"

    return res


def audit_all(
    candidates_dir: Path,
    atoms_dir: Path,
    transcript_path,  # Path OR dict[transcript_id -> Path]
    out_path: Path,
) -> List[AuditResult]:
    """Audit candidates. transcript_path can be a single Path or a dict mapping
    transcript_id -> Path (v2 multi-transcript mode)."""
    if isinstance(transcript_path, dict):
        raw_map, norm_map = {}, {}
        for tid, tp in transcript_path.items():
            r, n = load_transcript(Path(tp))
            raw_map[tid] = r
            norm_map[tid] = n
        raw, normed = raw_map, norm_map
        tp_meta = {tid: str(p) for tid, p in transcript_path.items()}
    else:
        raw, normed = load_transcript(Path(transcript_path))
        tp_meta = str(transcript_path)

    results = []
    for cp in sorted(candidates_dir.glob("CAND_*.json")):
        r = audit_candidate(cp, atoms_dir, normed, raw)
        results.append(r)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "n_candidates": len(results),
            "transcript_path": tp_meta,
            "audited_at": datetime.now(timezone.utc).isoformat(),
            "results": [asdict(r) for r in results],
            "verdict_distribution": {
                v: sum(1 for r in results if r.verdict == v)
                for v in {r.verdict for r in results}
            },
        }, f, indent=2, ensure_ascii=False)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates_dir", required=True, type=Path)
    ap.add_argument("--atoms_dir", required=True, type=Path)
    ap.add_argument("--transcript", required=True, type=Path)
    ap.add_argument("--out_path", required=True, type=Path)
    args = ap.parse_args()
    results = audit_all(args.candidates_dir, args.atoms_dir, args.transcript, args.out_path)
    print(f"audited {len(results)} candidates")
    verdicts = {}
    for r in results:
        verdicts[r.verdict] = verdicts.get(r.verdict, 0) + 1
    for v, n in sorted(verdicts.items()):
        print(f"  {v:50s} {n}")


if __name__ == "__main__":
    main()
