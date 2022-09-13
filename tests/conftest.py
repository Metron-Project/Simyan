"""
The Conftest module.

This module contains pytest fixtures.
"""
import os

import pytest

from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache


@pytest.fixture(scope="session")
def comicvine_api_key():
    """Set the ComicVine API key fixture."""
    return os.getenv("COMICVINE__API_KEY", default="IGNORED")


@pytest.fixture(scope="session")
def session(comicvine_api_key) -> Comicvine:
    """Set the Simyan session fixture."""
    return Comicvine(
        api_key=comicvine_api_key, cache=SQLiteCache("tests/cache.sqlite", expiry=None)
    )
