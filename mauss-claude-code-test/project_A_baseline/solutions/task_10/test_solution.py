"""Tests for the MarkovChain text generator."""

import pytest

from solution import MarkovChain


SAMPLE = "the quick brown fox jumps over the lazy dog the quick brown fox"


def test_invalid_order():
    with pytest.raises(ValueError):
        MarkovChain(order=0)


def test_train_builds_transitions():
    mc = MarkovChain(order=1)
    mc.train(SAMPLE)
    # "the" appears followed by "quick", "lazy", "quick"
    assert "quick" in mc.transitions[("the",)]
    assert "lazy" in mc.transitions[("the",)]


def test_generate_length_words():
    mc = MarkovChain(order=1)
    mc.train(SAMPLE)
    out = mc.generate(length=10, seed=42)
    assert isinstance(out, str)
    assert len(out.split()) == 10


def test_generate_deterministic_with_seed():
    mc = MarkovChain(order=2)
    mc.train(SAMPLE)
    a = mc.generate(length=15, seed=123)
    b = mc.generate(length=15, seed=123)
    assert a == b


def test_generate_varies_by_seed():
    mc = MarkovChain(order=1)
    mc.train(SAMPLE)
    a = mc.generate(length=20, seed=1)
    b = mc.generate(length=20, seed=2)
    # With small text we may still collide, but seed change should usually differ.
    # Use richer text to reduce flakiness.
    mc2 = MarkovChain(order=1)
    mc2.train(" ".join(["alpha beta gamma delta epsilon zeta eta theta iota kappa"] * 5))
    a2 = mc2.generate(length=30, seed=1)
    b2 = mc2.generate(length=30, seed=2)
    assert (a != b) or (a2 != b2)


def test_generate_higher_order():
    mc = MarkovChain(order=2)
    mc.train(SAMPLE)
    out = mc.generate(length=8, seed=0)
    assert len(out.split()) == 8


def test_generate_zero_length():
    mc = MarkovChain(order=1)
    mc.train(SAMPLE)
    assert mc.generate(length=0, seed=1) == ""


def test_generate_without_training_raises():
    mc = MarkovChain(order=1)
    with pytest.raises(ValueError):
        mc.generate(length=5, seed=1)


def test_dead_end_restart():
    # Text where only one transition exists for the last state.
    mc = MarkovChain(order=1)
    mc.train("a b c")  # transitions: a->b, b->c; ("c",) is dead end
    out = mc.generate(length=10, seed=1)
    # Should still produce 10 words by restarting.
    assert len(out.split()) == 10


def test_generated_words_come_from_corpus():
    mc = MarkovChain(order=1)
    mc.train(SAMPLE)
    vocab = set(SAMPLE.split())
    out = mc.generate(length=25, seed=7)
    for w in out.split():
        assert w in vocab
