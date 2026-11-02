"""Fixtures shared by the whole test suite."""

import pytest


@pytest.fixture
def product_name():
    """A valid product name."""
    return "Desk lamp"
