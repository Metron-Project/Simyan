"""
The Conftest module.

This module contains pytest fixtures.
"""
import os

import pytest

from simyan import SQLiteCache, create_session


@pytest.fixture(scope="session")
def comicvine_api_key():
    """Set the ComicVine API key fixture."""
    return os.getenv("COMICVINE_API_KEY", "INVALID")


@pytest.fixture(scope="session")
def comicvine(comicvine_api_key):
    """Set the Simyan session fixture."""
    return create_session(api_key=comicvine_api_key, cache=SQLiteCache("tests/Simyan-Cache.sqlite", expiry=None))
