#!/usr/bin/env python3
"""Tests for the deterministic core of Step 2 (real-I/O smallest loop).

No live WebSearch or Opus needed: real_io results are injected as mock dicts so
the count-derivation, the executed Gate-3 collision rule, the determinism
contract, and the Step-2 hallucination checker can all be verified offline —
including that the collision rule and the checker have teeth.

Run:  python3 paradigm_shift/test_smallest_loop_step2.py
"""
from __future__ import annotations

import copy
import unittest

import smallest_loop_step2 as s2
import multi_parameter_scorer as scorer

RULES, GP, _IN = s2.load_config()
WEIGHTS = scorer.load_weights()

A_TXT = "Sparse mixture-of-experts routing activates only a few expert subnetworks per token."
B_TXT = "Regulatory gene networks selectively activate developmental modules so a single genome induces many distinct body plans depending on which modules switch on."


def mk_frozen(cid="C1", **ov):
    return {
        "cand_id": cid,
        "atom_a": {"atom_id": ov.get("a_id", "ML_X"), "source_id": "s1",
                   "source_type": "arxiv", "speaker_or_author": "anon",
                   "text": A_TXT, "atom_type": "mechanism",
                   "domain_tags": ["ml", "routing"]},
        "atom_b": {"atom_id": ov.get("b_id", "BIO_Y"), "source_id": "s2",
                   "source_type": "essay", "speaker_or_author": "anon",
                   "text": B_TXT, "atom_type": "first_principle",
                   "domain_tags": ["biology", "evodevo"]},
        "joint_topic": ov.get("joint_topic", "developmental routing of expert modules"),
        "mechanism": ov.get("mechanism",
                            "The router activates expert modules the way regulatory networks induce body plans."),
        "operator": ov.get("operator", "INDUCES"),
        "primary_quote": ov.get("primary_quote",
                               "routing activates only a few expert subnetworks per token"),
        "content_words": ov.get("content_words",
                               ["activates", "developmental", "evodevo", "expert",
                                "modules", "regulatory", "routing"]),
    }


def dict_io(mapping):
    return lambda name: mapping.get(name)


class TestContentWords(unittest.TestCase):
    def test_excludes_generic_keeps_distinctive(self):
        cw = s2.content_words("A novel neural network for developmental routing of experts")
        self.assertIn("developmental", cw)
        self.assertIn("routing", cw)
        for generic in ("neural", "network", "novel"):
            self.assertNotIn(generic, cw)

    def test_dedup_and_sorted(self):
        cw = s2.content_words("routing routing morphogenesis")
        self.assertEqual(cw, sorted(set(cw)))
        self.assertEqual(cw.count("routing"), 1)


class TestPaperHeuristics(unittest.TestCase):
    def test_is_arxiv_and_is_paper(self):
        self.assertTrue(s2.is_arxiv({"url": "https://arxiv.org/abs/2401.00001"}))
        self.assertTrue(s2.is_paper({"url": "https://doi.org/10.1/x"}))
        self.assertTrue(s2.is_paper({"url": "https://openreview.net/forum?id=x"}))
        self.assertFalse(s2.is_paper({"url": "https://example.com/blog"}))
        self.assertFalse(s2.is_arxiv({"url": "https://news.site/post"}))

    def test_overlap_count(self):
        res = {"title": "Routing experts", "snippet": "developmental modules activate"}
        ov = s2.overlap_count(res, ["routing", "developmental", "morphogenesis"])
        self.assertEqual(set(ov), {"routing", "developmental"})


class TestBelindaGate(unittest.TestCase):
    def test_grounded_mechanism_passes(self):
        self.assertTrue(s2.belinda_gate(mk_frozen(), GP)["pass"])

    def test_fabricated_quote_fails(self):
        g = s2.belinda_gate(mk_frozen(primary_quote="not present in any atom text here"), GP)
        self.assertFalse(g["quote_grounded"])
        self.assertFalse(g["pass"])

    def test_rejected_operator_fails(self):
        self.assertFalse(s2.belinda_gate(mk_frozen(operator="ANALOGY_TRANSFERS_TO_OPEN"), GP)["pass"])


