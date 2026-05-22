"""Orchestrator for Paradigm-Shift Finder v1.

Drives the 6-layer pipeline with checkpoint-based resumability.

Stages:
    manifest   — write run manifest from input transcripts
    snippets   — reuse TARI snippet_decomposer (per-transcript)
    atoms      — paradigm_shift atom_typer over all snippets
    candidates — analogy_engine: typed combinator brainstorm
    audit      — reuse TARI self_model_audit (mechanical traceability)
    scored     — impact_filter scoring
    stress     — first_principles_stress with RAG + self-consistency
    market     — market_verifier check for existing products/startups
    label      — write impact labeling prompt
    summary    — write summary.md

Each stage writes a stage-specific directory. Re-running with
--resume_from skips completed stages.

Web searches in Layer 5 and Layer 6 are wired through a `search_cache`
JSON file. The orchestrator never calls a live web_search itself; an
external agent loop (Claude Code) must pre-fetch results and write them
to `_search_cache.json` for the stress/market stages to use.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))
sys.path.insert(0, str(THIS_DIR.parent / "tari"))

from snippet_decomposer import decompose  # noqa: E402
from atom_extractor import extract_all  # noqa: E402  (TARI atom extractor)
from self_model_audit import audit_all  # noqa: E402

from atom_typer import extract_all_paradigm_atoms  # noqa: E402
from analogy_engine import brainstorm_paradigm_candidates  # noqa: E402
from impact_filter import score_all_candidates  # noqa: E402
from first_principles_stress import (  # noqa: E402
    stress_test_all, synthesized_search_callback,
)
from market_verifier import verify_all, synthesized_market_search  # noqa: E402
from impact_label_logger import build_label_prompt  # noqa: E402


STAGES = ["manifest", "snippets", "atoms_tari", "atoms_paradigm",
          "candidates", "audit", "scored", "stress", "market",
          "label", "summary"]


@dataclass
class RunPaths:
    run_dir: Path
    manifest_path: Path
    snippets_root: Path
    atoms_tari_dir: Path
    atoms_paradigm_dir: Path
    candidates_dir: Path
    audit_path: Path
    scored_dir: Path
    stress_dir: Path
    market_dir: Path
    label_prompt_path: Path
    summary_path: Path
    search_cache_path: Path
    framing_cache_path: Path


def build_paths(run_dir: Path) -> RunPaths:
    return RunPaths(
        run_dir=run_dir,
        manifest_path=run_dir / "manifest.json",
        snippets_root=run_dir / "snippets",
        atoms_tari_dir=run_dir / "atoms_tari",
        atoms_paradigm_dir=run_dir / "atoms",
        candidates_dir=run_dir / "candidates",
        audit_path=run_dir / "audit" / "self_model_audit.json",
        scored_dir=run_dir / "scored",
        stress_dir=run_dir / "stress",
        market_dir=run_dir / "market",
        label_prompt_path=run_dir / "label_prompt.md",
        summary_path=run_dir / "summary.md",
        search_cache_path=run_dir / "_search_cache.json",
        framing_cache_path=run_dir / "_framing_cache.json",
    )


def write_manifest(manifest_in_path: Path, manifest_out_path: Path):
    """Copy the input manifest to the run directory (with run-start timestamp)."""
    with manifest_in_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)
    manifest["run_started_at"] = datetime.now(timezone.utc).isoformat()
    manifest_out_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_out_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def run_snippets_stage(manifest: dict, snippets_root: Path) -> Dict[str, List]:
    """Run TARI snippet decomposer per transcript; return {tid: snippets_list}."""
    snippets_root.mkdir(parents=True, exist_ok=True)
    out: Dict[str, List] = {}
    for t in manifest.get("transcripts", []):
        tid = t["id"]
        tpath = Path(t["path"])
        tdir = snippets_root / tid
        tdir.mkdir(parents=True, exist_ok=True)
        snippets = decompose(tpath, tdir, transcript_id=tid)
        out[tid] = snippets
    return out


def flatten_snippets(snippets_root: Path) -> Path:
    """Create a flat directory of all snippet JSONs (TARI atom_extractor expects this).
    Re-namespaces files to avoid name collisions across transcripts.
    """
    flat = snippets_root / "_flat"
    flat.mkdir(parents=True, exist_ok=True)
    for tdir in sorted(snippets_root.iterdir()):
        if not tdir.is_dir() or tdir.name == "_flat":
            continue
        for sp in sorted(tdir.glob("snippet_S*.json")):
            # Copy with prefix
            with sp.open("r", encoding="utf-8") as f:
                d = json.load(f)
            tid = d.get("transcript_id", tdir.name)
            new_sid = f"{tid}_{sp.name.replace('snippet_', '').replace('.json', '')}"
            new_name = f"snippet_{new_sid}.json"
            with (flat / new_name).open("w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
    return flat


def load_search_cache(path: Path) -> Dict[str, List[dict]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_framing_cache(path: Path) -> Dict[str, List[str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def stage_complete(path: Path) -> bool:
    """A stage is complete if its primary output exists."""
    if path.is_file():
        return path.exists() and path.stat().st_size > 0
    if path.is_dir():
        # Stage complete if directory exists and has an _index.json
        idx = path / "_index.json"
        return idx.exists()
    return False


def write_summary(paths: RunPaths, manifest: dict, run_id: str):
    """Write a markdown summary of the run."""
    lines: List[str] = []
    lines.append(f"# Paradigm-Shift Finder v1 — Run `{run_id}` Summary")
    lines.append("")
    lines.append(f"Manifest: `{paths.manifest_path.relative_to(Path.cwd()) if paths.manifest_path.is_relative_to(Path.cwd()) else paths.manifest_path}`")
    lines.append(f"Run started: {manifest.get('run_started_at', 'unknown')}")
    lines.append(f"Run ended:   {datetime.now(timezone.utc).isoformat()}")
    lines.append("")

    # Transcripts
    lines.append("## Transcripts")
    lines.append("")
    for t in manifest.get("transcripts", []):
        lines.append(f"- **{t['id']}** {t.get('speaker', '?')} — _{t.get('topic', '?')}_  `{t['path']}`")
    lines.append("")

    # Atom counts
    if paths.atoms_paradigm_dir.exists():
        idx_p = paths.atoms_paradigm_dir / "_index.json"
        if idx_p.exists():
            with idx_p.open("r", encoding="utf-8") as f:
                idx = json.load(f)
            lines.append("## Atoms")
            lines.append("")
            lines.append(f"- Paradigm atoms: {idx['n_atoms']}")
            lines.append(f"- By paradigm_type: {idx['paradigm_type_distribution']}")
            lines.append(f"- By transcript: {idx['transcript_distribution']}")
            lines.append("")

    if paths.atoms_tari_dir.exists():
        idx_t = paths.atoms_tari_dir / "_index.json"
        if idx_t.exists():
            with idx_t.open("r", encoding="utf-8") as f:
                idx = json.load(f)
            lines.append(f"- TARI atoms (kept for cross-reference): {idx.get('n_atoms', 0)}")
            lines.append("")

    # Candidates
    if paths.candidates_dir.exists():
        idx_c = paths.candidates_dir / "_index.json"
        if idx_c.exists():
            with idx_c.open("r", encoding="utf-8") as f:
                idx = json.load(f)
            lines.append("## Candidates")
            lines.append("")
            lines.append(f"- Total: {idx['n_candidates']}")
            lines.append(f"- By operator: {idx['operator_distribution']}")
            lines.append(f"- By type pair: {idx['type_pair_distribution']}")
            lines.append("")

    # Audit
    if paths.audit_path.exists():
        with paths.audit_path.open("r", encoding="utf-8") as f:
            audit = json.load(f)
        lines.append("## Self-model audit verdicts")
        lines.append("")
        verdicts = {}
        for r in audit.get("results", []):
            verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
        for k, n in sorted(verdicts.items(), key=lambda x: -x[1]):
            lines.append(f"- {k}: {n}")
        lines.append("")

    # Scored
    if paths.scored_dir.exists():
        idx_s = paths.scored_dir / "_index.json"
        if idx_s.exists():
            with idx_s.open("r", encoding="utf-8") as f:
                idx = json.load(f)
            lines.append("## Impact scoring")
            lines.append("")
            lines.append(f"- Weights mode: {idx['weights_used']}")
            lines.append(f"- N scored: {idx['n_scored']}")
            lines.append(f"- Top 5 by predicted_impact:")
            for cid in idx["candidate_ids_by_predicted_impact_desc"][:5]:
                cp = paths.scored_dir / f"{cid}.json"
                if cp.exists():
                    with cp.open("r", encoding="utf-8") as f:
                        c = json.load(f)
                    sc = c.get("impact_score", {})
                    lines.append(
                        f"  - {cid}  impact={sc.get('predicted_impact', 0):.3f}  "
                        f"th={sc.get('time_horizon', 0):.1f}  is={sc.get('impact_scale', 0):.1f}  "
                        f"pt={sc.get('poc_tractability', 0):.2f}  ia={sc.get('information_asymmetry', 0):.2f}"
                    )
            lines.append("")

    # Stress
    if paths.stress_dir.exists():
        idx_st = paths.stress_dir / "_index.json"
        if idx_st.exists():
            with idx_st.open("r", encoding="utf-8") as f:
                idx = json.load(f)
            lines.append("## First-principles stress test")
            lines.append("")
            lines.append(f"- N total: {idx['n_total']}")
            lines.append(f"- PASS_STRESS: {idx['n_pass_stress']}")
            lines.append(f"- Rejected: {idx['n_rejected']}")
            lines.append(f"- Verdict distribution: {idx['verdict_distribution']}")
            lines.append("")

    # Market
    if paths.market_dir.exists():
        idx_m = paths.market_dir / "_index.json"
        if idx_m.exists():
            with idx_m.open("r", encoding="utf-8") as f:
                idx = json.load(f)
            lines.append("## Market verifier")
            lines.append("")
            lines.append(f"- N total: {idx['n_total']}")
            lines.append(f"- SURVIVES_MARKET_CHECK: {idx['n_survives']}")
            lines.append(f"- Verdict distribution: {idx['verdict_distribution']}")
            lines.append(f"- Surviving IDs: {idx['surviving_ids']}")
            lines.append("")

    # Final candidates
    final_ids: List[str] = []
    if paths.market_dir.exists():
        idx_m = paths.market_dir / "_index.json"
        if idx_m.exists():
            with idx_m.open("r", encoding="utf-8") as f:
                final_ids = json.load(f).get("surviving_ids", [])
    lines.append("## Final paradigm-shift candidates")
    lines.append("")
    if not final_ids:
        lines.append("None. (Run 1 expectation: 0 survivors on academic transcripts.)")
        lines.append("")
        lines.append("This is mechanism validation only. See `design/paradigm_shift_finder_v1.md` §8 MV-1..MV-5.")
    else:
        for cid in final_ids:
            cp = paths.market_dir / f"{cid}.json"
            if cp.exists():
                with cp.open("r", encoding="utf-8") as f:
                    c = json.load(f)
                lines.append(f"### {cid}")
                lines.append("")
                lines.append(f"- Operator: {c.get('combination_operator')}")
                lines.append(f"- Atoms: {', '.join(c.get('combined_atom_ids', []))}")
                lines.append(f"- Claim: {c.get('claim', '')[:600]}")
                lines.append(f"- Validity hypothesis: {c.get('first_principles_validity_hypothesis', '')[:400]}")
                lines.append("")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Honest acknowledgment")
    lines.append("")
    lines.append("- First-principles RAG check reduces hallucination ~50-70%, not 100%.")
    lines.append("- Impact-score classifier needs 10+ runs (50+ candidates, 10-20 labels) to become meaningful.")
    lines.append("- Cross-field analogy may produce surface metaphor (R279 risk).")
    lines.append("- Tech-leader vision content overlaps Claude's training corpus.")
    lines.append("- Run 1 on academic transcripts is mechanism validation only.")
    lines.append("")

    paths.summary_path.write_text("\n".join(lines), encoding="utf-8")


def run(
    manifest_in_path: Path,
    run_dir: Path,
    run_id: str = "run_001",
    resume_from: Optional[str] = None,
    max_per_operator: int = 5,
    require_cross_transcript: bool = True,
    label_top_k: int = 3,
):
    paths = build_paths(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "audit").mkdir(parents=True, exist_ok=True)

    # Resume gating: skip stages whose primary output already exists
    resume_idx = 0
    if resume_from:
        resume_idx = STAGES.index(resume_from)

    # ---- Stage: manifest ----
    if resume_idx <= STAGES.index("manifest") and not stage_complete(paths.manifest_path):
        print(f"[STAGE manifest] writing {paths.manifest_path}")
        write_manifest(manifest_in_path, paths.manifest_path)
    with paths.manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    # ---- Stage: snippets ----
    if resume_idx <= STAGES.index("snippets"):
        complete = paths.snippets_root.exists() and any(
            d.is_dir() and any(d.glob("snippet_S*.json"))
            for d in paths.snippets_root.iterdir()
            if d.is_dir() and d.name != "_flat"
        )
        if not complete:
            print(f"[STAGE snippets] decomposing transcripts into {paths.snippets_root}")
            run_snippets_stage(manifest, paths.snippets_root)
        else:
            print("[STAGE snippets] already complete, skipping")
    flat_snippets = flatten_snippets(paths.snippets_root)

    # ---- Stage: atoms_tari (cross-reference; reuse TARI extractor) ----
    if resume_idx <= STAGES.index("atoms_tari") and not stage_complete(paths.atoms_tari_dir):
        print(f"[STAGE atoms_tari] extracting TARI atoms into {paths.atoms_tari_dir}")
        # TARI's extract_all globs `snippet_S*.json`; our flatten produces
        # `snippet_<tid>_<sid>.json`. Iterate per transcript subdir to bypass.
        for tdir in sorted(paths.snippets_root.iterdir()):
            if not tdir.is_dir() or tdir.name == "_flat":
                continue
            extract_all(tdir, paths.atoms_tari_dir, append=True)

    # ---- Stage: atoms_paradigm ----
    if resume_idx <= STAGES.index("atoms_paradigm") and not stage_complete(paths.atoms_paradigm_dir):
        print(f"[STAGE atoms_paradigm] extracting paradigm atoms into {paths.atoms_paradigm_dir}")
        date_map = {t["id"]: t.get("approx_date") for t in manifest.get("transcripts", [])}
        extract_all_paradigm_atoms(flat_snippets, paths.atoms_paradigm_dir, transcript_date_map=date_map)

    # ---- Stage: candidates ----
    if resume_idx <= STAGES.index("candidates") and not stage_complete(paths.candidates_dir):
        print(f"[STAGE candidates] running typed-combinator brainstorm into {paths.candidates_dir}")
        brainstorm_paradigm_candidates(
            paths.atoms_paradigm_dir, paths.candidates_dir,
            run_id=run_id,
            max_per_operator=max_per_operator,
            require_cross_transcript=require_cross_transcript,
        )

    # ---- Stage: audit ----
    if resume_idx <= STAGES.index("audit") and not paths.audit_path.exists():
        print(f"[STAGE audit] running self_model_audit into {paths.audit_path}")
        # Extend TARI's VALID_OPERATORS to include paradigm operators so the Q2
        # check accepts our 4 typed combinators. TARI's audit otherwise works
        # unchanged: Q1 atom existence + Q3 verbatim quote presence.
        import self_model_audit as sma
        from analogy_engine import VALID_TYPED_COMBINATORS
        for op in VALID_TYPED_COMBINATORS:
            sma.VALID_OPERATORS.add(op)

        # Build per-transcript-id path dict for multi-transcript audit
        tpath_map = {t["id"]: Path(t["path"]) for t in manifest.get("transcripts", [])}
        sma.audit_all(paths.candidates_dir, paths.atoms_paradigm_dir,
                      tpath_map, paths.audit_path)

    # ---- Stage: scored ----
    if resume_idx <= STAGES.index("scored") and not stage_complete(paths.scored_dir):
        print(f"[STAGE scored] scoring with impact_filter into {paths.scored_dir}")
        weights_path = THIS_DIR / "impact_filter_weights.json"
        score_all_candidates(paths.candidates_dir, paths.scored_dir,
                             weights_path=weights_path if weights_path.exists() else None)

    # ---- Stage: stress ----
    if resume_idx <= STAGES.index("stress") and not stage_complete(paths.stress_dir):
        print(f"[STAGE stress] running first-principles stress test into {paths.stress_dir}")
        cache = load_search_cache(paths.search_cache_path)
        framing_cache = load_framing_cache(paths.framing_cache_path)
        def search_fn(q: str):
            return cache.get(q, [])
        stress_test_all(paths.scored_dir, paths.stress_dir,
                        search_fn=search_fn,
                        framing_answers_map=framing_cache)

    # ---- Stage: market ----
    if resume_idx <= STAGES.index("market") and not stage_complete(paths.market_dir):
        print(f"[STAGE market] running market verifier into {paths.market_dir}")
        cache = load_search_cache(paths.search_cache_path)
        def search_fn(q: str):
            return cache.get(q, [])
        verify_all(paths.stress_dir, paths.market_dir, search_fn=search_fn)

    # ---- Stage: label ----
    if resume_idx <= STAGES.index("label") and not paths.label_prompt_path.exists():
        print(f"[STAGE label] writing labeling prompt to {paths.label_prompt_path}")
        # Source from market_dir (final pipeline output) if it has anything,
        # else from scored_dir
        src = paths.market_dir if (paths.market_dir / "_index.json").exists() else paths.scored_dir
        candidates = []
        for cp in sorted(src.glob("CAND_*.json")):
            with cp.open("r", encoding="utf-8") as f:
                candidates.append(json.load(f))
        if not candidates and paths.scored_dir.exists():
            for cp in sorted(paths.scored_dir.glob("CAND_*.json")):
                with cp.open("r", encoding="utf-8") as f:
                    candidates.append(json.load(f))
        prompt = build_label_prompt(candidates, run_id=run_id, top_k=label_top_k)
        paths.label_prompt_path.write_text(prompt, encoding="utf-8")

    # ---- Stage: summary ----
    if resume_idx <= STAGES.index("summary"):
        print(f"[STAGE summary] writing {paths.summary_path}")
        write_summary(paths, manifest, run_id)

    print("\n=== Run complete ===")
    print(f"Output directory: {paths.run_dir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path,
                    help="Input manifest JSON (see paradigm_shift/runs/run_001/manifest.json)")
    ap.add_argument("--run_dir", required=True, type=Path)
    ap.add_argument("--run_id", default="run_001")
    ap.add_argument("--resume_from", choices=STAGES, default=None,
                    help="Skip stages before this one (assumes their outputs exist).")
    ap.add_argument("--max_per_operator", type=int, default=5)
    ap.add_argument("--allow_intra_transcript", action="store_true")
    ap.add_argument("--label_top_k", type=int, default=3)
    args = ap.parse_args()

    run(
        manifest_in_path=args.manifest,
        run_dir=args.run_dir,
        run_id=args.run_id,
        resume_from=args.resume_from,
        max_per_operator=args.max_per_operator,
        require_cross_transcript=not args.allow_intra_transcript,
        label_top_k=args.label_top_k,
    )


if __name__ == "__main__":
    main()
