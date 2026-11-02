"""The README's section outline is a requirement, so a test holds it in place."""

from pathlib import Path

README = Path(__file__).parent.parent / "README.md"

REQUIRED_HEADINGS = [
    "Prerequisites",
    "Database setup",
    "Start backend",
    "Start frontend",
    "Verify (open local host)",
    "Notes",
]


def test_readme_has_exactly_the_required_section_headings_in_order():
    """
    GIVEN the project README
    WHEN its second-level headings are read from top to bottom
    THEN they are exactly the required sections, in the required order
    """
    lines = README.read_text().splitlines()
    headings = [line.removeprefix("## ") for line in lines if line.startswith("## ")]

    assert headings == REQUIRED_HEADINGS
