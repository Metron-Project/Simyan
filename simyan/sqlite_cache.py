"""The SQLiteCache module.

This module provides the following classes:

- SQLiteCache
"""

from __future__ import annotations

__all__ = ["SQLiteCache"]
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from simyan import get_cache_root


class SQLiteCache:
    """The SQLiteCache object to cache search results from Comicvine.

    Args:
        path: Path to database.
        expiry: How long to keep cache results.

    Attributes:
        expiry (int | None): How long to keep cache results.
        connection (sqlite3.Connection): Database connection
    """

    def __init__(self, path: Path | None = None, expiry: int | None = 14):
        self.expiry = expiry
        self.connection = sqlite3.connect(path or get_cache_root() / "cache.sqlite")
        self.connection.row_factory = sqlite3.Row

        self.connection.execute("CREATE TABLE IF NOT EXISTS queries (query, response, query_date);")
        self.delete()

    def select(self, query: str) -> dict[str, Any]:
        """Retrieve data from the cache database.

        Args:
            query: Search string
        Returns:
            Empty dict or select results.
        """
        if self.expiry:
            expiry = datetime.now(tz=timezone.utc).astimezone().date() - timedelta(days=self.expiry)
            cursor = self.connection.execute(
                "SELECT * FROM queries WHERE query = ? and query_date > ?;",
                (query, expiry.isoformat()),
            )
        else:
            cursor = self.connection.execute("SELECT * FROM queries WHERE query = ?;", (query,))
        if results := cursor.fetchone():
            return json.loads(results["response"])
        return {}

    def insert(self, query: str, response: dict[str, Any]) -> None:
        """Insert data into the cache database.

        Args:
            query: Search string
            response: Data to save
        """
        self.connection.execute(
            "INSERT INTO queries (query, response, query_date) VALUES (?, ?, ?);",
            (
                query,
                json.dumps(response),
                datetime.now(tz=timezone.utc).astimezone().date().isoformat(),
            ),
        )
        self.connection.commit()

    def delete(self) -> None:
        """Remove all expired data from the cache database."""
        if not self.expiry:
            return
        expiry = datetime.now(tz=timezone.utc).astimezone().date() - timedelta(days=self.expiry)
        self.connection.execute("DELETE FROM queries WHERE query_date < ?;", (expiry.isoformat(),))
        self.connection.commit()
