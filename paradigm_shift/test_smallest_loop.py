#!/usr/bin/env python3
"""Tests for the deterministic core of the smallest proof-of-loop run.

These cover everything that does NOT need a real Opus call: the 4-gate filter,
the determinism contract, the verbatim-quote grounding check, and — crucially —
that the anti-hallucination checker actually has teeth (it must FLAG a wrong
claim, not just rubber-stamp a correct one).

Run:  python3 paradigm_shift/test_smallest_loop.py
"""
from __future__ import annotations

import copy
import unittest

import smallest_loop as sl  # same dir is on sys.path via smallest_loop import side effects
import multi_parameter_scorer as scorer


RULES, GP, _INPUTS = sl.load_config()
WEIGHTS = scorer.load_weights()

GROUNDED_TEXT_A = "Sparse mixture-of-experts routing activates only a few expert subnetworks per token."
GROUNDED_TEXT_B = "Regulatory gene networks selectively activate developmental modules in evo-devo."


def mk_record(**ov) -> dict:
    """A well-formed, grounded record that passes Gates 2, 3, 4 by default."""
    rec = {
        "cand_id": ov.get("cand_id", "CAND_TEST"),
        "atom_a": {"atom_id": ov.get("a_id", "ML_X"), "source_id": "s1",
                   "source_type": "arxiv", "speaker_or_author": "anon",
                   "text": ov.get("a_text", GROUNDED_TEXT_A),
                   "atom_type": "mechanism", "domain_tags": ["ml", "routing"]},
        "atom_b": {"atom_id": ov.get("b_id", "BIO_Y"), "source_id": "s2",
                   "source_type": "essay", "speaker_or_author": "anon",
                   "text": ov.get("b_text", GROUNDED_TEXT_B),
                   "atom_type": "first_principle",
                   "domain_tags": ["biology", "evodevo"]},
        "smoke_io": ov.get("smoke_io", {
            "arxiv_hit_count_24m": 1, "recent_paper_count": 2,
            "saturation_cluster_distance": 0.92,
            "arxiv_citations_supporting": ["c1", "c2", "c3", "c4", "c5"],
            "belinda_3q_passes": True}),
        "joint_topic": ov.get("joint_topic", "modular_routing_as_developmental_activation"),
        "mechanism": ov.get("mechanism",
                            "The router activates expert modules the way regulatory networks induce body plans."),
        "operator": ov.get("operator", "INDUCES"),
        # default quote is a verbatim substring of atom_a text (>=30 chars)
        "primary_quote": ov.get("primary_quote",
                               "routing activates only a few expert subnetworks per token"),
        "verification_plan": ov.get("verification_plan", [
            {"source": "arxiv", "query": "q1"},
            {"source": "openalex", "query": "q2"},
            {"source": "pubmed", "query": "q3"},
            {"source": "semanticscholar", "query": "q4"},
            {"source": "google_scholar", "query": "q5"}]),
    }
    return rec


class TestGate2Quarantine(unittest.TestCase):
    def test_quarantined_atom_dropped_in_isolation(self):
        # The candidate passes Gates 1, 3, 4; ONLY the quarantined atom_id
        # should drop it, proving Gate 2 fires on its own.
        q = GP["quarantined_atoms"][0]  # a real quarantined id from the spec
        rec = mk_record(b_id=q)
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertTrue(v["gate_1_threshold"]["pass"])
        self.assertTrue(v["gate_3_cross_llm"]["pass"])
        self.assertTrue(v["gate_4_belinda"]["pass"])
        self.assertFalse(v["gate_2_quarantine"]["pass"])
        self.assertIn(q, v["gate_2_quarantine"]["quarantine_hits"])
        self.assertEqual(v["gates_failed"], ["gate_2_quarantine"])
        self.assertFalse(v["survived"])

    def test_clean_atoms_pass_gate2(self):
        v = sl.run_four_gates(mk_record(), GP, WEIGHTS)
        self.assertTrue(v["gate_2_quarantine"]["pass"])


