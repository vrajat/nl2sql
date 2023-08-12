"""Test nl2sql."""

import nl2sql


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(nl2sql.__name__, str)
