"""Project entry file."""
__version__ = "0.5.3"
__all__ = ["__version__", "create_session", "api", "SqliteCache"]

from typing import Optional

from deprecation import deprecated

from Simyan.exceptions import AuthenticationError
from Simyan.session import Session
from Simyan.sqlite_cache import SqliteCache


def create_session(api_key: Optional[str] = None, cache: Optional[SqliteCache] = None) -> Session:
    """Entry function that sets credentials to use the Comic Vine API, and whether to use a database cache for results.

    :param api_key: User's api key to access the Comic Vine api.
    :type api_key: str, optional

    :param cache: SqliteCache to use
    :type cache: SqliteCache, optional
    """
    if api_key is None:
        raise AuthenticationError("Missing API Key.")

    return Session(api_key=api_key, cache=cache)


@deprecated(deprecated_in="0.6", removed_in="1.0", current_version=__version__, details="Use `create_session` instead")
def api(api_key: Optional[str] = None, cache: Optional[SqliteCache] = None) -> Session:
    """Entry function that sets credentials to use the Comic Vine API, and whether to use a database cache for results.

    :param api_key: User's api key to access the Comic Vine api.
    :type api_key: str, optional

    :param cache: SqliteCache to use
    :type cache: SqliteCache, optional
    """
    return create_session(api_key=api_key, cache=cache)
