"""Integration tests for the HTML page, against a real database."""

from http import HTTPStatus

import pytest

pytestmark = pytest.mark.integration

NAME_LABEL = '<label for="name">Name</label>'
NAME_FIELD = 'name="name"'
CREATE_BUTTON = "Create product"
NO_PRODUCTS = "No products yet."


def test_page_shows_the_form_and_says_when_there_are_no_products(db_client):
    """
    GIVEN no products
    WHEN the page is opened
    THEN it shows the labelled name field, the create button, and an empty-list message
    """
    response = db_client.get("/")

    assert response.status_code == HTTPStatus.OK
    page = response.get_data(as_text=True)
    assert NAME_LABEL in page
    assert NAME_FIELD in page
    assert CREATE_BUTTON in page
    assert NO_PRODUCTS in page
