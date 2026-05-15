from src.pricing import format_price

def display_total(amount, currency_code=None):
    # This caller WILL pass currency_code if your refactor accepts it
    if currency_code:
        return format_price(amount, currency_code)
    return format_price(amount)
