"""Tests for the Roman numeral converter."""

import pytest

from solution import from_roman, to_roman


KNOWN_PAIRS = [
    (1, "I"),
    (2, "II"),
    (3, "III"),
    (4, "IV"),
    (5, "V"),
    (9, "IX"),
    (10, "X"),
    (14, "XIV"),
    (19, "XIX"),
    (40, "XL"),
    (49, "XLIX"),
    (50, "L"),
    (90, "XC"),
    (99, "XCIX"),
    (100, "C"),
    (400, "CD"),
    (444, "CDXLIV"),
    (500, "D"),
    (900, "CM"),
    (999, "CMXCIX"),
    (1000, "M"),
    (1987, "MCMLXXXVII"),
    (2024, "MMXXIV"),
    (3000, "MMM"),
    (3888, "MMMDCCCLXXXVIII"),
    (3999, "MMMCMXCIX"),
]


@pytest.mark.parametrize("n,roman", KNOWN_PAIRS)
def test_to_roman_known_values(n, roman):
    assert to_roman(n) == roman


@pytest.mark.parametrize("n,roman", KNOWN_PAIRS)
def test_from_roman_known_values(n, roman):
    assert from_roman(roman) == n


def test_roundtrip_full_range():
    for n in range(1, 4000):
        assert from_roman(to_roman(n)) == n


def test_to_roman_below_range():
    with pytest.raises(ValueError):
        to_roman(0)


def test_to_roman_above_range():
    with pytest.raises(ValueError):
        to_roman(4000)


def test_to_roman_negative():
    with pytest.raises(ValueError):
        to_roman(-3)


def test_to_roman_type_error_float():
    with pytest.raises(TypeError):
        to_roman(3.5)


def test_to_roman_type_error_str():
    with pytest.raises(TypeError):
        to_roman("3")


def test_to_roman_rejects_bool():
    with pytest.raises(TypeError):
        to_roman(True)


def test_from_roman_empty_string():
    with pytest.raises(ValueError):
        from_roman("")


def test_from_roman_invalid_character():
    with pytest.raises(ValueError):
        from_roman("IIA")


def test_from_roman_lowercase_rejected():
    with pytest.raises(ValueError):
        from_roman("iv")


def test_from_roman_type_error():
    with pytest.raises(TypeError):
        from_roman(4)


def test_from_roman_non_canonical_iiii():
    # 4 must be IV, not IIII
    with pytest.raises(ValueError):
        from_roman("IIII")


def test_from_roman_non_canonical_vv():
    # 10 must be X, not VV
    with pytest.raises(ValueError):
        from_roman("VV")


def test_from_roman_non_canonical_ic():
    # 99 must be XCIX, not IC
    with pytest.raises(ValueError):
        from_roman("IC")


def test_from_roman_non_canonical_repeats():
    with pytest.raises(ValueError):
        from_roman("MMMM")
