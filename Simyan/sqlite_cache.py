import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class SqliteCache:
    def __init__(self, name: str = "Simyan-Cache.sqlite", expiry: int = 14):
        self.expiry = expiry
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS queries (query, response, expiry);")
        self.delete()

    def select(self, query: str) -> Dict[str, Any]:
        self.cur.execute(
            "SELECT response FROM queries WHERE query = ? AND expiry > ?;",
            (query, datetime.now().strftime("%Y-%m-%d")),
        )
        result = self.cur.fetchone()
        if result:
            return json.loads(result[0])
        return {}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self.select(query=key) or None

    def insert(self, query: str, response: str):
        expiry = datetime.now() + timedelta(days=self.expiry)
        self.cur.execute(
            "INSERT INTO queries(query, response, expiry) VALUES(?, ?, ?);",
            (query, json.dumps(response), expiry.strftime("%Y-%m-%d")),
        )
        self.con.commit()

    def store(self, key: str, value: str):
        return self.insert(query=key, response=value)

    def delete(self):
        self.cur.execute(
            "DELETE FROM queries WHERE expiry < ?;",
            (datetime.now().strftime("%Y-%m-%d"),),
        )
        self.con.commit()
