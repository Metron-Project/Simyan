import os

import pytest

from Simyan import api, sqlite_cache


@pytest.fixture(scope="session")
def api_key():
    return os.getenv("COMICVINE", "INVALID")


@pytest.fixture(scope="session")
def talker(api_key):
    print(api_key)
    return api(
        api_key=api_key,
        cache=sqlite_cache.SqliteCache("tests/Simyan-Cache.sqlite"),
    )
