"""The HTML page for listing and creating products."""

from flask import Blueprint, render_template

blueprint = Blueprint("ui", __name__)


@blueprint.get("/")
def index():
    return render_template("index.html")
