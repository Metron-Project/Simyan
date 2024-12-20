"""The Volumes test module.

This module contains tests for Volume and BasicVolume objects.
"""

from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.volume import BasicVolume


def test_get_volume(session: Comicvine) -> None:
    """Test the get_volume function with a valid id."""
    result = session.get_volume(volume_id=18216)
    assert result is not None
    assert result.id == 18216

    assert len(result.characters) == 368
    assert len(result.concepts) == 19
    assert len(result.creators) == 95
    assert len(result.issues) == 67
    assert len(result.locations) == 48
    assert len(result.objects) == 368


def test_get_volume_fail(session: Comicvine) -> None:
    """Test the get_volume function with an invalid id."""
    with pytest.raises(ServiceError):
        session.get_volume(volume_id=-1)


def test_list_volumes(session: Comicvine) -> None:
    """Test the list_volumes function with a valid search."""
    search_results = session.list_volumes({"filter": "name:Green Lantern"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 18216)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/volume/4050-18216/"
    assert result.date_added == datetime(2008, 6, 6, 11, 8, 33)
    assert result.first_issue.id == 111265
    assert result.issue_count == 67
    assert result.last_issue.id == 278617
    assert result.name == "Green Lantern"
    assert result.publisher.id == 10
    assert str(result.site_url) == "https://comicvine.gamespot.com/green-lantern/4050-18216/"
    assert result.start_year == 2005


def test_list_volumes_empty(session: Comicvine) -> None:
    """Test the list_volumes function with an invalid search."""
    results = session.list_volumes({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_volumes_max_results(session: Comicvine) -> None:
    """Test the list_volumes function with max_results."""
    results = session.list_volumes(max_results=10)
    assert len(results) == 10


def test_search_volume(session: Comicvine) -> None:
    """Test the search function for a list of Volumes."""
    results = session.search(resource=ComicvineResource.VOLUME, query="Lantern")
    assert all(isinstance(x, BasicVolume) for x in results)
