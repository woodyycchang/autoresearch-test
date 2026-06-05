#!/usr/bin/env python3
"""Determinism worker: run the niche checker over all ground-truth fixtures
under the AMBIENT PYTHONHASHSEED, using a given params file. Prints
{construct_id: verdict} as JSON. run_cycle.py spawns this in subprocesses with
different PYTHONHASHSEED values to measure decision agreement.

Usage: PYTHONHASHSEED=<n> python3 _niche_worker.py <params_json_path> [audit_table_json]
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "engine"))
sys.path.insert(0, os.path.join(BASE, "ground_truth"))
from encyclopedia_engine import niche_check  # noqa: E402
from build_ground_truth import KNOWN_APPROACHES  # noqa: E402


def main():
    params_path = sys.argv[1]
    audit_table = None
    if len(sys.argv) > 2 and sys.argv[2] not in ("", "none"):
        audit_table = json.load(open(sys.argv[2]))
    with open(params_path) as f:
        blob = json.load(f)
    p = blob["params"] if "params" in blob else blob
    constructs = json.load(open(os.path.join(BASE, "ground_truth",
                                             "labeled_constructs.json")))["constructs"]
    out = {c["id"]: niche_check(c, p, KNOWN_APPROACHES, audit_table=audit_table)["verdict"]
           for c in constructs}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
