"""Alembic runs this file to apply migrations to the app's database."""

from alembic import context
from sqlalchemy import create_engine, pool

from simple_product_app import configured_database_url
from simple_product_app.models import Base

# Tests pass the URL of their throwaway database; otherwise use the app's.
url = context.config.attributes.get("database_url") or configured_database_url()
engine = create_engine(url, poolclass=pool.NullPool)

with engine.connect() as connection:
    # The models' metadata lets `alembic revision --autogenerate` and `alembic check`
    # compare the database with the code.
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()
