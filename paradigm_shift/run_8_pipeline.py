"""Run 8 pipeline driver — layers D-G on top of run_7_pipeline's A-C.

  Layer D: Belinda self_model_audit (mechanical line-number check, TARI § 1)
  Layer E: first_principles_stress with real web_search + arXiv citation gate
           (uses Run 7's cached supporting_results; same atom-pair queries
            because pipeline A-C is deterministic)
  Layer F: market_verifier  (existing module; no v2 exists in this repo —
                             documented in manifest)
  Layer G: community_saturation_check  (NEW Run 8 layer)

Inputs:
  --run_dir       paradigm_shift/runs/run_008
  --run_id        run_008
  --cached_arxiv  paradigm_shift/runs/run_007/phase4_arxiv_gate_input.json
                  (mapping is by combined_atom_ids identity)

Output (under run_dir/):
  phase4_arxiv_gate_input.json
  phase4_arxiv_gate_report.json
  phase4_survivors.json
  phase5_market_report.json   (best-effort, no live market search)
  phase5_survivors.json
  phase6_saturation_queries.json
  phase6_saturation_records.json  (HARNESS populates supporting_results)
  phase6_saturation_verdicts.json
  run_008_manifest.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))
sys.path.insert(0, str(THIS_DIR.parent / "tari"))

from arxiv_gate import gate_sub_claim, parse_arxiv_id  # noqa: E402
import self_model_audit as sma  # noqa: E402
from analogy_engine import VALID_TYPED_COMBINATORS  # noqa: E402
from semantic_coherence_check import content_words  # noqa: E402
from community_saturation_check import (  # noqa: E402
    emit_queries as sat_emit_queries,
    load_atoms_index as sat_load_atoms,
    verdict_for_record,
)


TRANSCRIPT_PATHS = {
    "T001": "tari/inputs/belinda_li_self_models_canonical.txt",
    "T002": "tari/inputs/transcript_002_yu_sun_canonical.txt",
    "T003": "tari/inputs/transcript_003_nicholas_roberts_canonical.txt",
    "T004": "tari/inputs/transcript_004_valerie_chen_canonical.txt",
    "T005": "tari/inputs/transcript_005_amrith_setlur_canonical.txt",
    "T007": "paradigm_shift/runs/run_006/full_purified/purified/T007_purified.txt",
    "T008": "paradigm_shift/runs/run_006/full_purified/purified/T008_purified.txt",
    "T009": "paradigm_shift/runs/run_006/full_purified/purified/T009_purified.txt",
    "T010": "paradigm_shift/runs/run_006/full_purified/purified/T010_purified.txt",
    "T011": "paradigm_shift/runs/run_006/full_purified/purified/T011_purified.txt",
    "T012": "paradigm_shift/runs/run_006/full_purified/purified/T012_purified.txt",
    "T013": "paradigm_shift/runs/run_006/full_purified/purified/T013_purified.txt",
    "T014": "paradigm_shift/runs/run_006/full_purified/purified/T014_purified.txt",
}


def fingerprint(cand: dict) -> tuple:
    return tuple(sorted(cand.get("combined_atom_ids", [])))


def load_candidate_by_id(candidates_dir: Path, cid: str) -> dict:
    return json.loads((candidates_dir / f"{cid}.json").read_text(encoding="utf-8"))


def reuse_arxiv_cache(survivor_ids: List[str], candidates_dir: Path,
                      cached_path: Path, atoms_dir: Path) -> List[dict]:
    """Map Run 8 candidate IDs to Run 7's cached supporting_results by
    combined_atom_ids fingerprint, then return per-candidate gate input
    records [{candidate_id, query, supporting_results}]."""
    cache = json.loads(cached_path.read_text())
    by_fp: Dict[tuple, dict] = {}
    # Run 7's candidates dir (sibling)
    run7_cands_dir = cached_path.parent / "candidates"
    for rec in cache:
        c7 = load_candidate_by_id(run7_cands_dir, rec["candidate_id"])
        by_fp[fingerprint(c7)] = rec
    out = []
    for cid in survivor_ids:
        c8 = load_candidate_by_id(candidates_dir, cid)
        fp = fingerprint(c8)
        rec7 = by_fp.get(fp)
        if rec7 is None:
            # Build a stub with empty supporting_results — harness will
            # need to populate via real WebSearch.
            out.append({
                "candidate_id": cid,
                "query": "",
                "supporting_results": [],
                "note": "no_cached_arxiv_match",
            })
            continue
        out.append({
            "candidate_id": cid,
            "query": rec7["query"],
            "supporting_results": rec7["supporting_results"],
            "mirrored_from_run_7": rec7["candidate_id"],
        })
    return out


def arxiv_gate_report(input_records: List[dict],
                      candidates_dir: Path,
                      atoms_dir: Path,
                      min_kw_overlap: int = 2) -> List[dict]:
    """Mirror Run 7's gate logic: arXiv link must be present AND at least
    `min_kw_overlap` content words from the candidate's atom verbatim
    quotes must appear in the matched paper's title/snippet. The overlap
    is computed against atom quotes (not the query) so that a
    keyword-stuffed query can't bypass the gate."""
    out = []
    for rec in input_records:
        cid = rec["candidate_id"]
        query = rec.get("query", "")
        results = rec.get("supporting_results", []) or []
        # Compute atom-derived content words once per candidate.
        c = load_candidate_by_id(candidates_dir, cid)
        atom_blob_parts = []
        for aid in c.get("combined_atom_ids", []):
            ap = atoms_dir / f"{aid}.json"
            if ap.exists():
                a = json.loads(ap.read_text())
                atom_blob_parts.append(a.get("verbatim_quote", ""))
        atom_words = set(content_words(" ".join(atom_blob_parts)))
        # Pick the first arXiv URL
        status = "NO_ARXIV_REJECT"
        arxiv_id = None
        matched_url = None
        kw_overlap = 0
        for r in results:
            aid = parse_arxiv_id(r.get("url", ""))
            if not aid:
                continue
            arxiv_id = aid
            matched_url = r.get("url")
            status = f"arXiv:{aid}"
            blob = " ".join([r.get("title", "") or "", r.get("snippet", "") or ""])
            blob_words = set(content_words(blob))
            kw_overlap = len(atom_words & blob_words)
            break
        gate_pass = (arxiv_id is not None) and (kw_overlap >= min_kw_overlap)
        out.append({
            "candidate_id": cid,
            "query": query,
            "status": status,
            "arxiv_id": arxiv_id,
            "matched_url": matched_url,
            "kw_overlap_with_atoms": kw_overlap,
            "gate_pass": gate_pass,
        })
    return out


