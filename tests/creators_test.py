"""The Creators test module.

This module contains tests for Creator and BasicCreator objects.
"""

from datetime import date, datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.creator import BasicCreator


def test_get_creator(session: Comicvine) -> None:
    """Test the get_creator function with a valid id."""
    result = session.get_creator(creator_id=40439)
    assert result is not None
    assert result.id == 40439

    assert len(result.characters) == 320
    assert len(result.issues) == 1640
    assert len(result.story_arcs) == 27
    assert len(result.volumes) == 604


def test_get_creator_fail(session: Comicvine) -> None:
    """Test the get_creator function with an invalid id."""
    with pytest.raises(ServiceError):
        session.get_creator(creator_id=-1)


def test_list_creators(session: Comicvine) -> None:
    """Test the list_creators function with a valid search."""
    search_results = session.list_creators({"filter": "name:Geoff Johns"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 40439)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/person/4040-40439/"
    assert result.country == "United States"
    assert result.date_added == datetime(2008, 6, 6, 11, 28, 14)
    assert result.date_of_birth == date(1973, 1, 25)
    assert result.date_of_death is None
    assert result.email is None
    assert result.gender == 1
    assert result.hometown == "Detroit, MI"
    assert result.issue_count is None
    assert result.name == "Geoff Johns"
    assert str(result.site_url) == "https://comicvine.gamespot.com/geoff-johns/4040-40439/"
    assert str(result.website) == "http://www.geoffjohns.com/"


def test_list_creators_empty(session: Comicvine) -> None:
    """Test the list_creators function with an invalid search."""
    results = session.list_creators({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_creators_max_results(session: Comicvine) -> None:
    """Test the list_creators function with max_results."""
    results = session.list_creators(max_results=10)
    assert len(results) == 10


def test_search_creator(session: Comicvine) -> None:
    """Test the search function for a list of Creators."""
    results = session.search(resource=ComicvineResource.CREATOR, query="Geoff")
    assert all(isinstance(x, BasicCreator) for x in results)
