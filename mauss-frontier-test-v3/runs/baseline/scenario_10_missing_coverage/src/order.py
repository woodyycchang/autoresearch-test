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
        # Validate quantities: negative quantities are not allowed
        for name, price, qty in items:
            if qty < 0:
                raise ValueError(f"Quantity cannot be negative for item {name!r}: {qty}")
            if price < 0:
                raise ValueError(f"Price cannot be negative for item {name!r}: {price}")
        # Cap discount_pct between 0 and 100
        if discount_pct < 0:
            discount_pct = 0
        if discount_pct > 100:
            discount_pct = 100
        subtotal = sum(price * qty for name, price, qty in items)
        discount = subtotal * (discount_pct / 100)
        after_discount = subtotal - discount
        # Free shipping check uses subtotal AFTER discount
        if free_shipping_threshold is not None and after_discount >= free_shipping_threshold:
            ship = 0
        else:
            ship = shipping
        total = after_discount * (1 + tax_rate) + ship
        return round(total, 2)
