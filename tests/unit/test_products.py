"""Unit tests for the product rules."""

from simple_product_app.products import clean_name


def test_clean_name_returns_the_name_without_surrounding_whitespace(product_name):
    """
    GIVEN a product name with spaces around it
    WHEN the name is cleaned
    THEN the same name comes back without the spaces
    """
    assert clean_name(f"  {product_name}  ") == product_name
