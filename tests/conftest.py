"""
The Conftest module.

This module contains pytest fixtures.
"""
import os

import pytest

from simyan.service import Comicvine
from simyan.sqlite_cache import SQLiteCache


@pytest.fixture(scope="session")
def api_key():
    """Set the ComicVine API key fixture."""
    return os.getenv("COMICVINE_API_KEY", default="Invalid")


@pytest.fixture(scope="session")
def session(api_key) -> Comicvine:
    """Set the Simyan session fixture."""
    return Comicvine(api_key=api_key, cache=SQLiteCache("tests/cache.sqlite", expiry=None))
