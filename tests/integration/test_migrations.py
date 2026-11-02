"""Integration tests for the database migrations."""

import pytest
from alembic import command
from sqlalchemy import inspect

pytestmark = pytest.mark.integration

EXPECTED_PRODUCTS_TABLE = {
    "columns": [
        {"name": "id", "type": "UUID", "nullable": False, "default": "uuidv7()"},
        {"name": "name", "type": "TEXT", "nullable": False, "default": None},
    ],
    "primary_key": ["id"],
}


def describe_table(engine, table_name):
    """The parts of a table the design specifies, or None if the table is missing."""
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        return None
    columns = [
        {
            "name": column["name"],
            "type": str(column["type"]),
            "nullable": column["nullable"],
            "default": column["default"],
        }
        for column in inspector.get_columns(table_name)
    ]
    primary_key = inspector.get_pk_constraint(table_name)["constrained_columns"]
    return {"columns": columns, "primary_key": primary_key}


def test_migrations_create_the_products_table(db_engine):
    """
    GIVEN a database migrated to the latest revision
    WHEN the products table is inspected
    THEN it has exactly the designed columns and primary key
    """
    assert describe_table(db_engine, "products") == EXPECTED_PRODUCTS_TABLE


def test_the_migrations_match_the_models(alembic_config):
    """
    GIVEN a database migrated to the latest revision
    WHEN Alembic compares it with the ORM models
    THEN it finds nothing that a new migration would need to change
    """
    command.check(alembic_config)
