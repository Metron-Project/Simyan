"""
The Test Init module.

This module contains tests for project init.
"""
import pytest
from deprecation import fail_if_not_removed

from simyan import api, create_session
from simyan.exceptions import AuthenticationError
from simyan.session import Session


@fail_if_not_removed
def test_api():
    """Test for api()."""
    with pytest.raises(AuthenticationError):
        api()

    session = None
    try:
        session = api(api_key="Something")
    except Exception as exc:
        print(f"simyan.api() raised {exc} unexpectedly!")

    assert session.__class__.__name__ == Session.__name__


def test_create_session():
    """Test for create_session()."""
    session = None
    try:
        session = create_session(api_key="Something")
    except Exception as exc:
        print(f"simyan.create_session() raised {exc} unexpectedly!")

    assert session.__class__.__name__ == Session.__name__


def test_invalid_session():
    """Test for invalid session."""
    session = create_session(api_key="Invalid")
    with pytest.raises(AuthenticationError):
        session.publisher(_id=1)
