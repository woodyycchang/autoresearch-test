from src.pricing import format_price

def generate_invoice(items):
    lines = []
    for item, price in items:
        lines.append(f"{item}: {format_price(price)}")
    return "\n".join(lines)
