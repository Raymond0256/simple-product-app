"""A small Flask app for creating and listing products."""

from flask import Flask


def create_app(database_url=None):
    app = Flask(__name__)
    app.config["DATABASE_URL"] = database_url
    return app
