"""Tests for the Markov chain text generator."""
from __future__ import annotations

import random
from collections import Counter

import pytest

from model import MarkovModel
from generator import MarkovGenerator
from storage import save, load


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

CORPUS = (
    "the quick brown fox jumps over the lazy dog "
    "the quick brown fox jumps over the lazy cat "
    "the quick brown fox sleeps under the old tree "
    "a quick brown fox jumps over the fence"
).split()

LONG_CORPUS = (
    "alpha beta gamma alpha beta gamma alpha beta delta "
    "alpha beta gamma alpha beta delta epsilon zeta eta theta"
).split()


@pytest.fixture
def trained_order2() -> MarkovModel:
    m = MarkovModel(order=2)
    m.train(CORPUS)
    return m


# ---------------------------------------------------------------------------
# 1. train -> generate produces sensible output
# ---------------------------------------------------------------------------

def test_train_then_generate_makes_sense(trained_order2):
    gen = MarkovGenerator(trained_order2, rng=random.Random(42))
    out = gen.generate(seed=["the", "quick"], length=10, temperature=1.0)

    # Seed preserved at front
    assert out[:2] == ["the", "quick"]
    # We produced more tokens than the seed
    assert len(out) > 2
    # Every generated bigram must come from the trained transitions.
    # (i.e. the generator only emits learned transitions)
    for i in range(len(out) - 2):
        state = tuple(out[i : i + 2])
        nxt = out[i + 2]
        assert state in trained_order2.transitions, (
            f"state {state!r} not in model"
        )
        assert nxt in trained_order2.transitions[state], (
            f"transition {state!r} -> {nxt!r} was never trained"
        )


def test_generate_returns_only_seed_when_length_zero(trained_order2):
    gen = MarkovGenerator(trained_order2, rng=random.Random(0))
    out = gen.generate(seed=["the", "quick"], length=0)
    assert out == ["the", "quick"]


def test_generator_seed_too_short_raises(trained_order2):
    gen = MarkovGenerator(trained_order2)
    with pytest.raises(ValueError):
        gen.generate(seed=["the"], length=5)


# ---------------------------------------------------------------------------
# 2. save / load round-trip preserves output
# ---------------------------------------------------------------------------

def test_save_load_roundtrip_preserves_model(tmp_path, trained_order2):
    path = tmp_path / "model.json"
    save(trained_order2, path)
    loaded = load(path)

    assert loaded.order == trained_order2.order
    assert loaded.transitions == trained_order2.transitions
    assert loaded == trained_order2


def test_save_load_roundtrip_preserves_generation(tmp_path, trained_order2):
    path = tmp_path / "model.json"
    save(trained_order2, path)
    loaded = load(path)

    # Same RNG seed + same model -> identical output.
    gen_a = MarkovGenerator(trained_order2, rng=random.Random(123))
    gen_b = MarkovGenerator(loaded, rng=random.Random(123))

    out_a = gen_a.generate(seed=["the", "quick"], length=15, temperature=1.0)
    out_b = gen_b.generate(seed=["the", "quick"], length=15, temperature=1.0)
    assert out_a == out_b


def test_save_load_unicode_tokens(tmp_path):
    m = MarkovModel(order=2)
    m.train(["café", "über", "naïve", "café", "über", "naïve", "café"])
    path = tmp_path / "uni.json"
    save(m, path)
    loaded = load(path)
    assert loaded == m


# ---------------------------------------------------------------------------
# 3. merge sums counts correctly (no double-count, no drop)
# ---------------------------------------------------------------------------

def test_merge_sums_counts():
    a = MarkovModel(order=1)
    a.train(["x", "y", "x", "y", "x", "z"])  # (x,)->{y:2,z:1}, (y,)->{x:2}
    b = MarkovModel(order=1)
    b.train(["x", "y", "x", "w"])  # (x,)->{y:1,w:1}, (y,)->{x:1}

    expected_x = Counter(a.next_distribution(("x",)))
    expected_x.update(b.next_distribution(("x",)))
    expected_y = Counter(a.next_distribution(("y",)))
    expected_y.update(b.next_distribution(("y",)))

    merged = a.merge(b)

    assert dict(merged.next_distribution(("x",))) == dict(expected_x)
    assert dict(merged.next_distribution(("y",))) == dict(expected_y)

    # Originals are NOT mutated (merge returns a new model).
    assert a.next_distribution(("x",)) == {"y": 2, "z": 1}
    assert b.next_distribution(("x",)) == {"y": 1, "w": 1}


