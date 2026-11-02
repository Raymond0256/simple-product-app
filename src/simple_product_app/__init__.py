"""A small Flask app for creating and listing products."""

import os

from flask import Flask
from sqlalchemy import create_engine

from simple_product_app import api, ui

DEFAULT_DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/simple_product_app"
)


def configured_database_url() -> str:
    """DATABASE_URL if it is set, otherwise the database that compose.yaml starts."""
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


def create_app(database_url=None):
    app = Flask(__name__)
    app.config["DATABASE_URL"] = database_url or configured_database_url()
    app.extensions["db_engine"] = create_engine(app.config["DATABASE_URL"])
    app.register_blueprint(api.blueprint)
    app.register_blueprint(ui.blueprint)
    return app
