"""Alembic runs this file to apply migrations to the app's database."""

from alembic import context
from sqlalchemy import create_engine, pool

from simple_product_app import configured_database_url

# Tests pass the URL of their throwaway database; otherwise use the app's.
url = context.config.attributes.get("database_url") or configured_database_url()
engine = create_engine(url, poolclass=pool.NullPool)

with engine.connect() as connection:
    context.configure(connection=connection)
    with context.begin_transaction():
        context.run_migrations()
