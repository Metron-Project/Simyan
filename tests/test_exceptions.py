"""
The Exceptions test module.

This module contains tests for Exceptions.
"""
import pytest

from simyan.comicvine import Comicvine
from simyan.exceptions import AuthenticationError, ServiceError


def test_unauthorized():
    """Test generating an AuthenticationError."""
    session = Comicvine(api_key="Invalid", cache=None)
    with pytest.raises(AuthenticationError):
        session.publisher(publisher_id=1)


def test_not_found(session: Comicvine):
    """Test a 404 Not Found raises a ServiceError."""
    with pytest.raises(ServiceError):
        session._get_request(endpoint="/invalid")


def test_timeout(comicvine_api_key: str):
    """Test a TimeoutError for slow responses."""
    session = Comicvine(api_key=comicvine_api_key, timeout=0.1, cache=None)
    with pytest.raises(ServiceError):
        session.publisher(publisher_id=1)