class TestGate12RealInputs(unittest.TestCase):
    def _io(self, cid, n_arxiv_novelty, n_recent):
        nov = {"results": [{"url": f"https://arxiv.org/abs/24{i:02d}.1",
                            "title": f"paper {i}", "snippet": ""}
                           for i in range(n_arxiv_novelty)]}
        com = {"results": [{"url": f"https://doi.org/10.1/{i}",
                            "title": f"recent {i}", "snippet": "2025"}
                           for i in range(n_recent)]}
        return {f"novelty_{cid}.json": nov, f"community_{cid}.json": com}

    def test_counts_derived_from_results(self):
        f = mk_frozen("C1")
        io = self._io("C1", n_arxiv_novelty=3, n_recent=4)
        r = s2.compute_gate12([f], GP, WEIGHTS, dict_io(io))[0]
        self.assertEqual(r["real_arxiv_hit_count"], 3)
        self.assertEqual(r["real_recent_paper_count"], 4)

    def test_only_near_absent_literature_passes_gate1(self):
        # With REAL inputs, Gate 1 (>=0.85) clears only when the idea is nearly
        # absent from the literature: 0 arxiv hits AND 0 recent papers.
        f = mk_frozen("C1")
        clear = s2.compute_gate12([f], GP, WEIGHTS, dict_io(self._io("C1", 0, 0)))[0]
        self.assertTrue(clear["gate_1_threshold"]["pass"], clear["composite"])
        self.assertTrue(clear["passed_g12"])

    def test_a_few_real_hits_fail_gate1(self):
        # Even a handful of real prior-art hits drops the composite below 0.85.
        f = mk_frozen("C1")
        r = s2.compute_gate12([f], GP, WEIGHTS, dict_io(self._io("C1", 1, 2)))[0]
        self.assertFalse(r["gate_1_threshold"]["pass"], r["composite"])
        self.assertFalse(r["passed_g12"])

    def test_arxiv_grounding_is_neutral_half(self):
        f = mk_frozen("C1")
        r = s2.compute_gate12([f], GP, WEIGHTS, dict_io(self._io("C1", 0, 0)))[0]
        self.assertEqual(r["params"]["arxiv_grounding"], 0.5)
        self.assertEqual(r["arxiv_grounding_policy"], "neutral_0.5_deferred_to_step3")

    def test_many_hits_lowers_novelty(self):
        f = mk_frozen("C1")
        few = s2.compute_gate12([f], GP, WEIGHTS, dict_io(self._io("C1", 1, 1)))[0]
        many = s2.compute_gate12([f], GP, WEIGHTS, dict_io(self._io("C1", 20, 30)))[0]
        self.assertLess(many["params"]["novelty_score"], few["params"]["novelty_score"])

    def test_quarantined_atom_fails_gate2(self):
        q = GP["quarantined_atoms"][0]
        f = mk_frozen("C1", b_id=q)
        r = s2.compute_gate12([f], GP, WEIGHTS, dict_io(self._io("C1", 1, 1)))[0]
        self.assertFalse(r["gate_2_quarantine"]["pass"])
        self.assertFalse(r["passed_g12"])

    def test_missing_io_is_zero_not_crash(self):
        f = mk_frozen("C1")
        r = s2.compute_gate12([f], GP, WEIGHTS, dict_io({}))[0]
        self.assertEqual(r["real_arxiv_hit_count"], 0)
        self.assertEqual(r["real_recent_paper_count"], 0)


class TestGate3Executed(unittest.TestCase):
    def _g12_pass(self, cid="C1"):
        return [{"cand_id": cid, "passed_g12": True}]

    def _verify(self, cid, reformulations):
        return {f"verify_{cid}.json": {"reformulations": reformulations}}

    def test_collision_when_paper_overlaps_two_words(self):
        reforms = [{"n": i, "query": f"q{i}", "results": []} for i in range(1, 5)]
        reforms.append({"n": 5, "query": "q5", "results": [
            {"url": "https://arxiv.org/abs/2401.1",
             "title": "Routing developmental experts", "snippet": "modules"}]})
        out = s2.compute_gate3(self._g12_pass(), [mk_frozen("C1")], GP,
                               dict_io(self._verify("C1", reforms)))[0]
        self.assertTrue(out["collided_any"])
        self.assertFalse(out["gate_3_executed_verify"]["pass"])

    def test_no_collision_when_results_clear(self):
        # 5 reformulations, results are non-papers or <2 overlap -> no collision
        reforms = [{"n": i, "query": f"q{i}", "results": [
            {"url": "https://news.site/post", "title": "Routing only", "snippet": ""}]}
            for i in range(1, 6)]
        out = s2.compute_gate3(self._g12_pass(), [mk_frozen("C1")], GP,
                               dict_io(self._verify("C1", reforms)))[0]
        self.assertFalse(out["collided_any"])
        self.assertTrue(out["gate_3_executed_verify"]["pass"])

    def test_paper_with_one_overlap_is_not_collision(self):
        reforms = [{"n": i, "query": f"q{i}", "results": [
            {"url": "https://arxiv.org/abs/2401.1", "title": "Routing in general",
             "snippet": "nothing else relevant"}]} for i in range(1, 6)]
        out = s2.compute_gate3(self._g12_pass(), [mk_frozen("C1")], GP,
                               dict_io(self._verify("C1", reforms)))[0]
        self.assertFalse(out["collided_any"])
        self.assertTrue(out["gate_3_executed_verify"]["pass"])

    def test_fewer_than_five_reformulations_fails(self):
        reforms = [{"n": i, "query": f"q{i}", "results": []} for i in range(1, 4)]
        out = s2.compute_gate3(self._g12_pass(), [mk_frozen("C1")], GP,
                               dict_io(self._verify("C1", reforms)))[0]
        self.assertFalse(out["gate_3_executed_verify"]["pass"])


