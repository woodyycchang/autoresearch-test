import pytest

from src.order import OrderTotal


# --- Basic / sanity ---

def test_empty_items():
    total = OrderTotal.calculate(items=[])
    assert total == 0.0


def test_multiple_items_subtotal():
    total = OrderTotal.calculate(
        items=[("a", 2.0, 3), ("b", 1.5, 2)],
    )
    # 6 + 3 = 9
    assert total == 9.0


def test_tax_applied_to_discounted_subtotal_not_shipping():
    # subtotal = 100, discount 10% => 90, tax 10% => 99, shipping 5 (flat, no tax)
    total = OrderTotal.calculate(
        items=[("x", 100.0, 1)],
        discount_pct=10,
        tax_rate=0.10,
        shipping=5.0,
    )
    assert total == 104.0


def test_rounding_to_two_decimals():
    # 0.1 * 3 = 0.30000... -> rounds to 0.3
    total = OrderTotal.calculate(items=[("x", 0.1, 3)])
    assert total == 0.30


# --- Bug 1: negative quantities ---

def test_negative_quantity_raises():
    with pytest.raises(ValueError):
        OrderTotal.calculate(items=[("x", 5.0, -1)])


def test_negative_price_raises():
    with pytest.raises(ValueError):
        OrderTotal.calculate(items=[("x", -5.0, 1)])


# --- Bug 2: discount_pct out of range ---

def test_discount_pct_over_100_raises():
    with pytest.raises(ValueError):
        OrderTotal.calculate(items=[("x", 10.0, 1)], discount_pct=150)


def test_discount_pct_negative_raises():
    with pytest.raises(ValueError):
        OrderTotal.calculate(items=[("x", 10.0, 1)], discount_pct=-5)


def test_discount_pct_exactly_100():
    # 100% off => subtotal becomes 0; tax of 0 is fine; shipping still applies
    total = OrderTotal.calculate(
        items=[("x", 50.0, 2)],
        discount_pct=100,
        tax_rate=0.10,
        shipping=4.0,
    )
    # (100 - 100)*1.10 + 4 = 4
    assert total == 4.0


# --- Bug 3: free_shipping_threshold uses AFTER-discount subtotal ---

def test_free_shipping_uses_after_discount_subtotal_not_met():
    # subtotal 100, discount 50% => 50. Threshold 75. Should NOT get free shipping.
    total = OrderTotal.calculate(
        items=[("x", 100.0, 1)],
        discount_pct=50,
        tax_rate=0,
        shipping=10.0,
        free_shipping_threshold=75,
    )
    # after_discount=50, ship=10 -> 60
    assert total == 60.0


def test_free_shipping_uses_after_discount_subtotal_met():
    # subtotal 100, discount 10% => 90. Threshold 75. Should get free shipping.
    total = OrderTotal.calculate(
        items=[("x", 100.0, 1)],
        discount_pct=10,
        tax_rate=0,
        shipping=10.0,
        free_shipping_threshold=75,
    )
    # after_discount=90 >= 75 -> ship=0 -> 90
    assert total == 90.0


def test_free_shipping_threshold_exact_boundary():
    # after_discount exactly equals threshold => free shipping (>=)
    total = OrderTotal.calculate(
        items=[("x", 100.0, 1)],
        discount_pct=0,
        tax_rate=0,
        shipping=7.0,
        free_shipping_threshold=100,
    )
    assert total == 100.0


def test_free_shipping_threshold_none_means_always_charge():
    total = OrderTotal.calculate(
        items=[("x", 100.0, 1)],
        shipping=5.0,
        free_shipping_threshold=None,
    )
    assert total == 105.0


# --- Combined ---

def test_full_combined_calculation():
    # subtotal = 2*10 + 3*4 = 32
    # discount 25% => 8 off => 24
    # tax 5% => 25.20
    # threshold 50, after_discount=24 < 50 => shipping=6
    # total = 31.20
    total = OrderTotal.calculate(
        items=[("a", 10.0, 2), ("b", 4.0, 3)],
        discount_pct=25,
        tax_rate=0.05,
        shipping=6.0,
        free_shipping_threshold=50,
    )
    assert total == 31.20
