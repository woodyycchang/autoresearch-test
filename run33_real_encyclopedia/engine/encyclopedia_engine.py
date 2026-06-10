#!/usr/bin/env python3
"""
encyclopedia_engine.py  —  Run 32 real-encyclopedia pipeline core.

Pure, deterministic functions for the four instrumented stages:
  1. MERGE ENGINE      -> make_construct / generate_constructs
  2. INTEGRITY CHECKER -> integrity_check        (genuine merge vs trivial/incoherent)
  3. NICHE CHECKER     -> niche_check            (R13 strict variant detection)
  4. (reasoning audit + coordination live in instrumentation/)

Nothing here calls a network or an LLM, so re-running on identical input is
byte-deterministic EXCEPT where v4's `borderline_rule == "order_first"` makes a
borderline verdict depend on approach-iteration order. That order-dependence is
the latent Run-27 weakness the determinism harness is built to expose; v5's
`conservative_reject` rule removes it.
"""
from __future__ import annotations
import json
import os
from itertools import combinations

# --- domain adjacency: near-domains are a smaller cognitive jump -------------
_ADJACENT = {
    frozenset({"machine_learning", "computer_science"}): 0.55,
    frozenset({"machine_learning", "neuroscience"}): 0.55,
    frozenset({"biology", "neuroscience"}): 0.50,
    frozenset({"physics", "chemistry"}): 0.55,
    frozenset({"physics", "materials"}): 0.55,
    frozenset({"chemistry", "materials"}): 0.55,
    frozenset({"biology", "ecology"}): 0.50,
    frozenset({"information_theory", "computer_science"}): 0.55,
    frozenset({"information_theory", "cryptography"}): 0.55,
    frozenset({"control_theory", "machine_learning"}): 0.55,
    frozenset({"economics", "ecology"}): 0.60,
    frozenset({"mathematics", "physics"}): 0.55,
    frozenset({"mathematics", "information_theory"}): 0.55,
}


def jaccard(a, b) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def domain_distance(d1: str, d2: str) -> float:
    if d1 == d2:
        return 0.0
    return _ADJACENT.get(frozenset({d1, d2}), 1.0)


def cognitive_distance(a: dict, b: dict) -> float:
    """High when the two concepts are from far domains AND solve different problems."""
    dd = domain_distance(a["domain"], b["domain"])
    prob_overlap = jaccard(a["problem_tokens"], b["problem_tokens"])
    cd = 0.6 * dd + 0.4 * (1.0 - prob_overlap)
    return round(cd, 4)


def make_construct(a: dict, b: dict) -> dict:
    """A construct = applying concept A's mechanism to concept B's problem.

    mech_core/problem_core are the donor's mechanism and the target's problem:
    a construct is a method-VARIANT of an existing approach exactly when its
    mech_core matches that approach's mechanism AND its problem_core matches
    that approach's problem (i.e. you have merely re-derived the approach)."""
    shared_mech = sorted(set(a["mechanism_tokens"]) & set(b["mechanism_tokens"]))
    return {
        "id": None,  # assigned by caller / ground-truth
        "parents": [a["id"], b["id"]],
        "parent_names": [a["name"], b["name"]],
        "statement": f"Use {a['name']}'s mechanism to address {b['name']}'s problem.",
        "cognitive_distance": cognitive_distance(a, b),
        "shared_mechanism_tokens": shared_mech,
        "mech_core": sorted(set(a["mechanism_tokens"])),       # donor mechanism
        "problem_core": sorted(set(b["problem_tokens"])),       # target problem
        "mechanism_tokens": sorted(set(a["mechanism_tokens"]) | set(b["mechanism_tokens"])),
        "problem_tokens": sorted(set(a["problem_tokens"]) | set(b["problem_tokens"])),
        "parent_problem_overlap": round(jaccard(a["problem_tokens"], b["problem_tokens"]), 4),
    }


# --------------------------------------------------------------------------
# STAGE 2: INTEGRITY CHECKER — genuine merge vs trivial / incoherent
# --------------------------------------------------------------------------
def integrity_check(c: dict, p: dict) -> dict:
    """Return {pass, reason}. A genuine merge needs distance, a transfer
    interface (shared mechanism token), and non-duplicate problems."""
    if not c["shared_mechanism_tokens"]:
        return {"pass": False, "reason": "incoherent_no_interface"}
    if c["cognitive_distance"] < p["merge_distance_min"]:
        return {"pass": False, "reason": "trivial_too_close"}
    if c["parent_problem_overlap"] > p["trivial_problem_overlap_max"]:
        return {"pass": False, "reason": "restatement_same_problem"}
    return {"pass": True, "reason": "genuine_merge"}


