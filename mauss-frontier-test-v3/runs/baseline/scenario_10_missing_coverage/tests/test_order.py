import pytest
from src.order import OrderTotal


def test_basic_no_discount_no_tax():
    total = OrderTotal.calculate(items=[("apple", 1.0, 2)])
    assert total == 2.0


def test_empty_items():
    total = OrderTotal.calculate(items=[])
    assert total == 0.0


def test_empty_items_with_shipping():
    total = OrderTotal.calculate(items=[], shipping=5.0)
    assert total == 5.0


def test_multiple_items():
    total = OrderTotal.calculate(items=[("a", 2.0, 3), ("b", 1.5, 2)])
    # 6.0 + 3.0 = 9.0
    assert total == 9.0


def test_discount_50pct():
    total = OrderTotal.calculate(items=[("a", 10.0, 1)], discount_pct=50)
    assert total == 5.0


def test_discount_100pct():
    total = OrderTotal.calculate(items=[("a", 10.0, 1)], discount_pct=100)
    assert total == 0.0


def test_tax_only():
    total = OrderTotal.calculate(items=[("a", 100.0, 1)], tax_rate=0.08)
    assert total == 108.0


def test_discount_and_tax():
    # subtotal = 100, discount = 10, after = 90, with 10% tax = 99
    total = OrderTotal.calculate(items=[("a", 100.0, 1)], discount_pct=10, tax_rate=0.10)
    assert total == 99.0


def test_shipping_added_no_tax_on_shipping():
    # subtotal = 100, discount = 0, after = 100, tax 10% = 110, + shipping 5 = 115
    total = OrderTotal.calculate(items=[("a", 100.0, 1)], tax_rate=0.10, shipping=5.0)
    assert total == 115.0


def test_free_shipping_threshold_met_after_discount():
    # subtotal = 100, discount 50%, after = 50; threshold = 50; should be free shipping
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        discount_pct=50,
        shipping=10.0,
        free_shipping_threshold=50,
    )
    assert total == 50.0


def test_free_shipping_threshold_not_met_after_discount():
    # subtotal = 100, discount 50%, after = 50; threshold = 60; shipping applies
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        discount_pct=50,
        shipping=10.0,
        free_shipping_threshold=60,
    )
    assert total == 60.0


def test_free_shipping_bug_uses_after_discount():
    # Critical: subtotal BEFORE discount = 100 (>= 80) but AFTER discount = 50 (< 80).
    # Threshold should compare against AFTER-discount value, so shipping applies.
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        discount_pct=50,
        shipping=10.0,
        free_shipping_threshold=80,
    )
    # after_discount = 50, threshold = 80 -> shipping applies
    assert total == 60.0


def test_free_shipping_threshold_none():
    # No threshold means shipping always charged
    total = OrderTotal.calculate(
        items=[("a", 100.0, 1)],
        shipping=10.0,
        free_shipping_threshold=None,
    )
    assert total == 110.0


def test_negative_quantity_raises():
    with pytest.raises(ValueError):
        OrderTotal.calculate(items=[("a", 1.0, -1)])


def test_negative_price_raises():
    with pytest.raises(ValueError):
        OrderTotal.calculate(items=[("a", -1.0, 1)])


def test_discount_over_100_capped():
    # discount_pct = 150 should be capped at 100, leading to total = 0
    total = OrderTotal.calculate(items=[("a", 10.0, 1)], discount_pct=150)
    assert total == 0.0


def test_discount_over_100_with_shipping():
    # discount_pct 200 -> capped at 100, subtotal post-discount = 0, plus shipping
    total = OrderTotal.calculate(
        items=[("a", 10.0, 1)], discount_pct=200, shipping=5.0
    )
    assert total == 5.0


def test_zero_quantity():
    total = OrderTotal.calculate(items=[("a", 10.0, 0)])
    assert total == 0.0


def test_rounding():
    # 1.005 * 3 = 3.015 -> rounded to 2 decimal places
    total = OrderTotal.calculate(items=[("a", 1.005, 3)])
    # Python rounds 3.015 to 3.02 (banker's rounding may differ; check actual computation)
    # 1.005 * 3 = 3.0149999... so round(3.0149999..., 2) = 3.01
    assert total == round(1.005 * 3, 2)


def test_complex_scenario():
    # multiple items, discount, tax, shipping with threshold met after discount
    items = [("apple", 2.0, 3), ("bread", 5.0, 2)]
    # subtotal = 6 + 10 = 16
    # discount 25% = 4, after = 12
    # threshold = 10, after_discount (12) >= 10 -> free shipping
    # tax 10% -> 12 * 1.10 = 13.2
    total = OrderTotal.calculate(
        items=items,
        discount_pct=25,
        tax_rate=0.10,
        shipping=5.0,
        free_shipping_threshold=10,
    )
    assert total == 13.2


def test_threshold_exactly_equal():
    # after_discount == threshold -> free shipping
    total = OrderTotal.calculate(
        items=[("a", 50.0, 1)],
        shipping=10.0,
        free_shipping_threshold=50,
    )
    assert total == 50.0
