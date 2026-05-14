"""Tests for the Roman numeral converter."""

import pytest

from solution import from_roman, to_roman


# --- to_roman ---------------------------------------------------------------

@pytest.mark.parametrize(
    "n,expected",
    [
        (1, "I"),
        (2, "II"),
        (3, "III"),
        (4, "IV"),
        (5, "V"),
        (9, "IX"),
        (10, "X"),
        (40, "XL"),
        (49, "XLIX"),
        (50, "L"),
        (90, "XC"),
        (100, "C"),
        (400, "CD"),
        (500, "D"),
        (900, "CM"),
        (1000, "M"),
        (1994, "MCMXCIV"),
        (2024, "MMXXIV"),
        (3999, "MMMCMXCIX"),
        (444, "CDXLIV"),
        (3888, "MMMDCCCLXXXVIII"),
    ],
)
def test_to_roman(n, expected):
    assert to_roman(n) == expected


@pytest.mark.parametrize("bad", [0, -1, 4000, 10000])
def test_to_roman_out_of_range(bad):
    with pytest.raises(ValueError):
        to_roman(bad)


@pytest.mark.parametrize("bad", ["1", 1.5, None, True])
def test_to_roman_wrong_type(bad):
    with pytest.raises(TypeError):
        to_roman(bad)


# --- from_roman -------------------------------------------------------------

@pytest.mark.parametrize(
    "s,expected",
    [
        ("I", 1),
        ("II", 2),
        ("III", 3),
        ("IV", 4),
        ("V", 5),
        ("IX", 9),
        ("X", 10),
        ("XL", 40),
        ("XLIX", 49),
        ("L", 50),
        ("XC", 90),
        ("C", 100),
        ("CD", 400),
        ("D", 500),
        ("CM", 900),
        ("M", 1000),
        ("MCMXCIV", 1994),
        ("MMXXIV", 2024),
        ("MMMCMXCIX", 3999),
        ("CDXLIV", 444),
    ],
)
def test_from_roman(s, expected):
    assert from_roman(s) == expected


@pytest.mark.parametrize(
    "bad",
    [
        "IIII",   # should be IV
        "VV",     # should be X
        "IC",     # not standard subtractive
        "IL",     # not standard subtractive
        "XM",     # not standard subtractive
        "VX",     # not standard subtractive
        "MMMM",   # > 3999
        "ABC",    # invalid chars
        "",       # empty
        "iv",     # lowercase
        "MCMC",   # non-canonical
    ],
)
def test_from_roman_invalid(bad):
    with pytest.raises(ValueError):
        from_roman(bad)


@pytest.mark.parametrize("bad", [1, None, ["I"], 1.0])
def test_from_roman_wrong_type(bad):
    with pytest.raises(TypeError):
        from_roman(bad)


# --- round-trip -------------------------------------------------------------

def test_round_trip_all():
    for n in range(1, 4000):
        assert from_roman(to_roman(n)) == n


def test_to_roman_returns_str():
    assert isinstance(to_roman(42), str)


def test_from_roman_returns_int():
    assert isinstance(from_roman("XLII"), int)
