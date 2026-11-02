"""Unit tests for the app factory."""

import pytest

from simple_product_app import create_app

ENVIRONMENT_DATABASE_URL = "postgresql://someone:secret@db.example:5432/products"


@pytest.mark.xfail(
    raises=AssertionError, strict=True, reason="RED: not implemented yet"
)
def test_create_app_reads_the_database_url_from_the_environment(monkeypatch):
    """
    GIVEN DATABASE_URL is set in the environment
    WHEN the app is created without a database URL
    THEN the app uses the URL from the environment
    """
    monkeypatch.setenv("DATABASE_URL", ENVIRONMENT_DATABASE_URL)

    app = create_app()

    assert app.config["DATABASE_URL"] == ENVIRONMENT_DATABASE_URL
