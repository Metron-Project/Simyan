__all__ = ["SQLiteCache"]

import json
import logging
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from simyan import get_cache_root
from simyan.cache.schemas import CacheData

LOGGER = logging.getLogger(__name__)


class SQLiteCache:
    """The SQLiteCache object to cache search results from Comicvine.

    Args:
        path: Path to database.
        expiry: How long to keep cache results.
    """

    def __init__(self, path: Path | None = None, expiry: timedelta | None = timedelta(days=14)):
        self._db_path: Path = path or (get_cache_root() / "cache.sqlite")
        self._expiry: timedelta | None = expiry
        self.initialize()
        self.cleanup()

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection]:
        conn: sqlite3.Connection | None = None
        try:
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
            conn.commit()
        finally:
            if conn:
                conn.close()

    def initialize(self) -> None:
        """Create the cache table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS queries (
            url TEXT PRIMARY KEY,
            response TEXT NOT NULL,
            created_at DATETIME NOT NULL
        );
        """
        with self._connect() as conn:
            conn.executescript(query)

    def _select(self, query: str, params: tuple) -> CacheData | None:
        with self._connect() as conn:
            if row := conn.execute(query, params).fetchone():
                try:
                    return CacheData(
                        url=row["url"],
                        response=json.loads(row["response"]),
                        created_at=row["created_at"],
                    )
                except json.JSONDecodeError as err:
                    LOGGER.warning(err)
                    self.delete(url=params[0])
        return None

    def select(self, url: str) -> CacheData | None:
        """Retrieve data from the cache database.

        Args:
            url: The URL used as the cache key.

        Returns:
            A `CacheData` instance if a matching record exists, otherwise `None`.
        """
        if self._expiry:
            query = """
            SELECT url, response, created_at
            FROM queries
            WHERE url = ? AND created_at > ?;
            """
            expiry = datetime.now(tz=timezone.utc) - self._expiry
            return self._select(query=query, params=(url, expiry.isoformat()))
        query = """
        SELECT url, response, created_at
        FROM queries
        WHERE url = ?;
        """
        return self._select(query=query, params=(url,))

    def insert(self, url: str, response: dict[str, Any]) -> None:
        """Insert data into the cache database.

        If a record with the same *url* already exists it is overwritten (upsert semantics).

        Args:
            url: The URL used as the cache key.
            response: The response body to store.
        """
        query = """
        INSERT INTO queries (url, response, created_at)
        VALUES (?, ?, ?)
        ON CONFLICT (url) DO UPDATE SET
            response = excluded.response,
            created_at = excluded.created_at;
        """
        with self._connect() as conn:
            conn.execute(
                query, (url, json.dumps(response), datetime.now(tz=timezone.utc).isoformat())
            )

    def delete(self, url: str) -> None:
        """Remove entry from the cache with the provided url.

        Args:
            url: The URL used as the cache key.
        """
        query = """
        DELETE FROM queries
        WHERE url = ?;
        """
        with self._connect() as conn:
            conn.execute(query, (url,))

    def cleanup(self) -> None:
        """Remove all expired entries from the cache database."""
        if not self._expiry:
            return
        query = """
        DELETE FROM queries
        WHERE created_at < ?;
        """
        expiry = datetime.now(tz=timezone.utc) - self._expiry
        with self._connect() as conn:
            conn.execute(query, (expiry.isoformat(),))
