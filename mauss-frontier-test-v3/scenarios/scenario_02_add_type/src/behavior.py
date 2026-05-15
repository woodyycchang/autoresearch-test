# Determines behavior outputs

def sound(animal):
    t = animal["type"]
    if t == "dog": return "woof"
    if t == "cat": return "meow"
    raise ValueError(f"No sound for: {t}")

def movement(animal):
    t = animal["type"]
    if t == "dog": return "run"
    if t == "cat": return "prowl"
    raise ValueError(f"No movement for: {t}")
