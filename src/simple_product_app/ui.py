"""The HTML page for listing and creating products."""

from http import HTTPStatus

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from sqlalchemy.orm import Session

from simple_product_app.products import clean_name, create_product, list_products

blueprint = Blueprint("ui", __name__)


@blueprint.get("/")
def index():
    with Session(current_app.extensions["db_engine"]) as session:
        return render_template("index.html", products=list_products(session))


@blueprint.post("/")
def create():
    typed = request.form["name"]
    try:
        name = clean_name(typed)
    except ValueError as error:
        with Session(current_app.extensions["db_engine"]) as session:
            page = render_template(
                "index.html",
                products=list_products(session),
                name=typed,
                error=str(error),
            )
        return page, HTTPStatus.UNPROCESSABLE_CONTENT
    with Session(current_app.extensions["db_engine"]) as session:
        create_product(session, name)
    return redirect(url_for("ui.index"))
