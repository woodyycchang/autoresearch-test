#!/usr/bin/env python3
"""Offline tests for Run 19 (no network, no Opus): gates, pair selection, audit,
param-nudge (Run 16 machinery), and search-quality scoring (the convergence signal)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run19_orchestrator as O  # noqa: E402
import run19_audit as A          # noqa: E402
import run19_merge as M          # noqa: E402

TF = O.RULES["reasoning_trace_schema"]["required_fields"]


def good_trace(decision="no collision found; the niche is novel"):
    return {"step": "s", "inputs_seen": "five real searches returned only the two source atoms",
            "reasoning": "the source papers recur but none occupy the fused niche, so it is novel",
            "decision": decision, "confidence": "high - all five searches agreed",
            "could_be_wrong_if": "a paper exists under vocabulary my queries never used"}


def atoms_fixture():
    return {"atoms": [
        {"atom_id": "P1S1", "paper_id": "P1", "text": "A concentration matrix controls routing entropy in the mixture of experts router.", "domain": "ml"},
        {"atom_id": "P2S1", "paper_id": "P2", "text": "The optimal schedule under the Fisher-Rao geometry recovers the cosine schedule for masked diffusion.", "domain": "ml"},
        {"atom_id": "P3S1", "paper_id": "P3", "text": "Geometric bounds on entropy production yield limits on the energy-delay-deficiency product.", "domain": "physics"}]}


def cand(cid, a, b, mech, quote, src):
    return {"cand_id": cid, "atom_a_id": a, "atom_b_id": b, "niche_name": "N", "mechanism": mech,
            "primary_quote": quote, "quote_source": src, "reasoning_trace": good_trace()}


def verify_fixture(per):
    cands = []
    for cid, (coll, nref, nhits) in per.items():
        reforms = [{"n": n + 1, "query": "q", "results": [{"title": f"p{i}", "url": "https://arxiv.org/pdf/1"} for i in (range(nhits) if n == 0 else [])]} for n in range(nref)]
        cands.append({"cand_id": cid, "collision_found": coll, "reformulations": reforms})
    return {"candidates": cands}


def cc_fixture(per): return {"candidates": [{"cand_id": cid, "mismatch_with_agent3": m} for cid, m in per.items()]}


class TestGatesPairs(unittest.TestCase):
    def test_composite_floor_and_clear(self):
        atoms = atoms_fixture(); c = cand("C", "P1S1", "P2S1", "a router regulates routing entropy", "A concentration matrix controls routing entropy", "atom_a")
        hi = O.run_gates(atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 0)}), cc_fixture({"C": False}))
        self.assertEqual(hi[0]["composite"], 1.0); self.assertTrue(hi[0]["gate_1_composite"]["pass"])
        lo = O.run_gates(atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 12)}), cc_fixture({"C": False}))
        self.assertFalse(lo[0]["gate_1_composite"]["pass"])

    def test_traces_and_determinism(self):
        atoms = atoms_fixture(); c = cand("C", "P1S1", "P2S1", "a router regulates entropy", "A concentration matrix controls routing entropy", "atom_a")
        args = (atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 3)}), cc_fixture({"C": False}))
        r = O.run_gates(*args, with_traces=True)[0]
        for g in ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"):
            for f in TF: self.assertTrue(str(r[g]["reasoning_trace"].get(f, "")).strip())
        self.assertEqual(O.verdicts_hash(O.run_gates(*args)), O.verdicts_hash(O.run_gates(*args)))

    def test_cross_paper_sparsest(self):
        atoms = atoms_fixture()["atoms"]; pairs = M.select_pairs(atoms, {"P1S1": 40, "P2S1": 3, "P3S1": 2})
        self.assertEqual((pairs[0][2], pairs[0][3]), ("P2S1", "P3S1"))


class TestAudit(unittest.TestCase):
    def test_logic_break_verify(self):
        r = A.audit_one(good_trace("no collision; novel"), source="AGENT_4_verifier", step_id="t", linked={"collision_found": True})
        self.assertTrue(r["logic_break"])
    def test_sparsity_consistency(self):
        ok = A.audit_one(good_trace("this sub-mechanism is sparse / rare"), source="AGENT_2_atom_search", step_id="t", linked={"paper_hits": 3})
        self.assertFalse(ok["logic_break"])
        bad = A.audit_one(good_trace("this sub-mechanism is sparse and rare"), source="AGENT_2_atom_search", step_id="t", linked={"paper_hits": 40})
        self.assertTrue(bad["logic_break"])


class TestParamNudge(unittest.TestCase):
    def test_nudge_toward_on_target(self):
        # on_target queries score high on mechanism_focus; diverge score low -> mechanism_focus param rises
        dp = {"params": {k: 0.5 for k in ["specificity", "mechanism_focus", "sparsity_seeking", "cross_paper_pairing", "collision_avoidance_phrasing"]},
              "labeled_examples": [
                  {"label": "on_target", "dims": {"specificity": 0.5, "mechanism_focus": 1.0, "sparsity_seeking": 0.5, "cross_paper_pairing": 0.5, "collision_avoidance": 0.5}},
                  {"label": "diverge", "dims": {"specificity": 0.5, "mechanism_focus": 0.0, "sparsity_seeking": 0.5, "cross_paper_pairing": 0.5, "collision_avoidance": 0.5}}]}
        params, nudges = O.nudge_from_labels(dp)
        self.assertIn("mechanism_focus", nudges)
        self.assertGreater(params["mechanism_focus"], 0.5)         # moved up toward on_target
        self.assertEqual(params["specificity"], 0.5)              # flat dim unchanged

    def test_no_labels_no_change(self):
        dp = {"params": {k: 0.5 for k in ["specificity", "mechanism_focus", "sparsity_seeking", "cross_paper_pairing", "collision_avoidance_phrasing"]}, "labeled_examples": []}
        params, nudges = O.nudge_from_labels(dp)
        self.assertEqual(nudges, {}); self.assertEqual(params["mechanism_focus"], 0.5)


class TestSearchQuality(unittest.TestCase):
    def test_score_query_dims(self):
        d = A.score_query("Matrix Bingham Fisher-Rao mixture of experts routing entropy prior work")
        self.assertGreaterEqual(d["sparsity_seeking"], 0.5)   # bingham + fisher-rao exotic
        self.assertEqual(d["collision_avoidance"], 1.0)        # 'prior work'
        self.assertGreaterEqual(d["mechanism_focus"], 0.6)     # routing+entropy mechanism terms
        self.assertEqual(d["cross_paper_pairing"], 1.0)        # ml_routing + geometry domains
    def test_generic_query_low(self):
        d = A.score_query("what is a neural network")
        self.assertEqual(d["collision_avoidance"], 0.2)
        self.assertEqual(d["sparsity_seeking"], 0.1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
