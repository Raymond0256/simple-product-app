"""Product rules, shared by the API and the UI."""

NAME_REQUIRED = "Name is required."


def clean_name(value: str) -> str:
    """Return the name without surrounding whitespace."""
    return value.strip()
