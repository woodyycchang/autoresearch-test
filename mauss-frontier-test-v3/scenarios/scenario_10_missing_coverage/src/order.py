class OrderTotal:
    """Calculate order total with discount, tax, and shipping.

    Args:
        items: list of (name, price, quantity)
        discount_pct: 0-100, percentage off subtotal
        tax_rate: 0-1, e.g. 0.08 for 8%
        shipping: flat shipping cost
        free_shipping_threshold: if subtotal AFTER discount >= this, shipping is free

    Returns:
        Total = ((subtotal - discount) * (1 + tax_rate)) + shipping_after_threshold
        (i.e. tax applies to discounted subtotal, not to shipping)
    """

    @staticmethod
    def calculate(items, discount_pct=0, tax_rate=0, shipping=0, free_shipping_threshold=None):
        # Bug 1: doesn't validate negative quantities (silently makes total negative)
        # Bug 2: discount_pct over 100 not capped (negative subtotal)
        # Bug 3: free_shipping_threshold check uses subtotal BEFORE discount (should be after)
        subtotal = sum(price * qty for name, price, qty in items)
        discount = subtotal * (discount_pct / 100)
        after_discount = subtotal - discount
        # Buggy threshold check:
        if free_shipping_threshold is not None and subtotal >= free_shipping_threshold:
            ship = 0
        else:
            ship = shipping
        total = after_discount * (1 + tax_rate) + ship
        return round(total, 2)
