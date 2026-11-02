"""Fixtures for tests that never touch a database."""

import pytest

from simple_product_app import create_app

# Nothing listens here, so a unit test that reaches the database fails loudly.
UNREACHABLE_DATABASE_URL = "postgresql://unit:unit@127.0.0.1:9/unit"


@pytest.fixture
def client():
    """A test client for an app whose database can't be reached."""
    return create_app(database_url=UNREACHABLE_DATABASE_URL).test_client()
