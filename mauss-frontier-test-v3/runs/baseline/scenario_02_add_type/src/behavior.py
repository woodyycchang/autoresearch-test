# Determines behavior outputs

def sound(animal):
    t = animal["type"]
    if t == "dog": return "woof"
    if t == "cat": return "meow"
    if t == "snake": return "hiss"
    raise ValueError(f"No sound for: {t}")

def movement(animal):
    t = animal["type"]
    if t == "dog": return "run"
    if t == "cat": return "prowl"
    if t == "snake": return "slither"
    raise ValueError(f"No movement for: {t}")
