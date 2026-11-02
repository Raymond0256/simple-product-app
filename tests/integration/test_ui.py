"""Integration tests for the HTML page, against a real database."""

import re
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


def test_page_lists_the_products_oldest_first(db_client, product_names):
    """
    GIVEN products created one after another
    WHEN the page is opened
    THEN it lists their names oldest first, and no empty-list message
    """
    for name in product_names:
        db_client.post("/api/products", json={"name": name})

    page = db_client.get("/").get_data(as_text=True)

    assert re.findall(r"<li>(.*?)</li>", page) == product_names
    assert NO_PRODUCTS not in page
