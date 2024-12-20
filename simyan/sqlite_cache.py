"""The SQLiteCache module.

This module provides the following classes:
- SQLiteCache
"""

__all__ = ["SQLiteCache"]
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from simyan import get_cache_root


class SQLiteCache:
    """The SQLiteCache object to cache search results from Comicvine.

    Args:
        path: Path to database.
        expiry: How long to keep cache results.
    """

    def __init__(self, path: Optional[Path] = None, expiry: Optional[int] = 14):
        self.expiry = expiry
        self.connection = sqlite3.connect(path or get_cache_root() / "cache.sqlite")
        self.connection.row_factory = sqlite3.Row

        self.connection.execute("CREATE TABLE IF NOT EXISTS queries (url, response, query_date);")
        self.cleanup()

    def select(self, url: str) -> dict[str, Any]:
        """Retrieve data from the cache database.

        Args:
            url: Url string used as key.

        Returns:
            Empty dict or select results.
        """
        if self.expiry:
            expiry = datetime.now(tz=timezone.utc).astimezone().date() - timedelta(days=self.expiry)
            cursor = self.connection.execute(
                "SELECT * FROM queries WHERE url = ? and query_date > ?;", (url, expiry.isoformat())
            )
        else:
            cursor = self.connection.execute("SELECT * FROM queries WHERE url = ?;", (url,))
        if results := cursor.fetchone():
            return json.loads(results["response"])
        return {}

    def insert(self, url: str, response: dict[str, Any]) -> None:
        """Insert data into the cache database.

        Args:
            url: Url string used as key.
            response: Response dict from url.
        """
        self.connection.execute(
            "INSERT INTO queries (url, response, query_date) VALUES (?, ?, ?);",
            (
                url,
                json.dumps(response),
                datetime.now(tz=timezone.utc).astimezone().date().isoformat(),
            ),
        )
        self.connection.commit()

    def delete(self, url: str) -> None:
        """Remove entry from the cache with the provided url.

        Args:
          url: Url string used as key.
        """
        self.connection.execute("DELETE FROM queries WHERE url = ?;", (url,))
        self.connection.commit()

    def cleanup(self) -> None:
        """Remove all expired entries from the cache database."""
        if not self.expiry:
            return
        expiry = datetime.now(tz=timezone.utc).astimezone().date() - timedelta(days=self.expiry)
        self.connection.execute("DELETE FROM queries WHERE query_date < ?;", (expiry.isoformat(),))
        self.connection.commit()
