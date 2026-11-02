"""JSON API for listing and creating products."""

from flask import Blueprint, jsonify

blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.post("/products")
def post_product():
    return jsonify({}), 501
