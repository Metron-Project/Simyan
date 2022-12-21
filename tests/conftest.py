"""
The Conftest module.

This module contains pytest fixtures.
"""
import os
from pathlib import Path

import pytest

from simyan.comicvine import Comicvine
from simyan.sqlite_cache import SQLiteCache


@pytest.fixture(scope="session")
def comicvine_api_key() -> str:
    """Set the Comicvine API key fixture."""
    return os.getenv("COMICVINE__API_KEY", default="IGNORED")


@pytest.fixture(scope="session")
def session(comicvine_api_key: str) -> Comicvine:
    """Set the Simyan session fixture."""
    return Comicvine(
        api_key=comicvine_api_key, cache=SQLiteCache(Path("tests/cache.sqlite"), expiry=None)
    )
