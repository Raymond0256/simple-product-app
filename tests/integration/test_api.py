"""Integration tests for the JSON API, against a real database."""

import uuid
from http import HTTPStatus

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.integration

TIME_ORDERED_UUID_VERSION = 7


def stored_names(engine):
    """The product names in the database, read straight from the table."""
    with engine.connect() as connection:
        return connection.execute(text("SELECT name FROM products")).scalars().all()


def test_post_products_creates_a_product(db_client, db_engine, product_name):
    """
    GIVEN an empty products table
    WHEN a product is posted with a name
    THEN the API answers 201 with the new product, and the product is stored
    """
    response = db_client.post("/api/products", json={"name": product_name})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json["name"] == product_name
    assert uuid.UUID(response.json["id"]).version == TIME_ORDERED_UUID_VERSION
    assert stored_names(db_engine) == [product_name]


def test_get_products_lists_products_in_creation_order(db_client, product_names):
    """
    GIVEN products created one after another
    WHEN the products are listed
    THEN they come back oldest first, each with its id and name
    """
    created = [
        db_client.post("/api/products", json={"name": name}).json
        for name in product_names
    ]

    response = db_client.get("/api/products")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"products": created}


def test_post_products_stores_the_name_trimmed(db_client, db_engine, product_name):
    """
    GIVEN a name with spaces around it
    WHEN it is posted
    THEN the API returns and stores the name without the spaces
    """
    response = db_client.post("/api/products", json={"name": f"  {product_name}  "})

    assert response.json["name"] == product_name
    assert stored_names(db_engine) == [product_name]


def test_post_products_ignores_unknown_fields(db_client, db_engine, product_name):
    """
    GIVEN a request with a field the API doesn't know
    WHEN it is posted
    THEN the product is created from its name alone
    """
    response = db_client.post(
        "/api/products", json={"name": product_name, "colour": "red"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert set(response.json) == {"id", "name"}
    assert stored_names(db_engine) == [product_name]
