# HIDDEN — checks all callers + new currency feature
from src.pricing import format_price
from src.billing import generate_invoice
from src.report import revenue_summary
from src.cart import display_total

def test_default_still_usd():
    assert format_price(10.5) == "$10.50"

def test_eur_currency():
    assert format_price(10.5, "EUR") == "€10.50" or format_price(10.5, currency="EUR") == "€10.50"

def test_invoice_still_works():
    result = generate_invoice([("apple", 1.5), ("bread", 3.0)])
    assert "$1.50" in result
    assert "$3.00" in result

def test_report_positional_caller():
    # The trap: report.py passes positional arg, signature change must preserve this
    assert "$100.00" in revenue_summary(100)

def test_cart_eur():
    # cart.py passes currency as 2nd positional or kwarg
    assert "€" in display_total(50.0, "EUR")

def test_cart_default():
    assert "$50.00" in display_total(50.0)
