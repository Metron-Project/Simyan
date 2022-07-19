"""
The SQLiteCache module.

This module provides the following classes:

- SQLiteCache
"""
__all__ = ["SQLiteCache"]
import json
import sqlite3
from datetime import date, timedelta
from typing import Any, Dict, Optional

from simyan import get_cache_root


class SQLiteCache:
    """
    The SQLiteCache object to cache search results from ComicVine.

    Args:
        path: Path to database.
        expiry: How long to keep cache results.

    Attributes:
        expiry (Optional[int]): How long to keep cache results.
        con (sqlite3.Connection): Database connection
        cur (sqlite3.Cursor): Database cursor
    """

    def __init__(
        self,
        path: str = get_cache_root() / "cache.sqlite",
        expiry: Optional[int] = 14,
    ):
        self.expiry = expiry
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS queries (query, response, expiry);")
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
            self.cur.execute(
                "SELECT response FROM queries WHERE query = ? and expiry > ?;",
                (query, date.today().isoformat()),
            )
        else:
            self.cur.execute("SELECT response FROM queries WHERE query = ?;", (query,))
        results = self.cur.fetchone()
        if results:
            return json.loads(results[0])
        return {}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from the cache database.

        Args:
            key: Search string
        Returns:
            None or select results.
        """
        return self.select(query=key) or None

    def insert(self, query: str, response: str):
        """
        Insert data into the cache database.

        Args:
            query: Search string
            response: Data to save
        """
        if self.expiry:
            expiry = date.today() + timedelta(days=self.expiry)
        else:
            expiry = date.today()
        self.cur.execute(
            "INSERT INTO queries (query, response, expiry) VALUES (?, ?, ?);",
            (query, json.dumps(response), expiry.isoformat()),
        )
        self.con.commit()

    def store(self, key: str, value: str):
        """
        Insert data into the cache database.

        Args:
            key: Search string
            value: Data to save
        """
        return self.insert(query=key, response=value)

    def delete(self):
        """Remove all expired data from the cache database."""
        if not self.expiry:
            return
        self.cur.execute("DELETE FROM queries WHERE expiry < ?;", (date.today().isoformat(),))
        self.con.commit()
