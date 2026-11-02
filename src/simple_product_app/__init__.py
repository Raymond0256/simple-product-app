"""A small Flask app for creating and listing products."""

import os

from flask import Flask

DEFAULT_DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/simple_product_app"
)


def create_app(database_url=None):
    app = Flask(__name__)
    app.config["DATABASE_URL"] = database_url or os.environ.get(
        "DATABASE_URL", DEFAULT_DATABASE_URL
    )
    return app
