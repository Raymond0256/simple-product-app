"""Database sessions for the request handlers."""

from flask import current_app
from sqlalchemy.orm import Session


def open_session() -> Session:
    """A new session on the app's engine. Use it in a `with` block."""
    return Session(current_app.extensions["db_engine"])
