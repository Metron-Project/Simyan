import os
from pathlib import Path

import pytest

from simyan.cache import SQLiteCache
from simyan.comicvine import Comicvine


@pytest.fixture(scope="session")
def comicvine_api_key() -> str:
    return os.getenv("COMICVINE__API_KEY", default="IGNORED")


@pytest.fixture(scope="session")
def session(comicvine_api_key: str) -> Comicvine:
    return Comicvine(
        api_key=comicvine_api_key, cache=SQLiteCache(path=Path("tests/cache.sqlite"), expiry=None)
    )
