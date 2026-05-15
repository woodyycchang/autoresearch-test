# Serializes animal back to spec dict

def to_spec(animal):
    t = animal["type"]
    if t in ("dog", "cat"):
        return {"type": t, "name": animal["name"]}
    raise ValueError(f"Cannot serialize: {t}")
