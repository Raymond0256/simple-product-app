"""JSON API for listing and creating products."""

from http import HTTPStatus

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException

from simple_product_app.db import open_session
from simple_product_app.products import clean_name, create_product, list_products

blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.get("/products")
def get_products():
    with open_session() as session:
        products = list_products(session)
        return jsonify(
            products=[{"id": product.id, "name": product.name} for product in products]
        )


@blueprint.post("/products")
def post_product():
    payload = request.get_json()
    value = payload.get("name") if isinstance(payload, dict) else None
    try:
        name = clean_name(value)
    except ValueError as error:
        return jsonify(error=str(error)), HTTPStatus.UNPROCESSABLE_CONTENT
    with open_session() as session:
        product = create_product(session, name)
        return jsonify(id=product.id, name=product.name), HTTPStatus.CREATED


@blueprint.errorhandler(HTTPException)
def http_error(error: HTTPException):
    """Send Flask's own errors, such as 400 and 415, as JSON instead of HTML."""
    return jsonify(error=error.description), error.code
