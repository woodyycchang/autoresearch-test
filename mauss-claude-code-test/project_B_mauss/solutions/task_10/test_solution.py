"""Pytest suite for MarkovChain (task_10)."""

import pytest

from solution import MarkovChain


def test_init_default_order():
    mc = MarkovChain()
    assert mc.order == 1
    assert mc.transitions == {}


def test_init_custom_order():
    assert MarkovChain(order=3).order == 3


def test_invalid_order():
    with pytest.raises(ValueError):
        MarkovChain(order=0)
    with pytest.raises(ValueError):
        MarkovChain(order=-2)


def test_train_builds_transitions_order1():
    mc = MarkovChain(order=1)
    mc.train("the cat sat on the mat")
    assert "cat" in mc.transitions[("the",)]
    assert "sat" in mc.transitions[("cat",)]
    assert "mat" in mc.transitions[("the",)]


def test_train_builds_transitions_order2():
    mc = MarkovChain(order=2)
    mc.train("the cat sat on the mat")
    assert mc.transitions[("the", "cat")] == ["sat"]
    assert mc.transitions[("cat", "sat")] == ["on"]


def test_train_non_string_raises():
    mc = MarkovChain()
    with pytest.raises(TypeError):
        mc.train(123)


def test_generate_length():
    mc = MarkovChain(order=1)
    mc.train("a b c d e f a b c d")
    out = mc.generate(5, seed=42)
    assert len(out.split()) == 5


def test_generate_zero_length():
    mc = MarkovChain(order=1)
    mc.train("a b c")
    assert mc.generate(0, seed=1) == ""


def test_generate_deterministic_with_seed():
    mc = MarkovChain(order=1)
    mc.train("the quick brown fox jumps over the lazy dog the end")
    a = mc.generate(8, seed=123)
    b = mc.generate(8, seed=123)
    assert a == b


def test_generate_different_seeds_can_differ():
    mc = MarkovChain(order=1)
    mc.train("a b c d e f g a b h a c i a d j")
    outputs = {mc.generate(6, seed=s) for s in range(20)}
    assert len(outputs) > 1


def test_generate_without_training_raises():
    mc = MarkovChain()
    with pytest.raises(RuntimeError):
        mc.generate(5, seed=1)


def test_generate_handles_dead_end():
    # "b" appears only at the end -> dead end. Generator must restart.
    mc = MarkovChain(order=1)
    mc.train("a b")
    out = mc.generate(10, seed=7)
    assert len(out.split()) == 10


def test_generate_words_come_from_training():
    text = "alpha beta gamma delta epsilon"
    mc = MarkovChain(order=1)
    mc.train(text)
    vocab = set(text.split())
    out = mc.generate(20, seed=9)
    assert set(out.split()).issubset(vocab)


def test_invalid_length():
    mc = MarkovChain()
    mc.train("a b c")
    with pytest.raises(ValueError):
        mc.generate(-1, seed=0)
