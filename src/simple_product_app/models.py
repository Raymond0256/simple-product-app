"""The database table, as a SQLAlchemy ORM model."""

import uuid

from sqlalchemy import Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    # PostgreSQL generates the id. UUIDv7 values are time-ordered.
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("uuidv7()")
    )
    name: Mapped[str] = mapped_column(Text)
