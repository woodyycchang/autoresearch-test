def validate_non_empty(s):
    if not isinstance(s, str) or not s.strip():
        raise ValueError("Input cannot be empty")
    return s
