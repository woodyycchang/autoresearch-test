#!/usr/bin/env python3
"""Offline tests for Run 17 deterministic logic (no network, no Opus).

Proves: the 4 inherited gates behave, every gate decision carries a complete
reasoning_trace, the gate math is deterministic, and AGENT 5's reasoning-auditor
correctly (a) validates complete traces, (b) flags incomplete/over-confident/
non-falsifiable traces, and (c) detects LOGIC BREAKS where a trace's decision
contradicts the recorded structured data (R10).

Run: python3 paradigm_shift/test_run17.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run17_orchestrator as O  # noqa: E402
import run17_audit as A          # noqa: E402
import run17_merge as M          # noqa: E402

TRACE_FIELDS = O.RULES["reasoning_trace_schema"]["required_fields"]


def good_trace(step="s", decision="no collision found; the niche is novel"):
    return {"step": step, "inputs_seen": "five real searches returned only the two source atoms",
            "reasoning": "the source papers recur but none occupy the fused niche, so it is novel",
            "decision": decision, "confidence": "high - all five searches agreed",
            "could_be_wrong_if": "a paper exists under vocabulary my queries never used"}


def atoms_fixture():
    return {"atoms": [
        {"atom_id": "A1", "text": "Routers softly encourage orthogonality in the router weights to balance load.", "domain": "ml"},
        {"atom_id": "A2", "text": "The hidden state is a model updated by a step of self-supervised learning at test time.", "domain": "ml"},
        {"atom_id": "A3", "text": "Off-fault damage enhances high-frequency wave radiation and reduces rupture speed.", "domain": "geology"},
    ]}


def cand(cid, a, b, mech, quote, src, niche="N"):
    return {"cand_id": cid, "atom_a_id": a, "atom_b_id": b, "niche_name": niche,
            "mechanism": mech, "primary_quote": quote, "quote_source": src,
            "reasoning_trace": good_trace()}


def verify_fixture(per):
    """per: {cid: (collision_found, n_reformulations, n_paper_hits)}"""
    cands = []
    for cid, (coll, nref, nhits) in per.items():
        reforms = []
        for n in range(nref):
            results = [{"title": f"p{n}_{i}", "url": "https://arxiv.org/pdf/1"} for i in range(nhits if n == 0 else 0)]
            reforms.append({"n": n + 1, "query": "q", "results": results})
        cands.append({"cand_id": cid, "collision_found": coll, "reformulations": reforms})
    return {"candidates": cands}


def crosscheck_fixture(per):
    return {"candidates": [{"cand_id": cid, "mismatch_with_agent3": m} for cid, m in per.items()]}


class TestGates(unittest.TestCase):
    def test_gate4_grounding(self):
        atoms = {a["atom_id"]: a for a in atoms_fixture()["atoms"]}
        c = cand("C", "A1", "A2", "the router induces orthogonality", "softly encourage orthogonality in the router weights", "atom_a")
        g = O.gate4_for(c, atoms)
        self.assertTrue(g["quote_grounded"])      # >=30-char real substring
        self.assertIn("induces", g["mechanism_verbs"])
        self.assertTrue(g["pass"])

    def test_gate4_paraphrased_quote_fails(self):
        atoms = {a["atom_id"]: a for a in atoms_fixture()["atoms"]}
        c = cand("C", "A1", "A2", "the router induces structure", "orthogonality is gently encouraged by the router", "atom_a")
        self.assertFalse(O.gate4_for(c, atoms)["quote_grounded"])

    def test_gate3_fusion(self):
        v = verify_fixture({"C": (False, 5, 0)})
        cc = crosscheck_fixture({"C": False})
        self.assertTrue(O.gate3_for("C", v, cc)["pass"])
        self.assertFalse(O.gate3_for("C", verify_fixture({"C": (False, 4, 0)}), cc)["pass"])  # too few
        self.assertFalse(O.gate3_for("C", verify_fixture({"C": (True, 5, 0)}), cc)["pass"])   # collision
        self.assertFalse(O.gate3_for("C", v, crosscheck_fixture({"C": True})["pass"] if False else crosscheck_fixture({"C": True}))["pass"])  # overturned

    def test_composite_floor_and_clear(self):
        atoms = atoms_fixture()
        c = cand("C", "A1", "A2", "the router induces orthogonality", "softly encourage orthogonality in the router weights", "atom_a")
        cands = {"candidates": [c]}
        # 0 paper hits -> novelty 1.0 -> composite 1.0 -> gate1 passes
        hi = O.run_gates(atoms, cands, verify_fixture({"C": (False, 5, 0)}), crosscheck_fixture({"C": False}))
        self.assertEqual(hi[0]["composite"], 1.0)
        self.assertTrue(hi[0]["gate_1_composite"]["pass"])
        # 12 paper hits -> novelty 0.4 -> composite 0.4*0.55+0.45=0.67 -> gate1 fails
        lo = O.run_gates(atoms, cands, verify_fixture({"C": (False, 5, 12)}), crosscheck_fixture({"C": False}))
        self.assertLess(lo[0]["composite"], 0.90)
        self.assertFalse(lo[0]["gate_1_composite"]["pass"])

    def test_every_gate_has_complete_reasoning_trace(self):
        atoms = atoms_fixture()
        c = cand("C", "A1", "A2", "the router induces orthogonality", "softly encourage orthogonality in the router weights", "atom_a")
        res = O.run_gates(atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 0)}),
                          crosscheck_fixture({"C": False}), with_traces=True)[0]
        for g in ("gate_1_composite", "gate_2_quarantine", "gate_3_verify", "gate_4_belinda"):
            tr = res[g]["reasoning_trace"]
            for f in TRACE_FIELDS:
                self.assertTrue(str(tr.get(f, "")).strip(), f"{g}.{f} empty")
        self.assertIn("SURVIVES", res["survival_reasoning_trace"]["decision"])

    def test_determinism(self):
        atoms = atoms_fixture()
        c = cand("C", "A1", "A2", "the router induces orthogonality", "softly encourage orthogonality in the router weights", "atom_a")
        args = (atoms, {"candidates": [c]}, verify_fixture({"C": (False, 5, 3)}), crosscheck_fixture({"C": False}))
        self.assertEqual(O.verdicts_hash(O.run_gates(*args)), O.verdicts_hash(O.run_gates(*args)))


class TestAudit(unittest.TestCase):
    def test_complete_trace_valid(self):
        r = A.audit_one(good_trace(), source="AGENT_3_verifier", step_id="t", linked={"collision_found": False})
        self.assertTrue(r["complete"])
        self.assertFalse(r["logic_break"])
        self.assertEqual(r["verdict"], "VALID")

    def test_incomplete_flagged(self):
        tr = good_trace(); tr["could_be_wrong_if"] = ""
        r = A.audit_one(tr, source="X", step_id="t")
        self.assertFalse(r["complete"])
        self.assertTrue(any("incomplete" in f for f in r["flags"]))

    def test_logic_break_verify(self):
        # trace claims "no collision / novel" but the recorded data says collision_found=True
        r = A.audit_one(good_trace(decision="no collision; the niche is novel and unoccupied"),
                        source="AGENT_3_verifier", step_id="t", linked={"collision_found": True})
        self.assertTrue(r["logic_break"])
        self.assertIn("LOGIC_BREAK:decision_contradicts_collision_data", r["flags"])

    def test_no_break_when_consistent(self):
        r = A.audit_one(good_trace(decision="no collision; novel niche"),
                        source="AGENT_3_verifier", step_id="t", linked={"collision_found": False})
        self.assertFalse(r["logic_break"])

    def test_logic_break_crosscheck(self):
        tr = good_trace(decision="I confirm AGENT 3's no-collision verdict; we agree")
        r = A.audit_one(tr, source="AGENT_4_crosschecker", step_id="t", linked={"mismatch_with_agent3": True})
        self.assertTrue(r["logic_break"])
        self.assertIn("LOGIC_BREAK:decision_contradicts_crosscheck_data", r["flags"])

    def test_overconfidence_flag(self):
        tr = good_trace()
        tr["confidence"] = "high - certain"
        tr["reasoning"] = "this is maybe novel but I am not sure the searches were exhaustive"
        r = A.audit_one(tr, source="X", step_id="t")
        self.assertTrue(r["overconfident"])

    def test_not_falsifiable_flag(self):
        tr = good_trace(); tr["could_be_wrong_if"] = "nothing"
        r = A.audit_one(tr, source="X", step_id="t")
        self.assertFalse(r["falsifiable"])
        self.assertIn("not_falsifiable", r["flags"])

    def test_auditor_emits_own_trace(self):
        r = A.audit_one(good_trace(), source="X", step_id="t")
        for f in TRACE_FIELDS:
            self.assertTrue(str(r["audit_reasoning_trace"].get(f, "")).strip())


class TestParsing(unittest.TestCase):
    def test_parse_obj_variants(self):
        self.assertEqual(M.parse_obj('{"a":1}')["a"], 1)
        self.assertEqual(M.parse_obj('```json\n{"a":2}\n```')["a"], 2)
        self.assertEqual(M.parse_obj('text before {"a":3} text after')["a"], 3)
        self.assertIsNone(M.parse_obj("no json here"))

    def test_trace_complete(self):
        self.assertTrue(M.trace_complete(good_trace()))
        bad = good_trace(); bad["reasoning"] = "  "
        self.assertFalse(M.trace_complete(bad))


if __name__ == "__main__":
    unittest.main(verbosity=2)
