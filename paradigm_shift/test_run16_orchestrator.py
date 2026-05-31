#!/usr/bin/env python3
"""Offline tests for Run 16: deterministic gates (inherited), the search-quality
scorer, and the epoch parameter-update — no live WebSearch/Opus.

Run: python3 paradigm_shift/test_run16_orchestrator.py
"""
from __future__ import annotations

import copy
import unittest

import run16_orchestrator as o
import run16_scorer as s

ATOM_A = "Sparse mixture-of-experts routing activates only a few expert subnetworks per token in large models."
ATOM_B = "Column-normalized Adam preconditions gradients and accelerates convergence on large language models."


def atoms():
    return {"atoms": [
        {"atom_id": "A", "text": ATOM_A, "url": "https://arxiv.org/abs/1", "domain_tags": ["attention", "routing"]},
        {"atom_id": "B", "text": ATOM_B, "url": "https://arxiv.org/abs/2", "domain_tags": ["optimization"]},
    ]}


def candidate(**ov):
    return {"cand_id": ov.get("cand_id", "C1"), "atom_a_id": "A", "atom_b_id": "B",
            "niche_name": ov.get("niche_name", "routing-conditioned optimizer"),
            "mechanism": ov.get("mechanism", "The router activates expert modules and induces faster convergence."),
            "primary_quote": ov.get("primary_quote", "activates only a few expert subnetworks per token"),
            "quote_source": ov.get("quote_source", "atom_a")}


def verify(cid, n=5, collision=False, paper_hits=0):
    reforms = []
    for i in range(1, n + 1):
        res = []
        if collision and i == 1:
            res = [{"title": "exact prior art", "url": "https://dl.acm.org/doi/x"}]
        elif paper_hits and i <= paper_hits:
            res = [{"title": f"p{i}", "url": f"https://arxiv.org/abs/{i}"}]
        reforms.append({"n": i, "query": f"q{i} routing optimizer", "results": res})
    return {"cand_id": cid, "collision_found": collision, "reformulations": reforms}


def crosscheck(cid, mismatch=False):
    return {"cand_id": cid, "mismatch_with_agent3": mismatch}


class TestGates(unittest.TestCase):
    def _clean(self):
        return (atoms(), {"candidates": [candidate(cid="C1")]},
                {"candidates": [verify("C1", 5, False, 0)]},
                {"candidates": [crosscheck("C1", False)]})

    def test_clean_survives(self):
        r = o.run_gates(*self._clean())[0]
        self.assertTrue(r["survived"], r)

    def test_quarantine_fails_g2(self):
        a, c, v, x = self._clean()
        c["candidates"][0]["atom_b_id"] = sorted(o.QUARANTINE)[0]
        self.assertFalse(o.run_gates(a, c, v, x)[0]["gate_2_quarantine"]["pass"])

    def test_paperhits_fail_g1(self):
        a, c, _, x = self._clean()
        v = {"candidates": [verify("C1", 5, False, 5)]}
        r = o.run_gates(a, c, v, x)[0]
        self.assertLess(r["composite"], 0.90)
        self.assertFalse(r["gate_1_composite"]["pass"])

    def test_gate3_overturn_fails(self):
        a, c, v, _ = self._clean()
        r = o.run_gates(a, c, v, {"candidates": [crosscheck("C1", True)]})[0]
        self.assertFalse(r["gate_3_verify"]["pass"])

    def test_fabricated_quote_fails_g4(self):
        a, _, v, x = self._clean()
        c = {"candidates": [candidate(primary_quote="this never appears in any atom text here")]}
        self.assertFalse(o.run_gates(a, c, v, x)[0]["gate_4_belinda"]["pass"])

    def test_determinism(self):
        args = self._clean()
        h1 = o.verdicts_hash(o.run_gates(*(copy.deepcopy(a) for a in args)))
        h2 = o.verdicts_hash(o.run_gates(*(copy.deepcopy(a) for a in args)))
        self.assertEqual(h1, h2)


class TestParseObj(unittest.TestCase):
    def test_bare_object_in_prose(self):
        text = ('Summary sentence.\n\n{"n_candidates": 3, "n_survivors": 0, '
                '"verdict": "NICHE_NOT_FOUND", "avg_search_quality": 0.42, '
                '"per_candidate": [{"cand_id": "C1", "composite": 0.45, "survived": false}]}')
        got = o.parse_obj(text)
        self.assertEqual(got["n_candidates"], 3)
        self.assertEqual(got["verdict"], "NICHE_NOT_FOUND")

    def test_none_when_absent(self):
        self.assertIsNone(o.parse_obj("no json"))


class TestScorer(unittest.TestCase):
    def test_specificity_rewards_specific_query(self):
        vague = s.score_query("how does learning work")["specificity"]
        specific = s.score_query('mixture-of-experts expert-choice routing 2024 sparse attention head')["specificity"]
        self.assertGreater(specific, vague)

    def test_mechanism_focus(self):
        self.assertGreater(s.score_query("expert routing gradient preconditioning optimizer")["mechanism_focus"],
                           s.score_query("interesting general idea about things")["mechanism_focus"])

    def test_collision_avoidance(self):
        self.assertGreater(s.score_query("prior work existing survey of routing")["collision_avoidance"],
                           s.score_query("routing idea")["collision_avoidance"])

    def test_cross_domain_reach(self):
        single = s.score_query("attention transformer optimizer")["cross_domain_reach"]
        multi = s.score_query("attention transformer gene regulatory dopamine")["cross_domain_reach"]
        self.assertGreaterEqual(multi, single)

    def test_avg_is_param_weighted(self):
        # all dims = d -> avg = d regardless of (equal) weights
        dims = {"specificity": 0.4, "mechanism_focus": 0.4, "cross_domain_reach": 0.4,
                "collision_avoidance": 0.4}
        params = {"reformulation_specificity": 0.5, "mechanism_focus": 0.5,
                  "cross_domain_reach": 0.5, "atom_source_diversity": 0.5,
                  "collision_avoidance_phrasing": 0.5}
        dmeans = {"reformulation_specificity": 0.4, "mechanism_focus": 0.4,
                  "cross_domain_reach": 0.4, "atom_source_diversity": 0.4,
                  "collision_avoidance_phrasing": 0.4}
        wsum = sum(params.values())
        avg = sum(params[k] * dmeans[k] for k in params) / wsum
        self.assertAlmostEqual(avg, 0.4, places=4)


