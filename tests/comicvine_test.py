import platform

from simyan import __version__
from simyan.comicvine import Comicvine


def test_default_user_agent(session: Comicvine) -> None:
    expected_user_agent = f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})"  # noqa: E501
    assert session._session.headers["User-Agent"] == expected_user_agent


def test_custom_user_agent(api_key: str) -> None:
    custom_ua = "MyCustomApp/1.0"
    session = Comicvine(api_key=api_key, user_agent=custom_ua, cache=None)
    assert session._session.headers["User-Agent"] == custom_ua


def test_empty_string_user_agent_uses_default(api_key: str) -> None:
    session = Comicvine(api_key=api_key, user_agent="", cache=None)
    expected_user_agent = f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})"  # noqa: E501
    assert session._session.headers["User-Agent"] == expected_user_agent


def test_headers_structure(api_key: str) -> None:
    session = Comicvine(api_key=api_key, cache=None)
    assert "Accept" in session._session.headers
    assert "User-Agent" in session._session.headers
    assert session._session.headers["Accept"] == "application/json"
