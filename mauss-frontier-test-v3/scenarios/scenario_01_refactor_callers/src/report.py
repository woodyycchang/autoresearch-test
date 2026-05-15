from src.pricing import format_price

def revenue_summary(total):
    # NOTE: passes positional only
    return f"Total revenue: {format_price(total)}"
