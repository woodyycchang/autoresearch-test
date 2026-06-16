#!/usr/bin/env python3
"""Scale worker: generate constructs from the full bank, run the niche checker
on every genuine merge under the ambient PYTHONHASHSEED, and print a compact
digest (verdict counts + a sha1 over the sorted (id,verdict) list). run_cycle
spawns this under two different seeds to confirm determinism holds AT SCALE.

Usage: PYTHONHASHSEED=<n> python3 _scale_worker.py <params_json> [audit_table_json]
"""
import json, os, sys, hashlib
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "engine"))
sys.path.insert(0, os.path.join(BASE, "ground_truth"))
from encyclopedia_engine import generate_constructs, integrity_check, niche_check, load_bank  # noqa
from build_ground_truth import KNOWN_APPROACHES  # noqa


def main():
    p = json.load(open(sys.argv[1]))
    p = p["params"] if "params" in p else p
    audit = None
    if len(sys.argv) > 2 and sys.argv[2] not in ("", "none"):
        audit = json.load(open(sys.argv[2]))
    bank = load_bank()
    cons = generate_constructs(bank, p)
    genuine = [c for c in cons if integrity_check(c, p)["pass"]]
    verdicts = []
    counts = Counter()
    borderline = 0
    for c in genuine:
        r = niche_check(c, p, KNOWN_APPROACHES, audit_table=audit)
        verdicts.append((c["id"], r["verdict"]))
        counts[r["verdict"]] += 1
        borderline += 1 if r.get("borderline") else 0
    verdicts.sort()
    digest = hashlib.sha1(json.dumps(verdicts).encode()).hexdigest()
    print(json.dumps({
        "n_generated": len(cons), "n_genuine": len(genuine),
        "verdict_counts": dict(counts), "borderline": borderline, "digest": digest}))


if __name__ == "__main__":
    main()
