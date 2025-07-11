"""The Publishers test module.

This module contains tests for Publisher and BasicPublisher objects.
"""

from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.publisher import BasicPublisher


def test_get_publisher(session: Comicvine) -> None:
    """Test the get_publisher function with a valid id."""
    result = session.get_publisher(publisher_id=364)
    assert result is not None
    assert result.id == 364

    assert len(result.characters) == 775
    assert len(result.story_arcs) == 38
    assert len(result.teams) == 42
    assert len(result.volumes) == 4693


def test_get_publisher_fail(session: Comicvine) -> None:
    """Test the get_publisher function with an invalid publisher_id."""
    with pytest.raises(ServiceError):
        session.get_publisher(publisher_id=-1)


def test_list_publishers(session: Comicvine) -> None:
    """Test the list_publishers function with a valid search."""
    search_results = session.list_publishers({"filter": "name:DC Comics"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 10)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/publisher/4010-10/"
    assert result.date_added == datetime(2008, 6, 6, 11, 8)
    assert result.location_address == "4000 Warner Blvd"
    assert result.location_city == "Burbank"
    assert result.location_state == "California"
    assert result.name == "DC Comics"
    assert str(result.site_url) == "https://comicvine.gamespot.com/dc-comics/4010-10/"


def test_list_publishers_empty(session: Comicvine) -> None:
    """Test the list_publishers function with an invalid search."""
    results = session.list_publishers({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_publishers_max_results(session: Comicvine) -> None:
    """Test the list_publishers function with max_results."""
    results = session.list_publishers(max_results=10)
    assert len(results) == 10


def test_search_publisher(session: Comicvine) -> None:
    """Test the search function for a list of Publishers."""
    results = session.search(resource=ComicvineResource.PUBLISHER, query="DC")
    assert all(isinstance(x, BasicPublisher) for x in results)
