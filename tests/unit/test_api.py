"""Unit tests for the JSON API's input checks, which run before any database call."""

from http import HTTPStatus

import pytest

from simple_product_app.products import NAME_REQUIRED


def test_post_products_rejects_a_blank_name(client, blank_name):
    """
    GIVEN a request whose name is only whitespace
    WHEN it is posted
    THEN the API answers 422 with the reason
    """
    response = client.post("/api/products", json={"name": blank_name})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json == {"error": NAME_REQUIRED}


@pytest.mark.xfail(
    raises=AssertionError, strict=True, reason="RED: not implemented yet"
)
def test_post_products_rejects_a_missing_name(client):
    """
    GIVEN a JSON object with no name in it
    WHEN it is posted
    THEN the API answers 422 with the reason
    """
    response = client.post("/api/products", json={})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json == {"error": NAME_REQUIRED}
