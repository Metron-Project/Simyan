"""Project entry file."""
__version__ = "0.5.3"
__all__ = ["__version__", "create_session", "api", "SqliteCache"]

from typing import Optional

from deprecation import deprecated

from Simyan.exceptions import AuthenticationError
from Simyan.session import Session
from Simyan.sqlite_cache import SqliteCache


def create_session(api_key: Optional[str] = None, cache: Optional[SqliteCache] = None) -> Session:
    """
    Entry function that sets credentials to use the ComicVine API, and whether to use a database cache for results.

    Args:
        api_key: User's API key to access the ComicVine API.
        cache: SqliteCache to use.

    Returns:
        A session object with the user's API key and Optional cache

    Raises:
        AuthenticationError: If no API key is provided
    """
    if api_key is None:
        raise AuthenticationError("Missing API Key.")

    return Session(api_key=api_key, cache=cache)


@deprecated(deprecated_in="0.6", removed_in="1.0", current_version=__version__, details="Use `create_session` instead")
def api(api_key: Optional[str] = None, cache: Optional[SqliteCache] = None) -> Session:
    """
    Entry function that sets credentials to use the ComicVine API, and whether to use a database cache for results.

    Args:
        api_key: User's API key to access the ComicVine API.
        cache: SqliteCache to use.

    Returns:
        A session object with the user's API key and Optional cache

    Raises:
        AuthenticationError: If no API key is provided
    """
    return create_session(api_key=api_key, cache=cache)
