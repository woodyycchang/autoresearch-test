#!/usr/bin/env python3
"""Run 17 AGENT 5 (reasoning-auditor) -- NEW ROLE.

Reads EVERY reasoning_trace emitted by AGENT 1-4 and audits each one with
DETERMINISTIC, fully-visible rules (so the auditor itself is not a black box).
For each trace it asks: are all six fields present? does the confidence carry a
rationale? is the claim falsifiable? does the decision share vocabulary with the
stated inputs (or is it a leap)? is confidence=high contradicted by hedging? and
-- the core check (R10) -- where a trace's decision restates a STRUCTURED fact
recorded elsewhere (collision_found, mismatch_with_agent3, quote_verified), does
the trace AGREE with that fact, or is it a LOGIC BREAK (reasoning != decision)?

Tools: Bash only (pure logic over committed JSON). No web, no LLM -- the audit
rules are visible Python, auditable line by line.

Reads : paradigm_shift/run_017/logs/{atoms_reasoning,candidates,verify,
        verify_reasoning,crosscheck}.json
Writes: paradigm_shift/run_017/logs/reasoning_audit.json

Usage: python3 paradigm_shift/run17_audit.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).parent
LOGS = THIS_DIR / "run_017" / "logs"
RULES = json.loads((THIS_DIR / "run_017" / "run17_rules.json").read_text())
TRACE_FIELDS = RULES["reasoning_trace_schema"]["required_fields"]

STOP = {
    "the", "and", "that", "this", "with", "from", "which", "into", "onto", "their",
    "they", "them", "then", "than", "what", "when", "whom", "whose", "have", "been",
    "were", "will", "would", "could", "should", "about", "would", "there", "these",
    "those", "such", "each", "both", "some", "more", "most", "less", "very", "also",
    "only", "because", "since", "while", "where", "does", "doesn", "isn", "not",
    "would", "into", "over", "under", "between", "across", "toward", "without",
    "thing", "things", "step", "decision", "reasoning", "inputs", "seen", "trace",
    "atom", "candidate", "niche", "search", "query", "result", "results", "paper",
    "papers",
}
HEDGES = [
    "unsure", "unclear", "not sure", "hard to tell", "can't tell", "cannot tell",
    "uncertain", "speculative", "tentative", "i think", "i guess", "not certain",
    "no idea", "unknown whether", "might or might not", "possibly", "perhaps",
    "maybe", "might be", "may be", "could be", "not confident",
]
# decision polarity for verify-style (collision / no-collision)
NO_COLLISION = [
    "no collision", "no bridging", "no same-core", "no same core", "not occupied",
    "no prior art", "no prior-art", "novel", "no duplicate", "no overlap", "no paper",
    "no exact", "gap exists", "unoccupied", "no published", "no existing",
    "no fused", "no merged", "no single paper", "no direct",
]
COLLISION = [
    "collision found", "collision exists", "already published", "prior art exists",
    "already exists", "is occupied", "duplicate found", "exact match", "same niche",
    "direct collision", "bridging paper found", "is published", "already studied combined",
]
CONFIRM = ["confirm", "agree", "concur", "uphold", "consistent with agent 3",
           "consistent with a3", "matches agent 3", "matches a3", "no mismatch", "upholds"]
DISPUTE = ["dispute", "disagree", "overturn", "overrule", "contradict", "mismatch",
           "differs from agent 3", "differs from a3", "reject agent", "refute"]


def norm(s) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip()


def content_tokens(s: str) -> set[str]:
    toks = re.findall(r"[a-z][a-z\-]{3,}", s.lower())
    return {t for t in toks if t not in STOP}


def overlap_score(decision: str, context: str) -> float:
    d = content_tokens(decision)
    if not d:
        return 0.0
    c = content_tokens(context)
    return round(len(d & c) / len(d), 3)


def conf_level(s: str):
    m = re.search(r"\b(high|medium|low)\b", str(s).lower())
    return m.group(1) if m else None


def conf_has_rationale(s: str) -> bool:
    s = norm(s)
    lvl = conf_level(s)
    if not lvl:
        return False
    rest = re.sub(r"\b" + lvl + r"\b", "", s, flags=re.I).strip(" -:;,.")
    return len(rest) >= 8  # a real clause, not just the bare level word


def find_hedges(s: str) -> list[str]:
    s = s.lower()
    return sorted({h for h in HEDGES if h in s})


def _has_any(text: str, phrases) -> list[str]:
    t = text.lower()
    return [p for p in phrases if p in t]


def verify_polarity(text: str):
    """Return ('no_collision'|'collision'|None, evidence)."""
    neg = _has_any(text, NO_COLLISION)
    pos = _has_any(text, COLLISION)
    if neg and not pos:
        return "no_collision", neg
    if pos and not neg:
        return "collision", pos
    if neg and pos:
        return "ambiguous", neg + pos
    return None, []


def confirm_polarity(text: str):
    conf = _has_any(text, CONFIRM)
    disp = _has_any(text, DISPUTE)
    if conf and not disp:
        return "confirm", conf
    if disp and not conf:
        return "dispute", disp
    if conf and disp:
        return "ambiguous", conf + disp
    return None, []


def audit_one(trace: dict, *, source: str, step_id: str, linked: dict | None = None) -> dict:
    """Apply every deterministic check to one reasoning_trace."""
    linked = linked or {}
    tr = {f: norm(trace.get(f, "")) for f in TRACE_FIELDS} if isinstance(trace, dict) else {}
    flags: list[str] = []

    # 1. completeness
    missing = [f for f in TRACE_FIELDS if not tr.get(f)]
    complete = not missing
    if missing:
        flags.append(f"incomplete:missing={missing}")

    # 2. confidence well-formed
    lvl = conf_level(tr.get("confidence", ""))
    conf_ok = bool(lvl) and conf_has_rationale(tr.get("confidence", ""))
    if not lvl:
        flags.append("confidence:no_level")
    elif not conf_ok:
        flags.append("confidence:missing_rationale")

    # 3. falsifiability
    cbw = tr.get("could_be_wrong_if", "").lower()
    falsifiable = bool(cbw) and cbw not in {"nothing", "n/a", "na", "none", "-"} and len(cbw) >= 8
    if not falsifiable:
        flags.append("not_falsifiable")

    # 4. inputs grounding (records overlap; low => possible leap, soft signal)
    ctx = tr.get("inputs_seen", "") + " " + tr.get("reasoning", "")
    grounding = overlap_score(tr.get("decision", ""), ctx)
    if tr.get("decision") and grounding < 0.15:
        flags.append(f"low_inputs_grounding({grounding})")

    # 5. overconfidence (hedges in reasoning/confidence while confidence=high)
    hedges = find_hedges(tr.get("reasoning", "") + " " + tr.get("confidence", ""))
    overconfident = (lvl == "high") and bool(hedges)
    if overconfident:
        flags.append(f"possible_overconfidence:hedges={hedges}")

    # 6. decision<->data consistency  ==> the core LOGIC BREAK check (R10)
    logic_break = False
    consistency = {"checked": False}
    if "collision_found" in linked:
        pol, ev = verify_polarity(tr.get("decision", "") + " " + tr.get("reasoning", ""))
        data_no_collision = not bool(linked["collision_found"])
        claim = {"no_collision": True, "collision": False}.get(pol)
        consistency = {"checked": True, "kind": "verify_collision",
                       "trace_polarity": pol, "evidence": ev,
                       "data_collision_found": linked["collision_found"]}
        if pol in ("no_collision", "collision"):
            if claim != data_no_collision:
                logic_break = True
                flags.append("LOGIC_BREAK:decision_contradicts_collision_data")
        else:
            consistency["note"] = "polarity_indeterminate (no break asserted)"
    elif "mismatch_with_agent3" in linked:
        pol, ev = confirm_polarity(tr.get("decision", "") + " " + tr.get("reasoning", ""))
        data_confirm = not bool(linked["mismatch_with_agent3"])
        claim = {"confirm": True, "dispute": False}.get(pol)
        consistency = {"checked": True, "kind": "crosscheck_confirm",
                       "trace_polarity": pol, "evidence": ev,
                       "data_mismatch_with_agent3": linked["mismatch_with_agent3"]}
        if pol in ("confirm", "dispute"):
            if claim != data_confirm:
                logic_break = True
                flags.append("LOGIC_BREAK:decision_contradicts_crosscheck_data")
        else:
            consistency["note"] = "polarity_indeterminate (no break asserted)"
    elif "quote_verified_substring" in linked:
        consistency = {"checked": True, "kind": "merge_quote_context",
                       "data_quote_verified": linked["quote_verified_substring"],
                       "note": "merge decision is a niche (not a boolean); quote grounding "
                               "is checked structurally by MAIN Gate-4, recorded here as context"}

    valid = complete and conf_ok and falsifiable and not logic_break
    # auditor's OWN reasoning_trace (the auditor is itself transparent)
    audit_trace = {
        "step": f"audit {source} :: {step_id}",
        "inputs_seen": f"6 fields present={not missing}; confidence_level={lvl}; "
                       f"grounding_overlap={grounding}; linked_data={ {k: linked[k] for k in linked} }",
        "reasoning": "Applied 6 deterministic checks (completeness, confidence rationale, "
                     "falsifiability, inputs-grounding overlap, overconfidence-hedge, "
                     "decision<->recorded-data consistency). A LOGIC BREAK is asserted ONLY "
                     "when the trace's detected polarity contradicts a structured fact.",
        "decision": ("LOGIC_BREAK" if logic_break else ("VALID" if valid else "FLAGGED_NONFATAL")),
        "confidence": ("high - all checks are deterministic over committed JSON"
                       if not (consistency.get("kind", "").startswith("verify") and
                               consistency.get("trace_polarity") in (None, "ambiguous"))
                       else "medium - polarity of the prose decision was indeterminate, so the "
                            "data-consistency check could not fire; format checks still deterministic"),
        "could_be_wrong_if": "the polarity phrase-lists miss a paraphrase, so a real "
                             "decision<->data contradiction is read as indeterminate (false negative), "
                             "or grounding overlap penalizes correct but differently-worded decisions.",
    }
    return {
        "trace_id": step_id, "source_agent": source, "step": tr.get("step", ""),
        "complete": complete, "missing_fields": missing,
        "confidence_level": lvl, "confidence_wellformed": conf_ok,
        "falsifiable": falsifiable, "inputs_grounding_overlap": grounding,
        "overconfident": overconfident, "hedges_found": hedges,
        "decision_data_consistency": consistency,
        "logic_break": logic_break, "flags": flags,
        "verdict": audit_trace["decision"], "audit_reasoning_trace": audit_trace,
    }


def collect() -> list[dict]:
    """Gather every reasoning_trace from AGENT 1-4 with its linked structured fact."""
    items: list[dict] = []

    # AGENT 1: atoms_reasoning.json
    p = LOGS / "atoms_reasoning.json"
    if p.exists():
        ar = json.loads(p.read_text())
        if isinstance(ar.get("overall_trace"), dict):
            items.append({"trace": ar["overall_trace"], "source": "AGENT_1_sourcer",
                          "step_id": "atoms.overall"})
        for at in ar.get("atom_traces", []):
            items.append({"trace": at.get("reasoning_trace", {}), "source": "AGENT_1_sourcer",
                          "step_id": f"atom.{at.get('atom_id', '?')}"})
        for dc in ar.get("discarded_traces", []):
            items.append({"trace": dc.get("reasoning_trace", {}), "source": "AGENT_1_sourcer",
                          "step_id": f"atom.discarded.{dc.get('label', '?')}"})

    # AGENT 2: candidates.json (reasoning_trace per candidate; link quote_verified)
    p = LOGS / "candidates.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            items.append({"trace": c.get("reasoning_trace", {}), "source": "AGENT_2_merger",
                          "step_id": f"merge.{c['cand_id']}",
                          "linked": {"quote_verified_substring": c.get("quote_verified_substring")}})

    # AGENT 3: verify_reasoning.json (verdict + per-reformulation); link collision_found
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
                items.append({"trace": c["verdict_trace"], "source": "AGENT_3_verifier",
                              "step_id": f"verify.verdict.{cid}",
                              "linked": {"collision_found": coll.get(cid)}})
            for rt in c.get("reformulation_traces", []):
                items.append({"trace": rt.get("reasoning_trace", {}), "source": "AGENT_3_verifier",
                              "step_id": f"verify.reform.{cid}.n{rt.get('n', '?')}"})

    # AGENT 4: crosscheck.json (reasoning_trace per candidate; link mismatch_with_agent3)
    p = LOGS / "crosscheck.json"
    if p.exists():
        for c in json.loads(p.read_text()).get("candidates", []):
            items.append({"trace": c.get("reasoning_trace", {}), "source": "AGENT_4_crosschecker",
                          "step_id": f"crosscheck.{c['cand_id']}",
                          "linked": {"mismatch_with_agent3": c.get("mismatch_with_agent3")}})
    return items


def main() -> int:
    items = collect()
    audits = [audit_one(it["trace"], source=it["source"], step_id=it["step_id"],
                        linked=it.get("linked")) for it in items]
    by_agent: dict[str, dict] = {}
    for a in audits:
        d = by_agent.setdefault(a["source_agent"], {"traces": 0, "complete": 0,
                                                     "flagged": 0, "logic_breaks": 0})
        d["traces"] += 1
        d["complete"] += int(a["complete"])
        d["flagged"] += int(bool(a["flags"]))
        d["logic_breaks"] += int(a["logic_break"])
    summary = {
        "total_traces_audited": len(audits),
        "all_complete": all(a["complete"] for a in audits),
        "n_complete": sum(a["complete"] for a in audits),
        "n_flagged_nonfatal": sum(1 for a in audits if a["flags"] and not a["logic_break"]),
        "n_logic_breaks": sum(a["logic_break"] for a in audits),
        "logic_break_trace_ids": [a["trace_id"] for a in audits if a["logic_break"]],
        "by_agent": by_agent,
        "consistency_checks_fired": sum(1 for a in audits
                                        if a["decision_data_consistency"].get("checked")),
    }
    out = {
        "run_id": "run_017", "agent": "5_reasoning_auditor",
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "method": "deterministic rule-based audit over committed reasoning_traces; "
                  "rules in run17_rules.json.audit_checks; auditor emits its own reasoning_trace "
                  "per audited trace so the auditor is not a black box (R9).",
        "summary": summary, "audits": audits,
    }
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "reasoning_audit.json").write_text(json.dumps(out, indent=2))
    print(f"[audit] {summary['total_traces_audited']} traces; complete={summary['n_complete']} "
          f"flagged_nonfatal={summary['n_flagged_nonfatal']} LOGIC_BREAKS={summary['n_logic_breaks']}")
    for a in audits:
        mark = "BREAK" if a["logic_break"] else ("FLAG " if a["flags"] else "ok   ")
        print(f"  [{mark}] {a['source_agent']:<20} {a['trace_id']:<28} "
              f"ground={a['inputs_grounding_overlap']} {('; '.join(a['flags']) if a['flags'] else '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
