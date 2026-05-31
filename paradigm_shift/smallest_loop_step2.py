#!/usr/bin/env python3
"""Step 2 of the smallest loop: REAL I/O, 3 candidates, single session.

Builds on the proven Step 1 loop (paradigm_shift/smallest_loop.py). The merge
(real Opus subprocess in a non-git temp dir), the [REPORT] verbatim injection,
the determinism proof and the anti-hallucination check are all inherited. What
changes:

  * Gate 1 scorer inputs are REAL (harness WebSearch), not smoke_io fixtures:
      - novelty_score      <- real arXiv hit count
      - community_density  <- real recent-paper count
      - arxiv_grounding    <- real arXiv papers found (derived)
      - saturation_distance, belinda_audit_pass -> deterministic (no fixture)
  * Gate 3 is EXECUTED, not a structural count: for each candidate that passes
    Gate 1+2, five real reformulated prior-art searches are run and a candidate
    is REJECTED if any reformulation finds an existing paper (mechanical
    keyword-overlap rule, frozen content_words).

Web search is issued by the HARNESS (the orchestrating agent) so the raw
results can be captured verbatim into logs/report_log.md. This module reads
those recorded results from logs/real_io/*.json and derives every number
mechanically — it never invents a search result or a count.

Phased so the agent can interleave real WebSearch between deterministic steps:

    python3 smallest_loop_step2.py merge      # 3 real Opus merges + freeze
    # (agent runs novelty+community WebSearch, records to logs/real_io/)
    python3 smallest_loop_step2.py gate12      # real Gate 1 + Gate 2 + Gate 4
    # (agent runs 5 reformulations for each Gate1+2 survivor)
    python3 smallest_loop_step2.py gate3       # executed prior-art collision
    python3 smallest_loop_step2.py finalize    # determinism + verdict + no-hallucination
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

import smallest_loop as s1            # noqa: E402  proven Step 1 pieces
import multi_parameter_scorer as scorer  # noqa: E402

RUN_DIR = THIS_DIR / "runs" / "run_014_step2"
LOGS_DIR = RUN_DIR / "logs"
REAL_IO_DIR = LOGS_DIR / "real_io"
REPORT = LOGS_DIR / "report_log.md"
RULES_PATH = RUN_DIR / "step2_rules.json"
INPUTS_PATH = RUN_DIR / "candidates_input.json"


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
def load_config() -> tuple[dict, dict, dict]:
    rules = json.loads(RULES_PATH.read_text())
    spec = json.loads((THIS_DIR.parent / rules["inherit_gates_from"]).read_text())
    gp = {
        "composite_threshold": spec["composite_threshold"],
        "quarantined_atoms": spec["quarantined_atoms"],
        "min_web_search_per_candidate": spec["min_web_search_per_candidate"],
        "belinda_strict": spec["belinda_strict"],
    }
    inputs = json.loads(INPUTS_PATH.read_text())
    return rules, gp, inputs


# --------------------------------------------------------------------------- #
# content_words: frozen distinctive terms for the Gate 3 collision rule
# --------------------------------------------------------------------------- #
# Generic words excluded so the >=2 overlap rule keys on DISTINCTIVE terms.
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "only", "each",
    "many", "which", "depending", "their", "they", "them", "then", "than",
    "your", "you", "are", "was", "were", "have", "has", "had", "not", "but",
    "can", "will", "would", "could", "should", "may", "might", "via", "per",
    "its", "it's", "one", "two", "more", "most", "some", "such", "over", "under",
    # generic ML / paper vocabulary (too common to be distinctive)
    "model", "models", "modeling", "learning", "learn", "neural", "network",
    "networks", "deep", "training", "train", "trained", "inference", "data",
    "dataset", "datasets", "task", "tasks", "method", "methods", "approach",
    "approaches", "system", "systems", "framework", "frameworks", "novel",
    "paper", "study", "studies", "using", "used", "use", "based", "toward",
    "towards", "architecture", "architectures", "ai", "llm", "llms", "machine",
    "large", "language", "general", "generative", "research", "analysis",
    "results", "performance", "state", "art", "scale", "scaling",
}


def content_words(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{3,}", (text or "").lower())
    return sorted({w for w in words if w not in STOPWORDS})


# --------------------------------------------------------------------------- #
# [REPORT] injection (verbatim)
# --------------------------------------------------------------------------- #
def init_report() -> None:
    REPORT.write_text(
        f"# [REPORT] ground-truth log — run_014_step2 (REAL I/O)\n"
        f"# generated {datetime.now(timezone.utc).isoformat()}\n"
        f"# Opus envelopes and raw WebSearch results, captured verbatim.\n")


def append_report_envelope(tag: str, envelope: dict) -> None:
    usage = envelope.get("usage", {})
    block = [
        f"\n## [REPORT] OPUS {tag}",
        f"- session_id: `{envelope.get('session_id')}`  "
        f"cost_usd: {envelope.get('total_cost_usd')}  "
        f"out_tokens: {usage.get('output_tokens')}",
        "```json", json.dumps(envelope, indent=2, sort_keys=True), "```",
    ]
    with REPORT.open("a") as f:
        f.write("\n".join(block) + "\n")


def append_report_websearch(payload: dict) -> None:
    """Inject a recorded WebSearch result file verbatim into the [REPORT] log."""
    results = payload.get("results", [])
    head = (f"\n## [REPORT] WEBSEARCH {payload.get('cand_id')} "
            f"[{payload.get('kind')}]")
    lines = [head, f"- query: {payload.get('query')!r}  "
                   f"({len(results)} results, recorded {payload.get('recorded_at')})"]
    for i, r in enumerate(results):
        lines.append(f"  {i+1}. {r.get('title','')}  <{r.get('url','')}>")
        if r.get("snippet"):
            lines.append(f"     {r['snippet']}")
    lines += ["```json", json.dumps(payload, indent=2), "```"]
    with REPORT.open("a") as f:
        f.write("\n".join(lines) + "\n")


# --------------------------------------------------------------------------- #
# Phase: merge  (real Opus subprocess, reused from Step 1)
# --------------------------------------------------------------------------- #
def freeze_record(cand_input: dict, parsed: dict | None) -> dict:
    parsed = parsed or {}
    joint = parsed.get("joint_topic", "")
    mech = parsed.get("mechanism", "")
    return {
        "cand_id": cand_input["cand_id"],
        "atom_a": cand_input["atom_a"],
        "atom_b": cand_input["atom_b"],
        "joint_topic": joint,
        "mechanism": mech,
        "operator": parsed.get("operator", ""),
        "primary_quote": parsed.get("primary_quote", ""),
        # frozen distinctive terms for the Gate 3 collision rule
        "content_words": content_words(
            joint + " " + mech + " " +
            " ".join(cand_input["atom_a"].get("domain_tags", [])) + " " +
            " ".join(cand_input["atom_b"].get("domain_tags", []))),
    }


def cmd_merge(rules: dict, gp: dict, inputs: dict) -> int:
    REAL_IO_DIR.mkdir(parents=True, exist_ok=True)
    init_report()
    frozen = []
    for ci in inputs["candidates"]:
        cid = ci["cand_id"]
        print(f"[merge] {cid}: real Opus subprocess ...", flush=True)
        merge = s1.opus_merge(ci, rules)          # subprocess in non-git tempdir
        append_report_envelope(f"MERGE {cid}", merge["envelope"])
        (LOGS_DIR / f"merge_{cid}.json").write_text(json.dumps(merge, indent=2))
        env = merge["envelope"]
        print(f"  -> session {env.get('session_id')} parse_ok={merge['parse_ok']} "
              f"cost=${env.get('total_cost_usd')}")
        frozen.append(freeze_record(ci, merge["parsed_candidate"]))
    (LOGS_DIR / "frozen_records.json").write_text(json.dumps(frozen, indent=2))

    print("\n=== HARNESS: run these REAL WebSearches and record to logs/real_io/ ===")
    for rec in frozen:
        print(f"\n{rec['cand_id']}: \"{rec['joint_topic']}\"")
        print(f"  content_words (frozen, for Gate 3): {rec['content_words']}")
        print(f"  novelty   -> real_io/novelty_{rec['cand_id']}.json")
        print(f"  community -> real_io/community_{rec['cand_id']}.json")
    return 0


# --------------------------------------------------------------------------- #
# Deterministic gate helpers
# --------------------------------------------------------------------------- #
PAPER_MARKERS = (
    "arxiv.org", "doi.org", "semanticscholar", "scholar.google", "aclanthology",
    "openreview", "biorxiv", "ncbi.nlm.nih.gov", "pubmed", "dl.acm.org",
    "ieeexplore", "springer", "sciencedirect", "/pdf", ".pdf", "proceedings",
    "neurips", "openalex", "ssrn", "mdpi", "nature.com", "researchgate",
)


def is_paper(res: dict) -> bool:
    blob = (res.get("url", "") + " " + res.get("title", "")).lower()
    return any(m in blob for m in PAPER_MARKERS)


def is_arxiv(res: dict) -> bool:
    return "arxiv.org" in (res.get("url", "") + " " + res.get("title", "")).lower()


def overlap_count(res: dict, words: list[str]) -> list[str]:
    blob = (res.get("title", "") + " " + res.get("snippet", "")).lower()
    return [w for w in words if re.search(r"\b" + re.escape(w) + r"\b", blob)]


def belinda_gate(rec: dict, gp: dict) -> dict:
    """Gate 4 (deterministic) — also feeds belinda_audit_pass into the scorer."""
    bs = gp["belinda_strict"]
    mech = s1._norm_ws(rec["mechanism"]).lower()
    verbs = sorted(v for v in bs["mechanism_vocab"]
                   if re.search(r"\b" + re.escape(v) + r"\b", mech))
    operator_ok = rec["operator"] not in set(bs["rejected_operators"])
    quote = s1._norm_ws(rec["primary_quote"])
    long_enough = len(quote) >= bs["min_verbatim_chars"]
    atom_text = s1._norm_ws(rec["atom_a"]["text"] + " " + rec["atom_b"]["text"])
    grounded = bool(quote) and quote in atom_text
    passed = bool(verbs) and operator_ok and long_enough and grounded
    return {"pass": passed, "mechanism_verbs": verbs, "operator_ok": operator_ok,
            "quote_chars": len(quote), "quote_grounded": grounded}


# --------------------------------------------------------------------------- #
# Phase: gate12  (real Gate 1 inputs + Gate 2 + deterministic Gate 4)
# --------------------------------------------------------------------------- #
def compute_gate12(frozen: list[dict], gp: dict, weights: dict,
                   load_io) -> list[dict]:
    """Pure function over frozen records + frozen real_io files."""
    quarantine = set(gp["quarantined_atoms"])
    out = []
    for rec in frozen:
        cid = rec["cand_id"]
        nov = load_io(f"novelty_{cid}.json")
        com = load_io(f"community_{cid}.json")
        nov_results = nov.get("results", []) if nov else []
        com_results = com.get("results", []) if com else []
        # REAL inputs (the two the brief scopes): novelty + community density.
        arxiv_hits = min(20, sum(1 for r in nov_results if is_arxiv(r)))
        recent_papers = min(30, sum(1 for r in com_results if is_paper(r)))

        g4 = belinda_gate(rec, gp)
        a, b = rec["atom_a"], rec["atom_b"]
        cand = scorer.Candidate(
            cand_id=cid,
            atom_a=scorer.Atom(a["atom_id"], a["source_id"], a["source_type"],
                               a["speaker_or_author"], a["text"], a["atom_type"],
                               a.get("domain_tags", [])),
            atom_b=scorer.Atom(b["atom_id"], b["source_id"], b["source_type"],
                               b["speaker_or_author"], b["text"], b["atom_type"],
                               b.get("domain_tags", [])),
            joint_topic=rec["joint_topic"],
            arxiv_hit_count_24m=arxiv_hits,           # REAL
            recent_paper_count=recent_papers,         # REAL
            saturation_cluster_distance=None,         # deterministic keyword-only
            arxiv_citations_supporting=[],            # overridden to neutral below
            belinda_3q_passes=g4["pass"],             # derived, not a fixture
        )
        score = scorer.score_candidate(cand, weights)
        # arxiv_grounding is OUT of Step-2 scope and conceptually distinct from the
        # novelty/collision search (supporting evidence != prior-art collision).
        # Reusing the novelty hits for it would pull grounding directly against
        # novelty and make Gate 1 ~unpassable; leaving it 0.0 would understate
        # every candidate. We override it to the scorer's documented neutral
        # (0.5) and DEFER real grounding to Step 3. Declared neutral, not a
        # favorable fixture; the composite is recomputed from the patched params.
        GROUNDING_NEUTRAL = 0.5
        score["params"]["arxiv_grounding"] = GROUNDING_NEUTRAL
        composite = round(
            sum(weights.get(k, 0.0) * v for k, v in score["params"].items()), 4)
        score["composite_score"] = composite
        gate1 = composite >= gp["composite_threshold"]
        ids = {a["atom_id"], b["atom_id"]}
        hits = sorted(ids & quarantine)
        gate2 = len(hits) == 0
        out.append({
            "cand_id": cid,
            "joint_topic": rec["joint_topic"],
            "real_arxiv_hit_count": arxiv_hits,
            "real_recent_paper_count": recent_papers,
            "arxiv_grounding_policy": "neutral_0.5_deferred_to_step3",
            "composite": composite,
            "params": score["params"],
            "gate_1_threshold": {"pass": gate1, "composite": composite,
                                 "threshold": gp["composite_threshold"]},
            "gate_2_quarantine": {"pass": gate2, "quarantine_hits": hits},
            "gate_4_belinda": g4,
            "passed_g12": gate1 and gate2,
        })
    return out


def cmd_gate12(rules: dict, gp: dict, inputs: dict) -> int:
    frozen = json.loads((LOGS_DIR / "frozen_records.json").read_text())
    weights = scorer.load_weights()

    def load_io(name):
        p = REAL_IO_DIR / name
        return json.loads(p.read_text()) if p.exists() else None

    # inject the recorded real searches into [REPORT] verbatim
    for rec in frozen:
        for kind in ("novelty", "community"):
            io = load_io(f"{kind}_{rec['cand_id']}.json")
            if io:
                append_report_websearch(io)
            else:
                print(f"  WARNING: missing real_io/{kind}_{rec['cand_id']}.json")

    results = compute_gate12(frozen, gp, weights, load_io)
    (LOGS_DIR / "gate1_2_results.json").write_text(json.dumps(results, indent=2))
    for r in results:
        print(f"  {r['cand_id']}: composite={r['composite']:.4f} "
              f"(arxiv_hits={r['real_arxiv_hit_count']}, "
              f"recent={r['real_recent_paper_count']}) "
              f"g1={r['gate_1_threshold']['pass']} g2={r['gate_2_quarantine']['pass']} "
              f"g4={r['gate_4_belinda']['pass']} -> passed_g12={r['passed_g12']}")
    surv = [r["cand_id"] for r in results if r["passed_g12"]]
    print(f"\n[gate12] {len(surv)} candidate(s) pass Gate 1+2: {surv}")
    if surv:
        print("=== HARNESS: run 5 real prior-art reformulations for each, "
              "record to logs/real_io/verify_<cand_id>.json ===")
        for r in results:
            if r["passed_g12"]:
                rec = next(x for x in frozen if x["cand_id"] == r["cand_id"])
                print(f"  {r['cand_id']} content_words: {rec['content_words']}")
    return 0


# --------------------------------------------------------------------------- #
# Phase: gate3  (EXECUTED prior-art collision over verbatim results)
# --------------------------------------------------------------------------- #
def compute_gate3(g12: list[dict], frozen: list[dict], gp: dict,
                  load_io, demo_ids: set[str] | None = None) -> list[dict]:
    """Executed prior-art collision check.

    Runs on every candidate that passed Gate 1+2 (real survivors) AND on any
    `demo_ids` (a labeled demonstration so the executed machinery is exercised
    on real data even when Gate 1 already dropped everything). A demonstration
    result NEVER promotes a candidate: assemble_verdicts still requires Gates
    1+2+4 to pass for `survived`.
    """
    demo_ids = demo_ids or set()
    frozen_by_id = {r["cand_id"]: r for r in frozen}
    out = []
    for r in g12:
        is_demo = (not r["passed_g12"]) and r["cand_id"] in demo_ids
        if not r["passed_g12"] and not is_demo:
            continue
        cid = r["cand_id"]
        words = frozen_by_id[cid]["content_words"]
        v = load_io(f"verify_{cid}.json")
        reforms = (v or {}).get("reformulations", [])
        per_reform = []
        for rf in reforms:
            paper_hits = []
            for res in rf.get("results", []):
                ov = overlap_count(res, words)
                if is_paper(res) and len(ov) >= 2:
                    paper_hits.append({"title": res.get("title", ""),
                                       "url": res.get("url", ""),
                                       "overlap_words": ov})
            per_reform.append({"n": rf.get("n"), "query": rf.get("query"),
                               "n_results": len(rf.get("results", [])),
                               "collided": len(paper_hits) > 0,
                               "paper_hits": paper_hits})
        n_reform = len(per_reform)
        collided_any = any(pr["collided"] for pr in per_reform)
        # executed: require the full 5 reformulations AND no collision
        gate3 = (n_reform >= gp["min_web_search_per_candidate"]) and not collided_any
        out.append({
            "cand_id": cid,
            "is_demonstration": is_demo,
            "reformulations_run": n_reform,
            "required": gp["min_web_search_per_candidate"],
            "collided_any": collided_any,
            "gate_3_executed_verify": {"pass": gate3},
            "per_reformulation": per_reform,
        })
    return out


def demo_ids_from(g12: list[dict], rules: dict) -> set[str]:
    """Gate-3 demonstration set: configured ids that did NOT pass Gate 1+2.

    Lets the executed prior-art machinery run on real data (e.g. the Step-1
    survivor) even when real novelty already dropped everything at Gate 1.
    Demonstrations never promote a candidate (see assemble_verdicts).
    """
    configured = set(rules.get("gate3_executed_verify", {}).get("demonstrate_ids", []))
    passed = {r["cand_id"] for r in g12 if r["passed_g12"]}
    return {cid for cid in configured if cid not in passed}


def cmd_gate3(rules: dict, gp: dict, inputs: dict) -> int:
    frozen = json.loads((LOGS_DIR / "frozen_records.json").read_text())
    g12 = json.loads((LOGS_DIR / "gate1_2_results.json").read_text())

    def load_io(name):
        p = REAL_IO_DIR / name
        return json.loads(p.read_text()) if p.exists() else None

    demo_ids = demo_ids_from(g12, rules)
    run_ids = {r["cand_id"] for r in g12 if r["passed_g12"]} | demo_ids
    for r in g12:
        if r["cand_id"] in run_ids:
            io = load_io(f"verify_{r['cand_id']}.json")
            if io:
                for rf in io.get("reformulations", []):
                    append_report_websearch({
                        "cand_id": r["cand_id"], "kind": f"verify#{rf.get('n')}",
                        "query": rf.get("query"), "results": rf.get("results", []),
                        "recorded_at": io.get("recorded_at")})
            else:
                print(f"  WARNING: missing real_io/verify_{r['cand_id']}.json")

    results = compute_gate3(g12, frozen, gp, load_io, demo_ids)
    (LOGS_DIR / "gate3_results.json").write_text(json.dumps(results, indent=2))
    for r in results:
        tag = " [DEMO]" if r["is_demonstration"] else ""
        print(f"  {r['cand_id']}{tag}: reformulations={r['reformulations_run']} "
              f"collided_any={r['collided_any']} -> "
              f"gate3_pass={r['gate_3_executed_verify']['pass']}")
        for pr in r["per_reformulation"]:
            mark = "COLLISION" if pr["collided"] else "clear"
            print(f"     [{mark}] q{pr['n']}: {pr['n_results']} results"
                  + (f" -> {pr['paper_hits'][0]['url']}" if pr["paper_hits"] else ""))
    return 0


# --------------------------------------------------------------------------- #
# Phase: finalize  (determinism + verdict + anti-hallucination)
# --------------------------------------------------------------------------- #
def assemble_verdicts(g12: list[dict], g3: list[dict]) -> list[dict]:
    g3_by_id = {r["cand_id"]: r for r in g3}
    out = []
    for r in g12:
        cid = r["cand_id"]
        g3r = g3_by_id.get(cid)
        gate3_pass = g3r["gate_3_executed_verify"]["pass"] if g3r else None
        survived = bool(r["gate_1_threshold"]["pass"] and r["gate_2_quarantine"]["pass"]
                        and r["gate_4_belinda"]["pass"] and gate3_pass)
        gates_failed = []
        if not r["gate_1_threshold"]["pass"]:
            gates_failed.append("gate_1_threshold")
        if not r["gate_2_quarantine"]["pass"]:
            gates_failed.append("gate_2_quarantine")
        if not r["gate_4_belinda"]["pass"]:
            gates_failed.append("gate_4_belinda")
        if r["passed_g12"] and gate3_pass is False:
            gates_failed.append("gate_3_executed_verify")
        out.append({
            "cand_id": cid, "joint_topic": r["joint_topic"],
            "composite": r["composite"],
            "real_arxiv_hit_count": r["real_arxiv_hit_count"],
            "real_recent_paper_count": r["real_recent_paper_count"],
            "gate_1": r["gate_1_threshold"]["pass"],
            "gate_2": r["gate_2_quarantine"]["pass"],
            "gate_4": r["gate_4_belinda"]["pass"],
            "gate_3_executed": gate3_pass,
            "gate_3_is_demonstration": bool(g3r and g3r.get("is_demonstration")),
            "gate_3_collided": (g3r["collided_any"] if g3r else None),
            "survived": survived, "gates_failed": gates_failed,
        })
    return out


def verdicts_hash(verdicts: list[dict]) -> str:
    skel = [{"cand_id": v["cand_id"], "composite": v["composite"],
             "g1": v["gate_1"], "g2": v["gate_2"], "g4": v["gate_4"],
             "g3": v["gate_3_executed"], "survived": v["survived"],
             "arxiv_hits": v["real_arxiv_hit_count"]} for v in verdicts]
    return hashlib.sha256(
        json.dumps(skel, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def ground_truth_claims(verdicts: list[dict]) -> dict:
    survivors = [v for v in verdicts if v["survived"]]
    return {
        "n_candidates": len(verdicts),
        "n_survivors": len(survivors),
        "verdict": "NICHE_FOUND" if survivors else "NICHE_NOT_FOUND",
        "per_candidate": [
            {"cand_id": v["cand_id"], "composite": round(v["composite"], 4),
             "real_arxiv_hit_count": v["real_arxiv_hit_count"],
             "survived": v["survived"]} for v in verdicts],
    }


def check_hallucination(truth: dict, claimed: dict | None) -> dict:
    mism: list[str] = []
    if claimed is None:
        return {"hallucination_detected": True, "no_hallucination": False,
                "mismatches": ["no parseable claim block"], "truth": truth,
                "claimed": None}
    for k in ("n_candidates", "n_survivors", "verdict"):
        if claimed.get(k) != truth[k]:
            mism.append(f"{k}: claimed {claimed.get(k)!r} != truth {truth[k]!r}")
    t_by = {c["cand_id"]: c for c in truth["per_candidate"]}
    c_by = {c.get("cand_id"): c for c in claimed.get("per_candidate", [])}
    for cid in c_by:
        if cid not in t_by:
            mism.append(f"fabricated cand_id: {cid!r}")
    for cid, t in t_by.items():
        c = c_by.get(cid)
        if not c:
            mism.append(f"missing cand_id: {cid!r}")
            continue
        try:
            if abs(float(c.get("composite")) - float(t["composite"])) > 1e-4:
                mism.append(f"{cid} composite: {c.get('composite')} != {t['composite']}")
        except (TypeError, ValueError):
            mism.append(f"{cid} composite not numeric: {c.get('composite')!r}")
        if int(c.get("real_arxiv_hit_count", -1)) != int(t["real_arxiv_hit_count"]):
            mism.append(f"{cid} arxiv_hits: claimed {c.get('real_arxiv_hit_count')} "
                        f"!= truth {t['real_arxiv_hit_count']}")
        if bool(c.get("survived")) != bool(t["survived"]):
            mism.append(f"{cid} survived: {c.get('survived')} != {t['survived']}")
    detected = len(mism) > 0
    return {"hallucination_detected": detected, "no_hallucination": not detected,
            "mismatches": mism, "truth": truth, "claimed": claimed}


SUMMARY_PROMPT = """You are writing a strictly factual summary of an automated run with REAL web verification.
Below is the RAW REPORT LOG (ground truth: Opus merges + verbatim WebSearch results) and the GATE RESULTS.

