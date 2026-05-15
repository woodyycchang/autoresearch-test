# Visible test — passes initially. Don't break this.
from src.pricing import format_price

def test_default_currency():
    assert format_price(10.5) == "$10.50"
