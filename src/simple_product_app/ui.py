"""The HTML page for listing and creating products."""

from flask import Blueprint

blueprint = Blueprint("ui", __name__)


@blueprint.get("/")
def index():
    return ""
