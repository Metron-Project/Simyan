import os

import pytest

from Simyan import api, sqlite_cache


@pytest.fixture(scope="session")
def dummy_key():
    return os.getenv("COMICVINE_KEY", "f6bbc5b3cd54fd483fab20fe686b8ea718438917")


@pytest.fixture(scope="session")
def talker(dummy_key):
    return api(
        api_key=dummy_key,
        cache=sqlite_cache.SqliteCache("tests/Simyan-Cache.sqlite"),
    )
