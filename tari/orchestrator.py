"""TARI v1 orchestrator.

End-to-end pipeline runner:
  1. snippet_decomposer  -> snippets/
  2. atom_extractor      -> atoms/
  3. brainstorm_engine   -> candidates/
  4. self_model_audit    -> audit/self_model_audit.json
  5. external_verifier   -> verdict/external_verification.json
  6. write summary.md

The orchestrator can be invoked in two modes:
  --search_mode synthesized   (default; reuses program_v20 synthesized search)
  --search_mode real          (orchestrator was invoked by an agent that has
                               provided a pre-fetched real_search results JSON
                               via --real_search_path)

The real-search path is left as a hook: when the agent loop wants real WebSearch
results, it issues the queries externally and writes a results JSON that the
orchestrator loads. This separation keeps the orchestrator deterministic
(no LLM call, no tool call) and the WebSearch step explicit / auditable.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

from snippet_decomposer import decompose
from atom_extractor import extract_all
from brainstorm_engine import brainstorm
from self_model_audit import audit_all
from external_verifier import verify_all, synthesized_search_callback, extract_content_words


def load_real_search_results(real_search_path: Path) -> dict:
    """Real WebSearch results map: { candidate_id: [ {title, snippet, url}, ... ] }"""
    if not real_search_path.exists():
        return {}
    with real_search_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def real_search_callback_factory(real_search_map: dict, candidate_id: str):
    def fn(query: str):
        return real_search_map.get(candidate_id, [])
    return fn


def run_epoch(
    transcript_path: Path,
    run_dir: Path,
    run_id: str,
    max_candidates: int = 15,
    real_search_path: Path = None,
) -> dict:
    snippets_dir = run_dir / "snippets"
    atoms_dir = run_dir / "atoms"
    candidates_dir = run_dir / "candidates"
    audit_path = run_dir / "audit" / "self_model_audit.json"
    verdict_path = run_dir / "verdict" / "external_verification.json"

    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "audit").mkdir(exist_ok=True)
    (run_dir / "verdict").mkdir(exist_ok=True)

    # 1. snippet decomposition
    snippets = decompose(transcript_path, snippets_dir)

    # 2. atom extraction
    atoms = extract_all(snippets_dir, atoms_dir)

    # 3. brainstorm
    candidates = brainstorm(atoms_dir, candidates_dir, run_id=run_id, max_candidates=max_candidates)

    # 4. audit
    audit_results = audit_all(candidates_dir, atoms_dir, transcript_path, audit_path)

    # 5. external verification
    # Convert audit_results dataclasses → dicts for verify_all expected shape
    audit_dicts = [
        {
            "candidate_id": r.candidate_id,
            "verdict": r.verdict,
        }
        for r in audit_results
    ]
    real_search_map = load_real_search_results(real_search_path) if real_search_path else {}

    # Per-candidate verification, choosing search fn based on availability
    from external_verifier import verify_candidate, ExternalResult
    from dataclasses import asdict
    pass_audit_ids = {r.candidate_id for r in audit_results if r.verdict.startswith("PASS")}
    verification_results = []
    for cp in sorted(candidates_dir.glob("CAND_*.json")):
        with cp.open("r", encoding="utf-8") as f:
            cand = json.load(f)
        if cand["candidate_id"] not in pass_audit_ids:
            continue
        if cand["candidate_id"] in real_search_map:
            search_fn = real_search_callback_factory(real_search_map, cand["candidate_id"])
            real_used = True
        else:
            search_fn = synthesized_search_callback
            real_used = False
        # Build atom_text for keyword check: concatenate the cited atoms' verbatim quotes.
        atom_texts = []
        for aid in cand.get("combined_atom_ids", []):
            ap = atoms_dir / f"{aid}.json"
            if ap.exists():
                with ap.open("r", encoding="utf-8") as f:
                    atom_texts.append(json.load(f).get("verbatim_quote", ""))
        atom_text = " ".join(atom_texts)
        r = verify_candidate(cand, search_fn=search_fn, record_real_websearch=real_used,
                             atom_text_for_keywords=atom_text)
        verification_results.append(r)

    with verdict_path.open("w", encoding="utf-8") as f:
        json.dump({
            "n_candidates_verified": len(verification_results),
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "results": [asdict(r) for r in verification_results],
            "verdict_distribution": {
                v: sum(1 for r in verification_results if r.verdict == v)
                for v in {r.verdict for r in verification_results}
            },
            "real_websearch_used_for_candidates": sorted(real_search_map.keys()),
        }, f, indent=2, ensure_ascii=False)

    # 6. summary
    summary = {
        "run_id": run_id,
        "transcript_path": str(transcript_path),
        "n_snippets": len(snippets),
        "n_atoms": len(atoms),
        "n_candidates": len(candidates),
        "audit_verdicts": {
            v: sum(1 for r in audit_results if r.verdict == v)
            for v in {r.verdict for r in audit_results}
        },
        "external_verdicts": {
            v: sum(1 for r in verification_results if r.verdict == v)
            for v in {r.verdict for r in verification_results}
        },
        "ended_at": datetime.now(timezone.utc).isoformat(),
    }
    write_summary_md(run_dir, summary, audit_results, verification_results, candidates, atoms, snippets)
    return summary


def write_summary_md(run_dir: Path, summary: dict, audit_results, verification_results, candidates, atoms, snippets):
    md = []
    md.append(f"# TARI v1 — Run `{summary['run_id']}` Summary\n")
    md.append(f"Transcript: `{summary['transcript_path']}`\n")
    md.append(f"Ended at: {summary['ended_at']}\n")
    md.append("\n---\n\n## Pipeline counts\n")
    md.append(f"- Snippets: **{summary['n_snippets']}**")
    md.append(f"- Atoms: **{summary['n_atoms']}**")
    md.append(f"- Candidates (brainstorm): **{summary['n_candidates']}**")
    md.append("")
    md.append("## Audit verdicts (Belinda Q1/Q2/Q3)\n")
    for v, n in sorted(summary["audit_verdicts"].items(), key=lambda x: -x[1]):
        md.append(f"- {v}: {n}")
    md.append("")
    md.append("## External verification verdicts\n")
    if summary["external_verdicts"]:
        for v, n in sorted(summary["external_verdicts"].items(), key=lambda x: -x[1]):
            md.append(f"- {v}: {n}")
    else:
        md.append("- (no candidates survived audit — external verification skipped)")
    md.append("")

    # Per-candidate detail
    md.append("\n---\n\n## Per-candidate detail\n")
    audit_by_id = {r.candidate_id: r for r in audit_results}
    verif_by_id = {r.candidate_id: r for r in verification_results}
    for c in candidates:
        cid = c.candidate_id
        md.append(f"\n### {cid}  ({c.combination_operator})\n")
        md.append(f"- Atoms: {', '.join(c.combined_atom_ids)}")
        md.append(f"- Source snippets: {', '.join(c.source_snippets)}")
        md.append(f"- Claim: {c.claim}")
        a = audit_by_id.get(cid)
        if a:
            md.append(f"- Audit verdict: **{a.verdict}**")
            md.append(f"  - Q1 (atoms exist): {a.q1_atoms_exist} — {a.q1_explanation}")
            md.append(f"  - Q2 (operator valid): {a.q2_operator_valid} — {a.q2_explanation}")
            md.append(f"  - Q3 (quotes verbatim): {a.q3_quotes_verbatim_in_transcript} — {a.q3_explanation}")
            if a.caveats:
                md.append(f"  - Caveats: {a.caveats}")
            if a.fail_reasons:
                md.append(f"  - Fail reasons: {a.fail_reasons}")
        v = verif_by_id.get(cid)
        if v:
            md.append(f"- External verdict: **{v.verdict}**")
            md.append(f"  - step 06 keyword hits: {v.step_06.get('n_results_above_threshold')} / {v.step_06.get('n_results_checked')}")
            md.append(f"  - step 14.6 max sim: {v.step_14_6.get('max_functional_similarity')}")
            md.append(f"  - step 13.5 survives attack: {v.step_13_5.get('spec_survives_attack')}")
            md.append(f"  - real WebSearch issued: {v.real_websearch_issued}")
    md.append("\n---\n\n## Atom type distribution\n")
    by_type = {}
    for a in atoms:
        by_type[a.atom_type] = by_type.get(a.atom_type, 0) + 1
    for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
        md.append(f"- {t}: {n}")
    md.append("\n## Snippet coverage\n")
    md.append(f"- First snippet: lines {snippets[0].start_line}-{snippets[0].end_line}")
    md.append(f"- Last snippet: lines {snippets[-1].start_line}-{snippets[-1].end_line}")
    md.append(f"- Mean sentences/snippet: {sum(s.sentence_count for s in snippets) / max(1, len(snippets)):.1f}")

    (run_dir / "summary.md").write_text("\n".join(md), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True, type=Path)
    ap.add_argument("--run_dir", required=True, type=Path)
    ap.add_argument("--run_id", required=True, type=str)
    ap.add_argument("--max_candidates", type=int, default=15)
    ap.add_argument("--real_search_path", type=Path, default=None,
                    help="JSON file mapping candidate_id -> list of {title, snippet, url}")
    args = ap.parse_args()
    summary = run_epoch(
        args.transcript,
        args.run_dir,
        args.run_id,
        max_candidates=args.max_candidates,
        real_search_path=args.real_search_path,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