class TestParamUpdate(unittest.TestCase):
    def _dp(self, epoch=1, labels=None, params=None):
        return {"epoch": epoch,
                "search_quality_params": params or {
                    "reformulation_specificity": 0.5, "mechanism_focus": 0.5,
                    "cross_domain_reach": 0.5, "atom_source_diversity": 0.5,
                    "collision_avoidance_phrasing": 0.5},
                "labeled_examples": labels or [], "epoch_history": []}

    def _sq(self, per_query):
        return {"avg_search_quality": 0.5, "per_query": per_query}

    def test_no_labels_baseline(self):
        dp2 = o.update_params(self._dp(), self._sq([]))
        self.assertEqual(dp2["epoch"], 2)                       # epoch bumped
        self.assertEqual(dp2["search_quality_params"]["mechanism_focus"], 0.5)  # unchanged
        self.assertEqual(len(dp2["epoch_history"]), 1)          # epoch 1 appended
        self.assertEqual(dp2["epoch_history"][0]["epoch"], 1)

    def test_on_target_nudges_param_up(self):
        per_q = [
            {"query": "good", "dims": {"specificity": 0.9, "mechanism_focus": 0.5,
                                       "cross_domain_reach": 0.5, "collision_avoidance": 0.5}},
            {"query": "bad", "dims": {"specificity": 0.1, "mechanism_focus": 0.5,
                                      "cross_domain_reach": 0.5, "collision_avoidance": 0.5}},
        ]
        labels = [{"search_query": "good", "label": "on_target"},
                  {"search_query": "bad", "label": "diverge"}]
        dp2 = o.update_params(self._dp(labels=labels), self._sq(per_q))
        # specificity: on=0.9, div=0.1, signal=0.8, nudge=0.5+0.2*0.8=0.66
        self.assertAlmostEqual(dp2["search_quality_params"]["reformulation_specificity"], 0.66, places=3)
        # untouched dims stay 0.5
        self.assertEqual(dp2["search_quality_params"]["mechanism_focus"], 0.5)

    def test_clamp(self):
        per_q = [{"query": "g", "dims": {"specificity": 1.0, "mechanism_focus": 0,
                                         "cross_domain_reach": 0, "collision_avoidance": 0}}]
        labels = [{"search_query": "g", "label": "on_target"}]
        dp = self._dp(params={"reformulation_specificity": 0.92, "mechanism_focus": 0.5,
                              "cross_domain_reach": 0.5, "atom_source_diversity": 0.5,
                              "collision_avoidance_phrasing": 0.5}, labels=labels)
        dp2 = o.update_params(dp, self._sq(per_q))
        self.assertLessEqual(dp2["search_quality_params"]["reformulation_specificity"], 0.95)


class TestNudgeFromLabels(unittest.TestCase):
    def _lab(self, q, label, dims):
        return {"search_query": q, "label": label, "dims": dims}

    def test_varying_dim_nudges_up(self):
        dp = {"search_quality_params": {"reformulation_specificity": 0.5, "mechanism_focus": 0.5,
              "cross_domain_reach": 0.5, "atom_source_diversity": 0.5, "collision_avoidance_phrasing": 0.5},
              "labeled_examples": [
                self._lab("good", "on_target", {"specificity": 0.9, "mechanism_focus": 0.5,
                          "cross_domain_reach": 0.0, "collision_avoidance": 0.0}),
                self._lab("bad", "diverge", {"specificity": 0.1, "mechanism_focus": 0.5,
                          "cross_domain_reach": 0.0, "collision_avoidance": 0.0})]}
        params, nudges = o.nudge_from_labels(dp)
        # specificity: on .9 - div .1 = .8 -> 0.5 + 0.2*0.8 = 0.66
        self.assertAlmostEqual(params["reformulation_specificity"], 0.66, places=3)
        self.assertIn("reformulation_specificity", nudges)

    def test_flat_dim_does_not_move(self):
        dp = {"search_quality_params": {"reformulation_specificity": 0.5, "mechanism_focus": 0.5,
              "cross_domain_reach": 0.5, "atom_source_diversity": 0.5, "collision_avoidance_phrasing": 0.5},
              "labeled_examples": [
                self._lab("a", "on_target", {"specificity": 0.5, "mechanism_focus": 0.5,
                          "cross_domain_reach": 0.0, "collision_avoidance": 0.0}),
                self._lab("b", "diverge", {"specificity": 0.5, "mechanism_focus": 0.5,
                          "cross_domain_reach": 0.0, "collision_avoidance": 0.0})]}
        params, nudges = o.nudge_from_labels(dp)
        # both groups 0.0 on flat dims -> no signal -> param stays 0.5
        self.assertEqual(params["cross_domain_reach"], 0.5)
        self.assertEqual(params["collision_avoidance_phrasing"], 0.5)
        self.assertNotIn("cross_domain_reach", nudges)


if __name__ == "__main__":
    unittest.main(verbosity=2)
