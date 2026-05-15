from src.parser import parse_animal
from src.behavior import sound

def test_dog_parse():
    a = parse_animal({"type": "dog", "name": "Buddy"})
    assert a["type"] == "dog"
    assert sound(a) == "woof"
