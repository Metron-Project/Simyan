"""
The SQLiteCache module.

This module provides the following classes:

- SQLiteCache
"""
__all__ = ["SQLiteCache"]
import json
import sqlite3
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from simyan import get_cache_root


class SQLiteCache:
    """
    The SQLiteCache object to cache search results from Comicvine.

    Args:
        path: Path to database.
        expiry: How long to keep cache results.

    Attributes:
        expiry (Optional[int]): How long to keep cache results.
        con (sqlite3.Connection): Database connection
    """

    def __init__(
        self,
        path: Path = None,
        expiry: Optional[int] = 14,
    ):
        self.expiry = expiry
        self.con = sqlite3.connect(path or get_cache_root() / "cache.sqlite")
        self.con.row_factory = sqlite3.Row

        self.con.execute("CREATE TABLE IF NOT EXISTS queries (query, response, query_date);")
        self.delete()

    def select(self, query: str) -> Dict[str, Any]:
        """
        Retrieve data from the cache database.

        Args:
            query: Search string
        Returns:
            Empty dict or select results.
        """
        if self.expiry:
            expiry = date.today() - timedelta(days=self.expiry)
            cursor = self.con.execute(
                "SELECT * FROM queries WHERE query = ? and query_date > ?;",
                (query, expiry.isoformat()),
            )
        else:
            cursor = self.con.execute("SELECT * FROM queries WHERE query = ?;", (query,))
        results = cursor.fetchone()
        if results:
            return json.loads(results["response"])
        return {}

    def insert(self, query: str, response: Dict[str, Any]) -> None:
        """
        Insert data into the cache database.

        Args:
            query: Search string
            response: Data to save
        """
        self.con.execute(
            "INSERT INTO queries (query, response, query_date) VALUES (?, ?, ?);",
            (query, json.dumps(response), date.today().isoformat()),
        )
        self.con.commit()

    def delete(self) -> None:
        """Remove all expired data from the cache database."""
        if not self.expiry:
            return
        expiry = date.today() - timedelta(days=self.expiry)
        self.con.execute("DELETE FROM queries WHERE query_date < ?;", (expiry.isoformat(),))
        self.con.commit()
