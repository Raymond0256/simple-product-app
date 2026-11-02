"""JSON API for listing and creating products."""

from http import HTTPStatus

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.orm import Session

from simple_product_app.products import clean_name, create_product, list_products

blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.get("/products")
def get_products():
    with Session(current_app.extensions["db_engine"]) as session:
        products = list_products(session)
        return jsonify(
            products=[{"id": product.id, "name": product.name} for product in products]
        )


@blueprint.post("/products")
def post_product():
    try:
        name = clean_name(request.get_json()["name"])
    except ValueError as error:
        return jsonify(error=str(error)), HTTPStatus.UNPROCESSABLE_CONTENT
    with Session(current_app.extensions["db_engine"]) as session:
        product = create_product(session, name)
        return jsonify(id=product.id, name=product.name), HTTPStatus.CREATED