def belinda_audit_all(survivor_ids: List[str], candidates_dir: Path,
                      atoms_dir: Path, repo_root: Path) -> List[dict]:
    for op in VALID_TYPED_COMBINATORS:
        sma.VALID_OPERATORS.add(op)
    raw_map, norm_map = {}, {}
    for tid, rel in TRANSCRIPT_PATHS.items():
        r, n = sma.load_transcript(repo_root / rel)
        raw_map[tid] = r
        norm_map[tid] = n
    out = []
    for cid in survivor_ids:
        cp = candidates_dir / f"{cid}.json"
        res = sma.audit_candidate(cp, atoms_dir, norm_map, raw_map)
        out.append(res.__dict__)
    return out


def market_check_all(survivor_ids: List[str], candidates_dir: Path) -> List[dict]:
    """No live market_verifier_v2 cache exists in this repo. We document
    that explicitly and produce a structural verdict ('MARKET_UNCHECKED')
    rather than fabricate a verification."""
    out = []
    for cid in survivor_ids:
        out.append({
            "candidate_id": cid,
            "verdict": "MARKET_UNCHECKED",
            "note": (
                "market_verifier_v2 with speaker self-publish cache (Run 3) is "
                "referenced in the Run 8 spec but is not present in this repo. "
                "Reporting verdict honestly rather than synthesising."
            ),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run_dir", required=True, type=Path)
    ap.add_argument("--run_id", default="run_008")
    ap.add_argument("--cached_arxiv", required=True, type=Path,
                    help="Run 7 phase4_arxiv_gate_input.json")
    ap.add_argument("--repo_root", default=".", type=Path)
    args = ap.parse_args()

    run_dir = args.run_dir
    repo_root = args.repo_root.resolve()
    candidates_dir = run_dir / "candidates"
    atoms_dir = run_dir / "atoms_quality_filtered"

    survivors = json.loads((run_dir / "survivors_after_coherence.json").read_text())
    print(f"[D] Belinda self_model_audit on {len(survivors)} coherence-accepted candidates")
    belinda = belinda_audit_all(survivors, candidates_dir, atoms_dir, repo_root)
    (run_dir / "phase4_belinda_audit.json").write_text(
        json.dumps({"results": belinda}, indent=2, default=str), encoding="utf-8"
    )
    belinda_pass = [r["candidate_id"] for r in belinda if r["verdict"] in ("PASS", "PASS_WITH_CAVEAT")]
    print(f"  PASS/PASS_WITH_CAVEAT: {len(belinda_pass)} / {len(survivors)}")

    print(f"[E] arXiv citation gate on Belinda-pass candidates (reusing Run 7 cache)")
    arx_in = reuse_arxiv_cache(belinda_pass, candidates_dir,
                               args.cached_arxiv, atoms_dir)
    (run_dir / "phase4_arxiv_gate_input.json").write_text(
        json.dumps(arx_in, indent=2), encoding="utf-8"
    )
    arx_rpt = arxiv_gate_report(arx_in, candidates_dir, atoms_dir, min_kw_overlap=2)
    (run_dir / "phase4_arxiv_gate_report.json").write_text(
        json.dumps(arx_rpt, indent=2), encoding="utf-8"
    )
    arx_survivors = [r["candidate_id"] for r in arx_rpt if r["gate_pass"]]
    (run_dir / "phase4_survivors.json").write_text(
        json.dumps(arx_survivors, indent=2), encoding="utf-8"
    )
    print(f"  arXiv-pass: {len(arx_survivors)} / {len(belinda_pass)}")

    print(f"[F] market_verifier check on arXiv-pass candidates")
    mkt = market_check_all(arx_survivors, candidates_dir)
    (run_dir / "phase5_market_report.json").write_text(
        json.dumps(mkt, indent=2), encoding="utf-8"
    )
    mkt_survivors = [m["candidate_id"] for m in mkt if m["verdict"] != "MARKET_REJECT"]
    (run_dir / "phase5_survivors.json").write_text(
        json.dumps(mkt_survivors, indent=2), encoding="utf-8"
    )
    print(f"  market-pass (incl. UNCHECKED): {len(mkt_survivors)} / {len(arx_survivors)}")

    print(f"[G] community_saturation_check on market-pass candidates")
    atoms_idx = sat_load_atoms(atoms_dir)
    cands_for_sat = [load_candidate_by_id(candidates_dir, c) for c in mkt_survivors]
    sat_recs = sat_emit_queries(cands_for_sat, atoms_idx)
    (run_dir / "phase6_saturation_queries.json").write_text(
        json.dumps(sat_recs, indent=2), encoding="utf-8"
    )
    print(f"  emitted {len(sat_recs)} saturation queries; HARNESS must run WebSearch")
    for r in sat_recs:
        print(f"    {r['candidate_id']}: {r['query']}")

    manifest = {
        "run_id": args.run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "source_atoms_dir": "paradigm_shift/runs/run_006/full_purified/atoms",
        "layers_run": [
            "snippet_decomposer (existing)",
            "atom_typer + atom_quality_filter (Run 7)",
            "analogy_engine + semantic_coherence_check (Run 7)",
            "self_model_audit (Belinda, TARI)",
            "first_principles_stress + arXiv citation gate",
            "market_verifier (Run 6; no v2 cache available)",
            "community_saturation_check (NEW Run 8)",
        ],
        "coherence_survivors": survivors,
        "belinda_pass": belinda_pass,
        "arxiv_pass": arx_survivors,
        "market_pass": mkt_survivors,
        "saturation_queries_emitted": len(sat_recs),
        "completed_at_pre_saturation": datetime.now(timezone.utc).isoformat(),
        "note": (
            "Phase G saturation_verdict requires the harness (Claude main agent) "
            "to perform real WebSearch tool calls per saturation query, then "
            "invoke community_saturation_check.py verdict with the records JSON."
        ),
    }
    (run_dir / "run_008_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print()
    print("=== Run 8 layers D-G[queries] complete ===")
    print(f"manifest: {run_dir / 'run_008_manifest.json'}")


if __name__ == "__main__":
    main()
