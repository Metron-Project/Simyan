from typing import Optional

from Simyan.exceptions import AuthenticationError
from Simyan.session import Session
from Simyan.sqlite_cache import SqliteCache


def api(api_key: Optional[str] = None, cache: SqliteCache = None) -> Session:
    if api_key is None:
        raise AuthenticationError("Missing API Key.")

    return Session(api_key=api_key, cache=cache)
