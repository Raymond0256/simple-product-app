"""The HTML page for listing and creating products."""

from http import HTTPStatus

from flask import Blueprint, redirect, render_template, request, url_for

from simple_product_app.db import open_session
from simple_product_app.products import clean_name, create_product, list_products

blueprint = Blueprint("ui", __name__)


def render_page(name: str = "", error: str | None = None) -> str:
    """The page, with every product and the form's current state."""
    with open_session() as session:
        return render_template(
            "index.html", products=list_products(session), name=name, error=error
        )


@blueprint.get("/")
def index():
    return render_page()


@blueprint.post("/")
def create():
    typed = request.form["name"]
    try:
        name = clean_name(typed)
    except ValueError as error:
        page = render_page(name=typed, error=str(error))
        return page, HTTPStatus.UNPROCESSABLE_CONTENT
    with open_session() as session:
        create_product(session, name)
    return redirect(url_for("ui.index"))
