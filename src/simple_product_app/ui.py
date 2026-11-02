"""The HTML page for listing and creating products."""

from flask import Blueprint, current_app, render_template
from sqlalchemy.orm import Session

from simple_product_app.products import list_products

blueprint = Blueprint("ui", __name__)


@blueprint.get("/")
def index():
    with Session(current_app.extensions["db_engine"]) as session:
        return render_template("index.html", products=list_products(session))