class TestGate3Demonstration(unittest.TestCase):
    """A Gate-1 failure can still be RUN through Gate 3 as a labeled demo, but
    a demo must NEVER be promoted to survivor."""

    def _verify(self, cid, reforms):
        return {f"verify_{cid}.json": {"reformulations": reforms}}

    def test_demo_runs_even_when_g12_failed(self):
        g12 = [{"cand_id": "C1", "passed_g12": False}]
        reforms = [{"n": i, "query": f"q{i}", "results": []} for i in range(1, 6)]
        out = s2.compute_gate3(g12, [mk_frozen("C1")], GP,
                               dict_io(self._verify("C1", reforms)), demo_ids={"C1"})
        self.assertEqual(len(out), 1)
        self.assertTrue(out[0]["is_demonstration"])

    def test_demo_does_not_run_without_demo_id(self):
        g12 = [{"cand_id": "C1", "passed_g12": False}]
        out = s2.compute_gate3(g12, [mk_frozen("C1")], GP, dict_io({}), demo_ids=set())
        self.assertEqual(out, [])

    def test_demonstration_never_promotes_to_survivor(self):
        # C1 fails Gate 1 (real arxiv hits) but its demo Gate-3 has no collision.
        f = mk_frozen("C1")
        io = {"novelty_C1.json": {"results": [
                  {"url": f"https://arxiv.org/abs/24{i:02d}.1", "title": f"p{i}"} for i in range(8)]},
              "community_C1.json": {"results": []},
              "verify_C1.json": {"reformulations": [
                  {"n": i, "query": "q", "results": []} for i in range(1, 6)]}}
        load = dict_io(io)
        g12 = s2.compute_gate12([f], GP, WEIGHTS, load)
        self.assertFalse(g12[0]["gate_1_threshold"]["pass"])  # dropped by real novelty
        g3 = s2.compute_gate3(g12, [f], GP, load, demo_ids={"C1"})
        self.assertTrue(g3[0]["is_demonstration"])
        self.assertTrue(g3[0]["gate_3_executed_verify"]["pass"])  # no collision
        v = s2.assemble_verdicts(g12, g3)[0]
        self.assertTrue(v["gate_3_executed"])          # demo result is recorded
        self.assertTrue(v["gate_3_is_demonstration"])
        self.assertFalse(v["survived"])                # but it is NOT a survivor
        self.assertIn("gate_1_threshold", v["gates_failed"])


class TestDeterminism(unittest.TestCase):
    def test_pipeline_hash_stable(self):
        f = mk_frozen("C1")
        io = {"novelty_C1.json": {"results": [{"url": "https://arxiv.org/abs/1", "title": "x"}]},
              "community_C1.json": {"results": []},
              "verify_C1.json": {"reformulations": [
                  {"n": i, "query": "q", "results": []} for i in range(1, 6)]}}
        load = dict_io(io)
        g12a = s2.compute_gate12([f], GP, WEIGHTS, load)
        g3a = s2.compute_gate3(g12a, [f], GP, load)
        va = s2.assemble_verdicts(g12a, g3a)
        g12b = s2.compute_gate12([copy.deepcopy(f)], GP, WEIGHTS, load)
        g3b = s2.compute_gate3(g12b, [f], GP, load)
        vb = s2.assemble_verdicts(g12b, g3b)
        self.assertEqual(s2.verdicts_hash(va), s2.verdicts_hash(vb))


class TestHallucinationCheckerStep2(unittest.TestCase):
    def _truth(self):
        return {"n_candidates": 2, "n_survivors": 0, "verdict": "NICHE_NOT_FOUND",
                "per_candidate": [
                    {"cand_id": "C1", "composite": 0.86, "real_arxiv_hit_count": 4, "survived": False},
                    {"cand_id": "C2", "composite": 0.40, "real_arxiv_hit_count": 9, "survived": False}]}

    def test_faithful_passes(self):
        self.assertTrue(s2.check_hallucination(self._truth(), copy.deepcopy(self._truth()))["no_hallucination"])

    def test_wrong_arxiv_count_caught(self):
        bad = copy.deepcopy(self._truth())
        bad["per_candidate"][0]["real_arxiv_hit_count"] = 0  # pretend it was novel
        self.assertTrue(s2.check_hallucination(self._truth(), bad)["hallucination_detected"])

    def test_wrong_composite_caught(self):
        bad = copy.deepcopy(self._truth())
        bad["per_candidate"][0]["composite"] = 0.99
        self.assertTrue(s2.check_hallucination(self._truth(), bad)["hallucination_detected"])

    def test_flipped_survived_caught(self):
        bad = copy.deepcopy(self._truth())
        bad["per_candidate"][0]["survived"] = True
        bad["n_survivors"] = 1
        self.assertTrue(s2.check_hallucination(self._truth(), bad)["hallucination_detected"])

    def test_missing_block_caught(self):
        self.assertTrue(s2.check_hallucination(self._truth(), None)["hallucination_detected"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
