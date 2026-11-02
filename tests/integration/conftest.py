"""Fixtures for tests that need a real PostgreSQL database."""

from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from testcontainers.community.postgres import PostgresContainer

from simple_product_app import create_app

POSTGRES_IMAGE = "postgres:18-alpine"
PYPROJECT = Path(__file__).parents[2] / "pyproject.toml"


def alembic_config_for(database_url):
    """Alembic's configuration from pyproject.toml, pointed at the given database."""
    config = Config(toml_file=str(PYPROJECT))
    config.attributes["database_url"] = database_url
    return config


@pytest.fixture(scope="session")
def database_url():
    """A throwaway PostgreSQL database, migrated to the latest revision."""
    with PostgresContainer(
        POSTGRES_IMAGE, username="test", password="test", dbname="test", driver=None
    ) as postgres:
        url = postgres.get_connection_url()
        command.upgrade(alembic_config_for(url), "head")
        yield url


@pytest.fixture
def db_engine(database_url):
    """An engine for the test database, disposed of after the test."""
    engine = create_engine(database_url)
    yield engine
    engine.dispose()


@pytest.fixture
def db_app(database_url, db_engine):
    """The app, using the test database, starting with no products."""
    with db_engine.begin() as connection:
        connection.execute(text("DELETE FROM products"))
    app = create_app(database_url=database_url)
    yield app
    app.extensions["db_engine"].dispose()


@pytest.fixture
def db_client(db_app):
    """A test client for the app that uses the test database."""
    return db_app.test_client()


@pytest.fixture
def alembic_config(database_url):
    """Alembic's configuration, pointed at the test database."""
    return alembic_config_for(database_url)
