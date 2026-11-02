"""Unit tests for the product rules."""

import pytest

from simple_product_app.products import NAME_REQUIRED, clean_name


def test_clean_name_returns_the_name_without_surrounding_whitespace(product_name):
    """
    GIVEN a product name with spaces around it
    WHEN the name is cleaned
    THEN the same name comes back without the spaces
    """
    assert clean_name(f"  {product_name}  ") == product_name


@pytest.mark.xfail(
    raises=(AssertionError, pytest.fail.Exception),
    strict=True,
    reason="RED: not implemented yet",
)
def test_clean_name_rejects_a_blank_name(blank_name):
    """
    GIVEN a name made only of whitespace
    WHEN the name is cleaned
    THEN it is rejected as missing
    """
    with pytest.raises(ValueError, match=NAME_REQUIRED):
        clean_name(blank_name)
