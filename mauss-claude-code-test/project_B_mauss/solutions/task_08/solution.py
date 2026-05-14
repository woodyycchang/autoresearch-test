"""Roman numeral converter with subtractive notation."""

# Ordered from largest to smallest, including subtractive pairs.
_ROMAN_PAIRS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

_ROMAN_MAP = dict(_ROMAN_PAIRS)


def to_roman(n):
    """Convert an integer in [1, 3999] to a Roman numeral string."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 1 or n > 3999:
        raise ValueError("n must be in range [1, 3999]")

    result = []
    for value, numeral in _ROMAN_PAIRS:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


def from_roman(s):
    """Convert a Roman numeral string back to an integer.

    Validates standard subtractive notation by round-tripping.
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    if not s:
        raise ValueError("empty string is not a valid Roman numeral")

    upper = s.upper()
    if upper != s:
        # Disallow lowercase to keep the canonical form strict.
        raise ValueError("Roman numeral must be uppercase")

    total = 0
    i = 0
    n = len(s)
    while i < n:
        # Check two-char subtractive pair first.
        if i + 1 < n and s[i:i + 2] in _ROMAN_MAP:
            total += _ROMAN_MAP[s[i:i + 2]]
            i += 2
        elif s[i] in _ROMAN_MAP:
            total += _ROMAN_MAP[s[i]]
            i += 1
        else:
            raise ValueError("invalid Roman numeral character: %r" % s[i])

    if total < 1 or total > 3999:
        raise ValueError("Roman numeral out of supported range")

    # Canonical-form check: reject non-standard forms like IIII, VV, IC.
    if to_roman(total) != s:
        raise ValueError("non-canonical Roman numeral: %r" % s)

    return total
