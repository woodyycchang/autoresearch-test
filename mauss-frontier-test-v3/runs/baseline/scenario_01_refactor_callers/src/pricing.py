def format_price(amount, currency="USD"):
    symbol = "€" if currency == "EUR" else "$"
    return f"{symbol}{amount:.2f}"
