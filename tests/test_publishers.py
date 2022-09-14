"""
The Publishers test module.

This module contains tests for Publisher and PublisherEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.publisher import PublisherEntry


def test_publisher(session: Comicvine):
    """Test using the publisher endpoint with a valid publisher_id."""
    result = session.publisher(publisher_id=10)
    assert result is not None
    assert result.publisher_id == 10

    assert result.alias_list == [
        "National Comics",
        "Detective Comics Inc.",
        "National Periodical Publications",
        "National Allied Publications",
        "Nicholson Publishing",
        "All-American Publications",
        "DC Entertainment",
        "DC Nation",
        "Johnny DC",
        "National Comics Publishing",
        "National Comics Publications",
    ]
    assert result.api_url == "https://comicvine.gamespot.com/api/publisher/4010-10/"
    assert len(result.characters) == 19641
    assert result.date_added == datetime(2008, 6, 6, 11, 8)
    assert result.location_address == "4000 Warner Blvd"
    assert result.location_city == "Burbank"
    assert result.location_state == "California"
    assert result.name == "DC Comics"
    assert result.site_url == "https://comicvine.gamespot.com/dc-comics/4010-10/"
    assert len(result.story_arcs) == 1281
    assert len(result.teams) == 1530
    assert len(result.volumes) == 7105


def test_publisher_fail(session: Comicvine):
    """Test using the publisher endpoint with an invalid publisher_id."""
    with pytest.raises(ServiceError):
        session.publisher(publisher_id=-1)


def test_publisher_list(session: Comicvine):
    """Test using the publisher_list endpoint with a valid search."""
    search_results = session.publisher_list({"filter": "name:DC Comics"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.publisher_id == 10][0]
    assert result is not None

    assert result.alias_list == [
        "National Comics",
        "Detective Comics Inc.",
        "National Periodical Publications",
        "National Allied Publications",
        "Nicholson Publishing",
        "All-American Publications",
        "DC Entertainment",
        "DC Nation",
        "Johnny DC",
        "National Comics Publishing",
        "National Comics Publications",
    ]
    assert result.api_url == "https://comicvine.gamespot.com/api/publisher/4010-10/"
    assert result.date_added == datetime(2008, 6, 6, 11, 8)
    assert result.location_address == "4000 Warner Blvd"
    assert result.location_city == "Burbank"
    assert result.location_state == "California"
    assert result.name == "DC Comics"
    assert result.site_url == "https://comicvine.gamespot.com/dc-comics/4010-10/"


def test_publisher_list_empty(session: Comicvine):
    """Test using the publisher_list endpoint with an invalid search."""
    results = session.publisher_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_publisher_list_max_results(session: Comicvine):
    """Test publisher_list endpoint with max_results."""
    results = session.publisher_list({"filter": "name:Comics"}, max_results=10)
    assert len(results) == 10


def test_search_publisher(session: Comicvine):
    """Test using the search endpoint for a list of Publishers."""
    results = session.search(resource=ComicvineResource.PUBLISHER, query="DC")
    assert all(isinstance(x, PublisherEntry) for x in results)


def test_search_publisher_max_results(session: Comicvine):
    """Test search endpoint with max_results."""
    results = session.search(resource=ComicvineResource.PUBLISHER, query="DC", max_results=10)
    assert all(isinstance(x, PublisherEntry) for x in results)
    assert len(results) == 0
