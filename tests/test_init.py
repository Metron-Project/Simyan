"""
Test Init module.

This module contains tests for project init.
"""
import pytest
from deprecation import fail_if_not_removed

from Simyan import api, create_session, exceptions, session


@fail_if_not_removed
def test_api():
    """Test for api()."""
    with pytest.raises(exceptions.AuthenticationError):
        api()

    m = None
    try:
        m = api(api_key="Something")
    except Exception as exc:
        print(f"Simyan.api() raised {exc} unexpectedly!")

    assert m.__class__.__name__ == session.Session.__name__


def test_create_session():
    """Test for create_session()."""
    with pytest.raises(exceptions.AuthenticationError):
        create_session()

    m = None
    try:
        m = create_session(api_key="Something")
    except Exception as exc:
        print(f"Simyan.create_session() raised {exc} unexpectedly!")

    assert m.__class__.__name__ == session.Session.__name__
