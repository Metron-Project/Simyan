"""The Origins test module.

This module contains tests for Origin and BasicOrigin objects.
"""

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.origin import BasicOrigin


def test_get_origin(session: Comicvine) -> None:
    """Test the get_origin function with a valid id."""
    result = session.get_origin(origin_id=1)
    assert result is not None
    assert result.id == 1

    assert result.character_set is None
    assert len(result.characters) == 4477
    assert len(result.profiles) == 0


def test_get_origin_fail(session: Comicvine) -> None:
    """Test the get_origin function with an invalid id."""
    with pytest.raises(ServiceError):
        session.get_origin(origin_id=-1)


def test_list_origins(session: Comicvine) -> None:
    """Test the list_origins function with a valid search query."""
    search_results = session.list_origins({"filter": "name:Mutant"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 1)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/origin/4030-1/"
    assert result.name == "Mutant"
    assert str(result.site_url) == "https://comicvine.gamespot.com/mutant/4030-1/"


def test_list_origins_empty(session: Comicvine) -> None:
    """Test the list_origins function with an invalid search query."""
    results = session.list_origins({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_origins_max_results(session: Comicvine) -> None:
    """Test the list_origins function with max results."""
    results = session.list_origins(max_results=3)
    assert len(results) == 3


def test_search_origin(session: Comicvine) -> None:
    """Test the search function for a list of Origins."""
    results = session.search(resource=ComicvineResource.ORIGIN, query="Mutant")
    assert all(isinstance(x, BasicOrigin) for x in results)
