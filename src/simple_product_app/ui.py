"""The HTML page for listing and creating products."""

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
    name = clean_name(request.form["name"])
    with Session(current_app.extensions["db_engine"]) as session:
        create_product(session, name)
    return redirect(url_for("ui.index"))
