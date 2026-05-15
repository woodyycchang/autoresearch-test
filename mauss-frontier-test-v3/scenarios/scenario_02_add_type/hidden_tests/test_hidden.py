from src.parser import parse_animal
from src.behavior import sound, movement
from src.serializer import to_spec

def test_snake_parse():
    a = parse_animal({"type": "snake", "name": "Slither"})
    assert a["type"] == "snake"
    assert a["name"] == "Slither"

def test_snake_sound():
    a = parse_animal({"type": "snake", "name": "S"})
    assert sound(a) == "hiss"

def test_snake_movement():
    a = parse_animal({"type": "snake", "name": "S"})
    assert movement(a) == "slither"

def test_snake_serialize():
    a = parse_animal({"type": "snake", "name": "S"})
    spec = to_spec(a)
    assert spec == {"type": "snake", "name": "S"}

def test_existing_types_still_work():
    d = parse_animal({"type": "dog", "name": "Buddy"})
    assert sound(d) == "woof" and movement(d) == "run"
    c = parse_animal({"type": "cat", "name": "Mr"})
    assert sound(c) == "meow" and movement(c) == "prowl"
