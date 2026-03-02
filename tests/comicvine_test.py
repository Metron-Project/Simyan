import platform

from httpx import Timeout

from simyan import __version__
from simyan.comicvine import Comicvine


def test_default_user_agent(comicvine_api_key: str) -> None:
    session = Comicvine(api_key=comicvine_api_key, cache=None)
    expected_user_agent = f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})"  # noqa: E501
    assert session._client.headers["User-Agent"] == expected_user_agent


def test_custom_user_agent(comicvine_api_key: str) -> None:
    custom_ua = "MyCustomApp/1.0"
    session = Comicvine(api_key=comicvine_api_key, user_agent=custom_ua, cache=None)
    assert session._client.headers["User-Agent"] == custom_ua


def test_custom_user_agent_with_all_params(comicvine_api_key: str) -> None:
    custom_ua = "TestApp/2.0 (Custom)"
    session = Comicvine(api_key=comicvine_api_key, timeout=60, cache=None, user_agent=custom_ua)
    assert session._client.headers["User-Agent"] == custom_ua
    assert session._client.timeout == Timeout(60)
    assert session._cache is None


def test_empty_string_user_agent_uses_default(comicvine_api_key: str) -> None:
    session = Comicvine(api_key=comicvine_api_key, user_agent="", cache=None)
    expected_user_agent = f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})"  # noqa: E501
    assert session._client.headers["User-Agent"] == expected_user_agent


def test_headers_structure(comicvine_api_key: str) -> None:
    session = Comicvine(api_key=comicvine_api_key, cache=None)
    assert "Accept" in session._client.headers
    assert "User-Agent" in session._client.headers
    assert session._client.headers["Accept"] == "application/json"
