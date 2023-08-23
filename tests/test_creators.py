"""The Creators test module.

This module contains tests for Creator and CreatorEntry objects.
"""
from datetime import date, datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.creator import CreatorEntry


def test_creator(session: Comicvine) -> None:
    """Test using the creator endpoint with a valid creator_id."""
    result = session.get_creator(creator_id=40439)
    assert result is not None
    assert result.id == 40439

    assert result.api_url == "https://comicvine.gamespot.com/api/person/4040-40439/"
    assert len(result.characters) == 271
    assert result.country == "United States"
    assert result.date_added.astimezone() == datetime(2008, 6, 6, 11, 28, 14).astimezone()
    assert result.date_of_birth == date(1973, 1, 25)
    assert result.date_of_death is None
    assert result.email is None
    assert result.gender == 1
    assert result.hometown == "Detroit, MI"
    assert result.issue_count is None
    assert len(result.issues) == 1547
    assert result.name == "Geoff Johns"
    assert result.site_url == "https://comicvine.gamespot.com/geoff-johns/4040-40439/"
    assert len(result.story_arcs) == 0
    assert len(result.volumes) == 577
    assert result.website == "http://www.geoffjohns.com"


def test_creator_fail(session: Comicvine) -> None:
    """Test using the creator endpoint with an invalid creator_id."""
    with pytest.raises(ServiceError):
        session.get_creator(creator_id=-1)


def test_creator_list(session: Comicvine) -> None:
    """Test using the creator_list endpoint with a valid search."""
    search_results = session.list_creators({"filter": "name:Geoff Johns"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 40439)
    assert result is not None

    assert result.api_url == "https://comicvine.gamespot.com/api/person/4040-40439/"
    assert result.country == "United States"
    assert result.date_added.astimezone() == datetime(2008, 6, 6, 11, 28, 14).astimezone()
    assert result.date_of_birth == date(1973, 1, 25)
    assert result.date_of_death is None
    assert result.email is None
    assert result.gender == 1
    assert result.hometown == "Detroit, MI"
    assert result.issue_count is None
    assert result.name == "Geoff Johns"
    assert result.site_url == "https://comicvine.gamespot.com/geoff-johns/4040-40439/"
    assert result.website == "http://www.geoffjohns.com"


def test_creator_list_empty(session: Comicvine) -> None:
    """Test using the creator_list endpoint with an invalid search."""
    results = session.list_creators({"filter": "name:INVALID"})
    assert len(results) == 0


def test_creator_list_max_results(session: Comicvine) -> None:
    """Test creator_list endpoint with max_results."""
    results = session.list_creators({"filter": "name:Geoff"}, max_results=10)
    assert len(results) == 10


def test_search_creator(session: Comicvine) -> None:
    """Test using the search endpoint for a list of Creators."""
    results = session.search(resource=ComicvineResource.CREATOR, query="Geoff")
    assert all(isinstance(x, CreatorEntry) for x in results)


def test_search_creator_max_results(session: Comicvine) -> None:
    """Test search endpoint with max_results."""
    results = session.search(resource=ComicvineResource.CREATOR, query="Geoff", max_results=10)
    assert all(isinstance(x, CreatorEntry) for x in results)
    assert len(results) == 10


def test_creator_with_dob(session: Comicvine) -> None:
    """Test creators date of birth & death."""
    kirby = session.get_creator(creator_id=5614)
    assert kirby.date_of_birth == date(1917, 8, 28)
    assert kirby.date_of_death == date(1994, 2, 6)