# --------------------------------------------------------------------------
# STAGE 3: NICHE CHECKER — R13 strict variant detection (the key component)
# --------------------------------------------------------------------------
def variant_similarity(c: dict, approach: dict, p: dict) -> float:
    """Compare the construct's mechanism-donor and problem-target against an
    existing approach. High => the construct is just a variant of that approach."""
    sm = jaccard(c["mech_core"], approach["mechanism_tokens"])
    sp = jaccard(c["problem_core"], approach["problem_tokens"])
    return round(p["variant_w_mech"] * sm + p["variant_w_problem"] * sp, 4)


def _variant_scan(c: dict, p: dict, approaches: list):
    """Per-approach mechanism/problem Jaccards + combined similarity."""
    rows = []
    for a in approaches:
        mj = jaccard(c["mech_core"], a["mechanism_tokens"])
        pj = jaccard(c["problem_core"], a["problem_tokens"])
        comb = round(p["variant_w_mech"] * mj + p["variant_w_problem"] * pj, 4)
        rows.append({"id": a["id"], "mech_j": round(mj, 4), "prob_j": round(pj, 4), "comb": comb})
    return rows


def niche_check(c: dict, p: dict, approaches: list, audit_table: dict | None = None) -> dict:
    """Decide NICHE_FOUND vs REJECT(variant/saturated/integrity).

    v4 (variant_rule_mode='scalar', borderline_rule='neighbor_set_first'):
      borderline verdict resolved by iterating a *set* of neighbour ids ->
      PYTHONHASHSEED-dependent (the Run-27 determinism hazard).
    v5 (variant_rule_mode='two_factor', borderline_rule='conservative_reject'):
      variant iff it reuses a known mechanism AND echoes that approach's problem
      (or combined sim clears threshold); borderline -> blanket conservative
      reject; deterministic.
    v6 (borderline_rule='audit_gated'): a borderline construct that two_factor
      did NOT flag is routed to the FROZEN reasoning-audit table (`audit_table`,
      produced once by real Opus agents and cached for determinism). If the
      audit's confidence >= p['audit_confidence_gate'] its verdict is used
      (rescuing borderline GENUINE niches that v5 would have false-rejected);
      otherwise fall back to conservative reject. Deterministic given the table.
    """
    integ = integrity_check(c, p)
    if not integ["pass"]:
        return {"verdict": "REJECT", "reason": f"integrity:{integ['reason']}",
                "max_sim": None, "nearest": None, "borderline": False}

    rows = _variant_scan(c, p, approaches)
    max_row = max(rows, key=lambda r: (r["comb"], r["id"]))  # deterministic max
    max_sim, max_id = max_row["comb"], max_row["id"]
    thr = p["variant_similarity_threshold"]
    margin = p["confidence_margin"]
    borderline = abs(max_sim - thr) < margin
    neighbor_ids = {r["id"] for r in rows if r["comb"] >= p["saturation_band"]}
    saturated = len(neighbor_ids) > p["saturation_max_neighbors"]
    mode = p.get("variant_rule_mode", "scalar")
    rule = p.get("borderline_rule", "neighbor_set_first")

    if mode == "two_factor":
        mmin = p.get("mech_match_min", 0.6)
        pmin = p.get("problem_echo_min", 0.3)
        is_variant = any(
            (r["mech_j"] >= mmin and r["prob_j"] >= pmin) or r["comb"] >= thr
            for r in rows)
        if is_variant:
            return {"verdict": "REJECT", "reason": "method_variant", "max_sim": max_sim,
                    "nearest": max_id, "borderline": borderline}
        if borderline:
            # v6: consult the frozen reasoning-audit before the blanket reject.
            if rule == "audit_gated" and audit_table and c.get("id") in audit_table:
                a = audit_table[c["id"]]
                if a.get("confidence", 0.0) >= p.get("audit_confidence_gate", 0.75):
                    if a.get("is_variant"):
                        return {"verdict": "REJECT", "reason": "method_variant_audit",
                                "max_sim": max_sim, "nearest": max_id, "borderline": True,
                                "audit": {"used": True, "confidence": a["confidence"]}}
                    return {"verdict": "NICHE_FOUND", "reason": "borderline_audit_cleared",
                            "max_sim": max_sim, "nearest": max_id, "borderline": True,
                            "audit": {"used": True, "confidence": a["confidence"]}}
                # low-confidence audit -> fall through to conservative reject
                return {"verdict": "REJECT", "reason": "method_variant_borderline",
                        "max_sim": max_sim, "nearest": max_id, "borderline": True,
                        "audit": {"used": False, "confidence": a.get("confidence")}}
            # v5 blanket conservative reject (also v6 fallback when no audit entry)
            return {"verdict": "REJECT", "reason": "method_variant_borderline",
                    "max_sim": max_sim, "nearest": max_id, "borderline": True}
        if saturated:
            return {"verdict": "REJECT", "reason": "saturated_region", "max_sim": max_sim,
                    "nearest": max_id, "borderline": borderline}
        return {"verdict": "NICHE_FOUND", "reason": "passes_all_gates", "max_sim": max_sim,
                "nearest": max_id, "borderline": borderline}

    # ---- v4 scalar mode ----
    sim_by_id = {r["id"]: r["comb"] for r in rows}
    if borderline and rule == "neighbor_set_first":
        decided = None
        for aid in neighbor_ids:               # SET iteration -> hash-seed dependent
            decided = sim_by_id[aid] >= thr
            break
        if decided is None:
            decided = max_sim >= thr
        if decided:
            return {"verdict": "REJECT", "reason": "method_variant", "max_sim": max_sim,
                    "nearest": max_id, "borderline": True}
        if saturated:
            return {"verdict": "REJECT", "reason": "saturated_region", "max_sim": max_sim,
                    "nearest": max_id, "borderline": True}
        return {"verdict": "NICHE_FOUND", "reason": "passes_all_gates", "max_sim": max_sim,
                "nearest": max_id, "borderline": True}

    if max_sim >= thr:
        return {"verdict": "REJECT", "reason": "method_variant", "max_sim": max_sim,
                "nearest": max_id, "borderline": borderline}
    if saturated:
        return {"verdict": "REJECT", "reason": "saturated_region", "max_sim": max_sim,
                "nearest": max_id, "borderline": borderline}
    return {"verdict": "NICHE_FOUND", "reason": "passes_all_gates", "max_sim": max_sim,
            "nearest": max_id, "borderline": borderline}


