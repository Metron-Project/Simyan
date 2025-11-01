"""The Comicvine test module.

This module contains tests for the Comicvine class initialization and configuration.
"""

import platform

from simyan import __version__
from simyan.comicvine import Comicvine


def test_default_user_agent(comicvine_api_key: str) -> None:
    """Test that the default User-Agent is set correctly."""
    session = Comicvine(api_key=comicvine_api_key)
    expected_user_agent = f"Simyan/{__version__}/{platform.system()}: {platform.release()}"
    assert session.headers["User-Agent"] == expected_user_agent


def test_custom_user_agent(comicvine_api_key: str) -> None:
    """Test that a custom User-Agent can be set."""
    custom_ua = "MyCustomApp/1.0"
    session = Comicvine(api_key=comicvine_api_key, user_agent=custom_ua)
    assert session.headers["User-Agent"] == custom_ua


def test_custom_user_agent_with_all_params(comicvine_api_key: str) -> None:
    """Test that custom User-Agent works with all initialization parameters."""
    custom_ua = "TestApp/2.0 (Custom)"
    session = Comicvine(api_key=comicvine_api_key, timeout=60, cache=None, user_agent=custom_ua)
    assert session.headers["User-Agent"] == custom_ua
    assert session.timeout == 60
    assert session.cache is None


def test_empty_string_user_agent_uses_default(comicvine_api_key: str) -> None:
    """Test that an empty string User-Agent falls back to default."""
    session = Comicvine(api_key=comicvine_api_key, user_agent="")
    expected_user_agent = f"Simyan/{__version__}/{platform.system()}: {platform.release()}"
    assert session.headers["User-Agent"] == expected_user_agent


def test_headers_structure(comicvine_api_key: str) -> None:
    """Test that headers are properly structured."""
    session = Comicvine(api_key=comicvine_api_key)
    assert "Accept" in session.headers
    assert "User-Agent" in session.headers
    assert session.headers["Accept"] == "application/json"