class TestGate3Structural(unittest.TestCase):
    def test_fewer_than_min_sources_fails(self):
        rec = mk_record(verification_plan=[{"source": "arxiv", "query": "q"},
                                           {"source": "pubmed", "query": "q"}])
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertFalse(v["gate_3_cross_llm"]["pass"])

    def test_duplicate_sources_do_not_count(self):
        rec = mk_record(verification_plan=[{"source": "arxiv", "query": "q"}] * 6)
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertEqual(v["gate_3_cross_llm"]["distinct_sources"], ["arxiv"])
        self.assertFalse(v["gate_3_cross_llm"]["pass"])

    def test_five_distinct_sources_pass(self):
        v = sl.run_four_gates(mk_record(), GP, WEIGHTS)
        self.assertTrue(v["gate_3_cross_llm"]["pass"])


class TestGate4Belinda(unittest.TestCase):
    def test_fabricated_quote_rejected(self):
        # quote not present in either atom text => grounding fails (anti-hallucination)
        rec = mk_record(primary_quote="this exact sentence appears in neither atom at all")
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertFalse(v["gate_4_belinda"]["quote_grounded"])
        self.assertFalse(v["gate_4_belinda"]["pass"])

    def test_short_quote_rejected(self):
        rec = mk_record(primary_quote="routing")  # < 30 chars
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertFalse(v["gate_4_belinda"]["pass"])

    def test_rejected_operator(self):
        rec = mk_record(operator="ANALOGY_TRANSFERS_TO_OPEN")
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertFalse(v["gate_4_belinda"]["operator_ok"])
        self.assertFalse(v["gate_4_belinda"]["pass"])

    def test_no_mechanism_verb(self):
        rec = mk_record(mechanism="It is, like, basically a big interesting thing overall.")
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertEqual(v["gate_4_belinda"]["mechanism_verbs"], [])
        self.assertFalse(v["gate_4_belinda"]["pass"])

    def test_grounded_quote_with_whitespace_diff_accepted(self):
        # extra internal whitespace must still match after normalization
        rec = mk_record(primary_quote="routing   activates only a few   expert subnetworks per token")
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertTrue(v["gate_4_belinda"]["quote_grounded"])


class TestGate1Threshold(unittest.TestCase):
    def test_low_quality_inputs_fail_threshold(self):
        rec = mk_record(
            a_text="Basically, you know, AI is gonna be like really big, obviously.",
            b_text="Right, the models just sort of get better, you know, I mean.",
            smoke_io={"arxiv_hit_count_24m": 18, "recent_paper_count": 26,
                      "saturation_cluster_distance": 0.15,
                      "arxiv_citations_supporting": [], "belinda_3q_passes": False})
        v = sl.run_four_gates(rec, GP, WEIGHTS)
        self.assertLess(v["composite"], GP["composite_threshold"])
        self.assertFalse(v["gate_1_threshold"]["pass"])

    def test_threshold_is_exact_boundary(self):
        v = sl.run_four_gates(mk_record(), GP, WEIGHTS)
        self.assertEqual(v["gate_1_threshold"]["pass"],
                         v["composite"] >= GP["composite_threshold"])


class TestFullPath(unittest.TestCase):
    def test_well_formed_record_survives_all_gates(self):
        v = sl.run_four_gates(mk_record(), GP, WEIGHTS)
        self.assertTrue(v["gate_1_threshold"]["pass"])
        self.assertTrue(v["gate_2_quarantine"]["pass"])
        self.assertTrue(v["gate_3_cross_llm"]["pass"])
        self.assertTrue(v["gate_4_belinda"]["pass"])
        self.assertTrue(v["survived"], "the survive-path must be reachable")
        self.assertIsNone(v["first_drop_gate"])


