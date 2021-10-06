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

    m = None
    try:
        m = api(api_key="Something")
    except Exception as exc:
        print(f"Simyan.api() raised {exc} unexpectedly!")

    assert m.__class__.__name__ == Session.__name__


def test_create_session():
    """Test for create_session()."""
    m = None
    try:
        m = create_session(api_key="Something")
    except Exception as exc:
        print(f"Simyan.create_session() raised {exc} unexpectedly!")

    assert m.__class__.__name__ == Session.__name__
