#!/usr/bin/env python3
"""Offline tests for the Run 15 orchestrator's deterministic core.

Feeds synthetic agent outputs (no live WebSearch/Opus) to prove: the 4 gates,
the Gate-3 fusion of verifier+cross-checker, determinism, and that the
cross-checker overturning the verifier actually flips Gate 3.

Run: python3 paradigm_shift/test_run15_orchestrator.py
"""
from __future__ import annotations

import copy
import unittest

import run15_orchestrator as o

ATOM_A_TEXT = "Sparse mixture-of-experts routing activates only a few expert subnetworks per token in large models."
ATOM_B_TEXT = "Regulatory gene networks selectively activate developmental modules so one genome induces many body plans."


def atoms():
    return {"atoms": [
        {"atom_id": "ARXIV_A", "text": ATOM_A_TEXT, "url": "https://arxiv.org/abs/1"},
        {"atom_id": "ARXIV_B", "text": ATOM_B_TEXT, "url": "https://arxiv.org/abs/2"},
    ]}


def candidate(**ov):
    return {
        "cand_id": ov.get("cand_id", "CAND_015_001"),
        "atom_a_id": ov.get("atom_a_id", "ARXIV_A"),
        "atom_b_id": ov.get("atom_b_id", "ARXIV_B"),
        "niche_name": ov.get("niche_name", "regulatory routing of experts"),
        "mechanism": ov.get("mechanism", "The router activates expert modules and induces specialization."),
        "primary_quote": ov.get("primary_quote", "activates only a few expert subnetworks per token"),
        "quote_source": ov.get("quote_source", "atom_a"),
    }


def candidates(cands):
    return {"candidates": cands}


def verify(cid, n_reform=5, collision=False, paper_hits=0):
    reforms = []
    for i in range(1, n_reform + 1):
        results = []
        if collision and i == 1:
            results = [{"title": "Mixture-of-experts for gene regulatory networks",
                        "url": "https://dl.acm.org/doi/10.1/x"}]
        elif paper_hits and i <= paper_hits:
            results = [{"title": f"paper {i}", "url": f"https://arxiv.org/abs/{i}"}]
        reforms.append({"n": i, "query": f"q{i}", "results": results})
    return {"cand_id": cid, "collision_found": collision, "reformulations": reforms}


def crosscheck(cid, mismatch=False):
    return {"cand_id": cid, "mismatch_with_agent3": mismatch}


class TestGate4Belinda(unittest.TestCase):
    def test_grounded_quote_passes(self):
        g = o.gate4_for(candidate(), {"ARXIV_A": {"text": ATOM_A_TEXT}})
        self.assertTrue(g["quote_grounded"])
        self.assertTrue(g["pass"])

    def test_fabricated_quote_fails(self):
        g = o.gate4_for(candidate(primary_quote="this phrase appears in no atom whatsoever here"),
                        {"ARXIV_A": {"text": ATOM_A_TEXT}})
        self.assertFalse(g["quote_grounded"])
        self.assertFalse(g["pass"])

    def test_short_quote_fails(self):
        g = o.gate4_for(candidate(primary_quote="too short"), {"ARXIV_A": {"text": ATOM_A_TEXT}})
        self.assertFalse(g["pass"])

    def test_no_mechanism_verb_fails(self):
        g = o.gate4_for(candidate(mechanism="It is a big interesting thing overall, broadly."),
                        {"ARXIV_A": {"text": ATOM_A_TEXT}})
        self.assertEqual(g["mechanism_verbs"], [])
        self.assertFalse(g["pass"])


class TestGate3Fusion(unittest.TestCase):
    def test_no_collision_enough_reforms_passes(self):
        g = o.gate3_for("C1", {"candidates": [verify("C1", 5, collision=False)]},
                        {"candidates": [crosscheck("C1", mismatch=False)]})
        self.assertTrue(g["pass"])

    def test_verifier_collision_fails(self):
        g = o.gate3_for("C1", {"candidates": [verify("C1", 5, collision=True)]},
                        {"candidates": [crosscheck("C1", mismatch=False)]})
        self.assertFalse(g["pass"])

    def test_too_few_reformulations_fails(self):
        g = o.gate3_for("C1", {"candidates": [verify("C1", 3, collision=False)]},
                        {"candidates": [crosscheck("C1", mismatch=False)]})
        self.assertFalse(g["pass"])

    def test_crosschecker_overturns_no_collision(self):
        # verifier said "no collision" but cross-checker flags mismatch -> Gate 3 fails
        g = o.gate3_for("C1", {"candidates": [verify("C1", 5, collision=False)]},
                        {"candidates": [crosscheck("C1", mismatch=True)]})
        self.assertTrue(g["crosscheck_overturned"])
        self.assertFalse(g["pass"])