# --------------------------------------------------------------------------
# STAGE 1 driver: generate constructs from the bank (cross-domain, transferable)
# --------------------------------------------------------------------------
def generate_constructs(bank: dict, p: dict) -> list:
    """Generate constructs from the concept-pair space.

    By default (v4) the FULL pair space is emitted and the integrity checker --
    not the generator -- decides which are genuine merges, so genuine-merge rate
    is a real measurement of raw generation quality.

    p['merge_require_interface'] (v5): emit only pairs that share >=1 mechanism
    token -- the transfer interface that coherence requires. This is the
    measurement-driven merge-engine upgrade (raw generation fails ~93% as
    incoherent_no_interface).
    p['merge_steer_strength'] > 0: additionally drop the closest fraction by
    cognitive distance (distance steering)."""
    concepts = bank["concepts"]
    require_iface = p.get("merge_require_interface", False)
    constructs = []
    for a, b in combinations(concepts, 2):
        if require_iface and not (set(a["mechanism_tokens"]) & set(b["mechanism_tokens"])):
            continue
        for donor, target in ((a, b), (b, a)):
            c = make_construct(donor, target)
            c["id"] = f"G_{donor['id']}__{target['id']}"
            constructs.append(c)
    constructs.sort(key=lambda c: c["id"])

    steer = p.get("merge_steer_strength", 0.0)
    if steer > 0.0:
        constructs.sort(key=lambda c: (-c["cognitive_distance"], c["id"]))
        keep = int(round(len(constructs) * (1.0 - steer)))
        constructs = sorted(constructs[:keep], key=lambda c: c["id"])
    return constructs


def load_bank(path: str | None = None) -> dict:
    path = path or os.path.join(os.path.dirname(__file__), "concept_banks.json")
    with open(path) as f:
        return json.load(f)


def load_params(path: str | None = None) -> dict:
    path = path or os.path.join(os.path.dirname(__file__), "direction_params.json")
    with open(path) as f:
        return json.load(f)["params"]
