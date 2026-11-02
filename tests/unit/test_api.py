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


def test_post_products_rejects_a_missing_name(client):
    """
    GIVEN a JSON object with no name in it
    WHEN it is posted
    THEN the API answers 422 with the reason
    """
    response = client.post("/api/products", json={})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json == {"error": NAME_REQUIRED}


@pytest.mark.parametrize("name", [42, True, ["not", "a", "string"]])
def test_post_products_rejects_a_name_that_is_not_a_string(client, name):
    """
    GIVEN a JSON object whose name is a number, a boolean or a list
    WHEN it is posted
    THEN the API answers 422 with the reason
    """
    response = client.post("/api/products", json={"name": name})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json == {"error": NAME_REQUIRED}


@pytest.mark.parametrize("body", ["[]", '"a string"', "null"])
def test_post_products_rejects_a_body_that_is_not_a_json_object(client, body):
    """
    GIVEN a JSON body that is an array, a string or null
    WHEN it is posted
    THEN the API answers 422 with the reason
    """
    response = client.post("/api/products", data=body, content_type="application/json")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json == {"error": NAME_REQUIRED}


@pytest.mark.xfail(
    raises=AssertionError, strict=True, reason="RED: not implemented yet"
)
@pytest.mark.parametrize(
    ("body", "content_type", "status"),
    [
        ('{"name": ', "application/json", HTTPStatus.BAD_REQUEST),
        (
            "name=x",
            "application/x-www-form-urlencoded",
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        ),
    ],
    ids=["malformed-json", "not-json"],
)
def test_post_products_reports_unreadable_bodies_as_json_errors(
    client, body, content_type, status
):
    """
    GIVEN a body that is broken JSON, or not JSON at all
    WHEN it is posted
    THEN the API answers with Flask's status for it, as a JSON error
    """
    response = client.post("/api/products", data=body, content_type=content_type)

    assert response.status_code == status
    assert response.is_json
    assert list(response.json) == ["error"]
