"""Product rules, shared by the API and the UI."""

NAME_REQUIRED = "Name is required."


def clean_name(value: str) -> str:
    """Return the name without surrounding whitespace, or raise if it is blank."""
    name = value.strip()
    if not name:
        raise ValueError(NAME_REQUIRED)
    return name