class TestFullGatesAndDeterminism(unittest.TestCase):
    def _scenario_survivor(self):
        a = atoms()
        c = candidates([candidate(cid="CAND_015_001")])
        v = {"candidates": [verify("CAND_015_001", 5, collision=False, paper_hits=0)]}
        x = {"candidates": [crosscheck("CAND_015_001", mismatch=False)]}
        return a, c, v, x

    def test_clean_candidate_can_survive(self):
        a, c, v, x = self._scenario_survivor()
        res = o.run_gates(a, c, v, x)[0]
        self.assertTrue(res["gate_1_composite"]["pass"], res["composite"])
        self.assertTrue(res["gate_2_quarantine"]["pass"])
        self.assertTrue(res["gate_3_verify"]["pass"])
        self.assertTrue(res["gate_4_belinda"]["pass"])
        self.assertTrue(res["survived"])

    def test_quarantined_atom_fails_gate2(self):
        a, c, v, x = self._scenario_survivor()
        c["candidates"][0]["atom_b_id"] = sorted(o.QUARANTINE)[0]
        res = o.run_gates(a, c, v, x)[0]
        self.assertFalse(res["gate_2_quarantine"]["pass"])
        self.assertFalse(res["survived"])

    def test_many_paper_hits_lowers_composite_below_090(self):
        a, c, _, x = self._scenario_survivor()
        v = {"candidates": [verify("CAND_015_001", 5, collision=False, paper_hits=5)]}
        res = o.run_gates(a, c, v, x)[0]
        self.assertLess(res["composite"], 0.90)
        self.assertFalse(res["gate_1_composite"]["pass"])

    def test_determinism_hash_stable(self):
        a, c, v, x = self._scenario_survivor()
        h1 = o.verdicts_hash(o.run_gates(copy.deepcopy(a), copy.deepcopy(c),
                                         copy.deepcopy(v), copy.deepcopy(x)))
        h2 = o.verdicts_hash(o.run_gates(copy.deepcopy(a), copy.deepcopy(c),
                                         copy.deepcopy(v), copy.deepcopy(x)))
        self.assertEqual(h1, h2)


class TestPaperHeuristics(unittest.TestCase):
    def test_is_paper(self):
        self.assertTrue(o.is_paper({"url": "https://arxiv.org/abs/1"}))
        self.assertTrue(o.is_paper({"url": "https://dl.acm.org/doi/x"}))
        self.assertFalse(o.is_paper({"url": "https://example.com/blog"}))


class TestParseObj(unittest.TestCase):
    def test_raw_object(self):
        self.assertEqual(o.parse_obj('{"a": 1}'), {"a": 1})

    def test_fenced_block(self):
        self.assertEqual(o.parse_obj('text\n```json\n{"a": 2}\n```'), {"a": 2})

    def test_bare_object_embedded_in_prose(self):
        # the real finalize case: prose summary followed by an unfenced JSON object
        text = ('This run processed 3 atoms. None survived.\n\n'
                '{"n_candidates": 3, "n_survivors": 0, "verdict": "NICHE_NOT_FOUND", '
                '"per_candidate": [{"cand_id": "CAND_015_001", "composite": 0.45, "survived": false}]}')
        got = o.parse_obj(text)
        self.assertIsNotNone(got)
        self.assertEqual(got["n_candidates"], 3)
        self.assertEqual(got["verdict"], "NICHE_NOT_FOUND")

    def test_prefers_last_object(self):
        text = '{"draft": true} ... final answer: {"n_survivors": 0, "verdict": "X"}'
        self.assertEqual(o.parse_obj(text)["verdict"], "X")

    def test_no_json_returns_none(self):
        self.assertIsNone(o.parse_obj("no json here"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
