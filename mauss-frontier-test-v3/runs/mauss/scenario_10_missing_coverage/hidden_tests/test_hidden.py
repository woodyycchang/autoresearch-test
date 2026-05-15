import pytest
from src.order import OrderTotal

def test_with_discount():
    total = OrderTotal.calculate(
        items=[("a", 10.0, 1)],
        discount_pct=10,
        tax_rate=0,
        shipping=0,
    )
    assert total == 9.0

def test_with_tax():
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        tax_rate=0.10,
    )
    assert total == 110.0

def test_discount_then_tax():
    # 100 - 10% = 90, then * 1.08 = 97.2
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        discount_pct=10,
        tax_rate=0.08,
    )
    assert total == 97.2

def test_negative_quantity_rejected():
    # Bug 1: should not produce negative total
    with pytest.raises((ValueError, AssertionError)):
        OrderTotal.calculate(items=[("a", 10.0, -1)])

def test_discount_over_100_capped():
    # Bug 2: discount of 150% shouldn't go negative
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        discount_pct=150,
    )
    assert total >= 0, f"Negative total from over-100 discount: {total}"

def test_free_shipping_threshold_uses_discounted_total():
    # Bug 3: threshold should check AFTER discount, not before
    # Subtotal 100, 50% off = 50, threshold 75 → should NOT get free shipping
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        discount_pct=50,
        shipping=10,
        free_shipping_threshold=75,
    )
    # Discounted = 50, 50 < 75, so shipping should apply
    assert total == 60.0, f"Free shipping applied incorrectly: total={total}"

def test_free_shipping_when_qualifies():
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        shipping=10,
        free_shipping_threshold=50,
    )
    assert total == 100.0  # subtotal 100 >= 50 threshold, no shipping
