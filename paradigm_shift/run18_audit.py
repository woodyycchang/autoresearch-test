#!/usr/bin/env python3
"""Run 18 AGENT 5 (reasoning-auditor).

Same deterministic, fully-visible audit as Run 17, over every reasoning_trace
from AGENT 1 (atom decomposition), AGENT 2 (per-atom saturation), AGENT 3 (merges),
AGENT 4 (verify + crosscheck). Core check (R10): where a trace's decision restates
a recorded structured fact (collision_found, mismatch_with_agent3, quote_verified,
or per-atom paper_hits vs the sparse threshold), the trace must AGREE with the data,
else it is a LOGIC BREAK.

Reads : run_018/logs/{atoms_reasoning,atom_search,candidates,verify,verify_reasoning,crosscheck}.json
Writes: run_018/logs/reasoning_audit.json
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).parent
RUN_DIR = THIS_DIR / "run_018"
LOGS = RUN_DIR / "logs"
RULES = json.loads((RUN_DIR / "run18_rules.json").read_text())
TRACE_FIELDS = RULES["reasoning_trace_schema"]["required_fields"]
SPARSE_THRESHOLD = RULES["sourcing_method"]["sparse_threshold"]

STOP = {
    "the", "and", "that", "this", "with", "from", "which", "into", "onto", "their",
    "they", "them", "then", "than", "what", "when", "whom", "whose", "have", "been",
    "were", "will", "would", "could", "should", "about", "there", "these", "those",
    "such", "each", "both", "some", "more", "most", "less", "very", "also", "only",
    "because", "since", "while", "where", "does", "doesn", "isn", "not", "over",
    "under", "between", "across", "toward", "without", "thing", "things", "step",
    "decision", "reasoning", "inputs", "seen", "trace", "atom", "candidate", "niche",
    "search", "query", "result", "results", "paper", "papers",
}
HEDGES = ["unsure", "unclear", "not sure", "hard to tell", "can't tell", "cannot tell",
          "uncertain", "speculative", "tentative", "i think", "i guess", "not certain",
          "no idea", "unknown whether", "might or might not", "possibly", "perhaps",
          "maybe", "might be", "may be", "could be", "not confident"]
NO_COLLISION = ["no collision", "no bridging", "no same-core", "no same core", "not occupied",
                "no prior art", "no prior-art", "novel", "no duplicate", "no overlap", "no paper",
                "no exact", "gap exists", "unoccupied", "no published", "no existing", "no fused",
                "no merged", "no single paper", "no direct"]
COLLISION = ["collision found", "collision exists", "already published", "prior art exists",
             "already exists", "is occupied", "duplicate found", "exact match", "same niche",
             "direct collision", "bridging paper found", "is published"]
CONFIRM = ["confirm", "agree", "concur", "uphold", "consistent with agent 3", "consistent with a3",
           "matches agent 3", "matches a3", "no mismatch", "upholds"]
DISPUTE = ["dispute", "disagree", "overturn", "overrule", "contradict", "mismatch",
           "differs from agent 3", "differs from a3", "reject agent", "refute"]
SPARSE_W = ["sparse", "rare", "few paper", "under-studied", "understudied", "obscure",
            "low volume", "low-volume", "thin", "scarce", "underexplored", "under-explored", "niche"]
DENSE_W = ["dense", "mature", "crowded", "saturated", "many paper", "well-studied", "well studied",
           "high volume", "high-volume", "heavily studied", "common", "popular", "ubiquitous"]


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def content_tokens(s):
    return {t for t in re.findall(r"[a-z][a-z\-]{3,}", s.lower()) if t not in STOP}


def overlap_score(decision, context):
    d = content_tokens(decision)
    return round(len(d & content_tokens(context)) / len(d), 3) if d else 0.0


def conf_level(s):
    m = re.search(r"\b(high|medium|low)\b", str(s).lower())
    return m.group(1) if m else None


def conf_has_rationale(s):
    s = norm(s)
    lvl = conf_level(s)
    if not lvl:
        return False
    return len(re.sub(r"\b" + lvl + r"\b", "", s, flags=re.I).strip(" -:;,.")) >= 8


def find_hedges(s):
    s = s.lower()
    return sorted({h for h in HEDGES if h in s})


def _has_any(text, phrases):
    t = text.lower()
    return [p for p in phrases if p in t]


def _two_sided(text, pos_words, neg_words, pos_label, neg_label):
    pos = _has_any(text, pos_words)
    neg = _has_any(text, neg_words)
    if pos and not neg:
        return pos_label, pos
    if neg and not pos:
        return neg_label, neg
    if pos and neg:
        return "ambiguous", pos + neg
    return None, []


def verify_polarity(text):
    return _two_sided(text, NO_COLLISION, COLLISION, "no_collision", "collision")


def confirm_polarity(text):
    text = re.sub(r"\b(no|without|zero|0)\s+mismatch(es)?\b", " agree ", text.lower())
    return _two_sided(text, CONFIRM, DISPUTE, "confirm", "dispute")


def sparse_polarity(text):
    return _two_sided(text, SPARSE_W, DENSE_W, "sparse", "dense")


def audit_one(trace, *, source, step_id, linked=None):
    linked = linked or {}
    tr = {f: norm(trace.get(f, "")) for f in TRACE_FIELDS} if isinstance(trace, dict) else {}
    flags = []
    missing = [f for f in TRACE_FIELDS if not tr.get(f)]
    complete = not missing
    if missing:
        flags.append(f"incomplete:missing={missing}")
    lvl = conf_level(tr.get("confidence", ""))
    conf_ok = bool(lvl) and conf_has_rationale(tr.get("confidence", ""))
    if not lvl:
        flags.append("confidence:no_level")
    elif not conf_ok:
        flags.append("confidence:missing_rationale")
    cbw = tr.get("could_be_wrong_if", "").lower()
    falsifiable = bool(cbw) and cbw not in {"nothing", "n/a", "na", "none", "-"} and len(cbw) >= 8
    if not falsifiable:
        flags.append("not_falsifiable")
    ctx = tr.get("inputs_seen", "") + " " + tr.get("reasoning", "")
    grounding = overlap_score(tr.get("decision", ""), ctx)
    if tr.get("decision") and grounding < 0.15:
        flags.append(f"low_inputs_grounding({grounding})")
    hedges = find_hedges(tr.get("reasoning", "") + " " + tr.get("confidence", ""))
    overconfident = (lvl == "high") and bool(hedges)
    if overconfident:
        flags.append(f"possible_overconfidence:hedges={hedges}")

    logic_break = False
    consistency = {"checked": False}
    dtext = tr.get("decision", "") + " " + tr.get("reasoning", "")
    if "collision_found" in linked:
        pol, ev = verify_polarity(dtext)
        consistency = {"checked": True, "kind": "verify_collision", "trace_polarity": pol,
                       "evidence": ev, "data_collision_found": linked["collision_found"]}
        if pol in ("no_collision", "collision"):
            if (pol == "no_collision") != (not bool(linked["collision_found"])):
                logic_break = True
                flags.append("LOGIC_BREAK:decision_contradicts_collision_data")
        else:
            consistency["note"] = "polarity_indeterminate (no break asserted)"
    elif "mismatch_with_agent3" in linked:
        pol, ev = confirm_polarity(dtext)
        consistency = {"checked": True, "kind": "crosscheck_confirm", "trace_polarity": pol,
                       "evidence": ev, "data_mismatch_with_agent3": linked["mismatch_with_agent3"]}
        if pol in ("confirm", "dispute"):
            if (pol == "confirm") != (not bool(linked["mismatch_with_agent3"])):
                logic_break = True
                flags.append("LOGIC_BREAK:decision_contradicts_crosscheck_data")
        else:
            consistency["note"] = "polarity_indeterminate (no break asserted)"
    elif "paper_hits" in linked:
        pol, ev = sparse_polarity(dtext)
        is_sparse = linked["paper_hits"] < SPARSE_THRESHOLD
        consistency = {"checked": True, "kind": "atom_sparsity", "trace_polarity": pol,
                       "evidence": ev, "data_paper_hits": linked["paper_hits"],
                       "sparse_threshold": SPARSE_THRESHOLD, "data_is_sparse": is_sparse}
        if pol in ("sparse", "dense"):
            if (pol == "sparse") != is_sparse:
                logic_break = True
                flags.append("LOGIC_BREAK:sparsity_label_contradicts_hit_count")
        else:
            consistency["note"] = "polarity_indeterminate (no break asserted)"
    elif "quote_verified_substring" in linked:
        consistency = {"checked": True, "kind": "merge_quote_context",
                       "data_quote_verified": linked["quote_verified_substring"],
                       "note": "merge decision is a niche (not boolean); quote grounding checked by MAIN Gate-4"}

    valid = complete and conf_ok and falsifiable and not logic_break
    audit_trace = {
        "step": f"audit {source} :: {step_id}",
        "inputs_seen": f"6 fields present={not missing}; confidence_level={lvl}; "
                       f"grounding_overlap={grounding}; linked_data={ {k: linked[k] for k in linked} }",
        "reasoning": "Applied 6 deterministic checks (completeness, confidence rationale, "
                     "falsifiability, inputs-grounding overlap, overconfidence-hedge, decision<->"
                     "recorded-data consistency). LOGIC BREAK only when detected polarity contradicts data.",
        "decision": ("LOGIC_BREAK" if logic_break else ("VALID" if valid else "FLAGGED_NONFATAL")),
        "confidence": ("high - deterministic checks over committed JSON" if consistency.get("trace_polarity") not in (None, "ambiguous")
                       or not consistency.get("checked")
                       else "medium - prose polarity indeterminate, so data-consistency could not fire; format checks still deterministic"),
        "could_be_wrong_if": "the polarity phrase-lists miss a paraphrase (false negative) or the "
                             "grounding overlap penalizes a correct but differently-worded short decision.",
    }
    return {"trace_id": step_id, "source_agent": source, "step": tr.get("step", ""),
            "complete": complete, "missing_fields": missing, "confidence_level": lvl,
            "confidence_wellformed": conf_ok, "falsifiable": falsifiable,
            "inputs_grounding_overlap": grounding, "overconfident": overconfident,
            "hedges_found": hedges, "decision_data_consistency": consistency,
            "logic_break": logic_break, "flags": flags,
            "verdict": audit_trace["decision"], "audit_reasoning_trace": audit_trace}


def collect():
    items = []
    p = LOGS / "atoms_reasoning.json"
    if p.exists():
        ar = json.loads(p.read_text())
        if isinstance(ar.get("overall_trace"), dict):
            items.append({"trace": ar["overall_trace"], "source": "AGENT_1_decomposer", "step_id": "atoms.overall"})
        for at in ar.get("atom_traces", []):
            items.append({"trace": at.get("reasoning_trace", {}), "source": "AGENT_1_decomposer",
                          "step_id": f"atom.{at.get('atom_id', '?')}"})
    p = LOGS / "atom_search.json"
    if p.exists():
        for a in json.loads(p.read_text()).get("atoms", []):
            if isinstance(a.get("reasoning_trace"), dict):
                items.append({"trace": a["reasoning_trace"], "source": "AGENT_2_atom_search",
                              "step_id": f"atomsearch.{a.get('atom_id', '?')}",
                              "linked": {"paper_hits": a.get("paper_hits")}})
    p = LOGS / "candidates.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            items.append({"trace": c.get("reasoning_trace", {}), "source": "AGENT_3_merger",
                          "step_id": f"merge.{c['cand_id']}",
                          "linked": {"quote_verified_substring": c.get("quote_verified_substring")}})
    coll = {}
    pv = LOGS / "verify.json"
    if pv.exists():
        for c in json.loads(pv.read_text()).get("candidates", []):
            coll[c["cand_id"]] = c.get("collision_found")
    p = LOGS / "verify_reasoning.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            cid = c.get("cand_id")
            if isinstance(c.get("verdict_trace"), dict):
                items.append({"trace": c["verdict_trace"], "source": "AGENT_4_verifier",
                              "step_id": f"verify.verdict.{cid}", "linked": {"collision_found": coll.get(cid)}})
            for rt in c.get("reformulation_traces", []):
                items.append({"trace": rt.get("reasoning_trace", {}), "source": "AGENT_4_verifier",
                              "step_id": f"verify.reform.{cid}.n{rt.get('n', '?')}"})
    p = LOGS / "crosscheck.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            items.append({"trace": c.get("reasoning_trace", {}), "source": "AGENT_4_crosschecker",
                          "step_id": f"crosscheck.{c['cand_id']}",
                          "linked": {"mismatch_with_agent3": c.get("mismatch_with_agent3")}})
    return items


def main():
    audits = [audit_one(it["trace"], source=it["source"], step_id=it["step_id"], linked=it.get("linked"))
              for it in collect()]
    by_agent = {}
    for a in audits:
        d = by_agent.setdefault(a["source_agent"], {"traces": 0, "complete": 0, "flagged": 0, "logic_breaks": 0})
        d["traces"] += 1
        d["complete"] += int(a["complete"])
        d["flagged"] += int(bool(a["flags"]))
        d["logic_breaks"] += int(a["logic_break"])
    summary = {"total_traces_audited": len(audits), "all_complete": all(a["complete"] for a in audits),
               "n_complete": sum(a["complete"] for a in audits),
               "n_flagged_nonfatal": sum(1 for a in audits if a["flags"] and not a["logic_break"]),
               "n_logic_breaks": sum(a["logic_break"] for a in audits),
               "logic_break_trace_ids": [a["trace_id"] for a in audits if a["logic_break"]],
               "by_agent": by_agent,
               "consistency_checks_fired": sum(1 for a in audits if a["decision_data_consistency"].get("checked"))}
    out = {"run_id": "run_018", "agent": "5_reasoning_auditor",
           "audited_at": datetime.now(timezone.utc).isoformat(),
           "method": "deterministic rule-based audit over committed reasoning_traces; rules in "
                     "run18_rules; auditor emits its own reasoning_trace per audited trace (not a black box).",
           "summary": summary, "audits": audits}
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "reasoning_audit.json").write_text(json.dumps(out, indent=2))
    print(f"[audit] {summary['total_traces_audited']} traces; complete={summary['n_complete']} "
          f"flagged_nonfatal={summary['n_flagged_nonfatal']} LOGIC_BREAKS={summary['n_logic_breaks']} "
          f"consistency_fired={summary['consistency_checks_fired']}")
    for a in audits:
        mark = "BREAK" if a["logic_break"] else ("FLAG " if a["flags"] else "ok   ")
        print(f"  [{mark}] {a['source_agent']:<22} {a['trace_id']:<26} ground={a['inputs_grounding_overlap']} "
              f"{('; '.join(a['flags']) if a['flags'] else '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
