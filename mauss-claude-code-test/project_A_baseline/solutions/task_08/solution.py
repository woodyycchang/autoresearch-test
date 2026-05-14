"""Roman numeral converter with standard subtractive notation."""

# Ordered pairs of (value, symbol) for greedy conversion.
_ROMAN_PAIRS = (
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
)

# Single-letter values for parsing.
_ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def to_roman(n):
    """Convert an integer in [1, 3999] to a Roman numeral string."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 1 or n > 3999:
        raise ValueError("n must be in [1, 3999]")

    result = []
    for value, symbol in _ROMAN_PAIRS:
        while n >= value:
            result.append(symbol)
            n -= value
    return "".join(result)


def from_roman(s):
    """Convert a Roman numeral string back to its integer value."""
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    if not s:
        raise ValueError("s must be non-empty")

    upper = s.upper()
    if upper != s:
        # Reject lowercase to keep canonical form strict.
        raise ValueError("Roman numerals must be uppercase")

    for ch in s:
        if ch not in _ROMAN_VALUES:
            raise ValueError("invalid Roman numeral character: %r" % ch)

    # Parse using subtractive notation: if a smaller numeral precedes a
    # larger one, subtract it; otherwise add it.
    total = 0
    prev = 0
    for ch in reversed(s):
        value = _ROMAN_VALUES[ch]
        if value < prev:
            total -= value
        else:
            total += value
            prev = value

    if total < 1 or total > 3999:
        raise ValueError("Roman numeral out of supported range [1, 3999]")

    # Ensure the string is in canonical form (round-trip check).
    if to_roman(total) != s:
        raise ValueError("non-canonical Roman numeral: %r" % s)

    return total
