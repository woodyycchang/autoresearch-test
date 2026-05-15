# Parses animal-spec dict into instance descriptor

def parse_animal(spec):
    t = spec.get("type")
    if t == "dog":
        return {"type": "dog", "name": spec.get("name", "Rex")}
    if t == "cat":
        return {"type": "cat", "name": spec.get("name", "Whiskers")}
    if t == "snake":
        return {"type": "snake", "name": spec.get("name", "Slinky")}
    raise ValueError(f"Unknown animal type: {t}")
