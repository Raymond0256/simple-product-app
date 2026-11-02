"""Product rules, shared by the API and the UI."""

from sqlalchemy.orm import Session

from simple_product_app.models import Product

NAME_REQUIRED = "Name is required."


def clean_name(value: str) -> str:
    """Return the name without surrounding whitespace, or raise if it is blank."""
    name = value.strip()
    if not name:
        raise ValueError(NAME_REQUIRED)
    return name


def create_product(session: Session, name: str) -> Product:
    """Store a product whose name is already clean, and return it."""
    product = Product(name=name)
    session.add(product)
    session.commit()
    return product