class TestVerificationSources(unittest.TestCase):
    def test_dicts_strings_and_dedup(self):
        plan = ["arxiv", "pubmed", {"source": "openalex"}, {"name": "ssrn"}, "arxiv"]
        self.assertEqual(sl.verification_sources(plan),
                         ["arxiv", "openalex", "pubmed", "ssrn"])

    def test_empty_and_blank_ignored(self):
        self.assertEqual(sl.verification_sources([{"source": ""}, "  ", {}]), [])

    def test_non_list_is_empty(self):
        self.assertEqual(sl.verification_sources(None), [])


class TestDeterminism(unittest.TestCase):
    def test_gates_are_deterministic(self):
        recs = [mk_record(cand_id="A"), mk_record(cand_id="B", b_id=GP["quarantined_atoms"][0])]
        h1 = sl.verdicts_hash(sl.gate_all(copy.deepcopy(recs), GP, WEIGHTS))
        h2 = sl.verdicts_hash(sl.gate_all(copy.deepcopy(recs), GP, WEIGHTS))
        self.assertEqual(h1, h2)

    def test_verdict_independent_of_input_object_identity(self):
        rec = mk_record()
        a = sl.run_four_gates(copy.deepcopy(rec), GP, WEIGHTS)
        b = sl.run_four_gates(copy.deepcopy(rec), GP, WEIGHTS)
        self.assertEqual(a["survived"], b["survived"])
        self.assertEqual(a["composite"], b["composite"])


class TestHallucinationChecker(unittest.TestCase):
    """The checker must have teeth: flag wrong claims, accept faithful ones."""

    def _truth(self):
        return {
            "n_candidates": 3, "n_survivors": 1, "verdict": "NICHE_FOUND",
            "per_candidate": [
                {"cand_id": "C1", "composite": 0.8700, "survived": True},
                {"cand_id": "C2", "composite": 0.8000, "survived": False},
                {"cand_id": "C3", "composite": 0.3000, "survived": False}],
        }

    def test_faithful_summary_passes(self):
        res = sl.check_hallucination(self._truth(), copy.deepcopy(self._truth()))
        self.assertTrue(res["no_hallucination"])
        self.assertEqual(res["mismatches"], [])

    def test_wrong_composite_is_caught(self):
        bad = copy.deepcopy(self._truth())
        bad["per_candidate"][0]["composite"] = 0.95  # inflated
        res = sl.check_hallucination(self._truth(), bad)
        self.assertTrue(res["hallucination_detected"])

    def test_wrong_survivor_count_is_caught(self):
        bad = copy.deepcopy(self._truth())
        bad["n_survivors"] = 2
        res = sl.check_hallucination(self._truth(), bad)
        self.assertTrue(res["hallucination_detected"])

    def test_flipped_survived_is_caught(self):
        bad = copy.deepcopy(self._truth())
        bad["per_candidate"][1]["survived"] = True
        res = sl.check_hallucination(self._truth(), bad)
        self.assertTrue(res["hallucination_detected"])

    def test_fabricated_candidate_is_caught(self):
        bad = copy.deepcopy(self._truth())
        bad["per_candidate"].append({"cand_id": "C_FAKE", "composite": 0.99, "survived": True})
        res = sl.check_hallucination(self._truth(), bad)
        self.assertTrue(res["hallucination_detected"])
        self.assertTrue(any("fabricated" in m for m in res["mismatches"]))

    def test_missing_claim_block_is_caught(self):
        res = sl.check_hallucination(self._truth(), None)
        self.assertTrue(res["hallucination_detected"])


class TestExtractJsonBlock(unittest.TestCase):
    def test_fenced_block(self):
        text = 'prose\n```json\n{"a": 1}\n```\ntrailing'
        self.assertEqual(sl.extract_json_block(text), {"a": 1})

    def test_last_block_wins(self):
        text = '```json\n{"a": 1}\n```\n```json\n{"a": 2}\n```'
        self.assertEqual(sl.extract_json_block(text), {"a": 2})

    def test_bare_object_fallback(self):
        self.assertEqual(sl.extract_json_block('result: {"x": [1,2]} done'), {"x": [1, 2]})

    def test_no_json_returns_none(self):
        self.assertIsNone(sl.extract_json_block("no json here at all"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
