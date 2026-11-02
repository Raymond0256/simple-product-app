"""Unit tests for the app factory."""

from simple_product_app import DEFAULT_DATABASE_URL, create_app

ENVIRONMENT_DATABASE_URL = "postgresql://someone:secret@db.example:5432/products"


def test_create_app_reads_the_database_url_from_the_environment(monkeypatch):
    """
    GIVEN DATABASE_URL is set in the environment
    WHEN the app is created without a database URL
    THEN the app uses the URL from the environment
    """
    monkeypatch.setenv("DATABASE_URL", ENVIRONMENT_DATABASE_URL)

    app = create_app()

    assert app.config["DATABASE_URL"] == ENVIRONMENT_DATABASE_URL


def test_create_app_falls_back_to_the_compose_database(monkeypatch):
    """
    GIVEN DATABASE_URL is not set
    WHEN the app is created without a database URL
    THEN the app uses the database that compose.yaml starts
    """
    monkeypatch.delenv("DATABASE_URL", raising=False)

    app = create_app()

    assert app.config["DATABASE_URL"] == DEFAULT_DATABASE_URL
