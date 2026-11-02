"""The HTML page for listing and creating products."""

from http import HTTPStatus

from flask import Blueprint, redirect, render_template, request, url_for

from simple_product_app.db import open_session
from simple_product_app.products import clean_name, create_product, list_products

blueprint = Blueprint("ui", __name__)


@blueprint.get("/")
def index():
    with open_session() as session:
        return render_template("index.html", products=list_products(session))


@blueprint.post("/")
def create():
    typed = request.form["name"]
    try:
        name = clean_name(typed)
    except ValueError as error:
        with open_session() as session:
            page = render_template(
                "index.html",
                products=list_products(session),
                name=typed,
                error=str(error),
            )
        return page, HTTPStatus.UNPROCESSABLE_CONTENT
    with open_session() as session:
        create_product(session, name)
    return redirect(url_for("ui.index"))
