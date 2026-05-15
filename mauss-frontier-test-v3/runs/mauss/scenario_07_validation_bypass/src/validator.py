def validate_non_empty(s):
    if s is None or not isinstance(s, str) or s.strip() == "":
        raise ValueError("Input cannot be empty")
