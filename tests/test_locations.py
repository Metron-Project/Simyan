"""
The Locations test module.

This module contains tests for Location and LocationEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.location import LocationEntry


def test_location(session: Comicvine):
    """Test using the location endpoint with a valid location_id."""
    result = session.location(location_id=56000)
    assert result is not None
    assert result.location_id == 56000

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/location/4020-56000/"
    assert result.issue_count == 26
    assert result.date_added == datetime(2009, 1, 2, 16, 16, 18)
    assert result.first_issue.id_ == 149271
    assert len(result.issues) == 26
    assert result.name == "Odym"
    assert result.site_url == "https://comicvine.gamespot.com/odym/4020-56000/"
    assert len(result.story_arcs) == 0
    assert len(result.volumes) == 1


def test_location_fail(session: Comicvine):
    """Test using the location endpoint with an invalid location_id."""
    with pytest.raises(ServiceError):
        session.location(location_id=-1)


def test_location_list(session: Comicvine):
    """Test using the location_list endpoint with a valid search."""
    search_results = session.location_list({"filter": "name:Odym"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.location_id == 56000][0]
    assert result is not None

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/location/4020-56000/"
    assert result.issue_count == 26
    assert result.date_added == datetime(2009, 1, 2, 16, 16, 18)
    assert result.first_issue.id_ == 149271
    assert result.name == "Odym"
    assert result.site_url == "https://comicvine.gamespot.com/odym/4020-56000/"


def test_location_list_empty(session: Comicvine):
    """Test using the location_list endpoint with an invalid search."""
    results = session.location_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_location_list_max_results(session: Comicvine):
    """Test location_list endpoint with max_results."""
    results = session.location_list({"filter": "name:Earth"}, max_results=10)
    assert len(results) == 10


def test_search_location(session: Comicvine):
    """Test using the search endpoint for a list of Locations."""
    results = session.search(resource=ComicvineResource.LOCATION, query="Earth")
    assert all(isinstance(x, LocationEntry) for x in results)


def test_search_location_max_results(session: Comicvine):
    """Test search endpoint with max_results."""
    results = session.search(resource=ComicvineResource.LOCATION, query="Earth", max_results=10)
    assert all(isinstance(x, LocationEntry) for x in results)
    assert len(results) == 10
