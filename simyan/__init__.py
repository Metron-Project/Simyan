"""simyan package entry file."""
__version__ = "0.7.4"
__all__ = ["__version__", "create_session", "api"]

from typing import Optional

from deprecation import deprecated

from simyan.exceptions import AuthenticationError
from simyan.session import Session
from simyan.sqlite_cache import SQLiteCache


@deprecated(
    deprecated_in="0.6.1",
    removed_in="0.8.0",
    current_version=__version__,
    details="Use `session.Session` instead",
)
def create_session(api_key: str, cache: Optional[SQLiteCache] = None) -> Session:
    """
    Entry function that sets credentials to use the ComicVine API, and whether to use a database \
    cache for results.

    Args:
        api_key: User's API key to access the ComicVine API.
        cache: SQLiteCache to use.
    Returns:
        A Session object with the user's API key and optional cache.
    """
    return Session(api_key=api_key, cache=cache)


@deprecated(
    deprecated_in="0.6.0",
    removed_in="0.8.0",
    current_version=__version__,
    details="Use `session.Session` instead",
)
def api(api_key: Optional[str] = None, cache: Optional[SQLiteCache] = None) -> Session:
    """
    Entry function that sets credentials to use the ComicVine API, and whether to use a database \
    cache for results.

    Args:
        api_key: User's API key to access the ComicVine API.
        cache: SQLiteCache to use.
    Returns:
        A Session object with the user's API key and optional cache.
    Raises:
        AuthenticationError: If no API key is provided.
    """
    if api_key is None:
        raise AuthenticationError("Missing API Key.")

    return Session(api_key=api_key, cache=cache)
