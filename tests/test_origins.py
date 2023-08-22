"""The Origins test module.

This module contains tests for Origin and OriginEntry objects.
"""

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.origin import OriginEntry


def test_origin(session: Comicvine) -> None:
    """Test using the origin endpoint with a valid origin_id."""
    result = session.get_origin(origin_id=1)
    assert result is not None
    assert result.id == 1

    assert result.api_url == "https://comicvine.gamespot.com/api/origin/4030-1/"
    assert result.character_set is None
    assert len(result.characters) == 4241
    assert result.name == "Mutant"
    assert result.profiles == []
    assert result.site_url == "https://comicvine.gamespot.com/mutant/4030-1/"


def test_origin_fail(session: Comicvine) -> None:
    """Test using the origin endpoint with an invalid origin_id."""
    with pytest.raises(ServiceError):
        session.get_origin(origin_id=-1)


def test_origin_list(session: Comicvine) -> None:
    """Test using the list origins endpoint with a valid search query."""
    search_results = session.list_origins({"filter": "name:Mutant"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 1)
    assert result is not None

    assert result.api_url == "https://comicvine.gamespot.com/api/origin/4030-1/"
    assert result.name == "Mutant"
    assert result.site_url == "https://comicvine.gamespot.com/mutant/4030-1/"


def test_origin_list_empty(session: Comicvine) -> None:
    """Test using the list origins endpoint with an invalid search query."""
    results = session.list_origins({"filter": "name:INVALID"})
    assert len(results) == 0


def test_origin_list_max_results(session: Comicvine) -> None:
    """Test list origins endpoint with max results."""
    results = session.list_origins(max_results=10)
    assert len(results) == 10


def test_search_origin(session: Comicvine) -> None:
    """Test using the search endpoint for a list of Origins."""
    results = session.search(resource=ComicvineResource.ORIGIN, query="Mutant")
    assert all(isinstance(x, OriginEntry) for x in results)
