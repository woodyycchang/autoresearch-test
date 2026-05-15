from src.order import OrderTotal

def test_basic_calculate():
    # Single existing test — passes
    total = OrderTotal.calculate(
        items=[("apple", 1.0, 2)],
        discount_pct=0,
        tax_rate=0,
        shipping=5.0,
    )
    assert total == 7.0  # 2.0 + 5.0