def test_merge_with_disjoint_states():
    a = MarkovModel(order=1)
    a.train(["a", "b", "a", "b"])  # (a,)->{b:2}, (b,)->{a:1}
    b = MarkovModel(order=1)
    b.train(["c", "d", "c", "d"])  # (c,)->{d:2}, (d,)->{c:1}

    merged = a.merge(b)
    assert merged.next_distribution(("a",)) == {"b": 2}
    assert merged.next_distribution(("c",)) == {"d": 2}


def test_merge_order_mismatch_raises():
    a = MarkovModel(order=1)
    b = MarkovModel(order=2)
    with pytest.raises(ValueError):
        a.merge(b)


# ---------------------------------------------------------------------------
# 4. temperature == 0 -> deterministic
# ---------------------------------------------------------------------------

def test_temperature_zero_is_deterministic(trained_order2):
    seed = ["the", "quick"]
    runs = []
    for s in range(5):
        gen = MarkovGenerator(trained_order2, rng=random.Random(s))
        runs.append(gen.generate(seed=seed, length=12, temperature=0.0))
    # Every run must be identical regardless of RNG seed.
    first = runs[0]
    for r in runs[1:]:
        assert r == first


def test_temperature_zero_picks_argmax():
    m = MarkovModel(order=1)
    # After 'a': b appears 3x, c appears 1x. Greedy must pick 'b'.
    m.train(["a", "b", "a", "b", "a", "b", "a", "c"])
    gen = MarkovGenerator(m, rng=random.Random(0))
    out = gen.generate(seed=["a"], length=1, temperature=0.0)
    assert out == ["a", "b"]


# ---------------------------------------------------------------------------
# 5. order=3 captures triplets
# ---------------------------------------------------------------------------

def test_order3_captures_triplets():
    tokens = "the quick brown fox jumps the quick brown fox sleeps".split()
    m = MarkovModel(order=3)
    m.train(tokens)

    # State (the, quick, brown) followed first by 'fox' both times -> count 2
    assert ("the", "quick", "brown") in m.transitions
    assert m.next_distribution(("the", "quick", "brown")) == {"fox": 2}

    # State (quick, brown, fox) followed by 'jumps' once and 'sleeps' once
    assert m.next_distribution(("quick", "brown", "fox")) == {"jumps": 1, "sleeps": 1}


def test_order3_states_are_triples():
    m = MarkovModel(order=3)
    m.train(["a", "b", "c", "d", "e", "f"])
    for state in m.states():
        assert isinstance(state, tuple)
        assert len(state) == 3


# ---------------------------------------------------------------------------
# 6. failure-mode safety: generator falls off when no transition exists
# ---------------------------------------------------------------------------

def test_generator_falls_off_gracefully():
    # Train so that the only state has exactly one transition that leads to a dead end.
    m = MarkovModel(order=2)
    # tokens: ['a','b','c'] -> state (a,b)->{c:1}, no state (b,c).
    m.train(["a", "b", "c"])
    gen = MarkovGenerator(m, rng=random.Random(0))
    out = gen.generate(seed=["a", "b"], length=10, temperature=1.0)
    # Should produce seed + one token, then stop because (b,c) has no successor.
    assert out == ["a", "b", "c"]


def test_generator_falls_off_when_seed_unknown():
    m = MarkovModel(order=2)
    m.train(["a", "b", "c", "d"])
    gen = MarkovGenerator(m, rng=random.Random(0))
    # State (z, z) was never trained -> generator must stop immediately.
    out = gen.generate(seed=["z", "z"], length=5, temperature=1.0)
    assert out == ["z", "z"]


# ---------------------------------------------------------------------------
# 7. extras: temperature semantics
# ---------------------------------------------------------------------------

def test_temperature_one_samples_proportional_to_counts():
    m = MarkovModel(order=1)
    # After 'a': b 9x, c 1x. With temperature=1 we expect ~90% b.
    m.train(["a", "b"] * 90 + ["a", "c"] * 10)
    gen = MarkovGenerator(m, rng=random.Random(42))
    samples = [gen.generate(["a"], length=1, temperature=1.0)[-1] for _ in range(2000)]
    counts = Counter(samples)
    # Reasonable bounds around 90/10
    assert 0.80 < counts["b"] / len(samples) < 0.97
    assert 0.03 < counts["c"] / len(samples) < 0.20


def test_invalid_order_raises():
    with pytest.raises(ValueError):
        MarkovModel(order=0)
    with pytest.raises(ValueError):
        MarkovModel(order=-1)


def test_invalid_temperature_raises(trained_order2):
    gen = MarkovGenerator(trained_order2, rng=random.Random(0))
    with pytest.raises(ValueError):
        gen.generate(seed=["the", "quick"], length=3, temperature=-0.5)
