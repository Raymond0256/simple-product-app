"""Fixtures shared by the whole test suite."""

import pytest


@pytest.fixture
def product_name():
    """A valid product name."""
    return "Desk lamp"


@pytest.fixture
def blank_name():
    """A name made only of whitespace."""
    return "   "