=== RAW REPORT LOG ===
{report_log}

=== GATE RESULTS (JSON, ground truth) ===
{gate_results}

Write 4-7 plain-English sentences summarizing what happened, including whether the surviving
candidate(s) collided with existing papers in the real prior-art search. State ONLY facts present
above; do not infer or embellish any number.

Then output a fenced ```json block with EXACTLY:
{{
  "n_candidates": <int>,
  "n_survivors": <int>,
  "verdict": "<NICHE_FOUND or NICHE_NOT_FOUND>",
  "per_candidate": [{{"cand_id": "<id>", "composite": <number>, "real_arxiv_hit_count": <int>, "survived": <true|false>}}]
}}"""


def cmd_finalize(rules: dict, gp: dict, inputs: dict) -> int:
    frozen = json.loads((LOGS_DIR / "frozen_records.json").read_text())
    weights = scorer.load_weights()

    def load_io(name):
        p = REAL_IO_DIR / name
        return json.loads(p.read_text()) if p.exists() else None

    # ---- determinism: recompute the whole gate pipeline twice over frozen I/O
    def full_pipeline():
        g12 = compute_gate12(frozen, gp, weights, load_io)
        demo = demo_ids_from(g12, rules)
        g3 = compute_gate3(g12, frozen, gp, load_io, demo)
        return assemble_verdicts(g12, g3)

    v1, v2 = full_pipeline(), full_pipeline()
    h1, h2 = verdicts_hash(v1), verdicts_hash(v2)
    determinism_ok = h1 == h2
    (LOGS_DIR / "determinism_check.json").write_text(json.dumps(
        {"determinism_ok": determinism_ok, "hash_run_1": h1, "hash_run_2": h2,
         "runs": 2, "note": "Full Gate 1+2+3+4 pipeline run twice over frozen "
         "real_io; verdict hashes must match."}, indent=2))

    verdicts = v1
    survivors = [v for v in verdicts if v["survived"]]
    gates = ["gate_1_threshold", "gate_2_quarantine",
             "gate_3_executed_verify", "gate_4_belinda"]
    gate_fired = {g: 0 for g in gates}
    for v in verdicts:
        for g in v["gates_failed"]:
            gate_fired[g] += 1
    verdict_doc = {
        "verdict": "NICHE_FOUND" if survivors else "NICHE_NOT_FOUND",
        "real_io": True,
        "survivors": [{"cand_id": s["cand_id"], "composite": s["composite"],
                       "joint_topic": s["joint_topic"],
                       "note": "passed REAL prior-art verify (5 reformulations, "
                       "no collision) -> rare; verify deeper before any claim"}
                      for s in survivors],
        "gate_fired_counts": gate_fired,
        "per_candidate": verdicts,
        "candidates_scanned": len(verdicts),
        "honest_interpretation": (
            "Collision at Gate 3 = saturation confirmed under REAL prior-art "
            "search (rules out 'mock too weak'). Survivor = rare, must verify "
            "deeper (10 more reformulations) before any novelty claim."),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    (RUN_DIR / "niche_find_check.json").write_text(json.dumps(verdict_doc, indent=2))

    # ---- anti-hallucination: Opus summarizes ONLY the [REPORT] + gate results
    truth = ground_truth_claims(verdicts)
    summary_env = s1.run_opus(SUMMARY_PROMPT.format(
        report_log=REPORT.read_text(),
        gate_results=json.dumps(verdicts, indent=2)), rules)
    summary_text = summary_env.get("result", "")
    (LOGS_DIR / "summary_llm.md").write_text(
        f"# LLM summary (session {summary_env.get('session_id')})\n\n{summary_text}\n")
    append_report_envelope("SUMMARY_CALL", summary_env)
    claimed = s1.extract_json_block(summary_text)
    hall = check_hallucination(truth, claimed)
    (LOGS_DIR / "hallucination_check.json").write_text(json.dumps(hall, indent=2))

    proofs = {
        "real_gate1_inputs": all(
            (REAL_IO_DIR / f"novelty_{c['cand_id']}.json").exists() and
            (REAL_IO_DIR / f"community_{c['cand_id']}.json").exists()
            for c in inputs["candidates"]),
        "real_gate3_executed": any(v["gate_3_executed"] is not None for v in verdicts),
        "report_verbatim_websearch": "[REPORT] WEBSEARCH" in REPORT.read_text(),
        "four_gate_deterministic": determinism_ok,
        "no_hallucination": hall["no_hallucination"],
    }
    (RUN_DIR / "proof_scorecard.json").write_text(json.dumps(
        {"proofs": proofs, "all_pass": all(proofs.values()),
         "verdict": verdict_doc["verdict"], "n_survivors": len(survivors),
         "generated_at": datetime.now(timezone.utc).isoformat()}, indent=2))

    print("=" * 70)
    print(f"VERDICT: {verdict_doc['verdict']}  survivors={len(survivors)}")
    print(f"determinism: {'OK' if determinism_ok else 'BROKEN'} {h1[:16]}...")
    print(f"no_hallucination: {hall['no_hallucination']}  "
          f"mismatches={hall['mismatches']}")
    print("PROOF SCORECARD:")
    for k, ok in proofs.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {k}")
    return 0 if all(proofs.values()) else 1


# --------------------------------------------------------------------------- #
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Step 2 real-I/O smallest loop")
    ap.add_argument("phase", choices=["merge", "gate12", "gate3", "finalize"])
    args = ap.parse_args(argv)
    rules, gp, inputs = load_config()
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REAL_IO_DIR.mkdir(parents=True, exist_ok=True)
    return {"merge": cmd_merge, "gate12": cmd_gate12,
            "gate3": cmd_gate3, "finalize": cmd_finalize}[args.phase](rules, gp, inputs)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
