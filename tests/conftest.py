import os

import pytest

from Simyan import api, sqlite_cache


@pytest.fixture(scope="session")
def comicvine_api_key():
    return os.getenv("COMICVINE_API_KEY", "INVALID")


@pytest.fixture(scope="session")
def comicvine(comicvine_api_key):
    return api(api_key=comicvine_api_key, cache=sqlite_cache.SqliteCache("tests/Simyan-Cache.sqlite"))
