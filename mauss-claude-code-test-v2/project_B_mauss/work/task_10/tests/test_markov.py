"""Tests for the Markov chain text generator."""
from __future__ import annotations

import random

import pytest

from model import MarkovModel
from generator import MarkovGenerator
from storage import save_model, load_model


CORPUS = (
    "the quick brown fox jumps over the lazy dog "
    "the quick brown fox jumps over the lazy dog "
    "the quick brown fox sleeps under the lazy dog"
)


# ---------- training / generation -----------------------------------------


def test_train_generate_produces_known_continuations():
    """After training, generation from a known seed should produce tokens
    that appeared as continuations in the corpus (no hallucinated tokens)."""
    m = MarkovModel(order=2)
    m.train(CORPUS)
    gen = MarkovGenerator(m, rng=random.Random(42))
    out = gen.generate(seed=["the", "quick"], length=5, temperature=1.0)
    assert out[:2] == ["the", "quick"]
    # every generated token must have appeared in the corpus
    corpus_tokens = set(CORPUS.split())
    for tok in out:
        assert tok in corpus_tokens, f"generator hallucinated token: {tok!r}"


def test_generate_respects_length():
    m = MarkovModel(order=2)
    m.train(CORPUS)
    gen = MarkovGenerator(m, rng=random.Random(0))
    out = gen.generate(seed=["the", "quick"], length=4, temperature=1.0)
    # seed(2) + at most 4 generated
    assert 2 <= len(out) <= 6


def test_generator_stops_when_no_transition_available():
    """If a state has no outgoing transition, generator should stop without
    crashing (the 'falls off' failure mode)."""
    m = MarkovModel(order=2)
    m.train("a b c")  # transitions: (a,b)->c only
    gen = MarkovGenerator(m, rng=random.Random(0))
    out = gen.generate(seed=["a", "b"], length=10, temperature=1.0)
    # we expect ['a','b','c'] then stop because (b,c) has no transition
    assert out == ["a", "b", "c"]


# ---------- save / load ---------------------------------------------------


def test_save_load_roundtrip_preserves_model(tmp_path):
    m = MarkovModel(order=2)
    m.train(CORPUS)
    path = tmp_path / "model.json"
    save_model(m, path)
    assert path.exists()
    m2 = load_model(path)
    assert m2.order == m.order
    assert m == m2


def test_save_load_roundtrip_preserves_generation(tmp_path):
    """A loaded model must produce the same output as the original given
    the same seed and deterministic settings (temperature=0)."""
    m = MarkovModel(order=2)
    m.train(CORPUS)
    path = tmp_path / "m.json"
    save_model(m, path)
    m2 = load_model(path)
    g1 = MarkovGenerator(m, rng=random.Random(7))
    g2 = MarkovGenerator(m2, rng=random.Random(7))
    out1 = g1.generate(seed=["the", "quick"], length=8, temperature=0.0)
    out2 = g2.generate(seed=["the", "quick"], length=8, temperature=0.0)
    assert out1 == out2


# ---------- merge ---------------------------------------------------------


def test_merge_sums_counts_without_double_counting():
    a = MarkovModel(order=1)
    a.train("a b a b a c")  # (a,)->{b:2,c:1}, (b,)->{a:2}
    b = MarkovModel(order=1)
    b.train("a b a d")  # (a,)->{b:1,d:1}, (b,)->{a:1}

    merged = a.merge(b)
    # Expected:
    # (a,) -> b: 2+1=3, c:1, d:1
    # (b,) -> a: 2+1=3
    assert merged.next_distribution(("a",)) == {"b": 3, "c": 1, "d": 1}
    assert merged.next_distribution(("b",)) == {"a": 3}

    # Sanity: the originals must be untouched by merge (no in-place mutation).
    assert a.next_distribution(("a",)) == {"b": 2, "c": 1}
    assert b.next_distribution(("a",)) == {"b": 1, "d": 1}


