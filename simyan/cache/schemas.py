__all__ = ["CacheData"]

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CacheData(BaseModel, extra="forbid"):
    """A single entry stored in the cache.

    Attributes:
        url: The URL that was requested, used as the cache key.
        response: The response body returned by the server.
        created_at: The UTC datetime at which the response was stored.
    """

    url: str
    response: dict[str, Any]
    created_at: datetime
