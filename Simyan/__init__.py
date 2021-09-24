"""Project entry file."""
__version__ = "0.5.2"

from typing import Optional

from Simyan.exceptions import AuthenticationError
from Simyan.session import Session
from Simyan.sqlite_cache import SqliteCache


def api(api_key: Optional[str] = None, cache: SqliteCache = None) -> Session:
    """Entry function that sets credentials to use the Comic Vine API, and whether to use a database cache for results.

    :param str, optional api_key: User's api key to access the Comic Vine api.
    :param SqliteCache optional: SqliteCache to use
    """
    if api_key is None:
        raise AuthenticationError("Missing API Key.")

    return Session(api_key=api_key, cache=cache)
