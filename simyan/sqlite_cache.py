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
        self._db_path = path or (get_cache_root() / "cache.sqlite")
        self._expiry = expiry
        self.initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS queries (
                    query TEXT NOT NULL PRIMARY KEY,
                    response TEXT,
                    query_date DATE
                );
                """
            )
        self.cleanup()

    def select(self, query: str) -> dict[str, Any]:
        """Retrieve data from the cache database.

        Args:
            query: Url string used as key.

        Returns:
            Empty dict or select results.
        """
        with self._connect() as conn:
            if self._expiry:
                expiry = datetime.now(tz=timezone.utc).astimezone().date() - timedelta(
                    days=self._expiry
                )
                row = conn.execute(
                    "SELECT * FROM queries WHERE query = ? and query_date > ?;",
                    (query, expiry.isoformat()),
                ).fetchone()
            else:
                row = conn.execute("SELECT * FROM queries WHERE query = ?;", (query,)).fetchone()
            return json.loads(row["response"]) if row else {}

    def insert(self, query: str, response: dict[str, Any]) -> None:
        """Insert data into the cache database.

        Args:
            query: Url string used as key.
            response: Response dict from url.
        """
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO queries (query, response, query_date) VALUES (?, ?, ?);",
                (
                    query,
                    json.dumps(response),
                    datetime.now(tz=timezone.utc).astimezone().date().isoformat(),
                ),
            )

    def delete(self, query: str) -> None:
        """Remove entry from the cache with the provided url.

        Args:
          query: Url string used as key.
        """
        with self._connect() as conn:
            conn.execute("DELETE FROM queries WHERE query = ?;", (query,))

    def cleanup(self) -> None:
        """Remove all expired entries from the cache database."""
        if not self._expiry:
            return
        expiry = datetime.now(tz=timezone.utc).astimezone().date() - timedelta(days=self._expiry)
        with self._connect() as conn:
            conn.execute("DELETE FROM queries WHERE query_date < ?;", (expiry.isoformat(),))
