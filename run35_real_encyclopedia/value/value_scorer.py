#!/usr/bin/env python3
"""
value_scorer.py  —  Run 35 generator-side value/plausibility stage.

A cross-domain construct 'apply mechanism A to problem B' is VALUABLE/PLAUSIBLE
when the structural properties A's mechanism REQUIRES (preconditions, union over
its mech_core tokens) are AFFORDED by problem B (affordances, union over its
problem_core tokens). structural_fit = coverage(preconditions by affordances).

This is a SEPARATE stage layered after the (frozen, production-ready) niche
checker; it does not touch the decision engine. Borderline structural-fit is
routed to a frozen Opus value-audit, reusing the niche-audit pattern, so the
stage stays deterministic.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_maps():
    pre = json.load(open(os.path.join(HERE, "precondition_map.json")))["map"]
    aff = json.load(open(os.path.join(HERE, "affordance_map.json")))["map"]
    return pre, aff


def preconditions(c, pre):
    s = set()
    for t in c.get("mech_core", []):
        s |= set(pre.get(t, []))
    return s


def affordances(c, aff):
    s = set()
    for t in c.get("problem_core", []):
        s |= set(aff.get(t, []))
    return s


def structural_fit(c, pre, aff):
    p = preconditions(c, pre)
    if not p:
        return None
    a = affordances(c, aff)
    return round(len(p & a) / len(p), 4)


def value_score(c, params, pre, aff, value_audit=None):
    """VALUABLE / USELESS / UNSCORED. Borderline fit -> frozen value-audit gate,
    else conservative USELESS (a niche must EARN 'valuable')."""
    fit = structural_fit(c, pre, aff)
    if fit is None:
        return {"verdict": "UNSCORED", "fit": None, "reason": "no_preconditions"}
    thr = params.get("value_threshold", 0.6)
    floor = params.get("value_floor", 0.35)
    if fit >= thr:
        return {"verdict": "VALUABLE", "fit": fit, "reason": "structural_fit_high"}
    if fit < floor:
        return {"verdict": "USELESS", "fit": fit, "reason": "preconditions_unmet"}
    # borderline band -> consult frozen value-audit
    if value_audit and c.get("id") in value_audit:
        a = value_audit[c["id"]]
        if a.get("confidence", 0.0) >= params.get("value_audit_gate", 0.75):
            return {"verdict": "VALUABLE" if a.get("is_valuable") else "USELESS",
                    "fit": fit, "reason": "value_audit", "audit_conf": a["confidence"]}
    return {"verdict": "USELESS", "fit": fit, "reason": "borderline_conservative"}