def test_merge_rejects_different_orders():
    a = MarkovModel(order=1)
    a.train("a b c")
    b = MarkovModel(order=2)
    b.train("a b c d")
    with pytest.raises(ValueError):
        a.merge(b)


# ---------- temperature ---------------------------------------------------


def test_temperature_zero_is_deterministic():
    """Temperature 0 (greedy) must produce identical output across runs
    *even with different RNG seeds*."""
    m = MarkovModel(order=2)
    m.train(CORPUS)
    g1 = MarkovGenerator(m, rng=random.Random(1))
    g2 = MarkovGenerator(m, rng=random.Random(99999))
    out1 = g1.generate(seed=["the", "quick"], length=10, temperature=0.0)
    out2 = g2.generate(seed=["the", "quick"], length=10, temperature=0.0)
    assert out1 == out2


def test_temperature_zero_picks_most_frequent():
    """Greedy should pick the most common transition."""
    m = MarkovModel(order=1)
    # (a,) -> b 3 times, -> c 1 time. Greedy must pick 'b'.
    m.train("a b a b a b a c")
    g = MarkovGenerator(m, rng=random.Random(0))
    out = g.generate(seed=["a"], length=1, temperature=0.0)
    assert out == ["a", "b"]


def test_temperature_high_is_more_uniform():
    """With a heavily skewed distribution, high temperature should produce
    the minority outcome at least sometimes; low (but nonzero) temperature
    should almost always pick the majority."""
    m = MarkovModel(order=1)
    # Heavy skew: 'b' appears 19 times after 'a', 'c' once.
    tokens = ["a", "b"] * 19 + ["a", "c"]
    m.train(tokens)

    rng_hot = random.Random(0)
    g_hot = MarkovGenerator(m, rng=rng_hot)
    hot_samples = [
        g_hot.generate(["a"], 1, temperature=5.0)[1] for _ in range(400)
    ]
    # At temperature 5 the distribution flattens significantly; 'c' should
    # appear meaningfully often. With uniform-ish sampling we expect ~40%.
    c_hot = hot_samples.count("c")
    assert c_hot > 40, f"hot sampling didn't flatten enough: c={c_hot}/400"

    rng_cold = random.Random(0)
    g_cold = MarkovGenerator(m, rng=rng_cold)
    cold_samples = [
        g_cold.generate(["a"], 1, temperature=0.1)[1] for _ in range(400)
    ]
    c_cold = cold_samples.count("c")
    # At temperature 0.1 distribution is extremely peaked on 'b'.
    assert c_cold < c_hot
    assert c_cold < 20


# ---------- order=3 captures triplets ------------------------------------


def test_order_three_captures_triplets():
    """An order-3 model must distinguish continuations based on the prior
    three tokens, not just one."""
    m = MarkovModel(order=3)
    # Same bigram (b c) appears in two different triplet contexts so order=1
    # or 2 would mix them, but order=3 keeps them separate.
    m.train("a b c d a b c d x y z a b c e x y z")
    # state (a,b,c) appears followed by 'd' twice and 'e' once.
    dist = m.next_distribution(("a", "b", "c"))
    assert dist == {"d": 2, "e": 1}
    # state (b,c,d) is followed by 'a' once and 'x' once.
    dist2 = m.next_distribution(("b", "c", "d"))
    assert dist2 == {"a": 1, "x": 1}

    # Generation from a triplet seed must continue consistently with training.
    g = MarkovGenerator(m, rng=random.Random(0))
    out = g.generate(seed=["a", "b", "c"], length=1, temperature=0.0)
    # Greedy: 'd' has count 2 vs 'e' count 1
    assert out == ["a", "b", "c", "d"]


# ---------- misc edge cases ----------------------------------------------


def test_short_training_data_does_not_crash():
    m = MarkovModel(order=2)
    m.train("only two")  # too short for order=2 -> no transitions
    assert list(m.states()) == []


def test_invalid_order_rejected():
    with pytest.raises(ValueError):
        MarkovModel(order=0)
    with pytest.raises(ValueError):
        MarkovModel(order=-1)
