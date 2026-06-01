#!/usr/bin/env python3
"""Offline tests for Run 18 deterministic logic (no network, no Opus).

Adds, on top of Run 17's coverage: sparsest-cross-paper-pair selection, and the
new AGENT-5 sparsity decision<->data check (a 'sparse'/'dense' label must agree
with the recorded per-atom paper-hit count vs the threshold).

Run: python3 paradigm_shift/test_run18.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run18_orchestrator as O  # noqa: E402
import run18_audit as A          # noqa: E402
import run18_merge as M          # noqa: E402

TF = O.RULES["reasoning_trace_schema"]["required_fields"]


def good_trace(decision="no collision found; the niche is novel"):
    return {"step": "s", "inputs_seen": "five real searches returned only the two source atoms",
            "reasoning": "the source papers recur but none occupy the fused niche, so it is novel",
            "decision": decision, "confidence": "high - all five searches agreed",
            "could_be_wrong_if": "a paper exists under vocabulary my queries never used"}


def atoms_fixture():
    return {"atoms": [
        {"atom_id": "P1S1", "paper_id": "P1", "text": "A concentration matrix controls routing entropy in the mixture of experts router weights.", "domain": "ml"},
        {"atom_id": "P2S1", "paper_id": "P2", "text": "The optimal schedule under the Fisher-Rao geometry recovers the cosine schedule for masked diffusion.", "domain": "ml"},
        {"atom_id": "P3S1", "paper_id": "P3", "text": "Geometric bounds on entropy production yield limits on the energy-delay-deficiency product in thermodynamic computing.", "domain": "physics"},
    ]}


def cand(cid, a, b, mech, quote, src):
    return {"cand_id": cid, "atom_a_id": a, "atom_b_id": b, "niche_name": "N", "mechanism": mech,
            "primary_quote": quote, "quote_source": src, "reasoning_trace": good_trace()}


def verify_fixture(per):
    cands = []
    for cid, (coll, nref, nhits) in per.items():
        reforms = [{"n": n + 1, "query": "q", "results": [{"title": f"p{i}", "url": "https://arxiv.org/pdf/1"}
                                                           for i in (range(nhits) if n == 0 else [])]} for n in range(nref)]
        cands.append({"cand_id": cid, "collision_found": coll, "reformulations": reforms})
    return {"candidates": cands}


def crosscheck_fixture(per):
    return {"candidates": [{"cand_id": cid, "mismatch_with_agent3": m} for cid, m in per.items()]}


class TestPairSelection(unittest.TestCase):
    def test_cross_paper_sparsest_first(self):
        atoms = atoms_fixture()["atoms"]
        hits = {"P1S1": 40, "P2S1": 3, "P3S1": 2}
        pairs = M.select_pairs(atoms, hits)
        # 3 cross-paper pairs; sparsest = P2S1+P3S1 (combined 5)
        self.assertEqual(len(pairs), 3)
        self.assertEqual((pairs[0][2], pairs[0][3]), ("P2S1", "P3S1"))
        self.assertEqual(pairs[0][0], 5)

    def test_same_paper_excluded(self):
        atoms = [{"atom_id": "P1A", "paper_id": "P1", "text": "x"}, {"atom_id": "P1B", "paper_id": "P1", "text": "y"},
                 {"atom_id": "P2A", "paper_id": "P2", "text": "z"}]
        pairs = M.select_pairs(atoms, {"P1A": 1, "P1B": 1, "P2A": 1})
        got = {(p[2], p[3]) for p in pairs}
        self.assertNotIn(("P1A", "P1B"), got)  # same paper excluded
        self.assertEqual(len(pairs), 2)


class TestGates(unittest.TestCase):
    def test_composite_floor_and_clear(self):
        atoms = atoms_fixture()
        c = cand("C", "P1S1", "P2S1", "a router regulates routing entropy", "A concentration matrix controls routing entropy", "atom_a")
        hi = O.run_gates(atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 0)}), crosscheck_fixture({"C": False}))
        self.assertEqual(hi[0]["composite"], 1.0)
        self.assertTrue(hi[0]["gate_1_composite"]["pass"])
        lo = O.run_gates(atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 12)}), crosscheck_fixture({"C": False}))
        self.assertFalse(lo[0]["gate_1_composite"]["pass"])

    def test_every_gate_has_trace_and_determinism(self):
        atoms = atoms_fixture()
        c = cand("C", "P1S1", "P2S1", "a router regulates routing entropy", "A concentration matrix controls routing entropy", "atom_a")
        args = (atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 3)}), crosscheck_fixture({"C": False}))
        res = O.run_gates(*args, with_traces=True)[0]
        for g in ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"):
            for f in TF:
                self.assertTrue(str(res[g]["reasoning_trace"].get(f, "")).strip())
        self.assertEqual(O.verdicts_hash(O.run_gates(*args)), O.verdicts_hash(O.run_gates(*args)))


class TestAudit(unittest.TestCase):
    def test_logic_break_verify(self):
        r = A.audit_one(good_trace("no collision; novel and unoccupied"), source="AGENT_4_verifier",
                        step_id="t", linked={"collision_found": True})
        self.assertTrue(r["logic_break"])

    def test_sparsity_consistency_ok(self):
        tr = good_trace("this sub-mechanism is sparse / rare in the literature")
        r = A.audit_one(tr, source="AGENT_2_atom_search", step_id="t", linked={"paper_hits": 3})
        self.assertEqual(r["decision_data_consistency"]["kind"], "atom_sparsity")
        self.assertFalse(r["logic_break"])  # sparse claim + 3 hits (<10) agree

    def test_sparsity_logic_break(self):
        tr = good_trace("this sub-mechanism is sparse and rare")
        r = A.audit_one(tr, source="AGENT_2_atom_search", step_id="t", linked={"paper_hits": 40})
        self.assertTrue(r["logic_break"])  # 'sparse' claim contradicts 40 hits
        self.assertIn("LOGIC_BREAK:sparsity_label_contradicts_hit_count", r["flags"])

    def test_complete_trace_valid(self):
        r = A.audit_one(good_trace(), source="X", step_id="t", linked={"collision_found": False})
        self.assertTrue(r["complete"])
        self.assertFalse(r["logic_break"])


class TestParsing(unittest.TestCase):
    def test_parse_obj_and_trace_complete(self):
        self.assertEqual(M.parse_obj('text {"a":3} more')["a"], 3)
        self.assertTrue(M.trace_complete(good_trace()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
