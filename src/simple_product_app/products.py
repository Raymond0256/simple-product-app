"""Product rules, shared by the API and the UI."""


def clean_name(value: str) -> str:
    """Return the name without surrounding whitespace."""
    return value.strip()
